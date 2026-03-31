"""
CSS Snippets CLI - Manage Obsidian CSS snippets.

Based on: https://help.obsidian.md/snippets
CSS snippets are stored in <vault>/.obsidian/snippets/
Appearance settings stored in <vault>/.obsidian/appearance.json
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional


def find_obsidian_vaults() -> List[Path]:
    """Find Obsidian vaults on the system."""
    vaults = []
    
    # Check common locations (avoid recursive home search due to timeouts)
    home = Path.home()
    search_paths = [
        home / "Documents",
        home / "Obsidian",
        home / "Library/Mobile Documents/iCloud~md~obsidian/Documents",
        home / "Desktop",
        home / "Projects",
    ]
    
    # Skip directories that might cause timeouts
    skip_names = {'.Trash', 'node_modules', '.git', '__pycache__', 'Library', 'CloudStorage'}
    
    def safe_rglob(base: Path, max_depth: int = 5):
        """Recursively find .obsidian directories with depth limit and skip rules."""
        if max_depth <= 0:
            return
        try:
            for item in base.iterdir():
                if item.name in skip_names:
                    continue
                if item.name == '.obsidian' and item.is_dir():
                    yield item
                elif item.is_dir() and not item.is_symlink():
                    yield from safe_rglob(item, max_depth - 1)
        except (PermissionError, OSError):
            pass
    
    for base in search_paths:
        if base.exists():
            for path in safe_rglob(base):
                vaults.append(path.parent)
    
    # Also check the Obsidian config for known vaults
    obsidian_config = home / "Library/Application Support/obsidian/obsidian.json"
    if obsidian_config.exists():
        try:
            import json
            config = json.loads(obsidian_config.read_text())
            for vault_id, vault_info in config.get('vaults', {}).items():
                vault_path = Path(vault_info.get('path', ''))
                if vault_path.exists():
                    vaults.append(vault_path)
        except Exception:
            pass
    
    return list(set(vaults))


def get_vault_path(vault_name: Optional[str] = None) -> Optional[Path]:
    """Get vault path by name or find the default one."""
    vaults = find_obsidian_vaults()
    
    if not vaults:
        return None
    
    if vault_name:
        for v in vaults:
            if v.name.lower() == vault_name.lower():
                return v
        return None
    
    # Return first vault found
    return vaults[0]


def get_snippets_dir(vault: Path) -> Path:
    """Get the snippets directory for a vault."""
    return vault / ".obsidian" / "snippets"


def get_appearance_file(vault: Path) -> Path:
    """Get the appearance.json file for a vault."""
    return vault / ".obsidian" / "appearance.json"


def read_appearance(vault: Path) -> dict:
    """Read appearance settings from vault."""
    ap_file = get_appearance_file(vault)
    if ap_file.exists():
        return json.loads(ap_file.read_text())
    return {}


def write_appearance(vault: Path, data: dict):
    """Write appearance settings to vault."""
    ap_file = get_appearance_file(vault)
    ap_file.write_text(json.dumps(data, indent=2))


class SnippetsManager:
    """Manage Obsidian CSS snippets."""
    
    def __init__(self, vault: Path):
        self.vault = vault
        self.snippets_dir = get_snippets_dir(vault)
    
    def list_snippets(self, show_status: bool = True) -> List[dict]:
        """List all snippets with their status."""
        self.snippets_dir.mkdir(exist_ok=True)
        
        # Get enabled snippets from appearance.json
        appearance = read_appearance(self.vault)
        enabled = set(appearance.get('enabledCssSnippets', []))
        
        snippets = []
        for f in sorted(self.snippets_dir.glob("*.css")):
            name = f.stem
            snippets.append({
                'name': name,
                'file': f.name,
                'path': str(f),
                'enabled': name in enabled,
                'size': f.stat().st_size,
            })
        
        return snippets
    
    def enable_snippet(self, name: str) -> bool:
        """Enable a snippet by name."""
        # Remove .css extension if provided
        name = name.replace('.css', '')
        
        snippet_file = self.snippets_dir / f"{name}.css"
        if not snippet_file.exists():
            print(f"Error: Snippet '{name}' not found", file=sys.stderr)
            return False
        
        appearance = read_appearance(self.vault)
        enabled = appearance.get('enabledCssSnippets', [])
        
        if name not in enabled:
            enabled.append(name)
            appearance['enabledCssSnippets'] = enabled
            write_appearance(self.vault, appearance)
            print(f"Enabled snippet: {name}")
        else:
            print(f"Snippet '{name}' already enabled")
        
        return True
    
    def disable_snippet(self, name: str) -> bool:
        """Disable a snippet by name."""
        name = name.replace('.css', '')
        
        appearance = read_appearance(self.vault)
        enabled = appearance.get('enabledCssSnippets', [])
        
        if name in enabled:
            enabled.remove(name)
            appearance['enabledCssSnippets'] = enabled
            write_appearance(self.vault, appearance)
            print(f"Disabled snippet: {name}")
        else:
            print(f"Snippet '{name}' not enabled")
        
        return True
    
    def toggle_snippet(self, name: str) -> bool:
        """Toggle a snippet's enabled state."""
        name = name.replace('.css', '')
        
        appearance = read_appearance(self.vault)
        enabled = appearance.get('enabledCssSnippets', [])
        
        if name in enabled:
            return self.disable_snippet(name)
        else:
            return self.enable_snippet(name)
    
    def create_snippet(self, name: str, content: str, enable: bool = False) -> bool:
        """Create a new snippet."""
        name = name.replace('.css', '')
        self.snippets_dir.mkdir(exist_ok=True)
        
        snippet_file = self.snippets_dir / f"{name}.css"
        if snippet_file.exists():
            print(f"Error: Snippet '{name}' already exists", file=sys.stderr)
            return False
        
        snippet_file.write_text(content)
        print(f"Created snippet: {snippet_file}")
        
        if enable:
            self.enable_snippet(name)
        
        return True
    
    def delete_snippet(self, name: str) -> bool:
        """Delete a snippet."""
        name = name.replace('.css', '')
        
        snippet_file = self.snippets_dir / f"{name}.css"
        if not snippet_file.exists():
            print(f"Error: Snippet '{name}' not found", file=sys.stderr)
            return False
        
        # Disable first
        self.disable_snippet(name)
        
        snippet_file.unlink()
        print(f"Deleted snippet: {name}")
        return True
    
    def show_snippet(self, name: str) -> Optional[str]:
        """Show snippet content."""
        name = name.replace('.css', '')
        
        snippet_file = self.snippets_dir / f"{name}.css"
        if not snippet_file.exists():
            print(f"Error: Snippet '{name}' not found", file=sys.stderr)
            return None
        
        return snippet_file.read_text()
    
    def edit_snippet(self, name: str, content: str) -> bool:
        """Update snippet content."""
        name = name.replace('.css', '')
        
        snippet_file = self.snippets_dir / f"{name}.css"
        if not snippet_file.exists():
            print(f"Error: Snippet '{name}' not found", file=sys.stderr)
            return False
        
        snippet_file.write_text(content)
        print(f"Updated snippet: {name}")
        return True
    
    def import_snippet(self, source_path: str, name: Optional[str] = None) -> bool:
        """Import a CSS file as a snippet."""
        source = Path(source_path)
        if not source.exists():
            print(f"Error: File not found: {source_path}", file=sys.stderr)
            return False
        
        self.snippets_dir.mkdir(exist_ok=True)
        
        if name:
            name = name.replace('.css', '')
            dest = self.snippets_dir / f"{name}.css"
        else:
            dest = self.snippets_dir / source.name
        
        shutil.copy2(source, dest)
        print(f"Imported snippet: {dest.stem}")
        return True
    
    def export_snippet(self, name: str, dest_path: str) -> bool:
        """Export a snippet to a file."""
        name = name.replace('.css', '')
        
        snippet_file = self.snippets_dir / f"{name}.css"
        if not snippet_file.exists():
            print(f"Error: Snippet '{name}' not found", file=sys.stderr)
            return False
        
        dest = Path(dest_path)
        shutil.copy2(snippet_file, dest)
        print(f"Exported snippet to: {dest}")
        return True
    
    def enable_all(self) -> bool:
        """Enable all snippets."""
        snippets = self.list_snippets()
        names = [s['name'] for s in snippets]
        
        appearance = read_appearance(self.vault)
        appearance['enabledCssSnippets'] = names
        write_appearance(self.vault, appearance)
        
        print(f"Enabled {len(names)} snippets")
        return True
    
    def disable_all(self) -> bool:
        """Disable all snippets."""
        appearance = read_appearance(self.vault)
        appearance['enabledCssSnippets'] = []
        write_appearance(self.vault, appearance)
        
        print("Disabled all snippets")
        return True


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for snippets commands."""
    parser = argparse.ArgumentParser(
        prog='obdev snippets',
        description='Manage Obsidian CSS snippets'
    )
    parser.add_argument('--vault', '-v', help='Vault name')
    parser.add_argument('--vault-path', '-p', help='Absolute vault path')
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # List
    p = sub.add_parser('list', aliases=['ls'], help='List snippets')
    p.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Enable
    p = sub.add_parser('enable', aliases=['on'], help='Enable a snippet')
    p.add_argument('name', help='Snippet name')
    
    # Disable
    p = sub.add_parser('disable', aliases=['off'], help='Disable a snippet')
    p.add_argument('name', help='Snippet name')
    
    # Toggle
    p = sub.add_parser('toggle', help='Toggle snippet state')
    p.add_argument('name', help='Snippet name')
    
    # Create
    p = sub.add_parser('create', aliases=['new'], help='Create a snippet')
    p.add_argument('name', help='Snippet name')
    p.add_argument('--content', '-c', help='CSS content')
    p.add_argument('--file', '-f', help='Read content from file')
    p.add_argument('--enable', '-e', action='store_true', help='Enable after creating')
    
    # Delete
    p = sub.add_parser('delete', aliases=['rm'], help='Delete a snippet')
    p.add_argument('name', help='Snippet name')
    
    # Show
    p = sub.add_parser('show', aliases=['cat'], help='Show snippet content')
    p.add_argument('name', help='Snippet name')
    
    # Edit
    p = sub.add_parser('edit', help='Update snippet content')
    p.add_argument('name', help='Snippet name')
    p.add_argument('--content', '-c', help='New CSS content')
    p.add_argument('--file', '-f', help='Read content from file')
    
    # Import
    p = sub.add_parser('import', help='Import a CSS file as snippet')
    p.add_argument('source', help='Source CSS file path')
    p.add_argument('--name', '-n', help='Snippet name (default: filename)')
    
    # Export
    p = sub.add_parser('export', help='Export snippet to file')
    p.add_argument('name', help='Snippet name')
    p.add_argument('dest', help='Destination file path')
    
    # Enable all
    sub.add_parser('enable-all', help='Enable all snippets')
    
    # Disable all
    sub.add_parser('disable-all', help='Disable all snippets')
    
    # List vaults
    sub.add_parser('vaults', help='List detected Obsidian vaults')
    
    return parser


def main(args: Optional[list] = None):
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    # Handle vaults command separately
    if parsed.command == 'vaults':
        vaults = find_obsidian_vaults()
        if not vaults:
            print("No Obsidian vaults found")
            return 1
        for v in vaults:
            print(v)
        return 0
    
    # Get vault
    if parsed.vault_path:
        vault = Path(parsed.vault_path)
    else:
        vault = get_vault_path(parsed.vault)
    
    if not vault or not vault.exists():
        print("Error: Vault not found. Use --vault or --vault-path", file=sys.stderr)
        return 1
    
    mgr = SnippetsManager(vault)
    
    if parsed.command in ('list', 'ls'):
        snippets = mgr.list_snippets()
        if getattr(parsed, 'json', False):
            print(json.dumps(snippets, indent=2))
        else:
            for s in snippets:
                status = "✓" if s['enabled'] else "✗"
                print(f"[{status}] {s['name']} ({s['size']} bytes)")
    
    elif parsed.command in ('enable', 'on'):
        mgr.enable_snippet(parsed.name)
    
    elif parsed.command in ('disable', 'off'):
        mgr.disable_snippet(parsed.name)
    
    elif parsed.command == 'toggle':
        mgr.toggle_snippet(parsed.name)
    
    elif parsed.command in ('create', 'new'):
        content = parsed.content or ''
        if parsed.file:
            content = Path(parsed.file).read_text()
        mgr.create_snippet(parsed.name, content, enable=parsed.enable)
    
    elif parsed.command in ('delete', 'rm'):
        mgr.delete_snippet(parsed.name)
    
    elif parsed.command in ('show', 'cat'):
        content = mgr.show_snippet(parsed.name)
        if content:
            print(content)
    
    elif parsed.command == 'edit':
        content = parsed.content
        if parsed.file:
            content = Path(parsed.file).read_text()
        if not content:
            print("Error: Provide --content or --file", file=sys.stderr)
            return 1
        mgr.edit_snippet(parsed.name, content)
    
    elif parsed.command == 'import':
        mgr.import_snippet(parsed.source, name=getattr(parsed, 'name', None))
    
    elif parsed.command == 'export':
        mgr.export_snippet(parsed.name, parsed.dest)
    
    elif parsed.command == 'enable-all':
        mgr.enable_all()
    
    elif parsed.command == 'disable-all':
        mgr.disable_all()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
