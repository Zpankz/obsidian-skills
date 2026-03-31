---
title: "Prompt - Drift"
created: 2026-03-06
description: "Prompt - Drift"
tags:
  - "vault-command"
related:
  - "[[Prompt - Contradict]]"
  - "[[Prompt - 7plan]]"
  - "[[Prompt - Trace]]"
---
## Drift — What Am I Avoiding?

Compare stated intentions against actual behavior over the past 30-60 days. Surface gaps between what you say matters and where time and energy actually go. Find what's being avoided.

**Usage:**`/drift`

---

## Step 1: Gather Stated Intentions

Read context files for stated priorities, goals, and commitments:

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

Extract:

- Stated priorities and goals
- Commitments made (to self and others)
- Things marked as important or urgent
- Open questions flagged for investigation
- Experiments proposed but not yet run
- Projects in "current" or "active" status

Also check daily notes for stated intentions:

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 30-60 days
```

Look for:

- "I need to..." / "I should..." / "I want to..." statements
- Carry-forward items from reflections
- Things mentioned as tomorrow's priority
- Recurring items that keep appearing

## Step 2: Gather Actual Behavior

### Calendar Analysis

Use Google Calendar to pull the past 30 days:

- Where did time actually go? (meeting types, projects, people)
- How much time was protected for deep work vs. consumed by meetings?
- Which projects got calendar time? Which got none?

### Tasks

Pull all tasks:

- What's overdue and by how long?
- What keeps getting pushed?
- What was completed vs. what sits?

### Daily Note Patterns

Across the past 30 days of daily notes:

- What topics come up repeatedly?
- What topics appear once and vanish?
- What gets energy (long writing, exclamation marks, ideas flowing)?
- What gets avoidance (mentioned briefly, no follow-through, "I should...")?

### Vault Activity

```bash
obsidian search query="<stated priority A>" path="Daily Notes" format=json  # How often does this appear?
obsidian search query="<stated priority B>" path="Daily Notes" format=json
obsidian backlinks file="<priority project note>" counts format=json  # Is anything linking TO this?
```

For each stated priority, measure how much actual vault activity it generated. Use `format=json | jq length` to count mentions quantitatively.

### Vault Tasks

```bash
obsidian tasks todo verbose format=json  # All open tasks — which priorities have tasks? Which don't?
```

Cross-reference: stated priorities with zero open tasks may signal systemic avoidance.

## Step 3: Message Review

Review recent messages for commitment language: "I'll", "I'm going to", "let me", "will you", "did you", "following up", "I promised", "I owe you". This surfaces commitments without wading through casual messages.

Look for:

- Commitments made to others that haven't been fulfilled
- Conversations about projects that got no follow-through
- People you said you'd get back to

## Step 4: The Drift Report

### Alignment Score

For each stated priority, rate alignment between intention and action (1-10):

| Priority | Stated Importance | Actual Time/Energy | Alignment | Drift |
| --- | --- | --- | --- | --- |
| ... | High | Low | 3/10 | Significant |

### What's Getting Attention It Wasn't Supposed To

Things consuming time that aren't in any priority list. Where is energy leaking?

### What's Being Avoided

The uncomfortable list. Things that are clearly important (stated in context files, mentioned repeatedly) but consistently get no action. For each:

- **What**: The thing being avoided
- **Evidence**: How many times mentioned vs. how much action taken
- **Possible why**: What might be driving the avoidance (fear, unclear next step, not actually important, too big, requires confrontation)
- **The cost**: What's the cost of continued avoidance?

#### Avoidance Decision Tree

For each avoided item, classify:

### Commitments to Others

Promises made that haven't been kept. Overdue follow-ups. People waiting.

### Recurring Push Pattern

Tasks or intentions that appear, get pushed, appear again, get pushed again. The loop. For each:

- How many times has this cycled?
- What breaks the loop?

### The Honest Assessment

A direct, compassionate summary of where the drift is. Not judgmental. Just clear. "Here's what you said mattered. Here's what you actually did. Here's where they don't match."

For each significant drift:

- **Drop it**: If it keeps getting avoided, maybe it's not actually a priority. Remove it.
- **Do it now**: If it genuinely matters, schedule it in the next 48 hours.
- **Delegate it**: If it matters but you won't do it, who else can?
- **Reframe it**: If the next step is unclear, define one concrete action.

---

## Output Format

**DRIFT REPORT -- \[Date range\]**

\[Alignment table\]

\[What's getting unplanned attention\]

\[What's being avoided, with decision tree classification\]

\[Commitments to others\]

\[Recurring push patterns\]

\[Honest assessment\]

\[Recommended corrections\]

---

## Output Guidelines

- Be honest but not harsh. This is a mirror, not a critic.
- Always cite specific dates, notes, and data. Vague drift reports are useless.
- The most valuable insight is often the simplest: "You said X matters. You haven't touched it in 3 weeks."
- Don't confuse busyness with avoidance. Some things legitimately got deprioritized. The real drift is things that STILL matter but aren't getting attention.
- Distinguish between "dropped and should stay dropped" vs. "dropped and it's costing you."

---

## Related Commands

- [[Prompt - Contradict|/contradict]] — Finds incompatible beliefs held simultaneously in the vault
- [[Prompt - 7plan|/7plan]] — Reshapes the next 7 days around intellectual threads alive in the vault
- [[Prompt - Trace|/trace]] — Traces how a specific idea or belief has evolved across the vault over time