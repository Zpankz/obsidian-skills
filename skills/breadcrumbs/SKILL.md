---
name: breadcrumbs
description: "Use this umbrella skill when a task spans multiple Breadcrumbs documentation workflows and you need to route to the right specialized breadcrumbs-* skill."
---

# Breadcrumbs Toolkit

Use this umbrella skill when a task spans multiple Breadcrumbs documentation workflows and you need to route to the right specialized skill.

These skills are grounded in the generated Breadcrumbs docs context under `breadcrumbs-docs-vault/`.

## Route to these skills

### Docs navigation and discovery
- `breadcrumbs-nav` — find the right docs page, command, view, builder, guide, or top-level concept

### Editing and terminology
- `breadcrumbs-edit` — create or edit Breadcrumbs docs pages using vault conventions
- `breadcrumbs-terminology` — enforce canonical Breadcrumbs terms like `Edge Fields`, `Field Groups`, and `Transitive Implied Relations`
- `breadcrumbs-code-conventions` — apply docs-vault formatting patterns like wikilinks, image embeds, frontmatter, Mermaid, and inline Dataview fields

### Workflow and validation
- `breadcrumbs-development-workflow` — orient to the docs vault, editing flow, and commit/Caliber workflow
- `breadcrumbs-testing-guide` — validate links, embeds, terminology, announcement chains, and markdown integrity

## Quick decision guide
- "Where are the docs for X?" → `breadcrumbs-nav`
- "Update this Breadcrumbs page" → `breadcrumbs-edit`
- "Check the wording/terms" → `breadcrumbs-terminology`
- "Make this match the docs style" → `breadcrumbs-code-conventions`
- "How do I work in this docs vault?" → `breadcrumbs-development-workflow`
- "Validate the docs before commit" → `breadcrumbs-testing-guide`

## Canonical source area
- `breadcrumbs-docs-vault/Home.md`
- `breadcrumbs-docs-vault/Concepts.md`
- `breadcrumbs-docs-vault/Edge Fields.md`
- `breadcrumbs-docs-vault/Field Groups.md`
- `breadcrumbs-docs-vault/Explicit Edge Builders/`
- `breadcrumbs-docs-vault/Implied Edge Builders/`
- `breadcrumbs-docs-vault/Views/`
- `breadcrumbs-docs-vault/Commands/`
- `breadcrumbs-docs-vault/Suggesters/`
- `breadcrumbs-docs-vault/Guides/`

## Related skills
- `breadcrumbs-edit` — for actual page creation and edits
- `breadcrumbs-nav` — for locating the right docs page or concept quickly
- `breadcrumbs-terminology` — for canonical Breadcrumbs vocabulary and naming checks
- `obsidian-markdown` — for general Obsidian markdown authoring patterns used inside docs pages
- `obsidian-links` — for wikilink validation and repair
- `dataview` — because Breadcrumbs docs use Dataview-style inline fields in examples

## Notes
- Prefer the specialized breadcrumbs subskill when the task is narrow and obvious.
- Use this umbrella skill when the task spans multiple Breadcrumbs docs concerns.
- Do not invent Breadcrumbs settings or APIs beyond what the docs export contains.
