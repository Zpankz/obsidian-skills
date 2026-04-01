# Obsidian MCP host architecture

This reference expands the core skill with a practical architecture for an Obsidian plugin that hosts MCP Apps and resolves elicitation.

## Recommended subsystems

## 1. Connection manager

Responsibilities:
- connect to MCP servers
- discover capabilities
- maintain reconnect/backoff state
- expose a normalized app/tool registry to the rest of the plugin

Keep transport and capability negotiation out of UI classes.

## 2. App registry

Responsibilities:
- map server-provided app resources to launchable Obsidian surfaces
- track metadata like title, server name, icon, and intended surface
- decide whether an app should open in a dedicated view or a modal

This layer should know *about* app resources, not about vault writes.

## 3. App surface manager

Responsibilities:
- create and restore leaves
- load iframes or embedded views
- manage app session IDs and per-view state
- handle refresh and teardown cleanly

A custom `ItemView` is the default for long-lived interactive apps.

## 4. Elicitation manager

Responsibilities:
- render form-mode elicitation with Obsidian modals
- launch URL-mode elicitation in the external browser
- hold waiting state while the user completes external flows
- return accept/decline/cancel results to the connection layer

Use this layer as the only bridge between protocol-level elicitation and Obsidian UI.

## 5. Vault action service

Responsibilities:
- read/write note content
- create assets in approved folders
- normalize paths
- centralize background file operations

This service should be the only place where the host mutates the vault in response to MCP-driven workflows.

## 6. Permission service

Responsibilities:
- classify operations by trust level
- decide when elicitation or native confirmation is mandatory
- provide human-readable reasons for blocked actions

This keeps safety logic explainable instead of scattered across handlers.

## Surface mapping guidance

### Use a custom view when
- the app is long-lived
- the user may work with notes alongside it
- reconnect state matters
- the app has its own internal navigation or canvas

Examples:
- Excalidraw runtime wrapper
- graph explorer
- search dashboard

### Use a modal when
- the workflow is short
- the user needs to answer a few questions
- the app is a focused wizard rather than a workspace

Examples:
- form elicitation
- export configuration
- rename approval

## Trust model

### Read-only
Safe by default:
- inspecting current note path
- listing files
- reading note metadata

### Safe write
Usually acceptable with explicit host policy:
- writing exports into plugin-owned or user-approved folders
- creating draft notes
- attaching generated assets

### Destructive or broad write
Require explicit user approval:
- rename/move/delete
- overwrite arbitrary note content
- bulk changes across multiple files

## Persistence guidance

Prefer simple persistence first:
- plugin settings for server config and trusted folders
- plugin data for transient app-session metadata
- vault-visible files only for user-relevant artifacts like exports or attached scenes

Avoid building a hidden mini-database unless the app truly needs it.

## Failure-mode handling

Design explicit UX for:
- server unavailable
- app resource unavailable
- iframe failed to load
- elicitation timed out or was declined
- vault write blocked by policy

Each case should have:
- visible status
- one obvious recovery action
- no silent partial state

## Suggested command set

Keep command names sentence-case and task-oriented:
- `Open MCP app browser`
- `Reconnect MCP app view`
- `Review pending tool approval`
- `Open embedded Excalidraw canvas`
- `Export current app output`

## Implementation order

1. One server
2. One app surface
3. One elicitation flow
4. One safe vault write path
5. Only then add registry/generalization
