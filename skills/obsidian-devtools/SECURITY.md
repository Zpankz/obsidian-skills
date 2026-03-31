# Security Policy

## Overview
The `obsidian-devtools` MCP server allows an LLM to execute code within your personal Obsidian vault. This is a powerful capability that carries inherent risks. We implement a **Defense in Depth** strategy to protect your data.

## Safe Mode
By default, the server runs in **Safe Mode**. This enforces the following restrictions:

1.  **Blocked Modules**: Direct access to Node.js built-ins is blocked via regex scanning of the input expression.
    -   `require('fs')`
    -   `require('child_process')`
    -   `electron.remote`
    -   `process.env`

2.  **Blocked Operations**: Specific high-risk Obsidian API calls are blocked.
    -   `app.vault.delete`
    -   `app.vault.trash`
    -   `app.vault.modify`
    -   `app.vault.create`

3.  **Scope Shadowing**: The evaluation context wraps your code in a closure that shadows dangerous globals (`process`, `require`, `module`) with `undefined`.

## Network Isolation
- The Obsidian debugging port is launched with `--remote-debugging-address=127.0.0.1`.
- This prevents other devices on your local network from connecting to the debugger.

## Process Management
- The launcher script manages the Obsidian process lifecycle.
- It ensures no "zombie" processes are left running with open debug ports if the server crashes.

## Disabling Safe Mode
**Warning**: Disabling Safe Mode gives the LLM full read/write access to your computer.
To disable, you must modify the `server.py` initialization:
```python
# src/obsidian_devtools/server.py
security = SecurityGuard(safe_mode=False)
```
We recommend keeping Safe Mode enabled and only whitelisting specific operations if absolutely necessary.
