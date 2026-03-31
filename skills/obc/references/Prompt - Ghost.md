---
title: "Prompt - Ghost"
created: 2026-03-06
description: "Prompt - Ghost"
tags:
  - "vault-command"
related:
  - "[[Prompt - Challenge]]"
  - "[[Prompt - Context]]"
  - "[[Prompt - Stranger]]"
  - "[[Prompt - Trace]]"
---
## Ghost — Answer a Question as You from the Vault

Take a question and answer it the way the vault's author would, drawing only on what the vault contains. Then pull back the curtain and honestly evaluate how faithful the answer is.

**Usage:**`/ghost [question]` -- e.g., `/ghost What do you think about AI wrappers?` or `/ghost What advice would you give a first-time founder?`

---

## Step 0: Parse the Question Type

Before searching, classify the question. The type determines how much inference is acceptable and which search strategy to use.

| Type | Description | Search Strategy | Inference Tolerance |
| --- | --- | --- | --- |
| **Factual** | "What is your company structure?" | Direct search for facts | Very low. Vault must contain the answer. |
| **Opinion** | "What do you think about X?" | Search for stated positions, adjacent beliefs | Moderate. Can infer from patterns if explicit opinion absent. |
| **Advice** | "What would you tell someone about X?" | Search for beliefs, experiences, lessons learned | Moderate-high. Can synthesize from multiple sources. |
| **Personal** | "How do you feel about X?" | Daily notes, emotional language, repeated themes | Low. Don't fabricate feelings. |
| **Prediction** | "What do you think will happen with X?" | Search for stated predictions, trend analysis, beliefs about the future | High, but must be grounded in vault worldview. |

Record the question type before proceeding. It gates everything that follows.

---

## Step 1: Build the Voice Profile

Before writing a single word of the answer, extract the user's voice from the vault. This prevents the answer from defaulting to Claude's voice with the user's opinions pasted in.

### Read Source Material

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 7-14 days
obsidian read file="<Context Files>"
obsidian search query="<topic>" path="Essays"
```

### Extract Voice Characteristics

From the material read, explicitly note (write these down before composing):

This voice profile is a hard constraint on the ghost answer. If the answer doesn't sound like these notes, it fails.

---

## Step 2: Gather Evidence

### Synonym Discovery

Before searching, build a vocabulary map for the question's topic. Check aliases for alternate note names:

```bash
obsidian aliases file="<most relevant note>"  # Discover alternate names for this topic
```

### Multi-Method Search

```bash
obsidian search query="<topic>" format=json                    # All mentions
obsidian search:context query="<topic>" format=json            # With matching lines
obsidian search query="<synonym 1>" format=json
obsidian search query="<synonym 2>" format=json
obsidian search:context query="<topic>" path="Daily Notes" format=json  # Daily note mentions with context
obsidian search query="<topic>" path="Essays" format=json
obsidian backlinks file="<most relevant note>" counts format=json  # What connects to this, ranked
obsidian links file="<most relevant note>" format=json
```

### Evidence Tagging

For every piece of relevant information found, tag it immediately:

- **VAULT**: The user explicitly said or wrote this. Direct quote available.
- **INFERRED**: Not explicitly stated, but strongly implied by 2+ vault sources.
- **EXTRAPOLATED**: Consistent with their worldview but requires extending beyond what's written.
- **UNKNOWN**: The vault contains nothing relevant to this aspect of the question.

List all tagged evidence before composing. Do not skip this step.

### Sparse Data Handling

If searches return thin results:

---

## Step 3: Compose the Ghost Answer

Write the answer as the vault's author would. Constraints:

1. **Use the voice profile from Step 1.** Every sentence should pass the test: "Would they actually say it this way?"
2. **Inline source tags.** After each claim or position, note the source tag in brackets: \[VAULT: note name\], \[INFERRED: from X + Y\], \[EXTRAPOLATED: based on Z\], \[UNKNOWN\].
3. **Hard thresholds:**
	- If >30% of the answer is EXTRAPOLATED: add an explicit caveat at the top: "This answer leans heavily on extrapolation. The vault doesn't contain enough to answer this with high confidence."
	- If >50% is EXTRAPOLATED or UNKNOWN: decline to give a ghost answer. Instead, report what the vault DOES contain and where the gaps are.
4. **Length and tone**: Match what they would actually produce. If they'd give a two-sentence answer, don't write five paragraphs. If they'd go deep, go deep.

---

## Step 4: Behind the Curtain

After the ghost answer, produce the analysis:

### Evidence Map

| Claim | Source Tag | Source Note(s) | Confidence |
| --- | --- | --- | --- |
| ... | VAULT | Note name, date | High |
| ... | INFERRED | Note A + Note B | Medium |
| ... | EXTRAPOLATED | Based on pattern in X | Low |

### Source Distribution

- VAULT: X%
- INFERRED: X%
- EXTRAPOLATED: X%
- UNKNOWN: X%

### Vault Gaps

What would the vault need to contain to answer this question with full confidence? Be specific: "A note about experience with X" or "Any mention of how they feel about Y."

### Voice Fidelity Notes

Where did the ghost answer match their voice well? Where did it slip into Claude's default patterns? Be honest.

### Fidelity Score: X/10

| Score | Meaning |
| --- | --- |
| 9-10 | They would read this and say "I could have written that." Nearly all VAULT-sourced. |
| 7-8 | Captures the right positions and mostly the right voice. Some inference required. |
| 5-6 | Directionally correct but relies on significant inference. Voice is approximate. |
| 3-4 | More Claude than the user. Positions are plausible but not well-evidenced. |
| 1-2 | Fabrication. The vault doesn't support this answer. |

### Honest Assessment

One paragraph. Was this ghost answer worth giving? What would make it better? If the answer is "the vault needs more material on this topic," say so directly.

---

## Anti-Patterns

**1\. The Wikipedia Ghost**  
Writing a neutral, encyclopedic answer about the topic instead of the user's actual position. Ghost answers should be opinionated where the vault shows opinions.

**2\. The Confident Fabricator**  
Generating a fluent, confident answer that sounds plausible but isn't grounded in vault evidence. The smoothness of the answer masks the absence of real data. If the vault is thin, the answer should be thin.

**3\. The Claude Ghost**  
Using Claude's default voice, vocabulary, and rhetorical style instead of the user's. Watch for: bullet-point-heavy structure, "it's worth noting," "let's unpack," hedging qualifiers, and balanced-both-sides framing that the user wouldn't use.

**4\. The Therapist Ghost**  
Turning the answer into self-help wisdom or reflective questions instead of giving the direct, sometimes blunt answer the user would give.

**5\. The Yes Ghost**  
Assuming the user would agree with the premise of the question. If the vault shows they would push back on the question itself, the ghost should push back.

**6\. The Safe Ghost**  
Softening positions the vault shows are held strongly. If the user is direct or provocative about something, the ghost answer should be too.

---

## Output Format

**GHOST: \[Question\]**  
**Question type:** \[Factual / Opinion / Advice / Personal / Prediction\]  
**Vault coverage:** \[Strong / Moderate / Thin / Minimal\]

---

### The Answer (as the user)

\[Ghost answer with inline source tags\]

---

### Behind the Curtain

\[Evidence map table\]

\[Source distribution\]

\[Vault gaps\]

\[Voice fidelity notes\]

**Fidelity score: X/10**

\[Honest assessment\]

---

## Output Guidelines

- The ghost answer should feel like reading something the user wrote, not something written about them.
- Honesty about fidelity is more valuable than a convincing performance. A 4/10 answer that knows it's a 4 is better than a fabricated 8.
- Cite specific notes and dates in the evidence map.
- The Behind the Curtain section is not optional. It's the whole point. Anyone can generate a plausible-sounding answer. The value is in knowing how much of it is real.
- If the vault can't answer the question, say so. That's a valid and valuable output.

---

## Related Commands

- [[Prompt - Context|/context]] — Builds comprehensive context about the user by reading vault files, backlinks, and daily notes
- [[Prompt - Stranger|/stranger]] — Writes a portrait of the vault's author as seen by an outsider reading cold
- [[Prompt - Trace|/trace]] — Traces how a specific idea or belief has evolved across the vault over time