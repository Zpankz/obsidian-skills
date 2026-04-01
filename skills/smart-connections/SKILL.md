---
name: smart-connections
description: "Use this umbrella skill when a task spans multiple Obsidian Smart Connections development workflows and you need to route to the right specialized smart-connections-* skill."
---

# Smart Connections Toolkit

Use this umbrella skill when a task spans multiple Smart Connections plugin workflows and you need to route to the right specialized skill.

This toolkit is grounded in the generated project context from `/Users/mikhail/projects/plugins/obsidian-smart-connections/CLAUDE.md`.

## Route to these skills

### Components and rendering
- `smart-connections-component-patterns` — build or edit `src/components/**` using the project’s `build_html` → `render` → `post_process` lifecycle

### Views and commands
- `smart-connections-view-command-flow` — add or edit Obsidian views, commands, ribbon actions, and view-leaf persistence flows

### Collection and item pipelines
- `smart-connections-collection-pipeline` — update collection defaults, action pre-processing, scoring/filtering, post-processing, and pinned/hidden result behavior

### Tests and migrations
- `smart-connections-ava-and-migration-harness` — add or update focused Ava regression tests and migration tests

## Quick decision guide
- "Add or change a component" → `smart-connections-component-patterns`
- "Add a view, command, or settings-tab flow" → `smart-connections-view-command-flow`
- "Change scoring, filters, pinned/hidden behavior, or collection settings" → `smart-connections-collection-pipeline`
- "Add tests or fix migration coverage" → `smart-connections-ava-and-migration-harness`

## Relevant source context
- `/Users/mikhail/projects/plugins/obsidian-smart-connections/CLAUDE.md`
- `src/main.js`
- `src/views/**`
- `src/components/**`
- `src/collections/**`
- `src/items/**`
- `src/actions/**`
- `src/utils/**`
- `migrations/**`

## Related skills
- `smart-connections-component-patterns` — for component composition and render lifecycles
- `smart-connections-view-command-flow` — for command, view, ribbon, and leaf-wiring changes
- `smart-connections-collection-pipeline` — for scoring, filtering, and pipeline behavior changes
- `smart-connections-ava-and-migration-harness` — for focused regression and migration coverage
- `obsidian-dev` — for broader Obsidian implementation and debugging patterns
- `obsidian-plugin-dev` — for plugin lifecycle and API guidance

## Notes
- Smart Connections in this generated context is a JavaScript Obsidian plugin with AVA tests and build/release scripts.
- Prefer the specialized smart-connections-* skill when the task is narrow and obvious.
