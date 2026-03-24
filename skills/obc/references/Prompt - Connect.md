---
title: "Prompt - Connect"
created: 2026-03-06
description: "Prompt - Connect"
tags:
  - "vault-command"
related:
  - "[[Prompt - Emerge]]"
  - "[[Prompt - Map]]"
  - "[[Prompt - Backlinks]]"
  - "[[Prompt - Synthesize]]"
  - "[[Prompt - Graph]]"
---
## Connect — Find Unexpected Bridges Between Domains

Takes two separate projects, topics, or domains and uses the vault's graph to find non-obvious connections between them.

**Usage:**`/connect [domain A] [domain B]` -- e.g., `/connect design engineering` or `/connect software fashion architecture`

---

## Step 1: Map Each Domain

For each of the two domains provided, build a picture of what exists in the vault:

```bash
obsidian search query="<domain A>" format=json                      # All notes mentioning this domain
obsidian search:context query="<domain A>" format=json              # With matching lines
obsidian backlinks file="<main note for domain A>" counts format=json  # Ranked inbound connections
obsidian links file="<main note for domain A>" format=json          # Outbound connections
obsidian tags file="<main note for domain A>"                       # Tags on the hub note
obsidian wordcount file="<main note for domain A>"                  # Thinking depth
```

Repeat for domain B.

Follow backlinks 2-3 hops from each domain's hub notes. Build a list of all notes, people, concepts, and themes that exist in each domain's neighborhood.

### Depth Asymmetry Handling

If Domain A has significantly more notes than Domain B (e.g., 50 vs. 10), pay extra attention to bridges from the smaller domain. The smaller domain's notes often contain insights the larger domain hasn't considered. The less-explored territory is where the surprises are.

When one domain is thin, go deeper on its backlinks. Follow 3-4 hops instead of 2-3. A sparse domain's connections are more valuable per link.

## Step 2: Find the Overlaps

Compare the two neighborhoods. Look for:

Notes that appear in both domains' backlink chains. These are natural bridges.

People mentioned in both domains. What's their role in each?

Concepts, values, or questions that appear in both domains even if the notes aren't linked.

```bash
obsidian search:context query="<theme from domain A>" format=json  # search within domain B's neighborhood
```

Structural similarities: both domains facing the same kind of problem, both evolving in the same direction, both stuck on the same question.

```bash
obsidian tags file="<notes in domain A>"
obsidian tags file="<notes in domain B>"
```

Tags that appear in both domains indicate thematic overlap.

## Step 3: Trace the Bridges

For each connection found, trace it deeper:

```bash
obsidian backlinks file="<bridging note>" counts format=json  # How connected is this bridge?
obsidian links file="<bridging note>" format=json
obsidian wordcount file="<bridging note>"                     # Is the bridge developed or thin?
```

How deep does the connection go? Is it surface-level (same word used) or structural (same underlying pattern)?

### Path-Finding

For the strongest bridges, trace the shortest path between the two domain hubs through the vault graph. What notes sit in between? These intermediary notes are often the most interesting, because they live at the intersection of two worlds without belonging fully to either.

```bash
obsidian backlinks file="<intermediary note>" counts format=json
obsidian links file="<intermediary note>" format=json
obsidian outline file="<intermediary note>" format=json  # What's inside? Structure reveals the connection's nature
```

What does that intermediary note contain? Why does it connect these two domains? This is often where the real insight lives.

### Temporal Analysis

Sort bridges by date of creation or last modification. Are the domains converging (recent connections increasing) or diverging (connections mostly old, nothing new)?

## Step 4: Synthesize

### Connection Map

For each bridge found:

**Bridge \[#\]: \[Title\]**

- **In Domain A:** \[How this concept/note/person appears\]
- **In Domain B:** \[How it appears differently\]
- **The connection:** \[What links them, and why it's interesting\]
- **Depth:** Surface / Structural / Foundational
- **Implication:** \[What this connection suggests for either domain\]

### The Strongest Bridge

The single most interesting connection between these domains. The one that reframes how you think about both.

### Missing Links

Connections that SHOULD exist based on the evidence but haven't been made yet. Suggest specific notes to link or create.

### The Question This Raises

What new question emerges from seeing these two domains connected that wasn't visible when they were separate?

---

## Output Format

**CONNECT: \[Domain A\] <-> \[Domain B\]**  
**Notes in A's neighborhood:** \[number\]  
**Notes in B's neighborhood:** \[number\]  
**Bridges found:** \[number\]  
**Trend:** \[Converging / Diverging / Stable\]

\[Connection map\]

\[Strongest bridge\]

\[Missing links\]

\[The question\]

---

## Output Guidelines

- The value is in non-obvious connections. If the bridge is something you already know, dig deeper.
- Always cite specific notes and dates.
- The best output makes you see both domains differently.
- Don't force connections that aren't there. If two domains genuinely don't connect, say so.

---

## Related Commands

- [[Prompt - Emerge|/emerge]] — Surfaces ideas the vault implies but has never explicitly stated
- [[Prompt - Map|/map]] — Analyzes vault topology, clusters, gaps, and the shape of thinking across the vault
- [[Prompt - Backlinks|/backlinks]] — Wires the vault graph by finding and executing missing connections