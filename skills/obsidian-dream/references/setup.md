# Obsidian Dream - Setup Guide

## Prerequisites
- Claude Code v2.1.59+
- Auto-memory enabled (`autoMemoryEnabled: true` in settings)

## Installation

### 1. Make the trigger script executable
```bash
chmod +x ~/obsidian-skills/skills/obsidian-dream/should-dream.sh
```

### 2. Add the Stop hook to Claude Code settings

Add this to your `~/.claude/settings.json` under `hooks.Stop`:

```json
{
  "type": "command",
  "command": "bash $HOME/obsidian-skills/skills/obsidian-dream/should-dream.sh && touch $HOME/.claude/.dream-pending || true"
}
```

### 3. Add the session-start trigger to your global CLAUDE.md

Add this to `~/.claude/CLAUDE.md`:

```markdown
## Auto Dream
If the file `~/.claude/.dream-pending` exists at session start, run `/obsidian-dream` as a subagent in the background, then delete the flag file: `rm ~/.claude/.dream-pending`. This is the memory consolidation system - it runs automatically every 24 hours.
```

### 4. Test it

```bash
# Force trigger
touch ~/.claude/.dream-pending
```

Then tell Claude: "The .dream-pending flag exists. Run /obsidian-dream now."

## How the auto-trigger works

1. **Session ends** - Stop hook runs `should-dream.sh` (checks if 24hrs have passed)
2. **Flag created** - If conditions are met, `~/.claude/.dream-pending` is created
3. **Next session** - Claude sees the flag in CLAUDE.md instructions, runs dream in background
4. **Cleanup** - Dream writes `.last-dream` timestamp, deletes the flag
