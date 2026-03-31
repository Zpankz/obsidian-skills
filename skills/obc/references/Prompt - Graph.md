---
title: "Prompt - Graph"
created: 2026-03-25
description: "Prompt - Graph"
tags:
  - "vault-command"
related:
  - "[[Prompt - Map]]"
  - "[[Prompt - Backlinks]]"
  - "[[Prompt - Audit]]"
  - "[[Prompt - Connect]]"
  - "[[Prompt - Emerge]]"
---
## Graph -- Quantitative Graph Analytics for Your Vault

Performs structural graph analytics on the vault's link topology -- centrality metrics, community detection, core-periphery analysis, and decomposition recommendations. The quantitative counterpart to /map. Where /map tells you the story of your vault's structure, /graph gives you the numbers.

**Usage:** `/graph` (full analytics) or `/graph [note]` (ego-network analysis for a specific note)

---

## What Makes This Different

This is NOT:

- [[Prompt - Map|/map]] (qualitative topology narrative -- Graph produces quantitative metrics and ranked tables)
- [[Prompt - Backlinks|/backlinks]] (wires missing links -- Graph analyzes the existing link structure without modifying it)
- [[Prompt - Audit|/audit]] (health check with action plan -- Graph is pure structural analysis, the analytical foundation Audit builds on)
- [[Prompt - Connect|/connect]] (finds bridges between two domains -- Graph identifies bridges across the entire vault computationally)

This IS: **Quantitative graph analytics with centrality scores, community structure, and structural recommendations.** Every note gets a number. Every cluster gets boundaries. Every structural role (hub, authority, broker, bridge, peripheral) gets identified. The output is tables and metrics, with narrative only to interpret them.

---

## Phase 1: Build Adjacency

Construct the vault's link graph. Start with vault-level metrics:

```bash
obsidian vault                                       # Total files, folders, size — the baseline
obsidian files total                                 # Total note count
obsidian links file="<note>" format=json             # repeat for every note, or sample the top 50-100
obsidian backlinks file="<note>" counts format=json  # inbound links for each
```

For large vaults, sample strategically: all notes with 3+ backlinks, plus a random sample of the rest. For smaller vaults (<200 notes), enumerate everything.

### Baseline Metrics

| Metric | Value |
|---|---|
| Total nodes (notes) | N |
| Total directed edges (links) | N |
| Graph density | edges / (nodes x (nodes-1)) |
| Average in-degree | N |
| Average out-degree | N |
| Max in-degree (note name) | N |
| Max out-degree (note name) | N |
| Reciprocal link rate | N% (links that go both directions) |

---

## Phase 2: Centrality Analysis

Compute five centrality metrics for each note. In practice, approximate these from the link and backlink data available through the CLI.

### In-Degree (Authority)

How many notes link TO this note. High in-degree = the vault treats this as authoritative.

```bash
obsidian backlinks file="<note>" counts format=json
```

### Out-Degree (Hub)

How many notes this note links TO. High out-degree = this note curates and connects.

```bash
obsidian links file="<note>" format=json
```

### Betweenness (Broker)

How many shortest paths between other notes pass through this one. High betweenness = this note is a critical connector. Removing it would fragment the graph.

Approximate betweenness by identifying notes that are the only connection between two clusters. Notes that appear in multiple clusters' backlink neighborhoods but belong to neither are likely high-betweenness.

### Closeness (Reach)

Average distance from this note to all other notes. High closeness = this note can reach everything quickly. It's central to the overall graph.

Approximate by counting how many notes are reachable within 1 hop, 2 hops, 3 hops.

### PageRank (Recursive Influence)

A note is important if important notes link to it. PageRank captures recursive influence -- being linked from a well-connected hub counts more than being linked from a peripheral note.

Approximate by weighting backlinks by the backlink count of the linking note.

### Centrality Table

Present the top 20 notes sorted by each metric:

| Rank | Note | In-Degree | Out-Degree | Betweenness | Closeness | PageRank |
|---|---|---|---|---|---|---|
| 1 | ... | N | N | est. | est. | est. |
| 2 | ... | N | N | est. | est. | est. |

Highlight notes that rank in the top 10 on 3+ metrics. These are the vault's most structurally important notes.

---

## Phase 3: Community Detection

Use tag co-occurrence and link patterns to identify clusters of notes that are more densely connected to each other than to the rest of the graph.

```bash
obsidian tags counts sort=count format=json | jq '.[0:25]'       # Top 25 themes — community seeds
obsidian backlinks file="<candidate cluster hub>" counts format=json
obsidian links file="<candidate cluster hub>" format=json
obsidian wordcount file="<candidate cluster hub>"                # Content depth alongside structural position
```

### Method

1. Start from the highest in-degree notes. Their backlink neighborhoods form initial cluster candidates.
2. For each candidate cluster, check internal density: what fraction of possible links between cluster members actually exist?
3. Merge overlapping clusters. Split clusters where internal density is low.
4. Assign remaining notes to the nearest cluster (most links to that cluster's members).

### Community Table

For each detected community:

| Community | Central Node | Size | Internal Density | Cross-Cluster Links | Top Tags |
|---|---|---|---|---|---|
| \[Name\] | \[Note\] | N notes | N% | N links to N other communities | tag1, tag2 |

### Cross-Community Bridges

Notes that have significant links to 2+ communities. These are the vault's bridge notes -- they connect different areas of thinking.

| Bridge Note | Communities Connected | Links to Each |
|---|---|---|
| \[Note\] | Community A (N), Community B (N) | ... |

---

## Phase 4: Core-Periphery Analysis

Classify every note into one of three structural roles:

### Core

High centrality + high betweenness + high PageRank. These notes are load-bearing. The vault's structure depends on them. Removing a core note would visibly fragment or weaken the graph.

### Semi-Periphery

Moderate scores on centrality metrics. Connected enough to be useful, but not structurally critical. Most notes in a healthy vault are semi-peripheral.

### Periphery

Low scores across all metrics. Weakly connected or disconnected. Peripheral notes are either new (haven't been integrated yet), niche (properly specialized), or neglected (should be connected but aren't).

### Classification Table

| Role | Count | % of Vault | Examples |
|---|---|---|---|
| Core | N | N% | \[top 5 note names\] |
| Semi-Periphery | N | N% | -- |
| Periphery | N | N% | \[notable examples\] |

A healthy vault has 5-15% core, 50-70% semi-periphery, and 20-40% periphery. Significant deviation from these ranges signals structural issues.

---

## Phase 5: Structural Recommendations

### Bridge Notes

Notes that are the sole connection between two communities. These are valuable but fragile. Recommendation: reinforce by adding alternative paths between the communities.

### Articulation Points

Notes whose removal would disconnect the graph into separate components. These are the vault's single points of failure.

```bash
obsidian backlinks file="<suspected articulation point>" counts format=json
obsidian links file="<suspected articulation point>" format=json
```

For each articulation point: what communities would become disconnected? How many notes would be isolated?

### Potential Mediator Notes

Pairs of notes with many common neighbors but no direct link. These "should" be connected based on structural position. They're the graph's missing edges.

### Structural Health Summary

- **Robustness:** How many articulation points? (fewer = more robust)
- **Efficiency:** Average path length between notes. (shorter = more efficient navigation)
- **Balance:** Are communities roughly similar in size, or is one dominant? (balanced = healthier)
- **Integration:** What percentage of notes are in the periphery? (lower = better integrated)

---

## Ego-Network Mode: `/graph [note]`

If called with a specific note, skip the full vault analysis and focus on that note's neighborhood.

### Ego-Network (1-2 Hop Neighborhood)

```bash
obsidian backlinks file="<note>" counts format=json
obsidian links file="<note>" format=json
```

For each 1-hop neighbor, also get their links and backlinks to build the 2-hop neighborhood.

### Note Profile

| Metric | Value | Vault Rank |
|---|---|---|
| In-degree | N | #N of N total |
| Out-degree | N | #N of N total |
| Betweenness (est.) | ... | #N of N total |
| PageRank (est.) | ... | #N of N total |
| Community | \[name\] | \[role in community\] |
| Structural role | Hub / Authority / Broker / Peripheral | -- |

### Role Classification

- **Hub:** High out-degree, links to many notes. Curates and organizes.
- **Authority:** High in-degree, many notes link here. The vault treats this as a key reference.
- **Broker:** High betweenness, connects otherwise disconnected areas.
- **Peripheral:** Low on all metrics. Weakly integrated.

### Connectivity Recommendations

What it would take to increase this note's connectivity and structural importance:

1. **Quick wins:** Notes in the same community that should link here but don't.
2. **Bridge potential:** Notes in other communities that share themes but aren't connected.
3. **Missing reciprocals:** Notes this links to that don't link back.

---

## Output Format

**GRAPH ANALYTICS -- \[Date\]**
**Scope:** \[Full vault / Ego-network for \[note name\]\]
**Nodes:** N | **Edges:** N | **Density:** N

---

\[Baseline metrics table\]

\[Centrality table (top 20)\]

\[Community table\]

\[Cross-community bridges\]

\[Core-periphery classification\]

\[Structural recommendations\]

---

## Output Guidelines

- Tables for metrics, narrative for insights. The numbers should be scannable; the interpretation should explain what they mean.
- Name actual notes, not abstractions. "Note X has betweenness rank #3" is useful. "Some notes are more central" is not.
- Centrality approximations are approximations. Label them as estimates and explain the method. Don't present approximate betweenness as if it were computed exactly.
- The structural recommendations are the actionable output. Metrics without recommendations are academic.
- For ego-network mode, focus on what the user can DO to improve the note's position. The profile is context; the recommendations are the value.
- A vault with high density everywhere is not necessarily healthy -- it might mean everything links to everything, which dilutes signal. Call out over-linking if present.

---

## Related Commands

- [[Prompt - Map|/map]] -- Analyzes vault topology, clusters, gaps, and the shape of thinking across the vault
- [[Prompt - Backlinks|/backlinks]] -- Wires the vault graph by finding and executing missing connections
- [[Prompt - Audit|/audit]] -- Vault structural health check combining analysis with action plan
- [[Prompt - Connect|/connect]] -- Finds unexpected bridges between two separate domains in the vault
- [[Prompt - Emerge|/emerge]] -- Surfaces ideas the vault implies but has never explicitly stated