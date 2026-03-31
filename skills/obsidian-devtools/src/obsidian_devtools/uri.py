"""
Advanced URI CLI - Generate and execute Obsidian Advanced URI commands.

Based on: https://publish.obsidian.md/advanced-uri-doc
"""

import argparse
import subprocess
import sys
import urllib.parse
from typing import Optional


def encode(value: str) -> str:
    """URL encode a value for use in URI parameters."""
    return urllib.parse.quote(str(value), safe='')


def build_uri(vault: Optional[str] = None, **params) -> str:
    """Build an obsidian://adv-uri URL from parameters."""
    base = "obsidian://adv-uri"
    
    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}
    
    if vault:
        params['vault'] = vault
    
    if not params:
        return base
    
    # Encode and join parameters
    encoded_params = '&'.join(f"{k}={encode(v)}" for k, v in params.items())
    return f"{base}?{encoded_params}"


def execute_uri(uri: str, dry_run: bool = False) -> bool:
    """Execute an Obsidian URI via macOS open command."""
    if dry_run:
        print(uri)
        return True
    
    try:
        subprocess.run(['open', uri], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing URI: {e}", file=sys.stderr)
        return False


class AdvancedURICLI:
    """CLI handler for Advanced URI commands."""
    
    def __init__(self, vault: Optional[str] = None, dry_run: bool = False):
        self.vault = vault
        self.dry_run = dry_run
    
    def _run(self, **params) -> bool:
        uri = build_uri(vault=self.vault, **params)
        return execute_uri(uri, dry_run=self.dry_run)
    
    # === Navigation ===
    
    def open_file(self, filepath: str, line: Optional[int] = None, 
                  column: Optional[int] = None, heading: Optional[str] = None,
                  block: Optional[str] = None, viewmode: Optional[str] = None,
                  openmode: Optional[str] = None) -> bool:
        """Open a file, optionally at a specific location."""
        params = {'filepath': filepath}
        if line: params['line'] = str(line)
        if column: params['column'] = str(column)
        if heading: params['heading'] = heading
        if block: params['block'] = block
        if viewmode: params['viewmode'] = viewmode
        if openmode: params['openmode'] = openmode
        return self._run(**params)
    
    def open_daily(self, viewmode: Optional[str] = None, 
                   openmode: Optional[str] = None) -> bool:
        """Open today's daily note."""
        params = {'daily': 'true'}
        if viewmode: params['viewmode'] = viewmode
        if openmode: params['openmode'] = openmode
        return self._run(**params)
    
    def open_workspace(self, workspace: str) -> bool:
        """Open a saved workspace."""
        return self._run(workspace=workspace)
    
    def save_workspace(self) -> bool:
        """Save the current workspace."""
        return self._run(saveworkspace='true')
    
    def open_bookmark(self, bookmark: str, openmode: Optional[str] = None) -> bool:
        """Open a bookmarked item."""
        params = {'bookmark': bookmark}
        if openmode: params['openmode'] = openmode
        return self._run(**params)
    
    def open_block(self, block: str) -> bool:
        """Search vault for block ID and open it."""
        return self._run(block=block)
    
    def open_settings(self, settingid: str) -> bool:
        """Open a settings tab by ID."""
        return self._run(settingid=settingid)
    
    # === Writing ===
    
    def write(self, filepath: str, data: str, mode: Optional[str] = None,
              heading: Optional[str] = None, line: Optional[int] = None,
              separator: Optional[str] = None) -> bool:
        """Write data to a file (write/append/prepend/overwrite/new)."""
        params = {'filepath': filepath, 'data': data}
        if mode: params['mode'] = mode
        if heading: params['heading'] = heading
        if line: params['line'] = str(line)
        if separator: params['separator'] = separator
        return self._run(**params)
    
    def write_daily(self, data: str, mode: str = 'append',
                    separator: Optional[str] = None) -> bool:
        """Write data to today's daily note."""
        params = {'daily': 'true', 'data': data, 'mode': mode}
        if separator: params['separator'] = separator
        return self._run(**params)
    
    def write_clipboard(self, filepath: str, mode: str = 'append') -> bool:
        """Write clipboard content to a file."""
        return self._run(filepath=filepath, clipboard='true', mode=mode)
    
    def write_clipboard_daily(self, mode: str = 'append') -> bool:
        """Write clipboard content to daily note."""
        return self._run(daily='true', clipboard='true', mode=mode)
    
    # === Search ===
    
    def search(self, search: str, filepath: Optional[str] = None) -> bool:
        """Search for text in a file."""
        params = {'search': search}
        if filepath: params['filepath'] = filepath
        return self._run(**params)
    
    def replace(self, search: str, replace: str, 
                filepath: Optional[str] = None) -> bool:
        """Replace text in a file."""
        params = {'search': search, 'replace': replace}
        if filepath: params['filepath'] = filepath
        return self._run(**params)
    
    def replace_regex(self, searchregex: str, replace: str,
                      filepath: Optional[str] = None) -> bool:
        """Replace text using regex in a file."""
        params = {'searchregex': searchregex, 'replace': replace}
        if filepath: params['filepath'] = filepath
        return self._run(**params)
    
    # === Commands ===
    
    def command(self, commandid: str, filepath: Optional[str] = None,
                line: Optional[int] = None, mode: Optional[str] = None,
                confirm: bool = False) -> bool:
        """Execute an Obsidian command."""
        params = {'commandid': commandid}
        if filepath: params['filepath'] = filepath
        if line: params['line'] = str(line)
        if mode: params['mode'] = mode
        if confirm: params['confirm'] = 'true'
        return self._run(**params)
    
    def command_by_name(self, commandname: str, filepath: Optional[str] = None,
                        confirm: bool = False) -> bool:
        """Execute an Obsidian command by its display name."""
        params = {'commandname': commandname}
        if filepath: params['filepath'] = filepath
        if confirm: params['confirm'] = 'true'
        return self._run(**params)
    
    # === Frontmatter ===
    
    def get_frontmatter(self, filepath: str, key: str) -> bool:
        """Copy frontmatter value to clipboard."""
        # Key can be simple "mykey" or complex "[key1,key2,0]"
        return self._run(filepath=filepath, frontmatterkey=key)
    
    def set_frontmatter(self, filepath: str, key: str, data: str) -> bool:
        """Set a frontmatter value."""
        return self._run(filepath=filepath, frontmatterkey=key, data=data)
    
    # === Canvas ===
    
    def canvas_focus(self, nodes: str, filepath: Optional[str] = None) -> bool:
        """Focus on canvas nodes (comma-separated IDs)."""
        params = {'canvasnodes': nodes}
        if filepath: params['filepath'] = filepath
        return self._run(**params)
    
    def canvas_viewport(self, viewport: str, filepath: Optional[str] = None) -> bool:
        """Set canvas viewport (x,y,zoom or use - to skip, ++ to add, -- to subtract)."""
        params = {'canvasviewport': viewport}
        if filepath: params['filepath'] = filepath
        return self._run(**params)
    
    # === Miscellaneous ===
    
    def file_exists(self, filepath: str) -> bool:
        """Check if file exists (copies 1 or 0 to clipboard)."""
        return self._run(filepath=filepath, exists='true')
    
    def update_plugins(self) -> bool:
        """Update all community plugins."""
        return self._run(updateplugins='true')
    
    def enable_plugin(self, plugin: str) -> bool:
        """Enable a plugin."""
        return self._run(**{'enable-plugin': plugin})
    
    def disable_plugin(self, plugin: str) -> bool:
        """Disable a plugin."""
        return self._run(**{'disable-plugin': plugin})
    
    def eval_js(self, code: str) -> bool:
        """Execute JavaScript code (requires setting enabled)."""
        return self._run(eval=code)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the URI CLI."""
    parser = argparse.ArgumentParser(
        prog='obdev uri',
        description='Generate and execute Obsidian Advanced URI commands'
    )
    parser.add_argument('--vault', '-v', help='Target vault name')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Print URI instead of executing')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # === Navigation commands ===
    
    # open
    p = subparsers.add_parser('open', help='Open a file')
    p.add_argument('filepath', help='File path')
    p.add_argument('--line', '-l', type=int, help='Line number')
    p.add_argument('--column', '-c', type=int, help='Column number')
    p.add_argument('--heading', '-H', help='Heading to navigate to')
    p.add_argument('--block', '-b', help='Block ID to navigate to')
    p.add_argument('--viewmode', choices=['source', 'preview', 'live'],
                   help='View mode')
    p.add_argument('--openmode', choices=['tab', 'split', 'window', 'true', 'false'],
                   help='How to open (tab/split/window)')
    
    # daily
    p = subparsers.add_parser('daily', help='Open daily note')
    p.add_argument('--viewmode', choices=['source', 'preview', 'live'])
    p.add_argument('--openmode', choices=['tab', 'split', 'window'])
    
    # workspace
    p = subparsers.add_parser('workspace', help='Open or save workspace')
    p.add_argument('name', nargs='?', help='Workspace name to open')
    p.add_argument('--save', action='store_true', help='Save current workspace')
    
    # bookmark
    p = subparsers.add_parser('bookmark', help='Open a bookmark')
    p.add_argument('name', help='Bookmark title')
    p.add_argument('--openmode', choices=['tab', 'split', 'window'])
    
    # block
    p = subparsers.add_parser('block', help='Find and open block by ID')
    p.add_argument('block_id', help='Block ID')
    
    # settings
    p = subparsers.add_parser('settings', help='Open settings tab')
    p.add_argument('tab', help='Settings tab ID')
    
    # === Writing commands ===
    
    # write
    p = subparsers.add_parser('write', help='Write to a file')
    p.add_argument('filepath', help='File path')
    p.add_argument('data', help='Data to write')
    p.add_argument('--mode', '-m', choices=['append', 'prepend', 'overwrite', 'new'],
                   help='Write mode')
    p.add_argument('--heading', '-H', help='Target heading')
    p.add_argument('--line', '-l', type=int, help='Target line')
    p.add_argument('--separator', '-s', help='Separator for append/prepend')
    
    # append (convenience)
    p = subparsers.add_parser('append', help='Append to a file')
    p.add_argument('filepath', help='File path')
    p.add_argument('data', help='Data to append')
    p.add_argument('--heading', '-H', help='Target heading')
    p.add_argument('--separator', '-s', help='Separator')
    
    # prepend (convenience)
    p = subparsers.add_parser('prepend', help='Prepend to a file')
    p.add_argument('filepath', help='File path')
    p.add_argument('data', help='Data to prepend')
    p.add_argument('--heading', '-H', help='Target heading')
    p.add_argument('--separator', '-s', help='Separator')
    
    # write-daily
    p = subparsers.add_parser('write-daily', help='Write to daily note')
    p.add_argument('data', help='Data to write')
    p.add_argument('--mode', '-m', choices=['append', 'prepend', 'overwrite'],
                   default='append')
    p.add_argument('--separator', '-s', help='Separator')
    
    # clipboard
    p = subparsers.add_parser('clipboard', help='Write clipboard to file')
    p.add_argument('filepath', nargs='?', help='File path (omit for daily)')
    p.add_argument('--daily', '-d', action='store_true', help='Write to daily note')
    p.add_argument('--mode', '-m', choices=['append', 'prepend', 'overwrite'],
                   default='append')
    
    # === Search commands ===
    
    # search
    p = subparsers.add_parser('search', help='Search in file')
    p.add_argument('query', help='Search query')
    p.add_argument('--filepath', '-f', help='File to search in')
    
    # replace
    p = subparsers.add_parser('replace', help='Search and replace')
    p.add_argument('search', help='Search text')
    p.add_argument('replacement', help='Replacement text')
    p.add_argument('--filepath', '-f', help='File to search in')
    p.add_argument('--regex', '-r', action='store_true', help='Use regex')
    
    # === Command execution ===
    
    # cmd
    p = subparsers.add_parser('cmd', help='Execute Obsidian command')
    p.add_argument('command_id', help='Command ID')
    p.add_argument('--filepath', '-f', help='File context')
    p.add_argument('--line', '-l', type=int, help='Line context')
    p.add_argument('--mode', '-m', choices=['append', 'prepend', 'overwrite'])
    p.add_argument('--confirm', action='store_true', help='Auto-confirm dialogs')
    p.add_argument('--by-name', action='store_true', help='Use command name instead of ID')
    
    # === Frontmatter ===
    
    # fm-get
    p = subparsers.add_parser('fm-get', help='Get frontmatter value (to clipboard)')
    p.add_argument('filepath', help='File path')
    p.add_argument('key', help='Frontmatter key (e.g., "title" or "[nested,key,0]")')
    
    # fm-set
    p = subparsers.add_parser('fm-set', help='Set frontmatter value')
    p.add_argument('filepath', help='File path')
    p.add_argument('key', help='Frontmatter key')
    p.add_argument('value', help='Value (JSON for complex types)')
    
    # === Canvas ===
    
    # canvas-focus
    p = subparsers.add_parser('canvas-focus', help='Focus canvas nodes')
    p.add_argument('nodes', help='Comma-separated node IDs')
    p.add_argument('--filepath', '-f', help='Canvas file')
    
    # canvas-viewport
    p = subparsers.add_parser('canvas-viewport', help='Set canvas viewport')
    p.add_argument('viewport', help='x,y,zoom (use - to skip, ++/-- to adjust)')
    p.add_argument('--filepath', '-f', help='Canvas file')
    
    # === Misc ===
    
    # exists
    p = subparsers.add_parser('exists', help='Check if file exists')
    p.add_argument('filepath', help='File path')
    
    # update-plugins
    subparsers.add_parser('update-plugins', help='Update all community plugins')
    
    # plugin
    p = subparsers.add_parser('plugin', help='Enable/disable plugin')
    p.add_argument('action', choices=['enable', 'disable'])
    p.add_argument('plugin_id', help='Plugin ID')
    
    # eval
    p = subparsers.add_parser('eval', help='Execute JavaScript')
    p.add_argument('code', help='JavaScript code')
    
    # raw (build custom URI)
    p = subparsers.add_parser('raw', help='Build custom URI with key=value pairs')
    p.add_argument('params', nargs='+', help='Parameters as key=value')
    
    return parser


def main(args: Optional[list] = None):
    """Main entry point for the URI CLI."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    cli = AdvancedURICLI(vault=parsed.vault, dry_run=parsed.dry_run)
    
    # Navigation
    if parsed.command == 'open':
        cli.open_file(parsed.filepath, line=parsed.line, column=parsed.column,
                      heading=parsed.heading, block=parsed.block,
                      viewmode=parsed.viewmode, openmode=parsed.openmode)
    
    elif parsed.command == 'daily':
        cli.open_daily(viewmode=parsed.viewmode, openmode=parsed.openmode)
    
    elif parsed.command == 'workspace':
        if parsed.save:
            cli.save_workspace()
        elif parsed.name:
            cli.open_workspace(parsed.name)
        else:
            print("Specify workspace name or --save", file=sys.stderr)
            return 1
    
    elif parsed.command == 'bookmark':
        cli.open_bookmark(parsed.name, openmode=parsed.openmode)
    
    elif parsed.command == 'block':
        cli.open_block(parsed.block_id)
    
    elif parsed.command == 'settings':
        cli.open_settings(parsed.tab)
    
    # Writing
    elif parsed.command == 'write':
        cli.write(parsed.filepath, parsed.data, mode=parsed.mode,
                  heading=parsed.heading, line=parsed.line,
                  separator=parsed.separator)
    
    elif parsed.command == 'append':
        cli.write(parsed.filepath, parsed.data, mode='append',
                  heading=parsed.heading, separator=parsed.separator)
    
    elif parsed.command == 'prepend':
        cli.write(parsed.filepath, parsed.data, mode='prepend',
                  heading=parsed.heading, separator=parsed.separator)
    
    elif parsed.command == 'write-daily':
        cli.write_daily(parsed.data, mode=parsed.mode, separator=parsed.separator)
    
    elif parsed.command == 'clipboard':
        if parsed.daily or not parsed.filepath:
            cli.write_clipboard_daily(mode=parsed.mode)
        else:
            cli.write_clipboard(parsed.filepath, mode=parsed.mode)
    
    # Search
    elif parsed.command == 'search':
        cli.search(parsed.query, filepath=parsed.filepath)
    
    elif parsed.command == 'replace':
        if parsed.regex:
            cli.replace_regex(parsed.search, parsed.replacement, 
                             filepath=parsed.filepath)
        else:
            cli.replace(parsed.search, parsed.replacement,
                       filepath=parsed.filepath)
    
    # Commands
    elif parsed.command == 'cmd':
        if parsed.by_name:
            cli.command_by_name(parsed.command_id, filepath=parsed.filepath,
                               confirm=parsed.confirm)
        else:
            cli.command(parsed.command_id, filepath=parsed.filepath,
                       line=parsed.line, mode=parsed.mode, confirm=parsed.confirm)
    
    # Frontmatter
    elif parsed.command == 'fm-get':
        cli.get_frontmatter(parsed.filepath, parsed.key)
    
    elif parsed.command == 'fm-set':
        cli.set_frontmatter(parsed.filepath, parsed.key, parsed.value)
    
    # Canvas
    elif parsed.command == 'canvas-focus':
        cli.canvas_focus(parsed.nodes, filepath=parsed.filepath)
    
    elif parsed.command == 'canvas-viewport':
        cli.canvas_viewport(parsed.viewport, filepath=parsed.filepath)
    
    # Misc
    elif parsed.command == 'exists':
        cli.file_exists(parsed.filepath)
    
    elif parsed.command == 'update-plugins':
        cli.update_plugins()
    
    elif parsed.command == 'plugin':
        if parsed.action == 'enable':
            cli.enable_plugin(parsed.plugin_id)
        else:
            cli.disable_plugin(parsed.plugin_id)
    
    elif parsed.command == 'eval':
        cli.eval_js(parsed.code)
    
    elif parsed.command == 'raw':
        # Parse key=value pairs
        params = {}
        for p in parsed.params:
            if '=' in p:
                k, v = p.split('=', 1)
                params[k] = v
            else:
                print(f"Invalid parameter format: {p}", file=sys.stderr)
                return 1
        uri = build_uri(vault=parsed.vault, **params)
        execute_uri(uri, dry_run=parsed.dry_run)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
