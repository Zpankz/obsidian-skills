---
name: extended-graph
description: "Use this umbrella skill when a task spans multiple Obsidian Extended Graph development workflows and you need to route to the right specialized extended-graph-* skill."
---

# Extended Graph Toolkit

Use this umbrella skill when a task spans multiple `obsidian-extended-graph` development workflows and you need to route to the right specialized skill.

This toolkit is grounded in the generated project context from `/Users/mikhail/projects/plugins/obsidian-extended-graph/CLAUDE.md`.

## Route to these skills

### Feature work
- `extended-graph-plugin-feature` — add a new plugin feature following the established feature-flag, settings, and barrel-export pattern

### Stats and graph metrics
- `extended-graph-stat-calculator` — add a new node or link stat calculator and register it in the calculator factories

### Settings UI
- `extended-graph-setting-section` — add a new settings section using `SettingsSection` or `SettingsSectionPerGraphType`

### Interactive filters
- `extended-graph-interactive-type` — add a new interactive filter type wired through `InteractiveManager`, legend UI, and settings

## Quick decision guide
- "Add a feature to Extended Graph" → `extended-graph-plugin-feature`
- "Add a new node/link metric" → `extended-graph-stat-calculator`
- "Add a new settings section" → `extended-graph-setting-section`
- "Add a new interactive/filter type" → `extended-graph-interactive-type`

## Relevant source context
- `/Users/mikhail/projects/plugins/obsidian-extended-graph/CLAUDE.md`
- `src/internal.ts` barrel export rule
- `src/settings/`
- `src/statsCalculators/`
- `src/graph/interactiveManager.ts`
- `src/types/restrictedStrings.ts`
- `i18n/en.json`, `i18n/fr.json`, `i18n/zh.json`

## Related skills
- `extended-graph-plugin-feature` — for end-to-end feature additions
- `extended-graph-stat-calculator` — for node or link metric work
- `extended-graph-setting-section` — for settings-surface changes
- `extended-graph-interactive-type` — for new filter and legend interaction types
- `obsidian-dev` — for broader Obsidian implementation and debugging patterns
- `obsidian-plugin-dev` — for plugin API, lifecycle, and submission guidance

## Notes
- All internal imports go through `src/internal.ts`.
- Extended Graph has no formal test framework in this generated context; validate with `npm run build`.
- Prefer the specialized extended-graph-* skill when the task is narrow and obvious.
