---
name: obsidian-mcp-apps
description: Build Obsidian plugins that host MCP Apps, render interactive ui:// resources, and handle elicitation dialogs. Trigger on MCP Apps, MCP UI, mcp-ui, or embedded tool UIs in Obsidian.
---

# Obsidian MCP Apps Skill

Use this skill when designing or implementing an Obsidian plugin that acts as an MCP host for embedded app UIs and structured human input.

## Terminology

- **Official term:** `MCP Apps`
- **Older/community terms you may still see:** `MCP UI`, `mcp-ui`
- **Interaction primitive for user input:** `elicitation`

When users say `mcp-ui`, treat that as MCP Apps unless they clearly mean a project with that exact name.

## Use this skill for

- hosting MCP Apps inside Obsidian custom views or modals
- rendering tool-linked `ui://` resources in an Obsidian plugin
- mapping MCP elicitation to native Obsidian UX
- designing human approval flows for vault writes, renames, deletes, or external auth
- embedding localhost-backed apps such as Excalidraw into Obsidian
- planning the architecture of an Obsidian MCP host plugin

## Prefer another skill when

- the task is broad Obsidian plugin work without MCP-specific UI concerns → `obsidian-plugin-dev`
- the main issue is lifecycle cleanup or view ownership → `obsidian-plugin-memory-management`
- the issue is wording, command names, or settings copy → `obsidian-plugin-ui-ux`
- the issue is styling/theme compatibility → `obsidian-plugin-css-styling`
- the issue is accessibility → `obsidian-plugin-accessibility`
- the task is inspecting a running Obsidian app via MCP/CDP → `obsidian-devtools`

## Related skills

- `obsidian-plugin-dev`
- `obsidian-plugin-memory-management`
- `obsidian-plugin-ui-ux`
- `obsidian-plugin-css-styling`
- `obsidian-plugin-accessibility`
- `obsidian-dev`
- `obsidian-devtools`
- `excalidraw-diagram`
- `obsidian-canvas`

## Default implementation stance

Use this order of preference unless the repo already chose differently:

1. **Native Obsidian surface first** for prompts, confirmations, status, and commands
2. **Embedded app view second** for richer interactive UIs
3. **External browser fallback** only when URL-mode elicitation or an existing web app truly requires it

Do not start by building a giant custom web shell when a custom `ItemView` plus a few modals will do.

## Architecture checklist

Before writing code, decide which role the plugin plays:

### 1. MCP host plugin
The Obsidian plugin itself connects to one or more MCP servers, negotiates capabilities, renders app UIs, and resolves elicitation.

Use this when Obsidian is the main user-facing shell.

### 2. Embedded app wrapper
The plugin embeds a specific existing UI, often a localhost-backed web app, and exposes commands/settings around it.

Use this first for things like `pi-excalidraw`, where the runtime already exists and the pain point is the separate browser tab.

### 3. Hybrid
The plugin hosts one specific app first, but is structured so the same surfaces can later support more MCP Apps.

This is usually the best long-term path.

## Recommended internal components

Split responsibilities early:

- **Connection manager** — MCP client connections, capability discovery, reconnect logic
- **App surface manager** — custom views, modals, iframe/webview lifecycle, app session bookkeeping
- **Elicitation manager** — form-mode prompts, URL-mode waiting states, approval/decline handling
- **Vault action service** — safe note/file operations using Obsidian APIs
- **Permission service** — trust tiers, dangerous-operation gating, allowed folders/actions
- **Settings layer** — server registry, feature flags, default folders, explicit trust controls

Do not bury all of this in `main.ts`.

## Obsidian surface selection

Choose the UI surface based on the job:

| Surface | Best for | Avoid when |
|---|---|---|
| `ItemView` / side pane | Long-lived apps, canvases, dashboards, Excalidraw-like UIs | The interaction is only a short confirmation |
| Modal | Form elicitation, approval dialogs, short wizards | The UI needs to stay open beside notes |
| Notice | Lightweight success/failure/status messages | User input or multi-step interaction is needed |
| Settings tab | Persistent configuration and trust policy | The task is contextual to one note or one operation |

## Elicitation mapping

### Form-mode elicitation
Map to a native Obsidian modal with explicit validation.

Good fit for:
- note title
- folder choice
- tags or frontmatter values
- rename confirmation
- export destination
- selecting one note among many candidates

Prefer native controls where possible:
- text inputs
- dropdowns
- toggles
- file/note pickers
- folder pickers

Keep the model out of the final confirmation step for destructive actions.

### URL-mode elicitation
Use when the user must complete something out-of-band:
- OAuth login
- external payment/approval page
- secure secret entry hosted elsewhere

Recommended pattern:
1. open the external browser
2. show a waiting modal or pane in Obsidian
3. listen for completion/callback state
4. resume the MCP workflow only after explicit completion

Do not fake URL-mode elicitation with an in-chat text prompt when the flow is meant to leave the host.

## Vault safety policy

Treat vault mutations as trust-tiered operations.

### Tier 1 — Read only
- list notes
- inspect metadata
- read file contents

### Tier 2 — Safe writes
- create draft notes in approved folders
- write exports/attachments into approved destinations
- update plugin-owned metadata

### Tier 3 — Destructive or broad changes
- overwrite arbitrary note content
- rename files or folders
- delete/trash files
- bulk refactors

Tier 3 actions should normally require elicitation or a native confirmation surface.

## Excalidraw-specific best practice

For `pi-excalidraw`, prefer an **embedded wrapper** before any deep rewrite.

### Good first version
- create a custom `ItemView`
- point an iframe or embedded webview at the localhost Excalidraw runtime
- expose commands like open, reconnect, fit to content, export image
- keep persistence simple at first

### Why this is the right first move
- reuses the working local runtime
- removes the browser-tab dependency
- keeps screenshot/export/viewport workflows attached to the Obsidian workspace
- creates a reusable pattern for future MCP Apps

### Avoid as a first step
- rewriting the runtime into a full Obsidian-only implementation
- forking protocol semantics unless required
- mixing Excalidraw rendering logic directly into plugin lifecycle code

Read `references/excalidraw-embedding.md` when the concrete target is a localhost-backed visual app.

## Implementation workflow

1. **Clarify the host model**
   - single dedicated app or general MCP host?
   - desktop-only or mobile too?

2. **Pick surfaces**
   - which flows need a view, modal, notice, or settings section?

3. **Define permission boundaries**
   - what can be read automatically?
   - what requires elicitation?

4. **Design lifecycle ownership**
   - who creates/destroys views?
   - how are reconnects handled?
   - what happens on unload?

5. **Implement the smallest vertical slice**
   - connect to one MCP server or one localhost runtime
   - render one view
   - support one approval flow

6. **Add vault integration second**
   - export into the vault
   - attach app state to notes
   - keep paths normalized and user-visible

7. **Generalize only after the narrow case works**
   - app registry
   - multiple server support
   - reusable elicitation infrastructure

## UX rules

- Use sentence case for commands, labels, and notices
- Prefer native-feeling Obsidian commands over custom jargon
- Always surface connection state clearly
- Make reconnect and retry obvious
- Do not silently mutate notes when the user expects review

## Accessibility and lifecycle rules

- keyboard access must work for app launch, modals, and confirmations
- icon buttons need accessible labels
- focus must land somewhere sensible after opening/closing a modal or view
- register and clean up all events and intervals using Obsidian lifecycle helpers
- do not keep stale references to views in plugin state longer than necessary

## File organization recommendation

A good starting split is:

- `main.ts`
- `mcp/connection-manager.ts`
- `mcp/elicitation-manager.ts`
- `mcp/app-registry.ts`
- `views/mcp-app-view.ts`
- `views/excalidraw-runtime-view.ts`
- `modals/elicitation-modal.ts`
- `modals/approval-modal.ts`
- `services/vault-action-service.ts`
- `services/permission-service.ts`
- `settings/plugin-setting-tab.ts`

Adjust to the repo, but keep protocol, UI, and vault mutation logic separate.

## Reference files

Read these bundled references when needed:

- `references/official-links.md` — official MCP Apps and elicitation docs to consult before coding protocol details
- `references/architecture.md` — practical host-plugin architecture and trust model guidance
- `references/excalidraw-embedding.md` — phased plan for embedding `pi-excalidraw` into an Obsidian custom view
- `references/plugin-scaffold.md` — concrete TypeScript-oriented starter structure for an Obsidian plugin that embeds a localhost-backed app view

## Output expectations

When using this skill, produce:
- a recommended architecture
- a phased implementation plan
- explicit UX and safety decisions
- any missing protocol questions that must be resolved before coding

If the user wants code, start with the smallest host/view slice rather than a large all-at-once implementation.
