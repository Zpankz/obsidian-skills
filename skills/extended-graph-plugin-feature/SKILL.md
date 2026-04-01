---
name: extended-graph-plugin-feature
description: "Use this skill to add a new feature to the Extended Graph plugin following the project’s feature-type, settings-section, per-graph-type toggle, graphics-wrapper, and barrel-export patterns. Do NOT use it for bug fixes or refactors of existing features."
---
# Add a New Feature to Extended Graph

## Critical

- **Barrel export rule**: ALL internal imports MUST use `"../internal"` or `"../../internal"`. Never import from specific files within `src/`. Every new file must be re-exported in `src/internal.ts`.
- **Feature type must exist** in `src/types/restrictedStrings.ts` before any settings or graph code can reference it.
- **Both graph types**: Every feature needs entries for both `'graph'` and `'localgraph'` in the `enableFeatures` record in `src/settings/settings.ts`.
- **i18n keys**: All user-facing strings go through the `t()` function (from `../internal`). Add keys to `i18n/en.json` first, then other locales.
- **Save settings pattern**: Every setting change callback must call `ExtendedGraphInstances.plugin.saveSettings()` after mutating `ExtendedGraphInstances.settings`.

## Instructions

### Step 1: Add the Feature type string

Edit `src/types/restrictedStrings.ts`. Add your feature's kebab-case identifier to the `Feature` union type.

```typescript
// src/types/restrictedStrings.ts
export type Feature = 'auto-enabled' | 'tags' | ... | 'layers' | 'yourFeature';
```

**Naming convention**: Use kebab-case for multi-word features (e.g., `'elements-stats'`, `'linksSameColorAsNode'`). Match existing naming — some use camelCase, some use kebab-case. Pick whichever is closest to existing features of similar scope.

**Verify**: `npm run build` should succeed with no type errors referencing the new Feature literal.

### Step 2: Add default settings

Edit `src/settings/settings.ts`:

1. Add any feature-specific properties to the `ExtendedGraphSettings` interface (around line 59+):

```typescript
export interface ExtendedGraphSettings {
    // ... existing properties ...
    
    // YourFeature
    yourFeatureProp: boolean;
    yourFeatureValue: number;
}
```

2. Add `'yourFeature': false` to BOTH `graph` and `localgraph` objects inside `DEFAULT_SETTINGS.enableFeatures` (around line 253):

```typescript
enableFeatures: {
    'graph': {
        // ... existing entries ...
        'yourFeature': false,
    },
    'localgraph': {
        // ... existing entries ...
        'yourFeature': false,
    }
},
```

3. Add default values for your feature-specific properties in `DEFAULT_SETTINGS`:

```typescript
// YourFeature
yourFeatureProp: false,
yourFeatureValue: 1,
```

4. Add a reload check in `SettingQuery.needReload()` (around line 609+). Follow the existing pattern:

```typescript
// YourFeature
if (newFeatures['yourFeature'] !== oldFeatures['yourFeature'])
    return true;
if (newFeatures['yourFeature']) {
    if (['yourFeatureProp', 'yourFeatureValue'].some(k => !equals(k)))
        return true;
}
```

**Verify**: `npm run build` succeeds. Check that both `graph` and `localgraph` have the new feature entry.

### Step 3: Add i18n strings

Edit `i18n/en.json`. Add entries under `features`:

```json
{
    "features": {
        "ids": {
            "yourFeature": "your feature"
        },
        "yourFeature": "Your Feature Name",
        "yourFeatureDesc": "Description of what this feature does.",
        "yourFeatureProp": "Property Label",
        "yourFeaturePropDesc": "Description of this property."
    }
}
```

- `features.ids.yourFeature` — short keyword used in nav sidebar
- `features.yourFeature` — section heading title
- `features.yourFeatureDesc` — section heading description

Also add equivalent keys to `i18n/fr.json` and `i18n/zh.json`.

**Verify**: No missing translation warnings at build time.

### Step 4: Create the settings section

Create `src/settings/settingYourFeature.ts`. Choose the correct base class:

- **`SettingsSectionPerGraphType`** — if the feature has a per-graph-type enable/disable toggle in the header (most features use this). Example: `settingArrows.ts`, `settingShapes.ts`.
- **`SettingsSection`** — if the feature has no per-graph-type toggle or manages its own toggles. Example: `settingImages.ts`.

**Pattern A: With per-graph-type toggle** (most common):

```typescript
import { Setting } from "obsidian";
import { ExtendedGraphSettingTab, ExtendedGraphInstances, SettingsSectionPerGraphType, t } from "../internal";

export class SettingYourFeature extends SettingsSectionPerGraphType {
    constructor(settingTab: ExtendedGraphSettingTab) {
        super(
            settingTab,
            'yourFeature',    // Feature type (must match restrictedStrings.ts)
            '',               // interactiveKey (empty string if not an interactive)
            t("features.ids.yourFeature"),  // keyword for nav
            t("features.yourFeature"),       // title
            'lucide-icon-name',              // icon (Lucide icon name)
            t("features.yourFeatureDesc")    // description
        );
    }

    protected override addBody() {
        this.addYourSetting();
    }

    private addYourSetting() {
        this.elementsBody.push(new Setting(this.settingTab.containerEl)
            .setName(t("features.yourFeatureProp"))
            .setDesc(t("features.yourFeaturePropDesc"))
            .addToggle(cb => {
                cb.setValue(ExtendedGraphInstances.settings.yourFeatureProp);
                cb.onChange(value => {
                    ExtendedGraphInstances.settings.yourFeatureProp = value;
                    ExtendedGraphInstances.plugin.saveSettings();
                })
            }).settingEl);
    }
}
```

**Key details**:
- The first arg to `super()` after `settingTab` is the `feature` string — it becomes `this.id` and must match the Feature type.
- Always push `.settingEl` to `this.elementsBody` — this enables collapse/expand behavior.
- Use `FeatureSetting` component (from `../internal`) if you need sub-feature toggles with both graph/localgraph toggles inline.

**Pattern B: Without per-graph-type toggle** (like `settingImages.ts`):

```typescript
import { Setting } from "obsidian";
import { ExtendedGraphSettingTab, FeatureSetting, ExtendedGraphInstances, SettingsSection, t } from "../internal";

export class SettingYourFeature extends SettingsSection {
    constructor(settingTab: ExtendedGraphSettingTab) {
        super(settingTab, 'yourFeature', t("features.ids.yourFeature"), t("features.yourFeature"), 'lucide-icon-name', t("features.yourFeatureDesc"));
    }

    protected override addBody() {
        // Use FeatureSetting for sub-features with graph/localgraph toggles
        this.elementsBody.push(new FeatureSetting(
            this.settingTab.containerEl,
            t("features.yourSubFeature"),
            t("features.yourSubFeatureDesc"),
            'yourFeature'
        ).settingEl);
    }
}
```

**Verify**: File compiles. Constructor args match base class signature.

### Step 5: Register the settings section in the tab

Edit `src/settings/settingTab.ts`:

1. The import is automatic via barrel — just add `SettingYourFeature` to the import from `"../internal"`.
2. Push a new instance into `this.sections` in the constructor, in the appropriate position:

```typescript
this.sections.push(new SettingYourFeature(this));
```

Place it logically among existing sections (look at the order in the constructor around line 62-80).

**Verify**: Open Obsidian settings → Extended Graph. Your section appears with the icon in the nav sidebar.

### Step 6: Add barrel export

Edit `src/internal.ts`. Add an export line in the settings group (around line 93-119):

```typescript
export * from "./settings/settingYourFeature";
```

Keep alphabetical ordering within the settings block.

**Verify**: `npm run build` succeeds with no unused export warnings.

### Step 7: Wire feature into graph initialization (if applicable)

If the feature affects graph rendering, edit `src/graph/graph.ts`. Check the feature flag before initializing:

```typescript
if (this.instances.settings.enableFeatures[this.instances.type]['yourFeature']) {
    // Initialize your feature's manager/renderer
}
```

Follow the existing pattern (see how `layers`, `folders`, `shapes` are conditionally initialized around lines 22-32 of `graph.ts`).

**Verify**: Feature only activates when its toggle is enabled for the current graph type.

### Step 8: Build and test

```bash
npm run build
```

Then manually verify in Obsidian:
1. Settings section appears with icon and description
2. Graph/Local toggles work independently
3. Feature-specific settings are saved and restored on reload
4. Feature activates/deactivates correctly in the graph view

## Examples

### Example: Adding a "Badges" feature

**User says**: "Add a badges feature that shows small badges on nodes based on properties"

**Actions taken**:

1. Add `'badges'` to the `Feature` type in `src/types/restrictedStrings.ts`
2. Add `badgeProperties: string[]` and `badgePosition: 'top-right' | 'top-left'` to `ExtendedGraphSettings` interface
3. Add `'badges': false` to both `graph` and `localgraph` in `DEFAULT_SETTINGS.enableFeatures`
4. Add defaults: `badgeProperties: [], badgePosition: 'top-right'` to `DEFAULT_SETTINGS`
5. Add reload check in `SettingQuery.needReload()`
6. Add i18n keys: `features.ids.badges`, `features.badges`, `features.badgesDesc`, etc. in all three locale files
7. Create `src/settings/settingBadges.ts` extending `SettingsSectionPerGraphType`:
   - Constructor: `super(settingTab, 'badges', '', t("features.ids.badges"), t("features.badges"), 'badge-check', t("features.badgesDesc"))`
   - `addBody()` adds property list and position dropdown
8. Register `new SettingBadges(this)` in `settingTab.ts` constructor
9. Add `export * from "./settings/settingBadges"` to `src/internal.ts`
10. Add conditional init in `src/graph/graph.ts`

**Result**: A "Badges" section in settings with Global/Local toggles, property selector, and position dropdown. Badges render on graph nodes when enabled.

## Common Issues

### `Type '"yourFeature"' is not assignable to type 'Feature'`
You forgot Step 1. Add your feature string to the `Feature` union in `src/types/restrictedStrings.ts`.

### Feature toggle exists but feature doesn't activate
Check `src/graph/graph.ts` — you must read `this.instances.settings.enableFeatures[this.instances.type]['yourFeature']` using the correct graph type (`this.instances.type`), not hardcoding `'graph'`.

### Settings don't persist after reload
Ensure every `onChange` callback calls `ExtendedGraphInstances.plugin.saveSettings()` AND that your properties have defaults in `DEFAULT_SETTINGS`. Missing defaults cause `undefined` on first load.

### Section doesn't collapse/expand
You must push `.settingEl` to `this.elementsBody`. If you push the `Setting` object instead of `setting.settingEl`, collapse won't work.

### Import not found for your new class
You forgot Step 6. Add `export * from "./settings/settingYourFeature"` to `src/internal.ts`. Never import directly from the file — always go through the barrel.

### `Cannot read properties of undefined (reading 'yourFeature')`
You added the feature to only one of `graph`/`localgraph` in `DEFAULT_SETTINGS.enableFeatures`. Both must have the entry. Also check that existing saved settings get merged properly — Obsidian's `loadData()` returns old saved data that won't have the new key.

### Settings section appears but has no nav icon
The `icon` parameter in the constructor must be a valid Lucide icon name. Check https://lucide.dev for available icons. If the icon string is empty (`''`), the nav entry is skipped (see `SettingsSection.addToNav()` line 79).

### Graph doesn't reload when settings change
You forgot the `needReload()` check in Step 2.4. Without it, `SettingQuery.needReload()` returns `false` and the graph won't rebuild when your feature is toggled.

## Related skills
- `extended-graph` — for broader Extended Graph workflow routing
- `extended-graph-setting-section` — because most features also need settings UI
- `extended-graph-interactive-type` — when the feature is filter or legend driven
- `obsidian-dev` — for wider Obsidian implementation patterns
