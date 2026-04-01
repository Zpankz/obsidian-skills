<!--
DIRECTORY TREE (orientation)
references/04-node-schema.md
  Covers: frontmatter spec · Obsidian base query syntax · CLI analytics injection
  Depends on: none
  Used by: /path build · /path scan · any note generation
-->

# Node Schema & Base Query Spec

## Contents
- [Frontmatter Schema](#frontmatter-schema)
- [Analytics Injection via Frontmatter](#analytics-injection)
- [Obsidian Base Query Syntax](#base-query-syntax)
- [CLI-Driven Context Loading](#cli-context-loading)

---

## Frontmatter Schema

Every generated `.md` note MUST conform to this schema.
Fields marked `[auto]` are computed by scripts and must not be hand-edited.

```yaml
---
# ── Identity ─────────────────────────────────────────────
id: "node_<uuid8>"              # [auto] stable identifier
title: "Concept Name"
aliases: []                     # optional alternate names

# ── Graph Position ────────────────────────────────────────
level: L2                       # L0 | L1 | L2 | L3
domain: "pharmacology"
cluster: "receptor_theory"      # topical cluster label
path_position: 7                # [auto] integer in current path

# ── PKG State ─────────────────────────────────────────────
mastery: 0.0                    # 0.0-1.0, updated post-session
correctness: null               # 0.0-1.0, how often answers are factually correct
transferability: null            # 0.0-1.0, performance on novel contexts for this concept
reuse_rate: null                 # 0.0-1.0, how often this schema aids other nodes
last_reviewed: null             # ISO date
review_count: 0
next_review: null               # [auto] spaced repetition date
status: gap                     # gap | in-progress | mastered | scaffold

# ── ZPD Calibration ───────────────────────────────────────
difficulty: 0.65                # 0.0–1.0 (domain expert estimate)
prerequisites: []               # list of [[wikilinks]]
unlocks: []                     # list of [[wikilinks]]
zpd_delta: null                 # [auto] difficulty − mastery(prerequisites)

# ── Zeigarnik Loop ────────────────────────────────────────
open_question: ""               # must be unanswerable without successor node
resolves_question_from: ""      # [[predecessor node]]
tension_level: medium           # low | medium | high

# ── MCMC Analytics ────────────────────────────────────────
priority: 0.0                   # [auto] centrality × impact × (1−mastery)
centrality: 0.0                 # [auto] eigenvector centrality in GKG
impact_unlocks: 0               # [auto] count of transitively unlocked nodes
criticality: false              # [auto] true if at energy landscape inflection
sigma_c: 0.0                    # [auto] criticality deviation metric

# ── Self-Distillation (F1/F3/F4/F5) ─────────────────
self_demo_sources: []           # [auto] [[mastered node]] IDs for scaffolding
best_attempt_summary: ""        # learner's own best explanation (post-mastery)
scaffold_strategy: "abstract"   # abstract | self_demo | hybrid
last_error_types: []            # [auto] most recent session error categories
last_misconceptions: []         # [auto] misconceptions from last session
retention_alert: false          # [auto] true if retention probe failed
difficulty_original: null       # [auto] preserved when GKG refines difficulty
active_priority_mechanism: ""   # [auto] which priority formula is active
active_scaffold_mechanism: ""   # [auto] which scaffold strategy is active

# ── Workflow ──────────────────────────────────────────────
estimated_minutes: 20
verified: false                 # set true after validate_vault.py passes
tags:
  - learning-path
  - L2
  - pharmacology
  - gap
---
```

**Validation constraints** (checked by `validate_vault.py`):
- `mastery` ∈ [0.0, 1.0]
- `difficulty` ∈ [0.0, 1.0]
- `zpd_delta` ∈ [0.10, 0.40] OR node is scaffold
- `open_question` non-empty for all non-terminal nodes
- `status` matches mastery threshold
- All `prerequisites` and `unlocks` resolve to existing vault nodes
- `scaffold_strategy` ∈ {abstract, self_demo, hybrid}
- `self_demo_sources` resolve to existing mastered nodes when non-empty
- `last_error_types` entries match feedback taxonomy (see [08])
- `retention_alert` = false unless explicitly set by retention probe failure
- `active_priority_mechanism` matches key in MECHANISM_REGISTRY['priority']
- `active_scaffold_mechanism` matches key in MECHANISM_REGISTRY['scaffold']

---

## Analytics Injection

After each `/olp` command, scripts update frontmatter for affected nodes.
This keeps analytics in context for subsequent Obsidian Base queries.

```python
def inject_analytics(node_path: Path, analytics: dict):
    """Update frontmatter with computed analytics without touching content."""
    content = node_path.read_text()
    fm, body = split_frontmatter(content)
    fm.update({
        'priority':       analytics['priority'],
        'centrality':     analytics['centrality'],
        'impact_unlocks': analytics['impact_unlocks'],
        'zpd_delta':      analytics['zpd_delta'],
        'criticality':    analytics['criticality'],
        'sigma_c':        analytics['sigma_c'],
        'next_review':    analytics['next_review'],
    })
    node_path.write_text(join_frontmatter(fm, body))
```

---

## Obsidian Base Query Syntax

The `.base` file uses Obsidian's native query language. These are designed
to be executable via CLI and automatically feed analytics into reasoning traversal.

### Priority Queue View
```json
{
  "filter": {
    "and": [
      { "property": "tags", "operator": "contains", "value": "learning-path" },
      { "property": "status", "operator": "in", "value": ["gap", "in-progress"] }
    ]
  },
  "sort": [
    { "property": "priority", "direction": "desc" },
    { "property": "path_position", "direction": "asc" }
  ],
  "columns": ["title", "level", "mastery", "difficulty", "zpd_delta", "priority", "criticality", "estimated_minutes"]
}
```

### Today's Session View (ZPD-calibrated)
```json
{
  "filter": {
    "or": [
      { "property": "next_review", "operator": "lte", "value": "today" },
      {
        "and": [
          { "property": "status", "operator": "eq", "value": "gap" },
          { "property": "path_position", "operator": "lte", "value": 3 }
        ]
      }
    ]
  },
  "sort": [{ "property": "priority", "direction": "desc" }],
  "columns": ["title", "open_question", "tension_level", "zpd_delta", "estimated_minutes", "criticality"]
}
```

### Zeigarnik Board (tension grouping)
```json
{
  "filter": {
    "and": [
      { "property": "tags", "operator": "contains", "value": "learning-path" },
      { "property": "open_question", "operator": "ne", "value": "" }
    ]
  },
  "groupBy": "tension_level",
  "columns": ["title", "open_question", "resolves_question_from", "mastery", "criticality"]
}
```

### Critical Nodes Alert
```json
{
  "filter": {
    "and": [
      { "property": "criticality", "operator": "eq", "value": true },
      { "property": "status", "operator": "ne", "value": "mastered" }
    ]
  },
  "sort": [{ "property": "sigma_c", "direction": "asc" }],
  "columns": ["title", "sigma_c", "tension_level", "zpd_delta", "priority"]
}
```

### Retention Alerts (F4)
```json
{
  "filter": {
    "and": [
      { "property": "retention_alert", "operator": "eq", "value": true },
      { "property": "status", "operator": "ne", "value": "gap" }
    ]
  },
  "sort": [{ "property": "centrality", "direction": "desc" }],
  "columns": ["title", "mastery", "last_reviewed", "centrality", "retention_alert"]
}
```

### Self-Demo Eligible (F3)
```json
{
  "filter": {
    "and": [
      { "property": "scaffold_strategy", "operator": "eq", "value": "self_demo" },
      { "property": "best_attempt_summary", "operator": "ne", "value": "" }
    ]
  },
  "sort": [{ "property": "centrality", "direction": "desc" }],
  "columns": ["title", "mastery", "best_attempt_summary", "centrality"]
}
```

### Error Pattern Analysis (F5)
```json
{
  "filter": {
    "property": "last_error_types", "operator": "ne", "value": []
  },
  "groupBy": "last_error_types",
  "columns": ["title", "last_error_types", "last_misconceptions", "mastery", "status"]
}
```

---

## CLI-Driven Context Loading

Each CLI command computes specific analytics and injects them as a YAML context
block prepended to the reasoning session. This prevents loading irrelevant data.

```bash
# Command → analytics computed → context injected
/path scan   → mastery_distribution.yaml
/path gap    → gap_priority_queue.yaml + centrality_scores.yaml
/path traverse → path.json + criticality.yaml + acceptance_rate.yaml
/path status → status_report.yaml (coverage + next nodes + feasibility)
/path compound → session_delta.yaml (mastery changes + resequence diff)
/path verify → validation_report.yaml (all checks pass/fail incl. V11-V14)
/path refine → gkg_refinement_report.yaml (difficulty recal + edge discovery)
/path meta   → meta_report.yaml (parameter adjustments + prediction errors)
/path self-eval -> eval_report.yaml (141 architectural checks + fix prescriptions)
/path consolidate -> consolidated_history.yaml (Pareto compressed epochs)
```

**Context injection pattern** (prepended to LLM context):
```
<analytics_context>
[YAML content from computed analytics file]
</analytics_context>

Use the above analytics to inform your reasoning.
Do NOT reload from disk — the analytics above are current.
```

This means the **LLM never reads the full vault** — it reads only the
pre-computed analytics injected by the CLI. Context is bounded, targeted, and
fresh without requiring expensive full-graph scans in-context.
