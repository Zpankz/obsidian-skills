from mcp.server.fastmcp import FastMCP
from .client import CDPClient
from .launcher import ObsidianLauncher
from .security import SecurityGuard
from .sdk import ObsidianClient
import json

# Initialize components
mcp = FastMCP("obsidian-devtools")
launcher = ObsidianLauncher()
client = CDPClient()
sdk = ObsidianClient(client)
security = SecurityGuard(safe_mode=True)

import logging
logger = logging.getLogger(__name__)

def main():
    mcp.run()

@mcp.tool()
async def obsidian_launch_debug(port: int = 9222, restart: bool = False) -> str:
    """Connects to Obsidian with remote debugging enabled."""
    if restart:
        await launcher.kill()

    launched = await launcher.ensure_running(port=port)
    if not launched and restart:
        return "Failed to launch Obsidian with debug flags."

    client.port = port
    client.base_url = f"http://localhost:{port}"

    try:
        await client.connect()
        vault = await sdk.get_vault_name()
        return f"Connected to Obsidian on port {port}. Vault: '{vault}'"
    except Exception as e:
        return f"Failed to connect: {e}"

@mcp.tool()
async def obsidian_eval(expression: str, await_promise: bool = True) -> str:
    """Executes JavaScript code in the Obsidian app context."""
    is_valid, error_msg = security.validate_eval(expression)
    if not is_valid:
        return "Security Violation: Expression contains blocked modules or patterns."

    try:
        result = await sdk.eval(expression, await_promise=await_promise)
        return str(result)
    except Exception as e:
        return f"Error executing script: {str(e)}"

@mcp.tool()
async def obsidian_inspect_dom(selector: str = "body") -> str:
    """Gets a simplified snapshot of the DOM structure."""
    from .dom import DOMInspector
    code = DOMInspector.get_inspection_script(selector)
    return await sdk.eval(code)

@mcp.tool()
async def obsidian_list_plugins() -> str:
    """List all enabled plugins."""
    try:
        plugins = await sdk.list_plugins()
        return "\\n".join([f"- {p['name']} ({p['version']}) [{p['id']}]" for p in plugins])
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_open_note(path: str, new_leaf: bool = False) -> str:
    """Open a note in the active vault."""
    try:
        await sdk.open_note(path, new_leaf)
        return f"Opened: {path}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_trigger_command(command_id: str) -> str:
    """Trigger an Obsidian command by ID."""
    try:
        success = await sdk.trigger_command(command_id)
        return "Command executed." if success else "Command not found."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_create_canvas(path: str, nodes_json: str, edges_json: str = "[]") -> str:
    """Create a new .canvas file."""
    try:
        nodes = json.loads(nodes_json)
        edges = json.loads(edges_json)
        await sdk.create_canvas(path, nodes, edges)
        return f"Created canvas at {path}"
    except Exception as e:
        return f"Error creating canvas: {e}"

@mcp.tool()
async def obsidian_graph_zoom(level: float) -> str:
    """Zoom the active graph view (1.0 = 100%)."""
    try:
        success = await sdk.graph_zoom_to(level)
        return "Zoomed graph." if success else "No active graph view found."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_get_frontmatter(path: str) -> str:
    """Get the frontmatter of a file."""
    try:
        fm = await sdk.get_frontmatter(path)
        return json.dumps(fm, indent=2) if fm else "No frontmatter found."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_update_frontmatter(path: str, key: str, value: str) -> str:
    """Update a frontmatter key. Value should be JSON-parseable string."""
    try:
        try:
            val = json.loads(value)
        except:
            val = value # Treat as string if not JSON
        await sdk.update_frontmatter(path, key, val)
        return f"Updated {key} in {path}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_discover_api(path: str) -> str:
    """
    Discover methods and properties of an object path (e.g. 'app.plugins.plugins.graph').
    Useful for reverse-engineering internal APIs.
    """
    try:
        props = await sdk.discover_object(path)
        output = [f"API Discovery for: {path}"]

        # Sort keys
        keys = sorted(props.keys())

        # Group by type
        methods = [k for k in keys if props[k] == 'function']
        objects = [k for k in keys if props[k] == 'object']
        others = [k for k in keys if props[k] not in ['function', 'object']]

        if methods:
            output.append("\nMethods:")
            output.extend([f"  ƒ {k}()" for k in methods])

        if objects:
            output.append("\nObjects:")
            output.extend([f"  📦 {k}" for k in objects])

        if others:
            output.append("\nProperties:")
            output.extend([f"  • {k}: {props[k]}" for k in others])

        return "\n".join(output)
    except Exception as e:
        return f"Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# MVP UNIFIED TOOLS (Generic Plugin Caller Pattern)
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_plugin(plugin: str, method: str, args: str = "{}") -> str:
    """
    Generic plugin method caller. Call ANY plugin API without dedicated tools.

    Args:
        plugin: Plugin ID (e.g., "dataview", "obsidian-git", "smart-connections")
        method: Dot-notation path to method (e.g., "api.query", "commit")
        args: JSON string of arguments to pass (e.g., '{"message": "test"}')

    Examples:
        obsidian_plugin("dataview", "api.query", '{"query": "FROM #tag"}')
        obsidian_plugin("obsidian-git", "push", "{}")
        obsidian_plugin("smart-connections", "env.smart_sources.search", '{"query": "test"}')
    """
    try:
        args_obj = json.loads(args) if args else {}
        result = await sdk.call_plugin(plugin, method, args_obj)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_query(action: str, query: str = "", source: str = "") -> str:
    """
    Unified Dataview query tool.

    Actions:
        - dql: Execute a Dataview DQL query
        - pages: Get pages matching source (folder, tag, or link)

    Examples:
        obsidian_query("dql", query="TABLE file.name FROM #concept")
        obsidian_query("pages", source='"Concepts/Maternal-Physiology"')
        obsidian_query("pages", source="#cardiovascular")
    """
    try:
        if action == "dql":
            result = await sdk.dataview_query(query)
        elif action == "pages":
            result = await sdk.dataview_pages(source)
        else:
            return f"Unknown action: {action}. Available: dql, pages"
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_graph(action: str, node: str = "", target: str = "", depth: int = 2, edge_type: str = "", k: int = 5, limit: int = 100, damping: float = 0.85, resolution: float = 1.0) -> str:
    """
    Unified Breadcrumbs graph navigation tool with advanced graphology operations.

    Actions:
        NAVIGATION:
        - neighbors: Get neighbors of a node (append :in or :out for direction)
        - paths: Find all paths between two nodes (Breadcrumbs DFS)
        - shortest: Find shortest path between two nodes (BFS)
        - traverse: Traverse graph from node up to depth (default: 2)
        - subgraph: Extract subgraph for nodes (comma-separated list)
        - export: Export the full graph as JSON

        CENTRALITY:
        - degree: Degree centrality (connection count)
        - betweenness: Betweenness centrality (bridge nodes)
        - closeness: Closeness centrality (average distance)
        - pagerank: PageRank centrality (importance via links)

        COMMUNITY DETECTION:
        - louvain: Louvain community detection (modularity optimization)
        - label_propagation: Label propagation communities (faster)

        LINK PREDICTION:
        - predict_links: Predict missing links (common neighbors, Jaccard, Adamic-Adar)

        PATH ANALYSIS:
        - k_shortest: Find k shortest paths (Yen's algorithm)
        - all_paths: Find all paths up to max length
        - components: Get connected components (sorted by size)
        - stats: Get detailed statistics for a node
        - filter: Filter nodes by edge type

    Examples:
        # Navigation
        obsidian_graph("neighbors", node="Cardiac-Output-Pregnancy:out")
        obsidian_graph("shortest", node="Cardiac-Output", target="Aortocaval-Compression")

        # Centrality
        obsidian_graph("degree")
        obsidian_graph("betweenness")
        obsidian_graph("pagerank", damping=0.85)

        # Communities
        obsidian_graph("louvain", resolution=1.0)
        obsidian_graph("label_propagation")

        # Link Prediction
        obsidian_graph("predict_links", node="Cardiac-Output", k=10)

        # Path Analysis
        obsidian_graph("k_shortest", node="Progesterone", target="Ion-Trapping", k=5)
        obsidian_graph("all_paths", node="Progesterone", target="Ion-Trapping", limit=20)
    """
    try:
        # === NAVIGATION ===
        if action == "neighbors":
            direction = "all"
            if ":" in node:
                node, direction = node.rsplit(":", 1)
            result = await sdk.breadcrumbs_neighbors(node, direction)

        elif action == "paths":
            result = await sdk.breadcrumbs_paths(node, target)

        elif action == "shortest":
            result = await sdk.breadcrumbs_shortest_path(node, target)

        elif action == "export":
            result = await sdk.breadcrumbs_export()

        elif action == "traverse":
            direction = "out"
            if ":" in node:
                node, direction = node.rsplit(":", 1)
            result = await sdk.breadcrumbs_traverse(node, depth, direction)

        elif action == "subgraph":
            nodes = [n.strip() for n in node.split(",")]
            result = await sdk.breadcrumbs_subgraph(nodes)

        # === CENTRALITY ===
        elif action == "degree":
            result = await sdk.graph_degree_centrality()

        elif action == "betweenness":
            result = await sdk.graph_betweenness_centrality()

        elif action == "closeness":
            result = await sdk.graph_closeness_centrality()

        elif action == "pagerank":
            result = await sdk.graph_pagerank(damping=damping)

        # === COMMUNITY DETECTION ===
        elif action == "louvain":
            result = await sdk.graph_louvain(resolution=resolution)

        elif action == "label_propagation":
            result = await sdk.graph_label_propagation()

        # === LINK PREDICTION ===
        elif action == "predict_links":
            result = await sdk.graph_link_prediction(node=node if node else None, top_k=k)

        # === PATH ANALYSIS ===
        elif action == "k_shortest":
            result = await sdk.graph_k_shortest_paths(node, target, k=k)

        elif action == "all_paths":
            result = await sdk.graph_all_paths(node, target, max_length=depth, limit=limit)

        elif action == "components":
            result = await sdk.breadcrumbs_connected_components()

        elif action == "stats":
            result = await sdk.breadcrumbs_node_stats(node)

        elif action == "filter":
            direction = "out"
            if ":" in node and node:
                node, direction = node.rsplit(":", 1)
            result = await sdk.breadcrumbs_filter_nodes(edge_type if edge_type else None, direction)

        else:
            return f"""Unknown action: {action}.

Available actions:
  NAVIGATION: neighbors, paths, shortest, traverse, subgraph, export
  CENTRALITY: degree, betweenness, closeness, pagerank
  COMMUNITIES: louvain, label_propagation
  LINK PREDICTION: predict_links
  PATH ANALYSIS: k_shortest, all_paths, components, stats, filter"""

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_batch_frontmatter(path: str, updates: str) -> str:
    """
    Update multiple frontmatter keys at once.

    Args:
        path: Path to the file in the vault
        updates: JSON string of key-value pairs to update

    Example:
        obsidian_batch_frontmatter(
            "Concepts/Cardiac-Output.md",
            '{"mastery_level": "competent", "last_reviewed": "2024-01-09", "exam_frequency": 8}'
        )
    """
    try:
        updates_obj = json.loads(updates)
        await sdk.batch_update_frontmatter(path, updates_obj)
        return f"Updated {len(updates_obj)} fields in {path}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_git(action: str, args: str = "{}") -> str:
    """
    Unified Git operations via obsidian-git plugin.

    Actions:
        - commit: Commit changes (args: {"message": "commit message"})
        - push: Push to remote
        - pull: Pull from remote
        - stage: Stage a file (args: {"path": "file.md"})
        - unstage: Unstage a file (args: {"path": "file.md"})
        - status: Get repository status

    Examples:
        obsidian_git("commit", '{"message": "Update concepts"}')
        obsidian_git("push")
        obsidian_git("status")
    """
    try:
        args_obj = json.loads(args) if args else {}
        result = await sdk.git_action(action, args_obj)
        return json.dumps(result, indent=2, default=str) if result else f"Git {action} completed."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_fields(action: str, path: str, field: str = "", value: str = "") -> str:
    """
    Metadata Menu field operations.

    Actions:
        - get: Get all fields for a file
        - set: Update a specific field value

    Examples:
        obsidian_fields("get", "Concepts/Cardiac-Output.md")
        obsidian_fields("set", "Concepts/Cardiac-Output.md", field="mastery_level", value='"competent"')
    """
    try:
        if action == "get":
            result = await sdk.metadata_get_fields(path)
            return json.dumps(result, indent=2, default=str)
        elif action == "set":
            value_obj = json.loads(value) if value else None
            await sdk.metadata_update_field(path, field, value_obj)
            return f"Updated {field} in {path}"
        else:
            return f"Unknown action: {action}. Available: get, set"
    except Exception as e:
        return f"Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# GRAPH REASONING TOOLS (Multihop Reasoning Framework)
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_evaluate(mode: str = "standard", source: str = "", target: str = "") -> str:
    """
    Unified graph reasoning evaluation with multihop analysis.

    Modes:
        - quick: Importance + Clusters only (~2s)
        - standard: All primitives (~5s)
        - comprehensive: Primitives + Chains + Metaschema (~10s)
        - deep: Everything + Path analysis for source/target (~15s)

    Args:
        mode: Evaluation depth (quick, standard, comprehensive, deep)
        source: Source concept for path analysis (deep mode)
        target: Target concept for path analysis (deep mode)

    Returns:
        Aggregated insights with cross-validated findings, quality scores,
        and actionable recommendations.

    Examples:
        obsidian_evaluate("quick")
        obsidian_evaluate("standard")
        obsidian_evaluate("comprehensive")
        obsidian_evaluate("deep", source="Progesterone-Vasodilation", target="Ion-Trapping-Fetus")
    """
    try:
        source_val = source if source else None
        target_val = target if target else None
        result = await sdk.evaluate(mode=mode, source=source_val, target=target_val)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def obsidian_reasoning(operation: str, concept: str = "", concepts: str = "", source: str = "", target: str = "", top_k: int = 20, resolution: float = 1.0, max_paths: int = 10) -> str:
    """
    Individual graph reasoning operations for fine-grained analysis.

    Operations:
        PRIMITIVES (Level 1):
        - importance: Multi-metric importance analysis (PageRank, Betweenness, Degree, Closeness)
        - gaps: Knowledge gap detection (link prediction, community gaps, isolated nodes)
        - clusters: Thematic cluster analysis (Louvain communities, centroids, boundaries)
        - paths: Learning path analysis between source and target concepts
        - bridges: Bridge concept identification (articulation points)

        CHAINS (Level 2):
        - prerequisite: Trace learning dependencies for a concept
        - mastery: Evaluate learning coverage and mastery progression

        METASCHEMA (Level 3):
        - metaschema: Extract topology, semantics, and dynamics insights

    Args:
        operation: Which reasoning operation to run
        concept: Single concept for prerequisite chain
        concepts: JSON array of concepts for mastery chain (e.g., '["Concept1", "Concept2"]')
        source: Source concept for path analysis
        target: Target concept for path analysis
        top_k: Number of top results for gap detection (default: 20)
        resolution: Resolution parameter for Louvain clustering (default: 1.0)
        max_paths: Maximum paths to return for path analysis (default: 10)

    Examples:
        obsidian_reasoning("importance")
        obsidian_reasoning("gaps", top_k=10)
        obsidian_reasoning("clusters", resolution=1.5)
        obsidian_reasoning("paths", source="Progesterone-Vasodilation", target="Ion-Trapping-Fetus")
        obsidian_reasoning("bridges")
        obsidian_reasoning("prerequisite", concept="Aortocaval-Compression")
        obsidian_reasoning("mastery", concepts='["Cardiac-Output-Pregnancy", "Aortocaval-Compression"]')
        obsidian_reasoning("metaschema")
    """
    try:
        if operation == "importance":
            result = await sdk.reasoning_importance_trace()
        elif operation == "gaps":
            result = await sdk.reasoning_gap_trace(top_k=top_k)
        elif operation == "clusters":
            result = await sdk.reasoning_cluster_trace(resolution=resolution)
        elif operation == "paths":
            if not source or not target:
                return "Error: 'paths' operation requires both 'source' and 'target' parameters"
            result = await sdk.reasoning_path_trace(source=source, target=target, max_paths=max_paths)
        elif operation == "bridges":
            result = await sdk.reasoning_bridge_trace()
        elif operation == "prerequisite":
            if not concept:
                return "Error: 'prerequisite' operation requires 'concept' parameter"
            result = await sdk.reasoning_prerequisite_chain(concept=concept)
        elif operation == "mastery":
            concepts_list = json.loads(concepts) if concepts else None
            result = await sdk.reasoning_mastery_chain(concepts=concepts_list)
        elif operation == "metaschema":
            result = await sdk.reasoning_metaschema()
        else:
            return f"""Unknown operation: {operation}.

Available operations:
  PRIMITIVES: importance, gaps, clusters, paths, bridges
  CHAINS: prerequisite, mastery
  METASCHEMA: metaschema

For comprehensive analysis, use obsidian_evaluate() instead."""

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_predict(
    operation: str,
    threshold: float = 0.3
) -> str:
    """
    Unified prediction tool for graph intelligence.

    Operations:
        - mega: Compute MEGA invariants (η, φ, κ, n, mega_score)
        - homology: Compute persistent homology (H0, H1, H2 Betti numbers)
        - bisimulation: Compute k-bisimulation structural equivalence classes
        - telos: Classify nodes into τ Strategic, λ Tactical, ο Operational
        - links: Predict new links using dialectical synthesis (Σ→Τ→Δ→Ρ)

    Args:
        operation: Which prediction to run
        threshold: Minimum score for link predictions (default: 0.3)

    Examples:
        obsidian_predict("mega")
        obsidian_predict("links", threshold=0.2)
        obsidian_predict("telos")
    """
    try:
        if operation == "mega":
            result = await sdk.compute_mega_invariants()
        elif operation == "homology":
            result = await sdk.compute_persistent_homology()
        elif operation == "bisimulation":
            result = await sdk.k_bisimulation_classes()
        elif operation == "telos":
            result = await sdk.compute_telos_hierarchy()
        elif operation == "links":
            result = await sdk.dialectical_link_synthesis(threshold=threshold)
        else:
            return f"""Unknown operation: {operation}.

Available operations:
  - mega: MEGA invariants (η, φ, κ, n)
  - homology: Persistent homology (H0, H1, H2)
  - bisimulation: k-bisimulation compression
  - telos: Three-level hierarchy classification
  - links: Dialectical link predictions"""

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_generate(
    output_type: str,
    name: str = "Generated",
    layout: str = "telos"
) -> str:
    """
    Generate canvas or base files from graph data.

    Types:
        - canvas: Generate canvas JSON with Telos-hierarchical layout
        - base: Generate .base file with MEGA formulas and views

    Args:
        output_type: "canvas" or "base"
        name: File name for base files
        layout: Canvas layout ("telos", "force", "radial")

    Examples:
        obsidian_generate("canvas")
        obsidian_generate("base", name="Maternal-MEGA-Analysis")
    """
    try:
        if output_type == "canvas":
            result = await sdk.generate_canvas_from_graph(layout=layout)
        elif output_type == "base":
            result = await sdk.generate_base_file(name=name)
        else:
            return f"Unknown output type: {output_type}. Use 'canvas' or 'base'."

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_apply(
    operation: str,
    canvas_path: str = "Maternal-Cardiovascular-Network.canvas",
    predictions_json: str = "[]",
    dry_run: bool = True
) -> str:
    """
    Apply predictions to files.

    Operations:
        - frontmatter: Apply link predictions to frontmatter (up/down/same fields)
        - canvas: Add predicted edges to existing canvas file

    Args:
        operation: "frontmatter" or "canvas"
        canvas_path: Path to canvas file (for canvas operation)
        predictions_json: JSON array of predictions (source, target, edgeType, field)
        dry_run: If True, show what would change without applying

    Examples:
        obsidian_apply("canvas", canvas_path="Network.canvas", predictions_json='[{"source":"A","target":"B","edgeType":"same"}]')
    """
    try:
        predictions = json.loads(predictions_json)

        if operation == "frontmatter":
            result = await sdk.apply_link_predictions(predictions=predictions, dry_run=dry_run)
        elif operation == "canvas":
            result = await sdk.add_predicted_edges_to_canvas(canvas_path=canvas_path, predictions=predictions)
        else:
            return f"Unknown operation: {operation}. Use 'frontmatter' or 'canvas'."

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# AI INTEGRATION TOOLS (Smart Connections + Copilot)
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_ai_search(query: str, limit: int = 10) -> str:
    """
    Semantic search using Smart Connections embeddings.

    Args:
        query: Search query (semantic, not keyword-based)
        limit: Maximum results to return (default: 10)

    Examples:
        obsidian_ai_search("cardiac output physiology", limit=5)
        obsidian_ai_search("mechanisms of drug transfer")
    """
    try:
        result = await sdk.ai_semantic_search(query, limit)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_ai_nearest(path: str, limit: int = 10) -> str:
    """
    Find semantically similar notes to a given note.

    Args:
        path: Path to the source note
        limit: Maximum results to return (default: 10)

    Examples:
        obsidian_ai_nearest("Concepts/Cardiac-Output-Pregnancy.md", limit=5)
    """
    try:
        result = await sdk.ai_find_nearest(path, limit)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_ai_lookup(query: str, context: str = "") -> str:
    """
    AI-powered lookup with optional context.

    Args:
        query: Query to look up
        context: Optional additional context

    Examples:
        obsidian_ai_lookup("aortocaval compression", context="maternal physiology")
    """
    try:
        context_val = context if context else None
        result = await sdk.ai_lookup(query, context_val)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_ai_index(action: str = "status", force: bool = False) -> str:
    """
    Manage Smart Connections index.

    Actions:
        - status: Get index status
        - reindex: Trigger reindexing (use force=True to force full reindex)

    Examples:
        obsidian_ai_index("status")
        obsidian_ai_index("reindex", force=True)
    """
    try:
        if action == "status":
            result = await sdk.ai_get_index_status()
        elif action == "reindex":
            result = await sdk.ai_reindex(force)
        else:
            return f"Unknown action: {action}. Available: status, reindex"
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_copilot(action: str, content: str = "", project_id: str = "") -> str:
    """
    Copilot AI operations - memory, context, and indexing.

    Actions:
        - memory_get: Get saved memory and recent conversations
        - memory_update: Update memory with new content (requires content arg)
        - context: Get project context (optional project_id)
        - index: Trigger vault indexing
        - index_status: Get vector store status

    Examples:
        obsidian_copilot("memory_get")
        obsidian_copilot("memory_update", content="User prefers detailed explanations")
        obsidian_copilot("context", project_id="maternal-physiology")
        obsidian_copilot("index_status")
    """
    try:
        if action == "memory_get":
            result = await sdk.copilot_get_memory()
        elif action == "memory_update":
            if not content:
                return "Error: memory_update requires 'content' argument"
            result = await sdk.copilot_update_memory(content)
        elif action == "context":
            project_val = project_id if project_id else None
            result = await sdk.copilot_get_context(project_val)
        elif action == "index":
            result = await sdk.copilot_index_vault()
        elif action == "index_status":
            result = await sdk.copilot_get_index_status()
        else:
            return f"""Unknown action: {action}.

Available actions:
  - memory_get: Get saved memory
  - memory_update: Update memory (requires content)
  - context: Get project context
  - index: Trigger indexing
  - index_status: Get index status"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# CONTENT MANAGEMENT TOOLS (Templater + Linter)
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_templater(action: str, template_path: str = "", target_path: str = "", content: str = "") -> str:
    """
    Templater operations - create notes from templates or parse content.

    Actions:
        - create: Create a new note from a template
        - parse: Parse Templater syntax in content

    Args:
        action: "create" or "parse"
        template_path: Path to template file (for create)
        target_path: Where to create the new note (for create)
        content: Content to parse (for parse)

    Examples:
        obsidian_templater("create", template_path="Templates/Concept.md", target_path="Concepts/NewConcept.md")
        obsidian_templater("parse", content="<% tp.date.now() %>")
    """
    try:
        if action == "create":
            if not template_path or not target_path:
                return "Error: create requires both 'template_path' and 'target_path'"
            result = await sdk.templater_create_from_template(template_path, target_path)
        elif action == "parse":
            if not content:
                return "Error: parse requires 'content' argument"
            result = await sdk.templater_parse(content)
        else:
            return f"Unknown action: {action}. Available: create, parse"
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_lint(action: str, path: str = "") -> str:
    """
    Linter operations - lint files for formatting.

    Actions:
        - file: Lint a single file
        - all: Lint all files in vault
        - folder: Lint all files in a folder

    Args:
        action: "file", "all", or "folder"
        path: File or folder path (for file/folder actions)

    Examples:
        obsidian_lint("file", path="Concepts/Cardiac-Output.md")
        obsidian_lint("all")
        obsidian_lint("folder", path="Concepts/")
    """
    try:
        if action == "file":
            if not path:
                return "Error: file action requires 'path' argument"
            result = await sdk.lint_file(path)
        elif action == "all":
            result = await sdk.lint_all()
        elif action == "folder":
            if not path:
                return "Error: folder action requires 'path' argument"
            result = await sdk.lint_folder(path)
        else:
            return f"Unknown action: {action}. Available: file, all, folder"
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# SPACED REPETITION TOOLS
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_sr(action: str, path: str = "", response: str = "") -> str:
    """
    Spaced Repetition operations - flashcards and review management.

    Actions:
        - stats: Get spaced repetition statistics
        - load: Load a note for review
        - sync: Sync spaced repetition data
        - review: Save review response (requires path and response: "easy"|"good"|"hard"|"again")

    Examples:
        obsidian_sr("stats")
        obsidian_sr("load", path="Concepts/Cardiac-Output.md")
        obsidian_sr("review", path="Concepts/Cardiac-Output.md", response="good")
        obsidian_sr("sync")
    """
    try:
        if action == "stats":
            result = await sdk.sr_get_stats()
        elif action == "load":
            if not path:
                return "Error: load action requires 'path' argument"
            result = await sdk.sr_load_note(path)
        elif action == "sync":
            result = await sdk.sr_sync()
        elif action == "review":
            if not path or not response:
                return "Error: review action requires both 'path' and 'response' arguments"
            if response not in ["easy", "good", "hard", "again"]:
                return f"Error: response must be one of: easy, good, hard, again"
            result = await sdk.sr_save_response(path, response)
        else:
            return f"""Unknown action: {action}.

Available actions:
  - stats: Get SR statistics
  - load: Load note for review
  - sync: Sync SR data
  - review: Save review response"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# CANNOLI TOOLS (Canvas LLM Workflows)
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_cannoli(action: str, canvas_path: str = "") -> str:
    """
    Cannoli operations - run canvas-based LLM workflows.

    Actions:
        - list: List all available Cannoli functions
        - run: Run a Cannoli canvas workflow
        - bake: Bake a canvas to a callable function

    Args:
        canvas_path: Path to canvas file (for run/bake)

    Examples:
        obsidian_cannoli("list")
        obsidian_cannoli("run", canvas_path="Workflows/AnalyzeConcept.canvas")
        obsidian_cannoli("bake", canvas_path="Workflows/GenerateSummary.canvas")
    """
    try:
        if action == "list":
            result = await sdk.cannoli_list_functions()
        elif action == "run":
            if not canvas_path:
                return "Error: run action requires 'canvas_path' argument"
            result = await sdk.cannoli_run(canvas_path)
        elif action == "bake":
            if not canvas_path:
                return "Error: bake action requires 'canvas_path' argument"
            result = await sdk.cannoli_bake(canvas_path)
        else:
            return f"""Unknown action: {action}.

Available actions:
  - list: List Cannoli functions
  - run: Run a canvas workflow
  - bake: Bake canvas to function"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# TASK MANAGEMENT TOOLS (TaskNotes)
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_task(action: str, title: str = "", task_id: str = "", project: str = "", due: str = "", priority: str = "") -> str:
    """
    TaskNotes operations - task management with projects and time tracking.

    Actions:
        - create: Create a new task
        - toggle: Toggle task completion status
        - list: List tasks (filtered by project if provided)

    Args:
        action: "create", "toggle", or "list"
        title: Task title (for create)
        task_id: Task ID (for toggle)
        project: Project name (for create/list filter)
        due: Due date in YYYY-MM-DD format (for create)
        priority: low, medium, high (for create)

    Examples:
        obsidian_task("create", title="Review cardiac concepts", project="Exam Prep", priority="high")
        obsidian_task("toggle", task_id="task-123")
        obsidian_task("list", project="Exam Prep")
    """
    try:
        if action == "create":
            if not title:
                return "Error: create action requires 'title' argument"
            project_val = project if project else None
            due_val = due if due else None
            priority_val = priority if priority else None
            result = await sdk.task_create(title, project_val, due_val, priority_val)
        elif action == "toggle":
            if not task_id:
                return "Error: toggle action requires 'task_id' argument"
            result = await sdk.task_toggle(task_id)
        elif action == "list":
            project_val = project if project else None
            result = await sdk.task_list(project_val)
        else:
            return f"""Unknown action: {action}.

Available actions:
  - create: Create new task
  - toggle: Toggle completion
  - list: List tasks"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# LLM ORCHESTRATION TOOLS
# ═══════════════════════════════════════════════════════════════

@mcp.tool()
async def obsidian_llm(
    action: str,
    model: str = "",
    messages: str = "[]",
    task_type: str = "",
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> str:
    """
    LLM operations using localhost:8045 endpoint (58 models available).

    Actions:
        - models: List all available models with tier stratification
        - call: Call a specific model
        - select: Select optimal model for task type

    Args:
        action: "models", "call", or "select"
        model: Model ID for call action
        messages: JSON array of messages for call action
        task_type: Task type for select action (reasoning, analysis, fast, image)
        temperature: Temperature for call (default: 0.7)
        max_tokens: Max tokens for call (default: 4096)

    Examples:
        obsidian_llm("models")
        obsidian_llm("call", model="claude-sonnet-4-5", messages='[{"role":"user","content":"Hello"}]')
        obsidian_llm("select", task_type="reasoning")
    """
    try:
        if action == "models":
            result = await sdk.llm_list_models()
        elif action == "call":
            if not model:
                return "Error: call action requires 'model' argument"
            import json as json_module
            msgs = json_module.loads(messages)
            result = await sdk.llm_call(model, msgs, temperature, max_tokens)
        elif action == "select":
            if not task_type:
                return "Error: select action requires 'task_type' argument"
            result = {"selected_model": await sdk.llm_select_model(task_type)}
        else:
            return f"""Unknown action: {action}.

Available actions:
  - models: List available models
  - call: Call a model
  - select: Select model for task type"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_strategy(
    strategy: str,
    query: str,
    context: str = "{}"
) -> str:
    """
    Execute a single strategy (graph, vector, or semantic).

    Strategies:
        - graph: Breadcrumbs traversal, importance analysis, gap detection
        - vector: Smart Connections semantic search and nearest neighbors
        - semantic: LLM reasoning chains with query classification

    Args:
        strategy: "graph", "vector", or "semantic"
        query: The query to process
        context: Optional JSON context with hints

    Examples:
        obsidian_strategy("graph", "cardiac output regulation")
        obsidian_strategy("vector", "mechanisms of vasodilation", '{"reference_path":"Concepts/..."}')
        obsidian_strategy("semantic", "explain ion trapping in fetus")
    """
    try:
        import json as json_module
        ctx = json_module.loads(context) if context else None

        if strategy == "graph":
            result = await sdk.strategy_graph(query, ctx)
        elif strategy == "vector":
            result = await sdk.strategy_vector(query, ctx)
        elif strategy == "semantic":
            result = await sdk.strategy_semantic(query, ctx)
        else:
            return f"""Unknown strategy: {strategy}.

Available strategies:
  - graph: Breadcrumbs graph traversal
  - vector: Smart Connections vector search
  - semantic: LLM reasoning chains"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_triple(
    query: str,
    context: str = "{}",
    strategies: str = ""
) -> str:
    """
    Execute triple concurrent strategy (graph + vector + semantic).

    Runs all three strategies in parallel and synthesizes results.

    Args:
        query: The query to process
        context: Optional JSON context
        strategies: Optional comma-separated list (default: all three)

    Examples:
        obsidian_triple("cardiac output in pregnancy")
        obsidian_triple("drug transfer mechanisms", strategies="graph,vector")
    """
    try:
        import json as json_module
        ctx = json_module.loads(context) if context and context != "{}" else None
        strat_list = strategies.split(",") if strategies else None

        result = await sdk.triple_concurrent_execute(query, ctx, strat_list)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_agent(
    action: str,
    task: str,
    task_type: str = "",
    context: str = "{}"
) -> str:
    """
    Agentic operations - task routing and execution.

    Actions:
        - route: Analyze task and determine optimal model/strategies
        - execute: Full agentic execution (route → strategies → synthesize)

    Args:
        action: "route" or "execute"
        task: The task description
        task_type: Optional explicit type (reasoning, analysis, fast, image)
        context: Optional JSON context

    Examples:
        obsidian_agent("route", "analyze cardiac output mechanisms")
        obsidian_agent("execute", "find knowledge gaps in maternal physiology")
    """
    try:
        import json as json_module
        ctx = json_module.loads(context) if context and context != "{}" else None
        tt = task_type if task_type else None

        if action == "route":
            result = await sdk.agent_route_task(task, tt)
        elif action == "execute":
            result = await sdk.agent_execute(task, tt, ctx)
        else:
            return f"""Unknown action: {action}.

Available actions:
  - route: Analyze and route task
  - execute: Full agentic execution"""
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_consensus(
    query: str,
    models: str = "",
    voting: str = "majority"
) -> str:
    """
    Get consensus from multiple LLM models.

    Args:
        query: The query to ask all models
        models: Comma-separated model IDs (default: one from each tier)
        voting: Strategy - "majority", "weighted", or "unanimous"

    Examples:
        obsidian_consensus("What is the primary mechanism of respiratory alkalosis in pregnancy?")
        obsidian_consensus("Explain MAC reduction", models="claude-opus-4-5,gemini-3-pro")
    """
    try:
        model_list = models.split(",") if models else None
        result = await sdk.multi_model_consensus(query, model_list, voting)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_chain(
    task: str,
    chain: str
) -> str:
    """
    Execute a chain of model calls with transformations.

    Each step can use a different model and transform the output.

    Args:
        task: Initial task/input
        chain: JSON array of chain steps

    Chain step format:
        {"model": "model-id", "prompt_template": "Given: {input}\\n\\nAnalyze...", "transform": "content"}

    Examples:
        obsidian_chain("cardiac output", '[{"model":"claude-haiku-4","prompt_template":"Define: {input}"},{"model":"claude-sonnet-4-5","prompt_template":"Expand on: {input}"}]')
    """
    try:
        import json as json_module
        chain_steps = json_module.loads(chain)
        result = await sdk.model_chain(task, chain_steps)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_fan_out(
    query: str,
    sub_queries: str,
    model: str = ""
) -> str:
    """
    Fan out a query into multiple sub-queries processed in parallel.

    Args:
        query: Main query for context
        sub_queries: Comma-separated or JSON array of sub-queries
        model: Model to use (default: fast tier)

    Examples:
        obsidian_fan_out("maternal cardiovascular changes", "heart rate,stroke volume,systemic resistance")
        obsidian_fan_out("pregnancy pharmacology", '["protein binding","volume of distribution","clearance"]')
    """
    try:
        import json as json_module
        # Parse sub_queries - try JSON first, then comma-separated
        try:
            sq_list = json_module.loads(sub_queries)
        except:
            sq_list = [q.strip() for q in sub_queries.split(",")]

        model_id = model if model else None
        result = await sdk.parallel_fan_out(query, sq_list, model_id)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def obsidian_orchestrate(
    intent: str,
    context: str = "{}"
) -> str:
    """
    Orchestrate multiple tools based on intent.

    Automatically classifies intent and executes appropriate tool categories.

    Tool categories:
        - core: eval, open_note, trigger_command
        - query: query, fields, frontmatter
        - graph: graph, evaluate, reasoning
        - ai: ai_search, ai_nearest, copilot
        - content: templater, lint, git
        - learning: sr (spaced repetition)
        - automation: cannoli, task, plugin
        - prediction: predict, generate, apply

    Args:
        intent: What the user wants to accomplish
        context: Optional JSON context

    Examples:
        obsidian_orchestrate("find and analyze cardiac concepts")
        obsidian_orchestrate("create flashcards for maternal physiology")
    """
    try:
        import json as json_module
        ctx = json_module.loads(context) if context and context != "{}" else None
        result = await sdk.orchestrate_tools(intent, ctx)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    main()
