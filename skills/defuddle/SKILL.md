---
name: defuddle
description: Extract clean markdown from web pages using Defuddle CLI, removing clutter to save tokens. Use when the user provides a URL to read or analyze.
---

# Defuddle Web Content Extractor

Use Defuddle to turn cluttered web pages into clean, readable Markdown before analysis or saving.

This is the default choice for ordinary public web pages because it usually preserves the main content while stripping navigation, ads, sidebars, and other token-wasting noise.

## When to use this skill

Typical triggers:
- "read this URL"
- "save this article as markdown"
- "extract the text from this page"
- "scrape this documentation page"
- "clean up this web content before summarizing it"

## When not to rely on Defuddle alone

Defuddle is not always the right tool for:
- login-protected pages
- sites that require heavy JavaScript interaction to reveal content
- workflows that need raw HTML structure rather than cleaned text

If extraction looks incomplete, switch to a browser-capable or raw-HTML approach.

## Quick start

Check availability and install if needed:

```bash
which defuddle || npm install -g defuddle
```

Extract readable Markdown:

```bash
defuddle parse <url> --md
```

## Recommended workflow

1. **Extract first** using `--md`
2. **Review the output** for missing sections or weird truncation
3. **Save to a file** if the page is long or will be reused
4. **Only fall back to raw HTML or another tool** if the cleaned output is obviously incomplete

## Common command patterns

### Read a page immediately

```bash
defuddle parse https://example.com/article --md
```

Use this when the next step is summarizing, analyzing, or quoting the content.

### Save a cleaned copy

```bash
defuddle parse https://docs.example.com/page --md -o documentation.md
defuddle parse https://blog.example.com/post --md -o notes/post-title.md
```

Use this when the page is long, should be archived, or should be processed later.

### Extract metadata only

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p author
defuddle parse <url> -p publishDate
defuddle parse <url> -p domain
```

Use this when building link catalogs or collecting source metadata without the full body.

### Use JSON output when needed

```bash
defuddle parse <url> --json
```

Use JSON only when you specifically need both HTML and Markdown output. For ordinary reading and summarization, `--md` is the better default.

## Quality checks

After extraction, verify:
1. the main heading and article body are present
2. obvious navigation/sidebar clutter is gone
3. the content is complete enough for the user's task

If the page is missing major sections, the site may be rendering content client-side.

## Why this skill matters

A raw documentation or news page can include huge amounts of HTML that add tokens but not meaning. Defuddle usually reduces that noise dramatically while keeping the information humans actually care about. That makes downstream summarization, note-taking, or conversion work cheaper and more reliable.

## Output expectations

When using this skill, make it clear:
- which URL you extracted
- whether you returned inline Markdown or saved a file
- whether the extraction looked complete
- whether a fallback tool may be needed
