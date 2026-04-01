# In-app automation

Use this reference when the job should run from inside Obsidian rather than from the operating system scheduler.

## Shell Commands plugin

Best for lightweight automation while Obsidian is open.

Useful triggers:
- every N seconds
- Obsidian startup or quit
- file created, modified, deleted, moved
- active editor or pane changes
- URI-based command execution

Strengths:
- easy to wire shell commands to app events
- supports dynamic variables such as date, file path, selection, and clipboard
- can route output to notifications, status bar, clipboard, or notes

Limitation:
- interval mode is timer-based, not true cron syntax
- not ideal for heavy jobs or precise calendar scheduling

## obsidian-cron plugin

Use when the user wants cron expressions inside Obsidian.

Example:

```javascript
const cron = app.plugins.plugins.cron.api;
cron.addCronJob('vault-health', '0 6 * * *', { enableMobile: false }, async (app) => {
  const files = app.vault.getFiles();
  console.log(`Vault has ${files.length} files`);
});
```

Strengths:
- true 5-field cron expressions
- callback gets `app`
- can coordinate with sync-aware workflows

Caveat:
- community-maintained and less active than the official CLI route

## Startup execution

Use these only when the job should run once at app launch.

### CodeScript Toolkit
Good for JS/TS startup scripts, bootstrap logic, pseudo-plugin patterns, and hot reload oriented workflows.

### JS Engine
Good for startup scripts and modular JS imported from the vault.

### Templater startup templates
Good for launch-time template-driven initialization. Can call external JS from the vault.

## Selection guide

Choose:
- **Shell Commands** for event-driven and interval work
- **obsidian-cron** for true cron inside the app
- **CodeScript Toolkit / JS Engine / Templater startup** for launch-time bootstrap only

## Related skill handoff

If the in-app automation becomes real plugin development, switch to `obsidian-dev` for implementation guidance.
If the commands themselves are better expressed through the official CLI, pair with `obsidian-cli`.