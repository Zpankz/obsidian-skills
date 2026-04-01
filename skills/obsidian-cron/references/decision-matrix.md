# Decision matrix

Choose the simplest automation surface that matches the user's intent.

| Requirement | Best choice | Why |
|---|---|---|
| Run every day/week/month at a fixed time | Obsidian CLI + `launchd`/`cron` | Most reliable scheduled automation |
| macOS laptop that sleeps/wakes often | Obsidian CLI + `launchd` | Better sleep/wake behavior than `cron` |
| Run every N seconds while Obsidian is open | Shell Commands plugin | Built for interval events |
| React to file created/modified/deleted events | Shell Commands plugin | Built-in file event hooks |
| Need true cron expression *inside* Obsidian | obsidian-cron plugin | Uses 5-field cron syntax with `app` access |
| Need direct `app` API on startup | CodeScript Toolkit / JS Engine / Templater startup | Best for one-time launch bootstrap |
| Need CLI-friendly exports for another agent | Obsidian CLI + external scheduler | Easy to log, test, and pipe to JSON |
| Need plugin reload / dev diagnostics as part of automation | Obsidian CLI + `obsidian-cli` skill, plus `obsidian-dev` | Keeps app-aware development workflow explicit |

## Rule of thumb

- If the automation can be expressed as a few `obsidian ...` commands, prefer the **CLI route**.
- If it needs to happen only while Obsidian is open and react to app events, prefer **Shell Commands**.
- If the user insists on cron expressions inside Obsidian or needs `app` in the scheduled callback, use **obsidian-cron**.
- If it should run once on launch, use a **startup script**, not a scheduler.

## Escalation path

Start simple and escalate only when needed:
1. Obsidian CLI command
2. Shell script wrapper
3. `launchd`/`cron`
4. in-app plugin scheduler
5. custom plugin code

That keeps the automation observable, testable, and easier to debug.