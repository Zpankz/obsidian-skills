"""
Bases CLI - Obsidian Bases syntax and database views.

Based on: https://help.obsidian.md/bases/syntax
Bases is Obsidian's built-in database feature for creating views of vault data.

This module provides utilities for creating and managing bases (database views).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# Bases Syntax Reference
# https://help.obsidian.md/bases/syntax
# ============================================================

BASES_SYNTAX_HELP = """
# Obsidian Bases Syntax Reference

## Basic Structure
A base is a code block with the `base` language identifier:

```base
filter: ...
view: table | list | ...
fields: [field1, field2, ...]
```

## Filters (WHERE clause)
Filter which notes appear in the view.

### Path filters
- `path("folder")` - notes in folder
- `path("folder/")` - notes in folder and subfolders
- `path("note.md")` - specific note

### Tag filters
- `#tag` - notes with tag
- `#tag/nested` - notes with nested tag
- `-#tag` - notes without tag

### Property filters
- `property = value` - exact match
- `property != value` - not equal
- `property > value` - greater than (numbers/dates)
- `property < value` - less than
- `property >= value` - greater or equal
- `property <= value` - less or equal
- `property contains "text"` - contains substring
- `property exists` - property exists
- `property not exists` - property doesn't exist
- `property = empty` - property is empty
- `property != empty` - property is not empty

### Date filters
- `date = today` - today
- `date = yesterday` - yesterday
- `date = tomorrow` - tomorrow
- `date > 2024-01-01` - after date
- `date = this week` - current week
- `date = last week` - previous week
- `date = next week` - next week

### Logical operators
- `filter1 AND filter2` - both conditions
- `filter1 OR filter2` - either condition
- `NOT filter` - negation
- `(filter1 OR filter2) AND filter3` - grouping

## Views
- `table` - tabular view (default)
- `list` - simple list
- `cards` - card grid
- `calendar` - calendar view (requires date field)

## Fields
Specify which properties to show:
```base
fields: [name, created, tags, status]
```

### Special fields
- `name` - note name/title
- `path` - full path
- `folder` - containing folder
- `created` - creation date
- `modified` - modification date
- `tags` - all tags
- `links` - outgoing links
- `backlinks` - incoming links

### Field options
```base
fields:
  - name
  - { field: status, label: "Status" }
  - { field: priority, sort: desc }
```

## Sorting
```base
sort: created desc
sort: [status asc, created desc]
```

## Grouping
```base
group: status
group: folder
```

## Formulas (computed fields)
```base
fields:
  - { formula: "length(tags)", label: "Tag Count" }
  - { formula: "format(modified, 'YYYY-MM-DD')", label: "Last Edit" }
```

### Formula functions
- `length(list)` - count items
- `sum(numbers)` - sum values
- `avg(numbers)` - average
- `min(values)` - minimum
- `max(values)` - maximum
- `format(date, pattern)` - format date
- `concat(a, b)` - join strings
- `if(condition, then, else)` - conditional

## Summaries
Aggregate data at the bottom of tables:
```base
summary:
  - { field: price, function: sum }
  - { field: count, function: avg }
```

Summary functions: `sum`, `avg`, `min`, `max`, `count`

## Examples

### Task list
```base
filter: #task AND status != "done"
view: table
fields: [name, due, priority, status]
sort: due asc
```

### Project overview
```base
filter: path("Projects/")
view: cards
fields: [name, status, tags]
group: status
```

### Recent notes
```base
filter: modified > last week
view: list
sort: modified desc
```

### Calendar of events
```base
filter: #event
view: calendar
fields: [name, date, location]
```
"""


class BasesGenerator:
    """Generate Obsidian Bases (database view) code blocks."""
    
    def __init__(self):
        self.config = {}
    
    def filter(self, filter_expr: str) -> 'BasesGenerator':
        """Set the filter expression."""
        self.config['filter'] = filter_expr
        return self
    
    def view(self, view_type: str) -> 'BasesGenerator':
        """Set the view type (table, list, cards, calendar)."""
        self.config['view'] = view_type
        return self
    
    def fields(self, fields: List[Any]) -> 'BasesGenerator':
        """Set the fields to display."""
        self.config['fields'] = fields
        return self
    
    def sort(self, sort_spec: str) -> 'BasesGenerator':
        """Set the sort order."""
        self.config['sort'] = sort_spec
        return self
    
    def group(self, group_by: str) -> 'BasesGenerator':
        """Set the grouping field."""
        self.config['group'] = group_by
        return self
    
    def summary(self, summaries: List[dict]) -> 'BasesGenerator':
        """Set summary aggregations."""
        self.config['summary'] = summaries
        return self
    
    def generate(self) -> str:
        """Generate the base code block."""
        lines = []
        
        if 'filter' in self.config:
            lines.append(f"filter: {self.config['filter']}")
        
        if 'view' in self.config:
            lines.append(f"view: {self.config['view']}")
        
        if 'fields' in self.config:
            fields = self.config['fields']
            if all(isinstance(f, str) for f in fields):
                lines.append(f"fields: [{', '.join(fields)}]")
            else:
                lines.append("fields:")
                for f in fields:
                    if isinstance(f, str):
                        lines.append(f"  - {f}")
                    else:
                        lines.append(f"  - {json.dumps(f)}")
        
        if 'sort' in self.config:
            lines.append(f"sort: {self.config['sort']}")
        
        if 'group' in self.config:
            lines.append(f"group: {self.config['group']}")
        
        if 'summary' in self.config:
            lines.append("summary:")
            for s in self.config['summary']:
                lines.append(f"  - {json.dumps(s)}")
        
        content = '\n'.join(lines)
        return f"```base\n{content}\n```"
    
    def reset(self) -> 'BasesGenerator':
        """Reset configuration."""
        self.config = {}
        return self


def generate_task_list(status_filter: Optional[str] = None) -> str:
    """Generate a task list base."""
    gen = BasesGenerator()
    
    filter_parts = ['#task']
    if status_filter:
        filter_parts.append(f'status = "{status_filter}"')
    else:
        filter_parts.append('status != "done"')
    
    return (gen
        .filter(' AND '.join(filter_parts))
        .view('table')
        .fields(['name', 'due', 'priority', 'status'])
        .sort('due asc')
        .generate())


def generate_project_overview(folder: str = "Projects") -> str:
    """Generate a project overview base."""
    return (BasesGenerator()
        .filter(f'path("{folder}/")')
        .view('cards')
        .fields(['name', 'status', 'tags', 'modified'])
        .group('status')
        .generate())


def generate_recent_notes(days: int = 7) -> str:
    """Generate a recent notes base."""
    period = "last week" if days == 7 else f"last {days} days"
    return (BasesGenerator()
        .filter(f'modified > {period}')
        .view('list')
        .sort('modified desc')
        .generate())


def generate_calendar(tag: str = "event") -> str:
    """Generate a calendar view base."""
    return (BasesGenerator()
        .filter(f'#{tag}')
        .view('calendar')
        .fields(['name', 'date', 'location'])
        .generate())


def generate_tag_query(tag: str, view_type: str = "table") -> str:
    """Generate a base for notes with a specific tag."""
    return (BasesGenerator()
        .filter(f'#{tag}')
        .view(view_type)
        .fields(['name', 'created', 'modified', 'tags'])
        .sort('modified desc')
        .generate())


def generate_folder_view(folder: str, view_type: str = "table") -> str:
    """Generate a base for notes in a folder."""
    return (BasesGenerator()
        .filter(f'path("{folder}/")')
        .view(view_type)
        .fields(['name', 'created', 'modified'])
        .sort('name asc')
        .generate())


def generate_custom(
    filter_expr: str,
    view_type: str = "table",
    fields: Optional[List[str]] = None,
    sort_by: Optional[str] = None,
    group_by: Optional[str] = None
) -> str:
    """Generate a custom base."""
    gen = BasesGenerator().filter(filter_expr).view(view_type)
    
    if fields:
        gen.fields(fields)
    
    if sort_by:
        gen.sort(sort_by)
    
    if group_by:
        gen.group(group_by)
    
    return gen.generate()


# Templates for common use cases
TEMPLATES = {
    'tasks': {
        'filter': '#task AND status != "done"',
        'view': 'table',
        'fields': ['name', 'due', 'priority', 'status'],
        'sort': 'due asc'
    },
    'projects': {
        'filter': 'path("Projects/")',
        'view': 'cards', 
        'fields': ['name', 'status', 'tags'],
        'group': 'status'
    },
    'recent': {
        'filter': 'modified > last week',
        'view': 'list',
        'sort': 'modified desc'
    },
    'daily': {
        'filter': 'path("Daily/")',
        'view': 'list',
        'sort': 'created desc'
    },
    'calendar': {
        'filter': '#event',
        'view': 'calendar',
        'fields': ['name', 'date', 'location']
    },
    'meetings': {
        'filter': '#meeting',
        'view': 'table',
        'fields': ['name', 'date', 'attendees', 'status'],
        'sort': 'date desc'
    },
    'reading': {
        'filter': '#book OR #article',
        'view': 'table',
        'fields': ['name', 'author', 'status', 'rating'],
        'group': 'status'
    }
}


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for bases commands."""
    parser = argparse.ArgumentParser(
        prog='obdev bases',
        description='Obsidian Bases syntax generator and reference'
    )
    
    sub = parser.add_subparsers(dest='command', help='Command')
    
    # Help/reference
    sub.add_parser('help', aliases=['syntax'], help='Show Bases syntax reference')
    
    # Generate from template
    p = sub.add_parser('template', aliases=['t'], help='Generate from template')
    p.add_argument('name', choices=list(TEMPLATES.keys()), help='Template name')
    p.add_argument('--output', '-o', help='Output file (creates .md note with base)')
    
    # List templates
    sub.add_parser('templates', aliases=['list'], help='List available templates')
    
    # Generate tasks
    p = sub.add_parser('tasks', help='Generate task list base')
    p.add_argument('--status', '-s', help='Filter by status')
    
    # Generate projects
    p = sub.add_parser('projects', help='Generate project overview')
    p.add_argument('--folder', '-f', default='Projects', help='Projects folder')
    
    # Generate recent
    p = sub.add_parser('recent', help='Generate recent notes view')
    p.add_argument('--days', '-d', type=int, default=7, help='Days to look back')
    
    # Generate calendar
    p = sub.add_parser('calendar', help='Generate calendar view')
    p.add_argument('--tag', '-t', default='event', help='Event tag')
    
    # Generate tag query
    p = sub.add_parser('tag', help='Generate tag query')
    p.add_argument('tag_name', help='Tag to query (without #)')
    p.add_argument('--view', '-v', default='table', choices=['table', 'list', 'cards'])
    
    # Generate folder view
    p = sub.add_parser('folder', help='Generate folder view')
    p.add_argument('folder_path', help='Folder path')
    p.add_argument('--view', '-v', default='table', choices=['table', 'list', 'cards'])
    
    # Custom generation
    p = sub.add_parser('custom', help='Generate custom base')
    p.add_argument('--filter', '-f', required=True, help='Filter expression')
    p.add_argument('--view', '-v', default='table', help='View type')
    p.add_argument('--fields', nargs='+', help='Fields to display')
    p.add_argument('--sort', '-s', help='Sort specification')
    p.add_argument('--group', '-g', help='Group by field')
    
    # Interactive builder
    sub.add_parser('builder', aliases=['build'], help='Interactive base builder')
    
    return parser


def main(args: Optional[list] = None):
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)
    
    if not parsed.command:
        parser.print_help()
        return 1
    
    output = None
    
    if parsed.command in ('help', 'syntax'):
        print(BASES_SYNTAX_HELP)
        return 0
    
    elif parsed.command in ('templates', 'list'):
        print("Available templates:")
        for name, config in TEMPLATES.items():
            view = config.get('view', 'table')
            filter_preview = config.get('filter', '')[:40]
            print(f"  {name:12} - {view:8} | {filter_preview}...")
        return 0
    
    elif parsed.command in ('template', 't'):
        template = TEMPLATES[parsed.name]
        gen = BasesGenerator()
        gen.config = template.copy()
        output = gen.generate()
        
        if parsed.output:
            Path(parsed.output).write_text(f"# {parsed.name.title()}\n\n{output}\n")
            print(f"Created: {parsed.output}")
            return 0
    
    elif parsed.command == 'tasks':
        output = generate_task_list(parsed.status)
    
    elif parsed.command == 'projects':
        output = generate_project_overview(parsed.folder)
    
    elif parsed.command == 'recent':
        output = generate_recent_notes(parsed.days)
    
    elif parsed.command == 'calendar':
        output = generate_calendar(parsed.tag)
    
    elif parsed.command == 'tag':
        output = generate_tag_query(parsed.tag_name, parsed.view)
    
    elif parsed.command == 'folder':
        output = generate_folder_view(parsed.folder_path, parsed.view)
    
    elif parsed.command == 'custom':
        output = generate_custom(
            filter_expr=parsed.filter,
            view_type=parsed.view,
            fields=parsed.fields,
            sort_by=parsed.sort,
            group_by=parsed.group
        )
    
    elif parsed.command in ('builder', 'build'):
        # Interactive builder
        print("Bases Interactive Builder")
        print("=" * 40)
        
        gen = BasesGenerator()
        
        filter_expr = input("Filter expression (e.g., #tag, path('folder'), property = value): ").strip()
        if filter_expr:
            gen.filter(filter_expr)
        
        view = input("View type [table/list/cards/calendar] (default: table): ").strip() or 'table'
        gen.view(view)
        
        fields_str = input("Fields (comma-separated, or leave empty): ").strip()
        if fields_str:
            fields = [f.strip() for f in fields_str.split(',')]
            gen.fields(fields)
        
        sort_str = input("Sort by (e.g., 'created desc'): ").strip()
        if sort_str:
            gen.sort(sort_str)
        
        group_str = input("Group by (field name): ").strip()
        if group_str:
            gen.group(group_str)
        
        print("\n" + "=" * 40)
        output = gen.generate()
    
    if output:
        print(output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
