---
title: "Prompt - Contradict"
created: 2026-03-06
description: "Prompt - Contradict"
tags:
  - "vault-command"
related:
  - "[[Prompt - Challenge]]"
  - "[[Prompt - Drift]]"
  - "[[Prompt - Trace]]"
---
## Contradict — Find Incompatible Beliefs Held Simultaneously

Surface beliefs that cannot both be true at the same time. Not evolution (that's [[Prompt - Trace|/trace]]), not pressure-testing (that's [[Prompt - Challenge|/challenge]]). This command finds places where the vault holds two positions that are logically incompatible, right now, and asks: which one do you actually believe?

**Usage:**`/contradict` (general) or `/contradict [domain]` (focused)

---

## How This Differs from /challenge and /trace

- [[Prompt - Challenge|/challenge]] pressure-tests current beliefs by finding evidence against them. It asks: "Is this wrong?"
- [[Prompt - Trace|/trace]] tracks how ideas evolved over time. It asks: "How did this change?"
- [[Prompt - Contradict|/contradict]] finds beliefs held simultaneously that cannot cohere. It asks: "You believe X and also Y. Both cannot be true. Which is it?"

The distinction matters. A challenge might reveal a belief is weak. A trace might show a belief changed. A contradiction reveals that two beliefs currently coexist and shouldn't.

---

## Step 1: Extract Beliefs

### Read All Context Files

```bash
obsidian read file="<Context File A>"
obsidian read file="<Context File B>"
obsidian read file="<Context File C>"
```

### Read Recent Daily Notes

```bash
obsidian daily:read
obsidian read path="Daily Notes/YYYY-MM-DD.md"  # past 14-21 days
```

### Structured Belief Extraction

For each source, extract explicit belief statements. Look for:

- "I believe...", "I think...", "The way to...", "What matters is..."
- Strong assertions, confident predictions, absolute statements
- Advice given to others (implies a belief)
- Decisions made (imply a belief about what's right)
- Priorities stated (imply a belief about what matters)
- Things rejected or criticized (imply a belief about what's wrong)

**Write each belief as a paired statement:**

- Belief: "\[Explicit statement\]"
- Source: \[Note name, date, context\]
- Implied inverse: "\[What this belief denies or excludes\]"

The implied inverse is critical. It's what makes contradiction detection possible. "I believe in focus" implies "I believe spreading thin is wrong." If another part of the vault shows enthusiastic spreading thin, that's a contradiction.

List ALL extracted beliefs before moving to detection. Minimum 15-20 beliefs to work with.

---

## Step 2: Detection Methods

Run all three detection methods independently. Each catches contradictions the others miss.

### Method 1: Explicit Contradictions

#### Within-Domain

Compare beliefs extracted from the same context file or the same time period. Do any directly conflict?

```bash
obsidian search:context query="<belief A statement>" format=json  # With matching lines for evidence
obsidian search:context query="<belief A inverse>" format=json
```

#### Cross-Domain

Compare beliefs across different context files. A belief about building may contradict a belief about living. These are the most interesting contradictions because they reveal compartmentalized thinking.

```bash
obsidian search:context query="<belief from domain A>" format=json  # Search across ALL context files
```

### Method 2: Implicit Contradictions

#### Stated Values vs. Revealed Preferences

What does the vault say matters vs. what does actual behavior (daily notes, calendar references, time allocation) reveal? A stated value of "deep focus" alongside daily notes filled with reactive scattered activity is an implicit contradiction.

```bash
obsidian search query="<stated value>" path="Daily Notes" format=json  # how often does it appear in practice?
```

Count frequency to quantify the gap between stated and revealed values.

#### Advice vs. Behavior

What advice does the vault give to others vs. what does the vault show about personal behavior? "You should ship fast" from someone whose own projects sit unshipped is a contradiction.

```bash
obsidian search query="should" path="Daily Notes"
obsidian search query="need to" path="Daily Notes"
```

### Method 3: Priority Contradictions

Two things cannot both be the top priority. If the vault treats multiple things as most important, that's a priority contradiction. These are often hidden because each domain has its own context file where it gets to be the center of attention.

Compare priority language across all context files. How many things are described as "the most important" or "the priority" or "what matters most"?

---

## Step 3: Evolution Filter

Before reporting any contradiction, run it through this 4-test filter. Many apparent contradictions are actually evidence of healthy evolution.

### Test 1: Temporal Currency

Are both beliefs current? If one was written 6+ months ago and the other last week, this might be evolution, not contradiction. Check:

```bash
obsidian search query="<older belief>" path="Daily Notes"  # does it still appear recently?
```

If the older belief hasn't appeared in 3+ months, it may simply be outdated. Flag it as "possibly resolved through evolution" rather than an active contradiction.

### Test 2: Domain Compartmentalization

Is it possible that both beliefs are true in their respective domains? "Move fast" in product and "be patient" in relationships is not a contradiction. But "move fast" in product and "be patient" in product IS one. Only flag cross-domain contradictions when the beliefs genuinely cannot coexist.

### Test 3: Confidence Marker Check

Do the contradicting beliefs have confidence markers? A `[solid]` belief contradicting a `[hypothesis]` is less concerning than two `[solid]` beliefs contradicting each other.

### Test 4: The "Cannot Both Be True" Test

The hardest test. State both beliefs plainly and ask: is there any reasonable interpretation where both can be true simultaneously? If yes, this is tension, not contradiction. Only report contradictions that genuinely fail this test.

---

## Step 4: Classify Each Contradiction

For each contradiction that survives the evolution filter:

### Category

**Resolve**: This is confused thinking. One of these beliefs needs to go. The contradiction is producing real costs (bad decisions, wasted energy, incoherent strategy).

**Hold**: This is productive tension. The contradiction is actually useful because reality is complex. Both beliefs capture something true, and holding them in tension is better than collapsing into one. But name it explicitly so it's held consciously, not accidentally.

**Celebrate**: This is evidence of growth. An old belief and a new belief that contradict each other, where the new one represents genuine learning. The contradiction exists because the vault hasn't been updated, not because the thinking is confused.

### Weight

| Weight | Definition |
| --- | --- |
| **Trivial** | Interesting but inconsequential. Different moods, different contexts. |
| **Moderate** | Affects decision-making in a specific area. Worth noting. |
| **Significant** | Affects strategy or identity. Needs conscious attention. |
| **Foundational** | If unresolved, undermines the coherence of a major life area. |

---

## Step 5: Output

### For Each Contradiction

**Contradiction \[#\]: \[Title\]**

**Belief A:** "\[Statement\]"

- Source: \[Note, date\]
- Confidence: \[If marked\]

**Belief B:** "\[Statement\]"

- Source: \[Note, date\]
- Confidence: \[If marked\]

**Why these cannot both be true:** \[Explicit logical statement\]

**Category:** Resolve / Hold / Celebrate  
**Weight:** Trivial / Moderate / Significant / Foundational

**What to do:** \[Specific recommendation based on category\]

### Synthesis

**Contradiction count:** \[number\]  
**By category:** Resolve: X, Hold: Y, Celebrate: Z  
**By weight:** Foundational: X, Significant: Y, Moderate: Z, Trivial: W

**The deepest contradiction:** The one that, if resolved, would clarify the most about everything else.

**Pattern in the contradictions:** Do they cluster? Is there a meta-contradiction (e.g., "Most contradictions are between what you say and what you do" or "Most contradictions are between your ambitions and your constraints")?

---

## Anti-Patterns

**1\. The Evolution Trap**  
Flagging changed beliefs as contradictions. If someone believed X in January and Y in June, that's evolution. Only flag it if BOTH are still active.

**2\. The Nuance Destroyer**  
Treating domain-appropriate variation as contradiction. Different contexts can warrant different approaches. Only flag when beliefs genuinely cannot coexist.

**3\. The Contradiction Factory**  
Finding contradictions everywhere by paraphrasing beliefs loosely enough that anything conflicts with anything. Be precise about what each belief actually claims.

**4\. The Problem Frame**  
Treating all contradictions as problems. Some contradictions are productive tensions that should be held, not resolved.

**5\. The Surface Scanner**  
Only finding explicit contradictions (word-level conflicts) and missing implicit ones (value-behavior gaps, advice-action gaps). Method 2 is where the real findings are.

**6\. The Therapist**  
Turning contradiction analysis into psychological diagnosis. This is logic analysis, not therapy. Stay structural.

---

## Output Format

**CONTRADICT REPORT**  
**Scope:** \[General / Domain-focused\]  
**Beliefs examined:** \[number\]  
**Contradictions found:** \[number\]  
**Survived evolution filter:** \[number\]

\[Contradictions, ordered by weight\]

\[Synthesis\]

\[The deepest contradiction\]

\[Pattern analysis\]

---

## Output Guidelines

- Be precise. Vague contradictions are not contradictions, they're mood shifts.
- Always cite specific notes and dates. Every belief should be traceable.
- The evolution filter is mandatory. Skipping it produces false positives.
- The best contradictions are ones that make you say "I genuinely believe both of those, and you're right, I can't."
- If the vault is well-integrated and genuinely non-contradictory, say so. Don't manufacture contradictions.

---

## Related Commands

- [[Prompt - Challenge|/challenge]] — Pressure-tests current beliefs using the vault's own history
- [[Prompt - Drift|/drift]] — Compares stated intentions against actual behavior to surface avoidance patterns
- [[Prompt - Trace|/trace]] — Traces how a specific idea or belief has evolved across the vault over time