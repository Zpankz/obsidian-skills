"""
Native Obsidian URI CLI - Baseline obsidian:// protocol commands.

Based on: https://help.obsidian.md/Extending+Obsidian/Obsidian+URI
These are the core URI actions built into Obsidian itself.
"""

import argparse
import subprocess
import sys
import urllib.parse
from typing import Optional


def encode(value: str) -> str:
    """URL encode a value."""
    return urllib.parse.quote(str(value), safe='')


def build_native_uri(action: str, **params) -> str:
    """Build a native obsidian:// URI."""
    params = {k: v for k, v in params.items() if v is not None}
    
    if not params:
        return f"obsidian://{action}"
    
    encoded = '&'.join(f"{k}={encode(str(v))}" for k, v in params.items())
    return f"obsidian://{action}?{encoded}"


def execute_uri(uri: str, dry_run: bool = False) -> bool:
    """Execute URI via macOS open command."""
    if dry_run:
        print(uri)
        return True
    
    try:
        subprocess.run(['open', uri], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


class NativeObsidianURI:
    """Native Obsidian URI commands."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
    
    def _run(self, action: str, **params) -> bool:
        uri = build_native_uri(action, **params)
        return execute_uri(uri, dry_run=self.dry_run)
    
    # === Open Action ===
    # https://help.obsidian.md/Extending+Obsidian/Obsidian+URI#Open+notes
    
    def open_vault(self, vault: Optional[str] = None, vault_id: Optional[str] = None) -> bool:
        """Open an Obsidian vault."""
        if vault_id:
            return self._run('open', vault=vault_id)
        elif vault:
            return self._run('open', vault=vault)
        else:
            return self._run('open')
    
    def open_file(self, file: str, vault: Optional[str] = None, 
                  path: Optional[str] = None) -> bool:
        """Open a file in a vault.
        
        Args:
            file: File path relative to vault root
            vault: Vault name
            path: Absolute file system path (alternative to vault+file)
        """
        if path:
            return self._run('open', path=path)
        return self._run('open', vault=vault, file=file)
    
    # === New Action ===
    # https://help.obsidian.md/Extending+Obsidian/Obsidian+URI#Create+notes
    
    def new_note(self, file: Optional[str] = None, name: Optional[str] = None,
                 content: Optional[str] = None, vault: Optional[str] = None,
                 path: Optional[str] = None, overwrite: bool = False,
                 silent: bool = False, append: bool = False, 
                 prepend: bool = False, clipboard: bool = False) -> bool:
        """Create a new note or update an existing one.
        
        Args:
            file: File path relative to vault root (with .md extension)
            name: Note name (without .md, uses default location)
            content: Content for the note
            vault: Vault name
            path: Absolute file path
            overwrite: Overwrite existing file
            silent: Don't open the note after creation
            append: Append content to existing note
            prepend: Prepend content to existing note  
            clipboard: Use clipboard content instead of content param
        """
        params = {'vault': vault}
        
        if path:
            params['path'] = path
        elif file:
            params['file'] = file
        elif name:
            params['name'] = name
        
        if clipboard:
            params['clipboard'] = 'true'
        elif content:
            params['content'] = content
        
        if overwrite:
            params['overwrite'] = 'true'
        if silent:
            params['silent'] = 'true'
        if append:
            params['append'] = 'true'
        if prepend:
            params['prepend'] = 'true'
        
        return self._run('new', **params)
    
    # === Daily Action ===
    # https://help.obsidian.md/Extending+Obsidian/Obsidian+URI#Create+a+daily+note
    
    def daily_note(self, vault: Optional[str] = None) -> bool:
        """Open or create today's daily note."""
        return self._run('daily', vault=vault)
    
    # === Search Action ===
    # https://help.obsidian.md/Extending+Obsidian/Obsidian+URI#Search
    
    def search(self, query: str, vault: Optional[str] = None) -> bool:
        """Open search with a query."""
        return self._run('search', vault=vault, query=query)
    
    # === Hook Action ===
    # For integration with Hook app
    
    def hook_get_address(self, vault: Optional[str] = None, 
                         file: Optional[str] = None) -> bool:
        """Get the Obsidian URI for Hook integration."""
        return self._run('hook-get-address', vault=vault, file=file)
    
    # === Show Plugin ===
    # Opens the community plugin browser to a specific plugin
    
    def show_plugin(self, plugin_id: str) -> bool:
        """Open the plugin browser to a specific plugin."""
        return self._run('show-plugin', id=plugin_id)
    
    # === x-callback-url Support ===
    # https://help.obsidian.md/Extending+Obsidian/Obsidian+URI#Use+x-callback-url+parameters
    
    def open_with_callback(self, file: str, vault: Optional[str] = None,
                           x_success: Optional[str] = None,
                           x_error: Optional[str] = None) -> bool:
        """Open a file with x-callback-url parameters."""
        params = {'vault': vault, 'file': file}
        if x_success:
            params['x-success'] = x_success
        if x_error:
            params['x-error'] = x_error
        return self._run('open', **params)
    
    def new_with_callback(self, content: str, vault: Optional[str] = None,
                          file: Optional[str] = None, name: Optional[str] = None,
                          x_success: Optional[str] = None,
                          x_error: Optional[str] = None) -> bool:
        """Create note with x-callback-url parameters."""
        params = {'vault': vault, 'content': content}
        if file:
            params['file'] = file
        elif name:
            params['name'] = name
        if x_success:
            params['x-success'] = x_success
        if x_error:
            params['x-error'] = x_error
        return self._run('new', **params)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for native URI commands."""
    parser = argparse.ArgumentParser(
        prog='obdev native',
        description='Native Obsidian URI commands (built-in obsidian:// protocol)'
    )
    parser.add_argument('--dry-run', '-n', action='store_true', help='Print URI only')
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # Open vault
    p = sub.add_parser('open-vault', help='Open an Obsidian vault')
    p.add_argument('--vault', '-v', help='Vault name')
    p.add_argument('--id', help='Vault ID')
    
    # Open file
    p = sub.add_parser('open', help='Open a file')
    p.add_argument('file', nargs='?', help='File path relative to vault')
    p.add_argument('--vault', '-v', help='Vault name')
    p.add_argument('--path', '-p', help='Absolute file system path')
    
    # New note
    p = sub.add_parser('new', help='Create a new note')
    p.add_argument('--file', '-f', help='File path (with .md)')
    p.add_argument('--name', help='Note name (without .md)')
    p.add_argument('--content', '-c', help='Note content')
    p.add_argument('--vault', '-v', help='Vault name')
    p.add_argument('--path', '-p', help='Absolute file path')
    p.add_argument('--overwrite', action='store_true', help='Overwrite existing')
    p.add_argument('--silent', '-s', action='store_true', help="Don't open after creation")
    p.add_argument('--append', '-a', action='store_true', help='Append to existing')
    p.add_argument('--prepend', action='store_true', help='Prepend to existing')
    p.add_argument('--clipboard', action='store_true', help='Use clipboard content')
    
    # Daily
    p = sub.add_parser('daily', help='Open/create daily note')
    p.add_argument('--vault', '-v', help='Vault name')
    
    # Search
    p = sub.add_parser('search', help='Open search')
    p.add_argument('query', help='Search query')
    p.add_argument('--vault', '-v', help='Vault name')
    
    # Show plugin
    p = sub.add_parser('show-plugin', help='Show plugin in browser')
    p.add_argument('plugin_id', help='Plugin ID')
    
    # x-callback-url examples
    p = sub.add_parser('open-callback', help='Open with x-callback-url')
    p.add_argument('file', help='File path')
    p.add_argument('--vault', '-v', help='Vault name')
    p.add_argument('--x-success', help='Success callback URL')
    p.add_argument('--x-error', help='Error callback URL')
    
    return parser


def main(args: Optional[list] = None):
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    cli = NativeObsidianURI(dry_run=parsed.dry_run)
    
    if parsed.command == 'open-vault':
        cli.open_vault(vault=parsed.vault, vault_id=parsed.id)
    
    elif parsed.command == 'open':
        if parsed.path:
            cli.open_file(file=parsed.file or '', path=parsed.path)
        elif parsed.file:
            cli.open_file(file=parsed.file, vault=parsed.vault)
        else:
            cli.open_vault(vault=parsed.vault)
    
    elif parsed.command == 'new':
        cli.new_note(
            file=parsed.file, name=parsed.name, content=parsed.content,
            vault=parsed.vault, path=parsed.path, overwrite=parsed.overwrite,
            silent=parsed.silent, append=parsed.append, prepend=parsed.prepend,
            clipboard=parsed.clipboard
        )
    
    elif parsed.command == 'daily':
        cli.daily_note(vault=parsed.vault)
    
    elif parsed.command == 'search':
        cli.search(parsed.query, vault=parsed.vault)
    
    elif parsed.command == 'show-plugin':
        cli.show_plugin(parsed.plugin_id)
    
    elif parsed.command == 'open-callback':
        cli.open_with_callback(
            parsed.file, vault=parsed.vault,
            x_success=getattr(parsed, 'x_success', None),
            x_error=getattr(parsed, 'x_error', None)
        )
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
