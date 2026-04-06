---
name: obsidian-plugin-react-components
description: Design or refactor React component architecture in Obsidian plugins. Trigger on compound components, context providers, prop drilling, or scaling plugin UI structure.
---

# Obsidian Plugin React Components

Use this skill when a React-based Obsidian plugin needs cleaner component architecture, not just better visuals.

Reach for it when the code already works but the component API is getting awkward, brittle, or hard to extend.

## Typical triggers

- "This component has too many props"
- "Can we refactor this settings panel to be more composable?"
- "I keep adding boolean flags to this modal or view"
- "Should this use context or compound components?"
- "How should I structure reusable React components for this plugin?"
- "This dashboard/view hierarchy is turning into prop drilling"

## What this skill focuses on

- composition over configuration
- compound components over monolithic configurable widgets
- lifting shared state into providers
- reducing prop drilling across settings panes, dialogs, and custom views
- replacing brittle render-prop or boolean-mode APIs with clearer composition patterns
- designing reusable component APIs that still feel manageable in Obsidian plugin codebases

## Obsidian-plugin use cases

- reusable settings sections used in multiple tabs or plugin views
- modal workflows with shared state across body, preview, and footer actions
- dashboards with cards, filters, and side panels that need coordinated state
- search, onboarding, or assistant panes that are growing beyond a single component file
- React wrappers around custom Obsidian views that need stable internal architecture

## Keep these decisions in order

1. If the issue is **component API shape**, use this skill.
2. If the issue is **visual styling or theming**, prefer `obsidian-plugin-shadcn-styling` or `obsidian-plugin-css-styling`.
3. If the issue is **which UI primitive to choose**, prefer `obsidian-plugin-shadcn-composition`.
4. If the issue is **runtime responsiveness or rerenders**, pair this skill with `obsidian-plugin-react-performance`.

## High-value patterns

- Replace mode booleans with explicit variants or composable subcomponents.
- Put shared state in provider components when sibling UI needs access.
- Prefer `children` composition over `renderHeader`, `renderFooter`, and similar render props unless the parent truly needs to inject data.
- Use context-backed compound components when several subparts belong to one conceptual widget.
- Keep state interfaces explicit: state, actions, and lightweight meta.

## Bundled resources

- `references/rules/architecture-avoid-boolean-props.md`
- `references/rules/architecture-compound-components.md`
- `references/rules/state-lift-state.md`
- `references/rules/state-context-interface.md`
- `references/rules/state-decouple-implementation.md`
- `references/rules/patterns-children-over-render-props.md`
- `references/rules/patterns-explicit-variants.md`
- `references/README.md`

## Related skills
- `obsidian-plugin-react-best-practices`
- `obsidian-plugin-react-performance`
- `obsidian-plugin-shadcn-composition`
- `obsidian-plugin-shadcn-ui`
- `obsidian-plugin-ui-ux`
- `obsidian-plugin-dev`
- `obsidian-dev`
