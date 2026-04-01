# Graph Schema Reference

## GitNexus Knowledge Graph

### Node Types (47 labels)

| Category | Labels | Description |
|----------|--------|-------------|
| Structure | `Project`, `File`, `Folder` | Repository structure |
| Code | `Function`, `Class`, `Method`, `Interface`, `Enum`, `TypeAlias` | Code entities |
| Organization | `Community`, `Process`, `Route` | Functional clusters and execution flows |
| Framework | `Controller`, `ServiceProvider`, `Middleware`, `Tool`, `Delegate` | Framework-specific patterns |
| Metadata | `Import`, `Export`, `Parameter`, `ReturnType`, `Field` | Symbol metadata |

### Relationship Types (22 types)

| Relationship | Description | Properties |
|-------------|-------------|------------|
| `CALLS` | Function/method invocation | confidence, file |
| `INHERITS` | Class inheritance | — |
| `IMPLEMENTS` | Interface implementation | — |
| `IMPORTS` | Module import | named, default, star |
| `EXPORTS` | Module export | named, default, re-export |
| `EXTENDS` | Class extension | — |
| `MEMBER_OF` | Class/module membership | — |
| `DEFINES` | File defines symbol | line, column |
| `STEP_IN_PROCESS` | Node in execution flow | order, depth |
| `BELONGS_TO_COMMUNITY` | Community membership | — |
| `DEPENDS_ON` | File-level dependency | — |
| `USES_TYPE` | Type reference | — |
| `RETURNS` | Return type | — |
| `HAS_PARAMETER` | Function parameter | position, type |
| `HAS_FIELD` | Class/interface field | type, access |
| `OVERRIDES` | Method override | — |
| `DECORATES` | Decorator application | — |
| `CONTAINS` | Folder/file containment | — |
| `REFERENCES` | Generic symbol reference | — |
| `ROUTES_TO` | HTTP route handler | method, path |
| `PROVIDES` | Dependency injection | — |
| `DELEGATES_TO` | Delegation pattern | — |

### Cypher Query Examples

Find all functions called by `onload`:
```cypher
MATCH (f:Function {name: 'onload'})-[:CALLS]->(g:Function)
RETURN g.name, g.file, g.line
ORDER BY g.file
```

Find the community containing a symbol:
```cypher
MATCH (f:Function {name: 'registerView'})-[:BELONGS_TO_COMMUNITY]->(c:Community)
RETURN c.name, c.description
```

Trace a 3-hop call chain:
```cypher
MATCH path = (start:Function {name: 'onload'})-[:CALLS*1..3]->(end:Function)
RETURN [n in nodes(path) | n.name] AS chain, length(path) AS depth
ORDER BY depth
```

Find orphan functions (no callers):
```cypher
MATCH (f:Function)
WHERE NOT ()-[:CALLS]->(f) AND f.name <> 'onload'
RETURN f.name, f.file
ORDER BY f.file
```

Find cross-community calls (potential coupling):
```cypher
MATCH (a:Function)-[:BELONGS_TO_COMMUNITY]->(ca:Community),
      (b:Function)-[:BELONGS_TO_COMMUNITY]->(cb:Community),
      (a)-[:CALLS]->(b)
WHERE ca <> cb
RETURN ca.name AS from_community, cb.name AS to_community,
       a.name AS caller, b.name AS callee
```

### Storage Layout

```
.gitnexus/
├── lbug/           # LadybugDB graph database
│   ├── nodes/      # Node tables
│   └── rels/       # Relationship tables
├── meta.json       # Index metadata and timestamps
├── search/         # BM25 + semantic indices
└── embeddings/     # ONNX model cache
```

Global registry: `~/.gitnexus/registry.json`
```json
{
  "repos": {
    "my-plugin": {
      "path": "/absolute/path/to/plugin",
      "indexedAt": "2026-03-15T10:00:00Z"
    }
  }
}
```

---

## Prowl Knowledge Graph

### Entity Model

| Entity | Description | Key Fields |
|--------|-------------|------------|
| File | Source file | path, language, glance_digest, dependency_depth |
| Symbol | Function/class/type/export | name, kind, file, line, signature |
| Import | Resolved import | source_file, target_file, symbols |
| Call | Function call edge | caller_symbol, callee_symbol, file |
| Inheritance | Class hierarchy | child, parent, kind (extends/implements) |
| Community | Louvain cluster | id, name, member_count, description |
| Process | Multi-step call chain | entry_point, steps, depth |

### Ranking Model

Prowl ranks search results using three signals:

1. **Community cohesion** — files in the same community as seed files rank higher
2. **Dependency depth** — topological sort rank; depth-0 files have no internal deps
3. **Session heat** — in-memory freshness score with 1-hour exponential decay; recently accessed files get 15% ranking boost

### Storage Layout

```
.prowl/
├── prowl.db        # SQLite database (symbols, calls, imports, communities)
├── embeddings.db   # Vector store (Snowflake Arctic 384-dim)
├── context/        # Plain-text context files (readable without MCP)
│   ├── overview.txt
│   └── <file>.ctx
└── config.json     # Project configuration and ignore patterns
```

### Glance Digests

Each file gets a ~15-token structural summary:
```
exports: SettingsTab, DEFAULT_SETTINGS | calls: Plugin.addSettingTab, Setting | callers: main.onload
```

Compare: reading the full file might cost 500-2000 tokens. The digest provides enough for routing decisions at 15 tokens.
