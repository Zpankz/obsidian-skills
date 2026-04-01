---
name: advanced-canvas
description: Use Advanced Canvas for presentations, flowcharts, custom shapes, edge styling, portals, collapsible groups, and enhanced canvas features. Trigger when the user mentions Advanced Canvas, canvas presentations, canvas slides, portals, canvas shapes, edge styling, or canvas export.
---

# Advanced Canvas Skill

This skill enables Claude Code to work with the Advanced Canvas plugin — a comprehensive enhancement suite for Obsidian's built-in canvas.

## Overview

Advanced Canvas extends Obsidian Canvas with presentations, custom node shapes, edge styling, portals (canvas-in-canvas), collapsible groups, focus mode, auto-resize, better export, and many more features. It stores custom metadata directly in `.canvas` JSON files.

## Commands

| Command ID | Name | Description |
|-----------|------|-------------|
| `start-presentation` | Start presentation | Begin slide presentation mode |
| `end-presentation` | End presentation | Exit presentation mode |
| `continue-presentation` | Continue presentation | Resume a paused presentation |
| `new-slide` | New slide | Create a new presentation slide |
| `create-new-slide` | Create new slide | Alternate slide creation command |
| `set-start-node` | Set start node | Mark a node as the first slide |
| `create-text-node` | Create text node | Add a text node to canvas |
| `create-file-node` | Create file node | Add a file-linked node |
| `create-group-around-selection` | Create group around selection | Wrap selected nodes in a group |
| `create-group` | Create group | Create an empty group |
| `toggle-collapse-group` | Toggle collapse group | Collapse/expand a group |
| `toggle-portal` | Toggle portal | Enable/disable portal view on a node |
| `toggle-focus-mode` | Toggle focus mode | Show only the focused node and neighbors |
| `toggle-readonly` | Toggle readonly | Toggle canvas read-only mode |
| `encapsulate-selection` | Encapsulate selection | Move selection into a sub-canvas |
| `swap-nodes` | Swap nodes | Swap positions of two selected nodes |
| `flip-selection-horizontally` | Flip horizontal | Mirror selection horizontally |
| `flip-selection-vertically` | Flip vertical | Mirror selection vertically |
| `pull-backlinks-to-canvas` | Pull backlinks | Add nodes for all backlinks |
| `pull-outgoing-links-to-canvas` | Pull outgoing links | Add nodes for all outgoing links |
| `export-all-as-image` | Export all as image | Export entire canvas as image |
| `export-selected-as-image` | Export selected as image | Export selection as image |
| `select-all-edges` | Select all edges | Select every edge on canvas |
| `select-connected-edges` | Select connected edges | Select edges touching selected nodes |
| `select-incoming-edges` | Select incoming edges | Select edges pointing to selected nodes |
| `select-outgoing-edges` | Select outgoing edges | Select edges leaving selected nodes |
| `flip-edge` | Flip edge | Reverse edge direction |
| `zoom-to-fit` | Zoom to fit | Zoom to show all content |
| `zoom-to-selection` | Zoom to selection | Zoom to selected nodes |
| `next-node` | Next node | Navigate to next node |
| `previous-node` | Previous node | Navigate to previous node |
| `copy-wikilink-to-node` | Copy wikilink to node | Copy a `[[wikilink]]` targeting the node |
| `auto-resize-height` | Auto resize height | Resize node to fit content |

## Node Shapes

Beyond the default rectangle, Advanced Canvas adds:

| Shape | Icon | Description |
|-------|------|-------------|
| Pill | `shape-pill` | Rounded capsule shape |
| Parallelogram | `shape-parallelogram` | Skewed rectangle |
| Document | `shape-document` | Document with wavy bottom |
| Database | `shape-database` | Cylinder shape |
| Predefined Process | `shape-predefined-process` | Double-bordered rectangle |

## Edge Styling

### Line Styles
- **Solid** — continuous line
- **Dashed** — dashed line
- **Dotted** — dotted line

### Arrow Types
- Triangle (filled)
- Triangle outline
- Thin triangle (open)
- Halved triangle
- Diamond (filled)
- Diamond outline
- Circle (filled)
- Circle outline

### Pathfinding Methods
- **Bezier** — smooth curved paths
- **Square** — right-angle paths (with optional rounding)
- **Pathfinder** — obstacle-aware routing (with optional diagonal movement)

## Presentation Mode

Turns canvas into a slide deck:

1. Create slides by adding group nodes (or use `New slide` command)
2. Set the first slide with `Set start node`
3. Number slides using node connections (edge order)
4. Start with `Start presentation` command
5. Navigate with arrow keys or Page Up/Down

### Presentation Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `defaultSlideDimensions` | (list) | Default size for new slides |
| `wrapInSlidePadding` | `20` | Padding around slide content |
| `resetViewportOnPresentationEnd` | `true` | Return to original view after |
| `useArrowKeysToChangeSlides` | `true` | Arrow key navigation |
| `usePgUpPgDownKeysToChangeSlides` | `true` | Page key navigation |
| `zoomToSlideWithoutPadding` | `true` | Fill screen with slide |
| `fullscreenPresentationEnabled` | `true` | Use browser fullscreen |
| `slideTransitionAnimationDuration` | `0.5` | Transition time in seconds |
| `slideTransitionAnimationIntensity` | `1.25` | Transition animation strength |

## Portals

Portals render the content of another `.canvas` file inline within a node. Toggle with the `Toggle portal` command. Edges into disabled portals can optionally still be shown.

## Collapsible Groups

Groups can be collapsed to hide their contents and expanded again. The `collapsedGroupPreviewOnDrag` setting shows a preview when dragging collapsed groups.

## Key Settings

### Node Behavior

| Setting | Default | Description |
|---------|---------|-------------|
| `nodeTypeOnDoubleClick` | `text` | What double-click creates |
| `alignNewNodesToGrid` | `true` | Snap new nodes to grid |
| `minNodeSize` | `60` | Minimum node dimension |
| `maxNodeWidth` | `-1` | Max width (-1 = unlimited) |
| `autoResizeNodeEnabledByDefault` | `true` | Auto-resize on by default |

### Edge Behavior

| Setting | Default | Description |
|---------|---------|-------------|
| `inheritEdgeColorFromNode` | `false` | Edge inherits source node color |
| `defaultEdgeLineDirection` | `unidirectional` | Default arrow direction |
| `edgeStyleUpdateWhileDragging` | `false` | Live update edge style |
| `edgeStyleSquarePathRounded` | `true` | Round corners on square paths |
| `allowFloatingEdgeCreation` | `false` | Allow edges with no target |

### Features Toggle

| Setting | Default | Description |
|---------|---------|-------------|
| `nodeStylingFeatureEnabled` | `true` | Custom node styles |
| `edgesStylingFeatureEnabled` | `true` | Custom edge styles |
| `collapsibleGroupsFeatureEnabled` | `true` | Collapsible groups |
| `presentationFeatureEnabled` | `true` | Presentation mode |
| `portalsFeatureEnabled` | `true` | Portal nodes |
| `betterExportFeatureEnabled` | `true` | Enhanced image export |
| `autoResizeNodeFeatureEnabled` | `true` | Auto-resize nodes |
| `floatingEdgeFeatureEnabled` | `true` | Floating edges |
| `flipEdgeFeatureEnabled` | `true` | Edge flipping |
| `focusModeFeatureEnabled` | `false` | Focus mode (off by default) |

## Canvas JSON Extensions

Advanced Canvas stores custom properties in `.canvas` JSON nodes. Custom style attributes for nodes and edges are persisted as additional keys in the node/edge objects within the canvas file.

## References

- Plugin manifest: `advanced-canvas` v6.0.0
- Author: [Developer-Mike](https://github.com/Developer-Mike)
- Funding: https://ko-fi.com/X8X27IA08
