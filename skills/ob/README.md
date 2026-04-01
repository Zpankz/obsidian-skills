# `obsidian-headless` Agent Skill

An [Agent Skill](https://agentskills.io) for the [`ob` CLI](https://github.com/obsidianmd/obsidian-headless) — the official headless client for **Obsidian Sync** and **Obsidian Publish**.

Teaches Claude to be an expert `ob` operator: setup, continuous sync, publish automation, CI/CD pipelines, systemd services, Docker deployments, and troubleshooting.

## Install in Claude Code

```bash
/skill install https://github.com/ZpankzY/obsidian-headless-skill
```

Or via plugin marketplace if registered:
```bash
/plugin marketplace add ZpankzY/obsidian-headless-skill
/plugin install obsidian-headless@obsidian-headless-skill
```

## Skill Contents

| File | Purpose |
|---|---|
| `SKILL.md` | Main instructions, decision tree, command cheatsheet, known issues |
| `references/commands.md` | Full option tables for all `ob` subcommands |
| `references/sync-workflows.md` | cron, CI/CD, pull-only, multi-vault, systemd patterns |
| `references/publish-workflows.md` | Publish setup, dry-run, frontmatter control, CI pipelines |
| `references/troubleshooting.md` | Known bugs (#12, #13, #15) + workarounds |
| `references/automation-patterns.md` | Docker, systemd, NAS, backup scripts |
| `scripts/check_ob_installed.py` | Preflight: verify Node.js, ob, and auth |
| `scripts/validate_vault_config.py` | Check vault sync/publish configuration |
| `scripts/generate_systemd_service.py` | Generate systemd unit for continuous sync |
| `evals/evals.json` | 6 eval test cases for skill quality testing |

## Example Triggers

- *"Help me set up continuous sync on my Linux server"*
- *"My ob sync keeps overwriting files with empty content"*
- *"Write a GitHub Actions workflow to sync my Obsidian vault every 6 hours"*
- *"Generate a systemd service for ob sync --continuous"*
- *"How do I publish only notes with publish: true in frontmatter?"*
- *"ob sync-setup is failing with 'Failed to validate password' on a shared vault"*

## Requires

- [Obsidian Sync](https://obsidian.md/sync) or [Obsidian Publish](https://obsidian.md/publish) subscription
- Node.js ≥22
- `npm install -g obsidian-headless` (v0.0.9+)

## Source

Tracks [obsidianmd/obsidian-headless](https://github.com/obsidianmd/obsidian-headless) — built against v0.0.9.