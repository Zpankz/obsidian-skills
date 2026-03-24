---
title: "Prompt - Graduate"
created: 2026-03-06
description: "Prompt - Graduate"
tags:
  - "vault-command"
related:
  - "[[Prompt - Backlinks]]"
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Make]]"
  - "[[Prompt - Audit]]"
---
## Graduate: Daily Note Idea Extractor

## Purpose

Ideas, insights, and original thinking accumulate in daily notes but rarely graduate into standalone notes where they can compound through backlinks. This command scans recent daily notes, surfaces the best candidates, and helps you decide what to promote.

---

## Step 1: Scan Recent Daily Notes

Read the past 14 days of daily notes:

```bash
obsidian daily:read
obsidian read file="YYYY-MM-DD"  # for each day in the past 14 days
```

Also find tagged ideas directly:

```bash
obsidian tag name="idea" verbose format=json     # All notes tagged #idea with counts
obsidian tag name="expand" verbose format=json   # All notes tagged #expand
obsidian unresolved counts verbose format=json   # [[links]] to notes that don't exist yet
```

For each daily note, extract candidates for graduation. Look for:

### Explicit signals

- `#idea` tags
- `#expand` tags
- Anything with language like "I should write about", "worth investigating", "need to explore", "this is important"
- Named concepts (capitalized or in quotes, e.g., "Context Architecture", "software will become fashion")
- Unresolved `[[links]]` to notes that don't exist yet but represent real ideas

### Implicit signals

- Paragraphs where energy is clearly high (longer passages, exclamation points, strong language)
- Original claims or frameworks (sentences that state a position, not just record events)
- Recurring themes that appear 3+ times across different days
- Questions that keep getting asked but never get their own note

### What NOT to extract

- Tasks and to-dos (those belong in task management, not note graduation)
- Meeting logistics or scheduling notes
- Complaints or venting without an underlying insight
- Things that already have their own standalone note

---

## Step 2: Cross-reference with Existing Vault

For each candidate, check if it already exists:

```bash
obsidian search query="<candidate concept>" format=json          # Does it exist elsewhere?
obsidian backlinks file="<candidate if it exists>" counts format=json  # How connected is it?
obsidian wordcount file="<candidate if it exists>"               # Is it thin or developed?
```

Categorize each candidate:

- **New concept** - No note exists, no substantial coverage elsewhere. Best candidate for graduation.
- **Underdeveloped** - A note exists but it's thin (just a title or a few lines). Candidate for enrichment rather than creation.
- **Already covered** - Substantial note exists. Skip, or flag if the daily note adds something the existing note doesn't have.
- **Recurring unresolved** - Referenced as `[[unresolved link]]` multiple times. High priority for graduation since the vault is already pointing at it.

---

## Step 3: Present Candidates

Present the candidates in a table, ordered by priority (recurring/high-energy ideas first):

| # | Idea / Concept | Source | Days Mentioned | Status | Recommendation |
| --- | --- | --- | --- | --- | --- |
| 1 | ... | Feb 17, Feb 18 | 2 | Unresolved link | Create standalone note |
| 2 | ... | Feb 14 | 1 | New concept | Create standalone note |
| 3 | ... | Feb 6, Feb 12 | 2 | Thin note exists | Enrich existing note |

For each candidate, include:

---

## Step 4: Graduate Selected Ideas

For each idea the user chooses to graduate, do the following:

### If creating a new standalone note:

### If enriching an existing note:

### If connecting to an MOC:

1. Read the relevant MOC
2. Add the idea/note to the MOC in the appropriate section
3. Create backlinks in both directions

---

## Step 5: Summary

After graduating selected ideas, output:

### Graduated Today

- List of notes created or enriched, with links

### Still in the Queue

- Ideas that were surfaced but not graduated (user chose to skip for now)
- These should be flagged if they appear again in the next [[Prompt - Graduate|/graduate]] run

### Vault Health

- Total ideas found in the scan period
- Number graduated vs. skipped
- Number of `#idea` tags found vs. untagged ideas found (the gap reveals how much is being missed by tagging alone)
- Recurring themes that keep appearing but haven't been graduated yet

---

## Guidelines

- Keep graduated notes concise. A mini-essay is 3-8 paragraphs, not a research paper.
- Preserve the original voice and energy from the daily notes. Don't sanitize the thinking.
- When in doubt about whether to graduate something, present it and let the user decide.
- The goal is 5-10 minutes per run. Surface the best candidates fast, act on the ones that matter, move on.
- If this is the first run, expect a larger backlog. Subsequent runs should be faster.
- Always ask before creating or modifying files.

---

## Related Commands

- [[Prompt - Backlinks|/backlinks]] — Wires the vault graph by finding and executing missing connections
- [[Prompt - Ideas|/ideas]] — Generates a comprehensive list of ideas across multiple domains from vault patterns
- [[Prompt - Make|/make]] — Scans the vault for ideas ready to become something the world sees