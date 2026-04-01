# Embedding `pi-excalidraw` in Obsidian

This is the recommended first practical target for an Obsidian MCP/App-hosting plugin because it removes the current browser-tab dependency without forcing an immediate runtime rewrite.

## Phase 1: Wrapper view

Build a dedicated `ItemView` that points to the existing localhost runtime.

### Responsibilities
- open a custom leaf
- render an iframe or equivalent embedded browser surface
- display connection status
- expose reconnect/reload controls

### Keep in scope
- connect to an already running runtime, or allow desktop-only launch
- show the runtime URL and status
- add commands to open and focus the view

### Keep out of scope
- rewriting the Excalidraw frontend
- replacing existing REST/WebSocket contracts
- custom persistence formats beyond what the runtime already supports

## Phase 2: Native Obsidian actions

Add commands and small UI affordances for:
- fit canvas to content
- export PNG/SVG into the vault
- save current scene bundle
- attach a scene or export to the active note

## Phase 3: Note-linked workflows

Once the embedded view is stable, add note-aware features such as:
- store a scene path in frontmatter
- open the scene associated with the current note
- save image exports into a note's attachment folder
- offer elicitation when multiple target notes or folders are plausible

## Port and lifecycle strategy

Prefer a predictable runtime strategy:
- default port first
- configurable override in plugin settings
- clear reconnect action if the runtime is down
- desktop-only auto-launch if process spawning is used

Do not assume mobile can manage a local runtime the same way desktop does.

## Why iframe-first is best

It is the smallest viable integration because it:
- reuses the existing frontend unchanged
- preserves screenshot/export/viewport behavior
- reduces risk versus a deep rewrite
- establishes the host-view pattern needed for future MCP Apps

## Recommended commands

- `Open embedded Excalidraw canvas`
- `Reconnect embedded Excalidraw canvas`
- `Fit embedded Excalidraw canvas`
- `Export embedded Excalidraw image`
- `Attach Excalidraw scene to current note`

## UX states to implement

The view should explicitly handle:
- runtime unavailable
- runtime reachable but frontend not loaded
- connected and ready
- reconnecting
- export failed

Users should always have a visible next step rather than a blank pane.
