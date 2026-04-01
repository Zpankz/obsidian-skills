---
name: breadcrumbs-terminology
description: "Use this skill to enforce canonical Breadcrumbs terminology across docs pages, including Edge Fields, Field Groups, Explicit and Implied Edge Builders, Transitive Implied Relations, Note Attributes, and official view/command names. Do NOT use it for general grammar review."
---
# Breadcrumbs Terminology

Enforce consistent terminology when writing or editing pages in the Breadcrumbs docs vault (`breadcrumbs-docs-vault/`). Every concept name, view name, command name, and field reference must match the canonical forms defined in the source docs.

## Critical

- **Never rename or paraphrase** a canonical term. `Edge Fields` is never "edge types", "link fields", or "field edges".
- **Never invent terms** not present in the docs export. If a concept lacks a page, it does not exist in Breadcrumbs terminology.
- **Wikilink references** must use the exact page name: `[[Edge Fields]]`, not `[[Edge Field]]` or `[[edge fields]]` (aliases handle display, but the link target is the page title).
- The canonical source files are:
  - `Concepts.md` — Graph, Node Attributes, Edge Attributes, Edge Sorters, Traversal
  - `Edge Fields.md` — field definitions (`up`, `same`, `down`, `next`, `prev`)
  - `Field Groups.md` — group definitions
  - `Note Attributes.md` — `BC-ignore-in-edges`, `BC-ignore-out-edges`
  - `Explicit Edge Builders/Explicit Edge Builders.md` — explicit vs implied distinction
  - `Implied Edge Builders/Implied Edge Builders.md` — implied edge rules
  - `Views/Views.md` — view names
  - `Commands/Commands.md` — command names
  - `Suggesters/Suggesters.md` — suggester names

## Instructions

### Step 1: Identify all Breadcrumbs terms in the content

Scan the text for any reference to Breadcrumbs concepts. Flag every noun phrase that refers to a plugin feature, setting, view, command, or field.

Verify: you have a list of every term candidate before proceeding.

### Step 2: Validate each term against the canonical glossary

Compare each identified term against this exact glossary. The **Canonical Form** column is the only acceptable spelling and capitalisation.

| Canonical Form | Wrong Forms (common mistakes) | Source File |
|---|---|---|
| Edge Fields | edge types, link fields, field edges, edge-fields | `Edge Fields.md` |
| Field Groups | field group, edge groups, groups of fields | `Field Groups.md` |
| Explicit Edge Builders | explicit builders, edge builders (when meaning explicit only) | `Explicit Edge Builders/Explicit Edge Builders.md` |
| Implied Edge Builders | implicit edges, inferred edges, implied builders | `Implied Edge Builders/Implied Edge Builders.md` |
| Transitive Implied Relations | transitive relations, transitive rules, implied transitive | `Implied Edge Builders/Transitive Implied Relations.md` |
| Implied Relation Rounds | rounds, implication rounds | `Implied Edge Builders/Implied Relation Rounds.md` |
| Note Attributes | note properties, BC attributes | `Note Attributes.md` |
| `BC-ignore-in-edges` | BC-ignore-in, ignore-in-edges, bc-ignore-in-edges | `Note Attributes.md` |
| `BC-ignore-out-edges` | BC-ignore-out, ignore-out-edges, bc-ignore-out-edges | `Note Attributes.md` |
| Tree View | tree-view, TreeView | `Views/Tree View.md` |
| Matrix View | matrix-view, MatrixView | `Views/Matrix View.md` |
| Codeblocks | code blocks, Code Blocks, codeblock | `Views/Codeblocks.md` |
| Trail View | trail-view, TrailView, breadcrumb trail | `Views/Trail View.md` |
| Previous-Next View | prev-next view, Previous/Next View | `Views/Previous-Next View.md` |
| Page Views | page view (singular when referring to the category) | `Views/Page Views.md` |
| Rebuild Graph | rebuild-graph, Rebuild graph | `Commands/Rebuild Graph.md` |
| Threading | thread, threading command | `Commands/Threading.md` |
| Freeze Crumbs to File | freeze crumbs, Freeze Crumbs | `Commands/Freeze Crumbs to File.md` |
| Create List Index | list index, List Index | `Commands/Create List Index.md` |
| Jump to First Neighbour | jump to neighbour, First Neighbour | `Commands/Jump to First Neighbour.md` |
| Graph Stats | graph-stats, Graph Statistics | `Commands/Graph Stats.md` |
| Typed Links | typed-links, type links | `Explicit Edge Builders/Typed Links.md` |
| Date Notes | date-notes, Date Note | `Explicit Edge Builders/Date Notes.md` |
| Dataview Notes | dataview-notes, Dataview notes | `Explicit Edge Builders/Dataview Notes.md` |
| Folder Notes | folder-notes, Folder Note | `Explicit Edge Builders/Folder Notes.md` |
| Tag Notes | tag-notes, Tag Note | `Explicit Edge Builders/Tag Notes.md` |
| Regex Notes | regex-notes, Regex Note | `Explicit Edge Builders/Regex Notes.md` |
| List Notes | list-notes, List Note | `Explicit Edge Builders/List Notes.md` |
| Dendron Notes | dendron-notes, Dendron Note | `Explicit Edge Builders/Dendron Notes.md` |
| Johnny Decimal Notes | johnny-decimal, JD Notes | `Explicit Edge Builders/Johnny Decimal Notes.md` |
| Edge Field Suggester | field suggester, edge suggester | `Suggesters/Edge Field Suggester.md` |
| Metadata Field Suggester | metadata suggester | `Suggesters/Metadata Field Suggester.md` |
| Edge Attributes | edge properties, link attributes | `Concepts.md` |
| Node Attributes | node properties | `Concepts.md` |
| Edge Sorters | edge sorting, sort fields | `Concepts.md` |
| Traversal | traverse, graph walk | `Concepts.md` |
| `BC-folder-note-field` | bc-folder-note, folder note field | folder index pages |

Verify: every term in your content matches a row in this table. If a term has no match, check the source files — it may be invalid.

### Step 3: Validate wikilink targets

For every `[[wikilink]]` in the content that references a Breadcrumbs concept:
1. Confirm the link target matches an actual `.md` filename in the vault (e.g., `[[Edge Fields]]` → `Edge Fields.md` exists).
2. For pages in subdirectories, the wikilink uses just the basename: `[[Typed Links]]`, not `[[Explicit Edge Builders/Typed Links]]`.
3. Aliases in YAML frontmatter (e.g., `Edge Fields.md` has alias `edge fields`) allow display variations but the link target must still be the page title.

Verify: run `find breadcrumbs-docs-vault -name '*.md' | sort` and confirm every link target resolves.

### Step 4: Check the explicit/implied distinction

Breadcrumbs draws a hard line between **explicit** and **implied** edges:
- **Explicit**: derived from existing structure in notes (YAML frontmatter, Dataview inline fields, tags, folders, dates, wikilinks). Created by Explicit Edge Builders.
- **Implied**: deduced from explicit edges using Transitive Implied Relations rules like `[parent, parent] -> grandparent`. Created by Implied Edge Builders.

If the content describes an edge as "implied" but it comes from note metadata, correct it to "explicit". If it describes an edge as "explicit" but it's derived from a transitive chain, correct it to "implied".

Verify: every use of "explicit" and "implied" in the content aligns with this distinction.

### Step 5: Validate default field names

The five default Edge Fields are exactly: `up`, `same`, `down`, `next`, `prev`. Not "previous" (the field is `prev`; the view is `Previous-Next View`). Custom fields like `parent`, `child`, `sibling`, `grandparent`, `aunt-uncle`, `cousin` appear in examples but are not defaults.

Verify: default fields are listed as `up`, `same`, `down`, `next`, `prev` — no extras, no omissions.

### Step 6: Validate transitive relation syntax

Transitive rules use the exact syntax: `[field-one, field-two] -> close-field` or `[field] <- close-field` (for reversed). Examples from docs:
- `[parent, parent] -> grandparent`
- `[up] <- down`
- `[sibling, sibling] -> sibling`
- `[parent, sibling] -> aunt-uncle`
- `[parent, child] -> sibling`
- `[parent, sibling, child] -> cousin`

Do not use arrow syntax like `=>`, `-->`, or prose like "parent of parent equals grandparent".

Verify: every transitive rule in the content uses `[fields] -> close` or `[fields] <- close` syntax.

## Examples

### Example 1: Reviewing a new guide page

**User says**: "I wrote a new guide page, check it for terminology."

**Content contains**: "Set up your edge types in settings, then use the tree-view to see implicit relationships."

**Actions taken**:
1. `edge types` → corrected to `[[Edge Fields]]`
2. `tree-view` → corrected to `[[Tree View]]`
3. `implicit relationships` → corrected to `[[Implied Edge Builders|implied]]` edges (and verified these are truly transitive-derived, not from metadata)

**Result**: "Set up your [[Edge Fields]] in settings, then use the [[Tree View]] to see [[Implied Edge Builders|implied]] relationships."

### Example 2: Validating a transitive rule description

**User says**: "Add a section explaining that parent => parent means grandparent."

**Actions taken**:
1. Arrow syntax `=>` corrected to canonical `[parent, parent] -> grandparent`
2. Term "means" replaced with the standard phrasing: "a chain of two `parent` fields collapses down to one `grandparent` field"
3. Confirmed `grandparent` is a custom field (not a default) and labeled it as such

**Result**:
> `[parent, parent] -> grandparent` — a chain of two `parent` fields collapses down to one `grandparent` field between the start and end nodes.

## Common Issues

### "Previous" vs `prev`
The default edge field is `prev` (not "previous"). But the view is `Previous-Next View` (not "Prev-Next View"). These are intentionally different. If you see `prev` used as a view name or `previous` used as a field name, one of them is wrong.

### "Implicit" vs "Implied"
Breadcrumbs always uses **implied**, never "implicit". Search for `implicit` — if found, replace with `implied`. The canonical terms are `Implied Edge Builders` and `Transitive Implied Relations`.

### "Code Blocks" vs "Codeblocks"
The view is `Codeblocks` (one word, capital C). Not "Code Blocks", "code blocks", or "codeblock" (singular). The page is `Views/Codeblocks.md`.

### "Neighbour" spelling
The command is `Jump to First Neighbour` with British spelling. Not "Neighbor". This matches the source file `Commands/Jump to First Neighbour.md`.

### Missing wikilink brackets around concept names
Every Breadcrumbs concept name that has its own page should be wikilinked on first use in a doc page. Run: `rg -n 'Edge Fields|Field Groups|Typed Links' <file>` and verify matches are wrapped in `[[ ]]`.

### Confusing Edge Builders with Edge Fields
`Edge Fields` are the typed labels (`up`, `down`, `parent`). `Explicit Edge Builders` are the mechanisms that create edges (Typed Links, Folder Notes, Date Notes, etc.). These are distinct concepts — do not conflate them.

## Related skills
- `breadcrumbs` — for broader Breadcrumbs workflow routing
- `breadcrumbs-edit` — when terminology review leads to doc edits
- `breadcrumbs-code-conventions` — to align naming fixes with docs formatting conventions
