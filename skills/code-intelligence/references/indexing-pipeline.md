# Indexing Pipeline Reference

## GitNexus: 14-Phase Pipeline

### Phase Summary

| Phase | Name | Description |
|-------|------|-------------|
| 1 | File scanning | Walk directory tree, respect `.gitignore` |
| 2 | Tree-sitter parsing | Extract ASTs for all supported languages |
| 3 | Symbol extraction | Functions, classes, methods, interfaces, enums, type aliases |
| 4 | Import resolution | Map import statements to target files and symbols |
| 5 | Call resolution | Match function calls to definitions (lexical → symbol table → heuristic) |
| 6 | Export resolution | Track named, default, and re-exports |
| 7 | Heritage resolution | Class inheritance and interface implementation chains |
| 8 | Field extraction | Class fields, interface properties, enum members |
| 9 | Return type collection | Function/method return types |
| 10-14 | Type resolution | Fixpoint iteration with Tarjan's SCC for cyclic dependencies |
| Post | Community detection | Leiden algorithm clusters related symbols |
| Post | Process detection | Trace execution flows from scored entry points |
| Post | Search indexing | BM25 full-text + semantic embedding (MiniLM ONNX) |

### Call Resolution Strategy

Three-tier approach with fallback:

1. **Lexical match** — Direct name match in scope
2. **Symbol table** — Cross-file resolution via import/export chains
3. **Heuristic** — Fuzzy match with confidence scoring for dynamic calls

Confidence scores propagate to `impact` tool results.

### Language Support

| Language | Parsing | Imports | Calls | Types | Heritage | Frameworks |
|----------|---------|---------|-------|-------|----------|------------|
| TypeScript | Full | Full | Full | Full | Full | React, Express, NestJS, Obsidian |
| JavaScript | Full | Full | Full | — | Full | Same as TS minus types |
| Python | Full | Full | Full | Partial | Full | Django, Flask, FastAPI |
| Java | Full | Full | Full | Full | Full | Spring Boot |
| Go | Full | Full | Full | Partial | Partial | — |
| Rust | Full | Full | Full | Partial | Partial | — |
| C# | Full | Full | Full | Full | Full | .NET |
| C++ | Full | Partial | Partial | Partial | Partial | — |
| Kotlin | Full | Full | Full | Full | Full | — |
| Swift | Full | Full | Full | Partial | Full | — |
| Ruby | Full | Partial | Partial | — | Partial | Rails |
| PHP | Full | Full | Partial | Partial | Full | Laravel |
| Dart | Full | Full | Full | Full | Full | Flutter |
| COBOL | Regex | JCL/COPY | Partial | — | — | — |
| Markdown | Headings | Cross-links | — | — | — | — |

### Performance Characteristics

| Metric | Value |
|--------|-------|
| Heap limit | 8GB (auto-expands via process re-spawn) |
| Worker parallelism | Available CPU cores |
| Max concurrent DB connections | 8 per repo |
| Connection idle timeout | 5 minutes |
| MCP startup | Skips heap check for minimal latency |
| Re-index trigger | Manual (`analyze --force`) |

### Obsidian Plugin Indexing Notes

Obsidian plugins are TypeScript projects. GitNexus provides **full resolution** for TypeScript, including:
- `Plugin` class inheritance from `obsidian`
- `addCommand`, `registerView`, `addSettingTab` call chains
- Workspace API usage patterns
- Event handler registration
- Ribbon icon → callback chains
- Settings class → `loadData`/`saveData` flows
- Modal and view component hierarchies

When indexing an Obsidian plugin, the graph captures the full lifecycle from `onload()` through all registered commands, views, and event handlers.

---

## Prowl: 8-Phase Pipeline

### Phase Summary

| Phase | Name | Description |
|-------|------|-------------|
| 1 | File scanning | Walk tree, respect `.gitignore` and custom ignores |
| 2 | Symbol extraction | Tree-sitter AST → functions, classes, types, exports |
| 3 | Import resolution | Map imports to target files |
| 4 | Call graph | Match function calls to definitions across files |
| 5 | Class inheritance | Trace extends/implements chains |
| 6 | Community detection | Louvain algorithm groups related symbols into subsystems |
| 7 | Process detection | Identify multi-step call chains from entry points |
| 8 | Vector embedding | Snowflake Arctic Embed S (384-dim) on symbol signatures |

### Language Support

| Language | Symbol Extraction | Import Resolution | Call Graph |
|----------|------------------|-------------------|------------|
| Go | Full | Full | Full |
| TypeScript | Full | Full | Full |
| JavaScript | Full | Full | Full |
| Rust | Full | Full | Full |
| Python | Full | Full | Full |
| Java | Full | Full | Full |
| C# | Full | Full | Full |
| Swift | Full | Full | Full |
| C++ | Full | Partial | Partial |
| C | Full | Partial | Partial |

### Performance Characteristics

| Metric | Value |
|--------|-------|
| Embedding model | Snowflake Arctic Embed S (~90MB) |
| Embedding dimensions | 384 |
| File watcher idle re-detect | 30 seconds |
| Session heat decay | 1-hour exponential |
| Heat weight in ranking | 15% |
| Token compression | ~14-32x vs raw file reads |
| Accuracy (SWE-bench) | 92.7% file-level (LocAgent, ACL 2025) |
| Cost reduction | ~86% token savings |

### Incremental Updates

Prowl's daemon mode watches for file changes:
1. Detects modified/added/deleted files
2. Re-extracts symbols for changed files
3. Cascades updates to callers and upstream dependencies
4. Re-runs community detection after 30 seconds of idle
5. Updates embeddings for changed signatures

This makes Prowl better suited for active development where the codebase changes frequently between queries.

### Comparison: When to Re-Index

| Scenario | GitNexus | Prowl |
|----------|----------|-------|
| Added a new file | `analyze --force` | Automatic (daemon) |
| Renamed a function | `analyze --force` | Automatic (daemon) |
| Major refactor | `analyze --force` | Automatic, but verify with `prowl` TUI |
| Switched branch | `analyze --force` | Automatic (daemon) |
| First-time index | `analyze` (3-60s depending on size) | `prowl` wizard (10-90s + model download) |
