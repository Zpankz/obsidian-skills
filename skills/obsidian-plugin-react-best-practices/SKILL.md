---
name: obsidian-plugin-react-best-practices
description: Use this skill when an Obsidian plugin frontend uses React and you want stronger rendering, state, bundle, and async performance patterns. Trigger when the user mentions rerenders, React lag, `useMemo`, `useEffect`, bundle size, slow dashboards, sluggish settings panes, dynamic imports, or React/Next.js best practices in a plugin UI. Adapts Vercel's React and Next.js best-practice guidance for plugin settings panes, custom views, dashboards, and other React-driven plugin UI.
---

# Obsidian Plugin React Best Practices

Use this umbrella skill when a plugin UI is built with React and you need performance-oriented guidance that goes beyond correctness.

## Typical triggers
- "This React view feels slow"
- "Do we need `useMemo` here?"
- "How can we reduce rerenders in this plugin panel?"
- "Should this be dynamically imported?"
- "Can you apply React best practices to this plugin UI?"

## Applicability check

This skill is most useful when the plugin has a React-based frontend.

- Many rules apply directly to client-side React in Obsidian plugin views, modals, and settings tabs.
- Some rules are **Next.js or server-component specific** and should only be applied when the plugin repo actually uses Next.js, SSR, RSC, or server actions.
- For non-React plugin UIs, prefer `obsidian-plugin-dev`, `obsidian-plugin-css-styling`, and `obsidian-plugin-accessibility`.

## Highest-value categories for Obsidian plugins

1. **Bundle size optimization** — important because plugin payload size affects startup and view-load cost.
2. **Re-render optimization** — especially important for settings panes, search UIs, dashboards, and graph-heavy panels.
3. **Rendering performance** — helps avoid sluggishness in larger plugin views.
4. **Client-side patterns** — useful for event listeners, browser storage, and deduplicated subscriptions.
5. **JavaScript hot-path cleanup** — helpful in large vault views, filtering, sorting, and repeated lookups.

## Categories included

- async waterfall elimination
- bundle-size optimization
- server-side performance
- client-side data fetching and subscriptions
- re-render optimization
- rendering performance
- JavaScript micro-performance
- advanced callback and initialization patterns

## Obsidian-specific adaptation notes

When using this skill in a plugin:
- prioritize the client-side React guidance first
- treat SSR/RSC/server-action rules as optional unless the project truly uses those technologies
- optimize for responsive note-adjacent UI rather than abstract benchmarks
- combine with `obsidian-plugin-shadcn-ui` when the plugin uses React + Tailwind + shadcn/ui
- combine with `obsidian-plugin-accessibility` so optimization never regresses usability

## Bundled resources

- `references/AGENTS.md` — compiled Vercel guide
- `references/README.md` — structure and maintenance notes
- `references/rules/` — individual rule files by category

## Related skills
- `obsidian-plugin-react-performance`
- `obsidian-plugin-react-components`
- `obsidian-plugin-shadcn-ui`
- `obsidian-plugin-shadcn-composition`
- `obsidian-plugin-accessibility`
- `obsidian-plugin-css-styling`
- `obsidian-plugin-dev`
- `obsidian-dev`
