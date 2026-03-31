---
title: "Prompt - Stranger"
created: 2026-03-06
description: "Prompt - Stranger"
tags:
  - "vault-command"
related:
  - "[[Prompt - Ghost]]"
  - "[[Prompt - Challenge]]"
  - "[[Prompt - Context]]"
---
## Stranger — A Portrait from the Outside

Write a portrait of who the vault's author is, as seen by someone reading this vault cold, with no prior context. The stranger sees everything in the vault but knows nothing else. What picture would they form?

**Usage:**`/stranger`

---

## Step 1: Structural Survey

Before reading any content, map the vault's shape. Structure reveals priorities before words do.

```bash
obsidian vault                                          # Total files, folders, size — the vital signs
obsidian orphans total                                  # Count orphans
obsidian deadends                                       # Notes with no outgoing links
obsidian unresolved counts verbose format=json          # Things referenced but never created, ranked
obsidian tags counts sort=count format=json | jq '.[0:20]'  # Top 20 themes, machine-readable
obsidian folders                                        # Folder structure
```

Record:

- Total note count, folder count, vault size
- Number of orphans and deadends (ratio to total = isolation metric)
- Most-used tags (top 15-20) with counts
- Number of unresolved links (highest-count ones reveal the biggest mental gaps)
- Folder structure and relative sizes (use `obsidian folder path="X" info=files` for specific folders)

This structural data is raw material for the portrait. Do not skip it.

---

## Step 2: Read the Content

### Context Files

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

### Daily Notes

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 14-21 days
```

### Essays and Published Work

```bash
obsidian search query="" path="Essays"
obsidian read file="<each essay found>"
```

### Follow the Graph

For the 5 most-linked notes in the vault:

```bash
obsidian backlinks file="<note>" counts format=json  # Ranked connections — which notes are the gravitational centers
obsidian links file="<note>" format=json
```

---

## Step 3: Seven Forced Intermediate Analyses

Complete ALL seven analyses before composing the portrait. Write out each one explicitly. These are the raw materials. Skipping them leads to a shallow portrait.

### Analysis 1: Topic Frequency Map

What topics appear most often across all vault material? Rank the top 10-15 by raw frequency. Note which topics appear in daily notes vs. context files vs. essays. A topic that appears in daily notes but not context files is lived but not yet formalized. The reverse means it's theorized but not practiced.

### Analysis 2: Stated vs. Revealed Priorities

| Stated Priority | Evidence of Stated | Actual Time/Energy (from daily notes) | Gap? |
| --- | --- | --- | --- |
| ... | Context file X | Mentioned X times in Y days | Yes/No |

Stated priorities come from context files. Revealed priorities come from what actually gets written about, worked on, and returned to in daily notes. Where these diverge is the most interesting data in the vault.

### Analysis 3: Emotional Frequency Analysis

Scan daily notes for emotional language. What emotions appear most? What triggers them? What is conspicuously absent?

Categories to track:

- Excitement/energy (what produces it?)
- Frustration/friction (what causes it?)
- Satisfaction/pride (what earns it?)
- Anxiety/worry (what drives it?)
- Absence (what emotions are never expressed?)

### Analysis 4: Relationship Map

Who appears in the vault? How often? In what context? Who is mentioned with warmth, who with obligation, who with aspiration? Build a rough map of the social world as the vault reveals it.

### Analysis 5: Recurring Questions

What questions keep appearing across daily notes and context files? Questions asked once are curiosity. Questions asked repeatedly are obsessions. List the top 5-7 recurring questions.

### Analysis 6: Writing Style Fingerprint

From essays and daily notes, characterize the writing:

- Sentence length tendencies
- Use of metaphor and analogy
- Degree of abstraction vs. concreteness
- Characteristic vocabulary (words used repeatedly)
- What is never said (euphemisms, avoidances, topics approached indirectly)

### Analysis 7: Conspicuous Absences

What is NOT in the vault that you would expect from someone with this profile? What topics, people, activities, or emotions are missing? Absences are data. A vault that talks about work constantly but never mentions rest is telling you something. A vault that mentions a child but never describes time together is telling you something different.

---

## Step 4: Compose the Portrait

Written in third person throughout. The stranger is describing someone they have never met, based only on what they read. Shift to "you" only in the final section.

### Section 1: First Impression

What would a stranger notice first about this vault and its author? The dominant energy, the obvious preoccupations, the immediate personality that comes through. Keep this to 2-3 paragraphs. This is a first impression, not a summary.

### Section 2: What They Actually Care About

Not what they say they care about. What the vault's weight distribution reveals. Where does attention actually go? What gets the most ink, the most links, the most returns? Where is the gravitational center? Use evidence from Analysis 1 and 2.

### Section 3: What They Are Building Toward

Based on the trajectory visible across context files and daily notes, what is this person building? Not just the stated projects, but the shape of the life they seem to be constructing. What does the vault suggest they want to be true in 2-3 years?

### Section 4: The Patterns They Cannot See

This is the hardest and most valuable section. What patterns are visible from outside that would be invisible from inside? The stranger can see things the author can't because the stranger has no ego invested in the narrative.

Six pattern types to check:

1. **Contradiction patterns**: Beliefs held simultaneously that don't cohere
2. **Avoidance patterns**: Topics or actions consistently skirted
3. **Repetition patterns**: The same idea recycled under different names without deepening
4. **Projection patterns**: Attributing to external circumstances what originates internally
5. **Narrative patterns**: Stories told about self that the evidence doesn't fully support
6. **Blind spot patterns**: Entire domains of life or thought that are simply absent

Minimum requirement: at least 2 patterns that are uncomfortable and at least 2 that are admiring. A stranger portrait that is all critique or all praise has failed.

### Section 5: The Unasked Question

Shift to second person ("you") for this section only. Based on everything in the vault, what is the one question this person has never asked but should? The question that, if answered honestly, would change the most about how they operate. This is not a rhetorical device. It should be a genuinely unasked question, one that the vault's own evidence points toward but that never appears.

---

## Self-Verification Checklist

Before outputting, verify:

- All 7 intermediate analyses were completed explicitly
- Portrait contains at least 2 uncomfortable observations
- Portrait contains at least 2 admiring observations
- Third person is used throughout except Section 5
- Every claim in the portrait traces back to specific vault evidence
- The Unasked Question is genuinely unasked (search the vault to confirm)
- The portrait would be recognizable to the author but contains things they haven't articulated to themselves

---

## Anti-Patterns

**1\. The Flattering Portrait**  
Making the subject sound impressive, visionary, or admirable without substance. A stranger doesn't flatter. They observe.

**2\. The Therapy Portrait**  
Turning the portrait into a psychological evaluation with advice. The stranger describes what they see. They don't prescribe.

**3\. The Summary Portrait**  
Simply listing what's in the vault. A portrait is a synthesis, not a table of contents. It reveals character, not content.

**4\. The Generic Portrait**  
Could describe any ambitious person. Every observation should be specific to THIS vault and THIS person.

**5\. The Judgmental Portrait**  
Moralizing about choices, priorities, or patterns. The stranger is perceptive, not righteous.

**6\. The Claude Portrait**  
Using Claude's characteristic framing: balanced observations, diplomatic hedging, "it's worth noting" structures. The stranger is direct.

---

## Output Format

**STRANGER: Portrait from the Outside**  
**Vault surveyed:** \[note count, tag count, date range of daily notes\]  
**Analysis depth:** \[number of notes read, backlink hops followed\]

---

\[Section 1: First Impression\]

\[Section 2: What They Actually Care About\]

\[Section 3: What They Are Building Toward\]

\[Section 4: The Patterns They Cannot See\]

\[Section 5: The Unasked Question\]

---

## Output Guidelines

- The portrait should feel like being seen by someone perceptive and unflinching.
- Cite specific vault evidence for every claim.
- The portrait is only valuable if it contains things the author already knows AND things they don't. Pure novelty is as useless as pure summary.
- The Unasked Question should land. If it doesn't cause a pause, it's not the right question.
- Do not soften observations to be polite. The stranger has no relationship to protect.

---

## Related Commands

- [[Prompt - Ghost|/ghost]] — Answers a question as the vault's author, drawing only on vault evidence
- [[Prompt - Challenge|/challenge]] — Pressure-tests current beliefs using the vault's own history
- [[Prompt - Context|/context]] — Builds comprehensive context about the user by reading vault files, backlinks, and daily notes