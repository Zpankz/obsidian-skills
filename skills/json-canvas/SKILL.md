---
name: json-canvas
description: "Create, edit, or validate JSON Canvas .canvas files with nodes, edges, groups, and layout-aware connections. Trigger on mind maps, flowcharts, boards, or canvas repair."
---

# JSON Canvas

Use this skill when the artifact is a **`.canvas` file** and the user wants a visual layout represented directly in JSON Canvas format.

## When to use this skill

Typical triggers:
- "make a `.canvas` file"
- "fix this Obsidian canvas JSON"
- "turn this outline into a canvas"
- "build a mind map / flowchart / board in JSON Canvas"
- "repair broken node links in a canvas"

If the user wants a diagram in Markdown or another visual format, use the more appropriate skill for that artifact instead.

## Canvas-building workflow

1. **Choose the layout first**
   - linear flow, hub-and-spoke mind map, Kanban-style board, grouped overview
2. **Create nodes next**
   - stable IDs, clear coordinates, widths/heights appropriate to content
3. **Add edges after nodes exist**
   - every edge must point to valid node IDs
4. **Use groups only when they improve readability**
   - they are visual containers, not data relationships
5. **Validate before finishing**
   - JSON parses
   - IDs are unique
   - every edge target exists
   - node spacing is readable

## File shape

A JSON Canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

Both arrays are optional in the spec, but in practice it is usually clearer to keep them present.

## Node types

### Shared node fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | unique identifier, usually a 16-character lowercase hex string |
| `type` | yes | `text`, `file`, `link`, or `group` |
| `x` | yes | top-left x coordinate |
| `y` | yes | top-left y coordinate |
| `width` | yes | node width in pixels |
| `height` | yes | node height in pixels |
| `color` | no | preset `"1"`-`"6"` or hex color |

### Text node

Use for notes written directly into the canvas.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 360,
  "height": 180,
  "text": "# Overview\n\n- point one\n- point two"
}
```

Use real newline escapes (`\n`) inside JSON strings.

### File node

Use for a note or attachment already stored in the vault.

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 440,
  "y": 0,
  "width": 360,
  "height": 260,
  "file": "Projects/Alpha.md"
}
```

Optional `subpath` can point at a heading or block.

### Link node

Use for external URLs.

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 880,
  "y": 0,
  "width": 320,
  "height": 160,
  "url": "https://obsidian.md"
}
```

### Group node

Use as a labeled visual region around related nodes.

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -40,
  "y": -40,
  "width": 1280,
  "height": 420,
  "label": "Project Overview",
  "color": "4"
}
```

Groups should usually be created after you know the node positions they need to contain.

## Edges

Edges connect nodes by ID.

| Field | Required | Notes |
|---|---|---|
| `id` | yes | unique identifier |
| `fromNode` | yes | source node ID |
| `toNode` | yes | target node ID |
| `fromSide` / `toSide` | no | `top`, `right`, `bottom`, `left` |
| `fromEnd` / `toEnd` | no | `none` or `arrow` |
| `color` | no | preset or hex |
| `label` | no | text label on connection |

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "toNode": "a1b2c3d4e5f67890",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "next"
}
```

## Layout recipes

### Linear process / flowchart
- place nodes left-to-right or top-to-bottom
- keep a consistent gap of roughly 80-160px
- prefer directional arrows

### Mind map
- put the central idea in the middle
- place branches around it with generous spacing
- use short labels and fewer edge labels

### Board / grouped overview
- create columns or lanes first
- place cards inside each lane
- wrap lanes or themes in group nodes when helpful

## Spacing guidelines

- align to a rough grid (10px or 20px increments)
- leave 50-100px between neighboring nodes
- leave 20-50px of padding inside groups
- make text nodes large enough that the content is readable without clipping

Suggested node sizes:

| Node style | Width | Height |
|---|---:|---:|
| small text card | 220-300 | 100-160 |
| medium content card | 320-420 | 160-260 |
| large overview node | 420-600 | 260-420 |
| file preview | 300-500 | 220-400 |

## Validation checklist

Before finishing a `.canvas` file, verify:
1. the JSON parses cleanly
2. all node and edge IDs are unique
3. every `fromNode` and `toNode` points to an existing node
4. node `type` values are valid
5. required type-specific fields are present (`text`, `file`, `url`)
6. side values are only `top`, `right`, `bottom`, or `left`
7. arrow-end values are only `none` or `arrow`
8. layout is readable and not heavily overlapping

## Common mistakes to avoid

- duplicate IDs
- edges pointing to deleted or misspelled node IDs
- using literal line breaks instead of escaped `\n` in JSON strings
- packing nodes too tightly to be readable
- using groups as if they create relationships between nodes

## Example minimal canvas

```json
{
  "nodes": [
    {
      "id": "6f0ad84f44ce9c17",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 320,
      "height": 160,
      "text": "# Start\n\nDefine the problem"
    },
    {
      "id": "a1b2c3d4e5f67890",
      "type": "text",
      "x": 460,
      "y": 0,
      "width": 320,
      "height": 160,
      "text": "# Next\n\nChoose an approach"
    }
  ],
  "edges": [
    {
      "id": "0123456789abcdef",
      "fromNode": "6f0ad84f44ce9c17",
      "fromSide": "right",
      "toNode": "a1b2c3d4e5f67890",
      "toSide": "left",
      "toEnd": "arrow"
    }
  ]
}
```

## References

- `references/EXAMPLES.md`
- https://jsoncanvas.org/spec/1.0/
- https://github.com/obsidianmd/jsoncanvas
