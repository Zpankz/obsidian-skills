---
title: "Prompt - Compound"
created: 2026-03-06
description: "Prompt - Compound"
tags:
  - "vault-command"
related:
  - "[[Prompt - Trace]]"
  - "[[Prompt - Emerge]]"
  - "[[Prompt - Leverage]]"
  - "[[Prompt - Evolve]]"
---
## Compound — Answer the Same Question Across Time to Show Context Compounding

Answer the same question three times: once with only the context available at an early point, once at a middle point, and once with today's full vault. The difference in answer quality demonstrates how accumulated context compounds over time.

**Usage:**`/compound [question]` -- e.g., `/compound How should I think about hiring?` or `/compound What's the right podcast format?`

---

## Step 0: Question Validation

Not every question benefits from this analysis. Before proceeding, classify the question:

**Good questions for /compound:**

- Questions where the answer depends on personal context (preferences, history, relationships, domain knowledge)
- Questions where more context would change the answer, not just lengthen it
- Questions about strategy, approach, or decision-making

**Bad questions for /compound:**

- Factual questions with stable answers ("What's our office address?")
- Questions where the answer is the same regardless of context
- Questions about topics the vault has barely touched

If the question is unsuitable, say so and suggest a better one. Don't force the exercise.

---

## Step 1: Map the Vault's Temporal Shape

Before selecting time periods, understand when context was actually accumulating.

### Daily Note Density

```bash
obsidian search query="" path="Daily Notes"  # get a list of all daily notes
```

Map the density: when did daily notes start? Are there gaps? When did writing become regular?

### Context File Timeline

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

For each context file, note:

- Any internal date references (when was it created? when was it last meaningfully updated?)
- Confidence markers and their distribution (more `[solid]` markers suggest maturity)
- References to other notes (backlink density as a proxy for integration)

### Backlink Presence from Dated Notes

```bash
obsidian backlinks file="<context file>" counts format=json  # which notes reference this, ranked by frequency
```

This reveals when a context file became integrated into daily thinking vs. sitting as an isolated document.

### Multi-Signal Date Availability

Build a timeline using all available signals:

- Daily note dates (explicit)
- Internal date references in context files
- Modification dates on key notes
- First appearance of key topics in daily notes
- Creation dates of context files themselves

---

## Step 2: Select Three Time Periods

### Period Selection Criteria

Choose periods at inflection points where relevant context roughly doubled, not at fixed intervals. The question determines what counts as "relevant context."

For the given question:

1. **Search for relevant material:**

```bash
obsidian search query="<question topic>" path="Daily Notes" format=json  # When and where this topic appears
obsidian search:context query="<question topic>" format=json             # With matching lines
obsidian search query="<synonym 1>" format=json
obsidian search query="<synonym 2>" format=json
```

1. **Map when relevant material accumulated:**
	- When did the first relevant note appear?
	- When did the relevant context file get created or start covering this topic?
	- When did daily notes start regularly touching this topic?
2. **Identify inflection points:**
	- **Period A (Early):** The vault's first real engagement with this topic. Minimal context.
	- **Period B (Middle):** A meaningful inflection, the point where an agent would have started giving noticeably better answers.
	- **Period C (Now):** Today. Full vault available.

If the vault doesn't have enough temporal depth on this topic, say so. Don't fabricate historical periods.

---

## Step 3: Context Inventory for Each Period

For each period, list exactly what an agent would have access to. Be exhaustive.

### Period A: \[Date or date range\]

**Available context:**

- Daily notes: \[list which ones exist and are relevant\]
- Context files: \[which existed? what did they contain on this topic?\]
- Essays: \[any relevant ones?\]
- Other notes: \[anything else relevant?\]
- **Total relevant data points:** \[number\]

### Period B: \[Date or date range\]

**Available context:**

- Daily notes: \[expanded list\]
- Context files: \[what's new or changed since Period A?\]
- Essays: \[any new ones?\]
- Other notes: \[anything new?\]
- **Total relevant data points:** \[number\]
- **What's new since Period A:** \[specific additions\]

### Period C: Now

**Available context:**

- \[Full current inventory\]
- **Total relevant data points:** \[number\]
- **What's new since Period B:** \[specific additions\]

---

## Step 4: Record Predictions

Before generating answers, the agent records its prediction:

> **Prediction:** Based on the context inventories above, I expect the answer quality to change in these specific ways between periods:
> 
> - Period A to B: \[predicted change\]
> - Period B to C: \[predicted change\]
> - Biggest expected improvement dimension: \[specificity / actionability / personal relevance / cross-domain connections\]

This prevents confabulation. The prediction is checked against actual results in Step 6.

---

## Step 5: Generate Three Answers

### Constraints

1. **Hard context boundaries.** When writing the Period A answer, you may ONLY use information that existed at that time. No knowledge leakage from later periods. This is the hardest constraint and the most important one.
2. **Equal length.** All three answers should be approximately the same length (within 20%). This isolates quality from volume.
3. **Same voice.** All three answers should be written in the vault author's voice.
4. **Tag sources.** Each claim tagged with \[VAULT: note, date\] so leakage is verifiable.

### Period A Answer: \[Date\]

*Context available: \[brief summary\]*

\[Answer using only Period A context\]

### Period B Answer: \[Date\]

*Context available: \[brief summary\]*

\[Answer using only Period A + B context\]

### Period C Answer: Now

*Context available: \[brief summary\]*

\[Answer using full vault\]

---

## Step 6: Self-Verification

### Anachronism Check

Reread the Period A answer. Does it contain any knowledge, terminology, or perspectives that only appeared later? If yes, flag it and correct.

```bash
obsidian search query="<suspicious term from Period A answer>" path="Daily Notes"  # when did this term first appear?
```

### Prediction Check

Compare the actual answer differences against the predictions from Step 4. Where was the prediction right? Where was it wrong? What does the discrepancy reveal?

---

## Step 7: Compounding Scorecard

### Scoring Table

| Dimension | Period A | Period B | Period C | Compounding? |
| --- | --- | --- | --- | --- |
| **Specificity** | /10 | /10 | /10 | Yes/No |
| **Actionability** | /10 | /10 | /10 | Yes/No |
| **Personal relevance** | /10 | /10 | /10 | Yes/No |
| **Cross-domain connections** | /10 | /10 | /10 | Yes/No |

Definitions:

- **Specificity**: Does the answer reference specific projects, people, decisions, or experiences? Or is it generic advice?
- **Actionability**: Could you act on this answer today? Or is it abstract?
- **Personal relevance**: Does the answer account for specific constraints, values, and context? Or could it apply to anyone?
- **Cross-domain connections**: Does the answer draw on multiple areas of the vault to produce a richer answer?

### Compounding Narrative

In 2-3 paragraphs: What changed between the answers? Where did the additional context produce the biggest improvement? Was the improvement gradual or did it jump at a specific inflection point?

### Null Result Handling

If the answers didn't meaningfully improve across periods, that's the finding. Possible reasons:

- The question isn't context-sensitive (any agent could answer it)
- The vault's relevant context didn't actually grow
- The context grew but in ways that don't affect this question

Don't force a compounding narrative if the data doesn't show it. Honest null results are more valuable than fabricated progress.

### The Compounding Rate

At the current rate of vault growth, estimate: how much better would the answer be in 6 months? What specific context additions would produce the biggest improvement?

---

## Anti-Patterns

**1\. The Volume Illusion**  
Making later answers longer and calling that improvement. Length is not quality. All three answers must be the same length.

**2\. The Knowledge Leak**  
Using information from Period C when writing Period A or B. This is the most common failure mode.

**3\. The Forced Compounding**  
Manufacturing improvement when the vault doesn't show it.

**4\. The Generic Early Answer**  
Making Period A deliberately vague or bad to make the improvement look more dramatic.

**5\. The Summary Trap**  
Turning the three answers into summaries of what the vault contains at each period, rather than genuine attempts to answer the question.

**6\. The Cheerleader**  
Celebrating every improvement uncritically. Some improvements are trivial. The scorecard should distinguish between meaningful and cosmetic improvements.

---

## Output Format

**COMPOUND: \[Question\]**  
**Vault temporal range:** \[earliest to latest relevant note\]  
**Periods selected:** \[Period A date, Period B date, Period C (now)\]  
**Relevant data points:** A: \[n\], B: \[n\], C: \[n\]

---

\[Period A Answer\]

\[Period B Answer\]

\[Period C Answer\]

---

\[Self-verification results\]

\[Compounding Scorecard table\]

\[Compounding narrative\]

\[The Compounding Rate\]

---

## Output Guidelines

- The three answers are the core of this command. They must be genuine attempts to answer the question, not demonstrations of what the vault contains.
- Equal length is a hard constraint. It prevents the lazy version where later answers are just longer.
- Knowledge leakage is the thing that ruins this exercise. Be vigilant about it.
- The null result is a valid finding. If compounding isn't happening for a topic, that's useful information about what the vault needs.
- Cite specific notes and dates in every answer. Traceability is what makes this exercise honest.

---

## Related Commands

- [[Prompt - Trace|/trace]] — Traces how a specific idea or belief has evolved across the vault over time
- [[Prompt - Emerge|/emerge]] — Surfaces ideas the vault implies but has never explicitly stated
- [[Prompt - Leverage|/leverage]] — Identifies high-leverage skills and knowledge that would produce disproportionate breakthroughs