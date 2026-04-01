---
name: internetvin-terminal
description: Use internetVin Terminal for embedded terminal sessions in Obsidian with multi-tab support, bookmarks, and output capture. Trigger when the user mentions embedded terminal, terminal tabs, terminal bookmarks, or capturing terminal output.
---

# internetVin Terminal Skill

This skill enables Claude Code to work with the internetVin Terminal plugin — an embedded PTY terminal for Obsidian with multi-tab support.

## Overview

internetVin Terminal embeds a full terminal emulator inside Obsidian. It supports multiple tabs, terminal bookmarks for marking positions in output, capturing terminal output to vault notes, and fullscreen mode.

**Desktop only** — requires native PTY access.

## Commands

| Command ID | Name | Description |
|-----------|------|-------------|
| `open-terminal` | Open Terminal | Open a terminal in the sidebar |
| `open-terminal-tab` | Open Terminal in Tab | Open a terminal as an editor tab |
| `toggle-fullscreen` | Toggle Fullscreen Terminal | Expand terminal to fill the window |
| `capture-terminal-output` | Capture Terminal Output to Note | Save current terminal content to a vault note |
| `add-bookmark` | Add Terminal Bookmark | Mark the current position in terminal output |
| `next-bookmark` | Next Terminal Bookmark | Jump to next bookmarked position |
| `prev-bookmark` | Previous Terminal Bookmark | Jump to previous bookmarked position |
| `clear-bookmarks` | Clear Terminal Bookmarks | Remove all terminal bookmarks |
| `show-shortcuts` | Show Terminal Shortcuts | Display keyboard shortcut reference |

## Features

### Multi-Tab Support

Multiple terminal sessions can run simultaneously in separate tabs. Use `Open Terminal in Tab` to create new sessions alongside your notes.

### Terminal Bookmarks

Bookmarks let you mark points in long terminal output for quick navigation:
- **Add Bookmark** — marks the current scroll position
- **Next/Previous Bookmark** — jumps between marked positions
- **Clear Bookmarks** — removes all marks

### Output Capture

**Capture Terminal Output to Note** saves the visible terminal content into a new vault note — useful for documenting command output, build logs, or debugging sessions.

### Fullscreen Mode

Toggle fullscreen to expand the terminal to the full Obsidian window — helpful for long-running processes or detailed output review.

## Usage Patterns

### Development Workflow
1. Open terminal in a tab alongside source code
2. Run build/test commands
3. Bookmark error locations in output
4. Capture relevant output to notes for documentation

### Vault Automation
1. Open terminal
2. Run shell scripts that modify vault files
3. Capture results to a log note

## References

- Plugin manifest: `internetvin-terminal` v1.1.0
- Author: Vin Verma
