<!--
DIRECTORY TREE (orientation)
references/02-pkg-gkg-differential.md
  Covers: gap algebra · priority formula · mastery scoring · CLI analytics output
  Depends on: none (standalone)
  Used by: /path scan · /path gap · /path status · /path compound
-->

# PKG/GKG Differential Analysis

## Contents
- [Graph Definitions](#graph-definitions)
- [Gap Algebra](#gap-algebra)
- [Priority Formula](#priority-formula)
- [Mastery Scoring](#mastery-scoring)
- [CLI Analytics Output Spec](#cli-analytics-output)

---

## Graph Definitions

```
GKG (Global Knowledge Graph)
  = canonical domain ontology constructed via RPP L0–L3 decomposition
  = complete set of nodes and edges representing the domain
  Node attributes: id, title, level, difficulty, prerequisites, unlocks, cluster

PKG (Personal Knowledge Graph)
  = learner's current mastery state
  = subset of GKG nodes with mastery scores ∈ [0, 1]
  Source: vault frontmatter scan OR explicit mastery ratings OR test performance

Δ (Gap Set)
  = GKG \ {n ∈ GKG : mastery(n) ≥ MASTERED_THRESHOLD}
  MASTERED_THRESHOLD = 0.85  (update in lessons.md if recalibrated)

Mastered set M = GKG \ Δ
Coverage = |M| / |GKG|  (reported by /path status)
```

---

## Gap Algebra

```python
def compute_gap(gkg: Graph, pkg: MasteryMap) -> list[GapNode]:
    gap = []
    for node in gkg.nodes:
        mastery = pkg.get(node.id, 0.0)  # default 0 if unseen
        if mastery < MASTERED_THRESHOLD:
            node.mastery = mastery
            node.gap_depth = node.difficulty × (1 − mastery)
            gap.append(node)
    return gap

def topological_sort_with_priority(gap: list[GapNode]) -> list[GapNode]:
    """Kahn's algorithm; priority as tiebreaker within same in-degree."""
    # Standard Kahn's algorithm
    # Tiebreaker: highest priority first when in_degree equal
    pass
```

**Partial mastery handling**: A node with mastery 0.4 is in the gap (below 0.85)
but is treated as partially scaffolded — its predecessors need less emphasis.

---

## Priority Formula

```
Priority(node) = C(node) × I(node) × (1 − m(node))

Where:
  C(node) = eigenvector_centrality(node, GKG)    ∈ [0, 1]
  I(node) = log(1 + |transitively_unlocked(node)|)  (log-scaled impact)
  m(node) = current mastery ∈ [0, 1]

Intuition:
  High centrality = many paths flow through this node
  High impact     = unlocks many downstream nodes
  Low mastery     = large remaining gap to fill
  Product         = leverage × remaining work = optimal priority

Special cases:
  Prerequisite-blocked node: Priority × 0.5 until prerequisites met
  Scaffold node:             Priority = predecessor.priority × 1.1
  L0 node (first pass):     Priority = max(all priorities) + 1  (always first)
```

---

## Mastery Scoring

**Sources** (in priority order):
1. Vault frontmatter `mastery:` field (most accurate, manually set)
2. Spaced repetition performance history (`review_scores` array)
3. Test/exam performance mapping
4. Default: 0.0 (no evidence = unknown)

**EMA update** (post-session):
```
mastery_new = (1 − α) × mastery_old + α × session_score
α = 0.30  (learning rate)

session_score sources:
  self-assessment: [0.0, 0.25, 0.50, 0.75, 1.0]
  quiz performance: n_correct / n_total
  viva: examiner rating normalised to [0, 1]
```

**Spaced repetition interval**:
```
easiness_factor = 1.3 + 0.9 × mastery  ∈ [1.3, 2.2]
interval(1) = 1 day
interval(2) = 3 days
interval(n) = interval(n-1) × easiness_factor, max=21 days
```

---

## CLI Analytics Output

Analytics computed by each `/olp` command and injected into context as YAML:

### `/path scan <vault>` → mastery_distribution.yaml
```yaml
scan_summary:
  vault_path: ./my_vault
  nodes_found: 87
  mastery_distribution:
    unknown_0.0:    34  (39%)
    learning_0-0.5: 28  (32%)
    proficient_0.5-0.85: 18  (21%)
    mastered_0.85+:  7   (8%)
  coverage: 8%
  highest_priority_gaps:
    - fick_principle: priority=0.82, mastery=0.0
    - time_constant:  priority=0.74, mastery=0.1
```

### `/path gap` → gap_priority_queue.yaml
```yaml
gap_analysis:
  total_gap_nodes: 80
  estimated_hours: 26.7
  top_10_by_priority:
    - rank: 1
      node: fick_principle
      level: L1
      priority: 0.82
      centrality: 0.91
      impact_unlocks: 14
      mastery: 0.0
      zpd_delta_from_L0: 0.22
    # ...
  critical_path:
    # Minimum nodes to master before exam date
    - fick_principle → time_constant → henderson_hasselbalch → ...
```

### `/path status` → status_report.yaml
```yaml
status:
  coverage: 35%
  mastered: 42/120
  in_progress: 15
  gap: 63
  next_3_nodes:
    - {node: time_constant, est_minutes: 25, tension: high}
    - {node: hill_equation, est_minutes: 20, tension: medium}
    - {node: spare_receptors, est_minutes: 15, tension: medium}
  estimated_completion_hours: 18.5
  days_to_exam: 4
  feasibility: WARNING — 18.5h needed, 4d×3h/d = 12h available
```
