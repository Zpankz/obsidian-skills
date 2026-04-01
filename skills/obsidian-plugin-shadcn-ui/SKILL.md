---
name: obsidian-plugin-shadcn-ui
description: Use this skill when an Obsidian plugin UI is built with React, Tailwind, and shadcn/ui components, or when the user explicitly wants to introduce that stack for richer plugin settings pages, dialogs, sheets, sidebars, dashboards, onboarding flows, or custom views. Trigger when the user mentions shadcn/ui, `components.json`, `shadcn init`, adding components like button/card/dialog, or making a React-based plugin UI substantially more polished. Covers shadcn CLI workflows, component selection, composition rules, styling rules, theming, and safe update workflows.
---

# Obsidian Plugin shadcn/ui

Use this umbrella skill when a plugin task needs polished React-based UI built with shadcn/ui, especially for settings tabs, dialogs, sheets, drawers, dashboards, sidebars, forms, and empty states.

## Typical triggers
- "Use shadcn for this plugin UI"
- "Add a card/dialog/table/sidebar to this plugin"
- "How do I initialize shadcn in this repo?"
- "Can we make this React-based plugin UI look like a real app?"
- "What shadcn components fit this settings or dashboard screen?"

## Important applicability check

Only apply this skill when the plugin actually uses, or intentionally plans to add, a React + Tailwind + shadcn-style frontend stack.

- Do **not** assume ordinary Obsidian plugins already have `components.json`, Tailwind, or shadcn CLI support.
- If the repo does not already use shadcn/ui, first confirm whether the user wants to add that stack.
- For non-React or DOM-helper-first plugin UIs, prefer `obsidian-plugin-css-styling`, `obsidian-plugin-accessibility`, and `obsidian-plugin-ui-ux`.

## Core principles

1. **Use existing components first** before inventing custom markup.
2. **Compose, do not reinvent** settings layouts, cards, tabs, alerts, empty states, and overlays.
3. **Prefer built-in variants and semantic tokens** over one-off styling overrides.
4. **Preview CLI changes before overwriting local customizations**.
5. **Keep plugin UI aligned with Obsidian expectations** for accessibility, focus behavior, and restraint.

## Recommended Obsidian-plugin workflow

1. Confirm the frontend stack: React, Tailwind, `components.json`, package manager, alias paths.
2. If shadcn is already present, inspect project info with the correct package runner.
3. Use CLI search/docs before adding components.
4. For existing components, prefer `--dry-run` and `--diff` before updates.
5. Map shadcn components into plugin-specific surfaces:
   - settings tab
   - modal or dialog
   - side panel or sheet
   - custom view or dashboard
   - onboarding or empty state
6. After composition, apply `obsidian-plugin-accessibility`, `obsidian-plugin-css-styling`, and `obsidian-plugin-react-best-practices` for final polish.

## High-value rules to enforce

- Use semantic colors and variants, not raw color utilities for component theming.
- Use `gap-*`, not `space-x-*` or `space-y-*`.
- Use `FieldGroup` and `Field` for forms instead of ad hoc stacks.
- Put grouped items inside their required Group components.
- Give `Dialog`, `Sheet`, and `Drawer` an explicit title.
- Use `Alert`, `Empty`, `Skeleton`, `Separator`, and `Badge` instead of custom equivalents.
- Use the configured icon library and `data-icon` conventions.
- Use `--dry-run`, `--diff`, and `--view` before overwriting generated component code.

## Bundled resources

- `references/cli.md` — shadcn CLI command and flag reference
- `references/customization.md` — theming, CSS variables, and component customization
- `references/rules/styling.md` — layout, tokens, spacing, and class usage rules
- `references/rules/forms.md` — form layout and validation patterns
- `references/rules/composition.md` — component composition and selection guidance
- `references/rules/icons.md` — icon import and placement rules
- `references/rules/base-vs-radix.md` — primitive differences that affect API usage

## Related skills
- `obsidian-plugin-shadcn-styling`
- `obsidian-plugin-shadcn-composition`
- `obsidian-plugin-react-best-practices`
- `obsidian-plugin-react-performance`
- `obsidian-plugin-react-components`
- `obsidian-plugin-css-styling`
- `obsidian-plugin-accessibility`
- `obsidian-plugin-ui-ux`
- `obsidian-plugin-dev`
- `obsidian-dev`
- `obsidian-ops`
