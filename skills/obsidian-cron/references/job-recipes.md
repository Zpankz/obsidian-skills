# Job recipes

These are starter patterns you can adapt.

## Morning routine script

```bash
#!/bin/bash
set -euo pipefail

obsidian vault="Research" daily
obsidian vault="Research" daily:append content="- [ ] Review inbox\n- [ ] Check calendar"
obsidian vault="Research" search query="status::active" format=json > "$HOME/tmp/active_notes.json"
```

Use with a 7:00 AM `launchd` or `cron` schedule.

## Vault export for another agent

```bash
#!/bin/bash
set -euo pipefail

OUT="$HOME/tmp/obsidian-active-items.json"
obsidian vault="Research" search query="status::active" format=json > "$OUT"
echo "Wrote $OUT"
```

Good for downstream agent processing.

## Weekly note command via app context

```bash
obsidian eval code="app.commands.executeCommandById('periodic-notes:open-weekly-note')"
```

Use when the job depends on an installed plugin command.

## Reload plugin after local development build

```bash
obsidian plugin:reload id=my-plugin
obsidian dev:errors
```

Useful in dev loops, but if the user is editing plugin code also load `obsidian-dev`.

## Shell Commands watcher idea

Use a Shell Commands file-modified trigger to run a lightweight command that:
1. checks a note path or recent file
2. extracts needed context
3. writes a short summary or shows a notification

This is better than a system cron job when the trigger is a live Obsidian event.

## Safety checklist before shipping automation

- the job can be run manually
- logs are configured
- target vault is explicit if needed
- repeated runs do not corrupt notes
- plugin dependencies are called out clearly
- the user knows how to disable the scheduler
