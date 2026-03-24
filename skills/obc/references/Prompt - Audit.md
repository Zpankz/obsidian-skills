---
title: "Prompt - Audit"
created: 2026-03-25
description: "Prompt - Audit"
tags:
  - "vault-command"
related:
  - "[[Prompt - Backlinks]]"
  - "[[Prompt - Make]]"
  - "[[Prompt - Map]]"
  - "[[Prompt - Graduate]]"
  - "[[Prompt - XArticle]]"
  - "[[Prompt - Graph]]"
---
## Audit -- Vault Structural Health Check

Combines backlink analysis with readiness scoring to find structural weaknesses, orphaned value, and ideas that are mature enough to act on. The comprehensive diagnostic that tells you what shape your vault is in and what to do about it.

**Usage:** `/audit` (full vault) or `/audit [folder]` (focused on a specific folder)

---

## What Makes This Different

This is NOT:

- [[Prompt - Map|/map]] (qualitative topology overview -- Audit produces quantitative health metrics and action plans)
- [[Prompt - Backlinks|/backlinks]] (wires missing links -- Audit diagnoses structural health broadly, linking is one output)
- [[Prompt - Make|/make]] (scores idea readiness -- Audit scores vault health, with readiness as one dimension)
- [[Prompt - Graduate|/graduate]] (promotes daily note ideas -- Audit identifies mature notes across the whole vault, not just daily notes)

This IS: **A comprehensive health check that combines structural analysis + readiness scoring + a prioritized action plan.** Think of it as a physical exam for your vault. The output is a diagnosis and a treatment plan.

---

## Phase 1: Structural Scan

Get baseline metrics for the vault (or folder if scoped):

```bash
obsidian vault                                           # Total files, folders, size — the baseline
obsidian orphans total                                   # Count orphans first
obsidian orphans                                         # List orphans
obsidian deadends                                        # Notes with no outgoing links
obsidian unresolved counts verbose format=json           # Referenced but never created, ranked by frequency
obsidian tags counts sort=count format=json | jq '.[0:25]'  # Top 25 themes, machine-readable
obsidian files total                                     # Total vault file count
obsidian recents                                         # Recently modified notes — for recency assessment
```

Compute structural KPIs:

- **Orphan ratio:** orphan count / total notes. How much of the vault is disconnected?
- **Average links per note:** total directed edges / total notes. How dense is the graph?
- **Cross-folder link rate:** links between different folders / total links. How siloed is the vault?
- **Deadend ratio:** deadend count / total notes. How much thinking stopped developing?
- **Unresolved ratio:** unresolved links / total links. How many ideas were referenced but never formalized?

```bash
obsidian backlinks file="<hub note A>" counts format=json
obsidian backlinks file="<hub note B>" counts format=json
obsidian links file="<hub note A>" format=json
obsidian links file="<hub note B>" format=json
```

Map the top 10-15 most connected notes. These are the load-bearing nodes of the vault.

---

## Phase 2: Readiness Scan

For notes with high backlink counts (top 20%), score their maturity:

```bash
obsidian backlinks file="<note>" counts format=json
obsidian properties file="<note>"
obsidian wordcount file="<note>"
obsidian outline file="<note>" format=json
```

For each high-connectivity note, assess:

- **Thesis clarity:** Does this note state a clear position or just collect fragments?
- **Connection quality:** Are its backlinks meaningful (same-topic notes) or noise (generic references)?
- **Recency:** Has it been touched in the last 30 days? 90 days? Longer?
- **Structural completeness:** Does it have headings, developed sections, or is it a stub?
- **Context integration:** Is it referenced from context files? Does it connect to active projects?

Score each on a simple Ready / Almost / Developing / Dormant scale:

- **Ready:** Clear thesis, deep connections, recent activity. Could be acted on (graduated, published, expanded) today.
- **Almost:** Has substance but missing one thing -- a clear thesis, recent attention, or key connections.
- **Developing:** Has potential but needs significant work. Multiple gaps.
- **Dormant:** Was once active but hasn't been touched in 90+ days. May still hold value.

---

## Phase 3: Health Dashboard

### KPI Table

| Metric | Value | Status | Benchmark |
|---|---|---|---|
| Total notes | N | -- | -- |
| Orphan ratio | N% | Green/Yellow/Red | <10% Green, 10-25% Yellow, >25% Red |
| Avg links per note | N | Green/Yellow/Red | >3 Green, 1.5-3 Yellow, <1.5 Red |
| Cross-folder link rate | N% | Green/Yellow/Red | >20% Green, 10-20% Yellow, <10% Red |
| Deadend ratio | N% | Green/Yellow/Red | <15% Green, 15-30% Yellow, >30% Red |
| Unresolved ratio | N% | Green/Yellow/Red | <10% Green, 10-20% Yellow, >20% Red |

### Top 10 Orphans Worth Rescuing

Not all orphans matter. These are the ones with substance (high word count, clear topic, connection to active priorities) that would add the most value if connected:

| # | Note | Word Count | Topic | Suggested Connection |
|---|---|---|---|---|
| 1 | ... | ... | ... | Link to \[hub note\] because ... |

### Top 10 Mature Notes Ready for Graduation

Notes with the highest readiness scores that could become essays, standalone resources, or published work:

| # | Note | Readiness | Backlinks | Thesis | Suggested Action |
|---|---|---|---|---|---|
| 1 | ... | Ready | N | "..." | Publish as essay / Expand into project / ... |

### Structural Weak Points

- **Single points of failure:** Notes that, if removed, would disconnect major clusters. These are fragile -- they need reinforcement (more cross-links around them).
- **Isolated clusters:** Groups of notes that only connect to each other and nothing else.
- **Tag sprawl:** Tags used only once or twice. These fragment rather than organize.

---

## Phase 4: Action Plan

Produce a prioritized list of specific actions, ordered by impact:

### Critical (Do This Week)

Actions that address structural problems actively degrading vault value:

1. **\[Action\]:** \[Specific instruction\]. Why: \[impact\].
2. ...

### High (Do This Month)

Actions that would meaningfully improve vault health:

1. **\[Action\]:** \[Specific instruction\]. Why: \[impact\].
2. ...

### Medium (Backlog)

Actions worth doing when time allows:

1. **\[Action\]:** \[Specific instruction\]. Why: \[impact\].
2. ...

Action types include:

- **Link:** Connect note A to note B (specific location in the file)
- **Graduate:** Promote note X from daily notes to standalone (see [[Prompt - Graduate|/graduate]])
- **Merge:** Combine notes A and B (they cover the same topic under different names)
- **Delete:** Remove note X (empty stub with no backlinks and no value)
- **Create:** Build note X (referenced N times but never created)
- **Reinforce:** Add cross-links around fragile bridge note X

---

## Temporal Tracking

Compare against prior /audit runs:

```bash
obsidian search query="/audit" path="Daily Notes"
obsidian search query="vault health" path="Daily Notes"
obsidian search query="orphan ratio" path="Daily Notes"
```

If prior runs found:

- **KPI trends:** Is the orphan ratio improving or worsening? Are links per note increasing?
- **Action completion:** Which actions from the last audit were completed? What was the impact?
- **Regression detection:** Did any previously healthy metrics deteriorate? Why?

Present trends as directional arrows: improving, stable, or declining.

---

## Anti-Patterns

**1. The Stat Dump**
Producing metrics without interpretation. Every number needs context: is it good or bad? What should the user do about it? Numbers without actions are noise.

**2. The Completionist**
Suggesting the user fix every orphan and resolve every dead link. Focus on the 20% of actions that produce 80% of the value. A vault doesn't need to be perfect -- it needs to be functional.

**3. The Blame Game**
Framing the audit as a report card. This is a diagnostic tool, not a judgment. Orphans happen. Dead ends are natural. The question is which ones matter.

**4. The False Positive**
Flagging structural issues that aren't actually problems. Some notes should be orphans (reference material, templates). Some clusters should be isolated (distinct projects). Don't recommend connections that don't make sense just to improve metrics.

---

## Output Format

**AUDIT REPORT -- \[Date\]**
**Scope:** \[Full vault / Folder name\]
**Prior audit:** \[Date of last run, or "First run"\]

---

\[KPI Table with status indicators\]

\[Top 10 Orphans Worth Rescuing\]

\[Top 10 Mature Notes Ready for Graduation\]

\[Structural Weak Points\]

---

\[Action Plan by priority tier\]

---

\[Temporal comparison, if prior runs exist\]

---

## Output Guidelines

- Be specific: name actual notes, cite backlink counts, show exact connections to make.
- The KPI table should be scannable in 10 seconds. The action plan should be actionable in 30 minutes.
- Don't recommend fixing things that aren't broken. A vault with a 15% orphan ratio and high average links is healthy.
- The most valuable output is the action plan. If the user does nothing else, the top 3 Critical actions should improve vault health measurably.
- This should feel like a maintenance report from someone who knows the system, not a generic checklist.

---

## Related Commands

- [[Prompt - Backlinks|/backlinks]] -- Wires the vault graph by finding and executing missing connections
- [[Prompt - Make|/make]] -- Scans the vault for ideas ready to become something the world sees
- [[Prompt - Map|/map]] -- Analyzes vault topology, clusters, gaps, and the shape of thinking across the vault
- [[Prompt - Graduate|/graduate]] -- Extracts ideas from daily notes and promotes them to standalone notes
- [[Prompt - XArticle|/xarticle]] -- Finds which idea is most ready to become an X article by scoring graph density, energy, and synthesis potential