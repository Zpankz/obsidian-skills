# Sync Workflows

## One-Shot Sync

```bash
cd /path/to/vault
ob sync
# or with explicit path:
ob sync --path /path/to/vault
```

Exit codes: `0` = success, non-zero = error (check stderr).

---

## Continuous Sync (Daemon Mode)

```bash
ob sync --continuous --path /vaults/work
```

Watches for filesystem changes and syncs automatically. Runs until killed.

**Background process with PID tracking:**
```bash
ob sync --continuous --path /vaults/work > /var/log/ob-sync.log 2>&1 &
echo $! > /var/run/ob-sync.pid

# Stop it later:
kill $(cat /var/run/ob-sync.pid)
```

---

## Cron-Based Sync

```cron
# Sync every 30 minutes (single vault)
*/30 * * * * /usr/local/bin/ob sync --path /vaults/main >> /var/log/ob-sync.log 2>&1

# Sync multiple vaults hourly
0 * * * * /usr/local/bin/ob sync --path /vaults/personal >> /var/log/ob-personal.log 2>&1
0 * * * * /usr/local/bin/ob sync --path /vaults/work >> /var/log/ob-work.log 2>&1
```

Find `ob` path with `which ob`. Use full path in crontab to avoid PATH issues.

---

## Pull-Only Mode (Read-Only Replica)

Recommended for servers, NAS devices, and CI — downloads remote changes but never pushes local modifications. Also the workaround for the bidirectional oscillation bug (issue #15).

```bash
ob sync-config --path /vaults/backup --mode pull-only
ob sync --continuous --path /vaults/backup
```

---

## Mirror-Remote Mode

Strictest read-only mode — pulls remote changes AND reverts any local modifications. Ideal for CI environments needing a guaranteed-clean snapshot.

```bash
ob sync-config --path /vaults/mirror --mode mirror-remote
ob sync --path /vaults/mirror
```

---

## Multi-Vault Setup

```bash
# Setup each vault once
ob sync-setup --vault "Personal" --path /vaults/personal
ob sync-setup --vault "Work" --path /vaults/work --device-name "server-prod"

# Sync all in parallel
ob sync --path /vaults/personal &
ob sync --path /vaults/work &
wait
echo "All vaults synced"
```

---

## CI/CD Pipeline (GitHub Actions)

```yaml
name: Sync Obsidian Vault

on:
  schedule:
    - cron: '0 */6 * * *'   # Every 6 hours
  workflow_dispatch:         # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install ob
        run: npm install -g obsidian-headless

      - name: Login
        run: ob login --email "${{ secrets.OB_EMAIL }}" --password "${{ secrets.OB_PASSWORD }}"

      - name: Checkout vault
        uses: actions/checkout@v4
        with:
          path: vault
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup vault (idempotent)
        run: |
          if ! ob sync-status --path vault 2>/dev/null; then
            ob sync-setup --vault "${{ secrets.OB_VAULT_NAME }}" --path vault
          fi

      - name: Sync (pull-only — safe for CI)
        run: ob sync --path vault
        env:
          OB_SYNC_MODE: pull-only

      - name: Commit synced files
        run: |
          cd vault
          git config user.name "ob-sync-bot"
          git config user.email "bot@example.com"
          git add -A
          git diff --staged --quiet || git commit -m "chore: sync vault $(date -u +%Y-%m-%dT%H:%M:%SZ)"
          git push
```

---

## NAS / Home Server (systemd)

Use `scripts/generate_systemd_service.py` or create manually. See `references/automation-patterns.md` for the full unit file template.

Quick install:
```bash
python scripts/generate_systemd_service.py \
  --vault-path /vaults/main \
  --user your-username \
  --output /etc/systemd/system/ob-sync-main.service

sudo systemctl daemon-reload
sudo systemctl enable --now ob-sync-main.service
journalctl -fu ob-sync-main.service
```

---

## E2EE Vault Automation

```bash
# Initial setup (run once — password stored in vault config after this)
ob sync-setup \
  --vault "SecureVault" \
  --path /vaults/secure \
  --password "$VAULT_PASS" \
  --device-name "server-prod"

# Subsequent syncs — no password needed
ob sync --path /vaults/secure
```

Protect the vault config directory (`/vaults/secure/.obsidian-sync/`) — it contains stored credentials.

---

## Exclude Folders from Sync

```bash
# Exclude specific folders
ob sync-config --path /vaults/work --excluded-folders "Archive,Temp,scratch"

# Clear exclusions
ob sync-config --path /vaults/work --excluded-folders ""
```

---

## Sync Only Specific File Types

```bash
# Sync markdown only (no attachments)
ob sync-config --path /vaults/main --file-types ""

# Sync everything including unsupported types
ob sync-config --path /vaults/main --file-types "image,audio,video,pdf,unsupported"
```