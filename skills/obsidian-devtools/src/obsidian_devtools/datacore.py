"""
Datacore CLI - Query Obsidian's Datacore plugin via DevTools Protocol.

Executes Datacore queries through Obsidian's JavaScript API.
Based on: https://github.com/blacksmithgu/datacore
"""

import argparse
import asyncio
import json
import sys
from typing import Optional

from .client import CDPClient
from .launcher import ObsidianLauncher


# JavaScript templates for Datacore operations
JS_CHECK_DATACORE = """
(function() {
    const dc = app.plugins.plugins['datacore'];
    return dc ? { available: true, version: dc.manifest.version } : { available: false };
})()
"""

JS_QUERY = """
(function() {
    const dc = app.plugins.plugins['datacore']?.api;
    if (!dc) return { error: 'Datacore not available' };
    try {
        const results = dc.query(`{query}`);
        return results.map(r => {{
            id: r.$id,
            type: r.$typename,
            path: r.$path || r.$file,
            link: r.$link?.path,
            fields: r.fields?.reduce((acc, f) => {{ acc[f.key] = f.value; return acc; }}, {{}}) || {{}}
        }});
    } catch (e) {
        return { error: e.message };
    }
})()
"""

JS_FULLQUERY = """
(function() {
    const dc = app.plugins.plugins['datacore']?.api;
    if (!dc) return { error: 'Datacore not available' };
    try {
        const result = dc.fullquery(`{query}`);
        return {
            duration: result.duration,
            revision: result.revision,
            count: result.results.length,
            results: result.results.slice(0, {limit}).map(r => ({
                id: r.$id,
                type: r.$typename,
                path: r.$path || r.$file,
                link: r.$link?.path,
                fields: r.fields?.reduce((acc, f) => { acc[f.key] = f.value; return acc; }, {}) || {}
            }))
        };
    } catch (e) {
        return { error: e.message };
    }
})()
"""

JS_PAGE = """
(function() {
    const dc = app.plugins.plugins['datacore']?.api;
    if (!dc) return { error: 'Datacore not available' };
    try {
        const page = dc.page(`{path}`);
        if (!page) return { error: 'Page not found' };
        return {
            id: page.$id,
            path: page.$path,
            name: page.$name,
            link: page.$link?.path,
            tags: page.$tags || [],
            links: page.$links?.map(l => l.path) || [],
            fields: page.fields?.reduce((acc, f) => { acc[f.key] = f.value; return acc; }, {}) || {},
            sections: page.$sections?.map(s => ({
                title: s.$title,
                level: s.$level,
                position: s.$position
            })) || []
        };
    } catch (e) {
        return { error: e.message };
    }
})()
"""

JS_EVAL = """
(function() {
    const dc = app.plugins.plugins['datacore']?.api;
    if (!dc) return { error: 'Datacore not available' };
    try {
        const result = dc.evaluate(`{expression}`);
        return { result: result };
    } catch (e) {
        return { error: e.message };
    }
})()
"""

JS_TYPES = """
(function() {
    return {
        types: [
            '@file', '@page', '@section', '@block', '@block-list',
            '@codeblock', '@datablock', '@list-item', '@task'
        ],
        description: {
            '@file': 'All files in vault',
            '@page': 'All markdown pages',
            '@section': 'All sections in markdown pages',
            '@block': 'All blocks in markdown pages',
            '@block-list': 'All list blocks',
            '@codeblock': 'All codeblocks',
            '@datablock': 'Datacore datablocks (yaml:data)',
            '@list-item': 'All list items',
            '@task': 'All task items (- [ ])'
        }
    };
})()
"""


class DatacoreCLI:
    """Datacore CLI client."""
    
    def __init__(self, port: int = 9222):
        self.port = port
        self.client = CDPClient(port=port)
    
    async def connect(self) -> bool:
        """Connect to Obsidian via CDP."""
        try:
            await self.client.connect()
            return True
        except Exception:
            # Try launching Obsidian
            launcher = ObsidianLauncher()
            await launcher.ensure_running(port=self.port)
            try:
                await self.client.connect()
                return True
            except Exception:
                return False
    
    async def close(self):
        """Close connection."""
        await self.client.close()
    
    async def _eval(self, js: str) -> dict:
        """Evaluate JavaScript and return result."""
        result = await self.client.evaluate(js)
        if isinstance(result, str):
            try:
                return json.loads(result)
            except:
                return {"result": result}
        return result if isinstance(result, dict) else {"result": result}
    
    async def check(self) -> dict:
        """Check if Datacore is available."""
        return await self._eval(JS_CHECK_DATACORE)
    
    async def query(self, query: str) -> list | dict:
        """Run a Datacore query."""
        js = JS_QUERY.replace("{query}", query.replace("`", "\\`"))
        return await self._eval(js)
    
    async def fullquery(self, query: str, limit: int = 100) -> dict:
        """Run a full Datacore query with metadata."""
        js = JS_FULLQUERY.replace("{query}", query.replace("`", "\\`")).replace("{limit}", str(limit))
        return await self._eval(js)
    
    async def page(self, path: str) -> dict:
        """Get a specific page."""
        js = JS_PAGE.replace("{path}", path.replace("`", "\\`"))
        return await self._eval(js)
    
    async def evaluate(self, expression: str) -> dict:
        """Evaluate a Datacore expression."""
        js = JS_EVAL.replace("{expression}", expression.replace("`", "\\`"))
        return await self._eval(js)
    
    async def types(self) -> dict:
        """Get available query types."""
        return await self._eval(JS_TYPES)


async def async_main(args: Optional[list] = None):
    """Async main entry point."""
    parser = argparse.ArgumentParser(
        prog='obdev datacore',
        description='Datacore query commands'
    )
    parser.add_argument('--port', '-p', type=int, default=9222, help='CDP port')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # Check
    sub.add_parser('check', help='Check if Datacore is available')
    
    # Query
    p = sub.add_parser('query', help='Run a Datacore query')
    p.add_argument('query', help='Query string (e.g., "@page and #tag")')
    p.add_argument('--limit', '-l', type=int, default=100, help='Result limit')
    p.add_argument('--full', '-f', action='store_true', help='Include query metadata')
    
    # Page
    p = sub.add_parser('page', help='Get a specific page')
    p.add_argument('path', help='Page path')
    
    # Eval
    p = sub.add_parser('eval', help='Evaluate an expression')
    p.add_argument('expression', help='Expression to evaluate')
    
    # Types
    sub.add_parser('types', help='List available query types')
    
    # Examples
    sub.add_parser('examples', help='Show query examples')
    
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    # Handle examples without connecting
    if parsed.command == 'examples':
        examples = """
# Datacore Query Examples

## Basic Type Queries
@page                           # All pages
@section                        # All sections
@task                           # All tasks
@block                          # All blocks
@codeblock                      # All codeblocks

## Tag Queries
#project                        # Objects tagged #project
#book/fiction                   # Nested tags

## Combined Queries
@page and #game                 # Pages tagged #game
@task and $completed = false    # Incomplete tasks
@page and rating >= 9           # Pages with rating >= 9

## Path Queries
path("Projects")                # Objects in Projects folder

## Link Queries
connected([[Note]])             # Objects linking to/from Note
linksto([[Note]])               # Objects linking TO Note
linkedfrom([[Note]])            # Objects linking FROM Note

## Field Queries
exists(rating)                  # Objects with rating field
@section and $name = "Daily"    # Sections named "Daily"

## Parent/Child Queries
parentof(@codeblock)            # Parents of codeblocks
childof(@page)                  # Children of pages
subtree(@page)                  # Pages and all children

## Expression Queries
@page and $name.contains("2024")   # Pages with 2024 in name
rating > 7 and #game               # Games rated > 7
"""
        print(examples)
        return 0
    
    cli = DatacoreCLI(port=parsed.port)
    
    if not await cli.connect():
        print("Error: Cannot connect to Obsidian. Is it running with --remote-debugging-port?", 
              file=sys.stderr)
        return 1
    
    try:
        if parsed.command == 'check':
            result = await cli.check()
            if parsed.json:
                print(json.dumps(result, indent=2))
            elif result.get('available'):
                print(f"Datacore v{result.get('version')} is available")
            else:
                print("Datacore is not available")
        
        elif parsed.command == 'query':
            if parsed.full:
                result = await cli.fullquery(parsed.query, limit=parsed.limit)
            else:
                result = await cli.query(parsed.query)
            
            if 'error' in result:
                print(f"Error: {result['error']}", file=sys.stderr)
                return 1
            
            if parsed.json:
                print(json.dumps(result, indent=2))
            elif parsed.full:
                print(f"Query: {parsed.query}")
                print(f"Duration: {result.get('duration', 0):.2f}ms")
                print(f"Results: {result.get('count', 0)}")
                print()
                for r in result.get('results', []):
                    print(f"  [{r.get('type', '?')}] {r.get('path', r.get('id', '?'))}")
            else:
                for r in result if isinstance(result, list) else []:
                    path = r.get('path', r.get('id', '?'))
                    rtype = r.get('type', '?')
                    print(f"[{rtype}] {path}")
        
        elif parsed.command == 'page':
            result = await cli.page(parsed.path)
            
            if 'error' in result:
                print(f"Error: {result['error']}", file=sys.stderr)
                return 1
            
            if parsed.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Path: {result.get('path')}")
                print(f"Name: {result.get('name')}")
                if result.get('tags'):
                    print(f"Tags: {', '.join(result['tags'])}")
                if result.get('fields'):
                    print("Fields:")
                    for k, v in result['fields'].items():
                        print(f"  {k}: {v}")
                if result.get('sections'):
                    print("Sections:")
                    for s in result['sections']:
                        indent = '  ' * s.get('level', 1)
                        print(f"{indent}{s.get('title', '(untitled)')}")
        
        elif parsed.command == 'eval':
            result = await cli.evaluate(parsed.expression)
            
            if 'error' in result:
                print(f"Error: {result['error']}", file=sys.stderr)
                return 1
            
            if parsed.json:
                print(json.dumps(result, indent=2))
            else:
                print(result.get('result'))
        
        elif parsed.command == 'types':
            result = await cli.types()
            
            if parsed.json:
                print(json.dumps(result, indent=2))
            else:
                print("Available Query Types:")
                for t in result.get('types', []):
                    desc = result.get('description', {}).get(t, '')
                    print(f"  {t:<15} {desc}")
        
        return 0
        
    finally:
        await cli.close()


def main(args: Optional[list] = None):
    """Main entry point."""
    try:
        loop = asyncio.get_running_loop()
        # Already in an event loop, create task
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, async_main(args)).result()
    except RuntimeError:
        # No running loop, safe to use asyncio.run
        return asyncio.run(async_main(args))


if __name__ == '__main__':
    sys.exit(main())
