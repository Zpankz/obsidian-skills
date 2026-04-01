# Official MCP Apps and elicitation links

Use these sources before implementing concrete protocol details. They are the canonical place to verify current field names, capabilities, and lifecycle semantics.

## MCP Apps

- MCP Apps overview: `https://modelcontextprotocol.io/extensions/apps/overview`
- MCP Apps build guide: `https://modelcontextprotocol.io/extensions/apps/build`
- SEP-1865 (MCP Apps): `https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp`

## Elicitation

- Elicitation spec: `https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation`
- URL-mode elicitation SEP: `https://modelcontextprotocol.io/seps/1036-url-mode-elicitation-for-secure-out-of-band-intera`
- Schema reference: `https://modelcontextprotocol.io/specification/2025-11-25/schema`

## Base MCP specification

- Spec index: `https://modelcontextprotocol.io/specification/2025-11-25`
- Server resources: `https://modelcontextprotocol.io/specification/2025-11-25/server/resources`

## What to verify from the docs before coding

### For MCP Apps
- how `ui://` resources are declared
- how tools link to UI resources
- capability negotiation requirements
- host ↔ app communication model
- sandboxing expectations

### For elicitation
- form-mode request/response shape
- URL-mode request/response shape
- completion handling
- decline/cancel semantics
- what fields are considered host-controlled vs server-controlled

## Implementation note

This skill treats `MCP UI` and `mcp-ui` as older names for what the official docs now call **MCP Apps**. When writing code comments, README text, or user-facing docs, prefer `MCP Apps` and mention the older terms only for searchability or migration context.
