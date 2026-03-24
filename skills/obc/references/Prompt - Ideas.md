---
title: "Prompt - Ideas"
created: 2026-03-06
description: "Prompt - Ideas"
tags:
  - "vault-command"
related:
  - "[[Prompt - Emerge]]"
  - "[[Prompt - Graduate]]"
  - "[[Prompt - Guests]]"
  - "[[Prompt - Make]]"
  - "[[Prompt - Leverage]]"
  - "[[Prompt - XArticle]]"
  - "[[Prompt - Synthesize]]"
  - "[[Prompt - Evolve]]"
---
## Ideas Generation

## Purpose

Generate a comprehensive list of ideas across multiple domains to fuel exploration, break through bottlenecks, and improve life. This command surfaces both obvious high-impact opportunities and non-obvious insights from patterns in the vault.

---

## Step 1: Vault Relationship Exploration

Start with structural analysis before reading individual files. This surfaces connections that aren't visible from reading files in isolation and primes the rest of the analysis.

```bash
obsidian vault                                          # Quick overview stats
obsidian orphans                                        # Notes nothing links to (forgotten ideas, neglected projects)
obsidian deadends                                       # Notes with no outgoing links (isolated thinking)
obsidian unresolved counts verbose format=json          # Broken [[links]] ranked by frequency — ideas pulling at you
obsidian tags counts sort=count format=json | jq '.[0:20]'  # Top 20 themes
obsidian tasks todo verbose format=json | jq '.[0:10]'  # Open tasks — unfinished commitments suggest ideas
```

For each context file and key daily note theme, trace connections:

```bash
obsidian backlinks file="<note>" counts format=json     # What else links to this, ranked
obsidian links file="<note>" format=json                # What does this link to
obsidian search:context query="<key theme>" format=json  # Where else does this theme appear, with lines
```

Follow backlink chains 2-3 hops deep from the most active themes. Look for:

### Cross-Domain Pattern Detection

Look for the same problem, question, or theme appearing across multiple domains simultaneously. These convergences signal breakthrough opportunities, because when three separate areas of life point at the same thing, it's probably important.

```bash
obsidian search:context query="<pattern from domain A>" format=json  # does it appear in domain B?
```

---

## Step 2: Deep Context Review

### Daily Notes (Past 30 Days)

Use the obsidian CLI to read daily notes from the past 30 days:

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # for each past day
```

Extract:

- Frustrations and friction points mentioned
- Things that sparked energy or excitement
- Recurring interests or curiosities
- Problems mentioned but not solved
- Wishes ("I wish I could...", "It would be nice if...")
- Things tried and abandoned (why?)
- Questions asked but not answered

**Sparse data handling:** If daily notes are sparse for this period, expand to 45-60 days.

### Context Files

Use the obsidian CLI to read all active context files:

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

Extract:

- Open questions (explicitly listed)
- Hypotheses marked as untested
- Things marked `[questioning]` or `[evolving]`
- Constraints that might be worth challenging
- Goals without clear paths

### Calendar (Past 2 Weeks + Next 2 Weeks)

Review calendar for:

- Where time is actually going (meeting types, patterns)
- What's crowding out exploration time
- Recurring commitments worth questioning
- Gaps that could be used differently

Review recent posts, threads, and engagement:

- Topics you're publicly thinking about
- Posts that got high engagement (what resonates with others)
- Posts that underperformed (interesting to you but not others, or wrong framing?)
- Threads you wrote (these are essays in disguise)
- Ideas that performed well worth expanding into longer content

### Messages (Past 30 Days)

Review recent messages for patterns:

- Conversations that sparked energy or ideas
- People you keep meaning to follow up with
- Plans discussed but not acted on
- Relationships worth deepening
- Recurring topics across conversations

### Essays & Published Work

```bash
obsidian files folder="Essays"
obsidian search query="<relevant terms>" path="Essays"
```

Look for:

- Topics written about (what's the throughline?)
- Gaps in what's been explored
- Old ideas worth revisiting
- Things started but not finished

---

## Step 2.5: Temporal Tracking

Before generating ideas, check if previous /ideas runs exist in the vault:

```bash
obsidian search query="ideas generation" path="Daily Notes"
obsidian search query="/ideas" path="Daily Notes"
```

If prior runs are found:

- Which ideas from previous runs got traction? (Appeared in later daily notes, got calendar time, produced output)
- Which were abandoned? (Never mentioned again)
- Which keep recurring across runs? (These are persistent interests masquerading as ideas. They need commitment, not another suggestion.)

Prevent redundant suggestions. If an idea was generated before and went nowhere, either drop it or frame it differently: "This was suggested on \[date\] and didn't get traction. What would need to change for it to happen this time?"

---

## Step 3: Pattern Analysis

Before generating ideas, synthesize patterns:

### What's Working

Things that consistently produce energy, output, or satisfaction.

### What's Frustrating

Recurring friction, complaints, or energy drains.

### What's Missing

Gaps between stated goals and current activities. Things desired but not pursued.

### Recurring Interests

Topics, people, or activities that keep coming up across notes.

### Bottlenecks

Places where progress is blocked, often by the same thing repeatedly.

---

## Step 4: Generate Ideas

For each category below, generate 3-5 specific, actionable ideas. Prioritize ideas that are:

- High impact (would meaningfully improve life/work)
- Non-obvious (not the first thing that comes to mind)
- Grounded in actual patterns from the vault (not generic advice)

### Tools to Build

Custom tools, scripts, slash commands, or automations that would solve specific problems identified in the vault.

### Tools to Start Using

Existing products, apps, or services that would address identified needs.

### Systems to Implement

Workflows, processes, or routines that would create structure around recurring challenges.

### Products to Purchase

Physical items, subscriptions, or one-time purchases that would improve daily life.

### Habits to Adopt

Behavioral changes or practices to build.

### Subjects to Investigate

Topics worth going deep on, based on recurring interests or open questions.

### Things to Write & Publish

Essay ideas, threads, or content based on unique perspectives or experiences in the vault.

### Films to Watch

Based on interests, themes in work, or creative fuel needs.

### Conversations to Have

People to reach out to, relationships to deepen.

### Experiments to Run

Low-cost tests of ideas, beliefs, or approaches.

---

## Step 5: Prioritize

### Top 5 High-Impact, Do Now

The five ideas across all categories that would have the biggest positive impact and are actionable this week.

### Top 5 High-Impact, Requires Setup

Ideas that need more preparation but are worth investing in.

### Top 5 Non-Obvious Insights

Ideas that emerged from pattern recognition, not obvious from surface-level thinking.

### The One Thing

If you could only act on one idea from this entire list, which one would create the most positive change? Why?

---

## Step 6: Connect to Exploration

Based on this analysis, suggest:

### Tomorrow's Exploration

One specific thing to explore tomorrow.

### This Week's Investigation

A subject or project to go deeper on this week.

### This Month's Experiment

A larger experiment to run over the coming weeks.

---

## Output Guidelines

- Be specific, not generic. Every idea should connect to something actually in the vault or observed in activity.
- Cite sources: "Based on your note from \[date\] about..."
- Distinguish between obvious-but-important and genuinely non-obvious insights.
- Include rough effort/cost estimates where relevant.
- This should feel like talking to someone who deeply understands your situation, not reading a listicle.

---

## Related Commands

- [[Prompt - Emerge|/emerge]] — Surfaces ideas the vault implies but has never explicitly stated
- [[Prompt - Make|/make]] — Scans the vault for ideas ready to become something the world sees
- [[Prompt - Leverage|/leverage]] — Identifies high-leverage skills and knowledge that would produce disproportionate breakthroughs
- [[Prompt - XArticle|/xarticle]] — Finds which idea is most ready to become an X article by scoring graph density, energy, and synthesis potential