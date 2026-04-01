---
name: obsidian-plugin-shadcn-composition
description: Use this skill when assembling richer React-based Obsidian plugin interfaces with shadcn/ui components, especially if the user mentions settings forms, cards, tabs, dialogs, sheets, onboarding flows, empty states, alerts, or wants help choosing the right primitives for a plugin screen. Covers forms, cards, tabs, overlays, alerts, empty states, skeletons, separators, avatars, and component-composition rules that keep plugin UI accessible and maintainable.
---

# Obsidian Plugin shadcn Composition

Use this skill when building plugin settings pages, modals, onboarding flows, dashboards, or side panels from shadcn/ui primitives and you want the result to feel coherent rather than pieced together.

## Typical triggers
- "What shadcn components should I use for this settings page?"
- "Can you turn this custom markup into proper cards/dialogs/forms?"
- "I need a cleaner onboarding modal for my plugin"
- "Which primitive fits this side panel or empty state?"
- "Help me structure this form with shadcn"

## Prefer another skill when
- the main issue is visual theming or token usage → `obsidian-plugin-shadcn-styling`
- the main issue is component API architecture or prop drilling → `obsidian-plugin-react-components`
- the repo is not using shadcn/ui at all → `obsidian-plugin-css-styling` or `obsidian-plugin-dev`

## What this skill is best at

- choosing the right primitive for the interaction
- structuring forms with `FieldGroup` and `Field`
- composing cards, tabs, dialogs, sheets, drawers, alerts, empty states, and badges correctly
- preventing common composition mistakes like missing group containers or missing overlay titles
- replacing custom markup with standard reusable components where possible

## Obsidian-plugin use cases

- plugin settings tab with labeled controls and validation
- onboarding wizard or setup assistant
- dashboard-style custom view with cards, tabs, and badges
- modal workflows for configuration, confirmation, or search
- empty-state and loading-state design for views with async data

## Rules to keep front of mind

- forms use `FieldGroup` + `Field`
- grouped menu/select/command items stay inside their Group wrappers
- dialogs, sheets, and drawers require visible or screen-reader-only titles
- use full `Card` composition, not one oversized `CardContent`
- use `Skeleton`, `Alert`, `Empty`, `Separator`, and `Badge` instead of homegrown substitutes
- use `ToggleGroup` for small option sets instead of manual button state wiring

## Reference files

- `../obsidian-plugin-shadcn-ui/references/rules/forms.md`
- `../obsidian-plugin-shadcn-ui/references/rules/composition.md`
- `../obsidian-plugin-shadcn-ui/references/rules/base-vs-radix.md`

## Related skills
- `obsidian-plugin-shadcn-ui`
- `obsidian-plugin-shadcn-styling`
- `obsidian-plugin-accessibility`
- `obsidian-plugin-ui-ux`
- `obsidian-plugin-react-components`
- `obsidian-plugin-react-best-practices`
- `obsidian-plugin-dev`
