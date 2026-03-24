---
title: "Prompt - XArticle"
created: 2026-03-25
description: "Prompt - XArticle"
tags:
  - "vault-command"
related:
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Learned]]"
  - "[[Prompt - Map]]"
  - "[[Prompt - Synthesize]]"
  - "[[Prompt - Audit]]"
---
## XArticle — Find What to Write Next

Scan the vault for the topic that is most ready to become an X article right now. Not what sounds interesting in the abstract. The thing where the vault has already done most of the thinking, the energy is current, and multiple threads are waiting to be woven together.

**Usage:** `/xarticle` (full scan) or `/xarticle [topic]` (evaluate a specific topic's readiness)

## What Makes This Different

This is NOT:

- [[Prompt - Ideas|/ideas]] (generates ideas across all domains — XArticle finds which existing idea is ready to ship)
- [[Prompt - Learned|/learned]] (writes from a single recent insight — XArticle finds the topic with the deepest vault support)
- [[Prompt - Map|/map]] (shows vault structure — XArticle uses structure as a signal for article readiness)
- [[Prompt - Emerge|/emerge]] (surfaces implicit ideas — XArticle scores explicit ideas on publishability)

This IS: **Finding the intersection of graph density, current energy, and synthesis potential to identify the one topic you should write about next.** The vault has already been thinking about this topic. The article is partially written across dozens of notes. The job is to find it and pull it together.

## Phase 1: Topic Discovery

### Step 1: Structural Scan

```bash
obsidian tags counts sort=count format=json | jq '.[0:20]'  # Top 20 themes with counts
obsidian orphans                                             # Forgotten notes that may hold buried material
obsidian deadends                                            # Isolated thinking that never connected
```

### Step 2: Recent Energy

Read the past 14 days of daily notes to find what's actively alive:

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # for each of the past 13 days
```

Extract:

- Topics mentioned 3+ times in 14 days (repetition = energy)
- Ideas that evolved or shifted during this period (movement = readiness)
- Things described with conviction, frustration, or excitement (emotional charge = writing fuel)
- Conversations or external inputs that triggered new thinking (external validation = audience signal)

### Step 3: Context File Priorities

```bash
obsidian read file="<Company-Context>"
obsidian read file="<Project-Context>"
obsidian read file="Personal Workflow Context"
```

Extract topics that are both strategically important AND have recent energy. Strategic importance without energy produces lifeless writing. Energy without strategic alignment produces content that doesn't compound.

### Step 4: Graph Density Scoring

For each candidate topic (aim for 8-12 candidates from Steps 2-3):

```bash
obsidian search:context query="<candidate topic>" format=json                    # With matching lines
obsidian backlinks file="<most relevant note for this topic>" counts format=json  # Ranked connections
obsidian links file="<most relevant note for this topic>" format=json
obsidian wordcount file="<most relevant note for this topic>"                    # Material density in words
```

Score each candidate on:

- **Note count**: How many notes touch this topic? (minimum 5 for a substantive article)
- **Backlink depth**: How many hops deep does the network go? (1 hop = shallow, 3+ hops = deep)
- **Cross-domain reach**: Does this topic appear in multiple context files or tag clusters? (single-domain topics make narrow articles)
- **Unresolved links**: Are there `[[references]]` to things never written? (gaps signal the topic is still growing, which is good for a "here's what I'm figuring out" article but bad for a "here's the answer" article)

### Step 5: Prior Article Check

```bash
obsidian search query="xarticle" path="Daily Notes"
obsidian search query="article" path="Daily Notes"
obsidian search query="published" path="Daily Notes"
obsidian search:context query="wrote about"
```

Check what's been written before. Don't suggest topics that were recently published unless the vault shows significant new thinking since then.

## Phase 2: Candidate Scoring

**If `/xarticle [topic]` was called with a specific topic:** Skip Phase 1 discovery. Run Phase 2 scoring on only that topic, then go directly to Phase 3.

For each candidate, compute three scores:

### Graph Density (1-10)

How much material exists in the vault?

| Score | Meaning |
| --- | --- |
| 1-3 | Sparse: a few mentions, no dedicated notes |
| 4-6 | Moderate: several notes, some connections |
| 7-8 | Dense: many notes, deep backlink chains, cross-domain |
| 9-10 | Saturated: the vault has been obsessing over this |

### Current Energy (1-10)

How alive is this topic right now?

| Score | Meaning |
| --- | --- |
| 1-3 | Cold: hasn't appeared in daily notes for 2+ weeks |
| 4-6 | Warm: occasional mentions, stable thinking |
| 7-8 | Hot: appearing frequently, thinking is evolving |
| 9-10 | On fire: dominant theme, new insights arriving daily |

### Synthesis Potential (1-10)

Can multiple threads be woven into a single coherent article?

| Score | Meaning |
| --- | --- |
| 1-3 | Fragmented: related notes but no unifying thesis |
| 4-6 | Emerging: a thesis is forming but gaps remain |
| 7-8 | Ready: clear thesis, supporting evidence, counterarguments available |
| 9-10 | Overdue: the article is essentially written across the vault, just needs assembly |

### Composite Score

`(Graph Density x 0.3) + (Current Energy x 0.3) + (Synthesis Potential x 0.4)`

Synthesis Potential is weighted highest because a dense, energetic topic that can't be synthesized produces frustrated writing sessions. A topic that synthesizes cleanly produces articles that feel inevitable.

### Output: The Ranked List

For each candidate (ranked by composite score):

**#N: [Topic Name]** — Composite: X.X (Density: N, Energy: N, Synthesis: N)

**Draft thesis**: One sentence that captures what the article would argue.

**Vault evidence**: 2-3 specific notes or daily entries that contain the strongest material.

**What's missing**: What the vault doesn't yet have that the article would need. Is it fillable from your own thinking, or does it require external research?

**Audience signal**: Who would care about this and why? Any evidence from conversations, messages, or reactions that suggests demand?

## Phase 3: Deep Dive on the Top Pick

For the #1 ranked topic, build the article foundation:

### Material Extraction

Read every note the vault has on this topic:

```bash
obsidian search:context query="<topic>"
obsidian read file="<each relevant note>"
obsidian backlinks file="<central note>"  # follow 3 hops deep
```

Extract and organize:

- **Core argument**: What is the vault's strongest version of this idea?
- **Supporting evidence**: Anecdotes, data, examples, analogies from vault material
- **Counterarguments**: Places where the vault itself pushes back on this idea (from [[Prompt - Contradict|/contradict]] runs or daily note doubts)
- **Evolution**: How has thinking on this changed? The before/after is often the most compelling angle (see [[Prompt - Trace|/trace]])
- **Surprising connections**: Material from unrelated domains that strengthens the argument (see [[Prompt - Connect|/connect]])

### Structure Proposal

Propose 2-3 structural approaches for the article:

**Structure A: The Argument** — Thesis → evidence → counterargument → resolution → implication

**Structure B: The Journey** — What I used to think → what changed → what I think now → why it matters

**Structure C: The Framework** — Problem everyone faces → why common solutions fail → the model that works → how to apply it

For each structure, map specific vault material to each section. Show which notes feed which parts.

### The Hook

Draft 3 opening lines. The hook must pass this test: would someone scrolling X stop and read the next line? Draw from:

- A counterintuitive claim the vault supports
- A specific moment or anecdote from daily notes
- A question the vault keeps returning to

### Estimated Effort

- How much of the article can be assembled from existing vault material? (percentage)
- What new thinking or writing is needed?
- Estimated time from "start writing" to "ready to publish"

## Temporal Tracking

Check for previous runs:

```bash
obsidian search query="/xarticle" path="Daily Notes"
obsidian search query="article candidates" path="Daily Notes"
```

If prior runs found:

- Which topics were previously ranked highly? Were they written?
- If written: did the article perform well? Update the scoring model.
- If not written: why not? Has the topic's score changed? Rising scores on unwritten topics indicate growing urgency. Falling scores indicate the window may be closing.
- Remove topics that were published from the candidate list.

## Anti-Patterns

**1. The Evergreen Trap**
Topics that are always somewhat relevant but never urgently ready. They score 5-6 on everything forever. These make okay articles but never great ones. Flag them and suggest waiting for a spike in energy or a new angle.

**2. The Recency Bias**
Whatever happened yesterday feels like the most important thing to write about. Check: does this topic have graph density, or just energy? Energy alone produces reactive content that doesn't age well.

**3. The Expertise Performance**
Topics chosen to demonstrate knowledge rather than to share genuine insight. The vault reveals what you're actually wrestling with. Write about that, not about what you already know cold.

**4. The Scope Creep**
Topics where the vault material supports a book, not an article. If graph density is 9+ but synthesis potential is low, the topic may be too broad. Suggest a narrower slice that can be synthesized cleanly.

**5. The Rehash**
Topics already published that haven't evolved enough to warrant a new article. Check the temporal tracking. "I wrote about this 6 months ago and my thinking hasn't changed" is not an article — it's a repost.

**6. The External-Only Topic**
Topics where the vault has opinions but no original thinking or experience. These produce generic commentary. The best X articles come from topics where the vault holds material nobody else has.

## Output Guidelines

- The #1 pick should feel like a relief: "Yes, that's the one." If it doesn't, the scoring is off — revisit.
- Draft thesis statements should be specific and arguable. "Here's how I think about X" is not a thesis. "X is wrong because Y, and here's what to do instead" is.
- The vault material map should make starting the article feel easy, not overwhelming. If the material is abundant, curate ruthlessly.
- Include the runner-up. Sometimes the #2 pick is a better fit for the writer's current mood or available time.
- Be honest about gaps. If the #1 topic needs significant new thinking, say so. An article built entirely from existing vault material ships in hours. One that needs new research ships in weeks.

---

## Related Commands

- [[Prompt - Ideas|/ideas]] — Generates new ideas across all domains from vault patterns
- [[Prompt - Learned|/learned]] — Turns a single recent learning into a polished post at multiple depths
- [[Prompt - Map|/map]] — Topological view of the vault showing clusters, themes, and structural gaps
