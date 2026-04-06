---
name: smart-connections-ava-and-migration-harness
description: Add or update Smart Connections AVA regression tests for utilities and migrations. Trigger on "write test", "fix migration", or test changes under src/utils or migrations.
paths:
  - src/utils/**/*.test.js
  - src/utils/**/*.js
  - migrations/**/*.test.js
  - migrations/**/*.js
---
# Smart Connections AVA and Migration Harness

Use this skill when adding or updating focused Smart Connections regression coverage for utilities or migrations, especially when you need fixture-driven AVA tests and idempotent migration checks.

## Critical
- Keep the test file next to the code under test:
  - `src/utils/build_connections_codeblock.test.js` for utility regressions
  - `migrations/migrate_hidden_connections.test.js` for migration regressions
- Import Ava with `import test from 'ava';` and import the subject with an explicit `.js` extension.
- Always cover:
  - the happy path
  - a no-op path (`undefined`, empty object/array, already-migrated input)
  - nested object assertions with `t.deepEqual`
- Migration tests must verify idempotency: running the migration twice should return the same shape the second time.
- Do not use snapshots or integration-style demos here. This skill is for isolated regression coverage only.

## Instructions
1. Identify the subject and create the test file in the matching directory:
   - `src/utils/build_connections_codeblock.test.js` for helpers such as `build_connections_codeblock`
   - `migrations/migrate_hidden_connections.test.js` for migration functions such as `migrate_hidden_connections`
   Use the output from the user request to choose the exact filename. Verify the subject lives in one of those directories before proceeding.

2. Mirror the module imports used elsewhere in the repo:
   - `import test from 'ava';`
   - `import { <fn> } from './<file>.js';` for sibling utilities, or the correct relative path from `migrations/`
   - import fixture data inline in the test file unless the repo already exposes a shared fixture in `src/utils/`
   Verify the import resolves with the same relative path you would use in runtime code before proceeding.

```js
import test from 'ava';
import { build_connections_codeblock } from './build_connections_codeblock.js';
```

3. Build fixtures that match the actual data shape passed by callers.
   - For utilities, use minimal but realistic Obsidian-shaped objects/arrays/strings.
   - For migrations, use a pre-migration object and a post-migration expectation.
   - Create a fresh fixture inside each test body so mutation is visible when the function changes nested data.
   Verify the fixture reproduces the real nested keys and array members before proceeding.

4. Write regression cases with deep assertions.
   - Use `t.deepEqual(actual, expected)` for nested structures.
   - Use scalar assertions via ava as appropriate for the subject’s contract.
   - Include a no-op test that proves the function returns unchanged output for empty or already-processed input.
   This step uses the fixtures from Step 3. Verify the no-op case before proceeding to the next step.

5. For migration files, add idempotency coverage.
   - Run the migration once and assert the transformed result.
   - Run it a second time on the transformed result and assert the output stays the same.
   - If the migration intentionally omits fields, assert the omitted keys are absent with `t.deepEqual` against an exact object shape.
   This step uses the output from Step 4. Verify the second run is a no-op before proceeding to the next step.

6. Run the narrowest Ava command first, then widen only if needed.
   - Example targeted commands from this repo:
     - `npx ava src/utils/format_connections_as_links.test.js`
     - `npx ava src/utils/connections_list_item_state.test.js`
     - `npx ava src/utils/build_connections_codeblock.test.js`
   - For migration tests, run `npx ava migrations/migrate_hidden_connections.test.js`
   - If the helper is used in runtime code, finish with `npm test` and `npm run build`
   Verify the targeted test file passes before proceeding to the next step.

```js
import test from 'ava';
import { migrate_hidden_connections } from './migrate_hidden_connections.js';

test('migrates legacy hidden connection payload', (t) => {
  const input = {
    pluginData: {
      connections: {
        hidden: ['note-a.md'],
      },
    },
  };

  const migrated = migrate_hidden_connections(input);
  t.deepEqual(migrated, {
    pluginData: {
      connections_lists: {
        hidden: ['note-a.md'],
      },
    },
  });
});
```

## Examples
- User says: 'fix migrate_hidden_connections'
  - Actions taken: create `migrations/migrate_hidden_connections.test.js`, import `test` from `ava`, add a legacy fixture with hidden connections, assert the migrated object with `t.deepEqual`, and add a second test proving the migration returns the same output when run again.
  - Result: the migration is locked down with a regression test and stays idempotent.

```js
// migrations/migrate_hidden_connections.test.js
import test from 'ava';
import { migrate_hidden_connections } from './migrate_hidden_connections.js';

test('migration is idempotent', (t) => {
  const once = migrate_hidden_connections({ pluginData: {} });
  const twice = migrate_hidden_connections(once);
  t.deepEqual(twice, once);
});
```

- User says: 'adjust build_connections_codeblock'
  - Actions taken: update `src/utils/build_connections_codeblock.test.js`, feed in a minimal Markdown/codeblock fixture, assert the returned codeblock shape with `t.deepEqual`, and verify nested metadata is preserved.
  - Result: the helper keeps producing the same codeblock shape for all callers.

```js
// src/utils/build_connections_codeblock.test.js
import test from 'ava';
import { build_connections_codeblock } from './build_connections_codeblock.js';

test('builds codeblock from simple fixture', (t) => {
  const fixture = { title: 'Notes', source: 'A' };
  t.deepEqual(build_connections_codeblock(fixture), {
    type: 'smart-connections',
    title: 'Notes',
    source: 'A',
  });
});
```

## Common Issues
- If you see `Cannot find module './<file>.js'`, the import path is wrong. Fix the relative path and keep the explicit `.js` extension; this repo uses ESM-style imports in tests.
- If you see `AvaError: No tests found`, the file name or location is wrong. Place it under `src/utils/` or `migrations/` with `*.test.js`, then rerun the matching `npx ava <path>` command.
- If you see deep diff output like `Difference (- actual + expected)` on nested fields, replace scalar checks with `t.deepEqual`, and make sure your expected fixture includes every nested property the function preserves.
- If the original fixture changes after the function call, create a fresh fixture inside the test body and assert both the original and returned values. This usually means the function mutates in place and the test is accidentally reusing the same object for expected data.
- If you see an idempotency failure on the second migration run, the migration is still writing fields on already-migrated data. Update the migration so it returns the input unchanged when the target layout is already present.

## Related skills
- `smart-connections` — for broader Smart Connections workflow routing
- `smart-connections-collection-pipeline` — because many test changes come from pipeline edits
- `obsidian-ops` — for wider build-and-validation workflow guidance
