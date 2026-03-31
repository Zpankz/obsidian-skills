---
title: "Prompt - Backlinks"
created: 2026-03-06
description: "Prompt - Backlinks"
tags:
  - "vault-command"
related:
  - "[[Prompt - Connect]]"
  - "[[Prompt - Map]]"
  - "[[Prompt - Graduate]]"
  - "[[Prompt - Audit]]"
  - "[[Prompt - Graph]]"
---
## Backlinks — Wire the Graph

Your vault is the context layer for an augmented cognition system. Every missing link is a capability the agent doesn't have. Every connection made compounds because the agent uses it in every future [[Prompt - Today|/today]], [[Prompt - Connect|/connect]], [[Prompt - Trace|/trace]], [[Prompt - Challenge|/challenge]], and [[Prompt - Ideas|/ideas]] run. A connection that only existed in your head used to be fine. Now it's a capability gap that grows across every interaction.

**The boundary:** Your job is to make the graph traversable, not to generate understanding. You connect. The user thinks. When you find an empty hub, flag it. Don't fill it. When you find notes that should link, wire them. Don't rewrite them. The substance in this vault is human thinking. Your contribution is the wiring between those thoughts.

**Usage:**`/backlinks` or `/backlinks [cluster]`

If a cluster name is provided (e.g., `/backlinks defense-tech`), skip the full scan and focus Phases 3-4 on that cluster and its nearest neighbors. Faster results for known problem areas.

---

## Phase 1: Structural Inventory

Graph-only, fast. No content reads.

```bash
obsidian vault                                          # Total files, folders, size
obsidian orphans total                                  # Count orphans first
obsidian orphans                                        # List orphans
obsidian deadends                                       # Notes with no outgoing links
obsidian unresolved counts verbose format=json          # Broken [[links]] ranked by reference count
obsidian tags counts sort=count format=json | jq '.[0:25]'  # Top 25 themes
```

Get backlinks and links for top 15-20 hub notes. Use `counts format=json` for quantitative hub scoring:

```bash
obsidian backlinks file="<Hub Note A>" counts format=json  # Ranked inbound connections
obsidian backlinks file="<Hub Note B>" counts format=json
obsidian links file="<Hub Note A>" format=json
obsidian links file="<Hub Note B>" format=json
```

Also check any notes that appear as frequent backlink targets. Build a rough cluster map from the link structure. Use `jq length` to count connections quantitatively.

## Phase 2: Priority Context

Read 5-6 context files to build a priority filter:

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

Read recent daily notes (past 7 days):

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 7 days
```

Extract from these reads:

- Current priorities and active projects
- Open questions and active threads of thinking
- People and concepts getting current attention

This becomes the priority filter for scoring in Phase 6.

## Phase 3: Orphan Rescue Scan

Filter orphans from Phase 1. Skip non-note files:

- Images:.heic,.jpg,.jpeg,.png,.gif,.webp
- Media:.mov,.mp4,.wav,.mp3
- Fonts, canvases, templates
- Any file that isn't.md

For remaining orphans, apply this decision tree:

For each meaningful orphan, search for its nearest cluster neighbor:

```bash
obsidian search:context query="<key concept from orphan>" format=json  # Find nearest cluster neighbor
obsidian wordcount file="<orphan>"                                     # Is this worth rescuing? (thin vs. rich)
```

**Explicit cap:** Do not read more than 100 notes total across all phases. Be selective. Prioritize notes whose titles suggest relevance to current priorities.

## Phase 4: Cluster Bridge Analysis

```bash
obsidian search:context query="<theme from Cluster A>" format=json  # search in Cluster B's territory
```

Read intermediary notes that might serve as bridges between clusters.

Use synonym discovery like [[Prompt - Trace|/trace]] does: try 2-3 vocabulary variants for each concept. Ideas evolve under different names.

## Phase 5: Unresolved Link Triage

From the unresolved links gathered in Phase 1:

- **3+ references:** Likely worth creating as a stub note
- **2 references:** Check for near-duplicates or name variants of existing notes
- **1 reference:** Skip unless it's a critical concept from current priorities

Check for name variants that resolve to existing notes before recommending new stubs.

## Phase 6: Score and Recommend

Score each candidate connection on 3 dimensions (multiplicative):

| Dimension | What it measures | 1 | 3 | 5 |
| --- | --- | --- | --- | --- |
| Conceptual Strength | How real is this connection? | Same word, different context | Related problems/questions | Same thesis from different angles |
| Structural Impact | How much does this improve the graph? | 6th link to well-connected note | Rescues valuable orphan | Bridges two isolated clusters |
| Priority Alignment | Does it touch current priorities? | Neither note is active | One note relates to a priority | Both notes relate to active work |

- Composite = Conceptual x Structural x Priority (max 125)
- **Critical** (75+), **High** (40-74), **Medium** (15-39), **Low** (<15)

### Quality Controls

- Minimum Conceptual Strength of 2. Same word but different concept = skip.
- Cap at 30 total recommendations. Quality over quantity.
- Each connection must be explainable in one sentence.
- Include borderline cases with lower scores rather than silently excluding.

### Connection Taxonomy

Label each recommendation with one of these types:

1. **Orphan to Hub** - Orphaned note connected to its nearest cluster hub
2. **Cluster Bridge** - Two clusters share themes but zero links between them
3. **Internal Gap** - Within-cluster notes missing cross-references
4. **Empty Hub (flag only)** - Hub note referenced by many but has no content. Flagged for the user to write. NOT filled by agent.
5. **Semantic Twin** - Two notes about the same concept, different vocabulary
6. **Person to Concept** - Person note that should link to associated concepts
7. **Temporal Bridge** - Old thinking relevant to new work, never connected
8. **Unresolved Worth Creating** - `[[link]]` appearing 3+ times, worth formalizing

### Connection Card Format

For each recommendation:

```
### [#]. [Type]: [Short description]
**Score:** [X] (Conceptual [N] x Structural [N] x Priority [N])
**What:** [One-sentence description]
**Edit:** Add \`[[Target Note]]\` to [Source Note] in [section/location]
**Why:** [One sentence on what this unlocks]
```

For Empty Hub flags, use this format instead:

```
### [#]. Empty Hub: [Note name]
**Referenced by:** [list of notes that link to it]
**What this needs:** Your thinking. [N] notes point here and find nothing.
```

## Phase 7: Execute

Present findings by tier (Critical first).

Ask which to execute:

### Execution Rules

When executing approved connections:

### Post-Execution Verification

After making changes:

```bash
obsidian links file="<modified note>" format=json   # verify links resolved
obsidian backlinks file="<modified note>" counts format=json  # confirm new connections appear
```

Report: "Made X connections across Y notes. Z new stub notes created."

---

## Output Format

```
BACKLINKS REPORT -- [Date]
Vault size: [N] notes
Orphans assessed: [N] meaningful (of [N] total)
Connections recommended: [N] across [N] tiers

---
## Critical ([N])
[Connection cards]

## High ([N])
[Connection cards]

## Medium ([N])
[Connection cards]

## Summary
[Narrative: biggest structural gaps, what executing these changes unlocks]

---
Execute: All Critical+High / Critical only / Pick specific / None
```

---

## Limitations

Be honest about these:

- **False positives:** Include with lower score rather than silently exclude. Let the user decide.
- **Vocabulary drift:** Try 2-3 variants for each concept. Ideas evolve under different names.
- **Recency bias:** Flag old-but-rich orphans even if they don't match current priorities. Old thinking can be the most valuable.
- **Graph vs. content tension:** Well-connected notes can have shallow content. Poorly-connected notes can be deeply thoughtful. Connection count alone doesn't indicate value.

## Output Guidelines

- Be specific: name actual notes, cite content, show edit locations
- Quality over quantity. 10 excellent connections beat 30 mediocre ones.
- The best connections make you say "how was this not already linked?"
- Don't force connections. Same word but different concept = skip.
- After execution, report what changed and structural impact.

---

## Related Commands

- [[Prompt - Connect|/connect]] — Finds unexpected bridges between two separate domains in the vault
- [[Prompt - Map|/map]] — Analyzes vault topology, clusters, gaps, and the shape of thinking across the vault
- [[Prompt - Graduate|/graduate]] — Extracts ideas from daily notes and promotes them to standalone notes