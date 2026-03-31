---
title: "Prompt - Evolve"
created: 2026-03-25
description: "Prompt - Evolve"
tags:
  - "vault-command"
related:
  - "[[Prompt - Leverage]]"
  - "[[Prompt - Make]]"
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Money]]"
  - "[[Prompt - Compound]]"
---
## Evolve -- Find the Intersection of Readiness and Leverage

Finds ideas at the intersection of readiness and leverage -- things that are both mature enough to act on AND strategically important enough to produce disproportionate returns. Not just what's ready to ship. Not just what's strategically important. The things that are both.

**Usage:** `/evolve` (full scan) or `/evolve [domain]` (focused on a specific domain)

---

## What Makes This Different

This is NOT:

- [[Prompt - Make|/make]] (scores readiness only -- Evolve adds a strategic leverage dimension)
- [[Prompt - Leverage|/leverage]] (finds skill gaps and investment areas -- Evolve finds ready-to-ship items with strategic weight)
- [[Prompt - Ideas|/ideas]] (generates new ideas -- Evolve evaluates existing ideas on readiness x leverage)
- [[Prompt - Money|/money]] (revenue opportunities -- Evolve is broader, covering any form of strategic return)

This IS: **The intersection of readiness x leverage -- finding the thing that is BOTH ready to ship AND strategically important.** Most ideas are either ready but low-leverage (easy wins that don't compound) or high-leverage but unready (important but you can't act yet). The action zone is where both dimensions are high.

---

## Phase 1: Readiness Inventory

Find ideas and projects with high graph density and recent activity.

```bash
obsidian vault                                                  # Quick overview
obsidian search:context query="<domain if provided>" format=json
obsidian backlinks file="<hub note>" counts format=json
obsidian tags counts sort=count format=json | jq '.[0:20]'      # Top 20 themes
obsidian recents                                                 # Recently active notes = readiness signal
```

For each candidate, assess readiness:

```bash
obsidian search:context query="<candidate topic>" format=json
obsidian backlinks file="<candidate hub note>" counts format=json
obsidian links file="<candidate hub note>" format=json
obsidian wordcount file="<candidate hub note>"
```

Score each candidate on readiness (1-5):

| Score | Meaning |
|---|---|
| 1 | Raw -- a few scattered mentions, no thesis |
| 2 | Forming -- recurring theme, but no structure |
| 3 | Developing -- clear topic, some vault material, gaps remain |
| 4 | Almost -- thesis clear, material available, could ship with focused effort |
| 5 | Ready -- the vault has done most of the thinking, assembly is the main task |

For each candidate, note:

- **Material available:** How many notes, daily entries, and context file references?
- **Thesis clarity:** Can you state what this idea argues in one sentence?
- **Effort estimate:** Hours to produce a minimum viable version?

---

## Phase 2: Leverage Overlay

For each ready idea (readiness 3+), assess its strategic leverage.

### Domain Unlock Count

How many separate domains does this idea unlock or advance if shipped?

```bash
obsidian search:context query="<candidate topic>" format=json  # search across all context files
```

A high-leverage idea touches 3+ domains. An essay about a framework you developed might advance your reputation (audience), your consulting practice (revenue), your podcast (content), and your thinking (intellectual development) simultaneously.

### Constraint Breaking

What constraint does shipping this idea break?

- Does it resolve a bottleneck that's been blocking other work?
- Does it create an asset that makes future work easier?
- Does it unlock a relationship, opportunity, or capability?

### Compounding Potential

What compounds if this ships?

- Does it create something that gets more valuable over time?
- Does it establish a position that makes future ideas easier to publish?
- Does it build infrastructure (audience, credibility, network) that benefits everything else?

Score each candidate on leverage (1-5):

| Score | Meaning |
|---|---|
| 1 | Single-use -- benefits one project, no compounding |
| 2 | Narrow -- benefits 1-2 areas, limited compounding |
| 3 | Moderate -- touches 2-3 domains, some compounding |
| 4 | High -- touches 3-4 domains, breaks a constraint, compounds |
| 5 | Transformative -- unlocks multiple domains, breaks a major constraint, creates compounding infrastructure |

---

## Phase 3: Evolution Matrix

Plot every candidate on a 2x2 matrix:

```
                    LEVERAGE
                Low          High
           +-----------+-----------+
    High   | Easy Wins | ACTION    |
READINESS  |           | ZONE      |
           +-----------+-----------+
    Low    | Noise     | Investment|
           |           | Zone      |
           +-----------+-----------+
```

### Action Zone (High Readiness + High Leverage)

These are the priority items. Ready to ship AND strategically important. If you're going to do one thing, do something from here.

### Easy Wins (High Readiness + Low Leverage)

Ready to ship but won't move the needle much. Fine for low-energy days or building momentum. Don't mistake activity here for progress.

### Investment Zone (Low Readiness + High Leverage)

Strategically important but not ready yet. These need deliberate investment -- vault material, thinking time, research. Track them and revisit.

### Noise (Low Readiness + Low Leverage)

Neither ready nor important. Don't spend time here. If something sits in this quadrant across multiple /evolve runs, consider dropping it entirely.

Present the matrix with actual note names and scores:

| Candidate | Readiness | Leverage | Quadrant |
|---|---|---|---|
| \[Note/Topic\] | X/5 | X/5 | Action Zone / Easy Win / Investment / Noise |

---

## Phase 4: Evolution Path

For the top 3-5 items in the Action Zone, propose the specific next step.

### For Each Action Zone Item:

**\[Candidate Name\]** -- Readiness: X/5, Leverage: X/5

**What form should this take?**
Not every idea becomes an essay. Consider: article, product, conversation, system change, framework, tool, pitch, partnership proposal. Suggest 2-3 forms with reasoning.

**Minimum viable version:**
What is the smallest version of this that captures the core value? What could you ship in a single focused session?

**90-day path:**
If you committed to this for 90 days, what would the full evolution look like?

- **Week 1-2:** \[specific first action\]
- **Month 1:** \[milestone\]
- **Month 2:** \[milestone\]
- **Month 3:** \[what "done" looks like\]

**What it unlocks:**
Specifically, what becomes possible after this ships that isn't possible now?

### For Investment Zone Items:

**\[Candidate Name\]** -- Readiness: X/5, Leverage: X/5

**What's missing:**
Specific gaps that prevent readiness. Not "needs more thinking" but "needs a concrete example of X" or "needs the counterargument addressed."

**Investment required:**
Hours and type of work (research, writing, conversations, experimentation).

**When to revisit:**
What signal would indicate this has become ready?

---

## Temporal Tracking

Check if prior /evolve runs exist:

```bash
obsidian search query="/evolve" path="Daily Notes"
obsidian search query="evolution matrix" path="Daily Notes"
obsidian search query="action zone" path="Daily Notes"
```

If prior runs found:

- Which Action Zone items were acted on? What happened?
- Which moved between quadrants? (An item that moved from Investment to Action Zone is high priority. One that moved from Action Zone to Easy Wins lost its strategic moment.)
- Which have been in the Action Zone for 2+ runs without action? These are procrastination signals. Name them.

---

## Anti-Patterns

**1. The Easy Win Trap**
Doing only bottom-right items because they're comfortable and completable. Easy Wins feel productive but don't compound. If every /evolve run results in Easy Win actions and ignored Action Zone items, the strategy is broken.

**2. The Investment Fantasy**
Planning top-left items without committing resources. "I'll get to it when I have time" means never. If an Investment Zone item is truly high-leverage, it needs a concrete plan: what gets deprioritized to make room?

**3. The Optimization Loop**
Endlessly rescoring instead of acting. If the same items appear in the Action Zone across 3+ runs, stop evaluating and start executing. The scores aren't going to change. The work is.

**4. The Leverage Inflator**
Claiming everything is high-leverage because it "could" touch multiple domains. Leverage must be specific and evidence-based. "This essay could go viral" is not leverage. "This essay addresses a question three clients have asked me and would serve as a reusable asset for future client conversations" is leverage.

**5. The Readiness Deflator**
Underscoring readiness because the work isn't "perfect." Readiness means the vault has done most of the thinking. The gap between a 4 and a 5 is usually a few hours of focused work, not more research.

---

## Output Format

**EVOLVE REPORT**
**Scope:** \[General / Domain-focused\]
**Candidates assessed:** \[number\]
**Action Zone items:** \[number\]
**New since last run:** \[number, or "First run"\]

---

\[Evolution Matrix table\]

---

### Action Zone

\[Evolution path for each top item\]

### Investment Zone

\[Investment requirements for high-leverage unready items\]

### Easy Wins

\[Brief list -- available for low-energy execution\]

---

\[Temporal tracking results\]

---

## Output Guidelines

- The Action Zone is the entire point. If it's empty, say so -- it means either nothing is ready or nothing is strategically important enough. Both are useful findings.
- Be specific about forms and next steps. "Write an essay" is not an evolution path. "Draft the argument using notes X, Y, Z as source material, targeting 2,000 words, publishable on X" is.
- The 90-day path should be concrete enough to put on a calendar.
- Don't sugarcoat the Noise quadrant. If something is low readiness and low leverage, it's noise. Saying so saves time.
- The most valuable output is often the Investment Zone analysis -- knowing what's strategically important but not yet ready tells you where to direct vault-building energy.

---

## Related Commands

- [[Prompt - Leverage|/leverage]] -- Identifies high-leverage skills and knowledge that would produce disproportionate breakthroughs
- [[Prompt - Make|/make]] -- Scans the vault for ideas ready to become something the world sees
- [[Prompt - Ideas|/ideas]] -- Generates a comprehensive list of ideas across multiple domains from vault patterns
- [[Prompt - Money|/money]] -- Revenue advisor that diagnoses the revenue system and surfaces opportunities
- [[Prompt - Compound|/compound]] -- Answers the same question across three time periods to show context compounding