---
title: "Prompt - Today"
created: 2026-03-06
description: "Prompt - Today"
tags:
  - "vault-command"
related:
  - "[[Prompt - Context]]"
  - "[[Prompt - Close Day]]"
  - "[[Prompt - Schedule]]"
  - "[[Prompt - XDaily]]"
  - "[[Prompt - 7plan]]"
---
## Daily Review & Planning

## Step 1: Gather Context (Google Calendar + Tasks)

- Review today's calendar and the next 3 days
- Scan inbox for urgent or time-sensitive emails (last 24 hours)

### Google Tasks

Pull tasks from Google Tasks:

- **Overdue**: Tasks past their due date (flag prominently)
- **Due Today**: Tasks with today's deadline
- **Due This Week**: Upcoming tasks in the next 7 days
- **Quick Wins**: Low-effort tasks that can be knocked out fast
- **No Due Date**: Tasks that may need scheduling or are floating

### Obsidian Tasks

Pull incomplete tasks from the vault — these often capture commitments that never made it to Google Tasks:

```bash
obsidian tasks todo verbose format=json | jq '.[] | {file: .path, task: .text, line: .line}'
obsidian tasks daily todo format=json              # Tasks specifically in today's daily note
```

**Sparse data handling:** If the calendar is empty today, focus on vault patterns, overdue tasks, and context file priorities. If Google Tasks returns few results, check daily notes for informal task mentions ("I need to...", "TODO", "follow up on...") and obsidian tasks output above.

## Step 1.5: Review Recent Messages (Last 24 Hours)

Query recent messages for context on conversations, commitments, and things in flight. Look for: commitments made, plans confirmed, requests from others, follow-ups needed.

## Step 2: Review Obsidian Daily Notes

Read daily notes from the past 7 days:

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # for each of the past 6 days
obsidian recents                                 # Catch recently modified non-daily notes too
```

Look for: recurring themes, unfinished threads, commitments made, energy patterns.

**Sparse data handling:** If daily notes are sparse for recent days, expand the range to 10-14 days to find enough signal.

## Step 3: Load Context Files

Read and synthesize all active context files:

```bash
obsidian read file="<Company-Context>"
obsidian read file="<Project-Context>"
obsidian read file="Personal Workflow Context"
```

## Step 3.5: Detect Hard Constraints

Before prioritizing, check for unusual day structure that overrides normal prioritization:

- **Solo parenting?** Check if a partner has travel or commitments that change the childcare schedule
- **Travel day?** Any transit that compresses the work window
- **Recording day?** Content recording requires energy management and prep
- **Special events?** Launches, deadlines, investor meetings that dominate the day
- **Back-to-back meetings?** Days with no gaps require different strategies than open days

If hard constraints exist, flag them prominently. They override normal priority ranking.

## Step 4: Identify Preliminary Priorities

Before exploring the vault, synthesize what you've gathered so far into preliminary priorities:

- The 2-3 most pressing items from calendar, tasks, and recent notes
- The dominant themes from the past week of daily notes
- Any active tensions or open questions from context files

These preliminary priorities guide the vault exploration in the next step.

## Step 4.5: Deep Vault Exploration

Now that priorities are identified, use the vault to enrich and challenge them.

### Theme Surfacing

```bash
obsidian tags counts sort=count format=json | jq '.[0:15]'  # Top 15 themes, machine-readable
```

Compare the most active tags against today's preliminary priorities. Are you working on what you're thinking about? Or is there a disconnect?

### Priority-Informed Vault Search

For each of today's top 2-3 priorities:

```bash
obsidian search:context query="<priority topic>" format=json  # where does this appear, with matching lines
obsidian backlinks file="<related note>" counts format=json   # what connects to this, ranked
obsidian backlinks file="<second hop note>" counts format=json  # go 2-3 hops deep
```

### Broader Pattern Discovery

```bash
obsidian orphans                                    # any forgotten notes relevant to today?
obsidian search:context query="<meeting topic or person name>" format=json  # for key events on today's calendar
```

### Surface Contradictions

Check if today's priorities conflict with anything in the vault:

- Does a recent daily note express doubt about something you're prioritizing today?
- Does a context file's open question suggest a different focus?
- Has your thinking on today's key topic shifted over time?

The goal is not just cross-referencing but illuminating relationships you couldn't easily see on your own.

## Step 5: Synthesize & Deliver

### Core Theme for the Day

A single phrase or sentence that captures what today should be about. Base this on:

- What's most pressing from calendar/tasks
- Patterns from recent notes
- Current priorities from context files
- What the vault exploration revealed

### Top 2 Priorities

The two most important things to progress today. Prioritize based on:

- Blocks others if not done
- Has a hard deadline
- Compounds negatively if delayed
- Directly advances current goals from context files

### Quick Wins (5 items)

Tasks completable in <15 minutes that:

- Unblock someone else
- Clear mental overhead
- Prevent small things from becoming big problems
- Just feel good to get done

### Meeting Audit

Flag meetings that should be:

- **Cancelled**: No clear agenda, your input not essential, or could be async
- **Converted to async**: Can be replaced by a document, video, or message thread
- **Shortened**: Padded time that could be reduced

For each flagged meeting, suggest the specific action and what artifact could replace it if applicable.

---

## Step 6: Generate Interactive Dashboard

After completing the synthesis, create an interactive HTML dashboard (replace if exists).

### Dashboard Requirements

**Structure:**

**Interactivity:**

- Every schedule item and task is clickable to toggle complete
- Completed items show strikethrough and reduced opacity
- Progress ring updates in real-time as items are checked
- Current time block highlights automatically
- Live clock updates every second

**Persistence:**

- Use localStorage with a date-specific key
- Save state on every toggle
- Restore state on page load

**Data to include:**

- All schedule events for today with times and locations
- All tasks organized by category (overdue, due today, due this week, quick wins, floating)
- Task due dates and brief context
- Upcoming events for next 2-3 days
- Any important alerts

**Design notes:**

- Use system fonts
- Checkboxes with green fill when completed
- Overdue items marked in red
- Responsive grid that stacks on smaller screens
- Clean, minimal, focused on usability

---

## Related Commands

- [[Prompt - Context|/context]] — Builds comprehensive context about the user by reading vault files, backlinks, and daily notes
- [[Prompt - Close Day|/close-day]] — End-of-day processing that extracts, categorizes, and files insights from today's note
- [[Prompt - Schedule|/schedule]] — Context-aware scheduling that evaluates requests against current priorities
- [[Prompt - 7plan|/7plan]] — Reshapes the next 7 days around intellectual threads alive in the vault