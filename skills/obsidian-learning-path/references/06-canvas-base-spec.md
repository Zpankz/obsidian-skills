<!--
DIRECTORY TREE (orientation)
references/06-canvas-base-spec.md
  Covers: .canvas JSON schema · color coding · .base filter syntax · CLI generation
  Depends on: 04-node-schema (frontmatter fields used in base filters)
  Used by: /path build (emit phase)
-->

# Canvas & Base File Specification

## Contents
- [Canvas Color System](#canvas-color-system)
- [Canvas JSON Schema](#canvas-json-schema)
- [Base File Schema](#base-file-schema)
- [Layout Algorithm](#layout-algorithm)

---

## Canvas Color System

```
Node color by STATUS:
  gap         → "1" (red)      ← highest urgency
  in-progress → "3" (yellow)
  mastered    → "4" (blue)
  scaffold    → "5" (pink)

Node color by LEVEL (group borders):
  L0 → "6" (purple)   governing principles
  L1 → "1" (red)      atomic — high priority
  L2 → "4" (blue)     composite topics
  L3 → "5" (pink)     detail

Edge color by ZPD delta:
  Δ ≤ 0.22   → "4" (blue)    optimal zone
  Δ ∈ [0.22, 0.40] → "3" (yellow)  acceptable, watch
  Δ > 0.40   → "1" (red)     scaffold required

Edge color CRITICALITY override:
  is_critical = true → "6" (purple)  phase transition — handle with care
```

---

## Canvas JSON Schema

```json
{
  "nodes": [
    {
      "id": "group_L0",
      "type": "group",
      "label": "L0: Governing Principles (0.8% nodes → 51% coverage)",
      "x": -40,
      "y": -60,
      "width": 1400,
      "height": 280,
      "color": "6"
    },
    {
      "id": "node_<uuid>",
      "type": "file",
      "file": "concepts/<safe_title>.md",
      "x": 100,
      "y": 400,
      "width": 280,
      "height": 160,
      "color": "1"
    },
    {
      "id": "text_session_header",
      "type": "text",
      "text": "# Today's Session\nNext: [[time_constant]] → [[hill_equation]] → [[spare_receptors]]",
      "x": 1600,
      "y": 0,
      "width": 400,
      "height": 200,
      "color": "3"
    }
  ],
  "edges": [
    {
      "id": "edge_<from>_<to>",
      "fromNode": "node_<from_uuid>",
      "toNode": "node_<to_uuid>",
      "fromSide": "right",
      "toSide": "left",
      "label": "ZPD Δ=0.22 | ⚡ high tension",
      "color": "4"
    }
  ]
}
```

**Embedded analytics node** (always top-right of canvas):
```json
{
  "id": "analytics_panel",
  "type": "text",
  "text": "## Analytics\nCoverage: 35%\nGap nodes: 78\nEst. hours: 26h\nCritical: fick_principle, time_constant\nNext review: hill_equation (today)",
  "x": 1600,
  "y": 250,
  "width": 400,
  "height": 350,
  "color": "6"
}
```

---

## Base File Schema

Complete `.base` file for the progress tracker:

```json
{
  "filters": {
    "and": [
      {"file.hasTag": "learning-path"}
    ]
  },
  "views": [
    {
      "type": "table",
      "name": "🔴 Gap Priority Queue",
      "description": "Highest-leverage gaps, MCMC-ranked",
      "sort": [{"property": "priority", "direction": "desc"}],
      "filter": {
        "property": "status",
        "operator": "in",
        "value": ["gap", "in-progress"]
      },
      "columns": ["title", "level", "mastery", "difficulty", "zpd_delta", "priority", "criticality", "estimated_minutes", "open_question"]
    },
    {
      "type": "table",
      "name": "⚡ Today's Session",
      "description": "Due for review + next 3 path nodes",
      "sort": [{"property": "priority", "direction": "desc"}],
      "filter": {
        "or": [
          {"property": "next_review", "operator": "lte", "value": "today"},
          {
            "and": [
              {"property": "status", "operator": "eq", "value": "gap"},
              {"property": "path_position", "operator": "lte", "value": 3}
            ]
          }
        ]
      },
      "columns": ["title", "open_question", "tension_level", "zpd_delta", "estimated_minutes", "criticality", "sigma_c"]
    },
    {
      "type": "cards",
      "name": "🌀 Zeigarnik Board",
      "description": "Open questions by tension level",
      "groupBy": "tension_level",
      "filter": {
        "property": "open_question",
        "operator": "ne",
        "value": ""
      },
      "cardFields": ["title", "open_question", "resolves_question_from", "mastery", "path_position"]
    },
    {
      "type": "table",
      "name": "⚠️ Critical Nodes",
      "description": "Phase transition points — handle with care",
      "sort": [{"property": "sigma_c", "direction": "asc"}],
      "filter": {
        "and": [
          {"property": "criticality", "operator": "eq", "value": true},
          {"property": "status", "operator": "ne", "value": "mastered"}
        ]
      },
      "columns": ["title", "sigma_c", "tension_level", "zpd_delta", "priority", "mastery"]
    },
    {
      "type": "table",
      "name": "✅ Mastered — Spaced Repetition",
      "description": "Review schedule for consolidated knowledge",
      "sort": [{"property": "next_review", "direction": "asc"}],
      "filter": {
        "property": "status",
        "operator": "eq",
        "value": "mastered"
      },
      "columns": ["title", "mastery", "review_count", "next_review", "last_reviewed"]
    },
    {
      "type": "table",
      "name": "📍 Full Path",
      "description": "Complete ordered learning sequence",
      "sort": [{"property": "path_position", "direction": "asc"}],
      "columns": ["path_position", "title", "level", "status", "mastery", "zpd_delta", "tension_level", "criticality", "estimated_minutes"]
    }
  ]
}
```

---

## Layout Algorithm

```python
LAYOUT = {
    "L0": {"y_base": 0,    "color": "6"},
    "L1": {"y_base": 300,  "color": "1"},
    "L2": {"y_base": 650,  "color": "4"},
    "L3": {"y_base": 1000, "color": "5"},
}
NODE_W, NODE_H = 280, 160
H_GAP, V_GAP = 40, 80
COLS_PER_ROW = 5

# Position: col × (NODE_W + H_GAP), row × (NODE_H + V_GAP) + level_y_base
# Critical nodes: y_offset += 20 (visual prominence within row)
# Scaffold nodes: color override to "5", width = 220 (visually distinct)
```
