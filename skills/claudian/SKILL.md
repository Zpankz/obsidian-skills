---
name: claudian
description: Use Claudian to embed Claude Code as an AI collaborator in your Obsidian vault. Trigger when the user mentions Claudian, Claude Code in Obsidian, vault AI assistant, agentic Claude, or embedded Claude sessions.
---

# Claudian Skill

This skill enables Claude Code to configure and interact with the Claudian plugin — which embeds Claude Code directly inside Obsidian as a full agentic AI collaborator.

## Overview

Claudian wraps the Claude Code CLI and runs it with the vault as its working directory. This gives Claude full agentic capabilities within the vault: file read/write, search, bash commands, and multi-step workflows. It provides a multi-tab chat interface, inline editing, and deep Obsidian integration.

**Desktop only** — requires Claude Code CLI installed locally.

## Commands

| Command ID | Name | Description |
|-----------|------|-------------|
| `open-view` | Open chat | Open the Claudian chat panel |
| `new-session` | New session | Start a fresh Claude Code session |
| `new-tab` | New tab | Open an additional chat tab |
| `close-current-tab` | Close tab | Close the active chat tab |

## Key Settings

### Core

| Setting | Description |
|---------|-------------|
| Claude CLI path | Path to the Claude Code CLI binary |
| Custom system prompt | Additional system instructions for Claude |
| User variables | Key-value pairs injected into prompts |
| Name | How Claudian addresses the user |

### Context Windows

| Setting | Description |
|---------|-------------|
| Opus 1M context window | Enable 1M token context for Opus model |
| Sonnet 1M context window | Enable 1M token context for Sonnet model |

### Safety

| Setting | Description |
|---------|-------------|
| Enable bash mode (!) | Allow bash command execution |
| Enable command blocklist | Block specific dangerous commands |
| Blocked commands | Platform-specific blocked command patterns |
| Allowed export paths | Restrict file export to specific paths |

### Integration

| Setting | Description |
|---------|-------------|
| Claude Code plugins | Load Claude Code plugin skills |
| Load user Claude settings | Import user's Claude Code configuration |
| Excluded tags | Tags to exclude from context |
| Media folder | Folder for media file storage |
| Inline editing | Enable inline code editing in vault |
| Open in main editor area | Open chat in main area vs sidebar |
| Tab bar position | Position of the tab bar |
| Max chat tabs | Maximum number of concurrent tabs |

### Title Generation

| Setting | Description |
|---------|-------------|
| Auto-generate chat titles | Automatically name chat sessions |
| Title generation model | Model used for title generation |

## Multi-Language Support

Claudian supports full localization including English, Russian, Chinese (Simplified/Traditional), Japanese, Korean, French, Spanish, Portuguese, German, and Urdu.

## Architecture

```
Obsidian ──► Claudian Plugin ──► Claude Code CLI
                 │                     │
                 ├── Tab Manager        ├── File read/write
                 ├── Chat View          ├── Bash execution
                 ├── Inline Editor      ├── Search
                 └── Settings           └── Multi-step workflows
```

The vault becomes Claude's working directory, so all file operations are relative to the vault root. Claude Code's full tool set is available: Read, Write, Edit, Glob, Grep, Bash, and Agent.

## Usage Patterns

### Vault-Aware AI Chat
1. Open Claudian via command or ribbon
2. Ask questions about vault content — Claude reads files directly
3. Request edits — Claude modifies notes in place

### Multi-Session Workflows
1. Open multiple tabs for different tasks
2. Each tab maintains its own Claude Code session context
3. Switch between sessions without losing state

### Agentic Vault Operations
Claude can autonomously:
- Search across vault files using grep/glob
- Create, edit, and organize notes
- Run shell commands for automation
- Execute multi-step refactoring workflows
- Generate content based on existing vault structure

## References

- Plugin manifest: `claudian` v1.3.72
- Author: [Yishen Tu](https://github.com/YishenTu)
