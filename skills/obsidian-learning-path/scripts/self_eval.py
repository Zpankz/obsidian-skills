#!/usr/bin/env python3
"""
Self-Eval v3 — Architectural Introspection
============================================
Tests the skill's actual architecture against itself. No synthetic data.

Introspects:
  1. SKILL.md ↔ filesystem (every referenced file exists)
  2. Scripts ↔ node schema (every written field exists in schema)
  3. MECHANISM_REGISTRY ↔ BCME search law (axes match theory)
  4. PLATEAU_TYPES ↔ classify_plateau (ALL 7 types detectable)
  5. Routing table ↔ scripts (every command has implementation)
  6. F/G/N tags ↔ implementations (every finding has code)
  7. Cross-references between reference files
  8. Backward compatibility (legacy session format still accepted)
  9. Parameter governance (all tunables have bounds)
  10. Homoiconic closure (self_eval.py tests itself)
  11. Registry ↔ implementation coherence (slot_risk, defaults, reachability)
  12. Consolidation logic (Pareto compression present)

Usage: python self_eval.py --skill-dir /path/to/skill [--auto-fix]
"""

import re, ast, sys, argparse, importlib.util
from pathlib import Path
from datetime import date


class EvalResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.fixes = []

    def check(self, name, condition, detail="", fix=None):
        if condition:
            self.passed.append(name)
        else:
            self.failed.append({'test': name, 'detail': detail, 'fix': fix})
            if fix:
                self.fixes.append(fix)

    @property
    def rate(self):
        t = len(self.passed) + len(self.failed)
        return len(self.passed) / max(t, 1)


def load_text(path):
    return path.read_text(encoding='utf-8', errors='ignore') if path.exists() else ''


def extract_python_constants(source, name):
    """Extract a top-level dict constant from Python source."""
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == name:
                        return ast.literal_eval(node.value)
    except Exception:
        pass
    return None


def run_eval(skill_dir: Path):
    R = EvalResult()
    skill_md = load_text(skill_dir / 'SKILL.md')
    scripts_dir = skill_dir / 'scripts'
    refs_dir = skill_dir / 'references'

    # ═══════════════════════════════════════════════════
    # 1. SKILL.md ↔ FILESYSTEM
    # ═══════════════════════════════════════════════════
    print("--- 1. SKILL.md ↔ filesystem ---")

    # Extract script filenames from directory tree comment
    tree_py = re.findall(r'[├└]── (\w+\.py)', skill_md)
    for py in tree_py:
        R.check(f"1.1 tree:{py} exists", (scripts_dir / py).exists(),
                f"{py} referenced in tree but missing from scripts/",
                {'safe': False, 'action': f'Create {py} or remove from tree'})

    # Extract reference files from progressive loading map
    ref_nums = set(re.findall(r'\[(\d+)-', skill_md))
    for num in ref_nums:
        found = list(refs_dir.glob(f"{num}-*.md"))
        R.check(f"1.2 ref[{num}] exists", len(found) > 0,
                f"Reference [{num}] in SKILL.md but no {num}-*.md file")

    # ═══════════════════════════════════════════════════
    # 2. SCRIPTS ↔ NODE SCHEMA
    # ═══════════════════════════════════════════════════
    print("--- 2. scripts ↔ node schema ---")

    schema = load_text(refs_dir / '04-node-schema.md')
    compound_src = load_text(scripts_dir / 'compound_update.py')

    # Fields that compound_update.py writes to frontmatter
    fm_writes = re.findall(r'fm_up\["(\w+)"\]|fm_up\[\'(\w+)\'\]', compound_src)
    fm_writes += re.findall(r'"(\w+)":\s*\w', compound_src)  # dict literal keys
    written_fields = set(f[0] or f[1] for f in fm_writes if f[0] or f[1])
    # Filter to actual frontmatter fields (not local vars)
    known_fm = {'mastery', 'review_count', 'last_reviewed', 'next_review', 'status',
                'zpd_delta', 'last_error_types', 'last_misconceptions', 'scaffold_strategy',
                'correctness', 'transferability'}
    written_fields = written_fields & known_fm

    for field in written_fields:
        R.check(f"2.1 field:{field} in schema", field in schema,
                f"compound_update writes '{field}' but it's not in node schema",
                {'safe': False, 'action': f'Add {field} to 04-node-schema.md frontmatter'})

    # ═══════════════════════════════════════════════════
    # 3. MECHANISM_REGISTRY ↔ BCME SEARCH LAW
    # ═══════════════════════════════════════════════════
    print("--- 3. mechanism registry ↔ BCME ---")

    meta_src = load_text(scripts_dir / 'meta_compound.py')
    registry = extract_python_constants(meta_src, 'MECHANISM_REGISTRY')

    # BCME defines S = (X, G, T, Q, P, A, M) — 7 axes
    bcme_axes = {
        'representation': 'X (representation space)',
        'generator': 'G (candidate generator)',
        'traversal': 'T (traversal policy)',
        'evaluation': 'Q (evaluation metric)',
        'pruning': 'P (pruning/stopping)',
        'abstraction': 'A (abstraction level)',
        'modality': 'M (modality coupling)',
    }

    if registry:
        for axis, bcme_name in bcme_axes.items():
            R.check(f"3.1 axis:{axis} in registry", axis in registry,
                    f"BCME axis {bcme_name} missing from MECHANISM_REGISTRY")
            if axis in registry:
                n_mechs = len(registry[axis])
                R.check(f"3.2 {axis} has ≥2 mechanisms", n_mechs >= 2,
                        f"{axis} has only {n_mechs} mechanism (need ≥2 for swap)")

        total_mechs = sum(len(v) for v in registry.values())
        R.check(f"3.3 total mechanisms ≥ 20", total_mechs >= 20,
                f"Only {total_mechs} total mechanisms")
    else:
        R.check("3.0 MECHANISM_REGISTRY parseable", False,
                "Could not extract MECHANISM_REGISTRY from meta_compound.py")

    # ═══════════════════════════════════════════════════
    # 4. PLATEAU_TYPES ↔ classify_plateau
    # ═══════════════════════════════════════════════════
    print("--- 4. plateau types ↔ classifier ---")

    plateaus = extract_python_constants(meta_src, 'PLATEAU_TYPES')
    if plateaus:
        for ptype in plateaus:
            # Each plateau type should have recommended mechanisms
            rec = plateaus[ptype].get('recommended', {})
            R.check(f"4.1 {ptype} has recommendations", len(rec) > 0,
                    f"Plateau '{ptype}' has no recommended mechanism swaps")
            # Each recommended mechanism should exist in registry
            if registry:
                for slot, mech in rec.items():
                    R.check(f"4.2 {ptype}→{mech} exists in registry",
                            slot in registry and mech in registry.get(slot, {}),
                            f"Recommended {mech} not in registry[{slot}]")

        # Check classifier function returns all types
        R.check("4.3 classify_plateau function exists",
                "def classify_plateau" in meta_src)

        # Check each type has a detection path in classify_plateau
        classifier_body = meta_src[meta_src.find('def classify_plateau'):
                                    meta_src.find('\ndef ', meta_src.find('def classify_plateau') + 1)]
        for ptype in ['recall', 'discrimination', 'application', 'explanation',
                      'calibration', 'fluency', 'speed']:
            R.check(f"4.4 {ptype} detectable in classifier",
                    f"'{ptype}'" in classifier_body,
                    f"classify_plateau never returns '{ptype}'")
    else:
        R.check("4.0 PLATEAU_TYPES parseable", False,
                "Could not extract PLATEAU_TYPES from meta_compound.py")

    # ═══════════════════════════════════════════════════
    # 5. ROUTING TABLE ↔ SCRIPTS
    # ═══════════════════════════════════════════════════
    print("--- 5. routing ↔ scripts ---")

    commands = re.findall(r'`/path (\w+)', skill_md)
    script_map = {
        'build': 'pkg_gkg_diff.py', 'scan': 'pkg_gkg_diff.py',
        'gap': 'pkg_gkg_diff.py', 'traverse': 'mcmc_traversal.py',
        'compound': 'compound_update.py', 'refine': 'gkg_refine.py',
        'meta': 'meta_compound.py', 'verify': 'validate_vault.py',
        'status': 'pkg_gkg_diff.py', 'self-eval': 'self_eval.py',
        'consolidate': 'memory_consolidate.py',
        'improve': 'self_improve.py',
    }
    for cmd in commands:
        expected = script_map.get(cmd)
        if expected:
            R.check(f"5.1 /path {cmd} → {expected}", (scripts_dir / expected).exists(),
                    f"Command /path {cmd} maps to {expected} which doesn't exist")
        R.check(f"5.2 /path {cmd} in routing table", f'/path {cmd}' in skill_md)

    # ═══════════════════════════════════════════════════
    # 6. FINDING TAGS ↔ IMPLEMENTATION
    # ═══════════════════════════════════════════════════
    print("--- 6. finding tags ↔ implementation ---")

    all_sources = meta_src + compound_src + load_text(scripts_dir / 'gkg_refine.py')
    ref08 = load_text(refs_dir / '08-self-distillation-integration.md')

    for tag in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']:
        R.check(f"6.1 {tag} in SKILL.md", tag in skill_md)
        R.check(f"6.2 {tag} in ref08", tag in ref08)

    for tag in ['G1', 'G2', 'G3', 'G5', 'G6', 'G7']:
        R.check(f"6.3 {tag} in meta_compound", tag in meta_src,
                f"BCME gap {tag} not referenced in meta_compound.py")

    # ═══════════════════════════════════════════════════
    # 7. CROSS-REFERENCES BETWEEN REFERENCES
    # ═══════════════════════════════════════════════════
    print("--- 7. cross-references ---")

    ref01 = load_text(refs_dir / '01-theoretical-core.md')
    # ref01 should reference ref08
    R.check("7.1 ref01 → ref08 cross-ref", '[08' in ref01 or 'self-distillation' in ref01.lower())
    # ref08 should reference the papers
    for paper in ['SDFT', 'SDPO', 'HyperAgents', 'Bilevel']:
        R.check(f"7.2 {paper} in ref08", paper in ref08)
    # MCMC ref should mention tabu/orthogonal
    ref03 = load_text(refs_dir / '03-mcmc-hamiltonian.md')
    R.check("7.3 tabu noted in MCMC ref", 'tabu' in ref03.lower() or 'Tabu' in ref03)

    # ═══════════════════════════════════════════════════
    # 8. BACKWARD COMPATIBILITY
    # ═══════════════════════════════════════════════════
    print("--- 8. backward compatibility ---")

    R.check("8.1 scalar session format handled",
            "'score'" in compound_src or '"score"' in compound_src,
            "compound_update.py doesn't handle legacy scalar session format")
    R.check("8.2 EMA function exists", 'def ema' in compound_src or 'def ema_update' in compound_src)
    R.check("8.3 mastered threshold 0.85", '0.85' in compound_src)

    # ═══════════════════════════════════════════════════
    # 9. PARAMETER GOVERNANCE
    # ═══════════════════════════════════════════════════
    print("--- 9. parameter governance ---")

    bounds = extract_python_constants(meta_src, 'PARAM_BOUNDS')
    if bounds:
        for param, (lo, hi) in bounds.items():
            R.check(f"9.1 {param} bounded [{lo},{hi}]", lo < hi,
                    f"Invalid bounds: {lo} >= {hi}")
        R.check("9.2 alpha has bounds", 'alpha' in bounds)
        R.check("9.3 zpd_delta_target has bounds", 'zpd_delta_target' in bounds)
    else:
        R.check("9.0 PARAM_BOUNDS parseable", False)

    R.check("9.4 tabu_horizon in defaults", 'tabu_horizon' in meta_src)
    R.check("9.5 stall_epsilon in defaults", 'stall_epsilon' in meta_src)

    # ═══════════════════════════════════════════════════
    # 10. HOMOICONIC CLOSURE
    # ═══════════════════════════════════════════════════
    print("--- 10. homoiconic closure ---")

    self_eval_src = load_text(scripts_dir / 'self_eval.py')
    R.check("10.1 self_eval.py exists", (scripts_dir / 'self_eval.py').exists())
    R.check("10.2 self_eval tests MECHANISM_REGISTRY", 'MECHANISM_REGISTRY' in self_eval_src)
    R.check("10.3 self_eval tests PLATEAU_TYPES", 'PLATEAU_TYPES' in self_eval_src)
    R.check("10.4 self_eval tests itself (homoiconic)", 'self_eval.py' in self_eval_src)
    R.check("10.5 memory_consolidate.py exists", (scripts_dir / 'memory_consolidate.py').exists())
    R.check("10.6 /path self-eval in routing", '/path self-eval' in skill_md)
    R.check("10.7 /path consolidate in routing", '/path consolidate' in skill_md)
    R.check("10.8a /path improve in routing", '/path improve' in skill_md)
    R.check("10.8b self_improve.py exists", (scripts_dir / 'self_improve.py').exists())

    # Check the skill's own architecture is a traversable graph
    all_scripts = [f.name for f in scripts_dir.glob('*.py') if '__pycache__' not in str(f)]
    all_refs = [f.name for f in refs_dir.glob('*.md')]
    R.check("10.8 ≥10 scripts", len(all_scripts) >= 10, f"found {len(all_scripts)}")
    R.check("10.9 ≥8 references", len(all_refs) >= 8, f"found {len(all_refs)}")

    # The core invariant: Priority = Centrality × Impact × (1-Mastery) in SKILL.md
    R.check("10.10 priority formula in core model",
            'Centrality' in skill_md and 'Impact' in skill_md and 'Mastery' in skill_md)

    # v1 concepts preserved (graph theory grounding)
    for concept in ['Zeigarnik', 'ZPD', 'RPP', 'MCMC', 'Hamiltonian', 'eigenvector']:
        R.check(f"10.11 v1:{concept} preserved", concept in skill_md)

    # ═══════════════════════════════════════════════════
    # 11. REGISTRY ↔ IMPLEMENTATION COHERENCE
    # ═══════════════════════════════════════════════════
    print("--- 11. registry ↔ implementation ---")

    if registry:
        # 11.1: slot_risk in score_candidate must cover all registry axes
        score_fn = meta_src[meta_src.find('def score_candidate'):
                            meta_src.find('\ndef ', meta_src.find('def score_candidate') + 1)]
        for axis in registry:
            R.check(f"11.1 slot_risk has '{axis}'",
                    f"'{axis}'" in score_fn,
                    f"score_candidate slot_risk missing axis '{axis}'")

        # 11.2: DEFAULTS active_mechanisms must cover all registry axes
        defaults = extract_python_constants(meta_src, 'DEFAULTS')
        if defaults and 'active_mechanisms' in defaults:
            for axis in registry:
                R.check(f"11.2 DEFAULTS[active_mechanisms] has '{axis}'",
                        axis in defaults['active_mechanisms'],
                        f"Default mechanisms missing axis '{axis}'")
        else:
            R.check("11.2a DEFAULTS parseable", False)

        # 11.3: Majority of registry mechanisms should be reachable via plateau recommendations
        #        Some unreachable mechanisms are by design (manual selection / registry exploration)
        all_recommended = set()
        if plateaus:
            for pt in plateaus.values():
                for mech in pt.get('recommended', {}).values():
                    all_recommended.add(mech)
        total_mechs = sum(len(v) for v in registry.values())
        unreachable = []
        for axis, mechs in registry.items():
            for mech in mechs:
                if mech not in all_recommended:
                    default_mech = defaults.get('active_mechanisms', {}).get(axis, '') if defaults else ''
                    if mech != default_mech:
                        unreachable.append(f"{axis}:{mech}")
        max_unreachable = max(4, int(total_mechs * 0.55))  # ≤55% unreachable is OK
        R.check(f"11.3 unreachable mechanisms <= {max_unreachable}",
                len(unreachable) <= max_unreachable,
                f"{len(unreachable)} mechanisms never recommended: {unreachable[:5]}")

    # ═══════════════════════════════════════════════════
    # 12. CONSOLIDATION LOGIC
    # ═══════════════════════════════════════════════════
    print("--- 12. consolidation ---")

    R.check("12.1 consolidation in meta_compound", 'consolidation' in meta_src,
            "meta_compound.py has no consolidation logic")
    R.check("12.2 memory_consolidate has Pareto", 'pareto' in load_text(scripts_dir / 'memory_consolidate.py').lower(),
            "memory_consolidate.py doesn't reference Pareto compression")

    # ═══════════════════════════════════════════════════
    # 13. SELF-TOPOLOGY (η of skill's own graph)
    # ═══════════════════════════════════════════════════
    print("--- 13. self-topology ---")

    # Measure the skill's own graph: nodes = files, edges = cross-references
    all_files = set()
    for f in scripts_dir.glob('*.py'):
        all_files.add(f'scripts/{f.name}')
    for f in refs_dir.glob('*.md'):
        all_files.add(f'references/{f.name}')
    all_files.add('SKILL.md')
    assets_dir = skill_dir / 'assets'
    if assets_dir.exists():
        for f in assets_dir.iterdir():
            all_files.add(f'assets/{f.name}')

    self_edges = set()
    for f_path in list(scripts_dir.glob('*.py')) + list(refs_dir.glob('*.md')) + [skill_dir / 'SKILL.md']:
        content = load_text(f_path)
        src = f_path.name if f_path.parent == skill_dir else f'{f_path.parent.name}/{f_path.name}'
        for n in all_files:
            basename = Path(n).stem
            if basename in content and n != src and len(basename) > 3:
                self_edges.add((src, n))
        # Ref tags [01] [02]
        for ref_num in re.findall(r'\[(\d+)\]', content):
            matches = [n for n in all_files if n.startswith(f'references/{ref_num}-')]
            for m in matches:
                self_edges.add((src, m))

    self_eta = len(self_edges) / max(len(all_files), 1)
    R.check(f"13.1 self η ≥ 3.0 (currently {self_eta:.2f})", self_eta >= 3.0,
            f"Skill's own η = {self_eta:.2f} < 3.0 — insufficient internal cross-referencing",
            {'safe': False, 'action': 'Add cross-references between under-connected files'})
    R.check(f"13.2 self η ≥ 4.0 aspirational ({self_eta:.2f})", self_eta >= 4.0,
            f"Skill η = {self_eta:.2f} < 4.0 — below own prescribed target")

    # No isolates
    connected = set()
    for s, t in self_edges:
        connected.add(s)
        connected.add(t)
    isolates = all_files - connected
    R.check("13.3 no isolates", len(isolates) == 0,
            f"Isolated files: {isolates}")

    return R


def main():
    ap = argparse.ArgumentParser(description="Path Skill Self-Eval v3 (Architectural + Topological)")
    ap.add_argument("--skill-dir", default=".", help="Path to skill directory")
    ap.add_argument("--output", default="eval_report.yaml")
    ap.add_argument("--auto-fix", action="store_true")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    print(f"═══ PATH SKILL SELF-EVAL (architectural) ═══\n")

    R = run_eval(skill_dir)

    # Report
    import yaml
    report = {
        'date': date.today().isoformat(),
        'skill_dir': str(skill_dir),
        'pass': len(R.passed),
        'fail': len(R.failed),
        'rate': round(R.rate, 4),
        'health': 'HEALTHY' if R.rate >= 0.95 else ('DEGRADED' if R.rate >= 0.80 else 'FAILING'),
        'failures': R.failed if R.failed else None,
        'fix_coverage': len([f for f in R.failed if f.get('fix')]) / max(len(R.failed), 1),
    }
    Path(args.output).write_text(yaml.dump(report, default_flow_style=False))

    print(f"\n{'='*50}")
    print(f"PASS: {len(R.passed)} | FAIL: {len(R.failed)} | RATE: {R.rate:.0%}")
    print(f"Health: {report['health']}")
    if R.failed:
        print(f"\nFailed:")
        for f in R.failed:
            print(f"  ✗ {f['test']}: {f['detail'][:70]}")
    print(f"\nReport: {args.output}")
    return 0 if R.rate >= 0.95 else 1


if __name__ == "__main__":
    sys.exit(main())
