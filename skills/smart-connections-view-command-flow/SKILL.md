---
name: smart-connections-view-command-flow
description: Use this skill to implement Smart Connections view and command wiring in `src/main.js` and `src/views/**` with lifecycle-safe registration, cleanup, and leaf-location persistence. Reach for it when the user says "new view", "settings tab", "command", or "help modal". Do NOT use it for pure utility logic or stylesheet-only changes.
paths:
  - src/main.js
  - src/views/**/*.js
  - src/utils/view_leaf_location.js
  - src/utils/connections_view_refresh_handler.js
  - src/views/settings_tab.js
---
# Smart Connections View and Command Flow

Use this skill when wiring Smart Connections views, commands, ribbon actions, settings-tab entry points, or workspace-leaf persistence so registration and teardown stay aligned with the plugin lifecycle.

## Critical
- Put registration in `src/main.js` inside `SmartConnectionsPlugin extends SmartPlugin`, and keep cleanup on the plugin lifecycle. Do not register commands, views, or workspace listeners from render callbacks.
- Register each custom view once with `this.registerView(...)`; open it by its view type, not by creating ad hoc instances in commands.
- Use `src/utils/view_leaf_location.js` for any command that should reopen in the same pane or restore the previous leaf. Do not hand-roll leaf persistence.
- Keep settings UI in `src/views/settings_tab.js` and reuse `render_settings_config` from `obsidian-smart-env` instead of building a separate settings renderer.

## Instructions
1. Find the existing flow before changing anything.
   - Inspect `src/main.js`, `src/views/connections_item_view.js`, `src/views/lookup_item_view.js`, `src/views/release_notes_view.js`, and `src/views/settings_tab.js`.
   - Match the repo's naming pattern: existing files use `src/views/connections_item_view.js` and `src/views/lookup_item_view.js`, view classes use `PascalCase`, and view type strings are stable constants used by `registerView(...)`.
   Verify the closest existing view/command flow is identified before proceeding to the next step. This step uses the output from no prior step.

2. Build the new view shell in `src/views/connections_item_view.js`-style files (for example, `src/views/release_notes_view.js` for command/panel pages).
   - Use Obsidian API imports from `obsidian` the same way the existing view files do.
   - Export a view class with the same lifecycle shape as the current views:
     - `getViewType()`
     - `getDisplayText()`
     - `onOpen()`
     - `onClose()`
   - Render into `this.contentEl`, and clear with `this.contentEl.empty()` before rerendering.
   - If the request is for a settings-style page, keep the actual settings UI in `src/views/settings_tab.js` and use `render_settings_config` from `obsidian-smart-env`.
   Verify the view opens and closes without duplicate DOM or event listeners before proceeding to the next step. This step uses the output from Step 1.

```js
// src/views/connections_item_view.js
export class ConnectionsItemView extends ItemView {
  getViewType() { return 'connections-item-view'; }
  getDisplayText() { return 'Connections item'; }
  onOpen() { /* render */ }
  onClose() { /* cleanup */ }
}
```

3. Wire the command/view in `src/main.js`.
   - Add registration inside the plugin `onload()` block.
   - Use `this.registerView(viewType, leaf => new YourView(leaf))` for custom panes.
   - Use `this.addCommand({ id, name, callback })` for command palette actions.
   - Add ribbon icons only from `onload()`, and keep the callback idempotent.
   - If the flow opens a modal or help panel, instantiate it from the command callback; do not register the modal globally.
   Verify the command appears once in the command palette and the ribbon/action opens the intended view before proceeding to the next step. This step uses the output from Step 2.

```js
this.addCommand({
  id: 'open-connections-item-view',
  name: 'Open: Connection item view',
  callback: () => {
    const leaf = this.app.workspace.getLeaf('tab');
    leaf.setViewState({ type: 'connections-item-view', active: true });
  }
});
```

4. Persist and restore leaf location when the command should reopen an existing pane.
   - Import the helpers from `src/utils/view_leaf_location.js` instead of writing ad hoc workspace logic.
   - Store the current leaf/location state before switching views.
   - Restore into the same leaf or workspace region on the next invocation.
   - If the existing flow is a refresh flow rather than a reopen flow, compare it with `src/utils/connections_view_refresh_handler.js` and reuse the same workspace behavior.
   Verify the view reopens in the same pane after a second invocation or reload before proceeding to the next step. This step uses the output from Step 3.

5. Keep lifecycle edges safe.
   - Register workspace events through the plugin lifecycle helpers already used in `src/main.js` so they auto-dispose.
   - Do not attach DOM listeners from command callbacks; attach them in `onOpen()` and remove them in `onClose()`.
   - Keep any settings mutations inside the settings tab or collection settings file, not in the command handler.
   Verify `npm run build` succeeds before finishing. This step uses the output from Step 4.

## Examples
- User says: "Add a help modal command for the settings tab."
  - Actions taken: add a command in `src/main.js`; make the callback open the existing `src/views/settings_tab.js` style entry point or a dedicated view in `src/views/release_notes_view.js`; keep registration inside `onload()`; reuse `src/utils/view_leaf_location.js` if the panel should reopen in-place.
  - Result: the command appears once in Obsidian, opens the settings/help UI safely, and unloads cleanly with the plugin.

```js
// src/main.js
this.registerView('connections-item-view', leaf => new ConnectionsItemView(leaf));
this.registerView('connections-codeblock-view', leaf => new ConnectionsCodeblockView(leaf));
```

## Common Issues
- If you see "Cannot read properties of undefined (reading 'workspace')" in a command callback:
  1. Move the registration into `SmartConnectionsPlugin.onload()`.
  2. Use `this.app.workspace` from the plugin instance, not a free variable.
  3. Guard the active leaf before calling `setViewState`.

- If you see "View type already registered":
  1. Check `src/main.js` for duplicate `this.registerView(...)` calls.
  2. Ensure the view type is registered only once during plugin load.

- If you see "Command appears twice in the palette":
  1. Search for duplicate `this.addCommand(...)` entries in `src/main.js`.
  2. Remove any command registration from helper functions that run more than once.

- If the view opens in a new split every time:
  1. Use the helpers from `src/utils/view_leaf_location.js`.
  2. Reuse the existing leaf instead of calling `workspace.getLeaf(true)` unconditionally.

- If settings UI renders but changes do not persist:
  1. Keep the UI logic in `src/views/settings_tab.js`.
  2. Reuse `render_settings_config` from `obsidian-smart-env`.
  3. Verify the settings object passed to the tab is the same object used by the plugin or collection.

## Related skills
- `smart-connections` — for broader Smart Connections workflow routing
- `smart-connections-component-patterns` — when view work also changes rendered components
- `smart-connections-collection-pipeline` — when command/view flow depends on collection behavior
