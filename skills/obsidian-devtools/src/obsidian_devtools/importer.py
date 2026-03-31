"""
Importer CLI - Obsidian Importer plugin integration.

Based on: https://help.obsidian.md/plugins/importer
The Importer plugin allows importing notes from other apps into Obsidian.

This module provides utilities for preparing imports and triggering the Importer plugin.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================
# Supported Import Formats
# https://help.obsidian.md/plugins/importer
# ============================================================

SUPPORTED_FORMATS = {
    # Note-taking apps
    'notion': {
        'name': 'Notion',
        'extension': '.zip',
        'description': 'Export from Notion as Markdown & CSV, then import the ZIP'
    },
    'evernote': {
        'name': 'Evernote',
        'extension': '.enex',
        'description': 'Export notes from Evernote as ENEX file'
    },
    'onenote': {
        'name': 'Microsoft OneNote',
        'extension': None,
        'description': 'Requires OAuth sign-in through the Importer plugin'
    },
    'apple-notes': {
        'name': 'Apple Notes',
        'extension': None,
        'description': 'Mac-only, requires direct import through plugin'
    },
    'google-keep': {
        'name': 'Google Keep',
        'extension': '.zip',
        'description': 'Export via Google Takeout as ZIP'
    },
    'bear': {
        'name': 'Bear',
        'extension': '.bearnote',
        'description': 'Export Bear notes as Bear archive'
    },
    'roam': {
        'name': 'Roam Research',
        'extension': '.json',
        'description': 'Export from Roam as JSON'
    },
    
    # Standard formats
    'markdown': {
        'name': 'Markdown files',
        'extension': '.md',
        'description': 'Import existing Markdown files'
    },
    'html': {
        'name': 'HTML files',
        'extension': '.html',
        'description': 'Convert HTML to Markdown'
    },
    'txt': {
        'name': 'Plain text',
        'extension': '.txt',
        'description': 'Import plain text files'
    },
    
    # Specialized formats
    'zettelkasten': {
        'name': 'Zettelkasten',
        'extension': None,
        'description': 'Import from Zettelkasten-style systems'
    },
    'textbundle': {
        'name': 'TextBundle',
        'extension': '.textbundle',
        'description': 'Import TextBundle packages'
    }
}


def open_importer_plugin(vault: Optional[str] = None) -> bool:
    """Open the Importer plugin in Obsidian."""
    # Use obsidian:// URI to trigger the command
    uri = "obsidian://advanced-uri?commandid=obsidian-importer%3Aopen"
    if vault:
        uri = f"obsidian://advanced-uri?vault={urllib.parse.quote(vault)}&commandid=obsidian-importer%3Aopen"
    
    try:
        subprocess.run(['open', uri], check=True)
        return True
    except subprocess.CalledProcessError:
        # Fallback to basic URI
        uri = "obsidian://show-plugin?id=obsidian-importer"
        subprocess.run(['open', uri])
        return True


def find_vault_path(vault_name: Optional[str] = None) -> Optional[Path]:
    """Find an Obsidian vault path."""
    home = Path.home()
    
    # First check Obsidian's config for known vaults
    obsidian_config = home / "Library/Application Support/obsidian/obsidian.json"
    if obsidian_config.exists():
        try:
            config = json.loads(obsidian_config.read_text())
            for vault_id, vault_info in config.get('vaults', {}).items():
                vault_path = Path(vault_info.get('path', ''))
                if vault_path.exists():
                    if vault_name is None or vault_path.name.lower() == vault_name.lower():
                        return vault_path
        except Exception:
            pass
    
    # Fallback to searching common locations
    search_paths = [
        home / "Documents",
        home / "Obsidian", 
        home / "Library/Mobile Documents/iCloud~md~obsidian/Documents",
        home / "Desktop",
    ]
    
    skip_names = {'.Trash', 'node_modules', '.git', '__pycache__', 'Library', 'CloudStorage'}
    
    def safe_search(base: Path, max_depth: int = 4):
        if max_depth <= 0:
            return
        try:
            for item in base.iterdir():
                if item.name in skip_names:
                    continue
                if item.name == '.obsidian' and item.is_dir():
                    yield item.parent
                elif item.is_dir() and not item.is_symlink():
                    yield from safe_search(item, max_depth - 1)
        except (PermissionError, OSError):
            pass
    
    for base in search_paths:
        if base.exists():
            for vault in safe_search(base):
                if vault_name is None or vault.name.lower() == vault_name.lower():
                    return vault
    return None


class ImportPreparer:
    """Prepare files for import into Obsidian."""
    
    def __init__(self, dest_vault: Path):
        self.vault = dest_vault
        self.import_folder = dest_vault / "_imports"
    
    def prepare_folder(self, timestamp: bool = True) -> Path:
        """Create import staging folder."""
        if timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder = self.import_folder / ts
        else:
            folder = self.import_folder
        
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    
    def copy_files(self, sources: List[str], subfolder: Optional[str] = None) -> List[Path]:
        """Copy files to import folder."""
        dest = self.prepare_folder()
        if subfolder:
            dest = dest / subfolder
            dest.mkdir(exist_ok=True)
        
        copied = []
        for src in sources:
            src_path = Path(src)
            if not src_path.exists():
                print(f"Warning: {src} not found", file=sys.stderr)
                continue
            
            if src_path.is_dir():
                dest_path = dest / src_path.name
                shutil.copytree(src_path, dest_path)
            else:
                dest_path = dest / src_path.name
                shutil.copy2(src_path, dest_path)
            
            copied.append(dest_path)
            print(f"Copied: {src} -> {dest_path}")
        
        return copied
    
    def prepare_notion_export(self, zip_path: str) -> Path:
        """Prepare a Notion export for import."""
        import zipfile
        
        dest = self.prepare_folder()
        notion_dir = dest / "notion"
        notion_dir.mkdir()
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(notion_dir)
        
        print(f"Extracted Notion export to: {notion_dir}")
        return notion_dir
    
    def prepare_evernote_export(self, enex_path: str) -> Path:
        """Prepare an Evernote export for import."""
        dest = self.prepare_folder()
        dest_path = dest / Path(enex_path).name
        shutil.copy2(enex_path, dest_path)
        print(f"Copied Evernote export to: {dest_path}")
        return dest_path
    
    def prepare_roam_export(self, json_path: str) -> Path:
        """Prepare a Roam Research export for import."""
        dest = self.prepare_folder()
        dest_path = dest / Path(json_path).name
        shutil.copy2(json_path, dest_path)
        print(f"Copied Roam export to: {dest_path}")
        return dest_path


class MarkdownConverter:
    """Convert various formats to Markdown for import."""
    
    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """Convert HTML to Markdown (basic conversion)."""
        import re
        
        md = html_content
        
        # Headers
        for i in range(6, 0, -1):
            md = re.sub(f'<h{i}[^>]*>(.*?)</h{i}>', '#' * i + r' \1\n', md, flags=re.DOTALL)
        
        # Bold
        md = re.sub(r'<(strong|b)>(.*?)</\1>', r'**\2**', md, flags=re.DOTALL)
        
        # Italic
        md = re.sub(r'<(em|i)>(.*?)</\1>', r'*\2*', md, flags=re.DOTALL)
        
        # Links
        md = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', md, flags=re.DOTALL)
        
        # Images
        md = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*/?>', r'![](\1)', md)
        
        # Lists
        md = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', md, flags=re.DOTALL)
        md = re.sub(r'</?[ou]l[^>]*>', '', md)
        
        # Paragraphs
        md = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', md, flags=re.DOTALL)
        
        # Code
        md = re.sub(r'<code>(.*?)</code>', r'`\1`', md, flags=re.DOTALL)
        md = re.sub(r'<pre>(.*?)</pre>', r'```\n\1\n```', md, flags=re.DOTALL)
        
        # Line breaks
        md = re.sub(r'<br\s*/?>', '\n', md)
        
        # Strip remaining tags
        md = re.sub(r'<[^>]+>', '', md)
        
        # Clean up whitespace
        md = re.sub(r'\n{3,}', '\n\n', md)
        md = md.strip()
        
        return md
    
    @staticmethod
    def convert_file(source: str, dest: str, format_type: str = 'html') -> bool:
        """Convert a file to Markdown."""
        src_path = Path(source)
        dest_path = Path(dest)
        
        if not src_path.exists():
            print(f"Error: {source} not found", file=sys.stderr)
            return False
        
        content = src_path.read_text(encoding='utf-8')
        
        if format_type == 'html':
            md_content = MarkdownConverter.html_to_markdown(content)
        else:
            # Plain text - just copy
            md_content = content
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(md_content, encoding='utf-8')
        
        print(f"Converted: {source} -> {dest}")
        return True


def create_import_note(title: str, source_app: str, date: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> str:
    """Create a Markdown note with import metadata."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    frontmatter = {
        'imported_from': source_app,
        'import_date': date,
    }
    if tags:
        frontmatter['tags'] = tags
    
    # Build YAML frontmatter
    yaml_lines = ['---']
    for key, value in frontmatter.items():
        if isinstance(value, list):
            yaml_lines.append(f'{key}:')
            for item in value:
                yaml_lines.append(f'  - {item}')
        else:
            yaml_lines.append(f'{key}: {value}')
    yaml_lines.append('---')
    yaml_lines.append('')
    yaml_lines.append(f'# {title}')
    yaml_lines.append('')
    
    return '\n'.join(yaml_lines)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for importer commands."""
    parser = argparse.ArgumentParser(
        prog='obdev importer',
        description='Obsidian Importer plugin integration'
    )
    parser.add_argument('--vault', '-v', help='Target vault name')
    parser.add_argument('--vault-path', '-p', help='Target vault path')
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # List supported formats
    sub.add_parser('formats', aliases=['list'], help='List supported import formats')
    
    # Open importer
    sub.add_parser('open', help='Open the Importer plugin in Obsidian')
    
    # Show plugin info
    sub.add_parser('show-plugin', help='Open Importer plugin page')
    
    # Prepare imports
    p = sub.add_parser('prepare', help='Prepare files for import')
    p.add_argument('sources', nargs='+', help='Source files or directories')
    p.add_argument('--subfolder', '-s', help='Subfolder name in imports')
    
    # Prepare Notion
    p = sub.add_parser('notion', help='Prepare Notion export')
    p.add_argument('zip_file', help='Notion export ZIP file')
    
    # Prepare Evernote
    p = sub.add_parser('evernote', help='Prepare Evernote export')
    p.add_argument('enex_file', help='Evernote ENEX file')
    
    # Prepare Roam
    p = sub.add_parser('roam', help='Prepare Roam Research export')
    p.add_argument('json_file', help='Roam JSON export')
    
    # Convert HTML
    p = sub.add_parser('convert-html', help='Convert HTML files to Markdown')
    p.add_argument('source', help='Source HTML file')
    p.add_argument('dest', help='Destination Markdown file')
    
    # Batch convert
    p = sub.add_parser('batch-convert', help='Batch convert files to Markdown')
    p.add_argument('source_dir', help='Source directory')
    p.add_argument('dest_dir', help='Destination directory')
    p.add_argument('--format', '-f', default='html', choices=['html', 'txt'])
    p.add_argument('--extension', '-e', help='Source file extension (default: .html or .txt)')
    
    # Create import note
    p = sub.add_parser('create-note', help='Create a note with import metadata')
    p.add_argument('title', help='Note title')
    p.add_argument('--source', '-s', required=True, help='Source application')
    p.add_argument('--tags', '-t', nargs='+', help='Tags to add')
    p.add_argument('--output', '-o', help='Output file path')
    
    # Help for specific format
    p = sub.add_parser('help', help='Show help for a specific format')
    p.add_argument('format_name', nargs='?', choices=list(SUPPORTED_FORMATS.keys()))
    
    return parser


def main(args: Optional[list] = None):
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    # Get vault if needed
    vault = None
    if hasattr(parsed, 'vault_path') and parsed.vault_path:
        vault = Path(parsed.vault_path)
    elif hasattr(parsed, 'vault') and parsed.vault:
        vault = find_vault_path(parsed.vault)
    else:
        vault = find_vault_path()
    
    if parsed.command in ('formats', 'list'):
        print("Supported Import Formats:")
        print("=" * 60)
        for key, info in SUPPORTED_FORMATS.items():
            ext = info['extension'] or '(direct)'
            print(f"\n{key}:")
            print(f"  Name: {info['name']}")
            print(f"  Extension: {ext}")
            print(f"  {info['description']}")
        return 0
    
    elif parsed.command == 'open':
        vault_name = parsed.vault if hasattr(parsed, 'vault') else None
        open_importer_plugin(vault_name)
        print("Opening Importer plugin in Obsidian...")
        return 0
    
    elif parsed.command == 'show-plugin':
        subprocess.run(['open', 'obsidian://show-plugin?id=obsidian-importer'])
        return 0
    
    elif parsed.command == 'prepare':
        if not vault:
            print("Error: Vault not found. Use --vault or --vault-path", file=sys.stderr)
            return 1
        preparer = ImportPreparer(vault)
        preparer.copy_files(parsed.sources, subfolder=parsed.subfolder)
        print(f"\nFiles prepared in: {preparer.import_folder}")
        print("Now open the Importer plugin to complete the import.")
        return 0
    
    elif parsed.command == 'notion':
        if not vault:
            print("Error: Vault not found", file=sys.stderr)
            return 1
        preparer = ImportPreparer(vault)
        preparer.prepare_notion_export(parsed.zip_file)
        print("\nNotion export extracted. Open Importer plugin to complete import.")
        return 0
    
    elif parsed.command == 'evernote':
        if not vault:
            print("Error: Vault not found", file=sys.stderr)
            return 1
        preparer = ImportPreparer(vault)
        preparer.prepare_evernote_export(parsed.enex_file)
        print("\nEvernote export prepared. Open Importer plugin to complete import.")
        return 0
    
    elif parsed.command == 'roam':
        if not vault:
            print("Error: Vault not found", file=sys.stderr)
            return 1
        preparer = ImportPreparer(vault)
        preparer.prepare_roam_export(parsed.json_file)
        print("\nRoam export prepared. Open Importer plugin to complete import.")
        return 0
    
    elif parsed.command == 'convert-html':
        MarkdownConverter.convert_file(parsed.source, parsed.dest, 'html')
        return 0
    
    elif parsed.command == 'batch-convert':
        src_dir = Path(parsed.source_dir)
        dest_dir = Path(parsed.dest_dir)
        ext = parsed.extension or (f'.{parsed.format}')
        
        if not src_dir.exists():
            print(f"Error: Source directory not found: {src_dir}", file=sys.stderr)
            return 1
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for src_file in src_dir.rglob(f'*{ext}'):
            rel_path = src_file.relative_to(src_dir)
            dest_file = dest_dir / rel_path.with_suffix('.md')
            MarkdownConverter.convert_file(str(src_file), str(dest_file), parsed.format)
        
        print(f"\nBatch conversion complete. Output in: {dest_dir}")
        return 0
    
    elif parsed.command == 'create-note':
        note_content = create_import_note(
            parsed.title,
            parsed.source,
            tags=parsed.tags
        )
        
        if parsed.output:
            Path(parsed.output).write_text(note_content)
            print(f"Created: {parsed.output}")
        else:
            print(note_content)
        return 0
    
    elif parsed.command == 'help':
        if parsed.format_name:
            info = SUPPORTED_FORMATS.get(parsed.format_name)
            if info:
                print(f"\n{info['name']}")
                print("=" * 40)
                print(f"Format key: {parsed.format_name}")
                print(f"Extension: {info['extension'] or '(direct import)'}")
                print(f"\n{info['description']}")
                
                # Format-specific instructions
                instructions = {
                    'notion': """
How to export from Notion:
1. Open Notion
2. Go to Settings & Members > Settings
3. Scroll down to Export content
4. Choose "Markdown & CSV" format
5. Click Export
6. Use: obdev importer notion <zip_file>
""",
                    'evernote': """
How to export from Evernote:
1. Open Evernote desktop app
2. Select notebooks to export
3. File > Export Notes...
4. Choose ENEX format
5. Use: obdev importer evernote <enex_file>
""",
                    'roam': """
How to export from Roam Research:
1. Open Roam
2. Click "..." menu in sidebar
3. Export All > JSON
4. Use: obdev importer roam <json_file>
""",
                    'google-keep': """
How to export from Google Keep:
1. Go to takeout.google.com
2. Deselect all, then select Google Keep
3. Export and download the ZIP
4. Extract and use: obdev importer prepare <folder>
"""
                }
                
                if parsed.format_name in instructions:
                    print(instructions[parsed.format_name])
        else:
            print("Use 'obdev importer help <format>' for format-specific help")
            print("Available formats:", ', '.join(SUPPORTED_FORMATS.keys()))
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
