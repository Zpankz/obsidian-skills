# `ob` Command Reference

Full option tables for every `ob` subcommand. Load this file when the user asks about specific flags, options, or exact command syntax.

## Contents
- [ob login](#ob-login) | [ob logout](#ob-logout)
- [ob sync-list-remote](#ob-sync-list-remote) | [ob sync-list-local](#ob-sync-list-local)
- [ob sync-create-remote](#ob-sync-create-remote) | [ob sync-setup](#ob-sync-setup)
- [ob sync](#ob-sync) | [ob sync-config](#ob-sync-config)
- [ob sync-status](#ob-sync-status) | [ob sync-unlink](#ob-sync-unlink)
- [ob publish-list-sites](#ob-publish-list-sites) | [ob publish-create-site](#ob-publish-create-site)
- [ob publish-setup](#ob-publish-setup) | [ob publish](#ob-publish)
- [ob publish-config](#ob-publish-config) | [ob publish-site-options](#ob-publish-site-options)
- [ob publish-unlink](#ob-publish-unlink)

---

## `ob login`

```
ob login [--email <email>] [--password <password>] [--mfa <code>]
```

All options are interactive when omitted. If already logged in, displays account info without re-authenticating. To switch accounts, pass new credentials explicitly.

---

## `ob logout`

Clears stored flat-file credentials. No options.

---

## `ob sync-list-remote`

Lists all remote vaults accessible to the logged-in account (owned + shared). No options.

Output format:
```
Vaults:
  <id>  "<name>"  (<region>)

Shared vaults:
  <id>  "<name>"  (<region>)
```

---

## `ob sync-list-local`

Lists vaults configured on this machine with their local paths. No options.

---

## `ob sync-create-remote`

```
ob sync-create-remote --name "Vault Name" [--encryption <standard|e2ee>] [--password <password>] [--region <region>]
```

| Option | Default | Description |
|---|---|---|
| `--name` | required | Vault name |
| `--encryption` | `standard` | `standard` (managed) or `e2ee` (end-to-end encrypted) |
| `--password` | prompted if e2ee | E2EE password |
| `--region` | auto | Server region |

---

## `ob sync-setup`

Links a local directory to a remote vault. Creates `.obsidian-sync/` in the vault directory.

```
ob sync-setup --vault <id-or-name> [--path <local-path>] [--password <password>] [--device-name <name>] [--config-dir <name>]
```

| Option | Default | Description |
|---|---|---|
| `--vault` | required | Remote vault ID or name |
| `--path` | current directory | Local vault directory |
| `--password` | prompted if e2ee | E2EE decryption password |
| `--device-name` | hostname | Displayed in Obsidian Sync version history |
| `--config-dir` | `.obsidian` | Config directory name inside the vault |

---

## `ob sync`

```
ob sync [--path <local-path>] [--continuous]
```

| Option | Default | Description |
|---|---|---|
| `--path` | current directory | Vault directory (must be configured via `sync-setup`) |
| `--continuous` | false | Daemon mode — watches for changes and syncs in a loop |

Exit code 0 = success. Non-zero = error.

---

## `ob sync-config`

View or modify sync settings for a vault. Run with no options to display current config.

```
ob sync-config [--path <local-path>] [options]
```

| Option | Values | Description |
|---|---|---|
| `--path` | path | Local vault path (default: cwd) |
| `--mode` | `bidirectional`, `pull-only`, `mirror-remote` | Sync direction |
| `--conflict-strategy` | `merge`, `conflict` | Conflict resolution |
| `--file-types` | `image,audio,video,pdf,unsupported` | Attachment types to sync (comma-separated; empty string to clear) |
| `--configs` | `app,appearance,appearance-data,hotkey,core-plugin,core-plugin-data,community-plugin,community-plugin-data` | Config categories to sync |
| `--excluded-folders` | folder names | Folders to exclude (comma-separated; empty string to clear) |
| `--device-name` | string | Device display name |
| `--config-dir` | dir name | Config directory name |

---

## `ob sync-status`

```
ob sync-status [--path <local-path>]
```

Prints vault configuration + current sync state. Exit code 2 = vault not configured at this path.

---

## `ob sync-unlink`

```
ob sync-unlink [--path <local-path>]
```

Disconnects vault from sync and removes stored credentials. Does **not** delete local files. After running, kill any running `ob sync --continuous` process and restart if needed.

---

## `ob publish-list-sites`

Lists all Obsidian Publish sites accessible to the account. No options.

---

## `ob publish-create-site`

```
ob publish-create-site --slug <slug>
```

| Option | Description |
|---|---|
| `--slug` | Site slug for the publish URL (required) |

---

## `ob publish-setup`

```
ob publish-setup --site <id-or-slug> [--path <local-path>]
```

| Option | Description |
|---|---|
| `--site` | Site ID or slug (required) |
| `--path` | Local vault path (default: cwd) |

---

## `ob publish`

Scans for changes by comparing local file hashes to the remote site. Uploads new/changed files, removes deleted ones. Already incremental — only changed files are transferred.

```
ob publish [--path <local-path>] [--dry-run] [--yes] [--all]
```

| Option | Description |
|---|---|
| `--path` | Local vault path (default: cwd) |
| `--dry-run` | Show changes without publishing |
| `--yes` | Skip confirmation prompt |
| `--all` | Include files without a `publish` frontmatter key |

**File selection priority:**
1. `publish: true/false` in frontmatter (highest — overrides everything)
2. Configured includes/excludes (`ob publish-config`)
3. `--all` flag

---

## `ob publish-config`

```
ob publish-config [--path <local-path>] [--includes <folders>] [--excludes <folders>]
```

Run with no options to display current config.

| Option | Description |
|---|---|
| `--includes` | Folders to include, comma-separated (empty string to clear) |
| `--excludes` | Folders to exclude, comma-separated (empty string to clear) |

---

## `ob publish-site-options`

View or update remote site appearance and navigation. Run with no options to display current settings.

```
ob publish-site-options [--path <local-path>] [options]
```

| Option | Description |
|---|---|
| `--site-name <name>` | Site display name |
| `--index-file <path>` | Home page file path |
| `--logo <path>` | Logo file (empty string to clear) |
| `--default-theme <light\|dark>` | Default theme |
| `--show-navigation <bool>` | Navigation sidebar |
| `--show-graph <bool>` | Graph view |
| `--show-outline <bool>` | Table of contents |
| `--show-search <bool>` | Search bar |
| `--show-backlinks <bool>` | Backlinks panel |
| `--show-hover-preview <bool>` | Hover preview |
| `--show-theme-toggle <bool>` | Theme toggle button |
| `--readable-line-length <bool>` | Readable line length |
| `--strict-line-breaks <bool>` | Strict line breaks |
| `--hide-title <bool>` | Hide inline title |
| `--sliding-window <bool>` | Sliding window mode |
| `--nav-order <paths>` | Navigation order, comma-separated (empty string to clear) |
| `--nav-hidden <items>` | Hidden nav items, comma-separated (empty string to clear) |

---

## `ob publish-unlink`

```
ob publish-unlink [--path <local-path>]
```

Disconnects vault from publish site.