#!/usr/bin/env python3
"""
generate_systemd_service.py
Generate a systemd unit file for running `ob sync --continuous` as a service.

Usage:
  python scripts/generate_systemd_service.py \
    --vault-path /path/to/vault \
    [--user username] \
    [--mode pull-only|bidirectional|mirror-remote] \
    [--output /etc/systemd/system/ob-sync.service]
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


UNIT_TEMPLATE = """\
[Unit]
Description=Obsidian Headless Sync — {vault_name}
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=3

[Service]
Type=simple
User={user}
Environment="PATH={node_bin}:{path}"
ExecStartPre={ob_path} sync-status --path {vault_path}
ExecStart={ob_path} sync --continuous --path {vault_path}
Restart=on-failure
RestartSec=15
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ob-sync-{vault_slug}

[Install]
WantedBy=multi-user.target
"""


def find_ob() -> str:
    ob = shutil.which("ob")
    if not ob:
        print("Error: `ob` not found in PATH. Install with: npm install -g obsidian-headless")
        sys.exit(1)
    return ob


def get_node_bin() -> str:
    result = subprocess.run(
        ["node", "-e", "process.stdout.write(process.execPath)"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return str(Path(result.stdout).parent)
    return "/usr/local/bin"


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-").strip("-")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a systemd unit file for ob sync --continuous"
    )
    parser.add_argument("--vault-path", required=True, help="Absolute path to vault directory")
    parser.add_argument(
        "--user",
        default=os.getenv("USER", "obsidian"),
        help="System user to run the service as (default: current user)",
    )
    parser.add_argument(
        "--mode",
        choices=["pull-only", "bidirectional", "mirror-remote"],
        default="pull-only",
        help="Sync mode to configure before starting (default: pull-only — recommended for servers)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path for unit file (prints to stdout if omitted)",
    )
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    vault_name = vault_path.name
    vault_slug = slugify(vault_name)

    ob_path = find_ob()
    node_bin = get_node_bin()
    current_path = os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")

    # Warn about bidirectional mode
    if args.mode != "pull-only":
        print(
            f"⚠ Warning: mode '{args.mode}' selected. On headless servers, 'pull-only' is "
            "recommended to avoid the bidirectional oscillation bug (issue #15).",
            file=sys.stderr,
        )

    unit = UNIT_TEMPLATE.format(
        vault_name=vault_name,
        vault_slug=vault_slug,
        vault_path=str(vault_path),
        user=args.user,
        ob_path=ob_path,
        node_bin=node_bin,
        path=current_path,
    )

    service_name = f"ob-sync-{vault_slug}.service"

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(unit)
        print(f"✓ Unit file written to: {out_path}")
        print()
        print("Next steps:")
        print("  sudo systemctl daemon-reload")
        print(f"  sudo systemctl enable --now {out_path.name}")
        print(f"  journalctl -fu {out_path.stem}")
    else:
        print(unit)
        print(f"# ── Installation ──────────────────────────────")
        print(f"# sudo cp <above> /etc/systemd/system/{service_name}")
        print("# sudo systemctl daemon-reload")
        print(f"# sudo systemctl enable --now {service_name}")
        print(f"# journalctl -fu ob-sync-{vault_slug}")


if __name__ == "__main__":
    main()