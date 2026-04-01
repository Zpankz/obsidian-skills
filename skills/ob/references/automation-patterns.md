# Automation Patterns

## Docker

```dockerfile
FROM node:22-slim

RUN npm install -g obsidian-headless

ENV OB_EMAIL=""
ENV OB_PASSWORD=""
ENV OB_VAULT_NAME=""
ENV VAULT_PATH="/vault"

VOLUME ["/vault"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/sh
# entrypoint.sh
set -e

ob login --email "$OB_EMAIL" --password "$OB_PASSWORD"

if ! ob sync-status --path "$VAULT_PATH" 2>/dev/null; then
  ob sync-setup --vault "$OB_VAULT_NAME" --path "$VAULT_PATH"
fi

# Use pull-only to avoid oscillation bug on headless devices
ob sync-config --path "$VAULT_PATH" --mode pull-only

exec ob sync --continuous --path "$VAULT_PATH"
```

```bash
# Build and run
docker build -t ob-sync .
docker run -d \
  -e OB_EMAIL="me@example.com" \
  -e OB_PASSWORD="secret" \
  -e OB_VAULT_NAME="My Vault" \
  -v /local/vault:/vault \
  --name ob-sync \
  ob-sync

# View logs
docker logs -f ob-sync
```

---

## systemd Service

Generate with `scripts/generate_systemd_service.py` or create manually:

```ini
# /etc/systemd/system/ob-sync-work.service
[Unit]
Description=Obsidian Headless Sync — Work Vault
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=3

[Service]
Type=simple
User=alice
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStartPre=/usr/local/bin/ob sync-status --path /home/alice/vaults/work
ExecStart=/usr/local/bin/ob sync --continuous --path /home/alice/vaults/work
Restart=on-failure
RestartSec=15
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ob-sync-work

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ob-sync-work.service
journalctl -fu ob-sync-work.service
```

---

## Backup Script (one-shot with logging and exit code)

```bash
#!/usr/bin/env bash
# /usr/local/bin/ob-backup.sh
set -euo pipefail

VAULT_PATH="${1:-/vaults/main}"
LOG_FILE="/var/log/ob-backup.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log() { echo "[$TIMESTAMP] $*" | tee -a "$LOG_FILE"; }

log "Starting sync for $VAULT_PATH"

if ob sync --path "$VAULT_PATH"; then
  log "Sync completed successfully"
else
  EXIT=$?
  log "ERROR: Sync failed (exit code $EXIT)"
  exit $EXIT
fi
```

---

## NAS (Synology / TrueNAS)

1. Install Node.js 22 via NAS package manager or nvm over SSH
2. `npm install -g obsidian-headless`
3. Run `ob login` and `ob sync-setup` once interactively via SSH
4. **Use `pull-only` mode** to avoid the bidirectional oscillation bug
5. Add a scheduled task in the NAS UI (Task Scheduler):
   ```bash
   /usr/local/bin/ob sync --path /volume1/vaults/main
   ```

---

## Multiple Accounts

`ob` stores one account at a time (global flat-file credentials). To operate multiple accounts:

```bash
# Switch to account A and sync personal vault
ob login --email "personal@example.com" --password "$PASS_A"
ob sync --path /vaults/personal

# Switch to account B and sync work vault
ob login --email "work@company.com" --password "$PASS_B"
ob sync --path /vaults/work
```

Note: Switching accounts overwrites the stored credentials. If you need true concurrent multi-account operation, run separate Docker containers or separate user sessions.

---

## Verifying ob Health

```bash
ob --version                 # Check installed version
ob login                     # Shows account info (no re-auth if already logged in)
ob sync-list-remote          # Confirms API connectivity and lists vaults
ob sync-status --path .      # Check if current directory is a configured vault
```