---
name: extended-graph-interactive-type
description: "Use this skill to add a new Extended Graph interactive filter type, including `InteractiveManager` integration, color palettes, legend UI hooks, and settings wiring. Do NOT use it to tweak existing interactive types."
---
# Adding a New Interactive Filter Type

## Critical

- **Barrel exports only**: Every internal import MUST use `"../internal"` or `"../../internal"`. Never import from specific files within `src/`. After creating any new file, add its `export *` line to `src/internal.ts`.
- **Three categories of interactive**: Node-level (like tags, properties), link-level (like `LINK_KEY`), and folder-level (like `FOLDER_KEY`). The `InteractiveEventsDispatcher` routes events differently based on whether the key equals `LINK_KEY`, `FOLDER_KEY`, or something else (node interactive). Determine your category before starting.
- **Keys are string constants**: Each interactive type has a constant key (e.g., `TAG_KEY = "tag"`, `LINK_KEY = "link"`, `FOLDER_KEY = "folder"`) defined in `src/globalVariables.ts`. The key is used throughout as a dictionary key in `interactiveSettings`, `interactiveManagers`, and `typesMap`.
- **Feature flag required**: The `Feature` type in `src/types/restrictedStrings.ts` gates which interactives are available. Your new type needs a feature flag entry.

## Instructions

### Step 1: Define the Key Constant

Add a new constant to `src/globalVariables.ts`:

```typescript
export const MY_KEY: string = "mytype";
INVALID_KEYS[MY_KEY] = [];
```

Pattern follows `TAG_KEY`, `LINK_KEY`, `FOLDER_KEY` in the same file. `INVALID_KEYS` lists property keys to exclude when resolving this interactive.

**Verify**: `MY_KEY` is exported and `INVALID_KEYS[MY_KEY]` is initialized.

### Step 2: Add the Feature Flag

Edit `src/types/restrictedStrings.ts` — append your feature name to the `Feature` union type:

```typescript
export type Feature = 'auto-enabled' | 'tags' | ... | 'mytype';
```

Then in `src/settings/settings.ts`, add your feature to both `graph` and `localgraph` blocks inside `DEFAULT_SETTINGS.enableFeatures`:

```typescript
'graph': {
    ...
    'mytype': false,
},
'localgraph': {
    ...
    'mytype': false,
}
```

**Verify**: TypeScript compiles without errors (`npm run build` passes type check).

### Step 3: Register Default Interactive Settings

In `src/main.ts`, inside the `completeDefaultSettings()` method, add a block following the existing pattern:

```typescript
DEFAULT_SETTINGS.interactiveSettings[MY_KEY] = {
    colormap: "rainbow",
    colors: [],
    unselected: [],
    excludeRegex: { regex: "", flags: "" },
    noneType: "none",
    showOnGraph: true,
    enableByDefault: true,
};
```

The `InteractiveSettings` type is defined in `src/settings/settings.ts` (lines 32-42). Include `undefinedType` only if your interactive can be absent from a file (like properties). Tags and folders omit it.

**Verify**: `DEFAULT_SETTINGS.interactiveSettings[MY_KEY]` is populated before `loadSettings()` merges user data.

### Step 4: Implement Data Extraction

Edit `src/helpers/vault.ts` — add a case to `getFileInteractives()`:

```typescript
case MY_KEY:
    results = getMyTypeValues(file);
    break;
```

Then implement the extraction function in the same file:

```typescript
function getMyTypeValues(file: TFile): Set<string> {
    // Extract your interactive values from the file
    // Return Set<string> of type names
}
```

Also update `getNumberOfFileInteractives()` if your type supports counting per-type occurrences.

**Verify**: `getFileInteractives(MY_KEY, someFile)` returns a `Set<string>` with expected values.

### Step 5: Create the Settings UI Class

Create `src/settings/settingInteractives/settingMyType.ts` extending `SettingInteractives`:

```typescript
import { Setting } from "obsidian";
import { ExtendedGraphSettingTab, ExtendedGraphInstances, SettingInteractives, t, MY_KEY } from "../../internal";

export class SettingMyType extends SettingInteractives {
    constructor(settingTab: ExtendedGraphSettingTab) {
        super(
            settingTab,
            'mytype',           // feature key (matches Feature type)
            MY_KEY,             // interactive key constant
            t("features.ids.mytype"),       // keyword for i18n
            t("features.interactives.mytype"),  // title
            'icon-name',        // Lucide icon name
            t("features.interactives.mytypeDesc"), // description
            false               // canBeRecursive (true for hierarchical like tags/folders)
        );
    }

    protected override addBody(): void {
        super.addBody();  // adds noneType, colorPalette, specificColors, filter
        // Add type-specific settings here
    }

    protected override isValueValid(name: string): boolean {
        return name.length > 0;
    }

    protected override getPlaceholder(): string {
        return "mytype";
    }

    protected override getAllTypes(): string[] {
        // Return all possible values of this interactive from the vault
        return [];
    }
}
```

The constructor args match the pattern in `settingTags.ts` (line 7), `settingLinks.ts` (line 19), `settingFolders.ts` (line 8).

The base class `SettingInteractives` (in `settingInteractive.ts`) provides:
- `addNoneTypeSetting()` — sentinel type name
- `addColorPaletteSetting()` — colormap selector
- `addSpecificColorHeaderSetting()` — per-type color overrides
- `addFilterTypeSetting()` — type selection/exclusion

Call `super.addBody({ alsoAddUndefined: true })` only if your type can be absent (like properties).

**Verify**: The class compiles and follows the same constructor signature pattern.

### Step 6: Register in Barrel Export

Add to `src/internal.ts`:

```typescript
export * from "./settings/settingInteractives/settingMyType";
```

**Verify**: The new class is importable via `"../../internal"`.

### Step 7: Wire into Settings Tab

Edit `src/settings/settingTab.ts` — import and instantiate your setting class alongside existing ones:

```typescript
const settingMyType = new SettingMyType(this);
```

Place it near the existing `SettingTags`, `SettingLinks`, `SettingFolders` instantiations (around line 47-50).

**Verify**: The settings tab displays your new section.

### Step 8: Register in Graph Initialization

Edit `src/graph/graph.ts`, method `getInteractiveManagerKeys()` — add your key:

```typescript
if (this.instances.settings.enableFeatures[this.instances.type]['mytype']) keys.push(MY_KEY);
```

Then determine which set uses your manager:
- **Node interactive**: Already handled — `getNodeManagers()` returns all managers except `LINK_KEY` and `FOLDER_KEY`.
- **Link interactive**: Add to `getLinkManagers()` filter.
- **Folder-level interactive**: Add to `getFolderManagers()` filter.

**Verify**: `this.instances.interactiveManagers.get(MY_KEY)` returns a valid `InteractiveManager` when the feature is enabled.

### Step 9: Handle Events in InteractiveEventsDispatcher

If your type is a **node interactive**, no changes needed — the dispatcher already routes non-LINK, non-FOLDER keys to `onNodeInteractiveTypesAdded/Removed/ColorChanged` and the generic enable/disable paths.

If your type needs **custom event handling** (like folders need bbox management), add a new branch in `src/graph/interactiveEventsDispatcher.ts`:

```typescript
onInteractivesAdded(name: string, colorMaps: Map<string, Color.Color>) {
    if (name === LINK_KEY) { ... }
    else if (name === FOLDER_KEY) { ... }
    else if (name === MY_KEY) { this.onMyTypeAdded(colorMaps); }
    else { this.onNodeInteractiveTypesAdded(name, colorMaps); }
}
```

Repeat for `onInteractivesRemoved`, `onInteractiveColorChanged`, `onInteractivesDisabled`, `onInteractivesEnabled`.

**Verify**: Toggling your interactive type in the legend triggers the correct add/remove/enable/disable flow.

### Step 10: Add i18n Strings

Add translation keys to `i18n/en.json` (and optionally `fr.json`, `zh.json`):

```json
"features": {
    "ids": {
        "mytype": "My Type"
    },
    "interactives": {
        "mytype": "My Type Filter",
        "mytypeDesc": "Filter nodes by my type"
    }
}
```

**Verify**: `t("features.ids.mytype")` returns the expected string.

### Step 11: Update Settings Change Detection

In `src/settings/settings.ts`, in the `SettingQuery.hasSettingChanged()` method (around line 610+), add a check for your interactive:

```typescript
if (oldFeatures['mytype'] !== newFeatures['mytype']) return true;
if (newFeatures['mytype'] && !deepEquals(oldSettings.interactiveSettings[MY_KEY], newSettings.interactiveSettings[MY_KEY]))
    return true;
```

**Verify**: Changing your interactive's settings triggers a graph reload.

### Step 12: Update Color Suggester (if needed)

In `src/settings/settingInteractives/settingInteractive.ts`, the `SettingColor` constructor (line 230) has a switch on `key` for the suggester. If your key isn't `LINK_KEY`, `TAG_KEY`, or `FOLDER_KEY`, it falls through to the `default` case which uses `'property'` mode. If this is wrong for your type, add a case:

```typescript
case MY_KEY:
    suggester.setKey('mytype');
    break;
```

This requires also updating `InteractivesColorSuggester` in `src/suggester/InteractivesSuggester.ts`.

**Verify**: The color type-ahead in settings suggests correct values for your interactive.

## Examples

### Example: Adding a "status" interactive (node-level, from frontmatter property)

User says: "Add a new interactive filter for note status (draft, review, published)"

**Actions taken**:
1. Add `STATUS_KEY = "status"` to `src/globalVariables.ts`
2. Add `'status'` to `Feature` union in `src/types/restrictedStrings.ts`
3. Add default `enableFeatures` entries (`'status': false`) for both graph types
4. Add `DEFAULT_SETTINGS.interactiveSettings[STATUS_KEY]` in `main.ts:completeDefaultSettings()`
5. Add `case STATUS_KEY:` in `getFileInteractives()` returning frontmatter `status` values
6. Create `src/settings/settingInteractives/settingStatus.ts` extending `SettingInteractives`
7. Export from `src/internal.ts`
8. Instantiate in `src/settings/settingTab.ts`
9. Add `if (features['status']) keys.push(STATUS_KEY)` in `graph.ts:getInteractiveManagerKeys()`
10. No dispatcher changes needed (node interactive uses generic path)
11. Add i18n strings to `i18n/en.json`
12. Add change detection in `settings.ts:hasSettingChanged()`

**Result**: Status values appear in the graph legend with assigned colors from the colormap. Nodes can be filtered by status. Color palette and per-status color overrides work in settings.

## Common Issues

### "Cannot read properties of undefined (reading 'colormap')"
**Cause**: `interactiveSettings[MY_KEY]` was not initialized in `completeDefaultSettings()`.  
**Fix**: Add the default settings block in `src/main.ts:completeDefaultSettings()` method. This runs before `loadSettings()` merges saved data.

### Interactive types don't appear in the legend
**Cause**: The manager key isn't returned by `getInteractiveManagerKeys()` in `src/graph/graph.ts`.  
**Fix**: Ensure the feature flag check `this.instances.settings.enableFeatures[this.instances.type]['mytype']` is added and the feature is enabled in settings.

### Types not extracted from files
**Cause**: `getFileInteractives()` in `src/helpers/vault.ts` doesn't handle your key.  
**Fix**: Add a `case MY_KEY:` branch in the switch statement. Without it, the default case treats it as a frontmatter property key.

### Settings section doesn't show in the plugin settings tab
**Cause**: The setting class isn't instantiated in `settingTab.ts`, or it's not exported from `internal.ts`.  
**Fix**: 1. Add `export * from "./settings/settingInteractives/settingMyType"` to `src/internal.ts`. 2. Add `const settingMyType = new SettingMyType(this)` in `settingTab.ts`.

### Build error: "Type '"mytype"' is not assignable to type 'Feature'"
**Cause**: The feature name wasn't added to the `Feature` union type.  
**Fix**: Edit `src/types/restrictedStrings.ts` and add `'mytype'` to the `Feature` type union.

### Color palette changes don't take effect
**Cause**: `hasSettingChanged()` in `src/settings/settings.ts` doesn't detect changes to your interactive settings.  
**Fix**: Add the comparison block for your key in `SettingQuery.hasSettingChanged()` following the pattern of tags/links/folders checks.

## Related skills
- `extended-graph` — for broader Extended Graph workflow routing
- `extended-graph-plugin-feature` — when the interactive ships as a new feature
- `extended-graph-setting-section` — because interactives usually need settings UI
