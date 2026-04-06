---
name: smart-connections-collection-pipeline
description: Create or update Smart Connections collection, item, and action pipelines with scoring, filtering, and post-processing hooks. Trigger on "update scoring", "new action", or "collection settings".
paths:
  - src/collections/**
  - src/items/**
  - src/actions/**
  - src/utils/**
  - src/views/settings_tab.js
---
# Smart Connections Collection Pipeline

Use this skill when changing how Smart Connections collections, items, or actions normalize params, score and filter results, or preserve pinned and hidden-result semantics across the pipeline.

## Critical
- Use this skill only for pipeline changes in `src/collections/**`, `src/items/**`, `src/actions/**`, and the supporting utilities in `src/utils/**`.
- Never change the order of the pipeline in `src/items/connections_list.js`: `pre_process(params)` → `filter_and_score(params)` → `post_process(results, params)` → `merge_pinned_results(...)`.
- Preserve hidden-result filtering and frontmatter include/exclude behavior. Do not bypass `src/utils/filter_hidden_results.js` or `src/utils/merge_pinned_results.js`.
- Keep `src/actions/connections-list/pre_process.js` side-effect free except for mutating `params` with defaults.
- If settings are added or renamed, wire them through `src/collections/connections_lists.js` using the same key names the pipeline already reads. Do not create a separate settings surface unless the existing collection settings object already exposes it.

## Instructions
1. Identify the pipeline stage that owns the requested behavior.
   - Use `src/actions/connections-list/pre_process.js` for default params and normalization.
   - Use `src/items/connections_list.js` for filtering, scoring, and result merging.
   - Use `src/collections/connections_lists.js` for collection-level settings.
   - Use `src/utils/merge_pinned_results.js`, `src/utils/filter_hidden_results.js`, and `src/utils/connections_list_item_state.js` when the behavior depends on pinned/hidden state.
   - Verify the change belongs to one of those stages before proceeding to Step 2.

2. Update `src/actions/connections-list/pre_process.js` first when the request adds or changes defaults.
   - Mutate the incoming `params` object in place.
   - Keep the file focused on sane defaults only; do not add scoring logic, filtering, or UI concerns.
   - Keep the existing lower_snake_case file naming convention used by `src/actions/connections-list/pre_process.js`.
   - This step uses the output from Step 1.
   - Verify the final `params` shape contains every value needed by the downstream item pipeline before proceeding to Step 3.

3. Update `src/items/connections_list.js` next for scoring, filtering, and result composition.
   - Keep the repo’s deterministic flow: `pre_process(params)`, `filter_and_score(params)`, `post_process(results, params)`, then `merge_pinned_results(...)`.
   - Preserve existing frontmatter inclusion/exclusion checks before scoring.
   - Preserve hidden-result filtering before the final merge.
   - If you change scoring, keep pinned items pinned; do not let new sort logic push them behind regular results.
   - This step uses the output from Step 2.
   - Verify hidden notes stay hidden and pinned notes still appear in the expected position before proceeding to Step 4.

```js
// src/items/connections_list.js
const params = pre_process(rawParams);
const scored = filter_and_score(params);
const post = post_process(scored, params);
return merge_pinned_results(post, params);
```

4. Update `src/collections/connections_lists.js` when the request changes collection settings.
   - Keep setting keys aligned with the values consumed by `src/actions/connections-list/pre_process.js` and `src/items/connections_list.js`.
   - Reuse the same defaults the pipeline expects; do not duplicate default logic in the collection layer.
   - If the setting must be visible in the UI, expose it through the existing collection settings object instead of inventing a new settings path.
   - Do not touch `src/views/settings_tab.js` unless the collection settings object already requires it.
   - This step uses the output from Step 3.
   - Verify the setting persists and the item pipeline reads the value before proceeding to Step 5.

5. Add or update focused tests for the changed behavior.
   - Prefer existing utility tests such as `src/utils/filter_hidden_results.test.js`, `src/utils/merge_pinned_results.test.js`, and `src/utils/connections_list_item_state.test.js` when the behavior lives in a helper.
   - Cover helper behaviors that enforce the contract.
   - Run a targeted AVA check first:
     - `npx ava src/utils/format_connections_as_links.test.js src/utils/connections_list_item_state.test.js`
   - Then run `npm test`, and finally `npm run build`.
   - Verify all targeted tests and the build pass before finishing.

## Examples
- User says: "Update scoring so recent notes rank higher."
  - Actions taken: edit `src/items/connections_list.js` scoring logic, keep `filter_hidden_results` before `merge_pinned_results`, and add or update a targeted test in `src/utils/connections_list_item_state.test.js` if pinned state is affected.
  - Result: newer notes score higher without exposing hidden notes or demoting pinned results.

- User says: "Add a collection setting to exclude low-confidence matches."
  - Actions taken: add the default in `src/actions/connections-list/pre_process.js`, expose the setting in `src/collections/connections_lists.js`, and confirm `src/items/connections_list.js` reads that value before scoring.
  - Result: the new filter is available in collection settings and changes results without touching component code.

## Common Issues
- If you see `Cannot read properties of undefined (reading 'settings')`, the collection/action default was not initialized. Fix it by setting the fallback in `src/actions/connections-list/pre_process.js` and making sure `src/collections/connections_lists.js` uses the same key the item pipeline expects.
- If pinned results disappear after a scoring change, `merge_pinned_results(...)` is missing, moved too early, or the pinned marker was lost before `src/items/connections_list.js` returns results. Fix the order and keep the pinned-state data intact.
- If hidden notes start showing up, `filter_hidden_results` is not running before the final merge. Fix the order in `src/items/connections_list.js` so hidden filtering happens before pinned merging and post-processing does not re-add hidden entries.
- If frontmatter filtering no longer works, the new default likely bypassed the existing include/exclude checks. Restore those checks in `src/items/connections_list.js` before scoring.

## Related skills
- `smart-connections` — for broader Smart Connections workflow routing
- `smart-connections-ava-and-migration-harness` — to lock pipeline changes down with tests
- `smart-connections-component-patterns` — when pipeline output changes also require UI updates
