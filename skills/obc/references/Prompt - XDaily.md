---
title: "Prompt - XDaily"
created: 2026-03-06
description: "Prompt - XDaily"
tags:
  - "vault-command"
related:
  - "[[Prompt - Today]]"
  - "[[Prompt - Learned]]"
---
## X to Daily Notes

Pull recent tweets from your X/Twitter profile and surface anything worth adding to today's Obsidian daily note.

**Context:** Many people use X both for sharing work and as a scratchpad for thinking out loud. Tweets often contain raw ideas, observations, creative project seeds, and reactions that haven't been captured in the vault yet. The goal is to catch anything meaningful that would otherwise be lost.

## Step 1: Read Today's Daily Note

Use the obsidian CLI to read today's daily note:

```bash
obsidian daily:read
```

## Step 2: Open X Profile in Chrome

Use browser automation tools to load your X profile:

**Technical notes:**

## Step 3: Analyze & Compare

Compare the extracted tweets against today's daily note. Identify tweets that contain:

Filter out:

For tweets that pass the filter, use the obsidian CLI to check for vault connections:

```bash
obsidian search query="<tweet topic or key phrase>" format=json  # Find vault connections for each tweet
obsidian backlinks file="<matching note>" counts format=json     # How connected is this topic
```

If a tweet connects to an existing vault note, mention this in the suggestion: "This tweet about X connects to [[existing note]]." This makes the captured item more valuable by grounding it in existing thinking.

## Step 4: Present Suggestions

Present each suggested addition as a numbered item with:

- A short bold title describing the idea/theme
- The relevant tweet text (or synthesized version for threads)
- Why it's worth capturing (connects to X project, new idea, etc.)

Ask which items to add. Accept numbers (e.g., "1, 3, 5" or "all").

## Step 5: Add to Daily Notes

For approved items, use `obsidian daily:read` to get the current note content, then insert items above the reflection/wrap section. For simple appends, use:

```bash
obsidian daily:append content="<content>"
```

When inserting:

- Each item gets its own `---` separator
- Write in first person, direct, conversational
- Add relevant `[[backlinks]]` to existing vault notes where natural
- Tag ideas with `#idea` where appropriate
- Keep the raw energy of the original tweet but expand slightly for vault context
- Don't over-edit or make it sound formal

## Output Style

Be concise. This should feel like a quick 5-minute sweep, not a lengthy analysis.

---

## Related Commands

- [[Prompt - Today|/today]] — Reviews calendar, tasks, and vault patterns to generate a daily plan with priorities
- [[Prompt - Learned|/learned]] — Generates writing at three levels from vault thinking on a topic