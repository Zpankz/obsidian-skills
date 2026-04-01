---
name: notemdpro
description: "Use this umbrella skill when a task spans multiple NoteMD Pro workflows and you need to route to the right specialized notemdpro-* skill."
---

# NoteMD Pro Toolkit

Use this umbrella skill when a task spans multiple NoteMD Pro workflows and you need to route to the right specialized skill.

These imported skills were adapted from the upstream NoteMD Pro skill library for use inside `obsidian-skills`.

## Route to these independent skills

### Content and knowledge-graph building
- `notemdpro-content-generator` — generate full markdown from a title or thin stub
- `notemdpro-concept-extractor` — extract concepts and candidate knowledge nodes
- `notemdpro-link-analyzer` — add wiki-links across notes to build graph structure
- `notemdpro-selection-processor` — process only a selected passage instead of a whole file
- `notemdpro-qa-extractor` — extract answers to specific questions from long text

### Research and translation
- `notemdpro-web-researcher` — gather external research context before drafting or summarizing
- `notemdpro-text-translator` — translate markdown while preserving structure

### Diagram and formula repair
- `notemdpro-mermaid-healer` — fix Mermaid syntax and structural issues
- `notemdpro-mermaid-summarizer` — summarize documents as Mermaid mindmaps
- `notemdpro-formula-healer` — fix LaTeX/math delimiter issues

### Scaling and maintenance
- `notemdpro-batch-processor` — run NoteMD-style operations safely across many files
- `notemdpro-system-architecture` — inspect the NoteMD Pro architecture and module boundaries
- `notemdpro-test-driven-development` — protect NoteMD Pro utility changes with regression tests

## Decision guide
- User wants a note written from a title → `notemdpro-content-generator`
- User wants concepts or graph nodes extracted → `notemdpro-concept-extractor`
- User wants automatic wiki-link insertion → `notemdpro-link-analyzer`
- User wants research before writing → `notemdpro-web-researcher`
- User wants translation with markdown preserved → `notemdpro-text-translator`
- Mermaid is broken → `notemdpro-mermaid-healer`
- User wants a Mermaid mindmap summary → `notemdpro-mermaid-summarizer`
- LaTeX or math delimiters are broken → `notemdpro-formula-healer`
- Need to process many files or avoid rate-limit / OOM issues → `notemdpro-batch-processor`
- Need to understand internals or safely modify core logic → `notemdpro-system-architecture` or `notemdpro-test-driven-development`

## Local paths
- `skills/notemdpro-content-generator/SKILL.md`
- `skills/notemdpro-concept-extractor/SKILL.md`
- `skills/notemdpro-link-analyzer/SKILL.md`
- `skills/notemdpro-selection-processor/SKILL.md`
- `skills/notemdpro-qa-extractor/SKILL.md`
- `skills/notemdpro-web-researcher/SKILL.md`
- `skills/notemdpro-text-translator/SKILL.md`
- `skills/notemdpro-mermaid-healer/SKILL.md`
- `skills/notemdpro-mermaid-summarizer/SKILL.md`
- `skills/notemdpro-formula-healer/SKILL.md`
- `skills/notemdpro-batch-processor/SKILL.md`
- `skills/notemdpro-system-architecture/SKILL.md`
- `skills/notemdpro-test-driven-development/SKILL.md`

## Related skills
- `notemdpro-content-generator` — for full-document generation from a title or stub
- `notemdpro-link-analyzer` — for wiki-linking and graph construction
- `notemdpro-mermaid-healer` — for Mermaid repair and cleanup
- `obsidian-markdown` — for general markdown authoring and note-structure guidance
- `obsidian-links` — for wikilink conventions and validation
- `obsidian-mermaid` — for Mermaid authoring patterns complementary to NoteMD Pro healing/summarization

## Notes
- These imported skills are file-system based and do not rely on `app.vault`.
- Prefer the specialized `notemdpro-*` skill when the task is narrow and obvious.
- Use this umbrella skill when the task spans multiple NoteMD Pro operations.
