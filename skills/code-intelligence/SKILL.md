---
name: code-intelligence
description: Set up and use GitNexus and Prowl code intelligence engines within an Obsidian vault for plugin development, impact analysis, safe refactoring, and architecture exploration. Use when the user mentions code graphs, knowledge graphs for code, GitNexus, Prowl, codebase indexing, blast radius, impact analysis, call chains, symbol context, code intelligence, or wants to understand/refactor/debug Obsidian plugin source code using graph-powered tools. Also trigger when the user is developing an Obsidian plugin and needs dependency-aware refactoring, multi-file rename coordination, or execution flow tracing.
---

# Code Intelligence Skill

Graph-powered code intelligence for Obsidian plugin development using GitNexus and Prowl. These tools index codebases into knowledge graphs and expose them through MCP, giving AI agents pre-computed dependency maps, call chains, blast radius analysis, and semantic search — eliminating blind exploration.

## When to Use Which Tool

| Need | GitNexus | Prowl |
|------|----------|-------|
| Multi-repo unified graph | Yes (registry) | No (single repo) |
| Browser-based exploration | Yes (Web UI) | No |
| Community clustering | Leiden algorithm | Louvain algorithm |
| Semantic embeddings | MiniLM / ONNX | Snowflake Arctic (384-dim) |
| Incremental file watching | Manual re-index | Daemon with 30s idle re-detect |
| Token compression | ~14x (hybrid search) | ~15x (glance digests) |
| Language breadth | 15+ languages + COBOL | 10 languages |
| License | PolyForm Noncommercial | Apache 2.0 |
| Runtime | Node.js (npm) | Go binary |
| Graph storage | LadybugDB (native/WASM) | SQLite |
| Agent skill generation | Auto (`.claude/skills/`) | No |
| Session heat tracking | No | Yes (1-hour decay) |

**Rule of thumb**: Use GitNexus for broad multi-repo Obsidian plugin work and its richer tool suite. Use Prowl when you need incremental watching, Apache licensing, or lower overhead for a single focused repo.

## Quick Start

### GitNexus Setup

```bash
# Install globally
npm install -g gitnexus

# Index an Obsidian plugin codebase
cd /path/to/obsidian-plugin
npx gitnexus analyze

# Auto-configure MCP for Claude Code / Claudian
npx gitnexus setup

# Verify
gitnexus status
gitnexus list
```

### Prowl Setup

```bash
# Install (requires Go 1.25+)
go install github.com/neur0map/prowl/cmd/prowl@latest
export PATH="$HOME/go/bin:$PATH"

# Index and configure (interactive wizard)
cd /path/to/obsidian-plugin
prowl

# Start MCP server for agents
prowl mcp /path/to/obsidian-plugin
```

### MCP Registration for Claudian / Claude Code

GitNexus (serves all indexed repos from one server):
```bash
claude mcp add gitnexus -- npx -y gitnexus@latest mcp
```

Prowl (one server per repo):
```bash
claude mcp add prowl -- prowl mcp /path/to/plugin
```

For VIVA LLM, add the same commands to its MCP server settings.

## GitNexus MCP Tools

Seven tools available to the agent once the MCP server is running:

### `list_repos`
Discover all indexed repositories in the global registry (`~/.gitnexus/registry.json`).

### `query`
Process-grouped hybrid search combining BM25 full-text and semantic ranking via reciprocal rank fusion (RRF). Returns results organized by execution flow.

```
query({ repo: "obsidian-plugin-name", query: "settings tab render" })
```

### `context`
360-degree view of any symbol — callers, callees, containing process, community membership, and categorized references.

```
context({ repo: "my-plugin", symbol: "SettingsTab" })
```

### `impact`
Blast radius analysis showing upstream and downstream effects of changing a symbol. Returns depth-grouped dependents with confidence scores.

```
impact({ repo: "my-plugin", symbol: "saveSettings", depth: 3 })
```

Use this BEFORE making changes to understand the risk surface.

### `detect_changes`
Maps git diffs to affected graph entities. Scopes: `unstaged`, `staged`, `all`, `compare`.

```
detect_changes({ repo: "my-plugin", scope: "unstaged" })
```

### `rename`
Multi-file coordinated rename using graph validation. Always run with `dry_run: true` first.

```
rename({ repo: "my-plugin", old_name: "loadData", new_name: "loadSettings", dry_run: true })
```

### `cypher`
Raw graph queries for advanced analysis. Read-only (write queries blocked).

```
cypher({ repo: "my-plugin", query: "MATCH (f:Function)-[:CALLS]->(g:Function) WHERE f.name = 'onload' RETURN g.name, g.file" })
```

## Prowl MCP Tools

Five tools with community-aware ranking:

### `prowl_overview`
Maps entire project structure with ~15-token glance digests per file. Use as the first call to orient in an unfamiliar codebase.

### `prowl_scope`
Semantic search with 1-hop graph expansion. Results ranked by community cohesion and dependency depth. Session heat (recently accessed files) blends at 15% weight.

### `prowl_file_context`
Deep structural context for a single file: exports, function calls, callers, imports, and upstream dependency chain.

### `prowl_impact`
Blast radius showing direct and transitive dependents plus cross-community effects.

### `prowl_semantic_search`
Pure vector similarity search over embedded function/class signatures (384-dim Snowflake Arctic).

## Obsidian Plugin Development Workflows

### 1. Understand an Unfamiliar Plugin

```
# Index the plugin
cd /path/to/obsidian-plugin && npx gitnexus analyze

# In Claudian or Claude Code:
# → "What does this plugin do? Start with the onload entry point and trace the execution flows."
# Agent uses: list_repos → query("onload") → context(onload symbol) → follow call chains
```

With Prowl: run `prowl` in the plugin dir, then ask the agent — it calls `prowl_overview` for the full map, then `prowl_file_context` on `main.ts`.

### 2. Pre-Change Impact Analysis

Before modifying a function:
```
# Agent calls: impact({ symbol: "registerView", depth: 3 })
# Returns: all functions/files affected, grouped by distance
# Then: detect_changes({ scope: "unstaged" }) after editing
```

This prevents breaking view registration, settings wiring, or command palette entries that depend on the changed code.

### 3. Safe Multi-File Refactoring

Renaming a settings class across the plugin:
```
# Step 1: Dry run
rename({ old_name: "MyPluginSettings", new_name: "PluginConfig", dry_run: true })
# Returns: all files and locations that need updating

# Step 2: Apply
rename({ old_name: "MyPluginSettings", new_name: "PluginConfig", dry_run: false })
```

The graph ensures no reference is missed — including re-exports, type annotations, and constructor calls.

### 4. Debug a Call Chain

Tracing why a command fails:
```
# Agent calls: context({ symbol: "addCommand" })
# Sees: which functions register commands, what they call, upstream dependencies
# Then: query("error handling command") to find related error paths
```

### 5. Architecture Documentation

```bash
# GitNexus generates Mermaid diagrams via MCP prompt:
# detect_impact prompt → pre-commit scope analysis
# generate_map prompt → architecture docs with diagrams
```

### 6. Multi-Plugin Workspace

GitNexus indexes multiple repos into a shared registry:
```bash
cd ~/plugins/obsidian-plugin-a && npx gitnexus analyze
cd ~/plugins/obsidian-plugin-b && npx gitnexus analyze
cd ~/plugins/obsidian-plugin-c && npx gitnexus analyze

# One MCP server serves all three — agent switches with list_repos
```

## Graph Schema Reference

Read `references/graph-schema.md` for the full GitNexus node types (47 labels), relationship types (22 types), and Prowl's community/dependency model.

## Indexing Pipeline Reference

Read `references/indexing-pipeline.md` for details on the 14-phase GitNexus pipeline and 8-phase Prowl pipeline, including language support matrices and performance characteristics.

## Integration with Other Skills

| Companion Skill | Synergy |
|----------------|---------|
| `obsidian-dev` | Use code intelligence for implementation patterns the graph reveals |
| `obsidian-ops` | Run impact analysis before release builds |
| `obsidian-plugin-dev` | Graph-aware scaffolding and lifecycle safety |
| `claudian` | MCP tools connect directly through Claudian's Claude Code session |
| `viva-llm` | MCP tools available through VIVA LLM's MCP integration |
| `advanced-canvas` | Visualize dependency graphs as canvas nodes |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `gitnexus: command not found` | `npm install -g gitnexus` or use `npx gitnexus` |
| `prowl: command not found` | `go install github.com/neur0map/prowl/cmd/prowl@latest` and add `$HOME/go/bin` to PATH |
| Empty query results | Re-index: `npx gitnexus analyze --force` or re-run `prowl` |
| Stale index after edits | GitNexus: manual `analyze --force`. Prowl: daemon auto-updates (30s idle) |
| MCP server not connecting | Check `claude mcp list` — ensure server is registered. Restart Claudian |
| Large repo OOM | GitNexus auto-expands to 8GB heap. For bigger repos, use `--force` flag |
| LadybugDB lock errors | Only one `gitnexus mcp` process per repo. Kill duplicates |

## References

- [GitNexus](https://github.com/abhigyanpatwari/GitNexus) — Zero-server code intelligence engine
- [pi-gitnexus](https://github.com/tintinweb/pi-gitnexus) — Pi agent integration (auto-augments tool results)
- [Prowl](https://github.com/neur0map/prowl) — Context compiler for AI coding agents
- [MCP Specification](https://modelcontextprotocol.io) — Model Context Protocol
