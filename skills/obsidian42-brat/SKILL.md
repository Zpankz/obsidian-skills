---
name: obsidian42-brat
description: Use BRAT (Beta Reviewer's Auto-update Tool) to install, manage, and update beta plugins and themes from GitHub. Trigger when the user mentions BRAT, beta plugins, testing plugins, installing from GitHub, or plugin updates.
---

# BRAT Skill

This skill enables Claude Code to work with the BRAT plugin — the standard tool for installing and managing beta Obsidian plugins and themes directly from GitHub repositories.

## Overview

BRAT (Beta Reviewer's Auto-update Tool) lets users install Obsidian plugins and themes that are not yet in the official community directory. It pulls releases directly from GitHub repos, tracks versions, and auto-updates on startup.

## Commands

| Command ID | Name | Description |
|-----------|------|-------------|
| `AddBetaPlugin` | Add a beta plugin for testing | Install a plugin from a GitHub repo URL |
| `checkForUpdatesAndUpdate` | Check for updates and UPDATE | Check all beta plugins and apply updates |
| `checkForUpdatesAndDontUpdate` | Only check for updates (no update) | Check for available updates without applying |
| `reinstallOnePlugin` | Choose a single plugin to reinstall | Reinstall a specific beta plugin |
| `updateOnePlugin` | Choose a single plugin version to update | Update one plugin to a specific version |
| `restartPlugin` | Restart a plugin | Reload a plugin without restarting Obsidian |
| `enablePlugin` | Enable a plugin | Toggle a plugin on |
| `disablePlugin` | Disable a plugin | Toggle a plugin off |
| `GrabBetaTheme` | Grab a beta theme for testing | Install a theme from GitHub |
| `updateBetaThemes` | Update beta themes | Update all installed beta themes |
| `openGitHubZRepository` | Open GitHub repository for a plugin | Open plugin's repo in browser |
| `openGitHubRepoTheme` | Open GitHub repository for a theme | Open theme's repo in browser |
| `opentPluginSettings` | Open Plugin Settings Tab | Jump to Obsidian's plugin settings |

## Typical Workflows

### Install a Beta Plugin

1. Get the GitHub repository URL (e.g., `https://github.com/author/obsidian-plugin-name`)
2. Run command: **Plugins: Add a beta plugin for testing**
3. Paste the repo URL — BRAT downloads the latest release
4. The plugin appears in Settings → Community Plugins

### Install a Specific Version

Use the "with or without version" variant of AddBetaPlugin to pin a specific release tag.

### Update All Beta Plugins

Run **Plugins: Check for updates to all beta plugins and UPDATE** — BRAT checks each tracked repo for new releases and updates in place.

### Restart Without Full Reload

Use **Plugins: Restart a plugin** to reload a single plugin's code without restarting Obsidian — useful during development.

## Data Files

| File | Purpose |
|------|---------|
| `data.json` | Tracked repos, versions, and settings |
| `brat-migrations.json` | Migration state between BRAT versions |

## Integration Notes

- BRAT tracks plugins by their GitHub repo URL, not by plugin ID
- Works with both public and private repositories (with token)
- Themes are installed alongside plugins using the same mechanism
- Auto-update runs on Obsidian startup by default
- Compatible with all platforms (desktop and mobile)

## References

- Plugin manifest: `obsidian42-brat` v2.0.4
- Author: [TfTHacker](https://github.com/TfTHacker/obsidian42-brat)
- Help: https://tfthacker.com/BRAT
