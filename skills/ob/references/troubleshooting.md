# Troubleshooting

## Error: "Failed to validate password" (Shared Vaults)

**Symptom:** `ob sync-setup` exits with code 2: `Failed to validate password.`
**Observed even when:** `ob login` and `ob sync-list-remote` work fine.

**Causes & Fixes:**

1. **Shared vault quirk (issue #12):** Omit `--password` and let it prompt interactively:
   ```bash
   ob sync-setup --vault "SharedVaultName" --path /vaults/shared
   # Enter password interactively when prompted
   ```

2. **E2EE vault:** You need the **vault owner's** E2EE encryption password, not your account password.

3. **Freshly shared vault:** Wait a few minutes after sharing before setting up.

4. **Region mismatch:** Try using the vault ID (from `ob sync-list-remote`) instead of the name.

---

## `ob sync --continuous` Overwrites Files (Oscillation Bug)

**Symptom:** Sync version history shows files bouncing between correct content and 0 bytes / stale content in a repeating pattern.

**Cause:** Bidirectional mode can re-upload a file immediately after downloading it, before its local hash state is updated (issue #15, not yet fixed as of v0.0.9).

**Workaround (use on the server/headless side):**
```bash
ob sync-config --path /vault --mode pull-only
ob sync --continuous --path /vault
```

`pull-only` prevents the server from pushing local changes, eliminating the oscillation.

---

## After `ob sync-unlink`, Sync Targets Old Directory

**Symptom:** After running `ob sync-unlink` and then `ob sync-setup` in a new directory, `ob sync --continuous` still syncs to the old path.

**Cause:** A running `ob sync --continuous` process holds a reference to the old config (issue #13).

**Fix:**
1. Kill all running `ob` processes:
   ```bash
   pkill -f "ob sync"
   ```
2. Explicitly unlink the old directory:
   ```bash
   ob sync-unlink --path /old/vault/path
   ```
3. Setup the new directory:
   ```bash
   ob sync-setup --vault "My Vault" --path /new/vault/path
   ```
4. Verify with `ob sync-status --path /new/vault/path`.

---

## TimeoutNaNWarning on Every Sync

**Symptom:**
```
(node:12345) TimeoutNaNWarning: NaN is not a number.
Timeout duration was set to 1.
```

**Status:** Fixed in v0.0.9.

**Fix:**
```bash
npm update -g obsidian-headless
ob --version   # Should be ≥0.0.9
```

---

## "No sync configuration found"

**Symptom:** `ob sync-status` or `ob sync` prints "No sync configuration found for \<path>".

**Cause:** Vault not configured at this path, or you're in the wrong directory.

**Fix:**
```bash
# Check current directory
pwd
ob sync-status --path /explicit/vault/path

# Configure if not done
ob sync-setup --vault "My Vault" --path /path/to/vault
```

---

## Node.js Version Error

**Symptom:** `ob` fails with a syntax or runtime error at startup.

**Fix:**
```bash
node --version   # Must be ≥22.0.0
nvm install 22 && nvm use 22
# or: brew upgrade node
```

---

## Images Not Syncing

**Symptom:** Markdown files sync but images are missing.

**Cause:** `--file-types` config may have been accidentally cleared.

**Fix:**
```bash
ob sync-config --path /vault --file-types "image,audio,video,pdf,unsupported"
```

---

## Linux: No File Birthtime Preservation

**Status:** Expected behaviour. The `btime` native N-API addon is not included for Linux because Linux filesystems don't support `birthtime`. Sync itself works correctly; only file creation timestamps are not preserved on download.

---

## Config Syncing Deletes Remote Config Files

**Status:** Fixed in v0.0.4. Upgrade with `npm update -g obsidian-headless`.