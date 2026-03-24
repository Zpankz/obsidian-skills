---
title: "Prompt - Map"
created: 2026-03-06
description: "Prompt - Map"
tags:
  - "vault-command"
related:
  - "[[Prompt - Connect]]"
  - "[[Prompt - Backlinks]]"
  - "[[Prompt - Emerge]]"
  - "[[Prompt - XArticle]]"
  - "[[Prompt - Audit]]"
  - "[[Prompt - Graph]]"
---
## Map — Vault Topology & Intellectual Landscape

Analyze the structure and shape of thinking across the entire vault. Show where ideas are concentrated, where the dead zones are, what's central vs. peripheral, and what connections are missing.

**Usage:**`/map`

---

## Step 1: Structural Analysis

Get the full picture of vault structure using structured output for quantitative analysis:

```bash
obsidian vault                                          # Total files, folders, size at a glance
obsidian tags counts sort=count format=json | jq '.[0:25]'  # Top 25 themes with counts
obsidian orphans total                                  # Count orphans
obsidian orphans                                        # List orphans
obsidian deadends                                       # Notes with no outgoing links
obsidian unresolved counts verbose format=json          # Broken [[links]] ranked by reference count
```

Get link density for key notes — use `counts format=json` to find the true hubs:

```bash
obsidian backlinks file="<Hub Note A>" counts format=json  # Inbound links, ranked
obsidian backlinks file="<Hub Note B>" counts format=json
obsidian links file="<Hub Note A>" format=json             # Outbound links
obsidian links file="<Hub Note B>" format=json
obsidian wordcount file="<Hub Note A>"                     # Thinking density (words, not just links)
```

Count and categorize:

```bash
obsidian folder path="Daily Notes" info=files    # Daily note count + size
obsidian folder path="Essays" info=files         # Essay count + size
obsidian files total                             # Total vault file count
```

## Step 2: Identify Clusters

Trace the major clusters of thinking by following backlink chains from the most connected notes:

```bash
obsidian backlinks file="<highly connected note>" counts format=json  # Ranked inbound connections
obsidian links file="<highly connected note>" format=json             # Outbound connections
obsidian wordcount file="<highly connected note>"                     # Thinking depth (word count)
obsidian outline file="<highly connected note>" format=json           # Heading structure
```

For each cluster:

- What's the central node?
- How many notes are in the cluster?
- How dense are the internal connections?
- Does this cluster connect to other clusters, or is it isolated?

### Cluster Relationship Narrative

Don't just list clusters. Describe how they relate to each other:

- Which clusters should be connected but aren't? These are the biggest structural gaps.
- Which clusters are bridged by a single note? That note is a critical junction. If it were removed, two areas of thinking would become disconnected.
- Which clusters are appropriately separate? Not everything needs to connect.
- Where are the superclusters (groups of clusters that form a larger meta-theme)?

## Step 3: Find the Gaps

### Missing Connections

```bash
obsidian search:context query="<theme from cluster A>" format=json  # Does this appear in cluster B?
```

### Orphaned Value

Review orphaned notes. For each one, apply this decision logic:

### Unresolved Links

Review unresolved `[[links]]`. These are ideas referenced but never developed:

- Which ones are worth creating notes for?
- Which ones represent important thinking that never got its own space?

### Dead Zones

Areas of stated interest or priority that have very few notes or thin thinking. Compare stated priorities in context files against actual note density.

### Tag-to-Priority Ratio

For the top 10 tags by count, cross-reference against stated priorities in context files:

| Tag | Note Count | Stated Priority? | Ratio |
| --- | --- | --- | --- |
| ... | ... | High/Medium/Low/None | ... |

Ratios where a tag has high stated priority but low note count indicate **dead zones**: areas you say matter but aren't actually developing. Ratios where a tag has high note count but low stated priority indicate **attention sinks**: areas absorbing energy without being strategic.

## Step 4: Synthesize

### Vault Overview

- Total notes, daily notes, essays, context files
- Most connected notes (hubs)
- Most isolated notes (orphans worth rescuing)
- Tag distribution (where thinking is concentrated)

### Cluster Map

List each major cluster with:

- **Name**: What this cluster is about
- **Hub note**: The most connected note in this cluster
- **Size**: Approximate number of notes
- **Density**: How interconnected the notes are
- **Health**: Active and growing / Stable / Stagnant / Neglected
- **Connections to other clusters**: Which clusters does this one bridge to?

### The Shape of Your Thinking

A narrative description of what the vault reveals about where attention and intellectual energy are going. What dominates? What's underdeveloped relative to its stated importance?

### Strongest Connections

The most surprising or valuable links between clusters. Things that connect across domains in non-obvious ways.

- Notes to create (from unresolved links)
- Connections to make (orphans to connect, clusters to bridge)
- Areas to develop (dead zones that matter)
- Notes to revisit (orphaned value worth rescuing)

---

## Output Format

**VAULT MAP -- \[Date\]**

\[Overview stats\]

\[Cluster map with relationship narrative\]

\[Shape narrative\]

\[Tag-to-priority analysis\]

\[Gaps and dead zones\]

\[Recommended actions\]

---

## Output Guidelines

- Be specific: name actual notes, not abstractions
- The map should make the user see their vault differently than before running this command
- Focus on actionable insights, not just statistics
- The most valuable output is connections that should exist but don't

---

## Related Commands

- [[Prompt - Connect|/connect]] — Finds unexpected bridges between two separate domains in the vault
- [[Prompt - Backlinks|/backlinks]] — Wires the vault graph by finding and executing missing connections
- [[Prompt - Emerge|/emerge]] — Surfaces ideas the vault implies but has never explicitly stated
- [[Prompt - XArticle|/xarticle]] — Uses vault topology as a signal for article readiness, scoring topics on density, energy, and synthesis potential