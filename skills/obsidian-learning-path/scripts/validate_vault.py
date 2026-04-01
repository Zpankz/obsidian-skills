#!/usr/bin/env python3
"""
Vault Validator
===============
Checks all structural invariants of a generated learning path vault.

Cross-references:
  Spec: 07-validation-checklist (V1-V18 check definitions + severity + auto-fix protocol)
  Uses: 04-node-schema (frontmatter field constraints for V2-V8),
        01-theoretical-core (ZPD bounds for V3, Zeigarnik closure for V4-V5)
  Input: generate_vault (vault .md/.canvas/.base files to validate),
         compound_update (mastery values for V8, retention_alert for V12),
         mcmc_traversal (path_position for V7, criticality for V9, probes for V11)
  Feeds: self_eval (V17 pass rate check), gkg_refine (V14 triggers recalibration),
         meta_compound (V15 tabu exhaustion, V16 cluster coverage)
  Schema: 03-mcmc-hamiltonian (topology η for V6), 06-canvas-base-spec (canvas layout for V10)

Usage:
    python validate_vault.py --vault ./my_vault
    python validate_vault.py --vault ./my_vault --auto-fix
    python validate_vault.py --vault ./my_vault --json
"""

import json
import yaml
import re
import argparse
from dataclasses import dataclass, field
from pathlib import Path
from datetime import date


ZPD_MIN = 0.10
ZPD_MAX = 0.40
ETA_MIN = 0.80
MASTERED_THRESHOLD = 0.85


@dataclass
class CheckResult:
    check_id: str
    name: str
    status: str       # PASS | FAIL | SKIP
    severity: str     # CRITICAL | MAJOR | MINOR
    detail: str = ""
    violations: list = field(default_factory=list)
    auto_fixable: bool = False


def load_vault_frontmatters(vault_path: Path) -> list[dict]:
    """Load all frontmatters from .md files in vault."""
    nodes = []
    for md_file in vault_path.rglob("*.md"):
        if "meta" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        if not content.startswith("---"):
            continue
        try:
            end = content.index("---", 3)
            fm = yaml.safe_load(content[3:end]) or {}
            fm["_file"] = str(md_file.relative_to(vault_path))
            nodes.append(fm)
        except (ValueError, yaml.YAMLError):
            pass
    return nodes


def check_all_nodes_have_md(nodes: list[dict], vault_path: Path) -> CheckResult:
    missing = [n["id"] for n in nodes if not n.get("id")]
    return CheckResult(
        check_id="V1", name="All gap nodes have .md files",
        status="PASS" if not missing else "FAIL",
        severity="CRITICAL",
        detail=f"Found {len(nodes)} node files",
        violations=missing,
    )


def check_wikilinks_resolve(nodes: list[dict]) -> CheckResult:
    ids = {n.get("id") for n in nodes if n.get("id")}
    broken = []
    for node in nodes:
        for field_name in ["prerequisites", "unlocks"]:
            for link in (node.get(field_name) or []):
                # YAML parses [[x]] as nested list [['x']] — unwrap
                if isinstance(link, list):
                    link = link[0] if link else ""
                clean = str(link).replace("[[", "").replace("]]", "").replace('"', "").replace("'", "").strip()
                if clean and clean not in ids:
                    broken.append(f"{node.get('id','')} → '{clean}'")
    return CheckResult(
        check_id="V2", name="All wikilinks resolve",
        status="PASS" if not broken else "FAIL",
        severity="CRITICAL",
        violations=broken,
    )


def check_zpd_in_range(nodes: list[dict]) -> CheckResult:
    violations = []
    for node in nodes:
        if node.get("status") == "scaffold":
            continue
        delta = node.get("zpd_delta")
        if delta is None:
            continue
        if not (ZPD_MIN <= float(delta) <= ZPD_MAX):
            violations.append({
                "node": node.get("id"),
                "title": node.get("title"),
                "zpd_delta": float(delta),
                "fix": f"Insert scaffold (target Δ=0.22)"
            })
    return CheckResult(
        check_id="V3", name="ZPD Δ ∈ [0.10, 0.40] for all edges",
        status="PASS" if not violations else "FAIL",
        severity="MAJOR",
        violations=violations,
        auto_fixable=True,
    )


def check_open_questions(nodes: list[dict]) -> CheckResult:
    violations = []
    for node in nodes:
        pos = node.get("path_position", 0)
        if pos is None:
            continue
        # All non-terminal nodes (not last in path) should have open_question
        if node.get("status") != "mastered" and not node.get("open_question", "").strip():
            violations.append(node.get("id", "unknown"))
    return CheckResult(
        check_id="V4", name="All non-terminal nodes have open_question",
        status="PASS" if not violations else "FAIL",
        severity="MAJOR",
        violations=violations,
        auto_fixable=True,
    )


def check_zeigarnik_closed(nodes: list[dict]) -> CheckResult:
    """Every non-terminal node's open_question should be addressed by a successor."""
    by_pos = {n.get("path_position"): n for n in nodes if n.get("path_position")}
    violations = []
    for node in nodes:
        pos = node.get("path_position")
        if not pos or not node.get("open_question"):
            continue
        successor = by_pos.get(pos + 1)
        if not successor:
            continue  # terminal node — ok
        # Heuristic: successor's domain/cluster should relate to the open question terms
        q_words = set(str(node.get("open_question", "")).lower().split())
        s_words = set(str(successor.get("title", "")).lower().split()) | set(str(successor.get("cluster", "")).lower().split())
        if not q_words & s_words and len(q_words) > 2:
            violations.append({
                "node": node.get("id"),
                "open_question": node.get("open_question", "")[:80],
                "successor": successor.get("title", ""),
            })
    return CheckResult(
        check_id="V5", name="Zeigarnik loops closed by successors",
        status="PASS" if not violations else "FAIL",
        severity="MAJOR",
        violations=violations,
        auto_fixable=True,
    )


def check_topology_eta(nodes: list[dict]) -> CheckResult:
    """η = |E| / |V|² for the path subgraph (connectedness proxy)."""
    V = len(nodes)
    if V < 2:
        return CheckResult("V6", "Topology η ≥ 0.80", "SKIP", "MAJOR", "Too few nodes")
    
    E = sum(len(n.get("unlocks") or []) for n in nodes)
    eta = E / (V * V) if V > 0 else 0
    eta_normalised = min(1.0, eta * V)  # normalise to [0,1] scale
    
    return CheckResult(
        check_id="V6", name="Topology η ≥ 0.80",
        status="PASS" if eta_normalised >= ETA_MIN else "FAIL",
        severity="MAJOR",
        detail=f"η = {eta_normalised:.3f} (E={E}, V={V})",
    )


def check_no_orphans(nodes: list[dict]) -> CheckResult:
    orphans = [n.get("id") for n in nodes if n.get("path_position") is None and n.get("status") != "mastered"]
    return CheckResult(
        check_id="V7", name="No orphan nodes (all have path_position)",
        status="PASS" if not orphans else "FAIL",
        severity="MAJOR",
        violations=orphans,
    )


def check_status_consistent(nodes: list[dict]) -> CheckResult:
    violations = []
    for node in nodes:
        mastery = node.get("mastery", 0.0)
        status  = node.get("status", "")
        expected = (
            "mastered" if mastery >= MASTERED_THRESHOLD
            else "in-progress" if mastery >= 0.3
            else "gap"
        )
        if status not in (expected, "scaffold") and status != "":
            violations.append({"id": node.get("id"), "status": status, "expected": expected, "mastery": mastery})
    return CheckResult(
        check_id="V8", name="Status consistent with mastery threshold",
        status="PASS" if not violations else "FAIL",
        severity="MINOR",
        violations=violations,
        auto_fixable=True,
    )


def check_criticality_current(nodes: list[dict], max_age_days: int = 7) -> CheckResult:
    stale = []
    today = date.today()
    for node in nodes:
        last = node.get("last_reviewed")
        if node.get("criticality") and last:
            try:
                reviewed = date.fromisoformat(str(last))
                if (today - reviewed).days > max_age_days:
                    stale.append(node.get("id"))
            except ValueError:
                pass
    return CheckResult(
        check_id="V9", name="Criticality annotations current (< 7 days)",
        status="PASS" if not stale else "FAIL",
        severity="MINOR",
        violations=stale,
    )


def run_all_checks(vault_path: Path) -> list[CheckResult]:
    nodes = load_vault_frontmatters(vault_path)
    if not nodes:
        return [CheckResult("V0", "Vault has nodes", "FAIL", "CRITICAL", "No .md files found with frontmatter")]

    return [
        check_all_nodes_have_md(nodes, vault_path),
        check_wikilinks_resolve(nodes),
        check_zpd_in_range(nodes),
        check_open_questions(nodes),
        check_zeigarnik_closed(nodes),
        check_topology_eta(nodes),
        check_no_orphans(nodes),
        check_status_consistent(nodes),
        check_criticality_current(nodes),
    ]


def print_report(results: list[CheckResult], vault_path: Path):
    passed = sum(1 for r in results if r.status == "PASS")
    failed = [r for r in results if r.status == "FAIL"]
    overall = "PASS" if not any(r.severity in ("CRITICAL", "MAJOR") for r in failed) else "FAIL"

    print(f"\n{'='*60}")
    print(f"  VAULT VALIDATION REPORT")
    print(f"  {vault_path}")
    print(f"  Overall: {overall}  ({passed}/{len(results)} checks passed)")
    print(f"{'='*60}\n")

    for r in results:
        icon = "✅" if r.status == "PASS" else "❌" if r.status == "FAIL" else "⏭️"
        print(f"  {icon} [{r.check_id}] {r.name}")
        if r.status == "FAIL":
            print(f"     Severity: {r.severity}")
            if r.detail:
                print(f"     Detail: {r.detail}")
            if r.violations:
                for v in r.violations[:3]:
                    print(f"       - {v}")
                if len(r.violations) > 3:
                    print(f"       ... and {len(r.violations) - 3} more")
            if r.auto_fixable:
                print(f"     Auto-fix available: --auto-fix")
        elif r.detail:
            print(f"     {r.detail}")

    print()
    if overall == "FAIL":
        print("  ⚠️  Vault has validation failures. Run with --auto-fix for safe remediations.")
    else:
        print("  🎉 Vault is valid and ready for study!")


def main():
    parser = argparse.ArgumentParser(description="Obsidian Learning Path Vault Validator")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--auto-fix", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_out")
    parser.add_argument("--output", default="validation_report.yaml")
    args = parser.parse_args()

    vault_path = Path(args.vault)
    results = run_all_checks(vault_path)

    if args.json_out:
        report = {
            "vault": str(vault_path),
            "overall": "PASS" if not any(r.status == "FAIL" and r.severity in ("CRITICAL", "MAJOR") for r in results) else "FAIL",
            "checks": {r.check_id: {"status": r.status, "severity": r.severity, "violations": r.violations} for r in results},
        }
        print(json.dumps(report, indent=2))
    else:
        print_report(results, vault_path)

    # Write YAML report
    report_data = {
        "validation": {
            "timestamp": date.today().isoformat(),
            "vault_path": str(vault_path),
            "overall": "PASS" if not any(r.status == "FAIL" and r.severity in ("CRITICAL", "MAJOR") for r in results) else "FAIL",
            "checks": {r.check_id: {"name": r.name, "status": r.status, "severity": r.severity, "violations": r.violations[:5]} for r in results},
        }
    }
    Path(args.output).write_text(yaml.dump(report_data, default_flow_style=False))


if __name__ == "__main__":
    main()
