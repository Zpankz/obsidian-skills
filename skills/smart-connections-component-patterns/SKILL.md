---
name: smart-connections-component-patterns
description: Use this skill to build or edit Smart Connections components in `src/components/**` with the project’s `build_html` → `render` → `post_process` lifecycle, menu actions, and state-aware UI helpers. Reach for it when the user says "add component", "edit connections-list-item", or changes files under `src/components/`. Do NOT use it for migrations, release scripts, or non-component view/settings work.
paths:
  - src/components/**
  - src/components/**/*.js
  - src/components/**/*.css
---
# Smart Connections Component Patterns

Use this skill when editing or creating Smart Connections UI components under `src/components/**`, especially when you need to preserve the project’s component lifecycle, listener guards, and env/settings fallbacks.

## Critical
- Keep component work inside `src/components/**`; do not move UI logic into `src/main.js`, release scripts, or migration files.
- Match the existing component lifecycle used in this repo: `build_html(...)` → `render(...)` → `post_process(...)`.
- Guard all event attachment with `if (!container._has_listeners)` so rerenders do not duplicate handlers.
- Prefer existing helpers and patterns from:
  - `src/components/connections-list/v4.js`
  - `src/components/connections-list-item/v3.js`
  - `src/components/connections-view/v3.js`
  - `src/components/connections_codeblock.js`
  - `src/components/lookup/item_view.js`
- Keep fallbacks explicit, especially `opts.connections_settings ?? env.connections_lists.settings` or the equivalent env fallback used by nearby components.

## Instructions
1. **Pick the closest reference component before coding.**
   - For list item UI, start with `src/components/connections-list-item/v3.js`.
   - For list rendering, start with `src/components/connections-list/v4.js`.
   - For main view shells, start with `src/components/connections-view/v3.js` or `src/components/connections_codeblock.js`.
   - For lookup-style item UI, start with `src/components/lookup/item_view.js`.
   - Verify the target belongs in `src/components/**` and not `src/views/**` before proceeding to the next step.
   - This step uses the project context and existing component files as the source of truth.

```js
// src/components/connections-list/v4.js
// Start from this exact file when updating list rendering behavior.
```

2. **Copy the existing component shape exactly.**
   - Implement or edit the file with the same trio of methods used elsewhere in this repo:
     - `build_html(...)`
     - `render(...)`
     - `post_process(...)`
   - Use `this.create_doc_fragment(...)` when building DOM, `this.empty(...)` when replacing content, and `this.apply_style_sheet(...)` when the component needs CSS.
   - Keep naming consistent with the local file family, for example `connections_list_v4`, `connections_list_item_v3`, or `connections_view_v3`.
   - Verify the component can render from a fresh fragment before proceeding to the next step.
   - This step uses the output from Step 1.

```js
// src/components/connections-list-item/v3.js
build_html(opts, env) { return this.create_doc_fragment(); }
render(_state, opts, env) { this.empty(this.el); this.el.append(...); }
post_process(state, opts, env) { /* wire events + behavior */ }
```

3. **Wire DOM markers and actions the same way the repo already does.**
   - Add `data-` attributes for anything the UI needs to query later.
   - Keep click, drag, and context-menu handlers idempotent with `if (!container._has_listeners)`.
   - Reuse existing integrations instead of writing new ones:
     - `register_item_drag`
     - `register_item_hover_popover`
     - `open_source`
   - Verify each listener fires once per container and still works after rerender before proceeding to the next step.
   - This step uses the output from Step 2.

```js
const actionEl = container.querySelector('[data-action="open"]');
if (!container._has_listeners) {
  container.addEventListener('click', (event) => {
    if (actionEl && actionEl.contains(event.target)) {
      open_source(event, source, env);
    }
  });
  container._has_listeners = true;
}
```

4. **Thread settings and state through the same fallback chain used in the codebase.**
   - When a component needs settings, read from explicit options first and then fallback to env state, for example:
     - `opts.connections_settings ?? env.connections_lists.settings`
   - Keep mutable UI state isolated; derive display state from input parameters, not globals.
   - If you need pause/state behavior, mirror the patterns in `src/utils/pause_controls.js` and `src/utils/connections_list_item_state.js`.
   - Verify the component produces the same output when called with the same inputs before proceeding to the next step.
   - This step uses the output from Step 3.

5. **Keep CSS colocated and applied through the component.**
   - If the component needs styling, place CSS beside the component in the same family as `src/components/connections_codeblock.css`.
   - Apply styles through `this.apply_style_sheet(...)` rather than inline strings.
   - Do not invent a new global style pipeline for a single component.
   - Verify the component still loads and styles correctly in Obsidian before proceeding to the next step.
   - This step uses the output from Step 4.

6. **Validate with the repo’s actual commands before finishing.**
   - Run `npm run build` after component changes.
   - If you changed shared logic used by the component, run `npm test`.
   - If you changed helper behavior that already has targeted tests, run the relevant AVA commands, for example:
     - `npx ava src/utils/format_connections_as_links.test.js src/utils/connections_list_item_state.test.js`
   - Verify the build is clean before you consider the component done.
   - This step uses the output from Step 5.

## Examples
- **User says:** "Add a new action button to the connections list item."
  - **Actions taken:** Open `src/components/connections-list-item/v3.js`, mirror the existing `build_html` / `render` / `post_process` structure, add a `data-action` marker, attach the handler inside `if (!container._has_listeners)`, and fallback to `opts.connections_settings ?? env.connections_lists.settings` for behavior toggles.
  - **Result:** The new button renders like the existing list item UI, triggers once per click, and respects the current settings state.

```js
// src/components/connections-list-item/v3.js
// Example data marker used by tests and event delegation:
container.dataset.action = 'open-item';
```

- **User says:** "Edit the connections list component to show an extra label."
  - **Actions taken:** Update `src/components/connections-list/v4.js`, keep `this.create_doc_fragment(...)` for DOM construction, preserve `post_process(...)` for wiring, and run `npm run build` to confirm the component still composes correctly.
  - **Result:** The list layout changes without breaking rerenders or duplicated listeners.

```js
// src/components/connections-list/v4.js
const fragment = this.create_doc_fragment(...);
this.empty(this.container);
this.container.append(fragment);
```

## Common Issues
- **If you see `TypeError: Cannot read properties of undefined (reading 'settings')`:**
  1. Check the component’s settings access path.
  2. Use the repo pattern `opts.connections_settings ?? env.connections_lists.settings`.
  3. Verify the env value is available before proceeding.

- **If you see duplicate click behavior or handlers firing twice:**
  1. Find the listener attachment block in `post_process(...)`.
  2. Wrap the attachment in `if (!container._has_listeners)`.
  3. Set the guard flag after wiring listeners, then rerun the component.

- **If you see `TypeError: this.apply_style_sheet is not a function`:**
  1. Confirm the code is running inside the component instance pattern used in `src/components/**`.
  2. Call `this.apply_style_sheet(...)` only from the component lifecycle, not from a free function.
  3. Verify the component still uses the same class/helper shape as the nearby reference file.

- **If the component renders in code but never appears in Obsidian:**
  1. Confirm the component key is registered in `smart_env.config.js` under `components`.
  2. Match the export name and file name to the convention used by the family (`connections_list_v4`, `connections_list_item_v3`, `connections_view_v3`).
  3. Rebuild with `npm run build` and reload the plugin.

- **If styles are missing after the component loads:**
  1. Confirm the stylesheet is colocated with the component family, like `src/components/connections_codeblock.css`.
  2. Make sure the component calls `this.apply_style_sheet(...)`.
  3. Verify the CSS file path matches the component file path exactly before proceeding.

## Related skills
- `smart-connections` — for broader Smart Connections workflow routing
- `smart-connections-view-command-flow` — when component work also changes a view shell or command path
- `smart-connections-collection-pipeline` — when rendering depends on pipeline output shape
- `obsidian-dev` — for wider Obsidian implementation patterns
