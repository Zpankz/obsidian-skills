# API Reference

## Tools

### `obsidian_launch_debug`
Initializes the connection to Obsidian.

**Signature:**
```python
obsidian_launch_debug(port: int = 9222, restart: bool = False) -> str
```
- `port`: The remote debugging port (default: 9222).
- `restart`: If `True`, force-kills any running Obsidian instance and restarts it with debugging flags. Use this if connection fails.

### `obsidian_eval`
Executes JavaScript in the main Obsidian window context.

**Signature:**
```python
obsidian_eval(expression: str, await_promise: bool = True) -> str
```
- `expression`: The JavaScript code to run.
- `await_promise`: If `True`, waits for async operations to complete.

**Context:**
- `app`: The global Obsidian App object.
- `window`: The browser window object.
- `__mcp`: Injected helper utilities.

### `obsidian_inspect_dom`
Returns a simplified snapshot of the DOM.

**Signature:**
```python
obsidian_inspect_dom(selector: str = "body") -> str
```
- `selector`: CSS selector to root the inspection (e.g., `.workspace-leaf.mod-active`).

## Helper API (`window.__mcp`)
These helpers are injected into the runtime to simplify common tasks.

- `__mcp.listPlugins()`: Returns array of enabled plugin IDs.
- `__mcp.getFileState(path)`: Returns metadata for a file.
