---
name: obsidian-plugin-shadcn-styling
description: Style and theme an Obsidian plugin that already uses shadcn/ui. Trigger when the user wants a cleaner, more consistent, or more polished shadcn-based plugin UI.
---

# Obsidian Plugin shadcn Styling

Use this skill when the plugin already uses shadcn/ui and you need the UI to look more polished without drifting into brittle custom styling.

## Typical triggers
- "Make this settings page prettier"
- "These shadcn components look inconsistent"
- "Can we theme this plugin view better?"
- "Replace these raw Tailwind color classes with something cleaner"
- "Why does this dialog feel visually off?"

## Prefer another skill when
- the repo is not clearly using shadcn/ui or Tailwind → `obsidian-plugin-css-styling`
- the issue is component architecture or prop design → `obsidian-plugin-react-components`
- the issue is which form/card/dialog primitives to compose → `obsidian-plugin-shadcn-composition`
- the issue is copy, labels, or settings wording → `obsidian-plugin-ui-ux`

## Focus areas

- semantic colors instead of raw palette classes
- built-in variants before custom overrides
- `className` for layout, not for rewriting component internals
- `gap-*` and `size-*` conventions
- icon-library alignment and `data-icon` placement
- CSS-variable based theme customization
- adding custom tokens safely when built-ins are insufficient

## Obsidian-specific guidance

When applying shadcn styling in an Obsidian plugin:
- keep the UI visually restrained so it still feels at home inside Obsidian
- prefer theme tokens and CSS variables over hard-coded light/dark overrides
- verify focus states and contrast with `obsidian-plugin-accessibility`
- use `obsidian-plugin-css-styling` for broader plugin-level container scoping and coexistence with Obsidian styles

## Good defaults

- prefer `variant="outline"`, `variant="secondary"`, etc. before custom classes
- prefer `bg-primary`, `text-muted-foreground`, `text-destructive`, etc. over raw color utilities
- use `cn()` for conditional classes
- avoid manual z-index tweaks on overlay primitives
- customize through global variables or explicit component variants, not scattered ad hoc overrides

## Reference files

- `../obsidian-plugin-shadcn-ui/references/rules/styling.md`
- `../obsidian-plugin-shadcn-ui/references/rules/icons.md`
- `../obsidian-plugin-shadcn-ui/references/customization.md`

## Related skills
- `obsidian-plugin-shadcn-ui`
- `obsidian-plugin-shadcn-composition`
- `obsidian-plugin-react-components`
- `obsidian-plugin-css-styling`
- `obsidian-plugin-accessibility`
- `obsidian-plugin-ui-ux`
- `obsidian-plugin-dev`
