"""
Local REST API CLI - Interface with the Obsidian Local REST API plugin.

Provides HTTP-based API access to Obsidian vaults.
Based on: https://github.com/coddingtonbear/obsidian-local-rest-api
"""

import argparse
import json
import os
import sys
import urllib.parse
from typing import Optional
import httpx


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 27124


class ObsidianRestClient:
    """Client for Obsidian Local REST API."""
    
    def __init__(self, api_key: Optional[str] = None, host: str = DEFAULT_HOST, 
                 port: int = DEFAULT_PORT, verify_ssl: bool = False):
        self.base_url = f"https://{host}:{port}"
        self.api_key = api_key or os.environ.get("OBSIDIAN_API_KEY", "")
        self.verify_ssl = verify_ssl
        self._client = None
    
    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                verify=self.verify_ssl,
                timeout=30.0
            )
        return self._client
    
    def close(self):
        if self._client:
            self._client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    # === System ===
    
    def status(self) -> dict:
        """Get system status (no auth required)."""
        r = self.client.get("/")
        r.raise_for_status()
        return r.json()
    
    # === Active File ===
    
    def active_get(self, as_json: bool = False, as_map: bool = False) -> str | dict:
        """Get the active file content."""
        headers = {}
        if as_json:
            headers["Accept"] = "application/vnd.olrapi.note+json"
        elif as_map:
            headers["Accept"] = "application/vnd.olrapi.document-map+json"
        
        r = self.client.get("/active/", headers=headers)
        r.raise_for_status()
        return r.json() if (as_json or as_map) else r.text
    
    def active_put(self, content: str) -> None:
        """Replace active file content."""
        r = self.client.put("/active/", content=content, 
                           headers={"Content-Type": "text/markdown"})
        r.raise_for_status()
    
    def active_append(self, content: str) -> None:
        """Append to active file."""
        r = self.client.post("/active/", content=content,
                            headers={"Content-Type": "text/markdown"})
        r.raise_for_status()
    
    def active_patch(self, content: str, operation: str, target_type: str, 
                     target: str, create_if_missing: bool = False,
                     content_type: str = "text/markdown") -> None:
        """Patch active file at specific location."""
        headers = {
            "Operation": operation,
            "Target-Type": target_type,
            "Target": urllib.parse.quote(target),
            "Content-Type": content_type,
        }
        if create_if_missing:
            headers["Create-Target-If-Missing"] = "true"
        
        r = self.client.patch("/active/", content=content, headers=headers)
        r.raise_for_status()
    
    def active_delete(self) -> None:
        """Delete active file."""
        r = self.client.delete("/active/")
        r.raise_for_status()
    
    # === Vault Files ===
    
    def vault_list(self, path: str = "") -> list:
        """List files in vault directory."""
        r = self.client.get(f"/vault/{path}")
        r.raise_for_status()
        return r.json().get("files", [])
    
    def vault_get(self, path: str, as_json: bool = False, as_map: bool = False) -> str | dict:
        """Get file content."""
        headers = {}
        if as_json:
            headers["Accept"] = "application/vnd.olrapi.note+json"
        elif as_map:
            headers["Accept"] = "application/vnd.olrapi.document-map+json"
        
        r = self.client.get(f"/vault/{path}", headers=headers)
        r.raise_for_status()
        return r.json() if (as_json or as_map) else r.text
    
    def vault_put(self, path: str, content: str, content_type: str = "text/markdown") -> None:
        """Create or replace file."""
        r = self.client.put(f"/vault/{path}", content=content,
                           headers={"Content-Type": content_type})
        r.raise_for_status()
    
    def vault_append(self, path: str, content: str) -> None:
        """Append to file."""
        r = self.client.post(f"/vault/{path}", content=content,
                            headers={"Content-Type": "text/markdown"})
        r.raise_for_status()
    
    def vault_patch(self, path: str, content: str, operation: str, target_type: str,
                    target: str, create_if_missing: bool = False,
                    content_type: str = "text/markdown") -> None:
        """Patch file at specific location."""
        headers = {
            "Operation": operation,
            "Target-Type": target_type,
            "Target": urllib.parse.quote(target),
            "Content-Type": content_type,
        }
        if create_if_missing:
            headers["Create-Target-If-Missing"] = "true"
        
        r = self.client.patch(f"/vault/{path}", content=content, headers=headers)
        r.raise_for_status()
    
    def vault_delete(self, path: str) -> None:
        """Delete file."""
        r = self.client.delete(f"/vault/{path}")
        r.raise_for_status()
    
    # === Periodic Notes ===
    
    def periodic_get(self, period: str = "daily", as_json: bool = False, 
                     as_map: bool = False, year: int = None, month: int = None, 
                     day: int = None) -> str | dict:
        """Get periodic note content."""
        headers = {}
        if as_json:
            headers["Accept"] = "application/vnd.olrapi.note+json"
        elif as_map:
            headers["Accept"] = "application/vnd.olrapi.document-map+json"
        
        if year and month and day:
            url = f"/periodic/{period}/{year}/{month}/{day}/"
        else:
            url = f"/periodic/{period}/"
        
        r = self.client.get(url, headers=headers)
        r.raise_for_status()
        return r.json() if (as_json or as_map) else r.text
    
    def periodic_put(self, content: str, period: str = "daily",
                     year: int = None, month: int = None, day: int = None) -> None:
        """Create or replace periodic note."""
        if year and month and day:
            url = f"/periodic/{period}/{year}/{month}/{day}/"
        else:
            url = f"/periodic/{period}/"
        
        r = self.client.put(url, content=content,
                           headers={"Content-Type": "text/markdown"})
        r.raise_for_status()
    
    def periodic_append(self, content: str, period: str = "daily",
                        year: int = None, month: int = None, day: int = None) -> None:
        """Append to periodic note."""
        if year and month and day:
            url = f"/periodic/{period}/{year}/{month}/{day}/"
        else:
            url = f"/periodic/{period}/"
        
        r = self.client.post(url, content=content,
                            headers={"Content-Type": "text/markdown"})
        r.raise_for_status()
    
    def periodic_patch(self, content: str, operation: str, target_type: str,
                       target: str, period: str = "daily",
                       year: int = None, month: int = None, day: int = None,
                       create_if_missing: bool = False,
                       content_type: str = "text/markdown") -> None:
        """Patch periodic note."""
        headers = {
            "Operation": operation,
            "Target-Type": target_type,
            "Target": urllib.parse.quote(target),
            "Content-Type": content_type,
        }
        if create_if_missing:
            headers["Create-Target-If-Missing"] = "true"
        
        if year and month and day:
            url = f"/periodic/{period}/{year}/{month}/{day}/"
        else:
            url = f"/periodic/{period}/"
        
        r = self.client.patch(url, content=content, headers=headers)
        r.raise_for_status()
    
    def periodic_delete(self, period: str = "daily",
                        year: int = None, month: int = None, day: int = None) -> None:
        """Delete periodic note."""
        if year and month and day:
            url = f"/periodic/{period}/{year}/{month}/{day}/"
        else:
            url = f"/periodic/{period}/"
        
        r = self.client.delete(url)
        r.raise_for_status()
    
    # === Commands ===
    
    def commands_list(self) -> list:
        """List available commands."""
        r = self.client.get("/commands/")
        r.raise_for_status()
        return r.json().get("commands", [])
    
    def commands_execute(self, command_id: str) -> None:
        """Execute a command."""
        r = self.client.post(f"/commands/{command_id}/")
        r.raise_for_status()
    
    # === Open ===
    
    def open_file(self, path: str, new_leaf: bool = False) -> None:
        """Open a file in Obsidian."""
        params = {"newLeaf": str(new_leaf).lower()} if new_leaf else {}
        r = self.client.post(f"/open/{path}", params=params)
        r.raise_for_status()


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='obdev rest',
        description='Obsidian Local REST API commands'
    )
    parser.add_argument('--api-key', '-k', help='API key (or set OBSIDIAN_API_KEY)')
    parser.add_argument('--host', default=DEFAULT_HOST, help=f'Host (default: {DEFAULT_HOST})')
    parser.add_argument('--port', '-p', type=int, default=DEFAULT_PORT, 
                       help=f'Port (default: {DEFAULT_PORT})')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # System
    sub.add_parser('status', help='Get system status')
    
    # Active file
    p = sub.add_parser('active-get', help='Get active file')
    p.add_argument('--map', action='store_true', help='Get document map')
    
    p = sub.add_parser('active-put', help='Replace active file')
    p.add_argument('content', help='Content (or - for stdin)')
    
    p = sub.add_parser('active-append', help='Append to active file')
    p.add_argument('content', help='Content (or - for stdin)')
    
    p = sub.add_parser('active-patch', help='Patch active file')
    p.add_argument('content', help='Content (or - for stdin)')
    p.add_argument('--op', required=True, choices=['append', 'prepend', 'replace'])
    p.add_argument('--type', required=True, choices=['heading', 'block', 'frontmatter'])
    p.add_argument('--target', required=True, help='Target (heading path, block id, or field)')
    p.add_argument('--create', action='store_true', help='Create target if missing')
    
    sub.add_parser('active-delete', help='Delete active file')
    
    # Vault files
    p = sub.add_parser('ls', help='List vault files')
    p.add_argument('path', nargs='?', default='', help='Directory path')
    
    p = sub.add_parser('cat', help='Get file content')
    p.add_argument('path', help='File path')
    p.add_argument('--map', action='store_true', help='Get document map')
    
    p = sub.add_parser('write', help='Create/replace file')
    p.add_argument('path', help='File path')
    p.add_argument('content', help='Content (or - for stdin)')
    
    p = sub.add_parser('append', help='Append to file')
    p.add_argument('path', help='File path')
    p.add_argument('content', help='Content (or - for stdin)')
    
    p = sub.add_parser('patch', help='Patch file')
    p.add_argument('path', help='File path')
    p.add_argument('content', help='Content (or - for stdin)')
    p.add_argument('--op', required=True, choices=['append', 'prepend', 'replace'])
    p.add_argument('--type', required=True, choices=['heading', 'block', 'frontmatter'])
    p.add_argument('--target', required=True, help='Target')
    p.add_argument('--create', action='store_true', help='Create target if missing')
    
    p = sub.add_parser('rm', help='Delete file')
    p.add_argument('path', help='File path')
    
    # Periodic notes
    p = sub.add_parser('periodic-get', help='Get periodic note')
    p.add_argument('--period', default='daily', 
                  choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--date', help='Date as YYYY-MM-DD')
    p.add_argument('--map', action='store_true', help='Get document map')
    
    p = sub.add_parser('periodic-put', help='Replace periodic note')
    p.add_argument('content', help='Content (or - for stdin)')
    p.add_argument('--period', default='daily',
                  choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--date', help='Date as YYYY-MM-DD')
    
    p = sub.add_parser('periodic-append', help='Append to periodic note')
    p.add_argument('content', help='Content (or - for stdin)')
    p.add_argument('--period', default='daily',
                  choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--date', help='Date as YYYY-MM-DD')
    
    p = sub.add_parser('periodic-patch', help='Patch periodic note')
    p.add_argument('content', help='Content (or - for stdin)')
    p.add_argument('--period', default='daily',
                  choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--date', help='Date as YYYY-MM-DD')
    p.add_argument('--op', required=True, choices=['append', 'prepend', 'replace'])
    p.add_argument('--type', required=True, choices=['heading', 'block', 'frontmatter'])
    p.add_argument('--target', required=True, help='Target')
    p.add_argument('--create', action='store_true', help='Create target if missing')
    
    p = sub.add_parser('periodic-delete', help='Delete periodic note')
    p.add_argument('--period', default='daily',
                  choices=['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    p.add_argument('--date', help='Date as YYYY-MM-DD')
    
    # Commands
    sub.add_parser('commands', help='List commands')
    p = sub.add_parser('exec', help='Execute command')
    p.add_argument('command_id', help='Command ID')
    
    # Open
    p = sub.add_parser('open', help='Open file in Obsidian')
    p.add_argument('path', help='File path')
    p.add_argument('--new-leaf', action='store_true', help='Open in new tab')
    
    return parser


def parse_date(date_str: str) -> tuple:
    """Parse YYYY-MM-DD into (year, month, day)."""
    if not date_str:
        return None, None, None
    parts = date_str.split('-')
    return int(parts[0]), int(parts[1]), int(parts[2])


def read_content(content: str) -> str:
    """Read content from argument or stdin."""
    if content == '-':
        return sys.stdin.read()
    return content


def main(args: Optional[list] = None):
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    try:
        with ObsidianRestClient(
            api_key=parsed.api_key,
            host=parsed.host,
            port=parsed.port
        ) as client:
            
            # System
            if parsed.command == 'status':
                result = client.status()
                print(json.dumps(result, indent=2) if parsed.json else result)
            
            # Active file
            elif parsed.command == 'active-get':
                result = client.active_get(as_json=parsed.json, as_map=parsed.map)
                print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
            
            elif parsed.command == 'active-put':
                content = read_content(parsed.content)
                client.active_put(content)
                print("Updated active file")
            
            elif parsed.command == 'active-append':
                content = read_content(parsed.content)
                client.active_append(content)
                print("Appended to active file")
            
            elif parsed.command == 'active-patch':
                content = read_content(parsed.content)
                client.active_patch(content, parsed.op, parsed.type, parsed.target,
                                   create_if_missing=parsed.create)
                print("Patched active file")
            
            elif parsed.command == 'active-delete':
                client.active_delete()
                print("Deleted active file")
            
            # Vault files
            elif parsed.command == 'ls':
                files = client.vault_list(parsed.path)
                if parsed.json:
                    print(json.dumps(files, indent=2))
                else:
                    for f in files:
                        print(f)
            
            elif parsed.command == 'cat':
                result = client.vault_get(parsed.path, as_json=parsed.json, as_map=parsed.map)
                print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
            
            elif parsed.command == 'write':
                content = read_content(parsed.content)
                client.vault_put(parsed.path, content)
                print(f"Wrote {parsed.path}")
            
            elif parsed.command == 'append':
                content = read_content(parsed.content)
                client.vault_append(parsed.path, content)
                print(f"Appended to {parsed.path}")
            
            elif parsed.command == 'patch':
                content = read_content(parsed.content)
                client.vault_patch(parsed.path, content, parsed.op, parsed.type,
                                  parsed.target, create_if_missing=parsed.create)
                print(f"Patched {parsed.path}")
            
            elif parsed.command == 'rm':
                client.vault_delete(parsed.path)
                print(f"Deleted {parsed.path}")
            
            # Periodic notes
            elif parsed.command == 'periodic-get':
                year, month, day = parse_date(parsed.date) if hasattr(parsed, 'date') else (None, None, None)
                result = client.periodic_get(parsed.period, as_json=parsed.json, 
                                            as_map=parsed.map, year=year, month=month, day=day)
                print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
            
            elif parsed.command == 'periodic-put':
                content = read_content(parsed.content)
                year, month, day = parse_date(parsed.date) if hasattr(parsed, 'date') else (None, None, None)
                client.periodic_put(content, parsed.period, year=year, month=month, day=day)
                print(f"Updated {parsed.period} note")
            
            elif parsed.command == 'periodic-append':
                content = read_content(parsed.content)
                year, month, day = parse_date(parsed.date) if hasattr(parsed, 'date') else (None, None, None)
                client.periodic_append(content, parsed.period, year=year, month=month, day=day)
                print(f"Appended to {parsed.period} note")
            
            elif parsed.command == 'periodic-patch':
                content = read_content(parsed.content)
                year, month, day = parse_date(parsed.date) if hasattr(parsed, 'date') else (None, None, None)
                client.periodic_patch(content, parsed.op, parsed.type, parsed.target,
                                     parsed.period, year=year, month=month, day=day,
                                     create_if_missing=parsed.create)
                print(f"Patched {parsed.period} note")
            
            elif parsed.command == 'periodic-delete':
                year, month, day = parse_date(parsed.date) if hasattr(parsed, 'date') else (None, None, None)
                client.periodic_delete(parsed.period, year=year, month=month, day=day)
                print(f"Deleted {parsed.period} note")
            
            # Commands
            elif parsed.command == 'commands':
                commands = client.commands_list()
                if parsed.json:
                    print(json.dumps(commands, indent=2))
                else:
                    for cmd in commands:
                        print(f"{cmd['id']:<40} {cmd['name']}")
            
            elif parsed.command == 'exec':
                client.commands_execute(parsed.command_id)
                print(f"Executed: {parsed.command_id}")
            
            # Open
            elif parsed.command == 'open':
                client.open_file(parsed.path, new_leaf=parsed.new_leaf)
                print(f"Opened: {parsed.path}")
        
        return 0
        
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
        return 1
    except httpx.ConnectError:
        print("Error: Cannot connect to Obsidian REST API. Is the plugin running?", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
