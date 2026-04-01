---
name: extended-graph-setting-section
description: "Use this skill to add a new Extended Graph settings section with `SettingsSection` or `SettingsSectionPerGraphType`, register it in the settings tab, add i18n keys, and preserve collapse/expand behavior. Do NOT use it for non-settings UI components."
---
# Setting Section

## Critical

- **All imports must go through `"../internal"`** — never import from specific files within `src/`. This is the barrel export pattern used everywhere.
- Every new setting section file must be re-exported from `src/internal.ts`.
- Every setting item added to the body **must** be pushed to `this.elementsBody` (the collapse/expand mechanism relies on this array).
- Always call `ExtendedGraphInstances.plugin.saveSettings()` after mutating any setting value.
- i18n keys must be added to all three locale files: `i18n/en.json`, `i18n/fr.json`, `i18n/zh.json`.

## Instructions

### Step 1: Add settings properties to `ExtendedGraphSettings`

Open `src/settings/settings.ts`. Add the new setting properties to the `ExtendedGraphSettings` interface, grouped with a comment:

```ts
// MyFeature
myFeatureEnabled: boolean;
myFeatureValue: number;
```

Also add default values in the `DEFAULT_SETTINGS` object (same file, further down):

```ts
myFeatureEnabled: false,
myFeatureValue: 1,
```

**Verify**: `npm run build` compiles without errors before proceeding.

### Step 2: Add i18n keys

Open `i18n/en.json`. Add keys under the `"features"` object. Follow the naming convention:
- Section title: `"features.myFeature"` — short display name (e.g. `"My Feature"`)
- Section nav keyword: `"features.ids.myFeature"` — lowercase keyword for the nav sidebar (e.g. `"my feature"`)
- Section description: `"features.myFeatureDesc"` — one-line description
- Individual settings: `"features.myFeatureSettingName"` and `"features.myFeatureSettingNameDesc"`

Example additions to `i18n/en.json`:
```json
"myFeature": "My Feature",
"myFeatureDesc": "Configure the my feature behavior",
"myFeatureSomeSetting": "Some Setting",
"myFeatureSettingDesc": "Description of the setting"
```

Add the same keys (with translated or identical values) to `i18n/fr.json` and `i18n/zh.json`.

**Verify**: All three locale files are valid JSON.

### Step 3: Create the setting section class

Create `src/settings/settingMyFeature.ts`. Choose the base class:
- **`SettingsSection`**: for sections that are simple on/off or don't need per-graph-type toggles (like `SettingDisplay`, `SettingImages`).
- **`SettingsSectionPerGraphType`**: for sections that need separate graph/localgraph enable toggles in the header (like `SettingArrows`). Requires a `Feature` type value.

#### Pattern A: Extending `SettingsSection`

```ts
import { Setting } from "obsidian";
import { ExtendedGraphSettingTab, ExtendedGraphInstances, SettingsSection, t } from "../internal";

export class SettingMyFeature extends SettingsSection {
    constructor(settingTab: ExtendedGraphSettingTab) {
        super(
            settingTab,
            'my-feature',                    // id — used for collapse state key
            t("features.ids.myFeature"),      // keyword — nav sidebar label
            t("features.myFeature"),          // title — section heading
            'lucide-icon-name',              // icon — Lucide icon name
            t("features.myFeatureDesc")       // description
        );
    }

    protected override addBody() {
        this.addSomeSetting();
    }

    private addSomeSetting() {
        this.elementsBody.push(new Setting(this.containerEl)
            .setName(t("features.myFeatureSomeSetting"))
            .setDesc(t("features.myFeatureSettingDesc"))
            .addToggle(cb => {
                cb.setValue(ExtendedGraphInstances.settings.myFeatureEnabled);
                cb.onChange(value => {
                    ExtendedGraphInstances.settings.myFeatureEnabled = value;
                    ExtendedGraphInstances.plugin.saveSettings();
                });
            }).settingEl);
    }
}
```

#### Pattern B: Extending `SettingsSectionPerGraphType`

Requires a `Feature` type value. If your feature needs a new `Feature` value, add it to the union type in `src/types/restrictedStrings.ts` and to `enableFeatures` defaults in `src/settings/settings.ts`.

```ts
import { Setting } from "obsidian";
import { ExtendedGraphSettingTab, ExtendedGraphInstances, SettingsSectionPerGraphType, t } from "../internal";

export class SettingMyFeature extends SettingsSectionPerGraphType {
    constructor(settingTab: ExtendedGraphSettingTab) {
        super(
            settingTab,
            'my-feature',                    // feature (must match Feature type)
            '',                              // interactiveKey ('' if not interactive)
            t("features.ids.myFeature"),
            t("features.myFeature"),
            'lucide-icon-name',
            t("features.myFeatureDesc")
        );
    }

    protected override addBody() {
        // Add settings here
    }
}
```

**Verify**: The file compiles and the class constructor parameters match the base class signature.

### Step 4: Export from `src/internal.ts`

Add the export line in the settings block (around lines 93–117), keeping alphabetical order among setting files:

```ts
export * from "./settings/settingMyFeature";
```

**Verify**: `npm run build` compiles.

### Step 5: Register in `src/settings/settingTab.ts`

1. The import is automatic via `"../internal"` (already imported).
2. In the `ExtendedGraphSettingTab` constructor, add your section to `this.sections` at the appropriate position:

```ts
this.sections.push(new SettingMyFeature(this));
```

The order in `this.sections` determines the display order in the settings tab. Place it logically among existing sections.

If your section uses color palettes (has `onCustomPaletteModified`), also push it to `this.settingsWithPalettes`.

**Verify**: `npm run build` compiles. Open the Obsidian settings tab and confirm the section appears with the correct icon, title, and collapse/expand behavior.

### Step 6: Add setting controls in `addBody()`

Common control patterns (always push `.settingEl` to `this.elementsBody`):

**Toggle:**
```ts
this.elementsBody.push(new Setting(this.containerEl)
    .setName(t("features.mySettingName"))
    .setDesc(t("features.mySettingNameDesc"))
    .addToggle(cb => {
        cb.setValue(ExtendedGraphInstances.settings.myBooleanSetting);
        cb.onChange(value => {
            ExtendedGraphInstances.settings.myBooleanSetting = value;
            ExtendedGraphInstances.plugin.saveSettings();
        });
    }).settingEl);
```

**Numeric text input:**
```ts
this.elementsBody.push(new Setting(this.containerEl)
    .setName(t("features.myNumericSetting"))
    .setDesc(t("features.myNumericSettingDesc"))
    .addText(cb => {
        cb.inputEl.addClass("number");
        cb.setValue(ExtendedGraphInstances.settings.myNumber.toString())
            .onChange(async (value) => {
                const floatValue = parseFloat(value);
                if (!isNaN(floatValue)) {
                    ExtendedGraphInstances.settings.myNumber = floatValue;
                    await ExtendedGraphInstances.plugin.saveSettings();
                }
            });
    }).settingEl);
```

**Per-graph-type feature toggle (using `FeatureSetting` component):**
```ts
import { FeatureSetting } from "../internal";

this.elementsBody.push(new FeatureSetting(
    this.containerEl,
    t("features.mySubFeature"),
    t("features.mySubFeatureDesc"),
    'my-feature'  // Must match a Feature type value
).settingEl);
```

**Slider:**
```ts
this.elementsBody.push(new Setting(this.containerEl)
    .setName(t("features.mySlider"))
    .addSlider(cb => {
        cb.setLimits(0, 100, 1)
            .setValue(ExtendedGraphInstances.settings.mySliderValue)
            .onChange(value => {
                ExtendedGraphInstances.settings.mySliderValue = value;
                ExtendedGraphInstances.plugin.saveSettings();
            });
    }).settingEl);
```

**Verify**: `npm run build` compiles successfully.

## Examples

**User says**: "Add a new settings section for controlling link labels"

**Actions taken**:
1. Added `linkLabelFontSize: number` and `linkLabelOpacity: number` to `ExtendedGraphSettings` interface and defaults in `src/settings/settings.ts`
2. Added i18n keys `features.ids.linkLabels`, `features.linkLabels`, `features.linkLabelsDesc`, `features.linkLabelFontSize`, `features.linkLabelFontSizeDesc`, `features.linkLabelOpacity`, `features.linkLabelOpacityDesc` to all three locale files
3. Created `src/settings/settingLinkLabels.ts` extending `SettingsSection` with id `'link-labels'`, icon `'type'`
4. Implemented `addBody()` with `addFontSize()` and `addOpacity()` private methods, each pushing to `this.elementsBody`
5. Added `export * from "./settings/settingLinkLabels"` to `src/internal.ts`
6. Added `this.sections.push(new SettingLinkLabels(this))` in `settingTab.ts` constructor after the links section
7. Ran `npm run build` to verify

**Result**: New collapsible "Link Labels" section appears in settings with a type icon, font size input, and opacity input.

## Common Issues

**Section doesn't collapse/expand**: Ensure every setting element's `.settingEl` is pushed to `this.elementsBody`. The collapse mechanism hides elements in this array. If you forget to push, those elements stay visible when collapsed.

**"Cannot read properties of undefined" on settings access**: You added a property to the `ExtendedGraphSettings` interface but forgot to add a default value in `DEFAULT_SETTINGS`. Existing saved settings won't have the new key, so it will be `undefined`.

**Section appears but has no nav icon**: The `icon` parameter in the constructor must be a valid Lucide icon name (e.g. `'image'`, `'monitor'`, `'mouse-pointer-2'`). An empty string `''` deliberately skips nav registration.

**Build error "has no exported member 'SettingMyFeature'"**: You forgot to add the `export * from "./settings/settingMyFeature"` line in `src/internal.ts`.

**Feature toggle doesn't work with `SettingsSectionPerGraphType`**: The `feature` parameter must exactly match a value in the `Feature` union type in `src/types/restrictedStrings.ts`. If it's a new feature, add it to that type AND add default `true`/`false` entries in `enableFeatures.graph` and `enableFeatures.localgraph` in `DEFAULT_SETTINGS`.

**i18n key returns the key string instead of translated text**: The key path doesn't match. Keys under `features` are accessed as `t("features.myKey")`. Double-check the nesting in `i18n/en.json` — the `ids` sub-object is only for nav keywords.

## Related skills
- `extended-graph` — for broader Extended Graph workflow routing
- `extended-graph-plugin-feature` — when the setting is part of a new feature
- `extended-graph-interactive-type` — for interactive-specific settings surfaces
