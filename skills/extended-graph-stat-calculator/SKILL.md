---
name: extended-graph-stat-calculator
description: "Use this skill to create a new node or link stat calculator in Extended Graph following the factory pattern in `src/statsCalculators/`, including type registration, labels, and barrel exports. Do NOT use it to modify existing calculators."
---
# Stat Calculator

Create a new node or link stat calculator that integrates with the existing factory pattern in `src/statsCalculators/`.

## Critical

- **All internal imports MUST use `"../../internal"`** — never import from specific files within `src/`. The project uses a barrel export at `src/internal.ts`.
- Every new calculator class, type literal, and label MUST be added to **all four registration points** (calculator file, factory, type union + label maps, `src/internal.ts` export). Missing any one will cause a build failure or silent omission from the UI.
- Run `npm run build` to verify — there is no test framework. A clean build with `tsc --noEmit` + esbuild is the only validation.

## Instructions

### Step 1: Create the calculator file

**For a node calculator** — create a new file in `src/statsCalculators/nodes/` (e.g., `src/statsCalculators/nodes/wordCountCalculator.ts` following the pattern from `src/statsCalculators/nodes/filenameLengthCalculator.ts`):

```ts
import { GraphologyGraph, GraphStatsDirection, NodeStat, NodeStatCalculator } from "../../internal";

export class WordCountCalculator extends NodeStatCalculator {
    constructor(stat: NodeStat, graphologyGraph?: GraphologyGraph) {
        super(stat, "wordCount", graphologyGraph);
    }

    override async getStat(id: string, direction: GraphStatsDirection): Promise<number> {
        if (!this.graphologyGraph) return NaN;
        // Compute and return a numeric measure for the node identified by `id`
    }

    // Optional: override if the metric has a reference URL
    static override getLink(): string {
        return "<url>";
    }
}
```

**For a link calculator** — create a new file in `src/statsCalculators/links/` (e.g., `src/statsCalculators/links/myMetricCalculator.ts` following the pattern from `src/statsCalculators/links/jaccardCalculator.ts`):

```ts
import { GraphologyGraph, LinkStat, LinkStatCalculator } from "../../internal";
import { Attributes, EdgeEntry } from "graphology-types";

export class MyMetricCalculator extends LinkStatCalculator {
    constructor(stat: LinkStat, graphologyGraph?: GraphologyGraph) {
        super(stat, "My Metric", graphologyGraph);
    }

    protected override async getStat(link: EdgeEntry<Attributes, Attributes>): Promise<number> {
        const g = this.graphologyGraph?.graphology;
        if (!g) return NaN;
        // Compute and return a numeric measure for the edge
    }
}
```

Naming conventions:
- Node function keys are **camelCase** strings (e.g., `"filenameLength"`, `"tagsCount"`, `"eccentricity"`).
- Link function keys use **Title Case with spaces** (e.g., `"Adamic Adar"`, `"Clustering Coefficient"`, `"Jaccard"`).
- Class names are PascalCase ending in `Calculator` (e.g., `FilenameLengthCalculator`, `JaccardCalculator`).

**Verify:** The file compiles in isolation — no circular imports, correct extends clause.

### Step 2: Register the function key in the base type and label maps

**For nodes** — edit `src/statsCalculators/nodes/nodeStatCalculator.ts`:

1. Add the new key to the `NodeStatFunction` union type (line ~3).
2. Add the label entry to `nodeStatFunctionLabels` using `t("statsFunctions.<key>")` (line ~5).
3. Add the NLP flag to `nodeStatFunctionNeedsNLP` — `true` only if the calculator requires wink-nlp or similar NLP processing (line ~29).
4. Add the dynamic flag to `nodeStatFunctionIsDynamic` — `true` if the value changes when the visible graph changes (graph-topology-dependent metrics), `false` for static file properties (line ~53).

Example for a node key `wordCount`:

```ts
// In NodeStatFunction union (line ~3), add 'wordCount':
export type NodeStatFunction = 'default' | 'constant' | ... | 'wordCount';

// In nodeStatFunctionLabels (line ~5):
'wordCount': t("statsFunctions.wordCount"),

// In nodeStatFunctionNeedsNLP (line ~29):
'wordCount': false,

// In nodeStatFunctionIsDynamic (line ~53):
'wordCount': false,
```

**For links** — edit `src/statsCalculators/links/linkStatCalculator.ts`:

1. Add the new key to the `LinkStatFunction` union type (line ~5).
2. Add the label to `linkStatFunctionLabels` (line ~7).
3. Add the NLP flag to `linkStatFunctionNeedsNLP` (line ~19).
4. Add the dynamic flag to `linkStatFunctionIsDynamic` (line ~31).

**Verify:** The type union and all three Record maps have the same set of keys. TypeScript will error if any key is missing from a Record.

### Step 3: Register in the factory

**For nodes** — edit `src/statsCalculators/nodes/nodeStatCalculatorFactory.ts`:

1. Import the new calculator class from `"../../internal"` (add to the import block at line ~1).
2. Add a `case '<functionKey>':` in the `getCalculator` switch (line ~28) returning `new <CalculatorName>Calculator(stat, g)`.
3. Add a matching `case` in the `getWarning` switch (line ~74) returning `<CalculatorName>Calculator.getWarning()`.

Example:

```ts
// In getCalculator switch:
case 'wordCount':
    return new WordCountCalculator(stat, g);

// In getWarning switch:
case 'wordCount':
    return WordCountCalculator.getWarning();
```

**For links** — edit `src/statsCalculators/links/linksStatCalculatorFactory.ts`:

1. Import the new calculator class from `"../../internal"` (add to the import block at line ~1).
2. Add a `case '<FunctionKey>':` in the `getCalculator` switch (line ~20) returning `new <CalculatorName>Calculator(stat, g)`.

**Verify:** The case string matches exactly the key added to the type union in Step 2.

### Step 4: Add i18n labels

Edit `i18n/en.json` (required) and `i18n/fr.json`, `i18n/zh.json` (if translations available). Add the label inside the `"statsFunctions"` object:

```json
"statsFunctions": {
    ...
    "wordCount": "Word count"
}
```

The key must match the string used in `t("statsFunctions.<key>")` from Step 2.

**Verify:** Every `t("statsFunctions.X")` call in the label maps has a corresponding entry in `en.json`.

### Step 5: Export via `src/internal.ts`

Add an export line to `src/internal.ts` in the statsCalculators section (lines ~66-88), maintaining alphabetical order within the nodes/links groups:

```ts
// For a node calculator (add near line ~88 alongside other node calculator exports):
export * from "./statsCalculators/nodes/wordCountCalculator";

// For a link calculator (add near line ~76 alongside other link calculator exports):
export * from "./statsCalculators/links/myMetricCalculator";
```

**Verify:** Run `npm run build` — clean build confirms all registrations are consistent.

## Examples

### User says: "Add a word count stat for nodes"

**Actions taken:**

1. Create `src/statsCalculators/nodes/wordCountCalculator.ts`:
```ts
import { getFile, GraphologyGraph, GraphStatsDirection, NodeStat, NodeStatCalculator } from "../../internal";
import { app } from "obsidian";

export class WordCountCalculator extends NodeStatCalculator {
    constructor(stat: NodeStat, graphologyGraph?: GraphologyGraph) {
        super(stat, "wordCount", graphologyGraph);
    }

    override async getStat(id: string, direction: GraphStatsDirection): Promise<number> {
        const file = getFile(id);
        if (!file) return 0;
        const content = await app.vault.cachedRead(file);
        return content.split(/\s+/).filter(w => w.length > 0).length;
    }
}
```

2. In `src/statsCalculators/nodes/nodeStatCalculator.ts`:
   - Add `'wordCount'` to `NodeStatFunction` union (line ~3).
   - Add `'wordCount': t("statsFunctions.wordCount")` to `nodeStatFunctionLabels` (line ~5).
   - Add `'wordCount': false` to `nodeStatFunctionNeedsNLP` (line ~29).
   - Add `'wordCount': false` to `nodeStatFunctionIsDynamic` (line ~53).

3. In `src/statsCalculators/nodes/nodeStatCalculatorFactory.ts`:
   - Import `WordCountCalculator` from `"../../internal"` (line ~1).
   - Add `case 'wordCount': return new WordCountCalculator(stat, g);` in `getCalculator` (line ~28).
   - Add `case 'wordCount': return WordCountCalculator.getWarning();` in `getWarning` (line ~74).

4. In `i18n/en.json` under `statsFunctions`: `"wordCount": "Word count"`

5. In `src/internal.ts` (line ~88): `export * from "./statsCalculators/nodes/wordCountCalculator";`

6. Run `npm run build` — clean build.

**Result:** "Word count" appears in the node size/color function dropdowns in settings.

## Common Issues

- **Build error `Property 'wordCount' is missing in type`**: You added the key to the `NodeStatFunction`/`LinkStatFunction` union but forgot to add it to one of the three Record maps (`Labels`, `NeedsNLP`, `IsDynamic`). TypeScript enforces exhaustive Records — add the key to all three.

- **Calculator not appearing in the settings dropdown**: The function key string in the constructor (`super(stat, "key", ...)`) doesn't match the string in the type union or the factory switch case. These must be identical, including casing and spaces.

- **`Cannot find module` or `is not exported`**: You forgot to add the `export *` line in `src/internal.ts`. Every calculator file must be re-exported through the barrel.

- **`t("statsFunctions.X")` returns the key string instead of the label**: The i18n key in `en.json` doesn't match. Check that `statsFunctions.<key>` in the JSON matches exactly what's passed to `t()`.

- **Node calculator `getStat` always returns NaN**: You're accessing `this.graphologyGraph` without the null check. Always guard with `if (!this.graphologyGraph) return NaN;` for graph-dependent calculators. For file-property calculators (like filename length), the graphology graph isn't needed.

- **Link calculator `getStat` signature mismatch**: Node calculators use `getStat(id: string, direction: GraphStatsDirection)` while link calculators use `getStat(link: EdgeEntry<Attributes, Attributes>)`. Using the wrong signature will silently fail to override the base method — use `override` keyword to catch this at compile time.

## Related skills
- `extended-graph` — for broader Extended Graph workflow routing
- `extended-graph-plugin-feature` — when a metric ships as part of a larger feature
- `obsidian-ref` — for reference-level validation and naming consistency
