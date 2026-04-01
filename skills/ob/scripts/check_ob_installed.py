#!/usr/bin/env python3
"""
check_ob_installed.py
Verify that the `ob` CLI (obsidian-headless) is installed, accessible,
and that the user is authenticated. Prints a structured status report.

Usage: python scripts/check_ob_installed.py
"""
import subprocess
import sys


def run(cmd: list[str]) -> tuple[int, str, str]:
    """Run a command, return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_node() -> dict:
    code, out, err = run(["node", "--version"])
    if code != 0:
        return {"ok": False, "error": "Node.js not found. Install Node.js ≥22."}
    version = out.lstrip("v")
    major = int(version.split(".")[0])
    if major < 22:
        return {
            "ok": False,
            "error": f"Node.js {version} found but ≥22 required. Run: nvm install 22",
        }
    return {"ok": True, "version": version}


def check_ob() -> dict:
    code, out, err = run(["ob", "--version"])
    if code != 0:
        return {
            "ok": False,
            "error": "ob not found in PATH. Run: npm install -g obsidian-headless",
        }
    return {"ok": True, "version": out}


def check_auth() -> dict:
    # `ob login` with no args: shows account info if logged in, prompts if not.
    # In non-interactive context it will fail if not logged in.
    code, out, err = run(["ob", "login"])
    # ob login exits 0 and prints account info if already authenticated
    if code != 0:
        return {
            "ok": False,
            "error": "Not authenticated. Run: ob login",
            "hint": err or out,
        }
    return {"ok": True, "info": out}


def main():
    checks: dict[str, dict] = {}

    print("── ob CLI preflight check ──────────────────")

    print("\n[1/3] Node.js")
    checks["node"] = check_node()
    if checks["node"]["ok"]:
        print(f"  ✓ Node.js {checks['node']['version']}")
    else:
        print(f"  ✗ {checks['node']['error']}")

    print("\n[2/3] ob CLI")
    checks["ob"] = check_ob()
    if checks["ob"]["ok"]:
        print(f"  ✓ ob {checks['ob']['version']}")
    else:
        print(f"  ✗ {checks['ob']['error']}")

    if checks["ob"]["ok"]:
        print("\n[3/3] Authentication")
        checks["auth"] = check_auth()
        if checks["auth"]["ok"]:
            print("  ✓ Authenticated")
            if checks["auth"].get("info"):
                for line in checks["auth"]["info"].splitlines():
                    print(f"    {line}")
        else:
            print(f"  ✗ {checks['auth']['error']}")
            if checks["auth"].get("hint"):
                print(f"    {checks['auth']['hint']}")

    print()
    all_ok = all(v["ok"] for v in checks.values())
    if all_ok:
        print("✓ All checks passed. ob is ready to use.")
        sys.exit(0)
    else:
        print("✗ Some checks failed. Fix the issues above before running ob.")
        sys.exit(1)


if __name__ == "__main__":
    main()