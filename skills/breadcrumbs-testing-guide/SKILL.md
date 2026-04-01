---
name: breadcrumbs-testing-guide
description: "Use this skill to validate Breadcrumbs docs integrity through wikilink checks, image embed checks, terminology validation, frontmatter checks, and announcement-chain verification. Do NOT use it for plugin unit or integration tests."
---
# Testing Guide

Validation patterns for the Breadcrumbs documentation vault. This project is a Markdown docs vault — "testing" means structural validation, terminology checks, broken link detection, and content consistency verification.

## Critical

- This vault has **no test framework** (no Jest, Vitest, or similar). All validation is done via shell commands (`rg`, `find`, `diff`).
- Never modify docs files as part of a validation pass — report issues only.
- Terminology must match the canonical terms in `CLAUDE.md` and `Concepts.md`. Do not accept synonyms (e.g., "Edge Types" instead of "Edge Fields").
- Image references use `![[filename.png]]` — never `![alt](path)` markdown syntax.
- Internal links use `[[wikilink]]` — never `[text](file.md)` syntax between docs pages.

## Instructions

### Step 1: Validate wikilink targets exist

Extract all `[[wikilink]]` targets and verify each resolves to an existing `.md` file in the vault.

```bash
# Extract all wikilink targets (strip display text after |)
rg -oN '\[\[([^\]|]+)' --type md --no-filename -r '$1' | sort -u > /tmp/bc-link-targets.txt

# List all page basenames (without .md)
find . -name '*.md' -not -path './Images/*' | sed 's|.*/||;s|\.md$||' | sort -u > /tmp/bc-pages.txt

# Find broken links (targets with no matching page)
comm -23 /tmp/bc-link-targets.txt /tmp/bc-pages.txt
```

**Verify**: The `comm` output should be empty. Any lines shown are broken wikilinks. Note: some targets may be aliases — cross-check against `aliases` in frontmatter before flagging.

### Step 2: Validate image embeds resolve

Every `![[image.png]]` embed must have a corresponding file in `Images/`.

```bash
# Extract all image embed targets
rg -oN '!\[\[([^\]]+\.png)\]\]' --type md --no-filename -r '$1' | sort -u > /tmp/bc-image-refs.txt

# List actual images
ls Images/*.png 2>/dev/null | sed 's|Images/||' | sort -u > /tmp/bc-images.txt

# Find missing images
comm -23 /tmp/bc-image-refs.txt /tmp/bc-images.txt
```

**Verify**: Output should be empty. Any lines are missing image files.

### Step 3: Check terminology consistency

The following canonical terms must be used exactly — not paraphrased or abbreviated:

| Canonical Term | Common Mistakes |
|---|---|
| Edge Fields | edge types, link types, field types |
| Field Groups | field sets, field collections |
| Explicit Edge Builders | explicit edges, manual edges |
| Implied Edge Builders | implicit edges, inferred edges |
| Transitive Implied Relations | transitive rules, chain rules |
| Note Attributes | note properties, BC attributes |
| BC-ignore-in-edges | BC-ignore-in, ignore-in-edges |
| BC-ignore-out-edges | BC-ignore-out, ignore-out-edges |

```bash
# Check for common wrong terms (case-insensitive)
rg -in 'edge types|link types|field types|field sets|implicit edges|inferred edges|transitive rules|chain rules' --type md
```

**Verify**: Output should be empty. Any matches indicate terminology that should be replaced with the canonical term.

### Step 4: Validate frontmatter patterns

Folder index pages (`Commands/Commands.md`, `Views/Views.md`, `Suggesters/Suggesters.md`) must have `BC-folder-note-field: down` in frontmatter.

```bash
# Check folder index pages have required frontmatter
for f in Commands/Commands.md Views/Views.md Suggesters/Suggesters.md; do
  if [ -f "$f" ]; then
    grep -q 'BC-folder-note-field:' "$f" || echo "MISSING BC-folder-note-field in $f"
  fi
done
```

**Verify**: No "MISSING" lines should appear.

### Step 5: Validate Announcement chaining

Announcement pages should chain via `next:: [[Announcement ...]]` inline fields. Verify the chain is unbroken.

```bash
# List announcements and their next links
for f in Announcements/Announcement*.md; do
  next=$(rg -oN 'next:: \[\[([^\]]+)\]\]' "$f" -r '$1' 2>/dev/null)
  echo "$f -> ${next:-END}"
done
```

**Verify**: Each announcement (except the latest) should point to the next one. No target should be missing from the vault.

### Step 6: Validate Mermaid diagram syntax

Mermaid blocks should use valid graph syntax.

```bash
# Find all mermaid blocks and check they start with a valid directive
rg -l '```mermaid' --type md
```

**Verify**: Manually inspect each file. Mermaid blocks should start with `graph LR`, `graph TD`, `flowchart LR`, or `flowchart TD`.

### Step 7: Check for markdown-style links between docs pages

Internal cross-references must use `[[wikilinks]]`, not `[text](file.md)` markdown links.

```bash
# Find markdown links pointing to local .md files (should be wikilinks instead)
rg -n '\[([^\]]*)\]\((?!http)[^)]*\.md\)' --type md
```

**Verify**: Output should be empty. External links (starting with `http`) are fine.

### Step 8: Run full validation suite

Combine all checks into one pass:

```bash
echo "=== Broken wikilinks ==="
rg -oN '\[\[([^\]|]+)' --type md --no-filename -r '$1' | sort -u | while read target; do
  find . -name "${target}.md" -not -path './Images/*' | grep -q . || echo "  BROKEN: [[${target}]]"
done

echo "=== Missing images ==="
rg -oN '!\[\[([^\]]+\.png)\]\]' --type md --no-filename -r '$1' | sort -u | while read img; do
  [ -f "Images/$img" ] || echo "  MISSING: ![[${img}]]"
done

echo "=== Wrong terminology ==="
rg -in 'edge types|link types|field types|field sets|implicit edges|inferred edges|transitive rules|chain rules' --type md || echo "  (none found)"

echo "=== Markdown links (should be wikilinks) ==="
rg -n '\[([^\]]*)\]\((?!http)[^)]*\.md\)' --type md || echo "  (none found)"
```

## Examples

### Example 1: Validate after editing a docs page

User says: "I just updated Typed Links.md, check if everything is consistent"

Actions taken:
1. Run Step 1 (wikilink validation) scoped to the changed file:
   ```bash
   rg -oN '\[\[([^\]|]+)' 'Explicit Edge Builders/Typed Links.md' -r '$1' | while read target; do
     find . -name "${target}.md" -not -path './Images/*' | grep -q . || echo "BROKEN: [[${target}]]"
   done
   ```
2. Run Step 2 (image validation) scoped to the file
3. Run Step 3 (terminology check) scoped to the file
4. Report findings

Result: "All 12 wikilinks in Typed Links.md resolve. 2 image embeds verified. No terminology issues found."

### Example 2: Pre-commit full validation

User says: "Run tests before I commit"

Actions taken:
1. Run Step 8 (full validation suite) from the vault root
2. Report any issues grouped by category
3. If clean: "All validation checks passed — safe to commit."

### Example 3: Check a specific term

User says: "Make sure we never say 'implicit edges' anywhere"

Actions taken:
1. Run targeted grep:
   ```bash
   rg -in 'implicit edges' --type md
   ```
2. Report: "Found 0 occurrences. The vault consistently uses 'Implied Edge Builders' as the canonical term."

## Common Issues

**Broken wikilink to an aliased page**
If `comm` reports a broken link but the target exists as an alias:
1. Check frontmatter: `rg -A5 '^---' TargetPage.md | grep aliases`
2. If the alias matches the link target, it's valid — not a broken link
3. The validation in Step 1 does not check aliases automatically; cross-reference manually

**Image embed shows `![[image.png]]` but file is missing**
1. Check if the filename has different casing: `ls Images/ | grep -i 'imagename'`
2. Check if the image was referenced but never downloaded (see `DOWNLOAD_INFO.md` for source)
3. If the image genuinely doesn't exist, flag it for the content author

**`rg` returns "No files found" or command not found**
1. Ensure you're running from the vault root: `pwd` should show `breadcrumbs-docs-vault/`
2. If `rg` is unavailable, use `grep -rn` as fallback (slower but functional)
3. The `--type md` flag requires ripgrep — with `grep` use `--include='*.md'` instead

**False positive: external URL flagged as local markdown link**
The regex in Step 7 excludes `http` prefixes, but `ftp://` or other protocols may match.
1. Review flagged lines manually
2. If the link starts with a protocol, it's external — ignore it

**Announcement chain appears broken but newest post has no `next::`**
This is expected — the most recent announcement is the chain terminus and should NOT have a `next::` field. Only flag missing `next::` on non-terminal announcements.

## Related skills
- `breadcrumbs` — for broader Breadcrumbs workflow routing
- `breadcrumbs-nav` — to resolve broken targets or ambiguous page names
- `breadcrumbs-terminology` — when validation turns up naming inconsistencies
