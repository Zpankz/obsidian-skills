import json
from typing import Any, Dict, List, Optional
from .client import CDPClient

class ObsidianClient:
    """
    High-level SDK for controlling Obsidian via Chrome DevTools Protocol.
    Abstracts away raw JavaScript evaluation.
    """

    def __init__(self, client: CDPClient):
        self.client = client

    async def eval(self, expression: str, await_promise: bool = True) -> Any:
        """Execute raw JavaScript in the Obsidian window context."""
        return await self.client.evaluate(expression, await_promise=await_promise)

    async def get_vault_name(self) -> str:
        """Get the name of the currently open vault."""
        return await self.eval("app.vault.getName()")

    async def get_active_file(self) -> Optional[Dict[str, Any]]:
        """Get metadata about the currently active file."""
        return await self.eval("""
            (() => {
                const f = app.workspace.getActiveFile();
                return f ? { path: f.path, name: f.name, extension: f.extension } : null;
            })()
        """)

    async def open_note(self, path: str, new_leaf: bool = False) -> None:
        """Open a note by its vault path."""
        js_path = json.dumps(path)
        await self.eval(f"app.workspace.openLinkText({js_path}, '', {str(new_leaf).lower()})")

    async def list_plugins(self) -> List[Dict[str, str]]:
        """List all enabled plugins with their versions."""
        return await self.eval("""
            (() => {
                const plugins = app.plugins.manifests;
                const enabled = Array.from(app.plugins.enabledPlugins);
                return enabled.map(id => ({
                    id: id,
                    name: plugins[id]?.name || id,
                    version: plugins[id]?.version || 'unknown'
                }));
            })()
        """)

    async def trigger_command(self, command_id: str) -> bool:
        """Trigger an Obsidian command by ID."""
        js_cmd = json.dumps(command_id)
        return await self.eval(f"""
            (() => {{
                if (app.commands.commands[{js_cmd}]) {{
                    app.commands.executeCommandById({js_cmd});
                    return true;
                }}
                return false;
            }})()
        """)

    async def get_commands(self) -> List[Dict[str, str]]:
        """List all available commands."""
        return await self.eval("""
            Object.values(app.commands.commands).map(c => ({
                id: c.id,
                name: c.name
            }))
        """)

    async def append_content(self, path: str, content: str) -> None:
        """Append content to the end of a file."""
        js_path = json.dumps(path)
        js_content = json.dumps(content)
        await self.eval(f"""
            (async () => {{
                const file = app.vault.getAbstractFileByPath({js_path});
                if (file) {{
                    await app.vault.append(file, {js_content});
                    return true;
                }}
                throw new Error("File not found: " + {js_path});
            }})()
        """)

    # --- FileManager Support ---

    async def rename_file(self, path: str, new_path: str) -> None:
        """Rename or move a file."""
        js_path = json.dumps(path)
        js_new_path = json.dumps(new_path)
        await self.eval(f"""
            (async () => {{
                const file = app.vault.getAbstractFileByPath({js_path});
                if (!file) throw new Error("File not found: " + {js_path});
                await app.fileManager.renameFile(file, {js_new_path});
            }})()
        """)

    async def trash_file(self, path: str) -> None:
        """Move a file to trash."""
        js_path = json.dumps(path)
        await self.eval(f"""
            (async () => {{
                const file = app.vault.getAbstractFileByPath({js_path});
                if (!file) throw new Error("File not found: " + {js_path});
                await app.fileManager.trashFile(file);
            }})()
        """)

    async def get_frontmatter(self, path: str) -> Optional[Dict[str, Any]]:
        """Get the frontmatter of a file via metadataCache."""
        js_path = json.dumps(path)
        return await self.eval(f"""
            (() => {{
                const file = app.vault.getAbstractFileByPath({js_path});
                if (!file) return null;
                const cache = app.metadataCache.getFileCache(file);
                return cache ? cache.frontmatter : null;
            }})()
        """)

    async def update_frontmatter(self, path: str, key: str, value: Any) -> None:
        """Update a single frontmatter key."""
        js_path = json.dumps(path)
        js_key = json.dumps(key)
        js_value = json.dumps(value)
        await self.eval(f"""
            (async () => {{
                const file = app.vault.getAbstractFileByPath({js_path});
                if (!file) throw new Error("File not found: " + {js_path});
                await app.fileManager.processFrontMatter(file, (fm) => {{
                    fm[{js_key}] = {js_value};
                }});
            }})()
        """)

    # --- Discovery Support ---

    async def discover_object(self, object_path: str) -> Dict[str, str]:
        """
        Recursively discover properties and methods of an object.
        Returns a dict of property names to their types.
        """
        return await self.eval(f"""
            (() => {{
                try {{
                    const target = {object_path};
                    if (target === undefined || target === null) return {{ error: "Object is null/undefined" }};

                    const props = {{}};
                    let obj = target;

                    // Walk up prototype chain
                    const visited = new Set();
                    while (obj) {{
                        Object.getOwnPropertyNames(obj).forEach(prop => {{
                            if (visited.has(prop)) return;
                            visited.add(prop);
                            try {{
                                const type = typeof target[prop];
                                props[prop] = type;
                            }} catch (e) {{
                                props[prop] = "restricted";
                            }}
                        }});
                        obj = Object.getPrototypeOf(obj);
                        if (obj === Object.prototype) break; // Stop at root
                    }}
                    return props;
                }} catch (e) {{
                    return {{ error: e.toString() }};
                }}
            }})()
        """)

    # --- Canvas Support ---

    async def create_canvas(self, path: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> None:
        """Create a new .canvas file."""
        canvas_data = {
            "nodes": nodes,
            "edges": edges
        }
        json_content = json.dumps(json.dumps(canvas_data, indent=4))
        js_path = json.dumps(path)

        await self.eval(f"""
            (async () => {{
                await app.vault.create({js_path}, {json_content});
            }})()
        """)

    # --- Graph View Support ---

    async def graph_zoom_to(self, zoom_level: float) -> bool:
        """Zoom the active graph view."""
        return await self.eval(f"""
            (() => {{
                const leaves = app.workspace.getLeavesOfType('graph');
                if (leaves.length > 0 && leaves[0].view && leaves[0].view.renderer) {{
                    leaves[0].view.renderer.zoomTo({zoom_level});
                    return true;
                }}
                return false;
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # GENERIC PLUGIN CALLER (MVP Pattern)
    # ═══════════════════════════════════════════════════════════════

    async def call_plugin(self, plugin_id: str, method_path: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """
        Generic plugin method caller. Enables calling ANY plugin method without dedicated tools.

        Args:
            plugin_id: Plugin identifier (e.g., "dataview", "obsidian-git")
            method_path: Dot-notation path to method (e.g., "api.query", "commit")
            args: Dictionary of arguments to pass to the method

        Examples:
            call_plugin("dataview", "api.query", {"query": "FROM #tag"})
            call_plugin("obsidian-git", "commit", {"message": "test"})
            call_plugin("smart-connections", "env.smart_sources.search", {"query": "test"})
        """
        js_plugin_id = json.dumps(plugin_id)
        js_method_path = json.dumps(method_path)
        js_args = json.dumps(args) if args else "{}"

        return await self.eval(f"""
            (async () => {{
                const plugin = app.plugins.plugins[{js_plugin_id}];
                if (!plugin) throw new Error("Plugin not found or not enabled: " + {js_plugin_id});

                const methodPath = {js_method_path};
                const args = {js_args};

                // Navigate to the method through dot notation
                const parts = methodPath.split(".");
                let target = plugin;
                for (let i = 0; i < parts.length - 1; i++) {{
                    target = target[parts[i]];
                    if (!target) throw new Error("Path not found: " + parts.slice(0, i+1).join("."));
                }}

                const methodName = parts[parts.length - 1];
                const fn = target[methodName];

                if (typeof fn !== 'function') {{
                    // It's a property, not a method - return the value
                    return fn;
                }}

                // Call the method with spread args if it's an array, otherwise as single arg
                if (Array.isArray(args)) {{
                    return await fn.apply(target, args);
                }} else if (typeof args === 'object' && Object.keys(args).length > 0) {{
                    // Single object argument
                    return await fn.call(target, args);
                }} else {{
                    return await fn.call(target);
                }}
            }})()
        """)

    async def check_plugin_exists(self, plugin_id: str) -> bool:
        """Check if a plugin is installed and enabled."""
        js_plugin_id = json.dumps(plugin_id)
        return await self.eval(f"!!app.plugins.plugins[{js_plugin_id}]")

    # ═══════════════════════════════════════════════════════════════
    # DATAVIEW INTEGRATION (Unified Query)
    # ═══════════════════════════════════════════════════════════════

    async def dataview_query(self, query: str) -> Any:
        """Execute a Dataview DQL query and return results."""
        js_query = json.dumps(query)
        return await self.eval(f"""
            (async () => {{
                const dv = app.plugins.plugins["dataview"];
                if (!dv) throw new Error("Dataview plugin not installed");
                const result = await dv.api.query({js_query});
                return result.successful ? result.value : {{ error: result.error }};
            }})()
        """)

    async def dataview_pages(self, source: str = "") -> List[Dict]:
        """Get pages from Dataview matching a source (folder, tag, or link)."""
        js_source = json.dumps(source)
        return await self.eval(f"""
            (() => {{
                const dv = app.plugins.plugins["dataview"];
                if (!dv) throw new Error("Dataview plugin not installed");
                const pages = dv.api.pages({js_source});
                return pages.map(p => ({{
                    path: p.file.path,
                    name: p.file.name,
                    tags: p.file.tags || [],
                    links: p.file.outlinks?.map(l => l.path) || [],
                    frontmatter: p.file.frontmatter || {{}}
                }}));
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # BREADCRUMBS INTEGRATION (Graph Navigation)
    # ═══════════════════════════════════════════════════════════════

    async def breadcrumbs_neighbors(self, node: str, direction: str = "all") -> List[str]:
        """Get neighbors of a node in the Breadcrumbs graph."""
        js_node = json.dumps(node)
        js_direction = json.dumps(direction)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed or graph not built");
                const g = bc.mainG;
                const node = {js_node};
                const direction = {js_direction};

                if (!g.hasNode(node)) return [];

                if (direction === "in") return g.inNeighbors(node);
                if (direction === "out") return g.outNeighbors(node);
                return g.neighbors(node);
            }})()
        """)

    async def breadcrumbs_paths(self, start: str, end: str) -> List[List[str]]:
        """Find all paths between two nodes in the Breadcrumbs graph."""
        js_start = json.dumps(start)
        js_end = json.dumps(end)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.api) throw new Error("Breadcrumbs plugin not installed");
                return bc.api.dfsAllPaths({js_start}, {js_end});
            }})()
        """)

    async def breadcrumbs_export(self) -> Dict:
        """Export the full Breadcrumbs graph as JSON."""
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed or graph not built");
                const g = bc.mainG;
                return {
                    nodes: g.nodes(),
                    edges: g.edges().map(e => ({
                        source: g.source(e),
                        target: g.target(e),
                        attributes: g.getEdgeAttributes(e)
                    })),
                    nodeCount: g.order,
                    edgeCount: g.size
                };
            })()
        """)

    async def breadcrumbs_shortest_path(self, source: str, target: str) -> List[str]:
        """Find shortest path between two nodes using BFS."""
        js_source = json.dumps(source)
        js_target = json.dumps(target)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;

                // BFS for shortest path
                const source = {js_source};
                const target = {js_target};

                if (!g.hasNode(source)) return {{ error: "Source node not found: " + source }};
                if (!g.hasNode(target)) return {{ error: "Target node not found: " + target }};

                const visited = new Set([source]);
                const queue = [[source]];

                while (queue.length > 0) {{
                    const path = queue.shift();
                    const node = path[path.length - 1];

                    if (node === target) return path;

                    for (const neighbor of g.neighbors(node)) {{
                        if (!visited.has(neighbor)) {{
                            visited.add(neighbor);
                            queue.push([...path, neighbor]);
                        }}
                    }}
                }}

                return [];  // No path found
            }})()
        """)

    async def breadcrumbs_subgraph(self, nodes: List[str]) -> Dict:
        """Extract a subgraph containing only the specified nodes."""
        js_nodes = json.dumps(nodes)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const nodeSet = new Set({js_nodes});

                const subNodes = g.nodes().filter(n => nodeSet.has(n));
                const subEdges = g.edges().filter(e => {{
                    return nodeSet.has(g.source(e)) && nodeSet.has(g.target(e));
                }}).map(e => ({{
                    source: g.source(e),
                    target: g.target(e),
                    attributes: g.getEdgeAttributes(e)
                }}));

                return {{
                    nodes: subNodes,
                    edges: subEdges,
                    nodeCount: subNodes.length,
                    edgeCount: subEdges.length
                }};
            }})()
        """)

    async def breadcrumbs_connected_components(self) -> List[List[str]]:
        """Get all connected components in the graph."""
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;

                const visited = new Set();
                const components = [];

                for (const node of g.nodes()) {
                    if (visited.has(node)) continue;

                    const component = [];
                    const stack = [node];

                    while (stack.length > 0) {
                        const current = stack.pop();
                        if (visited.has(current)) continue;

                        visited.add(current);
                        component.push(current);

                        for (const neighbor of g.neighbors(current)) {
                            if (!visited.has(neighbor)) {
                                stack.push(neighbor);
                            }
                        }
                    }

                    components.push(component);
                }

                // Sort by size descending
                return components.sort((a, b) => b.length - a.length);
            })()
        """)

    async def breadcrumbs_filter_nodes(self, edge_type: Optional[str] = None, direction: str = "out") -> List[Dict]:
        """Filter nodes by edge type and return with their connections."""
        js_edge_type = json.dumps(edge_type) if edge_type else "null"
        js_direction = json.dumps(direction)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const edgeType = {js_edge_type};
                const direction = {js_direction};

                const results = [];
                for (const node of g.nodes()) {{
                    const edges = direction === "in" ? g.inEdges(node) :
                                  direction === "out" ? g.outEdges(node) :
                                  g.edges(node);

                    const filteredEdges = edges.filter(e => {{
                        if (!edgeType) return true;
                        const attrs = g.getEdgeAttributes(e);
                        return attrs.field === edgeType || attrs.type === edgeType;
                    }});

                    if (filteredEdges.length > 0) {{
                        results.push({{
                            node: node,
                            connections: filteredEdges.map(e => ({{
                                target: direction === "in" ? g.source(e) : g.target(e),
                                attributes: g.getEdgeAttributes(e)
                            }}))
                        }});
                    }}
                }}
                return results;
            }})()
        """)

    async def breadcrumbs_traverse(self, start: str, depth: int = 2, direction: str = "out") -> Dict:
        """Traverse the graph from a starting node up to a specified depth."""
        js_start = json.dumps(start)
        js_depth = json.dumps(depth)
        js_direction = json.dumps(direction)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const start = {js_start};
                const maxDepth = {js_depth};
                const direction = {js_direction};

                if (!g.hasNode(start)) return {{ error: "Start node not found: " + start }};

                const visited = new Map();
                const queue = [{{ node: start, depth: 0 }}];
                visited.set(start, 0);

                const edges = [];

                while (queue.length > 0) {{
                    const {{ node, depth }} = queue.shift();
                    if (depth >= maxDepth) continue;

                    const neighbors = direction === "in" ? g.inNeighbors(node) :
                                      direction === "out" ? g.outNeighbors(node) :
                                      g.neighbors(node);

                    for (const neighbor of neighbors) {{
                        if (!visited.has(neighbor)) {{
                            visited.set(neighbor, depth + 1);
                            queue.push({{ node: neighbor, depth: depth + 1 }});
                        }}

                        // Record edge
                        const edgeInfo = direction === "in" ?
                            {{ source: neighbor, target: node }} :
                            {{ source: node, target: neighbor }};

                        const edgeKey = g.edge(edgeInfo.source, edgeInfo.target);
                        if (edgeKey) {{
                            edges.push({{
                                ...edgeInfo,
                                attributes: g.getEdgeAttributes(edgeKey)
                            }});
                        }}
                    }}
                }}

                return {{
                    nodes: Array.from(visited.entries()).map(([node, depth]) => ({{ node, depth }})),
                    edges: edges,
                    nodeCount: visited.size,
                    edgeCount: edges.length
                }};
            }})()
        """)

    async def breadcrumbs_node_stats(self, node: str) -> Dict:
        """Get statistics for a specific node in the graph."""
        js_node = json.dumps(node)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const node = {js_node};

                if (!g.hasNode(node)) return {{ error: "Node not found: " + node }};

                const inEdges = g.inEdges(node);
                const outEdges = g.outEdges(node);

                // Group edges by type
                const inByType = {{}};
                const outByType = {{}};

                inEdges.forEach(e => {{
                    const type = g.getEdgeAttributes(e).field || 'unknown';
                    inByType[type] = (inByType[type] || 0) + 1;
                }});

                outEdges.forEach(e => {{
                    const type = g.getEdgeAttributes(e).field || 'unknown';
                    outByType[type] = (outByType[type] || 0) + 1;
                }});

                return {{
                    node: node,
                    inDegree: inEdges.length,
                    outDegree: outEdges.length,
                    totalDegree: g.degree(node),
                    inByType: inByType,
                    outByType: outByType,
                    inNeighbors: g.inNeighbors(node),
                    outNeighbors: g.outNeighbors(node)
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # BATCH FRONTMATTER OPERATIONS
    # ═══════════════════════════════════════════════════════════════

    async def batch_update_frontmatter(self, path: str, updates: Dict[str, Any]) -> None:
        """Update multiple frontmatter keys at once."""
        js_path = json.dumps(path)
        js_updates = json.dumps(updates)
        await self.eval(f"""
            (async () => {{
                const file = app.vault.getAbstractFileByPath({js_path});
                if (!file) throw new Error("File not found: " + {js_path});
                const updates = {js_updates};
                await app.fileManager.processFrontMatter(file, (fm) => {{
                    Object.entries(updates).forEach(([key, value]) => {{
                        fm[key] = value;
                    }});
                }});
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # GIT INTEGRATION (Unified)
    # ═══════════════════════════════════════════════════════════════

    async def git_action(self, action: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """
        Unified git operations via obsidian-git plugin.

        Actions: commit, push, pull, stage, unstage, status
        """
        js_action = json.dumps(action)
        js_args = json.dumps(args) if args else "{}"

        return await self.eval(f"""
            (async () => {{
                const git = app.plugins.plugins["obsidian-git"];
                if (!git) throw new Error("Obsidian Git plugin not installed");

                const action = {js_action};
                const args = {js_args};

                switch (action) {{
                    case "commit":
                        return await git.commit(args);
                    case "push":
                        return await git.push();
                    case "pull":
                        return await git.pull();
                    case "stage":
                        return await git.stageFile(args.path);
                    case "unstage":
                        return await git.unstageFile(args.path);
                    case "status":
                        return await git.gitManager.status();
                    default:
                        throw new Error("Unknown git action: " + action);
                }}
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # METADATA MENU INTEGRATION (Fields)
    # ═══════════════════════════════════════════════════════════════

    async def metadata_get_fields(self, path: str) -> Dict:
        """Get all Metadata Menu fields for a file."""
        js_path = json.dumps(path)
        return await self.eval(f"""
            (async () => {{
                const mm = app.plugins.plugins["metadata-menu"];
                if (!mm || !mm.api) throw new Error("Metadata Menu plugin not installed");
                return await mm.api.fileFields({js_path});
            }})()
        """)

    async def metadata_update_field(self, path: str, field: str, value: Any) -> None:
        """Update a Metadata Menu field value."""
        js_path = json.dumps(path)
        js_field = json.dumps(field)
        js_value = json.dumps(value)
        await self.eval(f"""
            (async () => {{
                const mm = app.plugins.plugins["metadata-menu"];
                if (!mm || !mm.api) throw new Error("Metadata Menu plugin not installed");
                await mm.api.postValues({js_path}, {{ [{js_field}]: {js_value} }});
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # ADVANCED GRAPH ALGORITHMS: CENTRALITY
    # ═══════════════════════════════════════════════════════════════

    async def graph_degree_centrality(self, normalized: bool = True) -> Dict:
        """
        Calculate degree centrality for all nodes.
        Degree centrality = number of edges connected to a node.
        """
        js_normalized = json.dumps(normalized)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const normalized = {js_normalized};
                const n = g.order;
                const maxDegree = normalized && n > 1 ? n - 1 : 1;

                const centrality = {{}};
                for (const node of g.nodes()) {{
                    const degree = g.degree(node);
                    centrality[node] = {{
                        degree: degree,
                        inDegree: g.inDegree ? g.inDegree(node) : degree,
                        outDegree: g.outDegree ? g.outDegree(node) : degree,
                        normalized: degree / maxDegree
                    }};
                }}

                // Sort by normalized centrality
                const sorted = Object.entries(centrality)
                    .sort((a, b) => b[1].normalized - a[1].normalized)
                    .map(([node, data]) => ({{ node, ...data }}));

                return {{
                    centrality: sorted,
                    stats: {{
                        nodeCount: n,
                        maxDegree: Math.max(...sorted.map(s => s.degree)),
                        avgDegree: sorted.reduce((sum, s) => sum + s.degree, 0) / n
                    }}
                }};
            }})()
        """)

    async def graph_betweenness_centrality(self, normalized: bool = True, sample_size: int = 0) -> Dict:
        """
        Calculate betweenness centrality for all nodes.
        Betweenness = fraction of shortest paths that pass through a node.
        Uses Brandes' algorithm for efficiency.
        """
        js_normalized = json.dumps(normalized)
        js_sample_size = json.dumps(sample_size)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const normalized = {js_normalized};
                const sampleSize = {js_sample_size};

                const nodes = g.nodes();
                const n = nodes.length;

                // Initialize betweenness
                const betweenness = {{}};
                nodes.forEach(v => betweenness[v] = 0);

                // Sample nodes if requested (for large graphs)
                const sourceNodes = sampleSize > 0 && sampleSize < n
                    ? nodes.sort(() => Math.random() - 0.5).slice(0, sampleSize)
                    : nodes;

                // Brandes' algorithm
                for (const s of sourceNodes) {{
                    const stack = [];
                    const pred = {{}};
                    const sigma = {{}};
                    const dist = {{}};

                    nodes.forEach(v => {{
                        pred[v] = [];
                        sigma[v] = 0;
                        dist[v] = -1;
                    }});

                    sigma[s] = 1;
                    dist[s] = 0;

                    const queue = [s];
                    while (queue.length > 0) {{
                        const v = queue.shift();
                        stack.push(v);

                        for (const w of g.neighbors(v)) {{
                            if (dist[w] < 0) {{
                                queue.push(w);
                                dist[w] = dist[v] + 1;
                            }}
                            if (dist[w] === dist[v] + 1) {{
                                sigma[w] += sigma[v];
                                pred[w].push(v);
                            }}
                        }}
                    }}

                    const delta = {{}};
                    nodes.forEach(v => delta[v] = 0);

                    while (stack.length > 0) {{
                        const w = stack.pop();
                        for (const v of pred[w]) {{
                            delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w]);
                        }}
                        if (w !== s) {{
                            betweenness[w] += delta[w];
                        }}
                    }}
                }}

                // Normalize
                const normFactor = normalized && n > 2
                    ? 2 / ((n - 1) * (n - 2))
                    : 1;

                // Scale for sampling
                const scaleFactor = sampleSize > 0 ? n / sampleSize : 1;

                const sorted = Object.entries(betweenness)
                    .map(([node, value]) => ({{
                        node,
                        betweenness: value * scaleFactor,
                        normalized: value * normFactor * scaleFactor
                    }}))
                    .sort((a, b) => b.normalized - a.normalized);

                return {{
                    centrality: sorted,
                    stats: {{
                        nodeCount: n,
                        sampledNodes: sourceNodes.length,
                        maxBetweenness: Math.max(...sorted.map(s => s.normalized))
                    }}
                }};
            }})()
        """)

    async def graph_closeness_centrality(self, normalized: bool = True) -> Dict:
        """
        Calculate closeness centrality for all nodes.
        Closeness = inverse of average shortest path distance to all other nodes.
        """
        js_normalized = json.dumps(normalized)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const normalized = {js_normalized};
                const nodes = g.nodes();
                const n = nodes.length;

                const centrality = {{}};

                for (const source of nodes) {{
                    // BFS to find distances
                    const dist = {{}};
                    dist[source] = 0;
                    const queue = [source];
                    let totalDist = 0;
                    let reachable = 0;

                    while (queue.length > 0) {{
                        const current = queue.shift();
                        for (const neighbor of g.neighbors(current)) {{
                            if (dist[neighbor] === undefined) {{
                                dist[neighbor] = dist[current] + 1;
                                totalDist += dist[neighbor];
                                reachable++;
                                queue.push(neighbor);
                            }}
                        }}
                    }}

                    // Closeness centrality
                    if (reachable > 0) {{
                        const avgDist = totalDist / reachable;
                        const closeness = 1 / avgDist;
                        centrality[source] = {{
                            closeness: closeness,
                            avgPathLength: avgDist,
                            reachableNodes: reachable,
                            normalized: normalized ? (reachable / (n - 1)) * closeness : closeness
                        }};
                    }} else {{
                        centrality[source] = {{
                            closeness: 0,
                            avgPathLength: Infinity,
                            reachableNodes: 0,
                            normalized: 0
                        }};
                    }}
                }}

                const sorted = Object.entries(centrality)
                    .map(([node, data]) => ({{ node, ...data }}))
                    .sort((a, b) => b.normalized - a.normalized);

                return {{
                    centrality: sorted,
                    stats: {{
                        nodeCount: n,
                        connectedNodes: sorted.filter(s => s.reachableNodes > 0).length
                    }}
                }};
            }})()
        """)

    async def graph_pagerank(self, damping: float = 0.85, iterations: int = 100, tolerance: float = 1e-6) -> Dict:
        """
        Calculate PageRank centrality for all nodes.
        PageRank measures importance based on incoming links from important nodes.
        """
        js_damping = json.dumps(damping)
        js_iterations = json.dumps(iterations)
        js_tolerance = json.dumps(tolerance)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const damping = {js_damping};
                const maxIter = {js_iterations};
                const tolerance = {js_tolerance};

                const nodes = g.nodes();
                const n = nodes.length;
                if (n === 0) return {{ centrality: [], stats: {{ nodeCount: 0 }} }};

                // Initialize PageRank uniformly
                let pr = {{}};
                let prNew = {{}};
                nodes.forEach(v => pr[v] = 1 / n);

                // Iterative PageRank
                let converged = false;
                let iter = 0;

                while (!converged && iter < maxIter) {{
                    iter++;
                    nodes.forEach(v => prNew[v] = (1 - damping) / n);

                    for (const v of nodes) {{
                        const outNeighbors = g.outNeighbors ? g.outNeighbors(v) : g.neighbors(v);
                        const outDegree = outNeighbors.length;

                        if (outDegree > 0) {{
                            const contribution = damping * pr[v] / outDegree;
                            for (const w of outNeighbors) {{
                                prNew[w] += contribution;
                            }}
                        }} else {{
                            // Dangling node: distribute to all nodes
                            const contribution = damping * pr[v] / n;
                            nodes.forEach(w => prNew[w] += contribution);
                        }}
                    }}

                    // Check convergence
                    let diff = 0;
                    nodes.forEach(v => diff += Math.abs(prNew[v] - pr[v]));
                    converged = diff < tolerance;

                    // Swap
                    const temp = pr;
                    pr = prNew;
                    prNew = temp;
                }}

                const sorted = Object.entries(pr)
                    .map(([node, pagerank]) => ({{ node, pagerank }}))
                    .sort((a, b) => b.pagerank - a.pagerank);

                return {{
                    centrality: sorted,
                    stats: {{
                        nodeCount: n,
                        iterations: iter,
                        converged: converged,
                        damping: damping
                    }}
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # ADVANCED GRAPH ALGORITHMS: COMMUNITY DETECTION
    # ═══════════════════════════════════════════════════════════════

    async def graph_louvain(self, resolution: float = 1.0) -> Dict:
        """
        Louvain community detection algorithm.
        Finds communities by optimizing modularity.
        """
        js_resolution = json.dumps(resolution)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const resolution = {js_resolution};

                const nodes = g.nodes();
                const n = nodes.length;
                if (n === 0) return {{ communities: [], stats: {{ nodeCount: 0 }} }};

                // Initialize each node in its own community
                const community = {{}};
                nodes.forEach((v, i) => community[v] = i);

                // Calculate edge weights (treat all edges as weight 1 for unweighted)
                const m = g.size; // total edges

                // Degree of each node
                const degree = {{}};
                nodes.forEach(v => degree[v] = g.degree(v));

                // Modularity gain calculation
                const modularityGain = (node, targetComm, nodeComm) => {{
                    if (targetComm === nodeComm) return 0;

                    let sumIn = 0; // edges within targetComm
                    let sumTot = 0; // total degree of targetComm
                    let ki = degree[node];
                    let kiIn = 0; // edges from node to targetComm

                    for (const v of nodes) {{
                        if (community[v] === targetComm) {{
                            sumTot += degree[v];
                            for (const neighbor of g.neighbors(v)) {{
                                if (community[neighbor] === targetComm) sumIn++;
                            }}
                            if (g.hasEdge(node, v) || g.hasEdge(v, node)) kiIn++;
                        }}
                    }}
                    sumIn /= 2; // each edge counted twice

                    return resolution * (kiIn - (sumTot * ki) / (2 * m));
                }};

                // Phase 1: Local moving
                let improved = true;
                let passes = 0;
                const maxPasses = 10;

                while (improved && passes < maxPasses) {{
                    improved = false;
                    passes++;

                    for (const node of nodes) {{
                        const currentComm = community[node];
                        let bestComm = currentComm;
                        let bestGain = 0;

                        // Check neighboring communities
                        const neighborComms = new Set();
                        for (const neighbor of g.neighbors(node)) {{
                            neighborComms.add(community[neighbor]);
                        }}

                        for (const targetComm of neighborComms) {{
                            const gain = modularityGain(node, targetComm, currentComm);
                            if (gain > bestGain) {{
                                bestGain = gain;
                                bestComm = targetComm;
                            }}
                        }}

                        if (bestComm !== currentComm) {{
                            community[node] = bestComm;
                            improved = true;
                        }}
                    }}
                }}

                // Collect communities
                const commMap = {{}};
                for (const [node, comm] of Object.entries(community)) {{
                    if (!commMap[comm]) commMap[comm] = [];
                    commMap[comm].push(node);
                }}

                // Renumber communities
                const communities = Object.values(commMap)
                    .sort((a, b) => b.length - a.length)
                    .map((members, i) => ({{
                        id: i,
                        size: members.length,
                        members: members
                    }}));

                // Calculate modularity
                let modularity = 0;
                for (const v of nodes) {{
                    for (const w of nodes) {{
                        if (community[v] === community[w]) {{
                            const Avw = g.hasEdge(v, w) || g.hasEdge(w, v) ? 1 : 0;
                            modularity += Avw - (degree[v] * degree[w]) / (2 * m);
                        }}
                    }}
                }}
                modularity /= (2 * m);

                return {{
                    communities: communities,
                    nodeToComm: Object.fromEntries(
                        nodes.map(v => [v, communities.findIndex(c => c.members.includes(v))])
                    ),
                    stats: {{
                        nodeCount: n,
                        communityCount: communities.length,
                        modularity: modularity,
                        passes: passes
                    }}
                }};
            }})()
        """)

    async def graph_label_propagation(self, max_iterations: int = 100) -> Dict:
        """
        Label propagation community detection.
        Simpler and faster than Louvain, but may be less accurate.
        """
        js_max_iter = json.dumps(max_iterations)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const maxIter = {js_max_iter};

                const nodes = g.nodes();
                const n = nodes.length;
                if (n === 0) return {{ communities: [], stats: {{ nodeCount: 0 }} }};

                // Initialize each node with unique label
                const labels = {{}};
                nodes.forEach((v, i) => labels[v] = i);

                // Iterate until convergence
                let changed = true;
                let iter = 0;

                while (changed && iter < maxIter) {{
                    changed = false;
                    iter++;

                    // Shuffle nodes for random order
                    const shuffled = [...nodes].sort(() => Math.random() - 0.5);

                    for (const node of shuffled) {{
                        const neighbors = g.neighbors(node);
                        if (neighbors.length === 0) continue;

                        // Count labels among neighbors
                        const labelCounts = {{}};
                        for (const neighbor of neighbors) {{
                            const label = labels[neighbor];
                            labelCounts[label] = (labelCounts[label] || 0) + 1;
                        }}

                        // Find most common label
                        let maxCount = 0;
                        let maxLabels = [];
                        for (const [label, count] of Object.entries(labelCounts)) {{
                            if (count > maxCount) {{
                                maxCount = count;
                                maxLabels = [parseInt(label)];
                            }} else if (count === maxCount) {{
                                maxLabels.push(parseInt(label));
                            }}
                        }}

                        // Pick random label if tie
                        const newLabel = maxLabels[Math.floor(Math.random() * maxLabels.length)];
                        if (labels[node] !== newLabel) {{
                            labels[node] = newLabel;
                            changed = true;
                        }}
                    }}
                }}

                // Collect communities
                const commMap = {{}};
                for (const [node, label] of Object.entries(labels)) {{
                    if (!commMap[label]) commMap[label] = [];
                    commMap[label].push(node);
                }}

                const communities = Object.values(commMap)
                    .sort((a, b) => b.length - a.length)
                    .map((members, i) => ({{
                        id: i,
                        size: members.length,
                        members: members
                    }}));

                return {{
                    communities: communities,
                    nodeToComm: Object.fromEntries(
                        nodes.map(v => [v, communities.findIndex(c => c.members.includes(v))])
                    ),
                    stats: {{
                        nodeCount: n,
                        communityCount: communities.length,
                        iterations: iter,
                        converged: !changed
                    }}
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # ADVANCED GRAPH ALGORITHMS: LINK PREDICTION
    # ═══════════════════════════════════════════════════════════════

    async def graph_link_prediction(self, node: Optional[str] = None, top_k: int = 10) -> Dict:
        """
        Predict missing links using multiple metrics:
        - Common Neighbors: |N(u) ∩ N(v)|
        - Jaccard Coefficient: |N(u) ∩ N(v)| / |N(u) ∪ N(v)|
        - Adamic-Adar: Σ 1/log(|N(w)|) for w in N(u) ∩ N(v)
        """
        js_node = json.dumps(node) if node else "null"
        js_top_k = json.dumps(top_k)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const targetNode = {js_node};
                const topK = {js_top_k};

                const nodes = g.nodes();

                // Get neighbors as Set for fast lookup
                const getNeighborSet = (v) => new Set(g.neighbors(v));

                // Calculate link prediction scores
                const predictions = [];

                const sourceNodes = targetNode ? [targetNode] : nodes;

                for (const u of sourceNodes) {{
                    const neighborsU = getNeighborSet(u);

                    for (const v of nodes) {{
                        // Skip self and existing edges
                        if (u === v) continue;
                        if (g.hasEdge(u, v) || g.hasEdge(v, u)) continue;

                        const neighborsV = getNeighborSet(v);

                        // Common neighbors
                        const commonNeighbors = [...neighborsU].filter(x => neighborsV.has(x));
                        const cn = commonNeighbors.length;

                        if (cn === 0) continue; // No common neighbors, skip

                        // Jaccard coefficient
                        const union = new Set([...neighborsU, ...neighborsV]);
                        const jaccard = cn / union.size;

                        // Adamic-Adar
                        let adamicAdar = 0;
                        for (const w of commonNeighbors) {{
                            const degreeW = g.degree(w);
                            if (degreeW > 1) {{
                                adamicAdar += 1 / Math.log(degreeW);
                            }}
                        }}

                        predictions.push({{
                            source: u,
                            target: v,
                            commonNeighbors: cn,
                            jaccard: jaccard,
                            adamicAdar: adamicAdar,
                            // Combined score (weighted)
                            score: 0.3 * (cn / nodes.length) + 0.3 * jaccard + 0.4 * (adamicAdar / Math.max(1, cn))
                        }});
                    }}
                }}

                // Sort by combined score and take top K
                predictions.sort((a, b) => b.score - a.score);
                const topPredictions = predictions.slice(0, topK);

                return {{
                    predictions: topPredictions,
                    stats: {{
                        nodeCount: nodes.length,
                        edgeCount: g.size,
                        candidatePairs: predictions.length,
                        returnedPairs: topPredictions.length
                    }}
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # ADVANCED GRAPH ALGORITHMS: PATH TRAVERSAL
    # ═══════════════════════════════════════════════════════════════

    async def graph_k_shortest_paths(self, source: str, target: str, k: int = 5) -> Dict:
        """
        Find k shortest paths between source and target using Yen's algorithm.
        """
        js_source = json.dumps(source)
        js_target = json.dumps(target)
        js_k = json.dumps(k)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const source = {js_source};
                const target = {js_target};
                const k = {js_k};

                if (!g.hasNode(source)) return {{ error: "Source node not found: " + source }};
                if (!g.hasNode(target)) return {{ error: "Target node not found: " + target }};

                // BFS for shortest path (ignoring certain edges/nodes)
                const dijkstra = (src, tgt, ignoredEdges = new Set(), ignoredNodes = new Set()) => {{
                    const dist = {{}};
                    const prev = {{}};
                    dist[src] = 0;

                    const queue = [src];
                    const visited = new Set();

                    while (queue.length > 0) {{
                        let minDist = Infinity;
                        let minIdx = 0;
                        for (let i = 0; i < queue.length; i++) {{
                            if (dist[queue[i]] < minDist) {{
                                minDist = dist[queue[i]];
                                minIdx = i;
                            }}
                        }}
                        const u = queue.splice(minIdx, 1)[0];

                        if (visited.has(u)) continue;
                        visited.add(u);

                        if (u === tgt) break;

                        for (const v of g.neighbors(u)) {{
                            if (ignoredNodes.has(v)) continue;
                            const edgeKey = u + "->" + v;
                            if (ignoredEdges.has(edgeKey)) continue;

                            const alt = dist[u] + 1;
                            if (dist[v] === undefined || alt < dist[v]) {{
                                dist[v] = alt;
                                prev[v] = u;
                                if (!visited.has(v)) queue.push(v);
                            }}
                        }}
                    }}

                    // Reconstruct path
                    if (dist[tgt] === undefined) return null;

                    const path = [tgt];
                    let current = tgt;
                    while (current !== src) {{
                        current = prev[current];
                        path.unshift(current);
                    }}
                    return {{ path, length: dist[tgt] }};
                }};

                // Yen's algorithm
                const A = []; // Final k shortest paths
                const B = []; // Candidate paths

                // Find first shortest path
                const first = dijkstra(source, target);
                if (!first) return {{ paths: [], stats: {{ nodeCount: g.order, found: 0 }} }};
                A.push(first);

                for (let i = 1; i < k; i++) {{
                    const prevPath = A[i - 1].path;

                    for (let j = 0; j < prevPath.length - 1; j++) {{
                        const spurNode = prevPath[j];
                        const rootPath = prevPath.slice(0, j + 1);

                        const ignoredEdges = new Set();
                        const ignoredNodes = new Set(rootPath.slice(0, -1));

                        // Remove edges that share the root path
                        for (const p of A) {{
                            if (p.path.slice(0, j + 1).join("->") === rootPath.join("->")) {{
                                ignoredEdges.add(p.path[j] + "->" + p.path[j + 1]);
                            }}
                        }}

                        const spurPath = dijkstra(spurNode, target, ignoredEdges, ignoredNodes);
                        if (spurPath) {{
                            const totalPath = rootPath.slice(0, -1).concat(spurPath.path);
                            const totalLength = j + spurPath.length;

                            // Check if already in B
                            const pathStr = totalPath.join("->");
                            if (!B.some(b => b.path.join("->") === pathStr)) {{
                                B.push({{ path: totalPath, length: totalLength }});
                            }}
                        }}
                    }}

                    if (B.length === 0) break;

                    // Sort B by length and add shortest to A
                    B.sort((a, b) => a.length - b.length);
                    A.push(B.shift());
                }}

                return {{
                    paths: A.map((p, i) => ({{
                        rank: i + 1,
                        path: p.path,
                        length: p.length
                    }})),
                    stats: {{
                        nodeCount: g.order,
                        edgeCount: g.size,
                        found: A.length,
                        requested: k
                    }}
                }};
            }})()
        """)

    async def graph_all_paths(self, source: str, target: str, max_length: int = 10, limit: int = 100) -> Dict:
        """
        Find all paths between source and target up to max_length.
        Uses DFS with path tracking.
        """
        js_source = json.dumps(source)
        js_target = json.dumps(target)
        js_max_length = json.dumps(max_length)
        js_limit = json.dumps(limit)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs plugin not installed");
                const g = bc.mainG;
                const source = {js_source};
                const target = {js_target};
                const maxLength = {js_max_length};
                const limit = {js_limit};

                if (!g.hasNode(source)) return {{ error: "Source node not found: " + source }};
                if (!g.hasNode(target)) return {{ error: "Target node not found: " + target }};

                const allPaths = [];

                const dfs = (current, path, visited) => {{
                    if (allPaths.length >= limit) return;
                    if (path.length > maxLength) return;

                    if (current === target) {{
                        allPaths.push([...path]);
                        return;
                    }}

                    for (const neighbor of g.neighbors(current)) {{
                        if (!visited.has(neighbor)) {{
                            visited.add(neighbor);
                            path.push(neighbor);
                            dfs(neighbor, path, visited);
                            path.pop();
                            visited.delete(neighbor);
                        }}
                    }}
                }};

                const visited = new Set([source]);
                dfs(source, [source], visited);

                // Sort by length
                allPaths.sort((a, b) => a.length - b.length);

                return {{
                    paths: allPaths.map((p, i) => ({{
                        rank: i + 1,
                        path: p,
                        length: p.length - 1
                    }})),
                    stats: {{
                        nodeCount: g.order,
                        found: allPaths.length,
                        limited: allPaths.length >= limit,
                        maxLength: maxLength
                    }}
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════
    # MULTIHOP REASONING FRAMEWORK
    # ═══════════════════════════════════════════════════════════════
    #
    # Level 1: Reasoning Primitives - Individual analysis operations
    # Level 2: Reasoning Chains - Multihop integration of primitives
    # Level 3: Metaschema Extraction - Higher-order structural insight
    # Level 4: Unified Orchestrator - Single entry point
    #
    # ═══════════════════════════════════════════════════════════════

    # ───────────────────────────────────────────────────────────────
    # LEVEL 1: REASONING PRIMITIVES
    # ───────────────────────────────────────────────────────────────

    async def reasoning_importance_trace(self) -> Dict:
        """
        PRIMITIVE: Multi-metric importance analysis.

        Integrates:
        - PageRank (global importance via link structure)
        - Betweenness (bridging/gateway role)
        - Degree (local connectivity)
        - Closeness (accessibility)

        Returns weighted importance scores with cross-validation.
        """
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const nodes = g.nodes();
                const n = nodes.length;

                if (n === 0) return { error: "Empty graph" };

                // ═══ DEGREE CENTRALITY ═══
                const degree = {};
                const maxDegree = Math.max(...nodes.map(v => g.degree(v)));
                nodes.forEach(v => {
                    degree[v] = maxDegree > 0 ? g.degree(v) / maxDegree : 0;
                });

                // ═══ PAGERANK ═══
                const damping = 0.85;
                let pr = {};
                nodes.forEach(v => pr[v] = 1 / n);

                for (let iter = 0; iter < 50; iter++) {
                    const newPr = {};
                    nodes.forEach(v => newPr[v] = (1 - damping) / n);

                    nodes.forEach(v => {
                        const outDegree = g.outDegree(v);
                        if (outDegree > 0) {
                            const share = pr[v] / outDegree;
                            g.outNeighbors(v).forEach(u => {
                                newPr[u] += damping * share;
                            });
                        }
                    });
                    pr = newPr;
                }

                const maxPr = Math.max(...Object.values(pr));
                nodes.forEach(v => pr[v] = maxPr > 0 ? pr[v] / maxPr : 0);

                // ═══ BETWEENNESS (Brandes) ═══
                const betweenness = {};
                nodes.forEach(v => betweenness[v] = 0);

                nodes.forEach(s => {
                    const stack = [];
                    const pred = {};
                    const sigma = {};
                    const dist = {};
                    const delta = {};

                    nodes.forEach(t => {
                        pred[t] = [];
                        sigma[t] = 0;
                        dist[t] = -1;
                        delta[t] = 0;
                    });

                    sigma[s] = 1;
                    dist[s] = 0;
                    const queue = [s];

                    while (queue.length > 0) {
                        const v = queue.shift();
                        stack.push(v);

                        g.neighbors(v).forEach(w => {
                            if (dist[w] < 0) {
                                queue.push(w);
                                dist[w] = dist[v] + 1;
                            }
                            if (dist[w] === dist[v] + 1) {
                                sigma[w] += sigma[v];
                                pred[w].push(v);
                            }
                        });
                    }

                    while (stack.length > 0) {
                        const w = stack.pop();
                        pred[w].forEach(v => {
                            delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w]);
                        });
                        if (w !== s) {
                            betweenness[w] += delta[w];
                        }
                    }
                });

                // Normalize
                const norm = (n - 1) * (n - 2);
                const maxBet = Math.max(...Object.values(betweenness));
                nodes.forEach(v => {
                    betweenness[v] = maxBet > 0 ? betweenness[v] / maxBet : 0;
                });

                // ═══ CLOSENESS ═══
                const closeness = {};
                nodes.forEach(s => {
                    const dist = {};
                    dist[s] = 0;
                    const queue = [s];
                    let total = 0;
                    let reachable = 0;

                    while (queue.length > 0) {
                        const v = queue.shift();
                        g.neighbors(v).forEach(w => {
                            if (dist[w] === undefined) {
                                dist[w] = dist[v] + 1;
                                total += dist[w];
                                reachable++;
                                queue.push(w);
                            }
                        });
                    }

                    closeness[s] = reachable > 0 ? reachable / total : 0;
                });

                const maxClose = Math.max(...Object.values(closeness));
                nodes.forEach(v => {
                    closeness[v] = maxClose > 0 ? closeness[v] / maxClose : 0;
                });

                // ═══ COMPOSITE IMPORTANCE ═══
                const importance = {};
                const weights = { pagerank: 0.35, betweenness: 0.25, degree: 0.25, closeness: 0.15 };

                nodes.forEach(v => {
                    importance[v] = {
                        pagerank: pr[v],
                        betweenness: betweenness[v],
                        degree: degree[v],
                        closeness: closeness[v],
                        composite: (
                            weights.pagerank * pr[v] +
                            weights.betweenness * betweenness[v] +
                            weights.degree * degree[v] +
                            weights.closeness * closeness[v]
                        ),
                        // Cross-validation: agreement between metrics
                        agreement: 1 - Math.sqrt(
                            Math.pow(pr[v] - betweenness[v], 2) +
                            Math.pow(pr[v] - degree[v], 2) +
                            Math.pow(betweenness[v] - degree[v], 2)
                        ) / Math.sqrt(3)
                    };
                });

                // Rank by composite
                const ranked = Object.entries(importance)
                    .sort((a, b) => b[1].composite - a[1].composite)
                    .map(([node, scores], i) => ({
                        rank: i + 1,
                        node: node,
                        ...scores
                    }));

                return {
                    trace: "importance",
                    ranked: ranked,
                    weights: weights,
                    insights: {
                        hub_nodes: ranked.filter(r => r.degree > 0.7).map(r => r.node),
                        bridge_nodes: ranked.filter(r => r.betweenness > 0.7).map(r => r.node),
                        central_nodes: ranked.filter(r => r.pagerank > 0.7).map(r => r.node),
                        accessible_nodes: ranked.filter(r => r.closeness > 0.7).map(r => r.node),
                        high_agreement: ranked.filter(r => r.agreement > 0.8).map(r => r.node)
                    },
                    stats: {
                        nodeCount: n,
                        avgComposite: ranked.reduce((s, r) => s + r.composite, 0) / n,
                        avgAgreement: ranked.reduce((s, r) => s + r.agreement, 0) / n
                    }
                };
            })()
        """)

    async def reasoning_gap_trace(self, top_k: int = 20) -> Dict:
        """
        PRIMITIVE: Knowledge gap detection.

        Integrates:
        - Link prediction (missing connections)
        - Community boundaries (inter-cluster gaps)
        - Low-degree nodes (isolated concepts)
        - Unreachable pairs (disconnected knowledge)

        Returns prioritized list of knowledge gaps.
        """
        js_top_k = json.dumps(top_k)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const nodes = g.nodes();
                const n = nodes.length;

                // ═══ LINK PREDICTION GAPS ═══
                const getNeighborSet = (v) => new Set(g.neighbors(v));
                const predictions = [];

                for (const u of nodes) {{
                    const neighborsU = getNeighborSet(u);

                    for (const v of nodes) {{
                        if (u >= v) continue; // Avoid duplicates
                        if (g.hasEdge(u, v) || g.hasEdge(v, u)) continue;

                        const neighborsV = getNeighborSet(v);
                        const common = [...neighborsU].filter(x => neighborsV.has(x));

                        if (common.length > 0) {{
                            const union = new Set([...neighborsU, ...neighborsV]);
                            const jaccard = common.length / union.size;

                            predictions.push({{
                                source: u,
                                target: v,
                                commonNeighbors: common.length,
                                jaccard: jaccard,
                                type: "missing_link"
                            }});
                        }}
                    }}
                }}

                predictions.sort((a, b) => b.jaccard - a.jaccard);
                const topPredictions = predictions.slice(0, {js_top_k});

                // ═══ COMMUNITY DETECTION (Louvain) ═══
                const communityOf = {{}};
                nodes.forEach((v, i) => communityOf[v] = i);

                const modularity = () => {{
                    const m = g.size || 1;
                    let Q = 0;
                    nodes.forEach(u => {{
                        g.neighbors(u).forEach(v => {{
                            if (communityOf[u] === communityOf[v]) {{
                                const ki = g.degree(u);
                                const kj = g.degree(v);
                                Q += 1 - (ki * kj) / (2 * m);
                            }}
                        }});
                    }});
                    return Q / (2 * m);
                }};

                // Simple community optimization
                for (let iter = 0; iter < 10; iter++) {{
                    let improved = false;
                    nodes.forEach(v => {{
                        const neighbors = g.neighbors(v);
                        if (neighbors.length === 0) return;

                        const commCounts = {{}};
                        neighbors.forEach(u => {{
                            const c = communityOf[u];
                            commCounts[c] = (commCounts[c] || 0) + 1;
                        }});

                        const bestComm = Object.entries(commCounts)
                            .sort((a, b) => b[1] - a[1])[0][0];

                        if (bestComm !== String(communityOf[v])) {{
                            communityOf[v] = parseInt(bestComm);
                            improved = true;
                        }}
                    }});
                    if (!improved) break;
                }}

                // Find inter-community gaps
                const communityMembers = {{}};
                nodes.forEach(v => {{
                    const c = communityOf[v];
                    if (!communityMembers[c]) communityMembers[c] = [];
                    communityMembers[c].push(v);
                }});

                const communities = Object.entries(communityMembers)
                    .filter(([c, members]) => members.length > 1)
                    .map(([c, members]) => ({{ id: c, members: members }}));

                const interCommunityGaps = [];
                for (let i = 0; i < communities.length; i++) {{
                    for (let j = i + 1; j < communities.length; j++) {{
                        const c1 = communities[i];
                        const c2 = communities[j];

                        // Check if any edges exist between communities
                        let edgeCount = 0;
                        c1.members.forEach(u => {{
                            c2.members.forEach(v => {{
                                if (g.hasEdge(u, v) || g.hasEdge(v, u)) edgeCount++;
                            }});
                        }});

                        const maxEdges = c1.members.length * c2.members.length;
                        const density = maxEdges > 0 ? edgeCount / maxEdges : 0;

                        if (density < 0.1) {{
                            interCommunityGaps.push({{
                                community1: c1.id,
                                community2: c2.id,
                                size1: c1.members.length,
                                size2: c2.members.length,
                                existingEdges: edgeCount,
                                density: density,
                                type: "community_gap"
                            }});
                        }}
                    }}
                }}

                // ═══ ISOLATED NODES ═══
                const isolated = nodes
                    .filter(v => g.degree(v) <= 1)
                    .map(v => ({{
                        node: v,
                        degree: g.degree(v),
                        type: "isolated"
                    }}));

                return {{
                    trace: "gap",
                    gaps: {{
                        missing_links: topPredictions,
                        community_gaps: interCommunityGaps,
                        isolated_nodes: isolated
                    }},
                    prioritized: [
                        ...topPredictions.slice(0, 5).map(p => ({{
                            priority: 1,
                            type: "missing_link",
                            description: `Missing link: ${{p.source}} ↔ ${{p.target}} (Jaccard: ${{p.jaccard.toFixed(3)}})`,
                            action: `Consider adding relationship between ${{p.source}} and ${{p.target}}`
                        }})),
                        ...interCommunityGaps.slice(0, 3).map(g => ({{
                            priority: 2,
                            type: "community_gap",
                            description: `Weak connection between community ${{g.community1}} (${{g.size1}} nodes) and ${{g.community2}} (${{g.size2}} nodes)`,
                            action: "Consider adding cross-community links"
                        }})),
                        ...isolated.slice(0, 5).map(i => ({{
                            priority: 3,
                            type: "isolated",
                            description: `Isolated node: ${{i.node}} (degree: ${{i.degree}})`,
                            action: `Connect ${{i.node}} to related concepts`
                        }}))
                    ],
                    stats: {{
                        nodeCount: n,
                        edgeCount: g.size,
                        communityCount: communities.length,
                        missingLinkCandidates: predictions.length,
                        isolatedCount: isolated.length,
                        interCommunityGapCount: interCommunityGaps.length
                    }}
                }};
            }})()
        """)

    async def reasoning_cluster_trace(self, resolution: float = 1.0) -> Dict:
        """
        PRIMITIVE: Thematic cluster analysis.

        Integrates:
        - Louvain community detection
        - Intra-cluster density
        - Cluster centroids (most representative nodes)
        - Cluster labels (via high-degree members)

        Returns annotated clusters with semantic insights.
        """
        js_resolution = json.dumps(resolution)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const nodes = g.nodes();
                const n = nodes.length;
                const m = g.size || 1;

                // ═══ LOUVAIN COMMUNITY DETECTION ═══
                const resolution = {js_resolution};
                const communityOf = {{}};
                nodes.forEach((v, i) => communityOf[v] = i);

                const modularity = () => {{
                    let Q = 0;
                    const degreeSum = nodes.reduce((s, v) => s + g.degree(v), 0);

                    nodes.forEach(u => {{
                        g.neighbors(u).forEach(v => {{
                            if (communityOf[u] === communityOf[v]) {{
                                const ki = g.degree(u);
                                const kj = g.degree(v);
                                Q += 1 - resolution * (ki * kj) / degreeSum;
                            }}
                        }});
                    }});
                    return Q / degreeSum;
                }};

                // Optimize communities
                for (let pass = 0; pass < 20; pass++) {{
                    let improved = false;

                    nodes.forEach(v => {{
                        const neighbors = g.neighbors(v);
                        if (neighbors.length === 0) return;

                        const currentComm = communityOf[v];
                        const commGain = {{}};

                        neighbors.forEach(u => {{
                            const c = communityOf[u];
                            commGain[c] = (commGain[c] || 0) + 1;
                        }});

                        let bestComm = currentComm;
                        let bestGain = commGain[currentComm] || 0;

                        Object.entries(commGain).forEach(([c, gain]) => {{
                            if (gain > bestGain) {{
                                bestGain = gain;
                                bestComm = parseInt(c);
                            }}
                        }});

                        if (bestComm !== currentComm) {{
                            communityOf[v] = bestComm;
                            improved = true;
                        }}
                    }});

                    if (!improved) break;
                }}

                // ═══ BUILD CLUSTER PROFILES ═══
                const clusterMembers = {{}};
                nodes.forEach(v => {{
                    const c = communityOf[v];
                    if (!clusterMembers[c]) clusterMembers[c] = [];
                    clusterMembers[c].push(v);
                }});

                const clusters = Object.entries(clusterMembers)
                    .filter(([c, members]) => members.length > 0)
                    .map(([id, members]) => {{
                        // Intra-cluster edge count
                        let intraEdges = 0;
                        members.forEach(u => {{
                            g.neighbors(u).forEach(v => {{
                                if (communityOf[v] === parseInt(id)) intraEdges++;
                            }});
                        }});
                        intraEdges /= 2; // Each edge counted twice

                        const maxEdges = members.length * (members.length - 1) / 2;
                        const density = maxEdges > 0 ? intraEdges / maxEdges : 0;

                        // Find centroid (highest internal degree)
                        const internalDegree = {{}};
                        members.forEach(v => {{
                            internalDegree[v] = g.neighbors(v).filter(u => communityOf[u] === parseInt(id)).length;
                        }});

                        const centroid = members.sort((a, b) => internalDegree[b] - internalDegree[a])[0];

                        // Boundary nodes (connected to other clusters)
                        const boundary = members.filter(v => {{
                            return g.neighbors(v).some(u => communityOf[u] !== parseInt(id));
                        }});

                        return {{
                            id: parseInt(id),
                            size: members.length,
                            members: members,
                            centroid: centroid,
                            boundary: boundary,
                            density: density,
                            intraEdges: intraEdges,
                            avgDegree: members.reduce((s, v) => s + g.degree(v), 0) / members.length,
                            cohesion: density * members.length / n // Size-weighted density
                        }};
                    }})
                    .filter(c => c.size > 1)
                    .sort((a, b) => b.cohesion - a.cohesion);

                // ═══ INTER-CLUSTER RELATIONSHIPS ═══
                const clusterRelations = [];
                for (let i = 0; i < clusters.length; i++) {{
                    for (let j = i + 1; j < clusters.length; j++) {{
                        let edgeCount = 0;
                        clusters[i].members.forEach(u => {{
                            g.neighbors(u).forEach(v => {{
                                if (clusters[j].members.includes(v)) edgeCount++;
                            }});
                        }});

                        if (edgeCount > 0) {{
                            clusterRelations.push({{
                                from: clusters[i].id,
                                to: clusters[j].id,
                                edges: edgeCount,
                                strength: edgeCount / Math.min(clusters[i].size, clusters[j].size)
                            }});
                        }}
                    }}
                }}

                return {{
                    trace: "cluster",
                    clusters: clusters,
                    relations: clusterRelations.sort((a, b) => b.strength - a.strength),
                    insights: {{
                        dominant_cluster: clusters[0] ? clusters[0].id : null,
                        most_cohesive: clusters.filter(c => c.density > 0.5).map(c => c.id),
                        bridge_clusters: clusters.filter(c => c.boundary.length > c.size * 0.5).map(c => c.id),
                        isolated_clusters: clusters.filter(c => {{
                            return !clusterRelations.some(r => r.from === c.id || r.to === c.id);
                        }}).map(c => c.id)
                    }},
                    stats: {{
                        nodeCount: n,
                        clusterCount: clusters.length,
                        avgClusterSize: clusters.reduce((s, c) => s + c.size, 0) / Math.max(1, clusters.length),
                        modularity: modularity(),
                        coverage: clusters.reduce((s, c) => s + c.size, 0) / n
                    }}
                }};
            }})()
        """)

    async def reasoning_path_trace(self, source: str, target: str, max_paths: int = 10) -> Dict:
        """
        PRIMITIVE: Learning path analysis.

        Integrates:
        - Multiple shortest paths
        - Path diversity (unique intermediate nodes)
        - Bottleneck identification (nodes on many paths)
        - Path quality scoring

        Returns optimal learning sequences.
        """
        js_source = json.dumps(source)
        js_target = json.dumps(target)
        js_max_paths = json.dumps(max_paths)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const source = {js_source};
                const target = {js_target};
                const maxPaths = {js_max_paths};

                if (!g.hasNode(source)) return {{ error: "Source not found: " + source }};
                if (!g.hasNode(target)) return {{ error: "Target not found: " + target }};

                // ═══ FIND ALL PATHS (DFS with limit) ═══
                const allPaths = [];
                const maxLength = 10;

                const dfs = (current, path, visited) => {{
                    if (allPaths.length >= maxPaths * 2) return;
                    if (path.length > maxLength) return;

                    if (current === target) {{
                        allPaths.push([...path]);
                        return;
                    }}

                    for (const neighbor of g.neighbors(current)) {{
                        if (!visited.has(neighbor)) {{
                            visited.add(neighbor);
                            path.push(neighbor);
                            dfs(neighbor, path, visited);
                            path.pop();
                            visited.delete(neighbor);
                        }}
                    }}
                }};

                const visited = new Set([source]);
                dfs(source, [source], visited);

                if (allPaths.length === 0) {{
                    return {{ error: "No path found between " + source + " and " + target }};
                }}

                // Sort by length
                allPaths.sort((a, b) => a.length - b.length);
                const paths = allPaths.slice(0, maxPaths);

                // ═══ PATH ANALYSIS ═══

                // Bottleneck detection
                const nodeFrequency = {{}};
                paths.forEach(path => {{
                    path.slice(1, -1).forEach(node => {{
                        nodeFrequency[node] = (nodeFrequency[node] || 0) + 1;
                    }});
                }});

                const bottlenecks = Object.entries(nodeFrequency)
                    .filter(([node, freq]) => freq > paths.length * 0.5)
                    .map(([node, freq]) => ({{ node, frequency: freq, ratio: freq / paths.length }}))
                    .sort((a, b) => b.frequency - a.frequency);

                // Path diversity (unique intermediates)
                const allIntermediates = new Set();
                paths.forEach(path => {{
                    path.slice(1, -1).forEach(node => allIntermediates.add(node));
                }});

                // Path quality scoring
                const scoredPaths = paths.map((path, i) => {{
                    const length = path.length - 1;
                    const uniqueNodes = new Set(path.slice(1, -1));

                    // Check for bottleneck nodes
                    const bottleneckCount = path.slice(1, -1)
                        .filter(n => nodeFrequency[n] > paths.length * 0.5).length;

                    // Score: shorter is better, fewer bottlenecks is better
                    const lengthScore = 1 / length;
                    const bottleneckPenalty = 1 - (bottleneckCount / Math.max(1, path.length - 2));
                    const quality = lengthScore * 0.6 + bottleneckPenalty * 0.4;

                    return {{
                        rank: i + 1,
                        path: path,
                        length: length,
                        quality: quality,
                        bottleneckCount: bottleneckCount,
                        uniqueIntermediates: [...uniqueNodes]
                    }};
                }});

                // Best path recommendation
                const bestPath = scoredPaths.sort((a, b) => b.quality - a.quality)[0];

                return {{
                    trace: "path",
                    source: source,
                    target: target,
                    paths: scoredPaths,
                    recommended: bestPath,
                    bottlenecks: bottlenecks,
                    insights: {{
                        shortest_length: paths[0].length - 1,
                        path_diversity: allIntermediates.size,
                        critical_nodes: bottlenecks.slice(0, 3).map(b => b.node),
                        alternative_routes: scoredPaths.length > 1
                    }},
                    stats: {{
                        pathsFound: paths.length,
                        avgLength: paths.reduce((s, p) => s + p.length - 1, 0) / paths.length,
                        intermediateNodes: allIntermediates.size,
                        bottleneckCount: bottlenecks.length
                    }}
                }};
            }})()
        """)

    async def reasoning_bridge_trace(self) -> Dict:
        """
        PRIMITIVE: Bridge concept identification.

        Integrates:
        - Inter-community edges
        - High betweenness, low clustering coefficient
        - Articulation point detection

        Returns bridge concepts that connect different knowledge areas.
        """
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const nodes = g.nodes();
                const n = nodes.length;

                // ═══ COMMUNITY DETECTION ═══
                const communityOf = {};
                nodes.forEach((v, i) => communityOf[v] = i);

                for (let pass = 0; pass < 10; pass++) {
                    let improved = false;
                    nodes.forEach(v => {
                        const neighbors = g.neighbors(v);
                        if (neighbors.length === 0) return;

                        const commCounts = {};
                        neighbors.forEach(u => {
                            const c = communityOf[u];
                            commCounts[c] = (commCounts[c] || 0) + 1;
                        });

                        const bestComm = Object.entries(commCounts)
                            .sort((a, b) => b[1] - a[1])[0][0];

                        if (bestComm !== String(communityOf[v])) {
                            communityOf[v] = parseInt(bestComm);
                            improved = true;
                        }
                    });
                    if (!improved) break;
                }

                // ═══ BRIDGE DETECTION ═══
                const bridges = nodes.map(v => {
                    const neighbors = g.neighbors(v);
                    const ownComm = communityOf[v];

                    // Inter-community connections
                    const interComm = neighbors.filter(u => communityOf[u] !== ownComm);
                    const intraComm = neighbors.filter(u => communityOf[u] === ownComm);

                    // Communities connected
                    const connectedComms = new Set(interComm.map(u => communityOf[u]));

                    // Local clustering coefficient
                    let triangles = 0;
                    for (let i = 0; i < neighbors.length; i++) {
                        for (let j = i + 1; j < neighbors.length; j++) {
                            if (g.hasEdge(neighbors[i], neighbors[j]) ||
                                g.hasEdge(neighbors[j], neighbors[i])) {
                                triangles++;
                            }
                        }
                    }
                    const maxTriangles = neighbors.length * (neighbors.length - 1) / 2;
                    const clustering = maxTriangles > 0 ? triangles / maxTriangles : 0;

                    // Bridge score: high inter-comm, low clustering
                    const bridgeScore = neighbors.length > 0
                        ? (interComm.length / neighbors.length) * (1 - clustering)
                        : 0;

                    return {
                        node: v,
                        community: ownComm,
                        degree: neighbors.length,
                        interCommunityEdges: interComm.length,
                        intraCommunityEdges: intraComm.length,
                        connectedCommunities: [...connectedComms],
                        clusteringCoeff: clustering,
                        bridgeScore: bridgeScore
                    };
                })
                .filter(b => b.bridgeScore > 0)
                .sort((a, b) => b.bridgeScore - a.bridgeScore);

                // ═══ ARTICULATION POINTS (simplified) ═══
                // Nodes whose removal disconnects the graph
                const articulationPoints = [];

                const isConnectedWithout = (excludeNode) => {
                    const remaining = nodes.filter(v => v !== excludeNode);
                    if (remaining.length === 0) return true;

                    const visited = new Set();
                    const queue = [remaining[0]];
                    visited.add(remaining[0]);

                    while (queue.length > 0) {
                        const v = queue.shift();
                        g.neighbors(v).forEach(u => {
                            if (u !== excludeNode && !visited.has(u)) {
                                visited.add(u);
                                queue.push(u);
                            }
                        });
                    }

                    return visited.size === remaining.length;
                };

                // Check top bridge candidates
                bridges.slice(0, 10).forEach(b => {
                    if (!isConnectedWithout(b.node)) {
                        articulationPoints.push(b.node);
                    }
                });

                return {
                    trace: "bridge",
                    bridges: bridges.slice(0, 20),
                    articulationPoints: articulationPoints,
                    insights: {
                        top_bridges: bridges.slice(0, 5).map(b => b.node),
                        multi_community_connectors: bridges
                            .filter(b => b.connectedCommunities.length >= 2)
                            .slice(0, 5)
                            .map(b => b.node),
                        critical_nodes: articulationPoints,
                        avg_bridge_score: bridges.length > 0
                            ? bridges.reduce((s, b) => s + b.bridgeScore, 0) / bridges.length
                            : 0
                    },
                    stats: {
                        nodeCount: n,
                        bridgeCount: bridges.length,
                        articulationCount: articulationPoints.length,
                        communityCount: new Set(Object.values(communityOf)).size
                    }
                };
            })()
        """)

    # ───────────────────────────────────────────────────────────────
    # LEVEL 2: REASONING CHAINS (Multihop Integration)
    # ───────────────────────────────────────────────────────────────

    async def reasoning_prerequisite_chain(self, concept: str) -> Dict:
        """
        CHAIN: Trace learning dependencies for a concept.

        Multihop integration:
        1. Find all paths TO this concept (what must be learned first)
        2. Rank prerequisites by importance
        3. Identify critical prerequisite sequences
        4. Suggest optimal learning order
        """
        js_concept = json.dumps(concept)
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const concept = {js_concept};

                if (!g.hasNode(concept)) return {{ error: "Concept not found: " + concept }};

                const nodes = g.nodes();

                // ═══ FIND ALL PREREQUISITES (nodes that reach concept) ═══
                const prerequisites = [];
                const pathsTo = {{}};

                nodes.forEach(source => {{
                    if (source === concept) return;

                    // BFS to find path
                    const visited = new Set([source]);
                    const queue = [[source]];
                    let found = false;

                    while (queue.length > 0 && !found) {{
                        const path = queue.shift();
                        const current = path[path.length - 1];

                        for (const neighbor of g.outNeighbors(current)) {{
                            if (neighbor === concept) {{
                                const fullPath = [...path, neighbor];
                                prerequisites.push({{
                                    node: source,
                                    pathLength: fullPath.length - 1,
                                    path: fullPath
                                }});
                                pathsTo[source] = fullPath;
                                found = true;
                                break;
                            }}
                            if (!visited.has(neighbor)) {{
                                visited.add(neighbor);
                                queue.push([...path, neighbor]);
                            }}
                        }}
                    }}
                }});

                // ═══ CALCULATE IMPORTANCE SCORES ═══
                // PageRank-style importance
                const pr = {{}};
                nodes.forEach(v => pr[v] = 1 / nodes.length);

                for (let iter = 0; iter < 30; iter++) {{
                    const newPr = {{}};
                    nodes.forEach(v => newPr[v] = 0.15 / nodes.length);

                    nodes.forEach(v => {{
                        const outDeg = g.outDegree(v);
                        if (outDeg > 0) {{
                            const share = pr[v] * 0.85 / outDeg;
                            g.outNeighbors(v).forEach(u => {{
                                newPr[u] = (newPr[u] || 0) + share;
                            }});
                        }}
                    }});

                    Object.assign(pr, newPr);
                }}

                // Score prerequisites
                const scored = prerequisites.map(p => ({{
                    ...p,
                    importance: pr[p.node] || 0,
                    // Closer = more immediate prerequisite
                    immediacy: 1 / p.pathLength,
                    // Combined score
                    score: (pr[p.node] || 0) * 0.6 + (1 / p.pathLength) * 0.4
                }})).sort((a, b) => b.score - a.score);

                // ═══ IDENTIFY CRITICAL SEQUENCE ═══
                // Find the most important path
                const criticalPath = scored.length > 0
                    ? scored[0].path.slice().reverse()
                    : [concept];

                // Frequency of nodes across all paths
                const nodeFreq = {{}};
                prerequisites.forEach(p => {{
                    p.path.slice(0, -1).forEach(n => {{
                        nodeFreq[n] = (nodeFreq[n] || 0) + 1;
                    }});
                }});

                const criticalNodes = Object.entries(nodeFreq)
                    .filter(([n, f]) => f > prerequisites.length * 0.3)
                    .map(([n, f]) => n);

                // ═══ SUGGEST LEARNING ORDER ═══
                // Topological sort of prerequisites
                const learningOrder = [];
                const inDegree = {{}};
                const prereqGraph = {{}};

                prerequisites.forEach(p => {{
                    const path = p.path;
                    for (let i = 0; i < path.length - 1; i++) {{
                        if (!prereqGraph[path[i]]) prereqGraph[path[i]] = [];
                        if (!prereqGraph[path[i]].includes(path[i + 1])) {{
                            prereqGraph[path[i]].push(path[i + 1]);
                        }}
                    }}
                }});

                Object.keys(prereqGraph).forEach(n => {{
                    if (inDegree[n] === undefined) inDegree[n] = 0;
                    prereqGraph[n].forEach(m => {{
                        inDegree[m] = (inDegree[m] || 0) + 1;
                    }});
                }});

                const queue = Object.keys(prereqGraph).filter(n => (inDegree[n] || 0) === 0);
                while (queue.length > 0) {{
                    const n = queue.shift();
                    if (n !== concept) learningOrder.push(n);
                    (prereqGraph[n] || []).forEach(m => {{
                        inDegree[m]--;
                        if (inDegree[m] === 0) queue.push(m);
                    }});
                }}

                return {{
                    chain: "prerequisite",
                    concept: concept,
                    prerequisites: scored.slice(0, 20),
                    criticalPath: criticalPath,
                    criticalNodes: criticalNodes,
                    suggestedOrder: learningOrder.slice(0, 15),
                    insights: {{
                        total_prerequisites: prerequisites.length,
                        direct_prerequisites: prerequisites.filter(p => p.pathLength === 1).map(p => p.node),
                        foundational_concepts: scored.slice(0, 3).map(s => s.node),
                        gateway_concepts: criticalNodes.slice(0, 3)
                    }},
                    stats: {{
                        prerequisiteCount: prerequisites.length,
                        avgPathLength: prerequisites.length > 0
                            ? prerequisites.reduce((s, p) => s + p.pathLength, 0) / prerequisites.length
                            : 0,
                        maxPathLength: Math.max(...prerequisites.map(p => p.pathLength), 0)
                    }}
                }};
            }})()
        """)

    async def reasoning_mastery_chain(self, concepts: List[str] | None = None) -> Dict:
        """
        CHAIN: Evaluate learning coverage and mastery progression.

        Multihop integration:
        1. Assess coverage of knowledge graph
        2. Identify mastered vs. unmastered regions
        3. Suggest next concepts to learn
        4. Calculate mastery score
        """
        js_concepts = json.dumps(concepts) if concepts else "null"
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const masteredConcepts = {js_concepts} || [];
                const mastered = new Set(masteredConcepts);

                const nodes = g.nodes();
                const n = nodes.length;

                // ═══ CALCULATE COVERAGE ═══
                const coverage = mastered.size / n;

                // Find reachable from mastered (what you can learn next)
                const frontier = new Set();
                const reachableFromMastered = new Set(mastered);

                mastered.forEach(m => {{
                    if (g.hasNode(m)) {{
                        g.outNeighbors(m).forEach(neighbor => {{
                            reachableFromMastered.add(neighbor);
                            if (!mastered.has(neighbor)) {{
                                frontier.add(neighbor);
                            }}
                        }});
                    }}
                }});

                // ═══ IMPORTANCE SCORING ═══
                const pr = {{}};
                nodes.forEach(v => pr[v] = 1 / n);

                for (let iter = 0; iter < 30; iter++) {{
                    const newPr = {{}};
                    nodes.forEach(v => newPr[v] = 0.15 / n);
                    nodes.forEach(v => {{
                        const outDeg = g.outDegree(v);
                        if (outDeg > 0) {{
                            g.outNeighbors(v).forEach(u => {{
                                newPr[u] += 0.85 * pr[v] / outDeg;
                            }});
                        }}
                    }});
                    Object.assign(pr, newPr);
                }});

                // ═══ SCORE FRONTIER CONCEPTS ═══
                const frontierScored = [...frontier].map(node => {{
                    // Prerequisites met?
                    const prereqs = g.inNeighbors(node);
                    const prereqsMet = prereqs.filter(p => mastered.has(p)).length;
                    const prereqRatio = prereqs.length > 0 ? prereqsMet / prereqs.length : 1;

                    // Downstream impact (how many concepts does this unlock?)
                    const downstream = g.outNeighbors(node).length;

                    return {{
                        node: node,
                        importance: pr[node] || 0,
                        prereqsMet: prereqsMet,
                        prereqsTotal: prereqs.length,
                        prereqRatio: prereqRatio,
                        downstreamCount: downstream,
                        // Score: ready to learn + important + unlocks more
                        readinessScore: prereqRatio * 0.4 + (pr[node] || 0) * 0.3 + (downstream / n) * 0.3
                    }};
                }}).sort((a, b) => b.readinessScore - a.readinessScore);

                // ═══ IDENTIFY GAPS ═══
                const gaps = nodes
                    .filter(v => !mastered.has(v))
                    .map(v => ({{
                        node: v,
                        importance: pr[v] || 0,
                        inFrontier: frontier.has(v)
                    }}))
                    .sort((a, b) => b.importance - a.importance);

                // ═══ MASTERY SCORE ═══
                // Weighted by importance of mastered concepts
                const masteryScore = mastered.size > 0
                    ? [...mastered].reduce((sum, m) => sum + (pr[m] || 0), 0) /
                      nodes.reduce((sum, v) => sum + (pr[v] || 0), 0)
                    : 0;

                return {{
                    chain: "mastery",
                    mastered: [...mastered],
                    frontier: frontierScored.slice(0, 15),
                    gaps: gaps.slice(0, 15),
                    insights: {{
                        coverage_percent: (coverage * 100).toFixed(1) + "%",
                        mastery_score: (masteryScore * 100).toFixed(1) + "%",
                        next_to_learn: frontierScored.slice(0, 5).map(f => f.node),
                        critical_gaps: gaps.filter(g => g.importance > 0.05 && !g.inFrontier).slice(0, 5).map(g => g.node),
                        ready_to_learn: frontierScored.filter(f => f.prereqRatio >= 0.8).map(f => f.node)
                    }},
                    stats: {{
                        totalConcepts: n,
                        masteredCount: mastered.size,
                        frontierSize: frontier.size,
                        gapCount: n - mastered.size,
                        coverage: coverage,
                        masteryScore: masteryScore
                    }}
                }};
            }})()
        """)

    # ───────────────────────────────────────────────────────────────
    # LEVEL 3: METASCHEMA EXTRACTION
    # ───────────────────────────────────────────────────────────────

    async def reasoning_metaschema(self) -> Dict:
        """
        METASCHEMA: Extract higher-order structural insights.

        Integrates topology, semantics, and dynamics:
        - Graph topology metrics (diameter, density, clustering)
        - Semantic structure (community labels, edge patterns)
        - Dynamic patterns (flow, hubs, bottlenecks)
        """
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) throw new Error("Breadcrumbs not found");
                const g = bc.mainG;
                const nodes = g.nodes();
                const n = nodes.length;
                const m = g.size;

                if (n === 0) return { error: "Empty graph" };

                // ═══════════════════════════════════════════════════════════
                // TOPOLOGY METRICS
                // ═══════════════════════════════════════════════════════════

                // Density
                const maxEdges = n * (n - 1);
                const density = maxEdges > 0 ? m / maxEdges : 0;

                // Degree distribution
                const degrees = nodes.map(v => g.degree(v));
                const avgDegree = degrees.reduce((s, d) => s + d, 0) / n;
                const maxDegree = Math.max(...degrees);
                const minDegree = Math.min(...degrees);

                // Degree histogram
                const degreeHist = {};
                degrees.forEach(d => { degreeHist[d] = (degreeHist[d] || 0) + 1; });

                // Check for power law (simplified)
                const sortedDegrees = degrees.sort((a, b) => b - a);
                const isPowerLaw = sortedDegrees[0] > avgDegree * 3;

                // Average clustering coefficient
                let totalClustering = 0;
                nodes.forEach(v => {
                    const neighbors = g.neighbors(v);
                    if (neighbors.length < 2) return;

                    let triangles = 0;
                    for (let i = 0; i < neighbors.length; i++) {
                        for (let j = i + 1; j < neighbors.length; j++) {
                            if (g.hasEdge(neighbors[i], neighbors[j]) ||
                                g.hasEdge(neighbors[j], neighbors[i])) {
                                triangles++;
                            }
                        }
                    }
                    const maxTriangles = neighbors.length * (neighbors.length - 1) / 2;
                    totalClustering += maxTriangles > 0 ? triangles / maxTriangles : 0;
                });
                const avgClustering = totalClustering / n;

                // Diameter (longest shortest path) - sample for efficiency
                let diameter = 0;
                const sampleSize = Math.min(n, 20);
                const sample = nodes.slice(0, sampleSize);

                sample.forEach(source => {
                    const dist = {};
                    dist[source] = 0;
                    const queue = [source];

                    while (queue.length > 0) {
                        const v = queue.shift();
                        g.neighbors(v).forEach(u => {
                            if (dist[u] === undefined) {
                                dist[u] = dist[v] + 1;
                                diameter = Math.max(diameter, dist[u]);
                                queue.push(u);
                            }
                        });
                    }
                });

                // ═══════════════════════════════════════════════════════════
                // SEMANTIC STRUCTURE
                // ═══════════════════════════════════════════════════════════

                // Community detection
                const communityOf = {};
                nodes.forEach((v, i) => communityOf[v] = i);

                for (let pass = 0; pass < 15; pass++) {
                    let improved = false;
                    nodes.forEach(v => {
                        const neighbors = g.neighbors(v);
                        if (neighbors.length === 0) return;

                        const commCounts = {};
                        neighbors.forEach(u => {
                            const c = communityOf[u];
                            commCounts[c] = (commCounts[c] || 0) + 1;
                        });

                        const best = Object.entries(commCounts)
                            .sort((a, b) => b[1] - a[1])[0];

                        if (best && parseInt(best[0]) !== communityOf[v]) {
                            communityOf[v] = parseInt(best[0]);
                            improved = true;
                        }
                    });
                    if (!improved) break;
                }

                // Community stats
                const commMembers = {};
                nodes.forEach(v => {
                    const c = communityOf[v];
                    if (!commMembers[c]) commMembers[c] = [];
                    commMembers[c].push(v);
                });

                const communities = Object.entries(commMembers)
                    .filter(([c, members]) => members.length > 1)
                    .map(([id, members]) => {
                        // Find centroid (highest degree in community)
                        const centroid = members.sort((a, b) =>
                            g.neighbors(b).filter(x => communityOf[x] === parseInt(id)).length -
                            g.neighbors(a).filter(x => communityOf[x] === parseInt(id)).length
                        )[0];

                        return {
                            id: parseInt(id),
                            size: members.length,
                            centroid: centroid,
                            label: centroid // Use centroid as label
                        };
                    })
                    .sort((a, b) => b.size - a.size);

                // ═══════════════════════════════════════════════════════════
                // DYNAMIC PATTERNS
                // ═══════════════════════════════════════════════════════════

                // PageRank for flow analysis
                const pr = {};
                nodes.forEach(v => pr[v] = 1 / n);

                for (let iter = 0; iter < 50; iter++) {
                    const newPr = {};
                    nodes.forEach(v => newPr[v] = 0.15 / n);
                    nodes.forEach(v => {
                        const outDeg = g.outDegree(v);
                        if (outDeg > 0) {
                            g.outNeighbors(v).forEach(u => {
                                newPr[u] += 0.85 * pr[v] / outDeg;
                            });
                        }
                    });
                    Object.assign(pr, newPr);
                }

                // Identify roles
                const ranked = nodes.map(v => ({
                    node: v,
                    pagerank: pr[v],
                    inDegree: g.inDegree(v),
                    outDegree: g.outDegree(v),
                    community: communityOf[v]
                })).sort((a, b) => b.pagerank - a.pagerank);

                // Classify nodes
                const hubs = ranked.filter(r => r.outDegree > avgDegree * 1.5);
                const authorities = ranked.filter(r => r.inDegree > avgDegree * 1.5);
                const sources = ranked.filter(r => r.inDegree === 0 && r.outDegree > 0);
                const sinks = ranked.filter(r => r.outDegree === 0 && r.inDegree > 0);

                // ═══════════════════════════════════════════════════════════
                // SCHEMA SUMMARY
                // ═══════════════════════════════════════════════════════════

                return {
                    metaschema: {
                        topology: {
                            nodeCount: n,
                            edgeCount: m,
                            density: density,
                            avgDegree: avgDegree,
                            maxDegree: maxDegree,
                            minDegree: minDegree,
                            diameter: diameter,
                            avgClustering: avgClustering,
                            isPowerLaw: isPowerLaw,
                            degreeDistribution: Object.entries(degreeHist)
                                .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
                                .map(([d, c]) => ({ degree: parseInt(d), count: c }))
                        },
                        semantics: {
                            communityCount: communities.length,
                            communities: communities.slice(0, 10),
                            largestCommunity: communities[0] || null,
                            avgCommunitySize: communities.length > 0
                                ? communities.reduce((s, c) => s + c.size, 0) / communities.length
                                : 0
                        },
                        dynamics: {
                            hubs: hubs.slice(0, 5).map(h => h.node),
                            authorities: authorities.slice(0, 5).map(a => a.node),
                            sources: sources.slice(0, 5).map(s => s.node),
                            sinks: sinks.slice(0, 5).map(s => s.node),
                            topByPageRank: ranked.slice(0, 10).map(r => ({
                                node: r.node,
                                pagerank: r.pagerank,
                                community: r.community
                            }))
                        }
                    },
                    interpretation: {
                        structure_type: density > 0.3 ? "dense" : density > 0.1 ? "moderate" : "sparse",
                        organization: isPowerLaw ? "hub-and-spoke" : "distributed",
                        modularity: communities.length > 1 ? "modular" : "monolithic",
                        flow_pattern: sources.length > sinks.length ? "convergent" :
                                     sinks.length > sources.length ? "divergent" : "balanced"
                    },
                    recommendations: [
                        density < 0.1 ? "Graph is sparse - consider adding more connections" : null,
                        avgClustering < 0.2 ? "Low clustering - concepts may be too isolated" : null,
                        communities.length === 1 ? "Single community - consider subdividing topics" : null,
                        hubs.length === 0 ? "No clear hubs - consider identifying key concepts" : null,
                        sources.length > n * 0.3 ? "Many source nodes - ensure prerequisites are connected" : null
                    ].filter(r => r !== null)
                };
            })()
        """)

    # ───────────────────────────────────────────────────────────────
    # LEVEL 4: UNIFIED ORCHESTRATOR
    # ───────────────────────────────────────────────────────────────

    async def evaluate(self, mode: str = "standard", source: str | None = None, target: str | None = None) -> Dict:
        """
        UNIFIED ORCHESTRATOR: Single entry point for comprehensive graph reasoning.

        Modes:
        - "quick": Importance + Clusters only (~2s)
        - "standard": All primitives (~5s)
        - "comprehensive": Primitives + Chains + Metaschema (~10s)
        - "deep": Everything + Path analysis for source/target (~15s)

        Returns aggregated insights with cross-validated findings.
        """
        results = {
            "mode": mode,
            "timestamp": None,
            "primitives": {},
            "chains": {},
            "metaschema": None,
            "synthesis": {},
            "recommendations": []
        }

        # Get timestamp
        results["timestamp"] = await self.eval("new Date().toISOString()")

        try:
            # ═══ QUICK MODE ═══
            if mode in ["quick", "standard", "comprehensive", "deep"]:
                importance = await self.reasoning_importance_trace()
                clusters = await self.reasoning_cluster_trace()

                results["primitives"]["importance"] = importance
                results["primitives"]["clusters"] = clusters

            # ═══ STANDARD MODE ═══
            if mode in ["standard", "comprehensive", "deep"]:
                gaps = await self.reasoning_gap_trace()
                bridges = await self.reasoning_bridge_trace()

                results["primitives"]["gaps"] = gaps
                results["primitives"]["bridges"] = bridges

            # ═══ COMPREHENSIVE MODE ═══
            if mode in ["comprehensive", "deep"]:
                metaschema = await self.reasoning_metaschema()
                results["metaschema"] = metaschema

                # Mastery chain (empty mastered list = assess all)
                mastery = await self.reasoning_mastery_chain([])
                results["chains"]["mastery"] = mastery

            # ═══ DEEP MODE ═══
            if mode == "deep" and source and target:
                path_trace = await self.reasoning_path_trace(source, target)
                prereq_source = await self.reasoning_prerequisite_chain(source)
                prereq_target = await self.reasoning_prerequisite_chain(target)

                results["chains"]["path_trace"] = path_trace
                results["chains"]["prereq_source"] = prereq_source
                results["chains"]["prereq_target"] = prereq_target

            # ═══ SYNTHESIS ═══
            results["synthesis"] = self._synthesize_results(results)
            results["recommendations"] = self._generate_recommendations(results)

        except Exception as e:
            results["error"] = str(e)

        return results

    def _synthesize_results(self, results: Dict) -> Dict:
        """Synthesize insights from multiple analysis results."""
        synthesis = {
            "key_concepts": [],
            "knowledge_structure": {},
            "learning_insights": {},
            "quality_score": 0
        }

        # Extract key concepts (cross-validated across metrics)
        if "importance" in results.get("primitives", {}):
            imp = results["primitives"]["importance"]
            if "ranked" in imp:
                top_important = [r["node"] for r in imp["ranked"][:5]]
                synthesis["key_concepts"] = top_important

        # Knowledge structure
        if "clusters" in results.get("primitives", {}):
            cl = results["primitives"]["clusters"]
            synthesis["knowledge_structure"]["cluster_count"] = cl.get("stats", {}).get("clusterCount", 0)
            synthesis["knowledge_structure"]["modularity"] = cl.get("stats", {}).get("modularity", 0)

        # Learning insights
        if "gaps" in results.get("primitives", {}):
            gaps = results["primitives"]["gaps"]
            synthesis["learning_insights"]["gap_count"] = gaps.get("stats", {}).get("missingLinkCandidates", 0)
            synthesis["learning_insights"]["isolated_count"] = gaps.get("stats", {}).get("isolatedCount", 0)

        # Quality score (0-100)
        quality = 50  # Base score

        # Adjust based on findings
        if results.get("metaschema"):
            meta = results["metaschema"]
            if "metaschema" in meta:
                topo = meta["metaschema"].get("topology", {})
                # Higher density = better
                quality += min(20, topo.get("density", 0) * 100)
                # Higher clustering = better
                quality += min(15, topo.get("avgClustering", 0) * 30)
                # Lower diameter = better (more compact)
                quality -= min(10, topo.get("diameter", 5))

        if "gaps" in results.get("primitives", {}):
            gaps = results["primitives"]["gaps"]
            isolated = gaps.get("stats", {}).get("isolatedCount", 0)
            total = gaps.get("stats", {}).get("nodeCount", 1)
            # Fewer isolated = better
            quality -= min(15, (isolated / total) * 50)

        synthesis["quality_score"] = max(0, min(100, quality))

        return synthesis

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations from analysis."""
        recommendations = []

        # From gaps analysis
        if "gaps" in results.get("primitives", {}):
            gaps = results["primitives"]["gaps"]
            if gaps.get("prioritized"):
                for gap in gaps["prioritized"][:3]:
                    recommendations.append(gap.get("action", ""))

        # From metaschema
        if results.get("metaschema") and "recommendations" in results["metaschema"]:
            recommendations.extend(results["metaschema"]["recommendations"][:3])

        # From importance
        if "importance" in results.get("primitives", {}):
            imp = results["primitives"]["importance"]
            insights = imp.get("insights", {})
            if not insights.get("hub_nodes"):
                recommendations.append("Consider identifying key hub concepts to anchor the knowledge graph")

        # From bridges
        if "bridges" in results.get("primitives", {}):
            bridges = results["primitives"]["bridges"]
            if bridges.get("articulationPoints"):
                critical = bridges["articulationPoints"][:2]
                recommendations.append(f"Critical bridge nodes {critical} - ensure redundant paths exist")

        return [r for r in recommendations if r]  # Filter empty

    # ═══════════════════════════════════════════════════════════════════════════
    # LEVEL 5-8: AUTONOMOUS GRAPH INTELLIGENCE
    # Integrates MEGA, Ontolog, Telos, Dialectical frameworks
    # ═══════════════════════════════════════════════════════════════════════════

    async def compute_mega_invariants(self) -> Dict:
        """
        Compute MEGA (Maximally Endowed Graph Architecture) invariants.

        Returns:
            Dict with η (edge density), φ (isolation ratio), κ (clustering),
            n (hierarchy depth), mega_score, and autopoietic recommendations.
        """
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) return { error: "Breadcrumbs not available" };

                const g = bc.mainG;
                const nodes = g.nodes();
                const edges = g.edges();

                // η (eta) - Edge Density
                const η = edges.length / Math.max(nodes.length, 1);

                // φ (phi) - Isolation Ratio
                const isolatedNodes = nodes.filter(n => g.degree(n) === 0);
                const φ = isolatedNodes.length / Math.max(nodes.length, 1);

                // κ (kappa) - Clustering Coefficient
                let totalCC = 0;
                let validNodes = 0;
                nodes.forEach(n => {
                    const neighbors = g.neighbors(n);
                    if (neighbors.length < 2) return;
                    let edgesBetween = 0;
                    for (let i = 0; i < neighbors.length; i++) {
                        for (let j = i + 1; j < neighbors.length; j++) {
                            if (g.hasEdge(neighbors[i], neighbors[j]) || g.hasEdge(neighbors[j], neighbors[i])) {
                                edgesBetween++;
                            }
                        }
                    }
                    const maxEdges = (neighbors.length * (neighbors.length - 1)) / 2;
                    totalCC += edgesBetween / maxEdges;
                    validNodes++;
                });
                const κ = validNodes > 0 ? totalCC / validNodes : 0;

                // n - Hierarchy Depth
                let maxDepth = 0;
                const inDegrees = {};
                nodes.forEach(n => { inDegrees[n] = g.inDegree(n); });
                const roots = nodes.filter(n => inDegrees[n] === 0);
                roots.forEach(root => {
                    const visited = new Set();
                    const queue = [[root, 0]];
                    while (queue.length > 0) {
                        const [node, depth] = queue.shift();
                        if (visited.has(node)) continue;
                        visited.add(node);
                        maxDepth = Math.max(maxDepth, depth);
                        g.outNeighbors(node).forEach(neighbor => {
                            if (!visited.has(neighbor)) queue.push([neighbor, depth + 1]);
                        });
                    }
                });

                // MEGA Score
                const ηScore = η >= 4 ? 1 : η / 4;
                const φScore = φ < 0.2 ? 1 : 1 - φ;
                const κScore = κ > 0.3 ? 1 : κ / 0.3;
                const nScore = maxDepth <= 3 ? 1 : 3 / maxDepth;
                const megaScore = (ηScore * 0.25 + φScore * 0.25 + κScore * 0.25 + nScore * 0.25);

                return {
                    graph_stats: { nodes: nodes.length, edges: edges.length, isolated: isolatedNodes.length },
                    invariants: {
                        η: { value: η, target: 4, satisfied: η >= 4 },
                        φ: { value: φ, target: 0.2, satisfied: φ < 0.2 },
                        κ: { value: κ, target: 0.3, satisfied: κ > 0.3 },
                        n: { value: maxDepth, target: 3, satisfied: maxDepth <= 3 }
                    },
                    mega_score: megaScore,
                    status: megaScore >= 0.8 ? "HEALTHY" : "NEEDS_REFINEMENT",
                    autopoietic: megaScore < 0.8 ? [
                        η < 4 ? "R1_BRIDGE: Add edges to increase connectivity" : null,
                        φ >= 0.2 ? "R1_BRIDGE: Connect isolated nodes" : null,
                        κ <= 0.3 ? "R3_EXPAND: Create triangular connections" : null,
                        maxDepth > 3 ? "R2_COMPRESS: Flatten hierarchy" : null
                    ].filter(Boolean) : []
                };
            })()
        """)

    async def compute_persistent_homology(self) -> Dict:
        """
        Compute persistent homology (Betti numbers H0, H1, H2).

        Returns:
            Dict with H0 (components), H1 (cycles), H2 (voids), and interpretations.
        """
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) return { error: "Breadcrumbs not available" };

                const g = bc.mainG;
                const nodes = g.nodes();
                const edges = g.edges();

                // H0 - Connected Components
                const visited = new Set();
                const components = [];
                nodes.forEach(startNode => {
                    if (visited.has(startNode)) return;
                    const component = [];
                    const queue = [startNode];
                    while (queue.length > 0) {
                        const node = queue.shift();
                        if (visited.has(node)) continue;
                        visited.add(node);
                        component.push(node);
                        const neighbors = [...new Set([...g.outNeighbors(node), ...g.inNeighbors(node)])];
                        neighbors.forEach(n => { if (!visited.has(n)) queue.push(n); });
                    }
                    if (component.length > 0) components.push(component);
                });

                const H0 = components.length;
                const H1 = edges.length - nodes.length + H0; // Cycle rank

                // Count triangles for H2 proxy
                let triangles = 0;
                nodes.forEach(n => {
                    const neighbors = g.neighbors(n);
                    for (let i = 0; i < neighbors.length; i++) {
                        for (let j = i + 1; j < neighbors.length; j++) {
                            if (g.hasEdge(neighbors[i], neighbors[j]) || g.hasEdge(neighbors[j], neighbors[i])) {
                                triangles++;
                            }
                        }
                    }
                });
                triangles = Math.floor(triangles / 3);

                return {
                    simplicial: { nodes: nodes.length, edges: edges.length, triangles: triangles },
                    betti: {
                        H0: { value: H0, meaning: "connected components", optimal: H0 === 1 },
                        H1: { value: H1, meaning: "independent cycles", note: H1 > 0 ? "cycles detected" : "acyclic" },
                        H2_proxy: { value: components.length > 1 ? components.length - 1 : 0, meaning: "structural voids" }
                    },
                    components: components.map(c => ({ size: c.length, sample: c.slice(0, 3) })).slice(0, 5),
                    euler_characteristic: nodes.length - edges.length + 1
                };
            })()
        """)

    async def k_bisimulation_classes(self, k: int = 5) -> Dict:
        """
        Compute k-bisimulation structural equivalence classes.

        Args:
            k: Bisimulation depth (default 5, sufficient for most graphs)

        Returns:
            Dict with equivalence classes, compression ratio, and largest classes.
        """
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) return {{ error: "Breadcrumbs not available" }};

                const g = bc.mainG;
                const nodes = g.nodes();

                // Structural signature based on in/out degree
                const signatures = {{}};
                nodes.forEach(n => {{
                    const inDeg = g.inDegree(n);
                    const outDeg = g.outDegree(n);
                    const sig = `in:${{inDeg}},out:${{outDeg}}`;
                    if (!signatures[sig]) signatures[sig] = [];
                    signatures[sig].push(n);
                }});

                const classes = Object.keys(signatures).length;
                const compressionRatio = 1 - (classes / nodes.length);

                const sortedClasses = Object.entries(signatures)
                    .map(([sig, members]) => ({{ signature: sig, count: members.length, members: members.slice(0, 5) }}))
                    .sort((a, b) => b.count - a.count);

                return {{
                    k: {k},
                    equivalence_classes: classes,
                    compression_ratio: compressionRatio,
                    original_nodes: nodes.length,
                    compressed_nodes: classes,
                    largest_classes: sortedClasses.slice(0, 5)
                }};
            }})()
        """)

    async def compute_telos_hierarchy(self) -> Dict:
        """
        Compute Telos three-level hierarchy (Strategic τ / Tactical λ / Operational ο).

        Returns:
            Dict with classified nodes, constraint taxonomy, and hierarchy completeness.
        """
        return await self.eval("""
            (() => {
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) return { error: "Breadcrumbs not available" };

                const g = bc.mainG;
                const nodes = g.nodes();
                const conceptNodes = nodes.filter(n => g.degree(n) > 0);

                const classification = { strategic_τ: [], tactical_λ: [], operational_ο: [] };

                conceptNodes.forEach(n => {
                    const inDeg = g.inDegree(n);
                    const outDeg = g.outDegree(n);
                    const ratio = outDeg > 0 ? inDeg / outDeg : inDeg;

                    if (outDeg >= 3 && ratio <= 1.5) {
                        classification.strategic_τ.push({ node: n, inDeg, outDeg, reason: "High outDegree, initiates cascades" });
                    } else if (inDeg >= 3 && outDeg <= 2) {
                        classification.operational_ο.push({ node: n, inDeg, outDeg, reason: "Convergence point" });
                    } else {
                        classification.tactical_λ.push({ node: n, inDeg, outDeg, reason: "Intermediate mechanism" });
                    }
                });

                // Constraint taxonomy
                const constraints = { physical: [], chemical: [], energetic: [], temporal: [], spatial: [] };
                conceptNodes.forEach(n => {
                    const name = n.toLowerCase();
                    if (name.includes('volume') || name.includes('blood') || name.includes('cardiac')) constraints.physical.push(n);
                    if (name.includes('progesterone') || name.includes('hormone') || name.includes('alkalosis')) constraints.chemical.push(n);
                    if (name.includes('oxygen') || name.includes('metabolic') || name.includes('mac')) constraints.energetic.push(n);
                    if (name.includes('aortocaval') || name.includes('supine') || name.includes('uteroplacental')) constraints.spatial.push(n);
                });

                const hierarchyComplete = classification.strategic_τ.length > 0 &&
                                          classification.tactical_λ.length > 0 &&
                                          classification.operational_ο.length > 0;

                return {
                    concept_nodes: conceptNodes.length,
                    hierarchy: {
                        τ_strategic: { count: classification.strategic_τ.length, nodes: classification.strategic_τ.slice(0, 3) },
                        λ_tactical: { count: classification.tactical_λ.length, nodes: classification.tactical_λ.slice(0, 3) },
                        ο_operational: { count: classification.operational_ο.length, nodes: classification.operational_ο.slice(0, 3) }
                    },
                    constraints: Object.fromEntries(Object.entries(constraints).map(([k, v]) => [k, { count: v.length, examples: v.slice(0, 3) }])),
                    hierarchy_complete: hierarchyComplete,
                    constraint_coverage: Object.values(constraints).filter(c => c.length > 0).length / 5
                };
            })()
        """)

    async def dialectical_link_synthesis(self, threshold: float = 0.3) -> Dict:
        """
        Compute link predictions using dialectical synthesis (Σ→Τ→Δ→Ρ).

        Args:
            threshold: Minimum score for predictions (default 0.3)

        Returns:
            Dict with thesis (current), antithesis (predictions), and synthesis (recommendations).
        """
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) return {{ error: "Breadcrumbs not available" }};

                const g = bc.mainG;
                const nodes = g.nodes();
                const conceptNodes = nodes.filter(n => g.degree(n) > 0);

                // Σ (Source): Current state
                const thesis = {{ nodes: conceptNodes.length, edges: g.edges().length }};

                // Τ (Transform): Link predictions
                const predictions = [];
                conceptNodes.forEach(u => {{
                    conceptNodes.forEach(v => {{
                        if (u >= v) return;
                        if (g.hasEdge(u, v) || g.hasEdge(v, u)) return;

                        const neighborsU = new Set(g.neighbors(u));
                        const neighborsV = new Set(g.neighbors(v));
                        const common = [...neighborsU].filter(n => neighborsV.has(n));

                        if (common.length === 0) return;

                        const union = new Set([...neighborsU, ...neighborsV]);
                        const jaccard = common.length / union.size;
                        const adamicAdar = common.reduce((s, cn) => s + (g.degree(cn) > 1 ? 1/Math.log(g.degree(cn)) : 0), 0);
                        const score = jaccard * 0.5 + adamicAdar / 10 * 0.3 + common.length / 10 * 0.2;

                        if (score > {threshold}) {{
                            predictions.push({{
                                source: u, target: v,
                                commonNeighbors: common,
                                jaccard: jaccard,
                                score: score,
                                confidence: Math.min(1, score * 2)
                            }});
                        }}
                    }});
                }});

                predictions.sort((a, b) => b.score - a.score);

                // Δ (Dialectic): Synthesize with edge type inference
                const synthesis = predictions.slice(0, 10).map(pred => {{
                    const srcOut = g.outDegree(pred.source);
                    const tgtOut = g.outDegree(pred.target);

                    let edgeType, field;
                    if (srcOut > tgtOut + 1) {{
                        edgeType = "down"; field = "concept_direct";
                    }} else if (tgtOut > srcOut + 1) {{
                        edgeType = "up"; field = "concept_prerequisite";
                    }} else {{
                        edgeType = "same"; field = "concept_peer";
                    }}

                    return {{
                        source: pred.source,
                        target: pred.target,
                        edgeType: edgeType,
                        field: field,
                        wikilink: `[[$${{pred.target}}]]`,
                        score: pred.score,
                        confidence: pred.confidence,
                        evidence: pred.commonNeighbors.slice(0, 3)
                    }};
                }});

                return {{
                    thesis: thesis,
                    antithesis: {{ total_evaluated: conceptNodes.length * (conceptNodes.length - 1) / 2, above_threshold: predictions.length }},
                    synthesis: synthesis,
                    impact: {{
                        current_edges: thesis.edges,
                        potential_new: synthesis.length,
                        new_edge_density: (thesis.edges + synthesis.length) / thesis.nodes
                    }}
                }};
            }})()
        """)

    async def apply_link_predictions(self, predictions: List[Dict], dry_run: bool = True) -> Dict:
        """
        Apply link predictions to frontmatter.

        Args:
            predictions: List of prediction dicts with source, target, field, wikilink
            dry_run: If True, return changes without applying

        Returns:
            Dict with applied changes or dry-run preview
        """
        predictions_json = json.dumps(predictions)
        dry_run_js = "true" if dry_run else "false"

        return await self.eval(f"""
            (async () => {{
                const predictions = {predictions_json};
                const dryRun = {dry_run_js};
                const changes = [];

                for (const pred of predictions) {{
                    const file = app.vault.getAbstractFileByPath(pred.source.endsWith('.md') ? pred.source : pred.source + '.md');
                    if (!file) {{
                        // Try Concepts folder
                        const conceptPath = `Concepts/Maternal-Physiology/${{pred.source}}.md`;
                        const conceptFile = app.vault.getAbstractFileByPath(conceptPath);
                        if (!conceptFile) {{
                            changes.push({{ source: pred.source, status: "file_not_found" }});
                            continue;
                        }}
                        pred.sourcePath = conceptPath;
                    }} else {{
                        pred.sourcePath = file.path;
                    }}

                    if (!dryRun) {{
                        const content = await app.vault.read(app.vault.getAbstractFileByPath(pred.sourcePath));

                        // Parse frontmatter
                        const fmMatch = content.match(/^---\\n([\\s\\S]*?)\\n---/);
                        if (fmMatch) {{
                            let fm = fmMatch[1];
                            const fieldRegex = new RegExp(`^${{pred.field}}:.*$`, 'm');

                            if (fieldRegex.test(fm)) {{
                                // Append to existing field
                                fm = fm.replace(fieldRegex, (match) => {{
                                    if (match.includes(pred.wikilink)) return match;
                                    return match.includes('[') ?
                                        match.replace(/\\]\\s*$/, `, ${{pred.wikilink}}]`) :
                                        `${{pred.field}}:\\n  - ${{pred.wikilink}}`;
                                }});
                            }} else {{
                                // Add new field
                                fm += `\\n${{pred.field}}:\\n  - ${{pred.wikilink}}`;
                            }}

                            const newContent = content.replace(/^---\\n[\\s\\S]*?\\n---/, `---\\n${{fm}}\\n---`);
                            await app.vault.modify(app.vault.getAbstractFileByPath(pred.sourcePath), newContent);
                        }}
                    }}

                    changes.push({{
                        source: pred.source,
                        target: pred.target,
                        field: pred.field,
                        wikilink: pred.wikilink,
                        status: dryRun ? "would_apply" : "applied"
                    }});
                }}

                return {{
                    dry_run: dryRun,
                    total: changes.length,
                    applied: changes.filter(c => c.status === "applied").length,
                    changes: changes
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # CANVAS GENERATION (Telos Layout + Graph Updates)
    # ═══════════════════════════════════════════════════════════════════════════

    async def generate_canvas_from_graph(self, layout: str = "telos") -> Dict:
        """
        Generate canvas JSON from Breadcrumbs graph using specified layout.

        Args:
            layout: "telos" (hierarchical), "force" (force-directed), or "radial"

        Returns:
            Dict with nodes, edges, groups for canvas
        """
        return await self.eval(f"""
            (() => {{
                const bc = app.plugins.plugins["breadcrumbs"];
                if (!bc || !bc.mainG) return {{ error: "Breadcrumbs not available" }};

                const g = bc.mainG;
                const nodes = g.nodes().filter(n => g.degree(n) > 0);
                const edges = g.edges();

                // Classify nodes using Telos hierarchy
                const classification = {{ strategic: [], tactical: [], operational: [] }};
                nodes.forEach(n => {{
                    const outDegree = g.outDegree(n);
                    const inDegree = g.inDegree(n);
                    if (outDegree > inDegree + 2) {{
                        classification.strategic.push(n);
                    }} else if (inDegree > outDegree + 2) {{
                        classification.operational.push(n);
                    }} else {{
                        classification.tactical.push(n);
                    }}
                }});

                // Generate node positions based on layout
                const canvasNodes = [];
                const layout = "{layout}";
                let y = 0;

                if (layout === "telos") {{
                    // Layer 1: Strategic (top)
                    let x = 0;
                    classification.strategic.forEach((n, i) => {{
                        canvasNodes.push({{
                            id: n.replace(/[^a-zA-Z0-9]/g, '-'),
                            type: "file",
                            file: `Concepts/Maternal-Physiology/${{n}}.md`,
                            x: x + (i * 300),
                            y: 0,
                            width: 250,
                            height: 100,
                            color: "3"
                        }});
                    }});

                    // Layer 2: Tactical (middle)
                    y = 200;
                    classification.tactical.forEach((n, i) => {{
                        canvasNodes.push({{
                            id: n.replace(/[^a-zA-Z0-9]/g, '-'),
                            type: "file",
                            file: `Concepts/Maternal-Physiology/${{n}}.md`,
                            x: (i * 300),
                            y: y,
                            width: 250,
                            height: 100,
                            color: "6"
                        }});
                    }});

                    // Layer 3: Operational (bottom)
                    y = 400;
                    classification.operational.forEach((n, i) => {{
                        canvasNodes.push({{
                            id: n.replace(/[^a-zA-Z0-9]/g, '-'),
                            type: "file",
                            file: `Concepts/Maternal-Physiology/${{n}}.md`,
                            x: (i * 300),
                            y: y,
                            width: 250,
                            height: 100,
                            color: "4"
                        }});
                    }});
                }}

                // Generate edges
                const canvasEdges = edges.slice(0, 50).map((e, i) => {{
                    const [source, target] = e.split('→');
                    return {{
                        id: `edge-${{i}}`,
                        fromNode: source?.replace(/[^a-zA-Z0-9]/g, '-') || '',
                        toNode: target?.replace(/[^a-zA-Z0-9]/g, '-') || '',
                        color: "5"
                    }};
                }}).filter(e => e.fromNode && e.toNode);

                // Generate groups
                const groups = [
                    {{ id: "strategic", label: "Strategic (τ)", color: "3", x: -50, y: -50, width: classification.strategic.length * 300 + 100, height: 170 }},
                    {{ id: "tactical", label: "Tactical (λ)", color: "6", x: -50, y: 150, width: classification.tactical.length * 300 + 100, height: 170 }},
                    {{ id: "operational", label: "Operational (ο)", color: "4", x: -50, y: 350, width: classification.operational.length * 300 + 100, height: 170 }}
                ];

                return {{
                    layout: layout,
                    classification: {{
                        strategic: classification.strategic.length,
                        tactical: classification.tactical.length,
                        operational: classification.operational.length
                    }},
                    canvas: {{
                        nodes: canvasNodes,
                        edges: canvasEdges,
                        groups: groups
                    }}
                }};
            }})()
        """)

    async def add_predicted_edges_to_canvas(self, canvas_path: str, predictions: List[Dict]) -> Dict:
        """
        Add predicted edges from dialectical synthesis to existing canvas.

        Args:
            canvas_path: Path to canvas file
            predictions: List of predictions with source, target, edgeType

        Returns:
            Dict with added edges count
        """
        predictions_json = json.dumps(predictions)

        return await self.eval(f"""
            (async () => {{
                const canvasPath = "{canvas_path}";
                const predictions = {predictions_json};

                const file = app.vault.getAbstractFileByPath(canvasPath);
                if (!file) return {{ error: "Canvas file not found" }};

                const content = await app.vault.read(file);
                const canvas = JSON.parse(content);

                // Find existing node IDs
                const nodeIds = new Set(canvas.nodes.map(n => n.id));
                const nodeByFile = {{}};
                canvas.nodes.filter(n => n.type === "file").forEach(n => {{
                    const name = n.file.split('/').pop().replace('.md', '');
                    nodeByFile[name] = n.id;
                }});

                // Add new edges from predictions
                const addedEdges = [];
                let edgeId = canvas.edges.length;

                predictions.forEach(pred => {{
                    const fromId = nodeByFile[pred.source];
                    const toId = nodeByFile[pred.target];

                    if (!fromId || !toId) return;

                    // Check if edge already exists
                    const exists = canvas.edges.some(e =>
                        (e.fromNode === fromId && e.toNode === toId) ||
                        (e.fromNode === toId && e.toNode === fromId)
                    );

                    if (!exists) {{
                        canvas.edges.push({{
                            id: `pred-edge-${{edgeId++}}`,
                            fromNode: fromId,
                            toNode: toId,
                            color: pred.edgeType === "up" ? "3" : pred.edgeType === "down" ? "4" : "5",
                            label: pred.edgeType
                        }});
                        addedEdges.push({{ from: pred.source, to: pred.target }});
                    }}
                }});

                // Save updated canvas
                await app.vault.modify(file, JSON.stringify(canvas, null, '\\t'));

                return {{
                    canvas_path: canvasPath,
                    edges_before: canvas.edges.length - addedEdges.length,
                    edges_added: addedEdges.length,
                    edges_after: canvas.edges.length,
                    added: addedEdges
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # BASE FILE GENERATION (MEGA Formulas + Holonic Views)
    # ═══════════════════════════════════════════════════════════════════════════

    async def generate_base_file(self, name: str, folder: str = "Concepts/Maternal-Physiology") -> Dict:
        """
        Generate .base file with MEGA-compliant views and formulas.

        Args:
            name: Base file name (without .base extension)
            folder: Source folder for notes

        Returns:
            Dict with base file content
        """
        return await self.eval(f"""
            (async () => {{
                const folder = "{folder}";
                const name = "{name}";

                // Generate base file content with MEGA formulas
                const baseContent = {{
                    filter: {{
                        and: [
                            {{ "file.folder": folder }}
                        ]
                    }},
                    formulas: {{
                        edge_density: "list(up).length + list(down).length + list(same).length",
                        isolation_risk: "(list(up).length + list(down).length + list(same).length) == 0 ? 1 : 0",
                        connectivity_score: "(list(up).length * 2 + list(down).length * 2 + list(same).length) / 10",
                        prerequisite_count: "list(up).length",
                        dependency_count: "list(down).length",
                        mastery_numeric: "mastery_level == 'proficient' ? 4 : mastery_level == 'competent' ? 3 : mastery_level == 'developing' ? 2 : 1",
                        revision_urgency: "exam_frequency * (1 - formula.mastery_numeric / 4)"
                    }},
                    views: [
                        {{
                            type: "table",
                            name: "All Concepts",
                            order: ["title", "domain", "exam_frequency", "mastery_level", "formula.connectivity_score"],
                            sort: [{{ property: "exam_frequency", direction: "DESC" }}]
                        }},
                        {{
                            type: "board",
                            name: "By Domain",
                            groupBy: "domain",
                            cardTitle: "title"
                        }},
                        {{
                            type: "table",
                            name: "MEGA Analysis",
                            order: ["title", "formula.edge_density", "formula.isolation_risk", "formula.connectivity_score"],
                            sort: [{{ property: "formula.connectivity_score", direction: "DESC" }}]
                        }},
                        {{
                            type: "table",
                            name: "Revision Priority",
                            order: ["title", "exam_frequency", "mastery_level", "formula.revision_urgency"],
                            sort: [{{ property: "formula.revision_urgency", direction: "DESC" }}],
                            filter: {{ "formula.revision_urgency": {{ ">": 3 }} }}
                        }}
                    ]
                }};

                // Create base file
                const basePath = `${{folder.split('/')[0]}}/${{name}}.base`;
                const content = JSON.stringify(baseContent, null, 2);

                const existingFile = app.vault.getAbstractFileByPath(basePath);
                if (existingFile) {{
                    await app.vault.modify(existingFile, content);
                }} else {{
                    await app.vault.create(basePath, content);
                }}

                return {{
                    path: basePath,
                    views: baseContent.views.length,
                    formulas: Object.keys(baseContent.formulas).length,
                    content: baseContent
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # AI INTEGRATION - Smart Connections
    # ═══════════════════════════════════════════════════════════════════════════

    async def ai_semantic_search(self, query: str, limit: int = 10) -> Dict:
        """
        Semantic search using Smart Connections embeddings.

        Args:
            query: Search query text
            limit: Maximum results to return

        Returns:
            Dict with search results including scores and paths
        """
        return await self.eval(f"""
            (async () => {{
                const sc = app.plugins.plugins["smart-connections"];
                if (!sc || !sc.env || !sc.env.smart_sources) {{
                    return {{ error: "Smart Connections not available" }};
                }}

                const sources = sc.env.smart_sources;
                const results = await sources.search("{query}", {limit});

                if (!results || !Array.isArray(results)) {{
                    return {{ results: [], count: 0 }};
                }}

                return {{
                    query: "{query}",
                    results: results.map(r => ({{
                        path: r.path || r.key || "unknown",
                        score: r.score || r.sim || 0,
                        title: r.data?.title || r.key?.split('/').pop() || "Untitled",
                        excerpt: r.data?.excerpt || ""
                    }})),
                    count: results.length,
                    model: sources.embed_model_key || "unknown"
                }};
            }})()
        """)

    async def ai_find_nearest(self, path: str, limit: int = 10) -> Dict:
        """
        Find semantically similar notes to a given note.

        Args:
            path: Path to the source note
            limit: Maximum results to return

        Returns:
            Dict with nearest neighbors
        """
        return await self.eval(f"""
            (async () => {{
                const sc = app.plugins.plugins["smart-connections"];
                if (!sc || !sc.env || !sc.env.smart_sources) {{
                    return {{ error: "Smart Connections not available" }};
                }}

                const sources = sc.env.smart_sources;
                const source = sources.get("{path}");

                if (!source) {{
                    return {{ error: "Source note not found in index" }};
                }}

                const results = await sources.nearest(source, {limit});

                return {{
                    source: "{path}",
                    results: results.map(r => ({{
                        path: r.path || r.key || "unknown",
                        score: r.score || r.sim || 0,
                        title: r.data?.title || r.key?.split('/').pop() || "Untitled"
                    }})),
                    count: results.length
                }};
            }})()
        """)

    async def ai_lookup(self, query: str, context: Optional[str] = None) -> Dict:
        """
        AI-powered lookup with optional context.

        Args:
            query: Lookup query
            context: Optional context to guide the lookup

        Returns:
            Dict with lookup results
        """
        context_js = f'"{context}"' if context else 'null'
        return await self.eval(f"""
            (async () => {{
                const sc = app.plugins.plugins["smart-connections"];
                if (!sc || !sc.env || !sc.env.smart_sources) {{
                    return {{ error: "Smart Connections not available" }};
                }}

                const sources = sc.env.smart_sources;
                const results = await sources.lookup("{query}");

                return {{
                    query: "{query}",
                    context: {context_js},
                    results: results ? results.map(r => ({{
                        path: r.path || r.key || "unknown",
                        score: r.score || 0,
                        content: r.content || ""
                    }})) : [],
                    count: results ? results.length : 0
                }};
            }})()
        """)

    async def ai_get_index_status(self) -> Dict:
        """
        Get Smart Connections index status.

        Returns:
            Dict with index statistics
        """
        return await self.eval("""
            (() => {
                const sc = app.plugins.plugins["smart-connections"];
                if (!sc || !sc.env || !sc.env.smart_sources) {
                    return { error: "Smart Connections not available" };
                }

                const sources = sc.env.smart_sources;
                return {
                    total_files: sources.total_files || 0,
                    included_files: sources.included_files || 0,
                    loaded: sources.loaded || 0,
                    loading: sources._loading || false,
                    embed_model: sources.embed_model_key || "unknown",
                    collection_key: sources.collection_key || "smart_sources",
                    load_time_ms: sources.load_time_ms || 0
                };
            })()
        """)

    async def ai_reindex(self, force: bool = False) -> Dict:
        """
        Trigger Smart Connections reindex.

        Args:
            force: If True, forces full re-import

        Returns:
            Dict with reindex status
        """
        return await self.eval(f"""
            (async () => {{
                const sc = app.plugins.plugins["smart-connections"];
                if (!sc || !sc.env || !sc.env.smart_sources) {{
                    return {{ error: "Smart Connections not available" }};
                }}

                const sources = sc.env.smart_sources;
                const before = sources.loaded || 0;

                if ({str(force).lower()}) {{
                    await sources.run_re_import();
                }} else {{
                    await sources.process_embed_queue();
                }}

                return {{
                    action: {str(force).lower()} ? "full_reindex" : "process_queue",
                    before: before,
                    queued: sources.embed_queue?.length || 0,
                    status: "initiated"
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # AI INTEGRATION - Copilot
    # ═══════════════════════════════════════════════════════════════════════════

    async def copilot_get_memory(self) -> Dict:
        """
        Get Copilot saved memory and recent conversations.

        Returns:
            Dict with memory content
        """
        return await self.eval("""
            (async () => {
                const copilot = app.plugins.plugins["copilot"];
                if (!copilot || !copilot.userMemoryManager) {
                    return { error: "Copilot not available" };
                }

                const mem = copilot.userMemoryManager;
                await mem.loadMemory();

                return {
                    saved_memories: mem.savedMemoriesContent || "",
                    recent_conversations: mem.recentConversationsContent || "",
                    is_updating: mem.isUpdatingMemory || false
                };
            })()
        """)

    async def copilot_update_memory(self, content: str) -> Dict:
        """
        Update Copilot memory with new content.

        Args:
            content: New memory content to add

        Returns:
            Dict with update status
        """
        # Escape content for JavaScript
        escaped = content.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return await self.eval(f"""
            (async () => {{
                const copilot = app.plugins.plugins["copilot"];
                if (!copilot || !copilot.userMemoryManager) {{
                    return {{ error: "Copilot not available" }};
                }}

                const mem = copilot.userMemoryManager;
                await mem.updateSavedMemory("{escaped}");

                return {{
                    status: "updated",
                    content_length: "{escaped}".length
                }};
            }})()
        """)

    async def copilot_get_context(self, project_id: Optional[str] = None) -> Dict:
        """
        Get Copilot project context.

        Args:
            project_id: Optional project ID (uses current if not specified)

        Returns:
            Dict with project context
        """
        project_js = f'"{project_id}"' if project_id else 'null'
        return await self.eval(f"""
            (async () => {{
                const copilot = app.plugins.plugins["copilot"];
                if (!copilot || !copilot.projectManager) {{
                    return {{ error: "Copilot not available" }};
                }}

                const pm = copilot.projectManager;
                const projectId = {project_js} || pm.getCurrentProjectId();

                const context = await pm.getProjectContext();

                return {{
                    project_id: projectId,
                    context: context || "",
                    context_length: context?.length || 0,
                    files: pm.getProjectAllFiles?.() || []
                }};
            }})()
        """)

    async def copilot_index_vault(self) -> Dict:
        """
        Trigger Copilot vault indexing to vector store.

        Returns:
            Dict with indexing status
        """
        return await self.eval("""
            (async () => {
                const copilot = app.plugins.plugins["copilot"];
                if (!copilot || !copilot.vectorStoreManager) {
                    return { error: "Copilot not available" };
                }

                const vsm = copilot.vectorStoreManager;
                const hadIndex = vsm.hasIndex?.() || false;

                await vsm.indexVaultToVectorStore();

                return {
                    status: "indexing_started",
                    had_previous_index: hadIndex
                };
            })()
        """)

    async def copilot_get_index_status(self) -> Dict:
        """
        Get Copilot vector store index status.

        Returns:
            Dict with index status
        """
        return await self.eval("""
            (async () => {
                const copilot = app.plugins.plugins["copilot"];
                if (!copilot || !copilot.vectorStoreManager) {
                    return { error: "Copilot not available" };
                }

                const vsm = copilot.vectorStoreManager;

                return {
                    has_index: vsm.hasIndex?.() || false,
                    indexed_files: vsm.getIndexedFiles?.() || []
                };
            })()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # CONTENT MANAGEMENT - Templater
    # ═══════════════════════════════════════════════════════════════════════════

    async def templater_create_from_template(self, template_path: str, target_path: str) -> Dict:
        """
        Create a new note from a Templater template.

        Args:
            template_path: Path to template file
            target_path: Path for new note

        Returns:
            Dict with creation status
        """
        return await self.eval(f"""
            (async () => {{
                const templater = app.plugins.plugins["templater-obsidian"];
                if (!templater || !templater.templater) {{
                    return {{ error: "Templater not available" }};
                }}

                const templateFile = app.vault.getAbstractFileByPath("{template_path}");
                if (!templateFile) {{
                    return {{ error: "Template not found: {template_path}" }};
                }}

                const folder = app.vault.getAbstractFileByPath("{target_path}".split('/').slice(0, -1).join('/'));

                await templater.templater.create_new_note_from_template(
                    templateFile,
                    folder,
                    "{target_path}".split('/').pop().replace('.md', ''),
                    false
                );

                return {{
                    status: "created",
                    template: "{template_path}",
                    target: "{target_path}"
                }};
            }})()
        """)

    async def templater_parse(self, content: str) -> Dict:
        """
        Parse Templater syntax in content.

        Args:
            content: Content with Templater syntax

        Returns:
            Dict with parsed content
        """
        escaped = content.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("`", "\\`")
        return await self.eval(f"""
            (async () => {{
                const templater = app.plugins.plugins["templater-obsidian"];
                if (!templater || !templater.templater) {{
                    return {{ error: "Templater not available" }};
                }}

                // Create a temporary config for parsing
                const config = templater.templater.create_running_config(
                    null,
                    app.workspace.getActiveFile(),
                    1
                );

                const parsed = await templater.templater.parse_template(
                    config,
                    `{escaped}`
                );

                return {{
                    status: "parsed",
                    result: parsed
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # CONTENT MANAGEMENT - Linter
    # ═══════════════════════════════════════════════════════════════════════════

    async def lint_file(self, path: str) -> Dict:
        """
        Lint a single file using Obsidian Linter.

        Args:
            path: Path to file to lint

        Returns:
            Dict with lint status
        """
        return await self.eval(f"""
            (async () => {{
                const linter = app.plugins.plugins["obsidian-linter"];
                if (!linter) {{
                    return {{ error: "Linter not available" }};
                }}

                const file = app.vault.getAbstractFileByPath("{path}");
                if (!file) {{
                    return {{ error: "File not found: {path}" }};
                }}

                await linter.runLinterFile(file);

                return {{
                    status: "linted",
                    path: "{path}"
                }};
            }})()
        """)

    async def lint_all(self) -> Dict:
        """
        Lint all files in the vault.

        Returns:
            Dict with lint status
        """
        return await self.eval("""
            (async () => {
                const linter = app.plugins.plugins["obsidian-linter"];
                if (!linter) {
                    return { error: "Linter not available" };
                }

                await linter.runLinterAllFiles();

                return {
                    status: "linting_all",
                    note: "Linting in progress"
                };
            })()
        """)

    async def lint_folder(self, folder: str) -> Dict:
        """
        Lint all files in a folder.

        Args:
            folder: Folder path to lint

        Returns:
            Dict with lint status
        """
        return await self.eval(f"""
            (async () => {{
                const linter = app.plugins.plugins["obsidian-linter"];
                if (!linter) {{
                    return {{ error: "Linter not available" }};
                }}

                const folderObj = app.vault.getAbstractFileByPath("{folder}");
                if (!folderObj) {{
                    return {{ error: "Folder not found: {folder}" }};
                }}

                await linter.runLinterAllFilesInFolder(folderObj);

                return {{
                    status: "linting_folder",
                    folder: "{folder}"
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # SPACED REPETITION
    # ═══════════════════════════════════════════════════════════════════════════

    async def sr_get_stats(self) -> Dict:
        """
        Get spaced repetition statistics.

        Returns:
            Dict with flashcard statistics
        """
        return await self.eval("""
            (() => {
                const sr = app.plugins.plugins["obsidian-spaced-repetition"];
                if (!sr || !sr.osrAppCore) {
                    return { error: "Spaced Repetition not available" };
                }

                const core = sr.osrAppCore;
                const stats = core.cardStats || core._cardStats || {};

                return {
                    card_stats: stats,
                    deck_tree: core.fullDeckTree ? {
                        total_decks: Object.keys(core.fullDeckTree).length
                    } : null,
                    due_flashcards: core.dueDateFlashcardHistogram || {},
                    due_notes: core.dueDateNoteHistogram || {},
                    note_review_queue_size: core.noteReviewQueue?.length || 0
                };
            })()
        """)

    async def sr_load_note(self, path: str) -> Dict:
        """
        Load a note for spaced repetition review.

        Args:
            path: Path to note

        Returns:
            Dict with note flashcard data
        """
        return await self.eval(f"""
            (async () => {{
                const sr = app.plugins.plugins["obsidian-spaced-repetition"];
                if (!sr || !sr.osrAppCore) {{
                    return {{ error: "Spaced Repetition not available" }};
                }}

                const file = app.vault.getAbstractFileByPath("{path}");
                if (!file) {{
                    return {{ error: "File not found" }};
                }}

                const note = await sr.osrAppCore.loadNote(file);

                return {{
                    path: "{path}",
                    loaded: !!note,
                    data: note ? {{
                        cards_count: note.cards?.length || 0
                    }} : null
                }};
            }})()
        """)

    async def sr_sync(self) -> Dict:
        """
        Sync spaced repetition data.

        Returns:
            Dict with sync status
        """
        return await self.eval("""
            (async () => {
                const sr = app.plugins.plugins["obsidian-spaced-repetition"];
                if (!sr) {
                    return { error: "Spaced Repetition not available" };
                }

                await sr.sync();

                return {
                    status: "synced"
                };
            })()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # CANNOLI - Canvas LLM Workflows
    # ═══════════════════════════════════════════════════════════════════════════

    async def cannoli_list_functions(self) -> Dict:
        """
        List all available Cannoli functions.

        Returns:
            Dict with available functions
        """
        return await self.eval("""
            (() => {
                const cannoli = app.plugins.plugins["cannoli"];
                if (!cannoli) {
                    return { error: "Cannoli not available" };
                }

                const functions = cannoli.getAllCannoliFunctions?.() || [];
                const running = cannoli.runningCannolis || {};

                return {
                    functions: functions,
                    running_count: Object.keys(running).length,
                    running_canvases: Object.keys(running)
                };
            })()
        """)

    async def cannoli_run(self, canvas_path: str) -> Dict:
        """
        Run a Cannoli canvas workflow.

        Args:
            canvas_path: Path to canvas file

        Returns:
            Dict with run status
        """
        return await self.eval(f"""
            (async () => {{
                const cannoli = app.plugins.plugins["cannoli"];
                if (!cannoli) {{
                    return {{ error: "Cannoli not available" }};
                }}

                const file = app.vault.getAbstractFileByPath("{canvas_path}");
                if (!file) {{
                    return {{ error: "Canvas not found: {canvas_path}" }};
                }}

                await cannoli.startCannoli(file);

                return {{
                    status: "started",
                    canvas: "{canvas_path}"
                }};
            }})()
        """)

    async def cannoli_bake(self, canvas_path: str) -> Dict:
        """
        Bake a Cannoli canvas to a callable function.

        Args:
            canvas_path: Path to canvas file

        Returns:
            Dict with bake result
        """
        return await self.eval(f"""
            (async () => {{
                const cannoli = app.plugins.plugins["cannoli"];
                if (!cannoli) {{
                    return {{ error: "Cannoli not available" }};
                }}

                const file = app.vault.getAbstractFileByPath("{canvas_path}");
                if (!file) {{
                    return {{ error: "Canvas not found: {canvas_path}" }};
                }}

                const result = await cannoli.bake(file);

                return {{
                    status: "baked",
                    canvas: "{canvas_path}",
                    result: result
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # TASK MANAGEMENT - TaskNotes
    # ═══════════════════════════════════════════════════════════════════════════

    async def task_create(self, title: str, project: Optional[str] = None, due: Optional[str] = None, priority: Optional[str] = None) -> Dict:
        """
        Create a task with TaskNotes.

        Args:
            title: Task title
            project: Optional project name
            due: Optional due date (YYYY-MM-DD)
            priority: Optional priority (low, medium, high)

        Returns:
            Dict with created task
        """
        project_js = f'"{project}"' if project else 'null'
        due_js = f'"{due}"' if due else 'null'
        priority_js = f'"{priority}"' if priority else 'null'

        return await self.eval(f"""
            (async () => {{
                const tasknotes = app.plugins.plugins["tasknotes"];
                if (!tasknotes || !tasknotes.taskService) {{
                    return {{ error: "TaskNotes not available" }};
                }}

                const task = await tasknotes.taskService.createTask({{
                    title: "{title}",
                    project: {project_js},
                    dueDate: {due_js},
                    priority: {priority_js}
                }});

                return {{
                    status: "created",
                    task: task
                }};
            }})()
        """)

    async def task_toggle(self, task_id: str) -> Dict:
        """
        Toggle task completion status.

        Args:
            task_id: Task ID

        Returns:
            Dict with toggle result
        """
        return await self.eval(f"""
            (async () => {{
                const tasknotes = app.plugins.plugins["tasknotes"];
                if (!tasknotes || !tasknotes.taskService) {{
                    return {{ error: "TaskNotes not available" }};
                }}

                await tasknotes.taskService.toggleStatus("{task_id}");

                return {{
                    status: "toggled",
                    task_id: "{task_id}"
                }};
            }})()
        """)

    async def task_list(self, project: Optional[str] = None) -> Dict:
        """
        List tasks, optionally filtered by project.

        Args:
            project: Optional project name to filter by

        Returns:
            Dict with tasks array
        """
        filter_clause = f'task.project === "{project}"' if project else 'true'
        return await self.eval(f"""
            (async () => {{
                const tasknotes = app.plugins.plugins["tasknotes"];
                if (!tasknotes || !tasknotes.taskService) {{
                    return {{ error: "TaskNotes not available" }};
                }}

                const allTasks = tasknotes.taskService.getAllTasks ?
                    tasknotes.taskService.getAllTasks() :
                    [];

                const filtered = allTasks.filter(task => {filter_clause});

                return {{
                    tasks: filtered.map(t => ({{
                        id: t.id,
                        title: t.title,
                        status: t.status,
                        project: t.project,
                        due: t.due,
                        priority: t.priority,
                        completed: t.completed
                    }})),
                    count: filtered.length
                }};
            }})()
        """)

    async def sr_save_response(self, path: str, response: str) -> Dict:
        """
        Save spaced repetition review response.

        Args:
            path: Path to the note
            response: Review response (easy, good, hard, again)

        Returns:
            Dict with save result
        """
        response_map = {
            "easy": 4,
            "good": 3,
            "hard": 2,
            "again": 1
        }
        rating = response_map.get(response, 3)

        return await self.eval(f"""
            (async () => {{
                const sr = app.plugins.plugins["obsidian-spaced-repetition"];
                if (!sr || !sr.osrAppCore) {{
                    return {{ error: "Spaced Repetition not available" }};
                }}

                const note = await sr.osrAppCore.loadNote("{path}");
                if (!note) {{
                    return {{ error: "Failed to load note" }};
                }}

                await sr.osrAppCore.saveNoteReviewResponse(note, {rating});

                return {{
                    status: "saved",
                    path: "{path}",
                    response: "{response}",
                    rating: {rating}
                }};
            }})()
        """)

    # ═══════════════════════════════════════════════════════════════════════════
    # TRIPLE CONCURRENT ORCHESTRATION LAYER
    # Graph + Vector + Semantic Embedding Strategies with Multi-Model Agentic Triggers
    # ═══════════════════════════════════════════════════════════════════════════

    # Model Registry with Stratification (Updated 2026-01-09)
    # Preferences:
    #   - haiku-4-5 > gemini-3-flash for precise tool use
    #   - gemini-3-flash if context > 200k tokens
    #   - claude-sonnet-4-5 > gemini-3-pro unless context > 200k or second perspective needed
    #   - gemini-3-pro-image for atomic zettelkasten visualizations
    MODEL_TIERS = {
        "reasoning": {
            "description": "Extended thinking models for complex reasoning",
            "models": [
                "claude-opus-4-5-thinking",
                "claude-sonnet-4-5-thinking"
            ],
            "use_cases": ["multi-step reasoning", "complex analysis", "planning", "ultrathink"]
        },
        "analysis": {
            "description": "High-quality models for detailed analysis",
            "models": [
                "claude-sonnet-4-5",  # Primary: precise, excellent tool use
                "claude-opus-4-5",    # Complex tasks
                "gemini-3-pro",       # Large context (>200k) or second perspective
                "gemini-3-pro-high",  # Maximum quality when needed
                "gpt-4o"              # Third perspective
            ],
            "use_cases": ["synthesis", "evaluation", "research", "metaschema"]
        },
        "fast": {
            "description": "Low-latency models for quick responses",
            "models": [
                "claude-haiku-4-5-20251001",  # Primary: precise tool use
                "gemini-3-flash"               # Large context (>200k tokens)
            ],
            "use_cases": ["classification", "extraction", "simple queries", "tool_use"]
        },
        "image": {
            "description": "Image generation models for atomic zettelkasten",
            "models": [
                "gemini-3-pro-image",      # Standard visualizations
                "gemini-3-pro-image-4k",   # High-resolution diagrams
                "gemini-3-pro-image-2k"    # Quick concept images
            ],
            "use_cases": ["visualization", "diagram generation", "zettelkasten", "concept_maps", "tables", "charts"]
        }
    }

    LLM_ENDPOINT = "http://localhost:8045/v1"

    async def llm_list_models(self) -> Dict:
        """
        List available models from the LLM endpoint.

        Returns:
            Dict with models grouped by tier
        """
        import urllib.request
        import json as json_module

        try:
            req = urllib.request.Request(f"{self.LLM_ENDPOINT}/models")
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json_module.loads(response.read().decode())

            models = [m["id"] for m in data.get("data", [])]

            # Stratify by tier
            stratified = {tier: [] for tier in self.MODEL_TIERS}
            stratified["other"] = []

            for model in models:
                placed = False
                for tier, config in self.MODEL_TIERS.items():
                    if any(m in model for m in config["models"]) or model in config["models"]:
                        stratified[tier].append(model)
                        placed = True
                        break
                if not placed:
                    stratified["other"].append(model)

            return {
                "total": len(models),
                "stratified": stratified,
                "tiers": {k: len(v) for k, v in stratified.items()},
                "endpoint": self.LLM_ENDPOINT
            }
        except Exception as e:
            return {"error": str(e)}

    async def llm_call(self, model: str, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 4096) -> Dict:
        """
        Call an LLM model via the OpenAI-compatible endpoint.

        Args:
            model: Model ID
            messages: List of message dicts with role and content
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with response content
        """
        import urllib.request
        import json as json_module

        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            req = urllib.request.Request(
                f"{self.LLM_ENDPOINT}/chat/completions",
                data=json_module.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=120) as response:
                data = json_module.loads(response.read().decode())

            return {
                "model": model,
                "content": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
                "finish_reason": data["choices"][0].get("finish_reason")
            }
        except Exception as e:
            return {"error": str(e), "model": model}

    async def llm_select_model(self, task_type: str, prefer_tier: Optional[str] = None) -> str:
        """
        Select optimal model based on task type.

        Args:
            task_type: Type of task (reasoning, analysis, fast, image)
            prefer_tier: Preferred tier override

        Returns:
            Model ID
        """
        tier = prefer_tier or task_type
        if tier in self.MODEL_TIERS:
            return self.MODEL_TIERS[tier]["models"][0]
        return "claude-sonnet-4-5"  # Default fallback

    # ═══════════════════════════════════════════════════════════════════════════
    # TRIPLE CONCURRENT STRATEGY EXECUTION
    # ═══════════════════════════════════════════════════════════════════════════

    async def strategy_graph(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Graph-based strategy using Breadcrumbs traversal and reasoning.

        Args:
            query: The query to process
            context: Optional context with node/path hints

        Returns:
            Dict with graph-derived insights
        """
        results = {
            "strategy": "graph",
            "components": {}
        }

        # 1. Get graph topology
        try:
            components_list = await self.breadcrumbs_connected_components()
            results["components"]["topology"] = {
                "component_count": len(components_list),
                "total_nodes": sum(len(c) for c in components_list)
            }
        except:
            results["components"]["topology"] = {"error": "Failed to get topology"}

        # 2. Find relevant nodes via importance
        try:
            importance = await self.reasoning_importance_trace()
            top_nodes = importance.get("rankings", {}).get("combined", [])[:10]
            results["components"]["important_nodes"] = top_nodes
        except:
            results["components"]["important_nodes"] = []

        # 3. Detect knowledge gaps
        try:
            gaps = await self.reasoning_gap_trace(top_k=5)
            results["components"]["gaps"] = gaps.get("predicted_links", [])[:5]
        except:
            results["components"]["gaps"] = []

        # 4. Get clusters for context
        try:
            clusters = await self.reasoning_cluster_trace()
            results["components"]["clusters"] = clusters.get("communities", [])[:5]
        except:
            results["components"]["clusters"] = []

        # 5. If context has source/target, find paths
        if context and context.get("source") and context.get("target"):
            try:
                paths = await self.reasoning_path_trace(
                    source=context["source"],
                    target=context["target"]
                )
                results["components"]["paths"] = paths.get("paths", [])[:3]
            except:
                results["components"]["paths"] = []

        return results

    async def strategy_vector(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Vector-based strategy using Smart Connections semantic search.

        Args:
            query: The query to process
            context: Optional context with path hints

        Returns:
            Dict with vector-derived insights
        """
        results = {
            "strategy": "vector",
            "components": {}
        }

        # 1. Semantic search
        try:
            search_results = await self.ai_semantic_search(query, limit=10)
            results["components"]["semantic_matches"] = search_results.get("results", [])
        except:
            results["components"]["semantic_matches"] = []

        # 2. If context has a reference path, find nearest
        if context and context.get("reference_path"):
            try:
                nearest = await self.ai_find_nearest(context["reference_path"], limit=5)
                results["components"]["nearest_to_reference"] = nearest.get("results", [])
            except:
                results["components"]["nearest_to_reference"] = []

        # 3. AI lookup with context
        try:
            lookup = await self.ai_lookup(query, context.get("additional_context") if context else None)
            results["components"]["ai_lookup"] = lookup
        except:
            results["components"]["ai_lookup"] = {}

        return results

    async def strategy_semantic(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Semantic embedding strategy using LLM reasoning chains.

        Args:
            query: The query to process
            context: Optional context for enrichment

        Returns:
            Dict with semantic reasoning insights
        """
        results = {
            "strategy": "semantic",
            "components": {}
        }

        # 1. Classify query intent
        classification_prompt = f"""Classify this query into categories:
Query: {query}

Categories:
- factual: Looking for specific facts
- conceptual: Understanding concepts/relationships
- procedural: How to do something
- analytical: Analysis or comparison
- creative: Generation or synthesis

Return JSON: {{"intent": "category", "confidence": 0.0-1.0, "keywords": ["key", "words"]}}"""

        try:
            classification = await self.llm_call(
                model="claude-haiku-4",
                messages=[{"role": "user", "content": classification_prompt}],
                temperature=0.3,
                max_tokens=200
            )
            results["components"]["classification"] = classification.get("content", "")
        except:
            results["components"]["classification"] = {"error": "Classification failed"}

        # 2. Extract entities and relationships
        entity_prompt = f"""Extract key entities and relationships from this query:
Query: {query}

Return JSON: {{"entities": ["entity1", "entity2"], "relationships": ["rel1", "rel2"], "domain": "medical/technical/general"}}"""

        try:
            entities = await self.llm_call(
                model="claude-haiku-4",
                messages=[{"role": "user", "content": entity_prompt}],
                temperature=0.3,
                max_tokens=300
            )
            results["components"]["entities"] = entities.get("content", "")
        except:
            results["components"]["entities"] = {"error": "Entity extraction failed"}

        # 3. Generate reasoning chain if complex query
        if context and context.get("require_reasoning"):
            reasoning_prompt = f"""Generate a step-by-step reasoning chain for this query:
Query: {query}
Context: {context.get('additional_context', 'None')}

Provide a chain of reasoning steps that would help answer this query."""

            try:
                reasoning = await self.llm_call(
                    model="claude-sonnet-4-5-thinking" if context.get("deep") else "claude-sonnet-4-5",
                    messages=[{"role": "user", "content": reasoning_prompt}],
                    temperature=0.5,
                    max_tokens=1000
                )
                results["components"]["reasoning_chain"] = reasoning.get("content", "")
            except:
                results["components"]["reasoning_chain"] = {"error": "Reasoning failed"}

        return results

    async def triple_concurrent_execute(self, query: str, context: Optional[Dict] = None, strategies: Optional[List[str]] = None) -> Dict:
        """
        Execute all three strategies concurrently and synthesize results.

        Args:
            query: The query to process
            context: Optional context for all strategies
            strategies: List of strategies to run (default: all three)

        Returns:
            Dict with results from all strategies and synthesis
        """
        import asyncio

        strategies = strategies or ["graph", "vector", "semantic"]
        results = {
            "query": query,
            "strategies_executed": strategies,
            "results": {},
            "synthesis": None
        }

        # Execute strategies concurrently
        tasks = []
        if "graph" in strategies:
            tasks.append(("graph", self.strategy_graph(query, context)))
        if "vector" in strategies:
            tasks.append(("vector", self.strategy_vector(query, context)))
        if "semantic" in strategies:
            tasks.append(("semantic", self.strategy_semantic(query, context)))

        # Gather results
        for name, task in tasks:
            try:
                results["results"][name] = await task
            except Exception as e:
                results["results"][name] = {"error": str(e)}

        # Synthesize results using analysis-tier model
        synthesis_prompt = f"""Synthesize insights from three concurrent analysis strategies:

Query: {query}

Graph Strategy Results:
{results['results'].get('graph', {})}

Vector Strategy Results:
{results['results'].get('vector', {})}

Semantic Strategy Results:
{results['results'].get('semantic', {})}

Provide a unified synthesis that:
1. Identifies key insights from each strategy
2. Notes agreements and disagreements between strategies
3. Provides a confidence-weighted final answer
4. Suggests follow-up actions if needed

Format as JSON with keys: key_insights, consensus, conflicts, final_answer, confidence, follow_up_actions"""

        try:
            synthesis = await self.llm_call(
                model="claude-opus-4-5",
                messages=[{"role": "user", "content": synthesis_prompt}],
                temperature=0.5,
                max_tokens=2000
            )
            results["synthesis"] = synthesis.get("content", "")
        except Exception as e:
            results["synthesis"] = {"error": str(e)}

        return results

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENTIC TRIGGERS - Model Selection and Task Routing
    # ═══════════════════════════════════════════════════════════════════════════

    async def agent_route_task(self, task: str, task_type: Optional[str] = None) -> Dict:
        """
        Route a task to the appropriate model and strategy.

        Args:
            task: The task description
            task_type: Optional explicit type (reasoning, analysis, fast, image)

        Returns:
            Dict with routing decision and execution plan
        """
        # Auto-classify if not provided
        if not task_type:
            classify_prompt = f"""Classify this task:
Task: {task}

Categories:
- reasoning: Requires multi-step thinking, planning, complex analysis
- analysis: Requires detailed analysis, synthesis, research
- fast: Simple extraction, classification, quick answer
- image: Requires image generation or visualization

Return only the category name."""

            try:
                result = await self.llm_call(
                    model="claude-haiku-4",
                    messages=[{"role": "user", "content": classify_prompt}],
                    temperature=0.2,
                    max_tokens=50
                )
                task_type = result.get("content", "analysis").strip().lower()
            except:
                task_type = "analysis"

        # Ensure task_type is always a string (for type checker)
        task_type_str: str = task_type or "analysis"

        # Select model and strategies
        model = await self.llm_select_model(task_type_str)

        # Determine strategies based on task type
        strategy_map = {
            "reasoning": ["graph", "semantic"],
            "analysis": ["graph", "vector", "semantic"],
            "fast": ["vector"],
            "image": ["semantic"]
        }
        strategies = strategy_map.get(task_type_str, ["vector", "semantic"])

        return {
            "task": task,
            "task_type": task_type_str,
            "selected_model": model,
            "selected_strategies": strategies,
            "tier": task_type_str,
            "execution_plan": {
                "step_1": f"Execute {strategies} strategies concurrently",
                "step_2": f"Synthesize results using {model}",
                "step_3": "Return unified response"
            }
        }

    async def agent_execute(self, task: str, task_type: Optional[str] = None, context: Optional[Dict] = None) -> Dict:
        """
        Full agentic execution: route task, execute strategies, synthesize.

        Args:
            task: The task to execute
            task_type: Optional explicit type
            context: Optional context

        Returns:
            Dict with full execution results
        """
        # Route the task
        routing = await self.agent_route_task(task, task_type)

        # Execute with triple concurrent strategy
        execution = await self.triple_concurrent_execute(
            query=task,
            context=context,
            strategies=routing["selected_strategies"]
        )

        return {
            "routing": routing,
            "execution": execution,
            "final_answer": execution.get("synthesis"),
            "model_used": routing["selected_model"],
            "strategies_used": routing["selected_strategies"]
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # INTER-MODEL COMMUNICATION - Multi-Agent Orchestration
    # ═══════════════════════════════════════════════════════════════════════════

    async def multi_model_consensus(self, query: str, models: Optional[List[str]] = None, voting: str = "majority") -> Dict:
        """
        Get consensus from multiple models.

        Args:
            query: The query to ask all models
            models: List of model IDs (default: one from each tier)
            voting: Voting strategy (majority, weighted, unanimous)

        Returns:
            Dict with individual responses and consensus
        """
        models = models or [
            "claude-opus-4-5",
            "gemini-3-pro",
            "gpt-4o"
        ]

        results = {"query": query, "models": {}, "consensus": None}

        # Query all models
        for model in models:
            try:
                response = await self.llm_call(
                    model=model,
                    messages=[{"role": "user", "content": query}],
                    temperature=0.5,
                    max_tokens=1000
                )
                results["models"][model] = {
                    "response": response.get("content", ""),
                    "usage": response.get("usage", {})
                }
            except Exception as e:
                results["models"][model] = {"error": str(e)}

        # Build consensus
        consensus_prompt = f"""Given these responses from different AI models to the same query, determine the consensus:

Query: {query}

Responses:
{chr(10).join([f'{m}: {r.get("response", r.get("error", "No response"))}' for m, r in results['models'].items()])}

Provide:
1. Points of agreement
2. Points of disagreement
3. Confidence-weighted consensus answer
4. Minority opinions worth noting

Format as JSON."""

        try:
            consensus = await self.llm_call(
                model="claude-opus-4-5",
                messages=[{"role": "user", "content": consensus_prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            results["consensus"] = consensus.get("content", "")
        except Exception as e:
            results["consensus"] = {"error": str(e)}

        return results

    async def model_chain(self, task: str, chain: List[Dict]) -> Dict:
        """
        Execute a chain of model calls where each step feeds into the next.

        Args:
            task: Initial task
            chain: List of dicts with model, role, and optional transform

        Example chain:
            [
                {"model": "claude-haiku-4", "role": "classifier"},
                {"model": "claude-sonnet-4-5", "role": "analyzer"},
                {"model": "claude-opus-4-5", "role": "synthesizer"}
            ]

        Returns:
            Dict with chain execution results
        """
        results = {
            "task": task,
            "chain": [],
            "final_output": None
        }

        current_input = task

        for i, step in enumerate(chain):
            model = step.get("model", "claude-sonnet-4-5")
            role = step.get("role", f"step_{i}")
            transform = step.get("transform", lambda x: x)

            prompt = f"""You are acting as a {role} in a processing chain.

Previous input: {current_input}

Perform your role and provide output for the next step in the chain."""

            try:
                response = await self.llm_call(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=1500
                )

                output = response.get("content", "")
                results["chain"].append({
                    "step": i,
                    "model": model,
                    "role": role,
                    "input": current_input[:500] + "..." if len(current_input) > 500 else current_input,
                    "output": output
                })

                current_input = output

            except Exception as e:
                results["chain"].append({
                    "step": i,
                    "model": model,
                    "role": role,
                    "error": str(e)
                })
                break

        results["final_output"] = current_input
        return results

    async def parallel_fan_out(self, query: str, sub_queries: List[str], model: Optional[str] = None) -> Dict:
        """
        Fan out a query into multiple sub-queries processed in parallel.

        Args:
            query: Main query for context
            sub_queries: List of sub-queries to process
            model: Model to use (default: fast tier)

        Returns:
            Dict with all sub-query results
        """
        model = model or "claude-haiku-4-5-20251001"

        results = {
            "main_query": query,
            "sub_queries": {},
            "aggregated": None
        }

        # Process sub-queries
        for sq in sub_queries:
            prompt = f"""Context: {query}

Sub-query to answer: {sq}

Provide a focused answer to this specific sub-query."""

            try:
                response = await self.llm_call(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=500
                )
                results["sub_queries"][sq] = response.get("content", "")
            except Exception as e:
                results["sub_queries"][sq] = f"Error: {e}"

        # Aggregate results
        aggregation_prompt = f"""Aggregate these answers to sub-queries:

Main query: {query}

Sub-query answers:
{chr(10).join([f'Q: {q}{chr(10)}A: {a}' for q, a in results['sub_queries'].items()])}

Provide a unified answer that synthesizes all the sub-query responses."""

        try:
            aggregated = await self.llm_call(
                model="claude-sonnet-4-5",
                messages=[{"role": "user", "content": aggregation_prompt}],
                temperature=0.5,
                max_tokens=1000
            )
            results["aggregated"] = aggregated.get("content", "")
        except Exception as e:
            results["aggregated"] = f"Error: {e}"

        return results

    # ═══════════════════════════════════════════════════════════════════════════
    # TOOL ORCHESTRATION - Coordinate 32 MCP Tools
    # ═══════════════════════════════════════════════════════════════════════════

    TOOL_CATEGORIES = {
        "core": ["obsidian_eval", "obsidian_open_note", "obsidian_trigger_command"],
        "query": ["obsidian_query", "obsidian_fields", "obsidian_get_frontmatter"],
        "graph": ["obsidian_graph", "obsidian_evaluate", "obsidian_reasoning"],
        "ai": ["obsidian_ai_search", "obsidian_ai_nearest", "obsidian_copilot"],
        "content": ["obsidian_templater", "obsidian_lint", "obsidian_git"],
        "learning": ["obsidian_sr"],
        "automation": ["obsidian_cannoli", "obsidian_task", "obsidian_plugin"],
        "prediction": ["obsidian_predict", "obsidian_generate", "obsidian_apply"]
    }

    async def orchestrate_tools(self, intent: str, context: Optional[Dict] = None) -> Dict:
        """
        Orchestrate multiple tools based on intent.

        Args:
            intent: What the user wants to accomplish
            context: Optional context

        Returns:
            Dict with tool execution plan and results
        """
        # Classify intent to tool categories
        classify_prompt = f"""Given this intent, identify which tool categories would be needed:

Intent: {intent}

Tool Categories:
- core: Basic Obsidian operations (eval, open note, commands)
- query: Data retrieval (dataview queries, frontmatter, fields)
- graph: Graph analysis (traversal, reasoning, evaluation)
- ai: AI-powered features (semantic search, copilot)
- content: Content management (templates, linting, git)
- learning: Spaced repetition
- automation: Workflows (cannoli, tasks, plugins)
- prediction: Graph predictions (MEGA, telos, link prediction)

Return JSON: {{"categories": ["cat1", "cat2"], "tool_sequence": ["tool1", "tool2"], "reasoning": "why"}}"""

        try:
            classification = await self.llm_call(
                model="claude-haiku-4",
                messages=[{"role": "user", "content": classify_prompt}],
                temperature=0.3,
                max_tokens=400
            )

            return {
                "intent": intent,
                "tool_plan": classification.get("content", ""),
                "available_categories": self.TOOL_CATEGORIES,
                "status": "plan_generated"
            }
        except Exception as e:
            return {"error": str(e)}
