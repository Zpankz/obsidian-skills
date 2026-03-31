---
title: "Prompt - Synthesize"
created: 2026-03-25
description: "Prompt - Synthesize"
tags:
  - "vault-command"
related:
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Connect]]"
  - "[[Prompt - Emerge]]"
  - "[[Prompt - Make]]"
  - "[[Prompt - XArticle]]"
---
## Synthesize -- Weave Vault Threads into Coherent Narratives

Bridges discovery and ideation -- takes output from /connect (unexpected bridges) and /ideas (raw candidates) and produces unified synthesis: narratives that weave multiple threads into coherent wholes.

**Usage:** `/synthesize` (full vault scan) or `/synthesize [topic]` (focused synthesis on a specific topic)

---

## What Makes This Different

This is NOT:

- [[Prompt - Ideas|/ideas]] (generates new ideas across domains -- Synthesize weaves existing threads together)
- [[Prompt - Connect|/connect]] (finds bridges between two domains -- Synthesize combines 3+ threads into a single narrative)
- [[Prompt - Make|/make]] (scores readiness to ship -- Synthesize produces the narrative itself, not a readiness score)
- [[Prompt - Emerge|/emerge]] (surfaces implicit ideas -- Synthesize works with explicit threads and combines them)

This IS: **Weaving multiple vault threads into a single coherent narrative or framework.** The vault has been thinking about many things separately. Some of those things belong together. The job is to find which threads converge and produce a synthesis that is more than the sum of its parts.

---

## Phase 1: Gather Threads

Start with structural analysis to find the most active threads in the vault.

```bash
obsidian vault                                                  # Quick overview stats
obsidian search:context query="<topic if provided>" format=json  # With matching lines
obsidian backlinks file="<hub note for topic>" counts format=json
obsidian tags counts sort=count format=json | jq '.[0:20]'      # Top 20 themes, machine-readable
obsidian recents                                                 # Recently modified notes — active threads
```

Identify the 5-8 most active threads in the vault. An "active thread" is a cluster of notes, backlinks, and daily note mentions that form a coherent line of thinking.

For each thread:

- **Name it.** What is this thread about, in one phrase?
- **Extract the core claim/insight.** What does this thread say, reduced to a single sentence?
- **Count its evidence.** How many notes, daily entries, and backlinks support it?
- **Assess its maturity.** Is this thread still forming, or has it stabilized into a position?

```bash
obsidian search:context query="<thread A keyword>" format=json   # Where this thread appears, with matching lines
obsidian backlinks file="<thread A hub note>" counts format=json  # Ranked connections
obsidian wordcount file="<thread A hub note>"                    # Thinking density
obsidian outline file="<thread A hub note>" format=json          # Internal structure
```

Repeat for each thread.

If `/synthesize [topic]` was called with a specific topic, filter threads to those relevant to the topic. But don't filter too aggressively -- the best syntheses often pull in threads that seem tangential until you see the connection.

---

## Phase 2: Find Convergences

For each pair of threads, ask three questions:

1. **Do they reinforce each other?** Does Thread A's core claim strengthen Thread B's? If both point the same direction from different angles, they reinforce.
2. **Do they contradict each other?** Does Thread A's position conflict with Thread B's? Contradictions are valuable -- a synthesis that resolves a tension is more powerful than one that merely combines compatible ideas.
3. **Do they extend each other?** Does Thread A provide a missing piece for Thread B, or vice versa? Extensions create "Thread A is true, AND it implies Thread B in ways neither stated alone."

Build a convergence matrix:

| | Thread 1 | Thread 2 | Thread 3 | Thread 4 | Thread 5 |
|---|---|---|---|---|---|
| **Thread 1** | -- | reinforce | extend | none | contradict |
| **Thread 2** | | -- | none | extend | reinforce |
| ... | | | | | |

```bash
obsidian search:context query="<thread A keyword>" format=json   # search within thread B's notes
obsidian links file="<thread A hub>" format=json                 # do these threads share any links?
obsidian links file="<thread B hub>" format=json                 # compare — shared targets = convergence signal
```

Pairs with no relationship (none) are not candidates for synthesis. Pairs with relationships are raw material for Phase 3.

---

## Phase 3: Weave Narratives

From the convergence matrix, produce 2-3 synthesis narratives. Each narrative must combine 3 or more threads into a coherent whole.

For each synthesis narrative:

### Thesis

State the synthesis in one sentence. This should be a claim that could not exist from any single thread alone -- it requires the combination.

### Threads Woven

List the 3+ threads this synthesis combines. For each, explain what it contributes to the whole.

### Why They Belong Together

What is the underlying connection that makes these threads part of the same story? This is not "they're all about X" (that's a category, not a synthesis). It's "Thread A creates a condition that Thread B addresses, and Thread C explains why both matter."

### The New Insight

What emerges from the combination that wasn't visible in any thread alone? This is the synthesis's core value. If the combination doesn't produce something new, it's a summary, not a synthesis.

### Vault Evidence

```bash
obsidian read file="<key note for this synthesis>"
obsidian search:context query="<synthesis thesis keywords>" format=json
```

Cite specific notes, daily entries, and quotes that support the synthesis. Every claim traces back to vault material.

### Form Suggestion

What could this synthesis become? An essay, a framework, a decision, a project direction? Don't prescribe -- suggest 2-3 forms.

---

## Phase 4: Score & Rank

Score each synthesis narrative on three dimensions (1-5 each):

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **Novelty** | Restates what the vault already says | Combines known ideas in a new arrangement | Produces a genuinely new insight from the combination |
| **Evidence Depth** | Thin -- based on 2-3 vault data points | Moderate -- 5-8 data points across multiple notes | Deep -- 10+ data points across multiple domains and time periods |
| **Actionability** | Interesting but abstract | Suggests a direction or decision | Points to a specific action, project, or output |

**Total: /15**

Rank syntheses by total score. Present the strongest first.

---

## Temporal Tracking

Check for prior /synthesize runs:

```bash
obsidian search query="/synthesize" path="Daily Notes"
obsidian search query="synthesis" path="Daily Notes"
```

If prior runs found:

- Which syntheses were acted on? (Became essays, informed decisions, changed direction)
- Which were acknowledged but not acted on? (Still valid? Or overtaken by new thinking?)
- Which threads have gained new material since the last synthesis?

New material on previously synthesized threads may warrant an updated synthesis. Flag these.

---

## Anti-Patterns

**1. The Forced Connection**
Combining threads that don't naturally fit. If the convergence matrix shows "none" between threads, don't manufacture a synthesis. Three related threads make a better synthesis than five where two are shoehorned in.

**2. The Summary**
Restating what each thread says without producing something new from the combination. A synthesis must generate an insight that no single thread contains. If you could delete two threads and the narrative still works, it's a summary of the remaining thread.

**3. The Single-Thread**
A "synthesis" that is really just one idea dressed up with supporting details from other threads. The test: does removing any thread fundamentally change the narrative? If not, the removed thread wasn't actually part of the synthesis.

**4. The Abstraction Spiral**
Combining threads at such a high level of abstraction that the synthesis applies to everything and means nothing. "All your threads are about growth" is not a synthesis. Stay concrete. Name notes, cite quotes, reference specific ideas.

**5. The Quantity Play**
Producing 5-6 thin syntheses instead of 2-3 deep ones. Fewer, stronger syntheses are always better.

---

## Output Format

**SYNTHESIZE REPORT**
**Scope:** \[General / Topic-focused\]
**Threads identified:** \[number\]
**Convergence pairs found:** \[number with relationships\]
**Syntheses produced:** \[number\]
**New since last run:** \[number, or "First run"\]

---

\[Synthesis #1: Title\]
\[Thesis, threads, connection, new insight, evidence, form suggestion\]
\[Score: Novelty X | Evidence X | Actionability X | Total: X/15\]

\[Synthesis #2: Title\]
\[Same format\]

\[Synthesis #3: Title, if applicable\]
\[Same format\]

---

\[Temporal tracking results\]

---

## Output Guidelines

- Every synthesis must trace back to specific vault evidence. No evidence, no synthesis.
- The new insight is the most important section. If you can't articulate what the combination produces that the parts don't, the synthesis isn't real.
- Cite exact notes, dates, and quotes. The user should be able to verify every thread and every connection.
- Prefer 2-3 strong syntheses over many weak ones.
- This should feel like seeing your own thinking from a higher altitude -- familiar threads, but a new picture.

---

## Related Commands

- [[Prompt - Ideas|/ideas]] -- Generates a comprehensive list of ideas across multiple domains from vault patterns
- [[Prompt - Connect|/connect]] -- Finds unexpected bridges between two separate domains in the vault
- [[Prompt - Emerge|/emerge]] -- Surfaces ideas the vault implies but has never explicitly stated
- [[Prompt - Make|/make]] -- Scans the vault for ideas ready to become something the world sees
- [[Prompt - XArticle|/xarticle]] -- Finds which idea is most ready to become an X article by scoring graph density, energy, and synthesis potential