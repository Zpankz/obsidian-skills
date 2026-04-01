---
name: breadcrumbs-development-workflow
description: "Use this skill to work inside the Breadcrumbs docs vault, including setup, orientation, editing flow, terminology checks, Caliber sync, and commit workflow. Do NOT use it for Breadcrumbs plugin code development."
---
# Development Workflow

## Critical

- This is a **documentation vault**, not a code project. There is no build step, no test suite, no package manager. The "project" is a set of Markdown files exported from Obsidian Publish.
- **Never invent Breadcrumbs settings, APIs, or syntax** not present in the existing docs. `API.md` only documents `window.BCAPI` at a placeholder level.
- **Caliber must sync before every commit.** Check for the pre-commit hook first: `grep -q "caliber" .git/hooks/pre-commit 2>/dev/null && echo "hook-active" || echo "no-hook"`. If no hook, run `caliber refresh` manually before committing.
- **Terminology is strict.** Use exact terms from the terminology table below — never paraphrase "Edge Fields" as "link types" or "Explicit Edge Builders" as "edge creators".

## Instructions

### 1. Orient yourself in the vault structure

The vault has this layout:

```
breadcrumbs-docs-vault/
├── Home.md                          # Entry point
├── Concepts.md                      # Graph, traversal, edge attributes
├── Edge Fields.md                   # Core concept: typed link labels
├── Field Groups.md                  # Collections of fields
├── Note Attributes.md               # BC-ignore-in-edges, BC-ignore-out-edges
├── API.md                           # Placeholder — window.BCAPI only
├── Debugging.md                     # Log levels, edge build errors
├── Contributing.md                  # How to contribute
├── Explicit Edge Builders/          # 9 builder types (Typed Links, Date Notes, etc.)
├── Implied Edge Builders/           # Transitive rules, relation rounds
├── Views/                           # Tree, Matrix, Codeblocks, Trail, Previous-Next
├── Commands/                        # Rebuild Graph, Threading, Freeze Crumbs, etc.
├── Suggesters/                      # Edge Field Suggester, Metadata Field Suggester
├── Guides/                          # Layered Daily Notes, Personal Relationship Mgmt
├── Announcements/                   # Discord release announcements
├── Images/                          # Screenshots referenced via ![[image.png]]
├── CLAUDE.md                        # Agent instructions (Caliber-managed)
├── AGENTS.md                        # Agent instructions (Caliber-managed)
└── DOWNLOAD_INFO.md                 # Publish export metadata
```

**Verify:** Run `find . -name '*.md' -not -path './Images/*' | sort` to confirm all doc pages are present.

### 2. Understand the editing conventions

Before editing any file, follow these rules:

| Convention | Correct | Wrong |
|---|---|---|
| Internal links | `[[Edge Fields]]` | `[Edge Fields](Edge%20Fields.md)` |
| Image embeds | `![[filename.png]]` | `![](Images/filename.png)` |
| Mermaid diagrams | ` ```mermaid ` fenced block | HTML or image-based diagrams |
| Folder index frontmatter | `BC-folder-note-field: down` | No frontmatter on index pages |
| Announcement chaining | `next:: [[Announcement 2024-04-25]]` | Manual prev/next links |

**Verify:** After editing, confirm all internal links use `[[wikilink]]` syntax: `rg -n '\[.*\]\(.*\.md\)' <edited-file>` should return zero results.

### 3. Validate terminology before writing

These terms have precise meanings in Breadcrumbs. Always use the exact term:

| Term | Meaning | Key file |
|---|---|---|
| Edge Fields | Typed link labels (`up`, `down`, `parent`, `child`) | `Edge Fields.md` |
| Field Groups | Collections of fields for traversal/views | `Field Groups.md` |
| Explicit Edge Builders | Derive edges from notes/metadata/tags/folders/dates | `Explicit Edge Builders/Explicit Edge Builders.md` |
| Implied Edge Builders | Inferred edges via transitive rules | `Implied Edge Builders/Implied Edge Builders.md` |
| Transitive Implied Relations | Chain syntax `[parent, parent] -> grandparent` | `Implied Edge Builders/Transitive Implied Relations.md` |
| Note Attributes | `BC-ignore-in-edges`, `BC-ignore-out-edges` | `Note Attributes.md` |
| Views | Tree View, Matrix View, Codeblocks, Trail View, Previous-Next View | `Views/Views.md` |
| Commands | Rebuild Graph, Threading, Freeze Crumbs, Jump to First Neighbour | `Commands/Commands.md` |
| Suggesters | Edge Field Suggester, Metadata Field Suggester | `Suggesters/Suggesters.md` |

**Verify:** After writing, search your text for common misspellings: `rg -in 'link type|edge creator|breadcrumb field|implied link' <edited-file>` should return zero results.

### 4. Search the vault for existing content

Before adding new content, check what already exists:

```bash
# Search for a concept across all docs
rg -n 'Edge Fields|Field Groups|Typed Links' --type md

# Find all image references
rg -n '!\[\[.*\.png\]\]' --type md

# Check frontmatter patterns
rg -n '^---' --type md -A 5
```

**Verify:** Confirm your new content does not duplicate existing pages by checking filenames: `find . -name '*.md' | sort`.

### 5. Commit workflow

1. Check Caliber hook status:
   ```bash
   grep -q "caliber" .git/hooks/pre-commit 2>/dev/null && echo "hook-active" || echo "no-hook"
   ```
2. If **hook-active**: commit normally — Caliber syncs `CLAUDE.md`, `AGENTS.md`, and other agent configs automatically.
3. If **no-hook**: run Caliber manually first:
   ```bash
   caliber refresh && git add CLAUDE.md .claude/ .cursor/ .cursorrules .github/copilot-instructions.md .github/instructions/ AGENTS.md CALIBER_LEARNINGS.md .agents/ .opencode/ 2>/dev/null
   ```
4. If `caliber` is not found: tell the user to run `/setup-caliber`.
5. Stage your changed files and commit.

**Verify:** After committing, run `git diff --cached --name-only` to confirm only intended files were included.

### 6. Adding a new doc page

1. Determine which subfolder the page belongs in (`Explicit Edge Builders/`, `Views/`, `Commands/`, `Guides/`, etc.).
2. If it's a new page in a folder that has an index (e.g., `Commands/Commands.md`), add a `[[New Page]]` wikilink to the index.
3. Use the frontmatter pattern matching existing pages in that folder:
   - Index pages: `BC-folder-note-field: down`
   - Pages with alternate names: `aliases: [...]`
   - Announcement pages: include `next:: [[Announcement ...]]` inline field
4. Place any screenshots in `Images/` and reference them with `![[screenshot.png]]`.

**Verify:** Run `rg -n '\[\[New Page\]\]'` to confirm the new page is linked from at least one other page.

## Examples

### Example: Adding a new guide page

**User says:** "Add a guide for using Breadcrumbs with MOCs."

**Actions taken:**
1. Check existing guides: `ls Guides/` → `Guides.md`, `Layered Daily Notes.md`, `Personal Relationship Management.md`
2. Read `Guides/Guides.md` to see the index format
3. Create `Guides/MOC Workflow.md` with:
   - No special frontmatter (guides don't use `BC-folder-note-field`)
   - `[[wikilink]]` syntax for all internal references
   - Correct terminology: "Edge Fields" not "link types"
4. Add `[[MOC Workflow]]` to `Guides/Guides.md`
5. Check Caliber hook, commit

**Result:** New guide page linked from the Guides index, using vault conventions.

### Example: Fixing a broken image reference

**User says:** "The screenshot in Debugging.md isn't showing."

**Actions taken:**
1. Read `Debugging.md`, find `![[Rebuild Graph Error Notice.png]]`
2. Check if image exists: `ls Images/ | grep 'Rebuild Graph Error Notice'`
3. If missing, note it for the user. If present but misnamed, fix the embed to match the exact filename.

**Result:** Image embed matches the actual filename in `Images/`.

## Common Issues

### "Caliber: command not found" when committing
1. Caliber is not installed. Run `/setup-caliber` to configure it.
2. If already installed but not in PATH, check `which caliber` or look in `~/.local/bin/`.

### Markdown links appear instead of wikilinks after editing
Some editors auto-convert `[[wikilink]]` to `[wikilink](wikilink.md)`. After editing, always verify:
```bash
rg -n '\[.*\]\(.*\.md\)' <edited-file>
```
If matches found, convert them back to `[[Page Name]]` syntax.

### New page not appearing in Breadcrumbs graph
The page must be linked from at least one other page using `[[wikilink]]` syntax. Check:
```bash
rg -rn '\[\[New Page Name\]\]' .
```
If zero results, add a link from the appropriate index page (e.g., `Guides/Guides.md`, `Commands/Commands.md`).

### Image embed not rendering
Image embeds must use `![[filename.png]]` (not `![](path)`). Verify the exact filename:
```bash
ls Images/ | grep -i '<partial-name>'
```
Filenames are case-sensitive. Match exactly.

### Frontmatter YAML errors
Folder index pages (`Commands/Commands.md`, `Views/Views.md`, `Suggesters/Suggesters.md`) require:
```yaml
---
BC-folder-note-field: down
---
```
Do not add this to non-index pages. If a page uses `aliases`, format as a YAML list:
```yaml
---
aliases:
  - alternate name
---
```

## Related skills
- `breadcrumbs` — for broader Breadcrumbs task routing
- `breadcrumbs-testing-guide` — for validation before commit
- `obsidian-ops` — for repo workflow and release hygiene patterns
