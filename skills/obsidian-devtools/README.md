# Obsidian DevTools MCP Server

A powerful bridge between Claude Code and your local Obsidian instance, enabling deep inspection, automation, and development capabilities via the Chrome DevTools Protocol (CDP).

## Overview

This MCP server connects to Obsidian's Electron backend, allowing Claude to:
- 🔍 **Inspect DOM**: View the live structure of the Obsidian UI.
- 💻 **Execute Code**: Run arbitrary JavaScript in the application context (`app`, `window`).
- 🛠️ **Read Console**: Debug plugins and scripts by reading internal logs.
- 🚀 **Manage Process**: Automatically launch Obsidian with remote debugging enabled.

## Installation

This server is designed to run locally on macOS.

### Prerequisites
- Python 3.10+
- Obsidian installed at `/Applications/Obsidian.app`

### Setup
1. Clone or copy this repository to `~/.claude/mcp/obsidian-devtools`.
2. Install dependencies:
   ```bash
   cd ~/.claude/mcp/obsidian-devtools
   pip install -e .
   ```
3. Register with Claude Code:
   ```bash
   claude mcp add obsidian-devtools -- uv run python -m obsidian_devtools.server
   ```

## Usage

Once registered, you can use the `obsidian-devtools` skill in Claude Code.

### Key Tools
- `obsidian_launch_debug`: Connects to Obsidian (restarts if necessary).
- `obsidian_eval`: Runs JS code. Example: `obsidian_eval("app.vault.getName()")`.
- `obsidian_inspect_dom`: Returns a summarized DOM snapshot.

## Security

This tool provides **Remote Code Execution (RCE)** capabilities by design.
- **Safe Mode**: Enabled by default. Blocks file system writes (`fs.write`) and vault modifications.
- **Local Only**: Binds strictly to `127.0.0.1` to prevent network exposure.

See `SECURITY.md` for details.
