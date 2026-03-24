---
title: "Prompt - Leverage"
created: 2026-03-06
description: "Prompt - Leverage"
tags:
  - "vault-command"
related:
  - "[[Prompt - Money]]"
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Compound]]"
  - "[[Prompt - Evolve]]"
---
## Leverage -- Find the Breakthroughs Hiding in Plain Sight

Scan the entire vault to identify the specific skills, knowledge domains, investigations, and mental models that, if developed, would produce disproportionate breakthroughs across your life. Not general self-improvement. Not ideas to pursue. The precise leverage points where a concentrated investment of thinking, learning, or skill-building would crack open multiple stuck things simultaneously.

**The vault reveals the constraints. The solutions can come from anywhere.** The vault is the diagnostic tool, not the pharmacy. Once constraints are mapped, draw from any domain, any field, any discipline, any body of knowledge in the world to find what would break them open. The most transformative leverage points are often things the vault has never mentioned, precisely because they come from outside the current frame of thinking.

**Usage:** `/leverage` (full scan) or `/leverage [domain]` (focused on a specific area)

## What Makes This Different

This is NOT:

- [[Prompt - Ideas|/ideas]] (broad idea generation across categories)
- [[Prompt - Emerge|/emerge]] (implicit ideas the vault hasn't stated)
- [[Prompt - Connect|/connect]] (bridges between two domains)
- [[Prompt - Drift|/drift]] (gaps between intention and behavior)
- [[Prompt - Money|/money]] (revenue opportunities)

This IS: **Identifying the 3-7 things where investing 50-100 hours of deep learning or practice would produce step-function changes in capability, output, or trajectory.** The things where the ROI on attention is 10x-100x, not incremental.

The test: A true leverage point, when developed, unlocks progress in 3+ areas simultaneously. If it only helps one thing, it's a task, not leverage.

## Phase 1: Constraint Mapping

Before looking for leverage, map what's actually constrained. Breakthroughs only matter relative to bottlenecks.

### Step 1: Structural Scan

```bash
obsidian vault                                          # Quick overview stats
obsidian tags counts sort=count format=json | jq '.[0:20]'  # Top 20 themes
obsidian orphans
obsidian deadends
obsidian unresolved counts verbose format=json          # Broken [[links]] ranked by frequency
```

### Step 2: Read Context Files

Read all context files in the vault. For each context file, extract:

- Goals with no clear path forward (capability gap?)
- Items marked `[questioning]` or `[evolving]` (unresolved = potential leverage)
- Stated blockers, frustrations, or recurring frictions
- Things described as important but not progressing

### Step 3: Daily Notes (Past 30 Days)

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 30 days
```

Extract with precision:

- **Repeated frustrations**: The same friction appearing 3+ times signals a missing skill or model
- **Abandoned attempts**: Things started and stopped. Why? What was missing?
- **Admiration signals**: People, work, or capabilities described with envy or aspiration. These reveal desired but unowned capabilities.
- **"I wish I could..."** and **"I need to learn..."** statements
- **Energy patterns**: What produces flow? What drains? Flow signals proximity to leverage. Drain signals missing foundations.
- **Requests for help**: What do you keep asking others to do? That dependency is a potential leverage point.
- **Decisions deferred**: What keeps getting punted? Deferred decisions often signal missing frameworks for deciding.

### Step 4: Behavioral Archaeology

```bash
obsidian search query="stuck" path="Daily Notes"
obsidian search query="frustrated" path="Daily Notes"
obsidian search query="can't" path="Daily Notes"
obsidian search query="don't know how" path="Daily Notes"
obsidian search query="need to learn" path="Daily Notes"
obsidian search query="wish I" path="Daily Notes"
obsidian search query="asked" path="Daily Notes"
obsidian search query="delegated" path="Daily Notes"
obsidian search query="waiting on" path="Daily Notes"
obsidian search query="blocked" path="Daily Notes"
```

Also search for admiration and aspiration signals:

```bash
obsidian search query="impressive" path="Daily Notes"
obsidian search query="genius" path="Daily Notes"
obsidian search query="how did" path="Daily Notes"
obsidian search:context query="want to be"
obsidian search:context query="get better at"
```

### Step 5: Project and Domain Audit

For each active project (from context files), answer:

- What is the binding constraint on progress right now?
- Is the constraint a skill, a relationship, a decision, knowledge, or time?
- If the constraint is a skill or knowledge gap, what specifically is missing?
- How many OTHER projects share this same constraint?

**Critical**: Constraints shared across 3+ projects are the highest-leverage targets. One skill acquisition unblocks multiple fronts.

### Output of Phase 1: The Constraint Map

**Recurring Frictions** (things that keep causing problems)  
For each: what it is, how often it appears, what domains it affects

**Capability Gaps** (skills/knowledge the vault reveals as missing)  
For each: evidence from vault, which projects it blocks

**Dependency Points** (things that require other people because the skill doesn't exist internally)  
For each: who currently fills this, what it costs in time/money/autonomy

**Decision Bottlenecks** (choices that keep getting deferred)  
For each: what framework or knowledge would make the decision clear

## Phase 2: Leverage Detection

Six methods for finding leverage points, ordered by reliability.

### Method 1: Bottleneck Convergence (Highest Reliability)

Find skills or knowledge gaps that are the binding constraint across 3+ domains simultaneously.

Process:

1. Take the constraint map from Phase 1
2. For each constraint, list every project/domain it touches
3. Rank by number of domains affected
4. The constraint that appears in the most domains is the highest-leverage skill to develop

**Example**: If "can't write compelling narratives quickly" blocks the podcast (guest intros), the company (investor updates), X (threads), and essays (publishing cadence), then narrative writing speed is a leverage point. One skill, four unlocks.

Search for cross-domain constraints:

```bash
obsidian search:context query="<constraint from domain A>" format=json  # does it appear in domain B?
```

### Method 2: Adjacent Possible (High Reliability)

Find capabilities that are 80% developed but missing the final 20% that would make them powerful.

Look for:

- Skills used informally that have never been formalized or deepened
- Knowledge referenced but never systematically studied
- Tools used at surface level that have deep capabilities unused
- Frameworks applied intuitively that, if made explicit, would become transferable

```bash
obsidian search:context query="started learning"
obsidian search:context query="basics of"
obsidian search:context query="should go deeper"
obsidian search query="tutorial" path="Daily Notes"
obsidian search query="course" path="Daily Notes"
```

The adjacent possible is high-reliability because the foundation already exists. The incremental effort is small but the capability jump is large.

### Method 3: Multiplier Models (High Reliability)

Find mental models or frameworks that, once internalized, would change how decisions are made across all domains.

Look for:

- Decisions that keep being made badly or slowly (what framework is missing?)
- The same mistake pattern appearing in different contexts (what model would prevent it?)
- Advice consistently sought from others (what do they know that you don't?)
- Books, thinkers, or frameworks referenced with admiration but not yet internalized

```bash
obsidian search query="book" path="Daily Notes"
obsidian search query="read" path="Daily Notes"
obsidian search query="framework"
obsidian search query="model"
obsidian search:context query="thinking about"
```

A multiplier model is different from knowledge. Knowledge tells you facts. A model changes how you process ALL future information. Learning negotiation theory is knowledge. Internalizing game theory is a model.

### Method 4: Removal Leverage (Medium Reliability)

Find things that, if eliminated or automated, would free up disproportionate cognitive or temporal bandwidth.

Not "what should I learn?" but "what should I stop doing manually so I can learn?"

```bash
obsidian search query="every day" path="Daily Notes"
obsidian search query="routine" path="Daily Notes"
obsidian search query="always have to" path="Daily Notes"
obsidian search query="manual" path="Daily Notes"
obsidian search query="repetitive"
```

For each candidate:

- How much time does this consume per week?
- Could it be automated, delegated, or eliminated?
- What would you do with the freed time? (If the answer is vague, the removal isn't leverage. If the answer is specific and high-value, it is.)

### Method 5: Relationship Leverage (Medium Reliability)

Find knowledge domains or skills that would dramatically increase the value of existing relationships or unlock new ones.

```bash
obsidian search query="meeting with" path="Daily Notes"
obsidian search query="conversation with" path="Daily Notes"
obsidian search:context query="network"
obsidian search:context query="mentor"
obsidian search:context query="advisor"
```

Look for:

- Relationships where deeper domain knowledge would make conversations more valuable
- People in the network whose expertise, if partially acquired, would change the dynamic
- Domains where credibility is close but not yet established
- Communities you're adjacent to but can't fully participate in due to knowledge gaps

### Method 6: Identity Leverage (Use Sparingly, Low Reliability but High Impact)

Find the gap between who the vault says you are and who you would need to become for your stated goals to be achievable.

This is the most speculative method. Use only when other methods produce clear signals pointing the same direction.

```bash
obsidian search:context query="I am"
obsidian search:context query="I'm not"
obsidian search:context query="not my strength"
obsidian search:context query="someone who"
```

Look for:

- Self-limiting identity statements that conflict with stated goals
- Capabilities disclaimed that the goals actually require
- Roles avoided that the trajectory demands
- The version of yourself your projects need vs. the version the vault describes

## Phase 3: Beyond the Vault

**This is the most important phase.** The vault shows what you're already thinking about. The most powerful leverage points are often things the vault has NEVER mentioned, because they exist in domains outside your current awareness. The vault is a map of known territory. Breakthroughs live in unknown territory.

### Blind Spot Analysis

Based on the constraints mapped in Phase 1 and the goals in the vault, identify skills and knowledge domains that are completely absent from the vault but would be transformative if developed.

Think across:

- **Adjacent fields**: What disciplines neighbor your work but you've never studied? (e.g., if you run a media company but have never studied distribution theory, audience psychology, or narrative structure formally)
- **Foundational disciplines**: What underlying fields would upgrade everything? (e.g., statistics changes how you evaluate decisions; systems thinking changes how you design organizations; rhetoric changes how you persuade)
- **Counter-intuitive domains**: What fields seem irrelevant but contain transferable frameworks? (e.g., military strategy for resource allocation, game design for engagement, architecture for space design, ecology for community building)
- **Historical parallels**: What did people in similar positions learn that created their breakthrough? What body of knowledge separated those who broke through from those who plateaued?

### The Outsider's Prescription

If a world-class strategic advisor reviewed the vault's constraints with no loyalty to the current plan, what would they prescribe? What would they find obvious that's invisible from inside?

Consider:

- What would someone 10 years ahead on a similar path say is the thing they wish they'd learned sooner?
- What domain knowledge would make the stated goals trivially achievable instead of ambitious?
- What meta-skills (selling, negotiating, writing, public reasoning, financial modeling, hiring) are assumed to be "good enough" but might be the actual ceiling?
- What technical capabilities would collapse timelines if acquired?

### Imported Frameworks

For each constraint from Phase 1, ask: "What field has already solved this problem?" Don't reinvent. Import.

- If the constraint is about making better decisions, study decision science
- If the constraint is about building audience, study direct response marketing
- If the constraint is about managing energy, study performance psychology
- If the constraint is about building teams, study organizational design
- If the constraint is about creative output, study the workflows of prolific creators

The leverage is in bringing proven frameworks from one domain into a domain that hasn't seen them yet.

## Phase 4: Verification

For each candidate leverage point, run these filters:

### Filter 1: The 3+ Domain Test

Does developing this unlock progress in 3 or more separate domains? If it only helps one thing, it's a useful skill but not a leverage point. Downgrade it.

### Filter 2: The Evidence Test

For vault-sourced leverage points: Is there vault evidence of this constraint causing problems? Cite specific instances.  
For beyond-vault leverage points: Is there a clear logical chain from this skill/knowledge to the constraints identified in Phase 1? The evidence is the constraint, not the solution. The vault proves the problem exists. The solution can come from anywhere.

### Filter 3: The Feasibility Test

Can this realistically be developed with 50-100 hours of focused effort? If it requires 1,000+ hours or innate talent, it's not practical leverage. Flag it as long-term if the impact justifies it.

### Filter 4: The Counterfactual Test

If you had this skill/knowledge 6 months ago, what specific things would have gone differently? Be concrete. If you can't name specific situations, the leverage is theoretical, not real.

### Filter 5: The Already-Tried Test

```bash
obsidian search query="<the leverage point stated plainly>"
obsidian search query="<related skill/topic>" path="Daily Notes"
```

Has this been attempted before and abandoned? If yes, what was the blocker? Is the blocker still present? If the same thing keeps being identified as important but never developed, the real leverage point might be whatever is preventing the development, not the skill itself.

### Filter 6: The Compound Test

Does this leverage point compound over time, or is it a one-time unlock? Compound leverage (skills that get more valuable the more you use them) ranks higher than one-time leverage (knowledge that solves a specific problem once).

## Phase 5: Output

### The Leverage Map

For each leverage point (aim for 3-7, no more):

**Leverage Point \[#\]: \[Name\]**

**What it is:** \[One sentence. What skill, knowledge domain, mental model, or capability\]

**Source:** Vault-sourced (evidence of constraint in vault) / Beyond-vault (imported from external domain to address vault constraint) / Blind spot (completely absent from vault, identified through outside analysis)

**The constraint it breaks:** \[What specific friction, bottleneck, or limitation this resolves, with vault evidence of the constraint\]

**Domains it unlocks:** \[List every project/domain that would benefit, with a specific description of HOW for each\]

**The counterfactual:** \[What would have gone differently in the last 6 months if this had been developed\]

**How to develop it:** \[Specific path. Not "read about it" but: which book first, which course, which person to learn from, which project to practice on. The first 10 hours, the next 40, the final 50.\]

**Compound potential:** \[Does this get more valuable over time? How?\]

**Feasibility:** \[Hours required. Realistic timeline. What has to be deprioritized to make room.\]

**Confidence:** High (clear constraint evidence + clear solution path) / Medium (strong constraint signal + plausible solution) / Low (emerging signal, worth investigating)

### The Ranking

Order leverage points by: **(domains unlocked x constraint severity x compound potential) / effort required**

### The #1 Leverage Point

The single thing that, if you spent the next 90 days developing it seriously, would produce the most dramatic shift in your trajectory. Why this one above all others.

### The Surprising One

The leverage point you would never have identified yourself. The one that comes from outside the vault's frame entirely. A domain, skill, or body of knowledge that seems unrelated but would crack open the constraints the vault reveals.

### The Prerequisite Chain

Some leverage points depend on others. If learning B requires first learning A, show the chain. Start with the foundation.

### The Anti-Leverage List

Things that FEEL like they would be high-leverage but aren't, based on evidence:

- Skills the vault obsesses over that wouldn't actually change outcomes
- Knowledge domains that are interesting but not load-bearing
- Things that would be satisfying to learn but don't connect to any active constraint

For each: why it feels like leverage, why it isn't, and what to do instead.

## Temporal Tracking

Check for previous runs:

```bash
obsidian search query="/leverage" path="Daily Notes"
obsidian search query="leverage point" path="Daily Notes"
obsidian search query="breakthrough" path="Daily Notes"
```

If prior runs found:

- Which leverage points were identified before? Were they developed?
- If developed: did the predicted breakthrough occur? Update the model.
- If not developed: why not? Is the blocker itself a leverage point?
- What's changed since the last run?

Do not re-suggest leverage points that were previously identified and ignored without addressing why they were ignored.

## Anti-Patterns

**1\. The Self-Help List**  
Generic skills like "communication" or "leadership" or "discipline." Every leverage point must be specific to this person and these constraints. "Negotiation" is generic. "Learning to structure equity-for-services deals so the accelerator can acquire talent without cash" is leverage.

**2\. The Interesting-But-Irrelevant**  
Fascinating domains that would be fun to explore but don't connect to any active constraint. Intellectual curiosity is good. Calling it leverage is dishonest.

**3\. The Already-Strong Skill**  
Suggesting development in areas where the vault shows existing competence. Leverage comes from filling gaps, not polishing strengths (unless the strength is at 80% and the last 20% is transformative).

**4\. The Time Fantasy**  
Suggesting skill development that requires hundreds of hours when the vault shows no available time. Every suggestion must account for what gets displaced.

**5\. The Single-Domain Skill**  
Skills that only help one project. These are useful but they're not leverage. Leverage is definitionally multi-domain.

**6\. The Motivation Trap**  
"You should want to learn this" is not leverage analysis. The vault reveals what's actually blocking progress. Stay with the evidence for the constraint. Be creative and expansive for the solution.

**7\. The Guru Recommendation**  
Suggesting vague "go study under so-and-so" or "immerse yourself in X philosophy." The path must be concrete: specific resources, specific practice, specific milestones.

**8\. The Meta-Skill Spiral**  
"Learn how to learn" or "develop better systems for developing skills." These can be real leverage points but only when the evidence shows that the learning process itself is the bottleneck. Usually the bottleneck is more specific.

**9\. The Vault Ceiling**  
Limiting recommendations to only things the vault mentions. The vault reveals constraints. The solutions should come from ANYWHERE, including domains the vault has never touched. The most powerful leverage is often imported from an unexpected field.

## Output Guidelines

- The vault is the diagnostic instrument, not the boundary of the answer. Use it to find what's stuck. Draw from any domain to find what would unstick it.
- For vault-sourced leverage points, cite specific vault evidence for the constraint.
- For beyond-vault leverage points, show the logical chain: vault constraint -> why this external domain addresses it -> specific path to acquire it.
- The output should make the user see their own constraints differently. Not "you should learn X" but "here's why X is the thing standing between you and three things you want."
- Fewer, stronger leverage points beat a long list. 3 high-confidence findings are better than 10 speculative ones.
- The development path must be concrete enough to start tomorrow. Not "learn finance" but "read \[specific book\], then apply the framework to \[specific project\], then \[specific next step\]."
- The anti-leverage list is as valuable as the leverage list. Knowing what NOT to invest in saves as much time as knowing what to invest in.
- Be direct. This is a strategic tool, not encouragement. If the vault shows someone avoiding the obvious leverage point, say so.
- The best leverage points feel slightly uncomfortable. If every suggestion is exciting and fun, you're probably optimizing for engagement, not impact.
- The Surprising One should genuinely surprise. It should come from a domain that seems unrelated until you see the connection to the constraint. This is where the skill earns its keep.

---

## Related Commands

- [[Prompt - Money|/money]] — Revenue advisor that diagnoses the revenue system and surfaces opportunities
- [[Prompt - Ideas|/ideas]] — Generates a comprehensive list of ideas across multiple domains from vault patterns
- [[Prompt - Compound|/compound]] — Answers the same question across three time periods to show context compounding