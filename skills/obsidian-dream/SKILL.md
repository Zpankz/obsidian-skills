---
name: obsidian-dream
description: Consolidate corrections, decisions, and vault patterns from Claude Code sessions into persistent memory files. Use /obsidian-dream to run manually or auto-triggers every 24hrs via Stop hook.
tags: [memory, maintenance, consolidation, pkm, obsidian, autonomous, hook]
---

# Obsidian Dream - PKM Memory Consolidation

> Consolidates what you learned, decided, and corrected across Obsidian PKM sessions.

---

## Routing

| Command | What it does |
|---|---|
| `/obsidian-dream` | Full 4-phase consolidation |
| `/obsidian-dream dry-run` | Preview changes without writing |
| `/obsidian-dream status` | Show last dream time, memory stats |
| `/obsidian-dream prune` | Phase 4 only — trim and reindex |

---

## How It Works

```
ORIENT --> GATHER SIGNAL --> CONSOLIDATE --> PRUNE & INDEX
```

### Auto-trigger flow

```
Session ends
  --> Stop hook fires should-dream.sh (~10ms)
  --> Checks: 24hrs passed since last dream?
  --> If YES: creates ~/.claude/.dream-pending flag
Next session starts
  --> Claude sees .dream-pending, spawns /obsidian-dream in background
  --> Dream runs all 4 phases
  --> Writes .last-dream timestamp, deletes flag
```

### Safety boundary

During dream, you may **only write to memory files** (`~/.claude/projects/*/memory/`).
Never modify vault notes, source code, configs, or any other project files.
You may **read** vault files and source to verify memory accuracy.

---

## Phase 1: ORIENT

**Goal:** Map the current state of memory before changing anything.

### Steps

1. Find all project memory directories:
```bash
ls -d ~/.claude/projects/*/memory/ 2>/dev/null
```

2. Read `MEMORY.md` in each. Note:
   - Topic file count and sizes
   - Last modified dates
   - Stale entries (relative dates, references to moved/deleted notes)
   - Which projects are Obsidian vaults vs other repos

3. Read each topic file to understand what's stored.

4. Check for PKM-specific context clues:
   - Vault paths and structure patterns in memory
   - Knowledge graph state (PKG/GKG references from `/paths`)
   - Research domains and active learning paths
   - Cross-vault references and shared taxonomies

### Output
A mental map of: which projects have memory, what topics are covered, what's stale.

---

## Phase 2: GATHER SIGNAL

**Goal:** Extract important PKM-relevant information from recent sessions.

### Where to find transcripts
```bash
find ~/.claude/projects/*/sessions/ -name "*.jsonl" -mtime -7 2>/dev/null | sort -t/ -k6 -r
```

### Signal categories

Use targeted grep, not full reads. Each pattern targets a specific signal type.

**User corrections** (highest priority — things the user told you to stop doing or do differently):
```bash
grep -il "actually\|no,\|wrong\|incorrect\|not right\|stop doing\|don't do\|I said\|I meant\|that's not\|correction" ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null
```

**Preferences and habits:**
```bash
grep -il "I prefer\|always use\|never use\|I like\|I don't like\|I want\|from now on\|going forward\|remember that\|keep in mind\|make sure to\|default to" ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null
```

**Decisions and directions:**
```bash
grep -il "let's go with\|I decided\|we're using\|the plan is\|switch to\|move to\|chosen\|picked\|decision\|we agreed" ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null
```

**PKM and vault signals** (unique to this skill):
```bash
grep -il "vault\|frontmatter\|wikilink\|backlink\|dataview\|templater\|breadcrumbs\|canvas\|graph view\|daily note\|tag\|folder structure\|MOC\|map of content\|zettelkasten\|evergreen\|atomic note\|knowledge graph\|PKG\|GKG\|learning path\|mastery\|gap analysis\|spaced repetition" ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null
```

**Research and knowledge work signals:**
```bash
grep -il "research\|studying\|reading\|paper\|article\|source\|reference\|bibliography\|literature\|domain\|topic\|concept\|framework\|model\|theory\|hypothesis\|insight\|connection\|pattern\|synthesis\|summarize\|extract\|annotate" ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null
```

**Recurring patterns:**
```bash
grep -il "again\|every time\|keep forgetting\|as usual\|same as before\|like last time\|we always\|the usual" ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null
```

### How to read matches

For each matching file, read ONLY surrounding context. JSONL files have one JSON object per line. Focus on `"human"` type lines and the immediately following `"assistant"` response.

### What to extract

For each finding, note:
- **The fact** — what was said or decided
- **The date** — derive from session file modification time (convert to absolute)
- **Confidence** — explicit instruction (high) or implied preference (medium)?
- **Contradictions** — does this conflict with anything in memory?
- **Scope** — is this vault-specific, cross-vault, or general workflow?

---

## Phase 3: CONSOLIDATE

**Goal:** Merge new findings into existing memory files.

### Rules

1. **Never duplicate.** Check if it already exists. Update rather than create.

2. **Convert relative dates to absolute.** "Yesterday" from a March 15 session → "2026-03-14".

3. **Delete contradicted facts.** Remove old, write new. Note: `(Updated YYYY-MM-DD, previously: X)`.

4. **Preserve source attribution.** `(from session YYYY-MM-DD)`.

5. **PKM-aware topic organization.** Use topic files that reflect knowledge work:

   | File | Contents |
   |---|---|
   | `preferences.md` | How the user likes things done — formatting, workflow, tools |
   | `decisions.md` | Choices and rationale — vault structure, taxonomy, tool selection |
   | `corrections.md` | Things the user corrected — mistakes to avoid repeating |
   | `patterns.md` | Recurring workflows — daily routines, processing pipelines |
   | `vault-conventions.md` | Vault structure, frontmatter schemas, naming, folder taxonomy, link style |
   | `research-domains.md` | Active research areas, knowledge gaps, learning goals, domain expertise levels |
   | `knowledge-graph.md` | PKG/GKG state snapshots, graph evolution notes, path progress, gap analysis results |
   | `tools-and-integrations.md` | Plugin configs, AI4PKM agents, pollers, automation workflows |

   Create new topic files only when existing ones don't fit.

6. **Entry format:**
   ```markdown
   - [YYYY-MM-DD] The fact or preference. (source: session, confidence: high/medium)
   ```

7. **Cross-project consolidation.** Patterns that span multiple vaults or projects (e.g., "always use ISO dates in frontmatter") belong in user-level memory or a shared topic file, not duplicated per project.

8. **Consistency with /paths consolidate.** If `/paths` has run `memory_consolidate.py` and produced epoch summaries, read those as input — don't re-extract the same signals. Treat `/paths` session history as already-processed data. Dream consolidates the _meta-level_ (preferences, corrections, decisions) while `/paths consolidate` handles the _learning-level_ (mastery scores, gap evolution, path progress).

### How to write

Use the Edit tool to modify existing memory files, or Write to create new topic files. Always read a file before editing.

---

## Phase 4: PRUNE & INDEX

**Goal:** Keep MEMORY.md lean. Remove stale content. Enforce limits.

### MEMORY.md rules

MEMORY.md is an **index**, not a content store. Contains:
- One-line links to topic files with brief summaries
- Last-updated date per topic file

Never contains: full entries, verbose descriptions, duplicated content.

### Size limit: 200 lines

If over 200 lines:
1. Move inline content to topic files
2. Replace verbose entries with one-line summaries + links
3. Remove entries pointing to nonexistent files
4. Demote oldest entries to `archive.md`

### Prune stale entries

Remove or archive entries that:
- Are 90+ days old with no recent session references
- Are contradicted by newer entries
- Reference vaults, folders, or notes that no longer exist
- Describe workflows the user has clearly abandoned

### PKM-specific pruning

- Verify vault paths in memory still exist on disk
- Check that referenced notes/folders still exist in the vault
- Remove tool/plugin notes for plugins the user has uninstalled
- If `/paths` has updated GKG/PKG state, remove outdated snapshots from `knowledge-graph.md`
- Collapse old research-domain entries into summaries when the domain is no longer active

### Final index format

```markdown
# Memory Index

Last consolidated: YYYY-MM-DD

## Topic Files

| File | Summary | Updated |
|------|---------|---------|
| preferences.md | Workflow, formatting, communication preferences | YYYY-MM-DD |
| decisions.md | Architecture, taxonomy, tool choices and rationale | YYYY-MM-DD |
| corrections.md | Past mistakes to avoid repeating | YYYY-MM-DD |
| patterns.md | Recurring workflows, daily routines, processing pipelines | YYYY-MM-DD |
| vault-conventions.md | Vault structure, frontmatter, naming, folder taxonomy | YYYY-MM-DD |
| research-domains.md | Active research areas, knowledge gaps, learning goals | YYYY-MM-DD |
| knowledge-graph.md | PKG/GKG snapshots, path progress, gap analysis | YYYY-MM-DD |
| tools-and-integrations.md | Plugin configs, AI4PKM agents, automation | YYYY-MM-DD |

## Quick Reference

<!-- 5-10 most important facts for every session -->
- Fact 1
- Fact 2
```

### Record the dream timestamp

After all 4 phases:
```bash
date +%s > ~/.claude/projects/<project>/memory/.last-dream
rm -f ~/.claude/.dream-pending
```

---

## Safety

- **Never delete without replacement.** Removed entries must be contradicted (replaced) or moved (topic file / archive).
- **Back up before first run:**
  ```bash
  cp -r ~/.claude/projects/<project>/memory/ ~/.claude/projects/<project>/memory-backup-$(date +%Y%m%d)/
  ```
- **Dry run on first use.** Read all 4 phases, print what you WOULD change, confirm before applying.
- **Vault files are read-only.** Dream may read vault notes to verify memory but must NEVER modify them.

---

## Verification

After running, verify:
1. `wc -l` on MEMORY.md — under 200 lines
2. No duplicate entries across topic files
3. No relative dates remain ("yesterday", "last week")
4. All topic files referenced in MEMORY.md exist
5. No stale vault paths or note references
6. Print summary: entries added, updated, archived, contradictions resolved
