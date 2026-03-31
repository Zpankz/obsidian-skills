---
name: obsidian-devtools
description: Inspect and automate Obsidian via Chrome DevTools Protocol. Use when needing to execute JavaScript in the Obsidian app context, read console logs, inspect the DOM, debug plugins, or bridge Claude with a running Obsidian instance.
---

# Obsidian DevTools MCP Server

A bridge between Claude and a local Obsidian instance via Chrome DevTools Protocol (CDP). Requires Obsidian installed at `/Applications/Obsidian.app` and Python 3.10+.

## Setup

```bash
cd skills/obsidian-devtools
pip install -e .
claude mcp add obsidian-devtools -- uv run python -m obsidian_devtools.server
```

## Tools

### `obsidian_launch_debug`
Connect to Obsidian with remote debugging enabled.
- `port` (int, default 9222): debugging port
- `restart` (bool, default false): force-restart Obsidian

### `obsidian_eval`
Execute JavaScript in the Obsidian app context (`app`, `window`).
- `expression` (str): JS code to run
- `await_promise` (bool, default true): wait for async results

### `obsidian_inspect_dom`
Return simplified DOM snapshot.
- `selector` (str, default "body"): CSS selector for root element

## Injected Helpers (`window.__mcp`)

- `__mcp.listPlugins()` — enabled plugin IDs
- `__mcp.getFileState(path)` — file metadata

## Common Patterns

```javascript
// Vault name
app.vault.getName()

// List enabled plugins
Object.keys(app.plugins.manifests)

// Active file path
app.workspace.getActiveFile()?.path

// All files
app.vault.getFiles().map(f => f.path)
```

## Security

Safe mode enabled by default (blocks `fs.write` and vault modifications). Binds to `127.0.0.1` only. See `SECURITY.md` for details.
