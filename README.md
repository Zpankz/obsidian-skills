Agent Skills for use with Obsidian.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code and Codex CLI.

## Available Skills

This repo currently contains **97 skills**, audited into granular marketplace bundles so users can install just the parts they need.

### Marketplace bundles

| Plugin | Focus | Included skills |
|-------|-------|-----------------|
| `obsidian-skills-notes` | Core note authoring, structure, references, and vault interaction | `defuddle`, `obsidian-bases`, `obsidian-cli`, `obsidian-links`, `obsidian-markdown`, `obsidian-markdown-structure`, `obsidian-ref`, `obsidian-yaml-frontmatter` |
| `obsidian-skills-plugins` | Plugin-specific syntax and workflows | `advanced-canvas`, `claudian`, `datacore`, `dataview`, `internetvin-terminal`, `obsidian42-brat`, `tasks`, `templater`, `viva-examiner`, `viva-llm` |
| `obsidian-skills-automation` | Automation, sync, and headless vault ops | `ob` (`obsidian-headless`), `obsidian-cron`, `obsidian-vault-manager` |
| `obsidian-skills-workflows` | Higher-level AI-assisted PKM workflows | `ai4pkm-helper`, `gobi-onboarding`, `interactive-writing-assistant`, `obc`, `obsidian-dream`, `obsidian-learning-path` |
| `obsidian-skills-dev` | Obsidian development, debugging, project ops, theme work, code intelligence, skill discovery, and Gemini API development guidance | `code-intelligence`, `find-skills`, `gemini-api-dev`, `gemini-interactions-api`, `gemini-live-api-dev`, `obsidian-dev`, `obsidian-devtools`, `obsidian-ops`, `obsidian-theme-dev`, `skill-creator` |
| `obsidian-skills-plugin-devkit` | Imported Obsidian plugin development toolkit | `obsidian-plugin-dev` plus 9 specialized `obsidian-plugin-*` skills |
| `obsidian-skills-plugin-ui` | React-focused plugin UI toolkit | `obsidian-plugin-shadcn-ui`, `obsidian-plugin-shadcn-styling`, `obsidian-plugin-shadcn-composition`, `obsidian-plugin-react-best-practices`, `obsidian-plugin-react-performance`, `obsidian-plugin-react-components` |
| `obsidian-skills-visual` | Canvas, diagramming, and presentation workflows | `excalidraw-diagram`, `json-canvas`, `markdown-slides`, `obsidian-canvas`, `obsidian-mermaid` |
| `obsidian-skills-media` | Import/export, transcripts, images, and video pipelines | `docx-to-markdown`, `epub-to-markdown`, `gemini-image-skill`, `markdown-video`, `video-add-chapters`, `video-cleaning`, `video-full-process`, `youtube-transcript-summarizer` |
| `obsidian-skills-extended-graph` | Extended Graph plugin development toolkit | `extended-graph` plus 4 specialized `extended-graph-*` skills |
| `obsidian-skills-smart-connections` | Smart Connections plugin development toolkit | `smart-connections` plus 4 specialized `smart-connections-*` skills |
| `obsidian-skills-breadcrumbs` | Breadcrumbs plugin documentation toolkit | `breadcrumbs` plus 6 specialized `breadcrumbs-*` skills |
| `obsidian-skills-notemdpro` | Imported NoteMD Pro family with umbrella routing plus independent subskills | `notemdpro` plus 13 independent `notemdpro-*` subskills |
| `obsidian-skills-all` | Convenience bundle with every skill in the repo | all 97 skills |

### Cross-bundle integration opportunities

Some of the strongest workflows in this repo come from combining bundles rather than treating them as silos:

- **Breadcrumbs + notes/plugins**: use `obsidian-skills-breadcrumbs` with `obsidian-skills-notes` and `obsidian-skills-plugins` for docs work that mixes wikilinks, frontmatter, Dataview inline fields, and terminology enforcement.
- **Extended Graph + dev**: use `obsidian-skills-extended-graph` with `obsidian-skills-dev` when adding plugin features that also touch Obsidian API patterns, release hygiene, or debugging.
- **Smart Connections + dev/workflows**: use `obsidian-skills-smart-connections` with `obsidian-skills-dev` or `obsidian-skills-workflows` when collection pipelines feed user-facing workflows and plugin UX.
- **Gemini API + plugins/media**: use `obsidian-skills-dev` together with `obsidian-skills-plugins` or `obsidian-skills-media` when building Gemini-powered Obsidian plugins, Live voice flows, or image-generation/document workflows.
- **Plugin devkit + dev/plugins**: use `obsidian-skills-plugin-devkit` with `obsidian-skills-dev` and `obsidian-skills-plugins` when a task spans plugin scaffolding, lifecycle safety, accessibility, release checks, and plugin-specific UX rules.
- **Plugin UI + devkit**: use `obsidian-skills-plugin-ui` with `obsidian-skills-plugin-devkit` when an Obsidian plugin uses React and you want both implementation safety and higher-quality UI composition, theming, or performance.
- **NoteMD Pro + notes/visual/media**: use `obsidian-skills-notemdpro` with `obsidian-skills-notes`, `obsidian-skills-visual`, or `obsidian-skills-media` for markdown generation pipelines that also need link validation, Mermaid output, diagrams, or imported source material.

### Bundle details

#### `obsidian-skills-notes`

| Skill | What it covers |
|---|---|
| [defuddle](skills/defuddle) | Extracts clean markdown from ordinary web pages for reading, summarizing, or saving into a vault |
| [obsidian-bases](skills/obsidian-bases) | Creates and repairs Obsidian Bases `.base` files with views, filters, formulas, and summaries |
| [obsidian-cli](skills/obsidian-cli) | Operates a running Obsidian app through the `obsidian` CLI for live note and app actions |
| [obsidian-links](skills/obsidian-links) | Formats and validates Obsidian wikilinks, section links, and path conventions |
| [obsidian-markdown](skills/obsidian-markdown) | Creates and fixes Obsidian-flavored Markdown with wikilinks, embeds, callouts, tags, and note structure |
| [obsidian-markdown-structure](skills/obsidian-markdown-structure) | Enforces frontmatter placement, heading hierarchy, and overall markdown document structure |
| [obsidian-ref](skills/obsidian-ref) | Provides technical references for manifests, file formats, and Obsidian UX guidance |
| [obsidian-yaml-frontmatter](skills/obsidian-yaml-frontmatter) | Standardizes YAML frontmatter keys, value types, formatting, and link lists |

#### `obsidian-skills-plugins`

| Skill | What it covers |
|---|---|
| [advanced-canvas](skills/advanced-canvas) | Supercharges Obsidian Canvas with presentations, custom shapes, edge styling, portals, collapsible groups, and better export |
| [claudian](skills/claudian) | Embeds Claude Code as an AI collaborator in the vault with multi-tab sessions, inline editing, and agentic file operations |
| [datacore](skills/datacore) | Builds Datacore views with JSX/React syntax and `dc.*` APIs |
| [dataview](skills/dataview) | Creates Dataview DQL, inline queries, and DataviewJS over vault metadata |
| [internetvin-terminal](skills/internetvin-terminal) | Provides an embedded terminal with multi-tab support, bookmarks, output capture, and fullscreen mode |
| [obsidian42-brat](skills/obsidian42-brat) | Installs, manages, and updates beta plugins and themes directly from GitHub repositories |
| [tasks](skills/tasks) | Uses the Tasks plugin syntax for due dates, recurrence, priorities, and task queries |
| [templater](skills/templater) | Creates dynamic Templater templates with `tp.*` functions and automation flows |
| [viva-examiner](skills/viva-examiner) | Conducts real-time voice viva exams powered by Gemini Live with timed stations, scoring, and vault-logged feedback |
| [viva-llm](skills/viva-llm) | Multi-provider vault-integrated LLM with chat, voice calls, terminal, assistants, skills, MCP tools, and agent mode |

#### `obsidian-skills-automation`

| Skill | What it covers |
|---|---|
| [ob / obsidian-headless](skills/ob) | Runs headless Obsidian Sync and Publish workflows with the `ob` CLI in servers, CI, and automation |
| [obsidian-cron](skills/obsidian-cron) | Sets up scheduled and event-driven Obsidian automation with cron, launchd, scripts, and plugin timers |
| [obsidian-vault-manager](skills/obsidian-vault-manager) | Registers local vaults and manages notes, metadata, links, tags, and attachments inside them |

#### `obsidian-skills-workflows`

| Skill | What it covers |
|---|---|
| [ai4pkm-helper](skills/ai4pkm-helper) | Configures AI4PKM orchestrators, agents, pollers, and multi-worker automation workflows |
| [gobi-onboarding](skills/gobi-onboarding) | Provides an interactive Korean-language onboarding guide for Gobi Desktop 3.0 |
| [interactive-writing-assistant](skills/interactive-writing-assistant) | Supports ideation, outlining, drafting, revision, and PKM-connected writing collaboration |
| [obc](skills/obc) | Adds 30 high-level Obsidian vault commands for planning, reflection, discovery, strategy, and synthesis |
| [obsidian-dream](skills/obsidian-dream) | Consolidates long-running PKM session learnings into persistent memory files through a guarded, automation-friendly workflow |
| [obsidian-learning-path](skills/obsidian-learning-path) | Generates adaptive learning-path vaults, canvases, and Bases files for curriculum design, knowledge-gap analysis, and study sequencing |

#### `obsidian-skills-dev`

| Skill | What it covers |
|---|---|
| [code-intelligence](skills/code-intelligence) | Uses GitNexus and Prowl knowledge-graph tooling for repo exploration, dependency-aware refactoring, impact analysis, and codebase tracing |
| [find-skills](skills/find-skills) | Searches the broader agent-skills ecosystem and recommends installable skills when users need capabilities beyond what is already in the repo |
| [gemini-api-dev](skills/gemini-api-dev) | Implements Gemini API integrations with current SDKs, models, multimodal inputs, tools, and structured outputs |
| [gemini-interactions-api](skills/gemini-interactions-api) | Uses the Gemini Interactions API for stateful conversations, streaming, background tasks, tools, and agent-style flows |
| [gemini-live-api-dev](skills/gemini-live-api-dev) | Builds realtime Gemini Live voice/video/text experiences with WebSockets, VAD, native audio, and session management |
| [obsidian-dev](skills/obsidian-dev) | Implements and debugs Obsidian plugins and themes with repo-aware code patterns |
| [obsidian-devtools](skills/obsidian-devtools) | Inspects and automates a running Obsidian instance via Chrome DevTools Protocol |
| [obsidian-ops](skills/obsidian-ops) | Handles builds, linting, troubleshooting, packaging, release prep, and operational maintenance |
| [obsidian-theme-dev](skills/obsidian-theme-dev) | Develops Obsidian themes with CSS/SCSS patterns, variables, and selector guidance |
| [skill-creator](skills/skill-creator) | Creates, refines, benchmarks, and evaluates agent skills themselves |

**Related bundles:** `obsidian-skills-plugin-devkit`, `obsidian-skills-plugin-ui`, `obsidian-skills-plugins`, `obsidian-skills-media`, `obsidian-skills-extended-graph`, `obsidian-skills-smart-connections`

#### `obsidian-skills-plugin-devkit`

This imported bundle vendors and decomposes the upstream [gapmiss/obsidian-plugin-skill](https://github.com/gapmiss/obsidian-plugin-skill) project into an umbrella skill plus focused subskills.

**Umbrella and scaffolding**

| Skill | What it covers |
|---|---|
| [obsidian-plugin-dev](skills/obsidian-plugin-dev) | Umbrella router for Obsidian plugin rules spanning lifecycle safety, API usage, UI/UX, styling, accessibility, and submission readiness |
| [obsidian-plugin-boilerplate](skills/obsidian-plugin-boilerplate) | Scaffolds or retrofits plugin boilerplate with a local interactive generator and metadata validation workflow |

**Specialized plugin-development workflows**

| Skill | What it covers |
|---|---|
| [obsidian-plugin-memory-management](skills/obsidian-plugin-memory-management) | Prevents leaks and lifecycle mistakes around views, events, components, intervals, and unload cleanup |
| [obsidian-plugin-type-safety](skills/obsidian-plugin-type-safety) | Applies safer TypeScript patterns for `TFile`/`TFolder` narrowing, `unknown`, and `const`/`let` usage |
| [obsidian-plugin-ui-ux](skills/obsidian-plugin-ui-ux) | Enforces sentence case, command naming, locale handling, and native-feeling settings and interaction patterns |
| [obsidian-plugin-file-operations](skills/obsidian-plugin-file-operations) | Uses the safest Obsidian-native patterns for editing notes, processing frontmatter, trashing files, and handling paths |
| [obsidian-plugin-css-styling](skills/obsidian-plugin-css-styling) | Styles plugin UIs with `styles.css`, Obsidian CSS variables, scoped selectors, and theme-aware patterns |
| [obsidian-plugin-accessibility](skills/obsidian-plugin-accessibility) | Makes plugin UI keyboard accessible, screen-reader friendly, and touch-safe with proper focus and ARIA support |
| [obsidian-plugin-code-quality](skills/obsidian-plugin-code-quality) | Hardens plugin code for security, mobile compatibility, DOM safety, `requestUrl`, and production-quality cleanup |
| [obsidian-plugin-submission](skills/obsidian-plugin-submission) | Validates manifest naming, packaging, release assets, and community-plugin submission requirements |

The imported plugin-devkit skills are vendored from [gapmiss/obsidian-plugin-skill](https://github.com/gapmiss/obsidian-plugin-skill) under the MIT license and adapted for local marketplace packaging.

**Related bundles:** `obsidian-skills-dev`, `obsidian-skills-plugin-ui`, `obsidian-skills-plugins`, `obsidian-skills-extended-graph`, `obsidian-skills-smart-connections`

#### `obsidian-skills-plugin-ui`

This imported bundle adapts external React UI guidance into Obsidian-plugin-specific skills for teams that build richer plugin frontends with React, Tailwind, and shadcn/ui.

| Skill | What it covers |
|---|---|
| [obsidian-plugin-shadcn-ui](skills/obsidian-plugin-shadcn-ui) | Umbrella router for shadcn/ui usage in React-based Obsidian plugin settings tabs, dialogs, side panels, and custom views |
| [obsidian-plugin-shadcn-styling](skills/obsidian-plugin-shadcn-styling) | Applies shadcn semantic tokens, variants, icon conventions, theming, and CSS-variable customization without brittle overrides |
| [obsidian-plugin-shadcn-composition](skills/obsidian-plugin-shadcn-composition) | Composes forms, cards, tabs, overlays, alerts, empty states, skeletons, and other plugin UI building blocks correctly |
| [obsidian-plugin-react-best-practices](skills/obsidian-plugin-react-best-practices) | Adapts Vercel React and Next.js performance guidance for React-based plugin views, modals, settings tabs, and dashboards |
| [obsidian-plugin-react-performance](skills/obsidian-plugin-react-performance) | Focuses the Vercel guidance on the client-heavy subset most useful for responsive Obsidian plugin interfaces |
| [obsidian-plugin-react-components](skills/obsidian-plugin-react-components) | Refactors React component APIs toward compound components, lifted state, cleaner providers, and less prop-drilling in plugin UIs |

The imported plugin UI skills vendor and adapt material from [shadcn/ui](https://github.com/shadcn/ui) and [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) under the MIT license.

**How to choose within this bundle:** use `obsidian-plugin-shadcn-ui` as the umbrella router, `obsidian-plugin-shadcn-composition` when choosing or assembling UI primitives, `obsidian-plugin-shadcn-styling` when the issue is visual polish or token usage, `obsidian-plugin-react-components` when the component API is getting tangled, and the React best-practices or performance skills when the interface is slow or structurally inefficient.

**Related bundles:** `obsidian-skills-dev`, `obsidian-skills-plugin-devkit`, `obsidian-skills-plugins`, `obsidian-skills-visual`

#### `obsidian-skills-visual`

| Skill | What it covers |
|---|---|
| [excalidraw-diagram](skills/excalidraw-diagram) | Generates Excalidraw diagrams in Obsidian, standard, or animated `.excalidraw` formats |
| [json-canvas](skills/json-canvas) | Creates and repairs raw JSON Canvas `.canvas` files with nodes, edges, groups, and layout-aware connections |
| [markdown-slides](skills/markdown-slides) | Builds Deckset/Marp-compatible markdown slide decks with layout and speaker notes |
| [obsidian-canvas](skills/obsidian-canvas) | Creates and manages Obsidian Canvas files for maps, timelines, and visual summaries |
| [obsidian-mermaid](skills/obsidian-mermaid) | Produces Obsidian-compatible Mermaid diagrams with layout guidance for readability |

#### `obsidian-skills-media`

| Skill | What it covers |
|---|---|
| [docx-to-markdown](skills/docx-to-markdown) | Converts DOCX files to markdown while preserving headings, tables, formatting, metadata, and extracted images |
| [epub-to-markdown](skills/epub-to-markdown) | Converts EPUB books into single markdown files with metadata, TOC structure, and extracted images |
| [gemini-image-skill](skills/gemini-image-skill) | Generates document and slide images with Google Gemini or Imagen models |
| [markdown-video](skills/markdown-video) | Turns markdown slide decks and speaker notes into narrated presentation videos |
| [video-add-chapters](skills/video-add-chapters) | Transcribes videos and generates chapter markers, structured markdown, and optional highlight clips |
| [video-cleaning](skills/video-cleaning) | Removes pauses and filler words from spoken videos using transcription plus frame-accurate edits |
| [video-full-process](skills/video-full-process) | Runs a combined video cleaning and chaptering pipeline with transcript reuse and chapter remapping |
| [youtube-transcript-summarizer](skills/youtube-transcript-summarizer) | Extracts YouTube transcripts and writes structured markdown summaries, key points, and timelines |

#### `obsidian-skills-extended-graph`

This bundle packages specialized development workflows for the `obsidian-extended-graph` plugin.

**Umbrella**

| Skill | What it covers |
|---|---|
| [extended-graph](skills/extended-graph) | Umbrella router for Extended Graph feature work, stats calculators, settings sections, and interactive types |

**Specialized plugin-development workflows**

| Skill | What it covers |
|---|---|
| [extended-graph-plugin-feature](skills/extended-graph-plugin-feature) | Adds a new feature to Extended Graph using the project’s feature-flag, settings, i18n, graph-init, and barrel-export patterns |
| [extended-graph-stat-calculator](skills/extended-graph-stat-calculator) | Adds a new node or link stat calculator and registers it in the stats calculator factories |
| [extended-graph-setting-section](skills/extended-graph-setting-section) | Adds a new settings section using `SettingsSection` or `SettingsSectionPerGraphType` |
| [extended-graph-interactive-type](skills/extended-graph-interactive-type) | Adds a new interactive filter type wired through `InteractiveManager`, legend UI, and interactive settings |

These skills are derived from the generated local project context in `/Users/mikhail/projects/plugins/obsidian-extended-graph/`.

**Related bundles:** `obsidian-skills-dev`, `obsidian-skills-notes`, `obsidian-skills-visual`

#### `obsidian-skills-smart-connections`

This bundle packages specialized development workflows for the `obsidian-smart-connections` plugin.

**Umbrella**

| Skill | What it covers |
|---|---|
| [smart-connections](skills/smart-connections) | Umbrella router for Smart Connections component work, view and command wiring, collection pipelines, and AVA or migration test coverage |

**Specialized plugin-development workflows**

| Skill | What it covers |
|---|---|
| [smart-connections-component-patterns](skills/smart-connections-component-patterns) | Builds and edits Smart Connections components using the project’s `build_html` → `render` → `post_process` lifecycle and listener-guard patterns |
| [smart-connections-view-command-flow](skills/smart-connections-view-command-flow) | Implements Smart Connections views, commands, ribbon actions, settings-tab flows, and leaf-location persistence |
| [smart-connections-collection-pipeline](skills/smart-connections-collection-pipeline) | Updates collection, item, and action pipelines while preserving scoring, filtering, pinned results, and hidden-result behavior |
| [smart-connections-ava-and-migration-harness](skills/smart-connections-ava-and-migration-harness) | Adds or updates focused AVA regression tests and migration harness coverage for utilities and migrations |

**Naming note**

Earlier generated Smart Connections configs may refer to older names like `obsidian-smart-component-patterns`, `obsidian-view-command-flow`, or `ava-and-migration-harness`. In this repo, the canonical marketplace skill names are the namespaced forms:
- `smart-connections-component-patterns`
- `smart-connections-view-command-flow`
- `smart-connections-ava-and-migration-harness`

These skills are derived from the generated local project context in `/Users/mikhail/projects/plugins/obsidian-smart-connections/`.

**Related bundles:** `obsidian-skills-dev`, `obsidian-skills-notes`, `obsidian-skills-workflows`

#### `obsidian-skills-breadcrumbs`

This bundle packages the Breadcrumbs docs-vault skill family generated from the exported Breadcrumbs documentation.

**Umbrella**

| Skill | What it covers |
|---|---|
| [breadcrumbs](skills/breadcrumbs) | Umbrella router for Breadcrumbs docs navigation, editing, terminology, conventions, workflow, and validation |

**Navigation and editing**

| Skill | What it covers |
|---|---|
| [breadcrumbs-nav](skills/breadcrumbs-nav) | Locates the correct Breadcrumbs docs page for a concept, builder, view, command, guide, or suggester |
| [breadcrumbs-edit](skills/breadcrumbs-edit) | Creates and edits Breadcrumbs docs pages using the vault's wikilink, frontmatter, Mermaid, and inline-field conventions |

**Terminology and conventions**

| Skill | What it covers |
|---|---|
| [breadcrumbs-terminology](skills/breadcrumbs-terminology) | Enforces canonical Breadcrumbs terms like `Edge Fields`, `Field Groups`, and `Transitive Implied Relations` |
| [breadcrumbs-code-conventions](skills/breadcrumbs-code-conventions) | Applies docs-vault formatting patterns for links, embeds, frontmatter, codeblocks, and announcements |

**Workflow and validation**

| Skill | What it covers |
|---|---|
| [breadcrumbs-development-workflow](skills/breadcrumbs-development-workflow) | Orients contributors to the Breadcrumbs docs vault structure, editing flow, and Caliber-aware commit workflow |
| [breadcrumbs-testing-guide](skills/breadcrumbs-testing-guide) | Validates wikilinks, image embeds, terminology, frontmatter patterns, and docs integrity before commit |

These skills are derived from the generated Breadcrumbs docs-vault Caliber setup under `breadcrumbs-docs-vault/`.

**Related bundles:** `obsidian-skills-notes`, `obsidian-skills-plugins`, `obsidian-skills-dev`

#### `obsidian-skills-notemdpro`

This imported family is included as **independent skills** as well as an umbrella router skill.

**Umbrella**

| Skill | What it covers |
|---|---|
| [notemdpro](skills/notemdpro) | Umbrella NoteMD Pro skill that routes requests to the right specialized `notemdpro-*` subskill |

**Content and knowledge graph**

| Skill | What it covers |
|---|---|
| [notemdpro-content-generator](skills/notemdpro-content-generator) | Generates comprehensive markdown documents from a title or thin note, optionally with research context |
| [notemdpro-concept-extractor](skills/notemdpro-concept-extractor) | Extracts concepts, terminology, and candidate knowledge nodes from markdown documents |
| [notemdpro-link-analyzer](skills/notemdpro-link-analyzer) | Inserts wiki-links across notes to build an interconnected knowledge graph |
| [notemdpro-qa-extractor](skills/notemdpro-qa-extractor) | Pulls verbatim or targeted answers to specific questions from longer source text |
| [notemdpro-selection-processor](skills/notemdpro-selection-processor) | Processes only a selected snippet of text to save tokens and target specific passages |

**Research and translation**

| Skill | What it covers |
|---|---|
| [notemdpro-web-researcher](skills/notemdpro-web-researcher) | Gathers web research context before generation or summarization |
| [notemdpro-text-translator](skills/notemdpro-text-translator) | Translates markdown notes while preserving formatting and structure |

**Syntax healing and visual summarization**

| Skill | What it covers |
|---|---|
| [notemdpro-mermaid-healer](skills/notemdpro-mermaid-healer) | Fixes Mermaid syntax and structural rendering issues |
| [notemdpro-mermaid-summarizer](skills/notemdpro-mermaid-summarizer) | Converts documents into Mermaid mindmaps and visual summaries |
| [notemdpro-formula-healer](skills/notemdpro-formula-healer) | Repairs LaTeX and math delimiter formatting issues in markdown |

**Processing, architecture, and regression safety**

| Skill | What it covers |
|---|---|
| [notemdpro-batch-processor](skills/notemdpro-batch-processor) | Runs NoteMD-style operations safely across many markdown files with batching, throttling, and failure handling |
| [notemdpro-system-architecture](skills/notemdpro-system-architecture) | Explains the NoteMD Pro architecture, dependencies, and FileSystemPort-driven design |
| [notemdpro-test-driven-development](skills/notemdpro-test-driven-development) | Guides safe changes to NoteMD Pro utilities through regression-test discipline |

The imported NoteMD Pro skills are vendored from [Zpankz/notemdpro](https://github.com/Zpankz/notemdpro) under the MIT license and adapted for local marketplace packaging.

**Related bundles:** `obsidian-skills-notes`, `obsidian-skills-visual`, `obsidian-skills-media`, `obsidian-skills-workflows`

#### `obsidian-skills-all`

This bundle contains **every skill listed above** and is the recommended install if you want the old monolithic bundle experience.

## Installation

### Claude Code Plugin Marketplace

Add this repo to your Claude Code marketplace, then install one or more bundles:

```
/plugin marketplace add <owner>/obsidian-skills
/plugin install obsidian-skills-notes
/plugin install obsidian-skills-plugins
/plugin install obsidian-skills-automation
```

Other available bundles:
- `obsidian-skills-workflows`
- `obsidian-skills-dev`
- `obsidian-skills-plugin-devkit`
- `obsidian-skills-plugin-ui`
- `obsidian-skills-visual`
- `obsidian-skills-media`
- `obsidian-skills-extended-graph`
- `obsidian-skills-smart-connections`
- `obsidian-skills-breadcrumbs`
- `obsidian-skills-notemdpro`
- `obsidian-skills-all`

Install `obsidian-skills-all` if you want the old “everything in one install” experience.

### Migration from legacy bundles

The old two-bundle layout has been replaced by more granular distributions.

| Old bundle | Recommended replacement |
|---|---|
| `obsidian-skills-core` | `obsidian-skills-all` for a drop-in “install everything” experience, or install `obsidian-skills-notes` + `obsidian-skills-plugins` + `obsidian-skills-automation` + `obsidian-skills-workflows` + `obsidian-skills-dev` + `obsidian-skills-plugin-devkit` + `obsidian-skills-plugin-ui` + `obsidian-skills-visual` to stay closer to the previous core footprint |
| `obsidian-skills-extras` | `obsidian-skills-workflows` + `obsidian-skills-media`, and add `obsidian-skills-visual` if you also want `markdown-slides` |

Notes:
- `ob` / `obsidian-headless` is now included in `obsidian-skills-automation`
- `obsidian-skills-all` includes every current skill in the repository
- `obsidian-skills-plugin-devkit` is the dedicated home for plugin-specific scaffolding, lifecycle, accessibility, and submission guidance
- `obsidian-skills-plugin-ui` adds React, shadcn/ui, theming, composition, and UI-performance guidance for richer plugin frontends

### npx skills

```
npx skills add git@github.com:kepano/obsidian-skills.git
```

### Manual installation

Copy the `skills` folder to your vault's `.claude` directory:

```
your-vault/
├── .claude/
│   └── skills/
│       ├── dataview/SKILL.md
│       ├── templater/SKILL.md
│       └── tasks/SKILL.md
└── ... your notes ...
```

Or clone this repo and symlink:

```bash
git clone https://github.com/kepano/obsidian-skills.git
ln -s /path/to/obsidian-skills/skills /path/to/your-vault/.claude/skills
```

#### Claude Code

Add the contents of this repo to a `/.claude` folder in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex CLI

Copy the `skills/` directory into your Codex skills path (typically `~/.codex/skills`). See the [Agent Skills specification](https://agentskills.io/specification) for the standard skill format.

#### OpenCode

Clone the entire repo into the OpenCode skills directory (`~/.opencode/skills/`):

```sh
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

Do not copy only the inner `skills/` folder — clone the full repo so the directory structure is `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`.

OpenCode auto-discovers all `SKILL.md` files under `~/.opencode/skills/`. No changes to `opencode.json` or any config file are needed. Skills become available after restarting OpenCode.

## Skill Coverage

### Dataview
- DQL query types (LIST, TABLE, TASK, CALENDAR)
- FROM/WHERE/SORT/GROUP BY/FLATTEN clauses
- Inline fields and implicit fields
- All functions (string, numeric, date, array)
- DataviewJS API

### Datacore
- JSX/React view syntax
- Query hooks (dc.useQuery, dc.useCurrentFile)
- Type queries (@page, @task, @section, @block)
- Built-in components (dc.Table, dc.List, dc.Callout)
- State management with React hooks

### Templater
- Template syntax (`<% %>` vs `<%* %>`)
- All tp.* modules (date, file, system, web, config, frontmatter, hooks)
- Moment.js date formatting
- Complete template examples

### Tasks
- Task syntax (emojis and text formats)
- All date types and priorities
- Recurrence patterns
- Query filters, sorts, groups
- Custom statuses

## Fork README (sunnyhasija/obsidian-plugin-skills)

<details>
<summary>Appendix: Original README from <code>sunnyhasija/obsidian-plugin-skills</code></summary>

# Obsidian Plugin Skills for Claude Code

Claude Code skills for popular Obsidian plugins. These reference documents help Claude generate accurate plugin-specific syntax.

## What are Claude Code Skills?

[Skills](https://docs.anthropic.com/en/docs/claude-code/skills) are markdown files that Claude automatically loads when relevant keywords appear in your requests. When you mention "Dataview query" or "Templater template", Claude references these skills to generate correct syntax.

## Available Skills

| Skill | Plugin | Upstream PR |
|-------|--------|-------------|
| [Dataview](skills/dataview/SKILL.md) | [obsidian-dataview](https://github.com/blacksmithgu/obsidian-dataview) | [#2651](https://github.com/blacksmithgu/obsidian-dataview/pull/2651) |
| [Datacore](skills/datacore/SKILL.md) | [datacore](https://github.com/blacksmithgu/datacore) | [#158](https://github.com/blacksmithgu/datacore/pull/158) |
| [Templater](skills/templater/SKILL.md) | [Templater](https://github.com/SilentVoid13/Templater) | [#1682](https://github.com/SilentVoid13/Templater/pull/1682) |
| [Tasks](skills/tasks/SKILL.md) | [obsidian-tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) | [#3732](https://github.com/obsidian-tasks-group/obsidian-tasks/pull/3732) |

## Installation

Copy the `skills` folder to your vault's `.claude` directory:

```
your-vault/
├── .claude/
│   └── skills/
│       ├── dataview/SKILL.md
│       ├── templater/SKILL.md
│       └── tasks/SKILL.md
└── ... your notes ...
```

Or clone this repo and symlink:

```bash
git clone https://github.com/sunnyhasija/obsidian-plugin-skills.git
ln -s /path/to/obsidian-plugin-skills/skills /path/to/your-vault/.claude/skills
```

## Skill Coverage

### Dataview
- DQL query types (LIST, TABLE, TASK, CALENDAR)
- FROM/WHERE/SORT/GROUP BY/FLATTEN clauses
- Inline fields and implicit fields
- All functions (string, numeric, date, array)
- DataviewJS API

### Datacore
- JSX/React view syntax
- Query hooks (dc.useQuery, dc.useCurrentFile)
- Type queries (@page, @task, @section, @block)
- Built-in components (dc.Table, dc.List, dc.Callout)
- State management with React hooks

### Templater
- Template syntax (`<% %>` vs `<%* %>`)
- All tp.* modules (date, file, system, web, config, frontmatter, hooks)
- Moment.js date formatting
- Complete template examples

### Tasks
- Task syntax (emojis and text formats)
- All date types and priorities
- Recurrence patterns
- Query filters, sorts, groups
- Custom statuses

## Related Projects

- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) - Core Obsidian syntax (Markdown, Canvas, Bases)

## License

MIT

</details>

## License

MIT
