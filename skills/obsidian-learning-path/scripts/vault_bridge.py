#!/usr/bin/env python3
"""
Vault Bridge — Obsidian Ecosystem Adapter Layer
================================================
Provides a unified interface over three vault access methods:
  1. obsidian-cli (live Obsidian app — richest)
  2. ob (headless sync client)
  3. Direct file I/O (always available)

Auto-detects the best available method and cascades gracefully.

Cross-references:
  Uses: obsidian-cli skill, ob skill, obsidian-vault-manager skill
  Input: vault path or name
  Feeds: pkg_gkg_diff (PKG scan), compound_update (property writes),
         generate_vault (emit + sync), validate_vault (canvas verification)

Usage:
    # Probe available methods
    python vault_bridge.py probe --vault "Study Vault"

    # Scan PKG via best available method
    python vault_bridge.py scan --vault "Study Vault" --output pkg.json

    # Update mastery for a node
    python vault_bridge.py update --vault "Study Vault" --node "Fick Principle" \\
        --mastery 0.85 --status mastered

    # Sync vault (requires ob)
    python vault_bridge.py sync --vault "Study Vault"

    # Detect installed plugins
    python vault_bridge.py plugins --vault "Study Vault"
"""

import json
import subprocess
import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import date


# ─── Vault Manager Integration ────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
SKILLS_ROOT = SKILL_DIR.parent
VAULT_MANAGER_SCRIPTS = SKILLS_ROOT / 'obsidian-vault-manager' / 'scripts'
SKILLS_DATA = SKILLS_ROOT.parent / '.skills-data' / 'obsidian-learning-path'


def run(cmd: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def resolve_vault(vault_hint: Optional[str] = None) -> Path:
    """Resolve vault path using vault-manager registry, then fallbacks."""
    if vault_hint:
        # Try as direct path
        p = Path(vault_hint).expanduser()
        if (p / '.obsidian').exists():
            return p

        # Try via vault-manager registry
        registry_script = VAULT_MANAGER_SCRIPTS / 'vault_registry.py'
        if registry_script.exists():
            result = run(['python3', str(registry_script), 'get', '--name', vault_hint])
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return Path(data['path'])
                except (json.JSONDecodeError, KeyError):
                    pass

    # Try active vault from registry
    registry_script = VAULT_MANAGER_SCRIPTS / 'vault_registry.py'
    if registry_script.exists():
        result = run(['python3', str(registry_script), 'active'])
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return Path(data['path'])
            except (json.JSONDecodeError, KeyError):
                pass

    # Walk up from cwd
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / '.obsidian').exists():
            return parent

    raise FileNotFoundError("No vault found. Specify --vault or set active vault.")


# ─── Adapter Detection ────────────────────────────────────────────────────────

def obsidian_cli_available() -> bool:
    """Check if obsidian CLI is available and Obsidian is running."""
    try:
        result = run(['obsidian', 'eval', 'code=1'], timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def ob_configured(vault_path: Path) -> bool:
    """Check if ob (headless) is configured for this vault."""
    try:
        result = run(['ob', 'sync-status', '--path', str(vault_path)], timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


@dataclass
class ProbeResult:
    vault_path: str
    obsidian_cli: bool = False
    ob_headless: bool = False
    file_io: bool = True  # always available
    plugins: dict = field(default_factory=dict)
    best_method: str = "file_io"


def probe(vault_path: Path) -> ProbeResult:
    """Probe all available vault access methods."""
    result = ProbeResult(vault_path=str(vault_path))

    result.obsidian_cli = obsidian_cli_available()
    result.ob_headless = ob_configured(vault_path)

    if result.obsidian_cli:
        result.best_method = "obsidian_cli"
        result.plugins = detect_plugins_live()
    elif result.ob_headless:
        result.best_method = "ob_headless"
        result.plugins = detect_plugins_fs(vault_path)
    else:
        result.plugins = detect_plugins_fs(vault_path)

    return result


# ─── Plugin Detection ─────────────────────────────────────────────────────────

PLUGIN_PROBES = {
    'dataview': "!!app.plugins.plugins.dataview",
    'breadcrumbs': "!!app.plugins.plugins['breadcrumbs']",
    'bases': "!!app.plugins.plugins['bases']",
    'templater': "!!app.plugins.plugins['templater-obsidian']",
    'smart-connections': "!!app.plugins.plugins['smart-connections']",
}


def detect_plugins_live() -> dict[str, bool]:
    """Detect plugins via obsidian-cli eval."""
    results = {}
    for name, code in PLUGIN_PROBES.items():
        try:
            r = run(['obsidian', 'eval', f'code={code}'], timeout=5)
            results[name] = r.returncode == 0 and r.stdout.strip() == 'true'
        except:
            results[name] = False
    return results


def detect_plugins_fs(vault_path: Path) -> dict[str, bool]:
    """Detect plugins by checking .obsidian/plugins/ directory."""
    plugins_dir = vault_path / '.obsidian' / 'plugins'
    fs_names = {
        'dataview': 'dataview',
        'breadcrumbs': 'breadcrumbs',
        'bases': 'bases',
        'templater': 'templater-obsidian',
        'smart-connections': 'smart-connections',
    }
    return {name: (plugins_dir / fs_name).exists()
            for name, fs_name in fs_names.items()}


# ─── PKG Scanning ─────────────────────────────────────────────────────────────

def scan_pkg_dataview(vault_name: Optional[str] = None) -> list[dict]:
    """Scan PKG using Dataview DQL via obsidian-cli."""
    vault_arg = f'vault="{vault_name}" ' if vault_name else ''
    code = """
    const dv = app.plugins.plugins.dataview?.api;
    if (!dv) throw 'Dataview not available';
    const pages = dv.pages('#learning-path');
    JSON.stringify(pages.map(p => ({
        id: p.file.name,
        path: p.file.path,
        mastery: p.mastery ?? 0,
        difficulty: p.difficulty ?? 0.5,
        status: p.status ?? 'gap',
        level: p.level ?? 'L2',
        last_reviewed: p.last_reviewed?.toString() ?? null,
        next_review: p.next_review?.toString() ?? null,
        review_count: p.review_count ?? 0,
        open_question: p.open_question ?? '',
        tension_level: p.tension_level ?? 'medium',
        criticality: p.criticality ?? false
    })));
    """.strip()
    result = run(['obsidian', f'{vault_arg}eval', f'code={code}'], timeout=15)
    if result.returncode != 0:
        raise RuntimeError(f"Dataview scan failed: {result.stderr}")
    return json.loads(result.stdout)


def scan_pkg_files(vault_path: Path) -> list[dict]:
    """Scan PKG by parsing frontmatter from .md files."""
    import yaml
    pkg = []
    for md_file in vault_path.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8', errors='ignore')
        if not content.startswith('---'):
            continue
        end = content.find('---', 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(content[3:end])
        except:
            continue
        if not isinstance(fm, dict):
            continue
        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        if 'learning-path' not in tags:
            continue
        pkg.append({
            'id': md_file.stem,
            'path': str(md_file.relative_to(vault_path)),
            'mastery': fm.get('mastery', 0),
            'difficulty': fm.get('difficulty', 0.5),
            'status': fm.get('status', 'gap'),
            'level': fm.get('level', 'L2'),
            'last_reviewed': str(fm.get('last_reviewed', '')),
            'next_review': str(fm.get('next_review', '')),
            'review_count': fm.get('review_count', 0),
            'open_question': fm.get('open_question', ''),
            'tension_level': fm.get('tension_level', 'medium'),
            'criticality': fm.get('criticality', False),
        })
    return pkg


def scan_pkg(vault_path: Path, vault_name: Optional[str] = None) -> list[dict]:
    """Scan PKG using the best available method."""
    probe_result = probe(vault_path)

    if probe_result.obsidian_cli and probe_result.plugins.get('dataview'):
        try:
            return scan_pkg_dataview(vault_name)
        except RuntimeError:
            pass  # fall through

    return scan_pkg_files(vault_path)


# ─── Property Updates ──────────────────────────────────────────────────────────

def update_properties_cli(file_name: str, properties: dict,
                          vault_name: Optional[str] = None) -> bool:
    """Update note properties via obsidian-cli."""
    vault_arg = f'vault="{vault_name}" ' if vault_name else ''
    for key, value in properties.items():
        cmd = f'obsidian {vault_arg}property:set file="{file_name}" name="{key}" value="{value}" silent'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return False
    return True


def update_properties_file(vault_path: Path, file_name: str,
                           properties: dict) -> bool:
    """Update note properties by editing frontmatter directly."""
    import yaml
    # Find the file
    matches = list(vault_path.rglob(f'{file_name}.md'))
    if not matches:
        return False
    md_file = matches[0]

    content = md_file.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False
    end = content.find('---', 3)
    if end == -1:
        return False

    fm = yaml.safe_load(content[3:end]) or {}
    fm.update(properties)

    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
    new_content = f'---\n{new_fm}---{content[end + 3:]}'
    md_file.write_text(new_content, encoding='utf-8')
    return True


def update_node(vault_path: Path, node_name: str, properties: dict,
                vault_name: Optional[str] = None) -> bool:
    """Update a node's properties using best available method."""
    if obsidian_cli_available():
        if update_properties_cli(node_name, properties, vault_name):
            return True
    return update_properties_file(vault_path, node_name, properties)


# ─── Sync ──────────────────────────────────────────────────────────────────────

def sync_vault(vault_path: Path) -> bool:
    """Sync vault via ob if configured."""
    if not ob_configured(vault_path):
        print("ob not configured for this vault. Skipping sync.", file=sys.stderr)
        return False
    result = run(['ob', 'sync', '--path', str(vault_path)], timeout=120)
    return result.returncode == 0


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Vault Bridge — Obsidian adapter layer')
    parser.add_argument('command', choices=['probe', 'scan', 'update', 'sync', 'plugins'])
    parser.add_argument('--vault', help='Vault name or path')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--node', help='Node name (for update)')
    parser.add_argument('--mastery', type=float, help='Mastery value')
    parser.add_argument('--status', help='Status value')
    args = parser.parse_args()

    vault_path = resolve_vault(args.vault)

    if args.command == 'probe':
        result = probe(vault_path)
        print(json.dumps(asdict(result), indent=2))

    elif args.command == 'scan':
        pkg = scan_pkg(vault_path, args.vault)
        output = json.dumps(pkg, indent=2)
        if args.output:
            Path(args.output).write_text(output)
            print(f"PKG written to {args.output} ({len(pkg)} nodes)")
        else:
            print(output)

    elif args.command == 'update':
        if not args.node:
            parser.error("--node required for update")
        props = {}
        if args.mastery is not None:
            props['mastery'] = args.mastery
        if args.status:
            props['status'] = args.status
        props['last_reviewed'] = date.today().isoformat()
        success = update_node(vault_path, args.node, props, args.vault)
        print("Updated" if success else "Failed", args.node)

    elif args.command == 'sync':
        success = sync_vault(vault_path)
        print("Synced" if success else "Sync failed or not configured")

    elif args.command == 'plugins':
        result = probe(vault_path)
        print(json.dumps(result.plugins, indent=2))


if __name__ == '__main__':
    main()
