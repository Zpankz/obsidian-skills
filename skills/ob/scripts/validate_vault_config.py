#!/usr/bin/env python3
"""
validate_vault_config.py
Check whether a vault directory is properly configured for ob sync or ob publish.

Usage:
  python scripts/validate_vault_config.py [--path /path/to/vault] [--type sync|publish|both]
"""
import subprocess
import sys
import argparse
from pathlib import Path


def run(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_sync_config(vault_path: Path) -> dict:
    code, out, err = run(["ob", "sync-status", "--path", str(vault_path)])
    if code != 0:
        return {
            "ok": False,
            "error": f"Vault not configured for sync at {vault_path}",
            "fix": f"ob sync-setup --vault <name> --path {vault_path}",
        }
    return {"ok": True, "status": out}


def check_publish_config(vault_path: Path) -> dict:
    code, out, err = run(["ob", "publish-config", "--path", str(vault_path)])
    if code != 0:
        return {
            "ok": False,
            "error": f"Vault not configured for publish at {vault_path}",
            "fix": f"ob publish-setup --site <slug> --path {vault_path}",
        }
    return {"ok": True, "config": out}


def main():
    parser = argparse.ArgumentParser(description="Validate ob vault configuration")
    parser.add_argument("--path", default=".", help="Vault directory path (default: cwd)")
    parser.add_argument(
        "--type",
        choices=["sync", "publish", "both"],
        default="sync",
        help="What to validate (default: sync)",
    )
    args = parser.parse_args()

    vault_path = Path(args.path).resolve()
    print(f"Validating vault: {vault_path}")
    print()

    if not vault_path.exists():
        print(f"✗ Directory does not exist: {vault_path}")
        sys.exit(1)

    checks: dict[str, dict] = {}

    if args.type in ("sync", "both"):
        print("Checking sync configuration...")
        checks["sync"] = check_sync_config(vault_path)
        if checks["sync"]["ok"]:
            print("  ✓ Sync configured")
            for line in checks["sync"]["status"].splitlines():
                print(f"    {line}")
        else:
            print(f"  ✗ {checks['sync']['error']}")
            print(f"    Fix: {checks['sync']['fix']}")

    if args.type in ("publish", "both"):
        print("Checking publish configuration...")
        checks["publish"] = check_publish_config(vault_path)
        if checks["publish"]["ok"]:
            print("  ✓ Publish configured")
            for line in checks["publish"]["config"].splitlines():
                print(f"    {line}")
        else:
            print(f"  ✗ {checks['publish']['error']}")
            print(f"    Fix: {checks['publish']['fix']}")

    print()
    all_ok = all(v["ok"] for v in checks.values())
    if all_ok:
        print("✓ Vault configuration valid.")
        sys.exit(0)
    else:
        print("✗ Vault configuration incomplete. See fixes above.")
        sys.exit(1)


if __name__ == "__main__":
    main()