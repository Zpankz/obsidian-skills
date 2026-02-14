Agent Skills for use with Obsidian.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code and Codex CLI.

## Available Skills

### Core Skills

| Skill | Description |
|-------|-------------|
| [obsidian-markdown](skills/obsidian-markdown) | Create and edit [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown) (`.md`) with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax |
| [obsidian-bases](skills/obsidian-bases) | Create and edit [Obsidian Bases](https://help.obsidian.md/bases/syntax) (`.base`) with views, filters, formulas, and summaries |
| [json-canvas](skills/json-canvas) | Create and edit [JSON Canvas](https://jsoncanvas.org/) files (`.canvas`) with nodes, edges, groups, and connections |
| [obsidian-cli](skills/obsidian-cli) | Interact with Obsidian vaults via the [Obsidian CLI](https://help.obsidian.md/cli) including plugin and theme development |
| [defuddle](skills/defuddle) | Extract clean markdown from web pages using [Defuddle](https://github.com/kepano/defuddle-cli), removing clutter to save tokens |

### Plugin Skills (for Claude Code)

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
git clone https://github.com/kepano/obsidian-skills.git
ln -s /path/to/obsidian-skills/skills /path/to/your-vault/.claude/skills
```

#### Claude Code

Add the contents of this repo to a `/.claude` folder in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex CLI

Copy the `skills/` directory into your Codex skills path (typically `~/.codex/skills`). See the [Agent Skills specification](https://agentskills.io/specification) for the standard skill format.

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
