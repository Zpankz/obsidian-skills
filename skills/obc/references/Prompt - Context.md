---
title: "Prompt - Context"
created: 2026-03-06
description: "Prompt - Context"
tags:
  - "vault-command"
related:
  - "[[Prompt - Today]]"
  - "[[Prompt - Close Day]]"
  - "[[Prompt - Ghost]]"
  - "[[Prompt - Stranger]]"
---
## Context Loading

Your job is to build comprehensive context about the user before beginning any work. Read thoroughly and follow backlinks.

## Step 1: Vault Overview & Structure

Get a quick snapshot of the vault's size and shape, then read all context files:

```bash
obsidian vault                                     # Total files, folders, size at a glance
obsidian read file="README"                        # Vault overview and structure
obsidian read file="<Company-Context>"             # Company context
obsidian read file="<Project-Context>"             # Project context
obsidian read file="Personal Workflow Context"     # Scheduling, workflow, preferences
```

## Step 2: Explore Directories

List and understand the contents of key folders:

```bash
obsidian folder path="<Company>" info=files        # File count and size for key folders
obsidian folder path="<Project>" info=files
obsidian files folder="<Company>" ext=md
obsidian files folder="<Project>" ext=md
```

## Step 3: Follow Backlinks

As you read each file, follow backlinks and discover connections. Use `counts format=json` to prioritize which connections to follow first:

```bash
obsidian backlinks file="<note name>" counts format=json  # What links TO a note, ranked by count
obsidian links file="<note name>" format=json             # Outgoing links FROM a note
obsidian read file="<linked note>"                        # Read linked notes
```

Continue following backlinks recursively until you have read all connected documents. Prioritize notes with the highest backlink counts — these are hub notes.

## Step 4: Recent Daily Notes

Read today's note and the most recent daily notes (last 5-7 days). Also check recently modified notes for non-daily activity:

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # for each past day
obsidian recents                                 # Recently modified notes (catches non-daily edits)
```

Understand:

- What the user has been working on
- What they've been thinking about
- Current priorities and blockers
- Recent decisions and shifts

## Step 4b: Recent Weekly Learnings

Find and read the most recent 2-3 weekly learnings:

```bash
obsidian search query="Weekly Learnings" format=json | jq -r '.[0:3] | .[].file'
# Then read each result:
obsidian read file="<most recent learnings>"
```

These capture how thinking is evolving week to week.

## Step 4c: Open Tasks

Pull incomplete tasks from the vault to understand outstanding commitments:

```bash
obsidian tasks todo verbose format=json | jq '.[0:20]'  # Top 20 open tasks with file context
```

## Step 4d: Vault Structure & Hidden Connections

Explore the vault's structure and surface things that aren't visible from reading individual files:

```bash
obsidian vault                                      # Quick stats recap
obsidian orphans total                              # Count of orphaned notes
obsidian orphans                                    # Notes nothing links to (potentially forgotten)
obsidian deadends                                   # Notes with no outgoing links (isolated thinking)
obsidian unresolved counts verbose format=json      # Broken [[links]] ranked by reference count
obsidian tags counts sort=count format=json         # Theme distribution, machine-readable
```

Use this to understand:

- Which areas of thinking are well-connected vs. isolated
- What ideas have been started but not developed (orphans)
- What the user keeps referencing but hasn't formalized (unresolved links — the most-referenced ones are the biggest gaps)
- Where attention is concentrated vs. sparse (tag distribution)

Include notable findings in the synthesis.

## Step 5: Synthesis

Once you have read everything, provide a brief synthesis:

1. **Current priorities** - What matters most right now
2. **Active projects** - What's in motion
3. **Open questions** - What's unresolved
4. **Recent shifts** - What's changed in thinking or approach

Then say: "Context loaded. What would you like to work on?"

## Notes

- If a specific domain is passed as an argument (e.g., `/context podcast`), prioritize that domain's files but still read the core context
- Pay attention to confidence markers: `[solid]`, `[evolving]`, `[hypothesis]`, `[questioning]`
- The goal is maximum context so the agent can work effectively without asking basic questions

---

## Related Commands

- [[Prompt - Today|/today]] — Reviews calendar, tasks, and vault patterns to generate a daily plan with priorities
- [[Prompt - Close Day|/close-day]] — End-of-day processing that extracts, categorizes, and files insights from today's note
- [[Prompt - Ghost|/ghost]] — Answers a question as the vault's author, drawing only on vault evidence
- [[Prompt - Stranger|/stranger]] — Writes a portrait of the vault's author as seen by an outsider reading cold