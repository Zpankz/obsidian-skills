---
name: obsidian-headless
description: Use ob (obsidian-headless) for CLI vault sync, publish, and headless automation. Trigger on headless sync, ob commands, CI pipelines, or server-side vault operations.
---

# Obsidian Headless (`ob`) Skill

Expert assistant for `ob` — the official headless CLI for Obsidian Sync and Obsidian Publish.

**Prerequisites:** Node.js ≥22, an active [Obsidian Sync](https://obsidian.md/sync) or [Obsidian Publish](https://obsidian.md/publish) subscription, `obsidian-headless` installed globally.

```bash
npm install -g obsidian-headless
ob login
```

## Core Mental Model

`ob` operates on **configured vaults** — a local directory linked to a remote Obsidian Sync vault via `ob sync-setup`. Once configured, `ob sync` pulls/pushes changes; `ob sync --continuous` watches for changes and loops forever. Configuration is stored as flat files inside the vault's `.obsidian-sync/` directory (no keyring required — safe for headless servers).

**Key constraint:** `ob` requires an Obsidian Sync or Publish subscription. There is no offline or local-only mode.

## Workflow Decision Tree

```
User wants to...
├── First-time setup?
│   ├── 1. ob login
│   ├── 2. ob sync-list-remote      ← find vault ID/name
│   ├── 3. ob sync-setup --vault "Name" [--path <dir>]
│   └── 4. ob sync  (or --continuous)
│
├── Automate sync (server/cron/CI)?
│   └── → references/sync-workflows.md
│
├── Publish notes?
│   ├── 1. ob publish-setup --site <slug>
│   └── 2. ob publish [--dry-run] [--yes] [--all]
│   └── → references/publish-workflows.md
│
├── Troubleshoot an error?
│   └── → references/troubleshooting.md
│
└── Advanced scripting/Docker/systemd?
    └── → references/automation-patterns.md
```

## Essential Commands

| Command | Purpose |
|---|---|
| `ob login` | Authenticate (interactive; supports `--email`, `--password`, `--mfa`) |
| `ob logout` | Clear stored credentials |
| `ob sync-list-remote` | List all accessible remote vaults |
| `ob sync-setup --vault <id-or-name>` | Link a local directory to a remote vault |
| `ob sync` | One-shot sync (bidirectional by default) |
| `ob sync --continuous` | Continuous sync (daemon mode) |
| `ob sync-status` | Show current vault config + sync state |
| `ob sync-config --mode pull-only` | Change sync mode |
| `ob publish` | Publish vault to connected site |
| `ob publish --dry-run` | Preview what would be published |

## Sync Modes

| Mode | Behaviour | Use Case |
|---|---|---|
| `bidirectional` | Push local + pull remote | Default; two-way sync |
| `pull-only` | Pull only, ignore local changes | Read-only replica, CI artifact consumer |
| `mirror-remote` | Pull only + revert local changes | Strict remote-authoritative mirror |

Set via: `ob sync-config --mode <mode>`

## Authentication Model

Credentials are stored as flat files (no keyring required — safe for headless servers). Non-interactive login:

```bash
ob login --email "$OB_EMAIL" --password "$OB_PASSWORD"
# With 2FA:
ob login --email "$OB_EMAIL" --password "$OB_PASSWORD" --mfa "$TOTP_CODE"
```

For CI/CD, store credentials as repository secrets and re-run `ob login` at job start, or persist the vault config directory between runs.

## Publish: Frontmatter Control

Files are selected for publishing in priority order:
1. `publish: true` / `publish: false` in YAML frontmatter (overrides everything)
2. Included/excluded folders (set via `ob publish-config`)
3. `--all` flag (includes files with no publish frontmatter)

```bash
ob publish --dry-run    # Always preview first
ob publish --yes        # Only publish: true files
ob publish --all --yes  # Include untagged files
```

## Common Patterns

**One-shot sync in a cron job:**
```bash
0 * * * * cd /vaults/work && ob sync >> /var/log/ob-sync.log 2>&1
```

**Continuous sync as a background process:**
```bash
ob sync --continuous --path /vaults/work &
echo $! > /var/run/ob-sync.pid
```

**E2EE vault setup:**
```bash
ob sync-setup --vault "SecureVault" --path /vaults/secure --password "$VAULT_PASSWORD"
```

## Known Issues (v0.0.9)

- **Bidirectional oscillation** (`ob sync --continuous`): files can be re-uploaded immediately after download, causing version history churn and data loss risk. Workaround: `ob sync-config --mode pull-only`. ([#15](https://github.com/obsidianmd/obsidian-headless/issues/15))
- **Shared vault password error**: `ob sync-setup` for shared vaults may fail with "Failed to validate password" even with correct credentials. Workaround: omit `--password` and let it prompt. ([#12](https://github.com/obsidianmd/obsidian-headless/issues/12))
- **After `sync-unlink`**: May keep syncing old directory. Fix: kill running processes, re-run `sync-setup`. ([#13](https://github.com/obsidianmd/obsidian-headless/issues/13))
- **Linux**: `btime` native module (birthtime) not supported. Sync works normally; file creation timestamps are not preserved.

## Reference Files

Load when needed:
- `references/commands.md` — Full option tables for every `ob` subcommand
- `references/sync-workflows.md` — CI/CD, cron, multi-vault, pull-only, systemd patterns
- `references/publish-workflows.md` — Publish automation, site config, frontmatter strategies
- `references/troubleshooting.md` — Known bugs, error messages, workarounds
- `references/automation-patterns.md` — Docker, systemd, NAS, backup scripts

## Scripts

- `scripts/check_ob_installed.py` — Verify `ob` is installed, Node.js version, and auth state
- `scripts/validate_vault_config.py` — Check if a vault dir is configured for sync/publish
- `scripts/generate_systemd_service.py` — Generate a systemd unit for `ob sync --continuous`