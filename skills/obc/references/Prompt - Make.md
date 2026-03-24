---
title: "Prompt - Make"
created: 2026-03-06
description: "Prompt - Make"
tags:
  - "vault-command"
related:
  - "[[Prompt - Ideas]]"
  - "[[Prompt - Graduate]]"
  - "[[Prompt - Money]]"
  - "[[Prompt - Synthesize]]"
  - "[[Prompt - Audit]]"
  - "[[Prompt - Evolve]]"
---
## Make — What in Your Vault Should Become Something the World Sees?

Scan the vault broadly for ideas, perspectives, and experiences that have accumulated enough depth and originality to become real work. Surface what's ready, what's almost ready, and what natural forms each could take.

**Usage:**`/make` (general scan) or `/make [domain]` (focused on a specific area)

---

## Vault Access

If the [obsidian CLI](https://help.obsidian.md/cli) is available, use it for all vault reads and searches. It's significantly faster than filesystem tools and gives the agent direct access to backlinks, tags, search, and file metadata in real time. All `obsidian` commands below assume the CLI. If it's not available, fall back to reading files directly from the vault directory.

---

## What Counts as a Candidate

A candidate is NOT:

- An idea that just appeared once (that's too thin)
- A connection between two notes (that's [[Prompt - Connect|/connect]])
- An unnamed pattern implied by the vault (that's [[Prompt - Emerge|/emerge]])
- A brainstorm of possible projects (that's [[Prompt - Ideas|/ideas]])
- A daily note insight that needs promotion (that's [[Prompt - Graduate|/graduate]])
- An idea's evolution over time (that's [[Prompt - Trace|/trace]])

A candidate IS:

The test: Could someone sit down today and draft something from what the vault already contains? If the answer is "almost, with some focused work," it's a candidate. If the answer is "they'd need to start from scratch," it's not.

---

## Step 1: Density Detection

Find topics where sustained attention has created accumulated depth.

```bash
obsidian tags counts sort=count format=json | jq '.[0:20]'        # Top 20 themes with counts
obsidian search query="<top tag>" path="Daily Notes" format=json  # How often does this appear in daily notes
```

For each high-frequency tag or theme:

```bash
obsidian search:context query="<theme>" format=json                    # Where it appears, with matching lines
obsidian backlinks file="<theme note if it exists>" counts format=json  # How connected it is
obsidian wordcount file="<theme note if it exists>"                    # Actual word count = material density
```

### What to Look For

- Topics mentioned 10+ times across 5+ separate days
- Notes that keep getting longer as thinking accumulates
- Themes that appear in both daily notes and context files
- Topics with multiple backlinks forming a cluster

### What This Catches

Raw material. A topic with density has enough written material that a first draft could be assembled from existing vault content. Density alone doesn't mean it's worth making, but it means the work of creation is partially done.

**Track:** For each dense topic, note the approximate word count across all mentions, number of distinct days it appears, and whether it spans multiple domains.

---

## Step 2: Originality Detection

Find perspectives that diverge from conventional thinking and would add something to public discourse.

```bash
obsidian search:context query="most people think"
obsidian search:context query="the problem with"
obsidian search:context query="what people miss"
obsidian search:context query="actually"
obsidian search:context query="wrong about"
obsidian search:context query="nobody talks about"
obsidian search:context query="counterintuitive"
```

Also scan for notes where strong positions live. Use tags, backlinks, and search to find the notes in your vault that contain developed thinking about your work, projects, or worldview:

```bash
obsidian search:context query="I believe"
obsidian search:context query="my position"
obsidian tags counts sort=count   # find where thinking is concentrated, then read those notes
```

### What to Look For

- Claims that push against mainstream consensus
- Frameworks or mental models developed from direct experience
- Observations from an unusual vantage point
- Beliefs held with high confidence that most people would disagree with
- Contrarian positions backed by real experience, not just opinion

### What This Catches

Discourse value. An original perspective means the work would add something new to whatever conversation it enters. Without originality, even well-written work is redundant.

**Track:** For each original perspective, note what the conventional view is and how this vault's view differs.

---

## Step 3: Narrative Detection

Find stories, arcs, and turning points documented over time that have a beginning and a change.

```bash
obsidian search query="realized" path="Daily Notes"
obsidian search query="changed my mind" path="Daily Notes"
obsidian search query="used to think" path="Daily Notes"
obsidian search query="turning point" path="Daily Notes"
obsidian search query="before and after" path="Daily Notes"
obsidian search query="learned" path="Daily Notes"
obsidian search query="shifted" path="Daily Notes"
```

For promising threads, trace the full arc:

```bash
obsidian search query="<topic>" path="Daily Notes"
obsidian read file="YYYY-MM-DD"   # read key moments in the arc
```

### What to Look For

- A belief or approach that changed, with the before and after documented
- A project or relationship with a clear arc (challenge, struggle, resolution or ongoing tension)
- Experiences where the vault captured the journey, not just the conclusion
- Moments of genuine surprise or recognition documented in real time

### What This Catches

Story. The most compelling work is often not "here's what I think" but "here's what happened to me and what it revealed." Narrative candidates have the bones of a story already documented.

**Track:** For each narrative, note the rough arc (beginning, change, current state) and whether the emotional texture is preserved in the vault entries.

---

## Step 4: Tension Detection

Find unresolved questions where the vault contains substance on both sides.

```bash
obsidian search:context query="on one hand"
obsidian search:context query="not sure"
obsidian search:context query="torn between"
obsidian search:context query="the tension"
obsidian search:context query="both true"
obsidian search:context query="paradox"
obsidian search:context query="tradeoff"
```

Also check for items marked as uncertain or evolving in context files:

```bash
obsidian search:context query="questioning"
obsidian search:context query="evolving"
```

### What to Look For

- Questions that keep recurring because they resist simple answers
- Positions held simultaneously that create productive tension
- Tradeoffs that have been lived with and explored from multiple angles
- Problems where the vault documents the experience of sitting with ambiguity

### What This Catches

Productive ambiguity. The best essays and conversations often explore tensions rather than resolve them. A tension with substance on both sides is more compelling than a neat conclusion, because it invites the audience into the thinking rather than handing them an answer.

**Track:** For each tension, note what both sides are and whether the vault provides evidence/experience for each side.

---

## Step 5: Resonance Detection

Find topics with evidence that others care, that "this matters to me" could become "this should exist in the world."

```bash
obsidian search:context query="people keep asking"
obsidian search:context query="conversation about"
obsidian search:context query="someone said"
obsidian search:context query="response to"
obsidian search:context query="resonated"
obsidian search:context query="they asked"
obsidian search:context query="DM"
```

Also check for topics that generated external engagement:

```bash
obsidian search query="podcast" path="Daily Notes"
obsidian search query="thread" path="Daily Notes"
obsidian search query="posted" path="Daily Notes"
obsidian search query="feedback" path="Daily Notes"
```

### What to Look For

- Topics where conversations with others generated energy or follow-up
- Ideas that provoked strong reactions (agreement or disagreement)
- Questions others keep asking that the vault has developed answers for
- Themes from conversations that sparked deeper thinking
- Posts or threads that got traction and could be expanded

### What This Catches

Audience signal. Resonance means someone else has already validated that this topic matters. It doesn't guarantee good work, but it reduces the risk of making something into a void.

**Track:** For each resonant topic, note the evidence of external interest and who cared.

---

## Step 6: Cross-Reference and Deduplicate

### Check Against Already-Published Work

```bash
obsidian files folder="Essays"
obsidian search query="<candidate topic>" path="Essays"
```

If a candidate topic has already been published, discard it unless the vault contains substantial new thinking since publication.

### Check Against Previous /make Runs

```bash
obsidian search query="/make" path="Daily Notes"
```

If prior runs exist:

- Which candidates were surfaced before and acted on? (note what became of them)
- Which were surfaced and ignored? (either drop them or note "previously surfaced on \[date\], not acted on")
- Which are new since the last run?

### Merge Across Detection Methods

A topic that appears in multiple detection methods is a stronger candidate. Combine findings:

- If a topic has density AND originality, it has both material and a reason to exist publicly
- If a topic has narrative AND tension, it has story and depth
- If a topic has resonance AND any other signal, there's external validation on top of internal readiness

---

## Step 7: Score and Assess

### Readiness Scoring

Score each candidate on four dimensions (1-5 each):

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| **Depth** | A few scattered mentions | Several entries, some developed | Extensive material across multiple notes |
| **Originality** | Common observation | Somewhat distinctive angle | Genuinely novel perspective backed by experience |
| **Clarity** | Vague, hard to articulate | Core idea identifiable but fuzzy | Core idea articulable in 1-2 clear sentences |
| **Urgency** | Mentions decelerating or dormant | Steady | Accelerating, mentions increasing in frequency and intensity |

**Total: /20**

### Tiers

---

## Step 8: Natural Form Assessment

For each candidate scoring 11+, consider which forms it could naturally take. Present multiple options with reasoning, never a single prescribed format.

### Diagnostic Questions

**Essay / Long-form**

- Is there a single core argument or insight that could sustain 1,500-3,000 words?
- Does the vault contain enough supporting evidence and examples?

**Short Post / Provocation**

- Is the core idea sharp enough to land in 280 characters or a few paragraphs?
- Would brevity serve the idea better than elaboration?

**Documentary / Visual**

- Is there a visual dimension to the story (places, people, processes)?
- Would showing be more powerful than telling?

**Podcast Conversation**

- Is this topic better explored in dialogue than monologue?
- Who would be the ideal conversation partner? (suggest specific people with reasoning)

**Fiction / Speculative**

- Does the idea resist direct statement and work better through story?
- Is there a "what if" version that would be more compelling than a "what is" version?

**Series / Ongoing**

- Is this too large for a single work? Would it benefit from being explored in parts over time?
- Is the thinking still actively evolving, making a series more honest than a definitive piece?

Always present at least 2-3 forms for each candidate. Note which form the vault's existing material most naturally supports vs. which form might be most impactful.

---

## Output Format

**MAKE REPORT**  
**Scope:** \[General / Domain-focused\]  
**Detection methods run:** \[list\]  
**Candidates found:** \[number\]  
**New since last run:** \[number, or "First run"\]

---

### Ready (16-20)

**Candidate \[#\]: \[Title\]**

**Core idea:** \[1-2 sentences stating what this work would be about\]

**Score:** Depth: X | Originality: X | Clarity: X | Urgency: X | **Total: X/20**

**Detection methods:** \[Which methods surfaced this and what they found\]

**Evidence:**

- \[Specific note, date, quote\] -- \[why it matters\]
- \[Another note, date, quote\] -- \[why it matters\]
- \[Pattern or cluster\] -- \[why it matters\]

**Natural forms:**

- \[Form 1\]: \[Why this form works for this material. What already exists that supports it.\]
- \[Form 2\]: \[Why this form works. How it differs from Form 1.\]
- \[Form 3\]: \[If applicable\]

**What is still missing:** \[Specific gaps, not vague. E.g., "needs a concrete example of X in action" or "the counterargument to Y hasn't been explored"\]

---

\[Same format as Ready, with emphasis on "What is still missing"\]

---

### Developing (6-10)

\[Abbreviated format: Core idea, score, what would need to accumulate\]

---

### Synthesis

**Strongest candidate:** \[Which one and why, in 2-3 sentences\]

**The Surprise:** \[The candidate the user probably wouldn't identify themselves. Why it's worth attention despite not being top of mind.\]

**The Thread:** \[If a meta-theme connects multiple candidates, name it. What does it say about what this vault is really about?\]

**Conspicuous Absences:** \[Domains or topics with lots of vault activity but no viable candidates. Why? Is the thinking too early, too private, or too scattered?\]

---

## Anti-Patterns

**1\. The Content Calendar**  
Suggesting publishing schedules, cadences, or "you should post X per week." This is a scouting report, not a production plan.

**2\. The Title Generator**  
Generating headlines, hooks, or clickbait framings. The output is about what exists and what it could become, not how to market it.

**3\. The Format Prescriber**  
Assigning a single "best" format to each candidate. Always present multiple forms. The creator decides.

**4\. The Depth Fabricator**  
Inflating thin topics to fill the report. If the vault has three sentences on a topic, it's not a candidate no matter how interesting the topic is. Be honest about what's actually there.

**5\. The Originality Inflator**  
Dressing up common observations as unique perspectives. "Focus is important" is not an original insight. "Here's why I cancelled all recurring meetings and what happened" might be.

**7\. The Everything-Is-Ready Optimist**  
Inflating readiness scores to make the report feel productive. Most topics in any vault are Developing at best. A report with zero Ready candidates is an honest report.

**8\. The Duplicate**  
Resurfacing what [[Prompt - Emerge|/emerge]], [[Prompt - Ideas|/ideas]], [[Prompt - Graduate|/graduate]], or [[Prompt - Trace|/trace]] would already cover. This command's territory is specifically "what should become something the world sees" and the assessment of readiness. If another command handles it better, defer.

---

## Output Guidelines

- Every candidate must trace back to specific vault evidence. No evidence, no candidate.
- Cite exact notes, dates, and quotes. The user should be able to verify every claim.
- Be ruthlessly honest about readiness. A thin report with one genuine Ready candidate is better than a padded report with five inflated ones.
- "What is still missing" should be specific enough to act on. Not "needs more depth" but "needs a concrete example of how this played out" or "the vault discusses the benefits but never addresses the obvious counterargument that X."
- This should feel like a scouting report from someone who read the whole vault, not a content strategy deck.
- The Surprise finding is mandatory. There should always be one candidate the user wouldn't have identified themselves.

---

## Related Commands

- [[Prompt - Ideas|/ideas]] — Generates a comprehensive list of ideas across multiple domains from vault patterns
- [[Prompt - Graduate|/graduate]] — Extracts ideas from daily notes and promotes them to standalone notes
- [[Prompt - Money|/money]] — Revenue advisor that diagnoses the revenue system and surfaces opportunities