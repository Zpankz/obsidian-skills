import argparse
import asyncio
import sys
import json
from .client import CDPClient
from .sdk import ObsidianClient
from .launcher import ObsidianLauncher
from .server import main as serve_main
from .uri import main as uri_main
from .actions import main as actions_main
from .rest import main as rest_main
from .datacore import main as datacore_main
from .native import main as native_main
from .snippets import main as snippets_main
from .bases import main as bases_main
from .importer import main as importer_main

async def async_main():
    parser = argparse.ArgumentParser(description="Obsidian DevTools CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: open
    open_parser = subparsers.add_parser("open", help="Open a note")
    open_parser.add_argument("path", help="Path to the note")
    open_parser.add_argument("--new-leaf", action="store_true", help="Open in new tab")

    # Command: list-plugins
    subparsers.add_parser("list-plugins", help="List enabled plugins")

    # Command: eval
    eval_parser = subparsers.add_parser("eval", help="Evaluate JavaScript")
    eval_parser.add_argument("expression", help="JS expression")

    # Command: command
    cmd_parser = subparsers.add_parser("command", help="Trigger Obsidian command")
    cmd_parser.add_argument("id", help="Command ID (e.g., app:toggle-left-sidebar)")
    cmd_parser.add_argument("--list", action="store_true", help="List available commands")

    # Command: create-canvas
    canvas_parser = subparsers.add_parser("create-canvas", help="Create a canvas file")
    canvas_parser.add_argument("path", help="Path (e.g. Map.canvas)")
    canvas_parser.add_argument("--nodes", help="JSON string of nodes", required=True)

    # Command: graph-zoom
    zoom_parser = subparsers.add_parser("graph-zoom", help="Zoom the graph view")
    zoom_parser.add_argument("level", type=float, help="Zoom level (1.0 = 100%)")

    # Command: discover
    discover_parser = subparsers.add_parser("discover", help="Discover API methods")
    discover_parser.add_argument("path", help="Object path (e.g. app.workspace)")

    # Command: frontmatter
    fm_parser = subparsers.add_parser("frontmatter", help="Get or update frontmatter")
    fm_parser.add_argument("path", help="Path to note")
    fm_parser.add_argument("--key", help="Key to update")
    fm_parser.add_argument("--value", help="Value to set")

    # Command: serve (MCP server)
    subparsers.add_parser("serve", help="Run as MCP server")

    # Command: uri (Advanced URI)
    subparsers.add_parser("uri", help="Advanced URI commands (use 'obdev uri --help' for details)", add_help=False)

    # Command: actions (Actions URI plugin)
    subparsers.add_parser("actions", help="Actions URI plugin commands", add_help=False)

    # Command: rest (Local REST API)
    subparsers.add_parser("rest", help="Local REST API commands", add_help=False)

    # Command: datacore (Datacore queries)
    subparsers.add_parser("datacore", help="Datacore query commands", add_help=False)

    # Command: native (Native Obsidian URI)
    subparsers.add_parser("native", help="Native Obsidian URI commands (open, new, daily, search)", add_help=False)

    # Command: snippets (CSS snippets management)
    subparsers.add_parser("snippets", help="CSS snippets management", add_help=False)

    # Command: bases (Bases syntax generator)
    subparsers.add_parser("bases", help="Bases syntax generator and reference", add_help=False)

    # Command: importer (Importer plugin)
    subparsers.add_parser("importer", help="Importer plugin integration", add_help=False)

    # Check for passthrough commands early
    if len(sys.argv) > 1 and sys.argv[1] == 'uri':
        return uri_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'actions':
        return actions_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'rest':
        return rest_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'datacore':
        return datacore_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'native':
        return native_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'snippets':
        return snippets_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'bases':
        return bases_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'importer':
        return importer_main(sys.argv[2:])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Handle serve command separately (doesn't need CDP connection)
    if args.command == "serve":
        serve_main()
        return


    # Initialize connection
    client = CDPClient(port=9222)
    try:
        await client.connect()
        connected = True
    except Exception:
        connected = False

    if not connected:
        # Try launching
        launcher = ObsidianLauncher()
        print("Launching Obsidian with debug flags...")
        await launcher.ensure_running(port=9222)

        # Retry connection
        try:
            await client.connect()
            connected = True
        except Exception:
            connected = False

        if not connected:
            print("Error: Could not connect to Obsidian. Is it running with --remote-debugging-port=9222?")
            sys.exit(1)

    sdk = ObsidianClient(client)

    try:
        if args.command == "open":
            await sdk.open_note(args.path, args.new_leaf)
            print(f"Opened: {args.path}")

        elif args.command == "list-plugins":
            plugins = await sdk.list_plugins()
            for p in plugins:
                print(f"{p['id']:<25} {p['version']:<10} {p['name']}")

        elif args.command == "eval":
            result = await sdk.eval(args.expression)
            print(result)

        elif args.command == "command":
            if args.list:
                cmds = await sdk.get_commands()
                for c in cmds:
                    print(f"{c['id']:<40} {c['name']}")
            else:
                success = await sdk.trigger_command(args.id)
                if success:
                    print(f"Triggered: {args.id}")
                else:
                    print(f"Command not found: {args.id}")

        elif args.command == "create-canvas":
            nodes = json.loads(args.nodes)
            await sdk.create_canvas(args.path, nodes, [])
            print(f"Created canvas: {args.path}")

        elif args.command == "graph-zoom":
            success = await sdk.graph_zoom_to(args.level)
            if success:
                print(f"Zoomed graph to {args.level}")
            else:
                print("No active graph view found.")

        elif args.command == "discover":
            props = await sdk.discover_object(args.path)
            print(f"API Discovery for: {args.path}")
            keys = sorted(props.keys())
            for k in keys:
                print(f"  {k}: {props[k]}")

        elif args.command == "frontmatter":
            if args.key:
                try:
                    val = json.loads(args.value)
                except:
                    val = args.value
                await sdk.update_frontmatter(args.path, args.key, val)
                print(f"Updated {args.key} in {args.path}")
            else:
                fm = await sdk.get_frontmatter(args.path)
                print(json.dumps(fm, indent=2))

    except Exception as e:
        print(f"Error: {e}")

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
