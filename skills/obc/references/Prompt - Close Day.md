---
title: "Prompt - Close Day"
created: 2026-03-06
description: "Prompt - Close Day"
tags:
  - "vault-command"
related:
  - "[[Prompt - Context]]"
  - "[[Prompt - Today]]"
  - "[[Prompt - Learned]]"
  - "[[Prompt - Weekly Learnings]]"
---
## End-of-Day Processing

## Step 1: Read Today's Daily Note

Read today's daily note and get an outline of its structure:

```bash
obsidian daily:read
obsidian outline file="<today's date>" format=json    # Heading tree — shows what sections exist
obsidian tasks daily todo format=json                  # Incomplete tasks from today's note
```

Parse everything captured: free-form writing, meeting notes, ideas, commitments, tasks mentioned, people referenced.

## Step 1.5: Structured Vault Connection Discovery

After reading today's note, run these specific queries every time:

### Required Queries

```bash
obsidian tags counts sort=count format=json | jq '.[0:15]'    # Top 15 themes, machine-readable
obsidian search:context query="<theme 1 from today>" format=json  # for each major topic in today's note
obsidian search:context query="<theme 2 from today>" format=json
obsidian search:context query="<theme 3 from today>" format=json
obsidian backlinks file="<notes referenced today>" counts format=json  # ranked connections
obsidian orphans                                         # any forgotten notes that relate to today's themes?
```

### Confidence Marker Detection

Check if today's writing shifted confidence level on anything:

- Read the relevant context files for topics discussed today
- Compare today's language with the confidence markers in those files
- Flag: "Yesterday you were `[hypothesis]` on X, today you sound `[solid]` " or "You wrote confidently about X today but the context file still has it as `[questioning]` "
- Suggest specific marker updates if warranted

### Contradiction Surfacing

Check if anything written today contradicts a previous entry:

```bash
obsidian search:context query="<strong claim from today>"  # find earlier mentions
```

- Does today's writing take a position that conflicts with something written last week?
- Did today resolve a previously open question, or create a new contradiction?
- Flag: "On \[date\] you wrote \[X\]. Today you wrote \[Y\]. These don't agree. Worth reconciling?"

### Connection Insights

Surface findings as: "Today you wrote about X. This connects to [[note]] from \[date\] where you were thinking about Y. Worth revisiting?" and "This is the third time \[topic\] has come up in the past two weeks."

## Step 2: Extract & Categorize

### Action Items

Pull out anything that looks like a task or commitment:

- Things promised to others
- Things to follow up on
- Deadlines mentioned

### Ideas & Insights

Capture any original thinking worth preserving:

- Observations about work patterns
- Ideas for projects, content, or experiments
- Realizations or shifts in perspective

### People & Commitments

Note any commitments made to or involving others:

- Follow-ups owed
- Meetings to schedule
- Messages to send

### Questions Raised

Capture open questions that emerged:

- Things to investigate
- Decisions pending
- Uncertainties to resolve

## Step 3: Suggest Filing Locations

For each extracted item, recommend where it should live:

| Item | Type | Suggested Location | Action |
| --- | --- | --- | --- |
| ... | Insight | [[Context File]] | Add to relevant section |
| ... | Task | Google Tasks | Create task with due date |
| ... | Idea | [[Related Note]] | Add to running log |

## Step 4: Suggest Backlinks

Discover existing connections and verify note existence:

```bash
obsidian links file="<today's date>" format=json       # What today's note already links to
obsidian backlinks file="<today's date>" format=json   # What links TO today's note
obsidian search query="<person or project name>" format=json  # Verify notes exist before suggesting links
```

- People mentioned -> link to their note if exists
- Projects mentioned -> link to project notes
- Concepts mentioned -> link to relevant context files

Present as: "Consider adding these backlinks: [[Person]], [[Project]], [[Concept]] "

## Step 5: Context File Updates

Flag if anything from today should update a context file:

- New belief or shift in thinking -> relevant context file's "What's shifted recently"
- New constraint discovered -> Constraints section
- Question resolved or new question raised -> Open Questions section
- Confidence level change -> Update the marker

Ask: "Should I update \[context file\] with \[specific change\]?" for each suggestion.

## Step 6: Carry Forward

### What to carry into tomorrow

Based on today's note, what should be top of mind tomorrow?

- Unfinished priorities
- Commitments due soon
- Momentum to maintain

### Quick Wrap Answers

If the Quick Wrap section wasn't filled in, draft answers based on the day's content:

1. Did I explore anything new today?
2. What did I actually move forward?
3. What bottleneck became obvious?
4. One thing to carry into tomorrow?

---

## Output Format

### Today's Extraction

\[Categorized list of items pulled from the note\]

### Vault Connections

\[Confidence marker changes, contradictions found, recurring themes\]

### Filing Suggestions

\[Table of where things should go\]

### Backlinks to Add

\[List of suggested links\]

### Context File Updates

\[Specific changes to propose, with confirmation requests\]

### Carry Forward

\[What matters for tomorrow\]

### Quick Wrap (if not completed)

\[Draft answers to reflection questions\]

---

Keep output concise. The goal is a 5-minute ritual, not a lengthy report. Focus on filing and surfacing what matters, not summarizing the day.

---

## Related Commands

- [[Prompt - Today|/today]] — Reviews calendar, tasks, and vault patterns to generate a daily plan with priorities
- [[Prompt - Learned|/learned]] — Generates writing at three levels from vault thinking on a topic
- [[Prompt - Weekly Learnings|/weekly-learnings]] — Surfaces patterns and candidate topics for a weekly team email