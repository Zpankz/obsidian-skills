"""
Actions URI CLI - Interface with the obsidian-actions-uri plugin.

Provides x-callback-url based automation for Obsidian.
Based on: https://github.com/czottmann/obsidian-actions-uri
"""

import argparse
import subprocess
import sys
import urllib.parse
import json
from typing import Optional


def encode(value: str) -> str:
    """URL encode a value."""
    return urllib.parse.quote(str(value), safe='')


def build_uri(route: str, vault: Optional[str] = None, **params) -> str:
    """Build an obsidian://actions-uri URL."""
    base = f"obsidian://actions-uri{route}"
    
    params = {k: v for k, v in params.items() if v is not None}
    if vault:
        params['vault'] = vault
    
    if not params:
        return base
    
    encoded = '&'.join(f"{k.replace('_', '-')}={encode(str(v))}" for k, v in params.items())
    return f"{base}?{encoded}"


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


class ActionsURI:
    """Actions URI client."""
    
    def __init__(self, vault: Optional[str] = None, dry_run: bool = False):
        self.vault = vault
        self.dry_run = dry_run
    
    def _run(self, route: str, **params) -> bool:
        uri = build_uri(route, vault=self.vault, **params)
        return execute_uri(uri, dry_run=self.dry_run)
    
    # === Note operations ===
    
    def note_get(self, file: Optional[str] = None, uid: Optional[str] = None,
                 periodic_note: Optional[str] = None, silent: bool = False) -> bool:
        """Get note content."""
        return self._run('/note/get', file=file, uid=uid, 
                        periodic_note=periodic_note, silent=str(silent).lower())
    
    def note_open(self, file: Optional[str] = None, uid: Optional[str] = None,
                  periodic_note: Optional[str] = None) -> bool:
        """Open a note."""
        return self._run('/note/open', file=file, uid=uid, periodic_note=periodic_note)
    
    def note_create(self, file: Optional[str] = None, periodic_note: Optional[str] = None,
                    content: Optional[str] = None, apply: Optional[str] = None,
                    template_file: Optional[str] = None, if_exists: Optional[str] = None,
                    silent: bool = False) -> bool:
        """Create a new note."""
        return self._run('/note/create', file=file, periodic_note=periodic_note,
                        content=content, apply=apply, template_file=template_file,
                        if_exists=if_exists, silent=str(silent).lower())
    
    def note_append(self, content: str, file: Optional[str] = None, uid: Optional[str] = None,
                    periodic_note: Optional[str] = None, below_headline: Optional[str] = None,
                    create_if_not_found: bool = False, ensure_newline: bool = False,
                    silent: bool = False) -> bool:
        """Append content to a note."""
        return self._run('/note/append', file=file, uid=uid, periodic_note=periodic_note,
                        content=content, below_headline=below_headline,
                        create_if_not_found=str(create_if_not_found).lower(),
                        ensure_newline=str(ensure_newline).lower(),
                        silent=str(silent).lower())
    
    def note_prepend(self, content: str, file: Optional[str] = None, uid: Optional[str] = None,
                     periodic_note: Optional[str] = None, below_headline: Optional[str] = None,
                     create_if_not_found: bool = False, ignore_front_matter: bool = False,
                     silent: bool = False) -> bool:
        """Prepend content to a note."""
        return self._run('/note/prepend', file=file, uid=uid, periodic_note=periodic_note,
                        content=content, below_headline=below_headline,
                        create_if_not_found=str(create_if_not_found).lower(),
                        ignore_front_matter=str(ignore_front_matter).lower(),
                        silent=str(silent).lower())
    
    def note_replace(self, search: str, replace: str, file: Optional[str] = None,
                     uid: Optional[str] = None, periodic_note: Optional[str] = None,
                     regex: bool = False, silent: bool = False) -> bool:
        """Search and replace in a note."""
        route = '/note/search-regex-and-replace' if regex else '/note/search-string-and-replace'
        return self._run(route, file=file, uid=uid, periodic_note=periodic_note,
                        search=search, replace=replace, silent=str(silent).lower())
    
    def note_rename(self, new_filename: str, file: Optional[str] = None,
                    uid: Optional[str] = None, periodic_note: Optional[str] = None,
                    silent: bool = False) -> bool:
        """Rename/move a note."""
        return self._run('/note/rename', file=file, uid=uid, periodic_note=periodic_note,
                        new_filename=new_filename, silent=str(silent).lower())
    
    def note_delete(self, file: Optional[str] = None, uid: Optional[str] = None,
                    periodic_note: Optional[str] = None) -> bool:
        """Delete a note."""
        return self._run('/note/delete', file=file, uid=uid, periodic_note=periodic_note)
    
    def note_trash(self, file: Optional[str] = None, uid: Optional[str] = None,
                   periodic_note: Optional[str] = None) -> bool:
        """Move note to trash."""
        return self._run('/note/trash', file=file, uid=uid, periodic_note=periodic_note)
    
    def note_touch(self, file: Optional[str] = None, uid: Optional[str] = None,
                   periodic_note: Optional[str] = None) -> bool:
        """Touch note (update mtime)."""
        return self._run('/note/touch', file=file, uid=uid, periodic_note=periodic_note)
    
    def note_list(self, periodic_note: Optional[str] = None) -> bool:
        """List notes."""
        return self._run('/note/list', periodic_note=periodic_note)
    
    # === Note properties ===
    
    def props_get(self, file: Optional[str] = None, periodic_note: Optional[str] = None) -> bool:
        """Get note properties."""
        return self._run('/note-properties/get', file=file, periodic_note=periodic_note)
    
    def props_set(self, properties: str, file: Optional[str] = None,
                  periodic_note: Optional[str] = None, mode: str = 'overwrite') -> bool:
        """Set note properties (JSON)."""
        return self._run('/note-properties/set', file=file, periodic_note=periodic_note,
                        properties=properties, mode=mode)
    
    def props_clear(self, file: Optional[str] = None, periodic_note: Optional[str] = None) -> bool:
        """Clear all note properties."""
        return self._run('/note-properties/clear', file=file, periodic_note=periodic_note)
    
    def props_remove(self, keys: str, file: Optional[str] = None,
                     periodic_note: Optional[str] = None) -> bool:
        """Remove specific property keys (JSON array)."""
        return self._run('/note-properties/remove-keys', file=file, periodic_note=periodic_note,
                        keys=keys)
    
    # === File operations ===
    
    def file_list(self) -> bool:
        """List all files."""
        return self._run('/file/list')
    
    def file_open(self, file: str) -> bool:
        """Open a file."""
        return self._run('/file/open', file=file)
    
    def file_rename(self, file: str, new_filename: str, silent: bool = False) -> bool:
        """Rename a file."""
        return self._run('/file/rename', file=file, new_filename=new_filename,
                        silent=str(silent).lower())
    
    def file_delete(self, file: str) -> bool:
        """Delete a file."""
        return self._run('/file/delete', file=file)
    
    def file_trash(self, file: str) -> bool:
        """Move file to trash."""
        return self._run('/file/trash', file=file)
    
    def file_get_active(self) -> bool:
        """Get the active file."""
        return self._run('/file/get-active')
    
    # === Folder operations ===
    
    def folder_list(self) -> bool:
        """List folders."""
        return self._run('/folder/list')
    
    def folder_create(self, folder: str) -> bool:
        """Create a folder."""
        return self._run('/folder/create', folder=folder)
    
    def folder_rename(self, folder: str, new_foldername: str) -> bool:
        """Rename a folder."""
        return self._run('/folder/rename', folder=folder, new_foldername=new_foldername)
    
    def folder_delete(self, folder: str) -> bool:
        """Delete a folder."""
        return self._run('/folder/delete', folder=folder)
    
    def folder_trash(self, folder: str) -> bool:
        """Move folder to trash."""
        return self._run('/folder/trash', folder=folder)
    
    # === Commands ===
    
    def command_list(self) -> bool:
        """List available commands."""
        return self._run('/command/list')
    
    def command_execute(self, commands: str, pause_in_secs: float = 0.2) -> bool:
        """Execute commands (comma-separated IDs)."""
        return self._run('/command/execute', commands=commands, pause_in_secs=str(pause_in_secs))
    
    # === Search ===
    
    def search(self, query: str) -> bool:
        """Run Obsidian search."""
        return self._run('/search/all-notes', query=query)
    
    def omnisearch(self, query: str) -> bool:
        """Run Omnisearch query."""
        return self._run('/omnisearch/all-notes', query=query)
    
    # === Dataview ===
    
    def dataview_list(self, dql: str) -> bool:
        """Run Dataview LIST query."""
        return self._run('/dataview/list-query', dql=dql)
    
    def dataview_table(self, dql: str) -> bool:
        """Run Dataview TABLE query."""
        return self._run('/dataview/table-query', dql=dql)
    
    # === Tags ===
    
    def tags_list(self) -> bool:
        """List all tags."""
        return self._run('/tags/list')
    
    # === Info ===
    
    def info(self) -> bool:
        """Get plugin/Obsidian info."""
        return self._run('/info')


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='obdev actions',
        description='Actions URI plugin commands'
    )
    parser.add_argument('--vault', '-v', help='Target vault')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Print URI only')
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # Note commands
    p = sub.add_parser('note-get', help='Get note content')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--silent', '-s', action='store_true')
    
    p = sub.add_parser('note-open', help='Open a note')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    p = sub.add_parser('note-create', help='Create a note')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--content', '-c', help='Initial content')
    p.add_argument('--apply', choices=['content', 'templater', 'templates'])
    p.add_argument('--template', help='Template file path')
    p.add_argument('--if-exists', choices=['skip', 'overwrite'])
    p.add_argument('--silent', '-s', action='store_true')
    
    p = sub.add_parser('note-append', help='Append to a note')
    p.add_argument('content', help='Content to append')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--below', '-b', help='Below headline')
    p.add_argument('--create', action='store_true', help='Create if not found')
    p.add_argument('--newline', action='store_true', help='Ensure newline')
    p.add_argument('--silent', '-s', action='store_true')
    
    p = sub.add_parser('note-prepend', help='Prepend to a note')
    p.add_argument('content', help='Content to prepend')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--below', '-b', help='Below headline')
    p.add_argument('--create', action='store_true', help='Create if not found')
    p.add_argument('--ignore-frontmatter', action='store_true')
    p.add_argument('--silent', '-s', action='store_true')
    
    p = sub.add_parser('note-replace', help='Search and replace in note')
    p.add_argument('search', help='Search text')
    p.add_argument('replace', help='Replacement')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--regex', '-r', action='store_true', help='Use regex')
    p.add_argument('--silent', '-s', action='store_true')
    
    p = sub.add_parser('note-rename', help='Rename/move note')
    p.add_argument('new_name', help='New filename')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--silent', '-s', action='store_true')
    
    p = sub.add_parser('note-delete', help='Delete note')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    p = sub.add_parser('note-trash', help='Trash note')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    p = sub.add_parser('note-touch', help='Touch note')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--uid', '-u', help='Note UID')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    p = sub.add_parser('note-list', help='List notes')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    # Properties
    p = sub.add_parser('props-get', help='Get note properties')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    p = sub.add_parser('props-set', help='Set note properties')
    p.add_argument('properties', help='JSON properties')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--mode', choices=['overwrite', 'update'], default='overwrite')
    
    p = sub.add_parser('props-clear', help='Clear properties')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    p = sub.add_parser('props-remove', help='Remove property keys')
    p.add_argument('keys', help='JSON array of keys')
    p.add_argument('--file', '-f', help='File path')
    p.add_argument('--periodic', '-p', choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    
    # Files
    sub.add_parser('file-list', help='List all files')
    p = sub.add_parser('file-open', help='Open file')
    p.add_argument('file', help='File path')
    p = sub.add_parser('file-rename', help='Rename file')
    p.add_argument('file', help='File path')
    p.add_argument('new_name', help='New name')
    p.add_argument('--silent', '-s', action='store_true')
    p = sub.add_parser('file-delete', help='Delete file')
    p.add_argument('file', help='File path')
    p = sub.add_parser('file-trash', help='Trash file')
    p.add_argument('file', help='File path')
    sub.add_parser('file-active', help='Get active file')
    
    # Folders
    sub.add_parser('folder-list', help='List folders')
    p = sub.add_parser('folder-create', help='Create folder')
    p.add_argument('folder', help='Folder path')
    p = sub.add_parser('folder-rename', help='Rename folder')
    p.add_argument('folder', help='Folder path')
    p.add_argument('new_name', help='New name')
    p = sub.add_parser('folder-delete', help='Delete folder')
    p.add_argument('folder', help='Folder path')
    p = sub.add_parser('folder-trash', help='Trash folder')
    p.add_argument('folder', help='Folder path')
    
    # Commands
    sub.add_parser('cmd-list', help='List commands')
    p = sub.add_parser('cmd-exec', help='Execute commands')
    p.add_argument('commands', help='Command IDs (comma-separated)')
    p.add_argument('--pause', type=float, default=0.2, help='Pause between commands')
    
    # Search
    p = sub.add_parser('search', help='Search notes')
    p.add_argument('query', help='Search query')
    p = sub.add_parser('omnisearch', help='Omnisearch query')
    p.add_argument('query', help='Search query')
    
    # Dataview
    p = sub.add_parser('dv-list', help='Dataview LIST query')
    p.add_argument('dql', help='DQL query')
    p = sub.add_parser('dv-table', help='Dataview TABLE query')
    p.add_argument('dql', help='DQL query')
    
    # Tags
    sub.add_parser('tags', help='List tags')
    
    # Info
    sub.add_parser('info', help='Plugin info')
    
    return parser


def main(args: Optional[list] = None):
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    cli = ActionsURI(vault=parsed.vault, dry_run=parsed.dry_run)
    
    # Note operations
    if parsed.command == 'note-get':
        cli.note_get(file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic,
                    silent=parsed.silent)
    elif parsed.command == 'note-open':
        cli.note_open(file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic)
    elif parsed.command == 'note-create':
        cli.note_create(file=parsed.file, periodic_note=parsed.periodic, content=parsed.content,
                       apply=parsed.apply, template_file=parsed.template, if_exists=parsed.if_exists,
                       silent=parsed.silent)
    elif parsed.command == 'note-append':
        cli.note_append(parsed.content, file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic,
                       below_headline=parsed.below, create_if_not_found=parsed.create,
                       ensure_newline=parsed.newline, silent=parsed.silent)
    elif parsed.command == 'note-prepend':
        cli.note_prepend(parsed.content, file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic,
                        below_headline=parsed.below, create_if_not_found=parsed.create,
                        ignore_front_matter=parsed.ignore_frontmatter, silent=parsed.silent)
    elif parsed.command == 'note-replace':
        cli.note_replace(parsed.search, parsed.replace, file=parsed.file, uid=parsed.uid,
                        periodic_note=parsed.periodic, regex=parsed.regex, silent=parsed.silent)
    elif parsed.command == 'note-rename':
        cli.note_rename(parsed.new_name, file=parsed.file, uid=parsed.uid,
                       periodic_note=parsed.periodic, silent=parsed.silent)
    elif parsed.command == 'note-delete':
        cli.note_delete(file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic)
    elif parsed.command == 'note-trash':
        cli.note_trash(file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic)
    elif parsed.command == 'note-touch':
        cli.note_touch(file=parsed.file, uid=parsed.uid, periodic_note=parsed.periodic)
    elif parsed.command == 'note-list':
        cli.note_list(periodic_note=parsed.periodic)
    
    # Properties
    elif parsed.command == 'props-get':
        cli.props_get(file=parsed.file, periodic_note=parsed.periodic)
    elif parsed.command == 'props-set':
        cli.props_set(parsed.properties, file=parsed.file, periodic_note=parsed.periodic,
                     mode=parsed.mode)
    elif parsed.command == 'props-clear':
        cli.props_clear(file=parsed.file, periodic_note=parsed.periodic)
    elif parsed.command == 'props-remove':
        cli.props_remove(parsed.keys, file=parsed.file, periodic_note=parsed.periodic)
    
    # Files
    elif parsed.command == 'file-list':
        cli.file_list()
    elif parsed.command == 'file-open':
        cli.file_open(parsed.file)
    elif parsed.command == 'file-rename':
        cli.file_rename(parsed.file, parsed.new_name, silent=parsed.silent)
    elif parsed.command == 'file-delete':
        cli.file_delete(parsed.file)
    elif parsed.command == 'file-trash':
        cli.file_trash(parsed.file)
    elif parsed.command == 'file-active':
        cli.file_get_active()
    
    # Folders
    elif parsed.command == 'folder-list':
        cli.folder_list()
    elif parsed.command == 'folder-create':
        cli.folder_create(parsed.folder)
    elif parsed.command == 'folder-rename':
        cli.folder_rename(parsed.folder, parsed.new_name)
    elif parsed.command == 'folder-delete':
        cli.folder_delete(parsed.folder)
    elif parsed.command == 'folder-trash':
        cli.folder_trash(parsed.folder)
    
    # Commands
    elif parsed.command == 'cmd-list':
        cli.command_list()
    elif parsed.command == 'cmd-exec':
        cli.command_execute(parsed.commands, pause_in_secs=parsed.pause)
    
    # Search
    elif parsed.command == 'search':
        cli.search(parsed.query)
    elif parsed.command == 'omnisearch':
        cli.omnisearch(parsed.query)
    
    # Dataview
    elif parsed.command == 'dv-list':
        cli.dataview_list(parsed.dql)
    elif parsed.command == 'dv-table':
        cli.dataview_table(parsed.dql)
    
    # Tags
    elif parsed.command == 'tags':
        cli.tags_list()
    
    # Info
    elif parsed.command == 'info':
        cli.info()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
