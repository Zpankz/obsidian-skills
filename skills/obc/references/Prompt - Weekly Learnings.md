---
title: "Prompt - Weekly Learnings"
created: 2026-03-06
description: "Prompt - Weekly Learnings"
tags:
  - "vault-command"
related:
  - "[[Prompt - Learned]]"
  - "[[Prompt - Close Day]]"
---
## Weekly Learnings — Writing Prep

Help figure out what to write about in a weekly team email. Surface patterns, insights, and candidate topics from the week. Output everything to terminal. Do NOT create any files.

---

## Step 1: Read Previous Weekly Learnings (Continuity)

Find and read the two most recent weekly learnings files:

```bash
obsidian search query="Weekly Learnings" format=json | jq -r '.[0:3] | .[].file'
obsidian read file="<most recent weekly learnings>"
```

Extract:

- What was written about last time (so we don't repeat without development)
- Threads that were opened but not resolved
- Things promised ("I'll write more about this soon")
- The tone and style (first person, reflective, connects specific events to broader ideas)

---

## Step 2: Read Daily Notes (Past 7 Days)

Use the obsidian CLI to read all daily notes from the past 7 days:

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # for each of the past 6 days
```

Extract:

- What was actually worked on this week (not what was planned, what happened)
- Conversations and meetings that shifted thinking
- Ideas that emerged (especially ones with energy behind them)
- Decisions made or direction changes
- Problems encountered and how they were handled
- People mentioned and what the interactions were about
- Frustrations, breakthroughs, and realizations
- Anything that was surprising

---

## Step 3: Load Context Files

Use the obsidian CLI to read these for current state and priorities:

```bash
obsidian read file="<Company-Context>"
obsidian read file="<Project-Context>"
obsidian read file="Personal Workflow Context"
```

Use these to understand which events from the week connect to bigger strategic questions. The weekly learnings work best when specific things that happened reveal something about the larger direction.

---

## Step 3.5: Trace Idea Evolution

Use the obsidian CLI to explore how this week's thinking connects across notes and to the broader vault:

```bash
obsidian backlinks file="<key notes referenced this week>" counts format=json  # Ranked connections
obsidian search:context query="<recurring theme from daily notes>" format=json
obsidian tags counts sort=count format=json | jq '.[0:15]'  # Top 15 themes this week
obsidian links file="<daily note>" format=json               # For each day, see what it connects to
```

Look for:

- Ideas that appeared on multiple days this week (evolving thinking worth highlighting)
- Backlink chains showing how a conversation or meeting rippled into later thinking
- Themes from daily notes that connect to open questions in context files
- Notes from previous weeks that this week's thinking builds on or contradicts

The best weekly learnings come from noticing patterns the writer was too close to see. Use the graph structure to find these.

---

Review recent posts (past 7 days).

Look for:

These often reveal what you're genuinely excited about vs. what's just operational.

---

## Step 5: Review Calendar (Past 7 Days)

Pull the past week's calendar.

Look for:

- Key meetings that happened (especially external ones, recordings, team syncs)
- How time was actually spent
- Any deviation from the intended structure (and what that means)

---

## Step 6: Review Messages

Scan recent messages for:

- Important team conversations
- Decisions made
- Things that came up worth reflecting on for the team

---

## Step 7: Synthesize — Output to Terminal

Print everything below directly to the terminal. Do NOT create any files.

### Output Format:

**WEEKLY LEARNINGS PREP -- Week \[number\], \[year\]**

---

**FROM LAST EMAIL (threads to continue or resolve):**

- \[Thread from previous email that developed further this week\]
- \[Promise made that can now be addressed\]

---

**CANDIDATE TOPICS (ranked by depth of thinking + relevance to team):**

For each candidate:

**\[#\]. \[Topic name\]** -- \[Project area\]

- What happened: \[Specific events, conversations, or decisions\]
- The insight: \[The non-obvious thing worth sharing\]
- Source: \[Which daily notes, meetings, or posts contain the raw thinking\]

List 5-8 candidates.

---

**CONNECTING THREAD:**  
If there's a theme that ties multiple things together this week, name it. The best emails connect specifics to a bigger idea.

---

**OPERATIONAL UPDATES (not learnings, but the team should know):**

- \[Decisions, schedule changes, deals closed, etc.\]

---

**SUGGESTED STRUCTURE:**  
Recommend 3-4 sections for the email based on what has the most depth. The email should take no more than an hour to write.

---

## Output Guidelines

- Print everything to terminal. No file creation.
- Be specific: cite which daily note, which meeting, which post.
- Prioritize insights over updates. The team doesn't need a recap. They need to understand how you're thinking.
- Match existing tone: first person, reflective, connects specific events to broader ideas.

---

## Related Commands

- [[Prompt - Learned|/learned]] — Generates writing at three levels from vault thinking on a topic
- [[Prompt - Close Day|/close-day]] — End-of-day processing that extracts, categorizes, and files insights from today's note