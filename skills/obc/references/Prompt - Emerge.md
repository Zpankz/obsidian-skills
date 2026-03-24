---
title: "Prompt - Emerge"
created: 2026-03-06
description: "Prompt - Emerge"
tags:
  - "vault-command"
related:
  - "[[Prompt - Compound]]"
  - "[[Prompt - Connect]]"
  - "[[Prompt - Guests]]"
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Map]]"
  - "[[Prompt - Synthesize]]"
  - "[[Prompt - Graph]]"
---
## Emerge — Surface Ideas the Vault Implies but Never States

Find ideas that are implied by the vault's contents but have never been explicitly articulated. These are conclusions the vault's own evidence points toward, connections its structure suggests, patterns its behavior reveals, but that have never been written down. The vault knows things its author hasn't thought yet.

**Usage:**`/emerge` (general) or `/emerge [domain]` (focused on a specific area)

---

## What Counts as an Emergence

An emergence is NOT:

- A connection between two existing ideas (that's [[Prompt - Connect|/connect]])
- A contradiction between beliefs (that's [[Prompt - Contradict|/contradict]])
- An evolution of existing thinking (that's [[Prompt - Trace|/trace]])
- A restatement of something already in the vault

An emergence IS:

- A conclusion that follows from premises scattered across the vault, where the conclusion itself was never drawn
- A pattern that recurs across multiple domains but has never been named
- A belief that behavior reveals but that has never been articulated
- A direction that multiple threads point toward but that has never been identified as a destination

The test: if the emergence is surfaced and your reaction is "oh, I think that's right but I've never said it," it's a genuine emergence. If the reaction is "I already know that," it's not.

---

## Step 1: Structural Detection

Look for ideas the vault's structure implies through undrawn connections.

```bash
obsidian orphans                                        # Isolated notes that might connect to each other
obsidian deadends                                       # Notes that stopped developing
obsidian unresolved counts verbose format=json          # Referenced but never created, ranked by frequency
obsidian tags counts sort=count format=json | jq '.[0:20]'  # Theme distribution, machine-readable
obsidian random:read                                    # Read a random note — serendipity engine for emergence
```

### What to Look For

```bash
obsidian backlinks file="<orphan note A>" counts format=json  # What connects to this orphan?
obsidian backlinks file="<orphan note B>" counts format=json
obsidian links file="<deadend cluster note>" format=json
obsidian wordcount file="<orphan note A>"                     # Is this orphan thin or deeply developed?
```

**Confidence calibration**: Structural detection is the most reliable method because it's grounded in the vault's actual topology, not interpretation.

---

## Step 2: Thematic Detection

Find unnamed patterns that recur across 3+ domains.

### Read Across Domains

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

### Search for Recurring Patterns

```bash
obsidian search:context query="<pattern observed in domain A>" format=json  # With matching lines
obsidian search query="<pattern observed in domain A>" path="Daily Notes" format=json
```

### What to Look For

The same structural pattern appearing in different domains under different names. Examples:

- The same problem-solving approach applied everywhere but never identified as "the way I think"
- The same tension appearing in work, personal life, and creative projects but never named
- The same value driving decisions across domains without being stated as a core value

A thematic emergence must appear in at least 3 separate domains to qualify. Two is a coincidence. Three is a pattern.

---

## Step 3: Logical Detection

Find premises from different notes whose conclusions are never drawn.

### Read Recent Daily Notes

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 14-21 days
```

### Search for Belief Clusters

```bash
obsidian search:context query="I think"
obsidian search:context query="I believe"
obsidian search:context query="the problem is"
obsidian search:context query="what works"
```

### What to Look For

- Premise A appears in Note 1. Premise B appears in Note 2. A + B logically implies C. But C is never stated anywhere.
- A principle stated in one domain that, if applied to another domain, would produce a conclusion never drawn.
- A pattern of observations that, taken together, point at a theory that's never been articulated.

Be rigorous about the logic. The conclusion must actually follow from the premises, not merely be compatible with them.

**Confidence calibration**: Logical detection is moderate reliability. The conclusions are valid only if the premises are correctly interpreted, and premises in a personal vault are often more nuanced than they appear.

---

## Step 4: Behavioral Detection

Find recurring decisions that imply unarticulated beliefs.

### Analyze Patterns in Daily Notes

```bash
obsidian search query="decided" path="Daily Notes"
obsidian search query="chose" path="Daily Notes"
obsidian search query="going to" path="Daily Notes"
obsidian search query="not going to" path="Daily Notes"
obsidian search query="cancelled" path="Daily Notes"
obsidian search query="skipped" path="Daily Notes"
```

### What to Look For

- Decisions that consistently favor one option type over another (e.g., always choosing depth over breadth, always choosing people over systems)
- Things consistently avoided that reveal an unstated belief about risk or value
- Patterns of what gets energy vs. what gets procrastination
- Recurring "rules" that are followed but never written down

The gap between a behavioral pattern and an articulated belief is the emergence. If someone consistently chooses X over Y but has never written "I believe X is more important than Y," that belief is emergent.

**Confidence calibration**: Behavioral detection is high reliability. Actions are harder to fake than words. But beware of over-interpreting single decisions. The pattern must be consistent across 3+ instances.

---

## Step 5: Convergence Detection

Find multiple threads that, projected forward, point at the same unnamed destination.

### Read Forward-Looking Material

```bash
obsidian search:context query="want to"
obsidian search:context query="building toward"
obsidian search:context query="future"
obsidian search:context query="goal"
obsidian search:context query="vision"
obsidian search query="next" path="Daily Notes"
```

### What to Look For

- Multiple projects or priorities that, if completed, would create a specific outcome that's never been named as the goal
- Separate aspirations that point at a common destination
- Incremental decisions that, traced forward, converge on a life or work structure that hasn't been articulated

Convergence detection is the most speculative method. Use it sparingly and mark findings with lower confidence.

**Confidence calibration**: Convergence detection is the least reliable method. It requires projecting forward, which always involves interpretation. Only report convergences where 3+ independent threads clearly point the same direction.

---

## Step 6: Verification and Output

### Fabrication Check

For each potential emergence, ask: "Is this something the vault's evidence points at, or am I projecting a narrative?"

Run the check:

```bash
obsidian search query="<the emergence stated plainly>"  # if this returns results, it's NOT an emergence
```

If the emergence is already stated somewhere in the vault, it's not emergent. Discard it.

### Verification Frame

True emergences feel like recognition, not surprise. If a finding feels clever or counterintuitive, it's probably the agent being creative rather than the vault speaking. The best emergences are obvious in retrospect.

### Confidence Levels

- **High** (5+ data points across 2+ detection methods): Strong evidence from multiple angles.
- **Medium** (3-4 data points from 1-2 methods): Suggestive but not definitive.
- **Low** (1-2 data points from 1 method): Speculative. Worth naming but holding loosely.

### Detection Method Reliability

Rank findings by method reliability: Structural > Behavioral > Thematic > Logical > Convergence

### For Each Emergence

**Emergence \[#\]: \[Title\]**

**The idea:** \[State the emergent idea plainly, in one sentence\]

**Detection method:** \[Which method(s) found it\]

**Evidence:**

- \[Specific note, date, quote\] supports this because \[why\]
- \[Another specific note\] supports this because \[why\]
- \[Behavioral pattern / structural feature\] supports this because \[why\]

**Why it's emergent:** \[Why this hasn't been stated despite the evidence pointing to it\]

**Confidence:** High / Medium / Low  
**Data points:** \[number\]

**What to do with it:** Does this emergence want to be:

- A new belief to articulate in a context file?
- A question to investigate further?
- A name for something already being lived?
- Left alone (some things are better felt than formalized)?

### Synthesis

**Emergences found:** \[number\]  
**By method:** Structural: X, Thematic: Y, Logical: Z, Behavioral: W, Convergence: V  
**By confidence:** High: X, Medium: Y, Low: Z

**The strongest emergence:** The one with the most evidence from the most methods.

**Meta-emergence:** Is there a pattern in the emergences themselves? Do they collectively point at something even larger that's unnamed?

---

## Anti-Patterns

**2\. The Forced Emergence**  
Manufacturing emergences when the vault doesn't support them. If the vault is well-articulated and nothing is truly emergent, that's the finding. Don't fabricate.

**3\. The Obvious Emergence**  
Stating things the vault already says, just in slightly different words. If it's already in a context file, it's not emergent.

**5\. The Over-Interpreter**  
Reading too much into single data points. One note about a topic is not a pattern. Require 3+ data points minimum.

**6\. The Projection Machine**  
Imposing the agent's own frameworks onto the vault's data. The emergence should come from the vault, not from Claude's worldview.

**7\. The Creativity Trap**  
Generating novel, clever ideas and attributing them to the vault. Emergences are discovered, not invented. They should feel inevitable given the evidence, not surprising.

---

## Output Format

**EMERGE REPORT**  
**Scope:** \[General / Domain-focused\]  
**Detection methods run:** \[list\]  
**Potential emergences found:** \[number\]  
**Survived fabrication check:** \[number\]

\[Emergences, ordered by confidence\]

\[Synthesis\]

\[The strongest emergence\]

\[Meta-emergence, if any\]

---

## Output Guidelines

- Every emergence must trace back to specific vault evidence. No evidence, no emergence.
- The best emergences make you say "I've never said that, but yes, that's what I think."
- Prefer fewer, stronger emergences over many weak ones. Three solid findings are better than ten speculative ones.
- The fabrication check is mandatory. If the emergence is already in the vault, it's not emergent.
- This command should feel like the vault thinking on your behalf, surfacing what's already there but unnamed.

---

## Related Commands

- [[Prompt - Connect|/connect]] — Finds unexpected bridges between two separate domains in the vault
- [[Prompt - Ideas|/ideas]] — Generates a comprehensive list of ideas across multiple domains from vault patterns
- [[Prompt - Map|/map]] — Analyzes vault topology, clusters, gaps, and the shape of thinking across the vault