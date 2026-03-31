---
title: "Prompt - Trace"
created: 2026-03-06
description: "Prompt - Trace"
tags:
  - "vault-command"
related:
  - "[[Prompt - Contradict]]"
  - "[[Prompt - Ghost]]"
  - "[[Prompt - Compound]]"
  - "[[Prompt - Drift]]"
---
## Trace — Idea Evolution Over Time

Trace how a specific idea, concept, or belief has evolved across the vault over time. Shows the full arc of thinking development.

**Usage:**`/trace [topic]` -- e.g., `/trace software as fashion` or `/trace context management`

---

## Step 1: Synonym Discovery

Before searching, build a vocabulary map for this topic. Ideas often evolve under different vocabulary. Check aliases for alternate note names:

```bash
obsidian aliases file="<topic note if it exists>"  # Discover alternate names
```

Then search using the full vocabulary with structured output:

```bash
obsidian search query="<topic>" format=json                    # All mentions
obsidian search:context query="<topic>" format=json            # With matching lines for timeline building
obsidian search query="<synonym 1>" format=json
obsidian search query="<synonym 2>" format=json
obsidian search query="<related concept>" format=json
```

Also search daily notes specifically — this is the primary temporal data source:

```bash
obsidian search:context query="<topic>" path="Daily Notes" format=json  # With lines, for timeline extraction
obsidian search:context query="<synonym 1>" path="Daily Notes" format=json
```

And check context files, essays, and any Maps of Content:

```bash
obsidian search query="<topic>" path="Essays" format=json
obsidian read file="<any context file likely to contain this topic>"
obsidian property:read name="confidence" file="<topic note>"   # Check confidence marker if stored as property
```

## Step 1.5: Implicit Pattern Detection

Some ideas don't have explicit mentions but emerge through patterns across daily notes. Use broader contextual searches:

```bash
obsidian search:context query="<broader theme>"
obsidian tags counts sort=count  # check if related tags reveal hidden mentions
```

Look for:

- Daily notes that discuss the same problem this idea addresses, without naming it
- Emotional reactions to situations that this idea would explain
- Decisions made that reflect this thinking, even if the thinking wasn't articulated

Implicit mentions are often the earliest evidence of an idea forming.

## Step 2: Follow the Graph

For each note that mentions the topic:

```bash
obsidian backlinks file="<note>" counts format=json  # what else connects to this, ranked
obsidian links file="<note>" format=json             # what does this link to
```

Follow backlinks 2-3 hops out from the most significant mentions. The goal is to find:

## Step 3: Build the Timeline

Organize findings chronologically. For each significant mention or shift:

- **Date**: When it appeared
- **Context**: What was happening at the time (from daily notes, calendar if helpful)
- **The thinking**: What was believed or proposed at that point
- **Confidence level**: If marked with `[solid]`, `[evolving]`, `[hypothesis]`, `[questioning]`, note it
- **What triggered the shift**: Conversation, experience, reading, or just time

### Temporal Weighting

Recent mentions (past 3 months) suggest active evolution. The idea is alive and changing. Focus the narrative here. Older mentions establish origin but the story is in the active period.

If there's a long gap between mentions (e.g., nothing for 6 months, then a burst), that gap itself is interesting. What happened? Did the idea go dormant, or did it evolve underground?

## Step 4: Identify the Arc

Synthesize the timeline into a narrative:

### First Appearance

When and where this idea first showed up. What form was it in? Was it a question, a hunch, a reaction to something?

### Key Inflection Points

Moments where the thinking shifted meaningfully. What caused each shift?

### Current Position

Where the thinking stands now. What confidence level? What's resolved vs. still open?

### Confidence Marker Evolution

If the topic appears in a context file with a confidence marker, show how that marker changed over time. Was it `[hypothesis]` and now `[solid]`? When did the shift happen? Was there a specific event that triggered the upgrade? Was it earned through experience, or did it drift to `[solid]` without being tested?

### The Evolution Pattern

What kind of evolution was this? Options:

- **Linear deepening**: Same direction, just more refined over time
- **Pivots**: Fundamental changes in direction
- **Convergence**: Separate ideas that merged into one
- **Divergence**: One idea that split into multiple threads
- **Circular**: Keeps coming back to the same question without resolution

### Unresolved Tensions

Contradictions or open questions that remain. Things written at different times that don't agree with each other.

### What's Next

Based on the trajectory, where is this idea likely heading? What would resolve the open tensions?

---

## Output Format

**TRACE: \[Topic\]**  
**First appeared:** \[date\]  
**Time span:** \[X weeks/months\]  
**Mentions found:** \[number of notes\]  
**Velocity:** \[Accelerating / Steady / Dormant\]

\[Timeline with key moments\]

\[Arc narrative\]

\[Confidence marker evolution, if applicable\]

\[Unresolved tensions\]

\[What's next\]

---

## Output Guidelines

- Be specific: cite exact notes and dates
- Show the actual words used at different times so the evolution is visible
- Don't flatten the complexity. If the thinking contradicts itself across time, show that.
- The value is in seeing the shape of your own thinking from the outside. Make that shape visible.

---

## Related Commands

- [[Prompt - Ghost|/ghost]] — Answers a question as the vault's author, drawing only on vault evidence
- [[Prompt - Compound|/compound]] — Answers the same question across three time periods to show context compounding
- [[Prompt - Drift|/drift]] — Compares stated intentions against actual behavior to surface avoidance patterns