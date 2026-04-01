# System schedulers

Use this reference when the user wants scheduled automation outside the Obsidian UI.

## Preferred pattern

1. Put the real logic in a script file.
2. Test the script manually.
3. Add logging.
4. Schedule the script.
5. Re-run manually after any change.

## Script skeleton

```bash
#!/bin/bash
set -euo pipefail

LOG_DIR="$HOME/.local/state/obsidian-jobs"
mkdir -p "$LOG_DIR"

obsidian vault="Research" daily
obsidian vault="Research" daily:append content="- [ ] Review inbox"
```

Use a user-approved location such as:
- `~/scripts/`
- `<vault>/scripts/`
- project-specific automation folder

## macOS: launchd

Prefer `launchd` on macOS.

Minimal shape:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.obsidian.morning-routine</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/you/scripts/obsidian-morning.sh</string>
  </array>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>7</integer>
    <key>Minute</key><integer>0</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/tmp/obsidian-morning.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/obsidian-morning.err</string>
</dict>
</plist>
```

Typical lifecycle commands:

```bash
launchctl load ~/Library/LaunchAgents/com.obsidian.morning-routine.plist
launchctl unload ~/Library/LaunchAgents/com.obsidian.morning-routine.plist
launchctl kickstart -k gui/$(id -u)/com.obsidian.morning-routine
```

## Linux: cron

Use `crontab -e` for per-user schedules.

Examples:

```cron
0 7 * * * /home/you/scripts/obsidian-morning.sh >> /tmp/obsidian-cron.log 2>&1
0 */6 * * * /home/you/scripts/obsidian-health.sh >> /tmp/obsidian-health.log 2>&1
```

## Logging and debugging

Always give the user a place to inspect failures.

Good defaults:
- `/tmp/obsidian-<job>.log`
- `$HOME/.local/state/obsidian-jobs/<job>.log`
- a project-local `logs/` folder when appropriate

Debug checklist:
- run the script directly in a shell first
- run individual `obsidian ...` commands manually
- verify the target vault is explicit when needed
- check whether Obsidian is open and the CLI is enabled
- inspect stdout/stderr paths

## Idempotence and overlap

Scheduled jobs should tolerate retries and duplicates.

Use these patterns when needed:
- create guard files or lock files for long-running jobs
- search before appending repeated checklist items
- write exports to stable file paths and overwrite intentionally
- make note updates deterministic rather than “append forever”

## When not to use a system scheduler

Avoid `launchd`/`cron` when the job fundamentally depends on in-app events like:
- current selection
- active file changes
- file created/modified hooks inside the open app
- periodic UI updates while Obsidian is open

In those cases, read `in-app-automation.md`.