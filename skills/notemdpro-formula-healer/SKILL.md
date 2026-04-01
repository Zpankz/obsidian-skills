---
name: notemdpro-formula-healer
description: "Use this skill to repair LaTeX math delimiter issues, including malformed inline vs block math and single-dollar display math problems."
---

# NoteMD Pro - Formula Fixing

## Overview

This skill fixes LaTeX math formula formatting in markdown files. It converts single-line formulas delimited by single `$` to double `$$` for proper display math rendering.

## When to Use

- **Fix inline math**: Convert `$ formula $` to display math `$$ formula $$`
- **Batch repair**: Fix multiple files at once
- **Format consistency**: Ensure proper math rendering

## Function Call Chain

```
fixFormulaFormats (formulaFixer.ts)
├── read file content
├── apply regex pattern: /^(\s*)\$(\s*)$/gm
├── replace with: $1$$$$$2
└── return fixed content

fixFormulaFormatsInFile
├── read_file(inputPath)
├── fixFormulaFormats(content)
├── if changed: write_file(inputPath, content)
└── return: boolean (modified or not)

batchFixFormulaFormatsInFolder
├── get files in folder (.md, .txt)
├── for each file
│   └── fixFormulaFormatsInFile
└── return: { modifiedCount, errors[] }
```

## Code File

The full TypeScript code is available in: `formulaFixer.ts`

This file contains:

- `fixFormulaFormats()` - Core fix function
- `fixFormulaFormatsInFile()` - Single file processing
- `batchFixFormulaFormatsInFolder()` - Batch processing

## Fix Pattern

### Single-line Formula Conversion

**Input:**

```markdown
$

x^2 + y^2 = z^2

$
```

**Output:**

```markdown
$$

x^2 + y^2 = z^2


$$
```

### Regex Pattern (Current Limitation)

```typescript
// Pattern: ^(\s*)\$(\s*)$
// Matches: start of line, optional whitespace, single $, optional whitespace, end of line

// Replacement: $1$$$$$2
// Result: optional whitespace + $$ + $$ + optional whitespace
```

> [!WARNING] Regex Fragility
> The current line-based regex is highly brittle. It **fails** to properly handle inline math (`The value is $x=2$`), single-line block math containing text (`$x=2$`), or multi-line single-dollar blocks.

### 🚀 Future Robustness Upgrade (AST Parsing)

To make this Agentic skill enterprise-grade, the AI should be instructed to replace this simple Regex with an Abstract Syntax Tree (AST) parser like `remark-math`, or write heavily context-aware regex patterns that track state to safely distinguish between inline `$..$` and block `$$..$$` requirements.

### Usage Example

```typescript
import {
  fixFormulaFormats,
  fixFormulaFormatsInFile,
  batchFixFormulaFormatsInFolder,
} from "./formulaFixer";

// Fix formulas in a string
const content = `...
$

f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx

$
...`;

const fixed = fixFormulaFormats(content);

// Fix formulas in a single file
await fixFormulaFormatsInFile(inputPath, reporter);

// Fix formulas in a folder
const result = await batchFixFormulaFormatsInFolder(folderPath, reporter);
// Returns: { modifiedCount: number, errors: { file: string, message: string }[] }
```

## Batch Processing

### Settings

| Setting                  | Description                     |
| ------------------------ | ------------------------------- |
| `enableBatchParallelism` | Enable parallel processing      |
| `batchConcurrency`       | Number of concurrent operations |
| `batchSize`              | Files per batch                 |

### Progress Reporting

The batch function reports:

- Current file being processed
- Progress percentage
- Cancellation support
- Error collection

## Integration with Other Skills

### Links Processing

After adding wiki-links, `cleanupLatexDelimiters()` is called to fix LaTeX:

```typescript
// From mermaidProcessor.ts
export function cleanupLatexDelimiters(content: string): string {
    // 1. Protect escaped dollars
    processed = processed.replace(/\\\$/g, placeholder);

    // 2. Convert \( and \) to $
    processed = processed.replace(/\\\(/g, '$').replace(/\\\)/g, '$');

    // 3. Trim whitespace inside single $...$
    processed = processed.replace(/\$\s*([^$]*?)\s*\$/g, ...);

    // 4. Restore escaped dollars
    processed = processed.replace(new RegExp(placeholder, 'g'), '$');

    return processed;
}
```

This function handles:

- Converting `\( formula \)` to `$ formula $`
- Removing extra whitespace
- Protecting display math `$$...$$`

## Related skills
- `notemdpro` — for broader NoteMD Pro workflow routing
- `notemdpro-mermaid-healer` — for adjacent syntax-repair work
- `obsidian-markdown` — for markdown and math block context
