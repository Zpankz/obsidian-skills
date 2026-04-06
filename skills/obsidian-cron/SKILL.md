---
name: obsidian-cron
description: "Set up scheduled or event-driven Obsidian automation: cron jobs, launchd agents, periodic vault maintenance, and startup scripts. Trigger when the user wants Obsidian to run something automatically."
compatibility: "Best results when the Obsidian CLI is installed and Obsidian is running. This skill often pairs with bash, file editing, and community plugins such as Shell Commands, obsidian-cron, CodeScript Toolkit, JS Engine, or Templater."
---

# Obsidian Scheduled Automation

Use this skill when the user wants Obsidian to **do something automatically** instead of manually opening the app and clicking commands.

This includes:
- daily or weekly routines
- cron jobs and `launchd` agents
- note maintenance or vault health checks
- scheduled exports for agent workflows
- startup bootstrapping inside Obsidian
- file-event or interval-based automation while Obsidian is open

## Primary decision

Pick the execution surface before writing code.

1. **External scheduler + Obsidian CLI** — best default for reliable scheduled jobs.
2. **Shell Commands plugin** — best for lightweight event-driven or every-N-seconds actions while Obsidian is open.
3. **obsidian-cron plugin** — best when the user specifically wants true cron syntax inside Obsidian and needs direct app API access.
4. **Startup scripts** via CodeScript Toolkit, JS Engine, or Templater — best for things that should run once when Obsidian launches, not on a repeating schedule.

If the user is on **macOS**, prefer **`launchd` over `cron`** for scheduled jobs because it handles sleep/wake more reliably.

Read these references as needed:
- `references/decision-matrix.md` — choose the right automation surface quickly.
- `references/system-schedulers.md` — `launchd`, `cron`, script layout, logging, validation.
- `references/in-app-automation.md` — Shell Commands, obsidian-cron, startup execution options.
- `references/job-recipes.md` — reusable patterns and concrete examples.

## Working method

### 1) Clarify the job
Identify:
- **trigger**: exact time, interval, startup, file event, or manual URI
- **scope**: one note, daily note, search results, plugin command, or arbitrary JS
- **environment**: macOS, Linux, or another OS
- **dependency surface**: Obsidian CLI only, or a plugin API inside the app
- **failure tolerance**: can the job be skipped, retried, or safely re-run?

### 2) Choose the safest pattern
Use this order of preference:

- Choose **Obsidian CLI + scheduler** when the task can be expressed as CLI commands.
- Choose **Shell Commands** when the task is tightly coupled to Obsidian being open and reacting to events.
- Choose **obsidian-cron** when the user explicitly wants cron expressions inside the app or needs direct `app` access on a schedule.
- Choose **startup scripts** only for launch-time bootstrapping.

### 3) Make the job idempotent
Scheduled jobs often run more than once, run late, or overlap.

Design them so they are safe to repeat:
- append only when duplication is acceptable, otherwise check first
- write logs to predictable paths
- avoid destructive edits unless the user explicitly wants them
- prefer one script file per job instead of giant inline commands
- if overlap matters, add simple locking or guard files

### 4) Validate before scheduling
Before installing a scheduler:
1. run the underlying script manually
2. verify the CLI command works against the intended vault
3. confirm quoting for paths with spaces
4. confirm the output/log location exists or can be created
5. only then write the `launchd`, `cron`, or plugin config

### 5) Report the full automation package
When completing the task, provide:
- the script path you created or edited
- the scheduler config path
- the exact schedule
- required plugins or settings
- how to test manually
- how to inspect logs or failures

## Core patterns

### Pattern A: External scheduler + Obsidian CLI
Use this for recurring routines, exports, sync-adjacent automation, and vault maintenance.

Typical structure:
1. create a shell script in a user-approved scripts folder
2. use explicit `vault="..."` targeting when ambiguity would be risky
3. redirect stdout/stderr to logs
4. schedule the script with `launchd` or `cron`

Example shape:

```bash
#!/bin/bash
set -euo pipefail

obsidian vault="Research" daily
obsidian vault="Research" daily:append content="- [ ] Review inbox\n- [ ] Check calendar"
obsidian vault="Research" search query="status::active" format=json > "$HOME/tmp/active_notes.json"
```

For exact CLI syntax, also consult `../obsidian-cli/SKILL.md`.

### Pattern B: Shell Commands plugin
Use when the automation should fire while Obsidian is already open.

Good fits:
- every N seconds checks
- file created/modified/deleted watchers
- startup or quit hooks
- routing command output into the current note, notification, clipboard, or status bar

Remember: Shell Commands uses timers and events, **not true cron syntax**.

### Pattern C: obsidian-cron plugin
Use when the user wants cron expressions inside Obsidian and a callback with `app` access.

Example shape:

```javascript
const cron = app.plugins.plugins.cron.api;
cron.addCronJob('job-name', '0 7 * * *', { enableMobile: false }, async (app) => {
  // vault operations here
});
```

Treat it as useful but less actively maintained than the official CLI route.

### Pattern D: Startup scripts
Use for one-time bootstrap logic at launch:
- CodeScript Toolkit startup script
- JS Engine startup scripts
- Templater startup template

Do **not** reach for startup scripts when the real requirement is a repeating schedule.

## Common mistakes to avoid

- using `cron` on macOS when `launchd` would be more reliable
- scheduling untested inline commands instead of a real script file
- forgetting that Obsidian CLI automation depends on the app and CLI being available
- using Shell Commands for a true calendar schedule requirement
- using startup templates for recurring jobs
- writing jobs that duplicate note content every run
- omitting logs, then having no idea why the automation failed
- editing plugin code for a scheduler job without also loading `obsidian-dev`
- doing build or release work without also loading `obsidian-ops`

## Pairing with related skills

- Use **`obsidian-cli`** for exact command syntax and live app-driven note operations.
- Use **`obsidian-dev`** if the automation involves plugin code, TypeScript, or app API implementation details.
- Use **`obsidian-ops`** if the task also includes builds, packaging, syncing references, or release preparation.

## Output expectations

When using this skill, produce a practical automation plan, not abstract advice.

Include the concrete artifacts the user needs:
- scheduler choice and why
- ready-to-use script/config snippets
- file paths to create
- test command
- log/debug path
- caveats such as plugin maintenance, sleep/wake behavior, or duplication risk
