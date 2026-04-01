---
name: obsidian-cli
description: "Use this skill for operating a running Obsidian app through the `obsidian` CLI: read/create/search notes, update properties and tasks, target specific vaults, reload plugins, inspect the DOM, capture errors or screenshots, and run app-context JavaScript. Trigger whenever the user wants live Obsidian operations from the terminal instead of direct file edits. Do not use if Obsidian is not open or the task is just ordinary Markdown editing."
---

# Obsidian CLI

Use the `obsidian` CLI to work through a running Obsidian instance instead of treating the vault like a plain folder.

This skill is especially valuable when the user wants **live vault operations** or **plugin/theme debugging inside the app**.

## Preconditions

- Obsidian must be open.
- The Obsidian CLI must be installed and available as `obsidian`.
- When working with a specific vault, prefer `vault="..."` so commands target the right place.

If you're unsure which commands exist, run:

```bash
obsidian help
```

Official docs: https://help.obsidian.md/cli

## Working method

1. Decide whether the task is about **note content**, **vault querying**, or **developer tooling**.
2. Identify the right vault before making changes.
3. Prefer precise targeting:
   - `file="My Note"` for wikilink-style resolution
   - `path="Folder/My Note.md"` for exact path targeting
4. Quote values with spaces.
5. After mutating commands, verify the result with a read/search/list command when practical.

## Syntax reminders

Parameters take values with `=`:

```bash
obsidian create name="My Note" content="# Hello"
```

Boolean flags do not take values:

```bash
obsidian create name="My Note" content="Hello" silent overwrite
```

For multiline content, use escaped newlines and tabs:

```bash
obsidian append file="My Note" content="Line 1\nLine 2\n- bullet"
```

## Vault targeting

Commands default to the most recently focused vault. Use an explicit vault when ambiguity would be risky:

```bash
obsidian vault="Work Vault" search query="roadmap"
```

## File targeting

Most file-aware commands accept one of:

- `file="Note Name"` — resolves like an internal link
- `path="Folder/Note.md"` — exact vault-relative path

Prefer `path=` when multiple notes may share a name.

## Core note workflows

### Read and inspect notes

```bash
obsidian read file="My Note"
obsidian read path="Projects/Alpha.md"
obsidian backlinks file="My Note"
```

### Create and update notes

```bash
obsidian create name="New Note" content="# Title"
obsidian create name="New Note" content="# Title" template="Meeting" silent
obsidian append file="Daily Note" content="\n- [ ] Follow up"
```

### Search vault content

```bash
obsidian search query="status: active" limit=20
obsidian tags sort=count counts
obsidian backlinks file="Architecture"
```

### Manage properties and tasks

```bash
obsidian property:set file="Project Alpha" name="status" value="done"
obsidian daily:read
obsidian daily:append content="- [ ] Send update"
obsidian tasks daily todo
```

## Developer workflows

Use these commands when the user is building or debugging Obsidian plugins and themes.

### Plugin/theme edit loop

After changing plugin or theme code:

1. Reload the plugin:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. Check for runtime errors:
   ```bash
   obsidian dev:errors
   ```
3. Inspect console output if needed:
   ```bash
   obsidian dev:console level=error
   ```
4. Verify visually:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```

### App-context evaluation

```bash
obsidian eval code="app.vault.getFiles().length"
obsidian dev:css selector=".workspace-leaf" prop=background-color
obsidian dev:mobile on
```

Use these commands when file edits alone are not enough and the user needs information from the running app.

## High-value command patterns

Use `--copy` when the result should be placed on the clipboard.
Use `silent` when you do not want Obsidian to open files or steal focus.
Use `total` on list-style commands when the user wants counts as well as results.

## Common mistakes to avoid

- assuming the default vault is the correct vault
- using `file=` when duplicate note names make the target ambiguous
- sending multiline text without escaped newlines
- mutating notes without verifying the result
- editing plugin code but forgetting to reload and inspect errors in the running app

## Troubleshooting

### Command succeeds but affects the wrong note
Use `path=` or specify `vault=` explicitly.

### No visible effect after code changes
Reload the plugin or theme, then run:
```bash
obsidian dev:errors
obsidian dev:console level=error
```

### Need more commands than this skill lists
Run:
```bash
obsidian help
```
Because the CLI surface can evolve, treat `obsidian help` as the current source of truth.

## Output expectations

When using this skill, report:
- the exact command(s) you ran
- which vault/file was targeted
- what changed or what you observed
- any follow-up validation still recommended
