---
name: obsidian-plugin-react-performance
description: Optimize React-based Obsidian plugin UI for responsiveness, bundle size, and render efficiency. Trigger on laggy views, excessive rerenders, or lazy-loading needs.
---

# Obsidian Plugin React Performance

Use this skill when a plugin already uses React and performance or responsiveness matters more than adding new features.

## Typical triggers
- "This view rerenders constantly"
- "Typing in this search box is laggy"
- "Can we lazy-load this heavy panel?"
- "Why is this React plugin UI janky?"
- "Which optimizations matter most here?"

## Priorities for Obsidian plugins

### 1. Bundle and load cost
- reduce initial bundle weight
- lazy-load heavy components when they are not needed immediately
- avoid broad barrel imports in hot UI paths
- defer non-critical third-party code

### 2. Re-render control
- move expensive computation behind memoized components when justified
- avoid deriving state through effects when render-time derivation is sufficient
- avoid inline component definitions inside parent components
- use transitions or deferred values for non-urgent UI updates

### 3. Rendering quality
- use explicit conditional rendering instead of risky `&&` patterns
- hoist static JSX where helpful
- reduce unnecessary browser work in long or dense views

### 4. Client-side event and storage discipline
- deduplicate global listeners when many components subscribe
- use passive listeners for scroll-like events
- keep storage reads and writes disciplined and versioned

### 5. Async structure
- parallelize independent work
- defer awaits until they are genuinely needed
- avoid cold-path async work behind cheap synchronous guards

## Especially relevant reference files

- `../obsidian-plugin-react-best-practices/references/rules/bundle-dynamic-imports.md`
- `../obsidian-plugin-react-best-practices/references/rules/bundle-barrel-imports.md`
- `../obsidian-plugin-react-best-practices/references/rules/bundle-defer-third-party.md`
- `../obsidian-plugin-react-best-practices/references/rules/rerender-memo.md`
- `../obsidian-plugin-react-best-practices/references/rules/rerender-derived-state-no-effect.md`
- `../obsidian-plugin-react-best-practices/references/rules/rerender-no-inline-components.md`
- `../obsidian-plugin-react-best-practices/references/rules/rendering-conditional-render.md`
- `../obsidian-plugin-react-best-practices/references/rules/client-event-listeners.md`
- `../obsidian-plugin-react-best-practices/references/rules/client-passive-event-listeners.md`
- `../obsidian-plugin-react-best-practices/references/rules/async-parallel.md`
- `../obsidian-plugin-react-best-practices/references/rules/async-defer-await.md`
- `../obsidian-plugin-react-best-practices/references/rules/async-cheap-condition-before-await.md`

## Related skills
- `obsidian-plugin-react-best-practices`
- `obsidian-plugin-react-components`
- `obsidian-plugin-shadcn-ui`
- `obsidian-plugin-shadcn-styling`
- `obsidian-plugin-css-styling`
- `obsidian-plugin-accessibility`
- `obsidian-plugin-dev`
