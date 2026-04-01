<!--
DIRECTORY TREE (orientation)
references/09-obsidian-integration.md
  Covers: obsidian-cli hooks · ob sync · vault-manager · dataview PKG · breadcrumbs · dream coordination
  Depends on: 02-pkg-gkg-differential (PKG scanning), 04-node-schema (frontmatter), 06-canvas-base-spec (canvas/base)
  Used by: /olp build, /olp scan, /olp compound, /olp sync, /olp consolidate
-->

# Obsidian Ecosystem Integration

## Contents
- [Vault Bridge Architecture](#vault-bridge-architecture)
- [PKG Scanning Methods](#pkg-scanning-methods)
- [Property Update Methods](#property-update-methods)
- [Canvas and Base Integration](#canvas-and-base-integration)
- [Sync Workflows](#sync-workflows)
- [Memory Coordination](#memory-coordination)
- [Breadcrumbs Typed Links](#breadcrumbs-typed-links)
- [Plugin Detection](#plugin-detection)

---

## Vault Bridge Architecture

The vault bridge provides a unified interface over three vault access methods. It probes availability top-down and uses the richest available method.

```
┌─────────────────────────────────────────────┐
│              vault_bridge.py                 │
│                                             │
│  probe()                                    │
│    ├── obsidian-cli available?              │
│    │   └── obsidian eval code="1" 2>/dev/null│
│    │       ├── YES → LiveVault adapter      │
│    │       └── NO  ↓                        │
│    ├── ob configured?                       │
│    │   └── ob sync-status 2>/dev/null       │
│    │       ├── YES → HeadlessVault adapter  │
│    │       └── NO  ↓                        │
│    └── Direct file I/O (always available)   │
│        └── FileVault adapter                │
└─────────────────────────────────────────────┘
```

### Adapter capabilities

| Method | Read | Write | Search | Properties | Backlinks | Sync | Dataview |
|---|---|---|---|---|---|---|---|
| LiveVault (obsidian-cli) | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| HeadlessVault (ob) | ✓ | ✓ | — | — | — | ✓ | — |
| FileVault (direct I/O) | ✓ | ✓ | grep | Edit | — | — | — |

### Vault resolution

Before any operation, the bridge resolves the target vault:

```python
def resolve_vault(vault_hint: str | None) -> Path:
    """Resolve vault path using obsidian-vault-manager registry.

    Priority:
    1. Explicit vault_hint (name or path)
    2. obsidian-vault-manager active vault
    3. Current working directory (if .obsidian/ exists)
    """
    if vault_hint:
        # Try as path first
        p = Path(vault_hint).expanduser()
        if (p / '.obsidian').exists():
            return p
        # Try as name via vault-manager
        result = run(['python3', VAULT_MANAGER_SCRIPTS / 'vault_registry.py',
                      'get', '--name', vault_hint])
        if result.returncode == 0:
            return Path(json.loads(result.stdout)['path'])

    # Try active vault from registry
    result = run(['python3', VAULT_MANAGER_SCRIPTS / 'vault_registry.py', 'active'])
    if result.returncode == 0:
        return Path(json.loads(result.stdout)['path'])

    # Fallback: walk up from cwd looking for .obsidian/
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / '.obsidian').exists():
            return parent

    raise VaultNotFoundError("No vault found. Specify --vault or set active vault.")
```

---

## PKG Scanning Methods

### Method 1: Dataview DQL (richest, requires Obsidian running + Dataview)

```bash
obsidian eval code="
  const dv = app.plugins.plugins.dataview?.api;
  if (!dv) throw 'Dataview not available';
  const pages = dv.pages('#learning-path');
  JSON.stringify(pages.map(p => ({
    id: p.file.name,
    path: p.file.path,
    mastery: p.mastery ?? 0,
    difficulty: p.difficulty ?? 0.5,
    status: p.status ?? 'gap',
    level: p.level ?? 'L2',
    last_reviewed: p.last_reviewed?.toString() ?? null,
    next_review: p.next_review?.toString() ?? null,
    review_count: p.review_count ?? 0,
    open_question: p.open_question ?? '',
    tension_level: p.tension_level ?? 'medium',
    criticality: p.criticality ?? false,
    self_demo_sources: p.self_demo_sources ?? [],
    concept_scores: {
      core_mechanism: p.score_core ?? null,
      clinical_application: p.score_clinical ?? null,
      quantitative: p.score_quantitative ?? null,
      integration: p.score_integration ?? null
    }
  })));
"
```

**Advantages**: reads computed Dataview fields, respects aliases, handles inline fields.

### Method 2: obsidian-cli read (requires Obsidian running)

```bash
# Search for all learning-path tagged notes
obsidian search query="tag:#learning-path" limit=500

# Read individual notes for frontmatter
obsidian read file="Fick Principle"
```

Parse frontmatter from the read output. Less efficient than Dataview but works without plugins.

### Method 3: Direct file parsing (always works)

```bash
python scripts/pkg_gkg_diff.py --vault ./my_vault --output gap.json
```

The script walks the vault directory, parses YAML frontmatter from each .md file with the `learning-path` tag, and builds the PKG.

### Scanning decision tree

```python
def scan_pkg(vault_path: Path) -> dict:
    adapter = probe_adapter(vault_path)

    if isinstance(adapter, LiveVault) and adapter.has_plugin('dataview'):
        return adapter.dataview_scan()    # Method 1
    elif isinstance(adapter, LiveVault):
        return adapter.cli_scan()          # Method 2
    else:
        return file_scan(vault_path)       # Method 3
```

---

## Property Update Methods

### Live update (obsidian-cli)

```bash
obsidian property:set file="<note>" name="mastery" value="0.85" silent
obsidian property:set file="<note>" name="status" value="mastered" silent
obsidian property:set file="<note>" name="last_reviewed" value="2026-04-01" silent
obsidian property:set file="<note>" name="review_count" value="4" silent
obsidian property:set file="<note>" name="next_review" value="2026-04-08" silent
```

**Key**: use `silent` to avoid stealing focus. Batch updates with multiple sequential calls.

### File update (Edit tool)

Follow `obsidian-yaml-frontmatter` conventions:
- Lowercase property names
- ISO 8601 dates (`YYYY-MM-DD`)
- Arrays with `- item` syntax
- Preserve existing key order

```yaml
---
mastery: 0.85
status: mastered
last_reviewed: 2026-04-01
review_count: 4
next_review: 2026-04-08
---
```

---

## Canvas and Base Integration

### Canvas generation

The vault-emitter uses `json-canvas` spec for `.canvas` files:
- Color system per ref [06]: status colors, level groups, ZPD edge colors
- Analytics overlay node in top-right
- Session header with next 3 nodes

When writing canvases, follow `obsidian-canvas` skill conventions for node sizing, edge routing, and group nesting.

### Base generation

The `.base` file uses the Obsidian Bases plugin filter syntax from ref [06].
Six views: Gap Priority Queue, Today's Session, Zeigarnik Board, Critical Nodes, Mastered (SR), Full Path.

### Validation

After canvas/base generation:

```bash
# Verify canvas JSON is valid
obsidian eval code="
  const canvas = app.vault.getAbstractFileByPath('path.canvas');
  if (!canvas) throw 'Canvas not found';
  const data = JSON.parse(await app.vault.read(canvas));
  JSON.stringify({nodes: data.nodes.length, edges: data.edges.length});
"
```

---

## Sync Workflows

### Post-build sync

After `/olp build` generates vault files:

```bash
# Check if ob is configured for this vault
ob sync-status --path <vault_path> 2>/dev/null

# If configured, sync
ob sync --path <vault_path>
```

### Continuous sync during study

For long study sessions where mastery updates happen frequently:

```bash
# Start continuous sync in background
ob sync --continuous --path <vault_path> &
OB_PID=$!

# ... study session with compound updates ...

# Stop sync
kill $OB_PID
```

### Multi-device workflow

```
Desktop (Obsidian running)
  → /olp build generates vault
  → ob sync pushes to remote

Mobile / Tablet
  → Obsidian Sync pulls automatically
  → Student reviews on any device
  → Changes sync back

Next session
  → /olp scan reads updated mastery
  → /olp compound processes session
```

---

## Memory Coordination

### Division of responsibility

```
/olp consolidate (learning-level)
  ├── Mastery trajectory summaries
  ├── Error pattern aggregates
  ├── Mechanism effectiveness ratings
  ├── Plateau history
  └── Output: consolidated_history.yaml

/obsidian-dream (meta-level)
  ├── User corrections ("don't use scaffold X")
  ├── Workflow preferences
  ├── Vault convention changes
  ├── Tool/plugin decisions
  └── Output: memory topic files (preferences.md, corrections.md, etc.)
```

### How they coordinate

1. `/olp consolidate` writes `consolidated_history.yaml` into session_history/
2. `/obsidian-dream` Phase 2 (GATHER SIGNAL) skips learning-level data from session transcripts when `consolidated_history.yaml` exists — it treats that as already processed
3. Dream extracts only meta-level signals: corrections, preferences, decisions
4. Both write to `~/.claude/projects/<project>/memory/` but different topic files

### Session history location

```
~/.claude/projects/<project>/memory/
├── MEMORY.md                    ← dream index
├── preferences.md               ← dream topic
├── vault-conventions.md          ← dream topic
├── knowledge-graph.md            ← dream topic (PKG/GKG snapshots)
└── session_history/
    ├── session_delta_2026-03-28.yaml  ← /olp compound output
    ├── session_delta_2026-03-30.yaml
    ├── consolidated_history.yaml       ← /olp consolidate output
    └── .last-consolidation             ← timestamp
```

---

## Breadcrumbs Typed Links

When Breadcrumbs is installed, the vault-emitter adds typed links to node frontmatter:

```yaml
# Prerequisites → up links
up:
  - "[[Receptor Theory]]"
  - "[[Drug-Receptor Binding]]"

# Next in path → next link
next: "[[Hill Equation]]"

# Unlocks → down links
down:
  - "[[Spare Receptors]]"
  - "[[Receptor Desensitization]]"
```

This enables:
- **Tree View**: hierarchical L0→L3 visualization
- **Matrix View**: prerequisites × unlocks grid
- **Trail View**: breadcrumb trail from L0 to current node
- **Previous-Next View**: path sequence navigation

### Detection and conditional generation

```python
def should_add_breadcrumbs(adapter) -> bool:
    if isinstance(adapter, LiveVault):
        return adapter.has_plugin('breadcrumbs')
    # Fallback: check .obsidian/plugins/breadcrumbs/
    return (adapter.vault_path / '.obsidian/plugins/breadcrumbs').exists()
```

---

## Plugin Detection

Before using plugin-dependent features, probe for availability:

```python
PLUGIN_PROBES = {
    'dataview': "!!app.plugins.plugins.dataview",
    'breadcrumbs': "!!app.plugins.plugins['breadcrumbs']",
    'bases': "!!app.plugins.plugins['bases']",
    'templater': "!!app.plugins.plugins['templater-obsidian']",
    'smart-connections': "!!app.plugins.plugins['smart-connections']",
}

def detect_plugins(adapter) -> dict[str, bool]:
    if isinstance(adapter, LiveVault):
        results = {}
        for name, code in PLUGIN_PROBES.items():
            try:
                out = adapter.eval(code)
                results[name] = out.strip() == 'true'
            except:
                results[name] = False
        return results

    # Fallback: check plugin directories
    plugins_dir = adapter.vault_path / '.obsidian/plugins'
    return {name: (plugins_dir / name.replace("'", "")).exists()
            for name in PLUGIN_PROBES}
```

Features gracefully degrade when plugins are absent:
- No Dataview → fall back to file scanning
- No Breadcrumbs → skip typed links
- No Bases → skip .base file generation
- No Templater → use built-in node template
