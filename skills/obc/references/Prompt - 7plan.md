---
title: "Prompt - 7plan"
created: 2026-03-06
description: "Prompt - 7plan"
tags:
  - "vault-command"
related:
  - "[[Prompt - Today]]"
  - "[[Prompt - Schedule]]"
  - "[[Prompt - Drift]]"
---
## 7plan — Reshape the Next 7 Days Around What's Alive in the Vault

Build a deep understanding of the intellectual threads, rabbit holes, and latent patterns in your thinking, then reshape the next 7 days so the calendar serves those threads. Not scoring meetings against a static priority list, but understanding what's close to breaking through, what's been circling, what deserves dedicated time, and then making the calendar protect that.

**Usage:**`/7plan`

---

## Phase 1: Understand the Thinking (Vault-First)

Before touching the calendar, build a deep understanding of what you are actually thinking about, investigating, and trying to break through on. The calendar serves the thinking, not the other way around.

### Step 1: Structural Inventory

```bash
obsidian vault                                        # Quick size/shape overview
obsidian tags counts sort=count format=json | jq '.[0:20]'  # Top 20 themes, machine-readable
obsidian orphans total                                # Count orphans first
obsidian orphans                                      # Then list them
obsidian deadends                                     # Notes with no outgoing links
obsidian unresolved counts verbose format=json        # Broken [[links]] ranked by reference count
```

What themes are most active? What's been created but not connected? What's referenced but never developed? Use `format=json` output to compare tag counts quantitatively.

### Step 2: Read Daily Notes (past 14 days)

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # for each day in the past 14 days
```

Read each day. Look for:

- **Energy patterns**: What produced flow states vs. what drained
- **Recurring questions and investigations**: Ideas that keep surfacing
- **Stated intentions**: "I want to explore...", "I need to think about...", "I should write..."
- **Threads started but not continued**: Something sparked, then silence
- **Decisions made**: What was chosen, what was rejected, what does that reveal?

**Sparse data handling:** If daily notes are sparse for recent days, expand to 21 days.

### Step 3: Context Files

```bash
obsidian read file="<Company-Context>"
obsidian read file="<Project-Context>"
obsidian read file="Personal Workflow Context"
obsidian read file="<Health-Context>"
obsidian read file="<Family-Context>"
```

Extract:

- Stated priorities AND open questions
- Items marked with confidence levels (`[solid]`, `[evolving]`, `[hypothesis]`, `[questioning]`)
- Anything marked `[evolving]` or `[hypothesis]` is a candidate for dedicated thinking time

### Step 4: Deep Vault Exploration (the core)

This is what makes [[Prompt - 7plan|/7plan]] different. For each active thread identified from daily notes and tags:

```bash
obsidian search:context query="<thread>" format=json        # Where this thread appears, with matching lines
obsidian backlinks file="<related note>" counts format=json  # Ranked connections
obsidian links file="<related note>" format=json             # Outgoing links
obsidian wordcount file="<related note>"                     # How much thinking has accumulated here
```

Follow backlinks 2-3 hops. Build a map of:

- **Active investigations**: Rabbit holes currently being explored. What's the current state? What would move them forward?
- **Near-breakthrough ideas**: Threads that have accumulated enough thinking to crystallize into something (a piece of writing, a creative angle, an essay, a decision). These need protected time NOW.
- **Stalled threads**: Things that were energizing but stopped. Why? Is the block a missing conversation, a missing piece of research, or just lack of time?
- **Convergence points**: Separate threads that are pointing at the same conclusion. These are high-leverage: one session could connect multiple threads.
- **Latent patterns**: Recurring themes across domains that haven't been named or developed. These deserve dedicated thinking time.

### Step 5: Behavioral Patterns

```bash
obsidian search query="decided" path="Daily Notes"
obsidian search query="want to" path="Daily Notes"
obsidian search query="need to write" path="Daily Notes"
obsidian search query="cancelled" path="Daily Notes"
obsidian search query="skipped" path="Daily Notes"
```

What does behavior reveal about what actually matters vs. what just sounds important?

### Output of Phase 1: The Intellectual Map

Before touching the calendar, present:

**Top 3-5 Active Threads**  
For each: current state, what would advance it, how much time it needs, what type of work (writing, research, conversation, building)

**Near-Breakthrough Candidates**  
Threads that have accumulated enough thinking to crystallize. These deserve protected blocks this week.

**Stalled Threads Worth Reviving**  
If time opens up, these are worth restarting. Include what stalled them.

**The Meta-Pattern**  
What is all of this thinking converging toward? What's the unnamed destination?

---

## Phase 2: Calendar Reality

### Step 6: Google Calendar + Tasks + Email

**Calendar**: Next 7 days, detailed.

- Get all events for the next 7 days with attendees, descriptions, recurring status

**Tasks**: Pull all tasks from Google Tasks AND the vault:

- Overdue (critical)
- Due in the next 7 days
- Floating (no due date)

```bash
obsidian tasks todo verbose format=json | jq '.[] | {file: .path, task: .text, line: .line}'
```

Vault tasks often contain commitments that never made it to Google Tasks. Cross-reference both sources.

**Email**: Last 3 days of email for time-sensitive threads:

- Look for action items, requests, deadlines

---

## Phase 3: Triage — Calendar Serves the Thinking

Evaluate every calendar event against the intellectual map from Phase 1. The question isn't "is this meeting important in the abstract?" but "does this meeting advance the threads that are alive right now?"

### For each event, evaluate:

1. **Does this serve an active thread?** If a meeting connects to a near-breakthrough investigation, it stays. If it's disconnected from everything alive in the vault, it's a candidate for elimination.
2. **Are you the right person?** Creative direction, deep thinking = you. Operations, logistics, follow-ups = delegate.
3. **Could this be async?** If the meeting's purpose can be served by a document, email, or message thread, draft the replacement.
4. **Does this protect or consume creative time?** Morning meetings consume deep work windows. Can they move?
5. **Hard constraint check**: Protect family time and 2-3hr+ focus blocks.

### Triage categories

- **KEEP**: Directly serves an active thread or is a hard commitment
- **COMPRESS**: Shorten (1hr to 30min, 30min to 15min)
- **MOVE**: Reschedule to protect a deep work block or batch with similar meetings
- **DELEGATE**: Someone else can handle this
- **ASYNC**: Replace with a document, email, or message (draft the replacement)
- **CANCEL**: Low alignment, no clear outcome, won't be missed

### Delegation map

Create a delegation map of people and their domains so you know who to route tasks to.

---

## Phase 4: The 7-Day Plan

### For each day:

**Day theme**: What this day should serve, tied to an active thread from Phase 1.

**Protected block**: 2-3hr minimum for a specific thread/investigation. Name the thread and describe what to work on during the block.

**Events table**:

| Time | Event | Status | Action | Reasoning |
| --- | --- | --- | --- | --- |
| ... | ... | KEEP/DELEGATE/CANCEL/etc. | ... | Tied to vault context |

**Delegation briefs**: For any DELEGATE items, write a brief complete enough for the delegate to act without follow-up questions. Include: what it is, what needs to happen, who to contact, what success looks like.

**Async artifacts**: For any ASYNC items, draft the replacement document/email/message.

### Week Summary

**Before/After**:

- Meeting hours: \[before\] -> \[after\]
- Deep work blocks: \[before\] -> \[after\]
- Time reclaimed: \[hours\]

**Thread allocation**: Which active threads get dedicated time this week, and when.

**Deferred threads**: Which threads don't have time this week. Be honest about what's not getting attention.

**The single most important creative session of the week**: Which block, which thread, what it should produce.

---

## Phase 5: Execution (After Approval)

**Wait for explicit approval before making any changes.**

Once approved, offer to:

- Cancel/compress/move events via Google Calendar
- Create deep work blocks tied to specific threads (with descriptions naming the thread)
- Draft delegation emails to specific people
- Draft async replacement artifacts

---

## Output Guidelines

- All output is text in the session. No dashboard, no HTML file.
- The intellectual map in Phase 1 is the foundation. If it's thin, the rest falls apart. Spend the time here.
- Every calendar decision in Phase 3 must reference the intellectual map. "This meeting doesn't connect to any active thread" or "This directly serves the near-breakthrough on X."
- Deep work blocks must name the specific thread and what to work on. No generic "focus time."
- Delegation briefs must be complete. Name the person, the task, and what success looks like.
- Be direct. This is a planning tool, not a report.

---

## Related Commands

- [[Prompt - Today|/today]] — Reviews calendar, tasks, and vault patterns to generate a daily plan with priorities
- [[Prompt - Schedule|/schedule]] — Context-aware scheduling that evaluates requests against current priorities
- [[Prompt - Drift|/drift]] — Compares stated intentions against actual behavior to surface avoidance patterns