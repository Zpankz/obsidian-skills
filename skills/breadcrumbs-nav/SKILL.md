---
name: breadcrumbs-nav
description: "Use this skill to locate the right Breadcrumbs docs page, command, view, builder, guide, or suggester across the exported docs vault. Do NOT use it for editing content."
---
# Breadcrumbs Docs Navigation

Locate and surface the correct page(s) in the `breadcrumbs-docs-vault/` export when someone needs to find documentation about a Breadcrumbs concept, feature, or setting.

## Critical

- The vault root is `breadcrumbs-docs-vault/`. All paths below are relative to it.
- **Never modify files** — this skill is read-only navigation. Use a separate editing skill for changes.
- Use the **exact Breadcrumbs terminology** from the docs. Do not rename or paraphrase concepts. The canonical terms are:
  - `Edge Fields` (not "link types" or "edge types")
  - `Field Groups` (not "field collections")
  - `Explicit Edge Builders` (not "manual builders")
  - `Implied Edge Builders` (not "inferred builders")
  - `Transitive Implied Relations` (not "transitive rules")
  - `Note Attributes` (`BC-ignore-in-edges`, `BC-ignore-out-edges`)
  - View names exactly: `Tree View`, `Matrix View`, `Codeblocks`, `Trail View`, `Previous-Next View`, `Page Views`
  - Command names exactly: `Rebuild Graph`, `Threading`, `Freeze Crumbs to File`, `Create List Index`, `Jump to First Neighbour`, `Graph Stats`

## Instructions

### Step 1: Classify the user's query into a docs section

Map the question to one of these sections using the lookup table:

| Query mentions | Section | Index page |
|---|---|---|
| typed links, YAML links, Dataview links, wikilink edges, metadata properties, tags-as-edges, folders-as-edges, date notes, regex notes, dendron, johnny decimal, list notes | `Explicit Edge Builders/` | `Explicit Edge Builders/Explicit Edge Builders.md` |
| implied edges, transitive, inferred links, relation rounds | `Implied Edge Builders/` | `Implied Edge Builders/Implied Edge Builders.md` |
| tree view, matrix view, codeblocks, trail view, previous-next, page views, breadcrumb trail, navigation bar | `Views/` | `Views/Views.md` |
| rebuild graph, threading, freeze crumbs, list index, jump neighbour, graph stats, command palette | `Commands/` | `Commands/Commands.md` |
| suggester, autocomplete, edge field suggester, metadata field suggester | `Suggesters/` | `Suggesters/Suggesters.md` |
| daily notes guide, relationship management, practical use-case, how-to | `Guides/` | `Guides/Guides.md` |
| edge fields, field setup, `up`/`down`/`next`/`prev`/`same`, custom fields | Top-level | `Edge Fields.md` |
| field groups, direction groups, `ups`/`downs` | Top-level | `Field Groups.md` |
| BC-ignore, ignore edges, note attributes | Top-level | `Note Attributes.md` |
| graph, traversal, node attributes, edge attributes, edge sorters | Top-level | `Concepts.md` |
| API, BCAPI, window.BCAPI | Top-level | `API.md` |
| debugging, log levels, console errors, build errors | Top-level | `Debugging.md` |
| announcements, release notes, changelog | `Announcements/` | `Announcements/Announcements.md` |
| overview, quick start, getting started | Top-level | `Home.md` |

Verify: you have identified at least one matching section before proceeding.

### Step 2: Read the index page to confirm the target

Read the section's index page (from the table above) to confirm it contains a link to the specific sub-topic.

- Each index page uses `[[wikilink]]` syntax to list its children.
- Match the user's query to the wikilink target that best fits.

Verify: you have a specific filename (e.g., `Typed Links.md`, `Date Notes.md`) before proceeding.

### Step 3: Read the target page

Read the specific page. Paths follow this pattern:

```
breadcrumbs-docs-vault/<Section>/<Page>.md
```

For top-level pages:
```
breadcrumbs-docs-vault/<Page>.md
```

Verify: the page content answers the user's question. If not, check aliases in YAML frontmatter (e.g., `Edge Fields.md` has aliases `edge fields`, `field`) and try related pages.

### Step 4: Present the answer with source path

Return the relevant information and always cite the source file path so the user can navigate there directly.

Format: quote or summarize the relevant section, then append:
> Source: `breadcrumbs-docs-vault/<path>`

### Step 5: Surface related pages if applicable

If the page references other Breadcrumbs pages via `[[wikilinks]]`, mention them as "Related docs" so the user can explore further.

## Complete Vault Map

Use this as the authoritative file listing when you need to locate a page:

**Top-level docs:**
- `Home.md` — overview, quick start, use-cases
- `Concepts.md` — graph, traversal, edge/node attributes, edge sorters
- `Edge Fields.md` — field setup, `up`/`down`/`same`/`next`/`prev`, custom fields
- `Field Groups.md` — grouping fields by direction
- `Note Attributes.md` — `BC-ignore-in-edges`, `BC-ignore-out-edges`
- `API.md` — BCAPI (placeholder)
- `Debugging.md` — log levels, edge build errors
- `Contributing.md` — contribution guidelines

**Explicit Edge Builders/**
- `Explicit Edge Builders.md` — index
- `Typed Links.md` — YAML frontmatter and Dataview inline typed links
- `Tag Notes.md` — edges from tags
- `Regex Notes.md` — edges from regex patterns
- `List Notes.md` — edges from list items
- `Dendron Notes.md` — edges from Dendron-style note hierarchies
- `Johnny Decimal Notes.md` — edges from Johnny Decimal structure
- `Dataview Notes.md` — edges from Dataview fields
- `Date Notes.md` — edges from date-based note naming
- `Folder Notes.md` — edges from folder structure

**Implied Edge Builders/**
- `Implied Edge Builders.md` — index, explicit vs implied distinction
- `Transitive Implied Relations.md` — chain syntax `[parent, parent] -> grandparent`
- `Implied Relation Rounds.md` — multi-round implied edge processing

**Views/**
- `Views.md` — index, common display settings
- `Tree View.md` — hierarchical tree display
- `Matrix View.md` — grid/matrix of edges
- `Views/Codeblocks.md` — YAML codeblock-based views in notes
- `Page Views.md` — views embedded in note pages
- `Trail View.md` — breadcrumb trail at top of notes
- `Previous-Next View.md` — prev/next navigation

**Commands/**
- `Commands.md` — index
- `Rebuild Graph.md` — refresh the Breadcrumbs graph
- `Jump to First Neighbour.md` — navigate to first linked note
- `Freeze Crumbs to File.md` — persist implied edges to frontmatter
- `Create List Index.md` — generate list-based index
- `Commands/Threading.md` — thread navigation
- `Graph Stats.md` — graph statistics command

**Suggesters/**
- `Suggesters.md` — index
- `Edge Field Suggester.md` — autocomplete for edge fields
- `Metadata Field Suggester.md` — autocomplete for metadata fields

**Guides/**
- `Guides.md` — index
- `Layered Daily Notes.md` — daily/weekly/monthly note hierarchies
- `Personal Relationship Management.md` — modeling people with edges

**Announcements/**
- `Announcements.md` — index
- `Announcement 2024-03-18.md` through `Announcement 2024-04-25.md`

## Examples

### Example 1: "Where is the docs for date notes?"

**User says:** "Where is the docs for date notes?"

**Actions taken:**
1. Query mentions "date notes" → maps to `Explicit Edge Builders/`
2. Read `Explicit Edge Builders/Explicit Edge Builders.md` — confirms `[[Date Notes]]` is listed
3. Read `Explicit Edge Builders/Date Notes.md`
4. Return content with source path

**Result:** "Date Notes are documented in `breadcrumbs-docs-vault/Explicit Edge Builders/Date Notes.md`. They let you automatically create edges between notes based on date-based naming conventions. Related: `Layered Daily Notes.md` guide."

### Example 2: "What does Breadcrumbs call the thing where parent-of-parent becomes grandparent?"

**User says:** "What does Breadcrumbs call the thing where parent-of-parent becomes grandparent?"

**Actions taken:**
1. Query describes transitive chaining → maps to `Implied Edge Builders/`
2. Read `Implied Edge Builders/Implied Edge Builders.md` — confirms `[[Transitive Implied Relations]]`
3. Read `Implied Edge Builders/Transitive Implied Relations.md`
4. Return: this is called **Transitive Implied Relations**, using chain syntax like `[parent, parent] -> grandparent`

**Result:** "Breadcrumbs calls this **Transitive Implied Relations**. The chain syntax is `[parent, parent] -> grandparent`. Source: `breadcrumbs-docs-vault/Implied Edge Builders/Transitive Implied Relations.md`."

### Example 3: "How do I see a breadcrumb trail at the top of my notes?"

**User says:** "How do I see a breadcrumb trail at the top of my notes?"

**Actions taken:**
1. Query mentions "breadcrumb trail" → maps to `Views/`
2. Read `Views/Views.md` — find `[[Trail View]]` under `[[Page Views]]`
3. Read `Views/Trail View.md`
4. Return content with source path, mention Page Views as the parent concept

**Result:** "The **Trail View** renders a breadcrumb trail at the top of notes. It's one of the **Page Views**. Source: `breadcrumbs-docs-vault/Views/Trail View.md`. Related: `Page Views.md`, `Previous-Next View.md`."

## Common Issues

### "I can't find a page for X"

1. Check aliases: some pages have YAML aliases (e.g., `Edge Fields.md` has aliases `edge fields`, `field`; `Concepts.md` has alias `Reference`; `Explicit Edge Builders.md` has alias `explicit`; `Implied Edge Builders.md` has alias `implied`).
2. Search with: `rg -in '<term>' breadcrumbs-docs-vault/ --type md`
3. If the concept spans multiple pages, start with `Concepts.md` which defines foundational terms.

### "Is there docs for the Breadcrumbs API?"

`API.md` exists but is a placeholder — it only documents BCAPI at a high level. There is no comprehensive API reference in this vault export.

### "Where are the images referenced in the docs?"

Images are in `breadcrumbs-docs-vault/Images/` and referenced via `![[filename.png]]` embed syntax. They are screenshots, not editable diagrams.

### "The user asks about a feature not in the docs"

If a term doesn't match any page or alias in the vault map above, it may not be a Breadcrumbs feature. Say so explicitly rather than guessing. Check `Home.md` for the canonical feature list.

### "User confuses Breadcrumbs terms with generic terms"

Common mappings from generic terms to Breadcrumbs terminology:
- "link types" / "typed links" → `Edge Fields` (the fields) + `Typed Links` (the edge builder)
- "hierarchy" / "parent-child" → `Edge Fields` with `up`/`down` or custom `parent`/`child`
- "auto-generated links" → `Explicit Edge Builders` (from existing structure) or `Implied Edge Builders` (from transitive rules)
- "navigation" → `Views` (visual) or `Commands` like `Jump to First Neighbour` (keyboard)
- "autocomplete" → `Suggesters/`
- "ignore a note" → `Note Attributes` (`BC-ignore-in-edges`, `BC-ignore-out-edges`)

## Related skills
- `breadcrumbs` — for broader Breadcrumbs workflow routing
- `breadcrumbs-terminology` — to resolve naming questions while navigating docs
- `breadcrumbs-testing-guide` — to validate targets and links after locating pages
