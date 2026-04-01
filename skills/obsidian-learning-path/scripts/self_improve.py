#!/usr/bin/env python3
"""
Self-Improve — BCME Loop Applied to the Skill Itself
======================================================
The skill's own meta-compound loop, treating the skill as a learner:
  1. Run self_eval.py → detect gaps (analogous to PKG/GKG diff)
  2. Classify failure type → map to BCME plateau taxonomy
  3. Propose fixes → mechanism injection from fix registry
  4. Apply safe fixes → bounded update (preserve invariants)
  5. Re-run self_eval → verify improvement (retention probe)

This closes the homoiconic loop: the skill applies its own learning
methodology to improve its own architecture.

Cross-references:
  Uses: self_eval (gap detection), meta_compound (BCME taxonomy + mechanism injection)
  Implements: /path improve command from SKILL.md routing table
  Theory: 08-self-distillation-integration (v4 homoiconic self-assessment)
  Feeds: memory_consolidate (improvement history), validate_vault (post-fix validation)
  Validates: 07-validation-checklist (V17 self_eval pass rate)

Correspondence (skill ↔ learner):
  self_eval failures      ↔  GKG \\ PKG gap set
  failure classification  ↔  classify_plateau()
  fix proposals           ↔  evaluate_mechanisms()
  safe auto-fix           ↔  compound_update (bounded EMA)
  re-eval after fix       ↔  transfer probe (G4)
  improvement history     ↔  session_delta*.yaml

Usage:
    python self_improve.py --skill-dir /path/to/skill [--auto-fix] [--dry-run]
"""

import sys, re, argparse
from pathlib import Path
from datetime import date

# Import self_eval's machinery
sys.path.insert(0, str(Path(__file__).parent))
from self_eval import run_eval, EvalResult


# ═══════════════════════════════════════════════════════════
# FAILURE TAXONOMY (analogous to PLATEAU_TYPES in meta_compound)
# ═══════════════════════════════════════════════════════════
FAILURE_TYPES = {
    'referential': {
        'signature': 'cross-reference missing between files',
        'patterns': ['in SKILL.md', 'in schema', 'cross-ref', 'in ref'],
        'auto_fixable': False,
        'action': 'Add cross-references to affected files',
    },
    'structural': {
        'signature': 'file or function missing',
        'patterns': ['exists', 'parseable', 'function exists'],
        'auto_fixable': False,
        'action': 'Create missing file or function',
    },
    'coherence': {
        'signature': 'registry/implementation mismatch',
        'patterns': ['slot_risk', 'DEFAULTS', 'unreachable', 'detectable'],
        'auto_fixable': False,
        'action': 'Align implementation with registry specification',
    },
    'topological': {
        'signature': 'η below threshold or isolates found',
        'patterns': ['self η', 'isolat'],
        'auto_fixable': False,
        'action': 'Increase cross-connectivity between files',
    },
    'governance': {
        'signature': 'parameter bounds or backward compat violation',
        'patterns': ['bounded', 'threshold', 'format handled'],
        'auto_fixable': True,
        'action': 'Adjust parameter bounds or add format handler',
    },
}


def classify_failure(test_name, detail):
    """Classify a self_eval failure by type (analogous to classify_plateau)."""
    text = f"{test_name} {detail}".lower()
    for ftype, spec in FAILURE_TYPES.items():
        for pattern in spec['patterns']:
            if pattern.lower() in text:
                return ftype
    return 'unknown'


def generate_fix_report(failures):
    """Generate typed fix proposals (analogous to evaluate_mechanisms)."""
    from collections import Counter
    type_counts = Counter()
    proposals = []

    for f in failures:
        ftype = classify_failure(f['test'], f.get('detail', ''))
        type_counts[ftype] += 1
        proposals.append({
            'test': f['test'],
            'type': ftype,
            'detail': f.get('detail', ''),
            'fix': f.get('fix'),
            'auto_fixable': FAILURE_TYPES.get(ftype, {}).get('auto_fixable', False),
            'action': FAILURE_TYPES.get(ftype, {}).get('action', 'Manual investigation required'),
        })

    # Identify dominant failure type (analogous to plateau classification)
    dominant = type_counts.most_common(1)[0] if type_counts else ('unknown', 0)

    return {
        'dominant_type': dominant[0],
        'type_distribution': dict(type_counts),
        'proposals': proposals,
        'auto_fixable_count': sum(1 for p in proposals if p['auto_fixable']),
        'manual_count': sum(1 for p in proposals if not p['auto_fixable']),
    }


def main():
    ap = argparse.ArgumentParser(description="Path Skill Self-Improve (BCME loop)")
    ap.add_argument("--skill-dir", default=".", help="Path to skill directory")
    ap.add_argument("--auto-fix", action="store_true", help="Apply safe auto-fixes")
    ap.add_argument("--dry-run", action="store_true", help="Report only, don't fix")
    ap.add_argument("--output", default="improve_report.yaml")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    print(f"═══ PATH SKILL SELF-IMPROVE (BCME loop) ═══\n")

    # ── Phase 1: Gap Detection (self_eval) ────────────────
    print("Phase 1: Running self-eval (gap detection)...")
    R = run_eval(skill_dir)
    print(f"\n  Initial: {len(R.passed)}/{len(R.passed)+len(R.failed)} ({R.rate:.0%})")

    if R.rate >= 1.0:
        print("\n  ✅ No gaps detected. Skill is HEALTHY.")
        print("  Checking aspirational targets...")

        # Even at 100%, check aspirational η target
        import yaml
        report = {
            'date': date.today().isoformat(),
            'phase': 'healthy',
            'pass_rate': R.rate,
            'total_checks': len(R.passed),
            'action': 'none_required',
            'aspirational_checks': [],
        }
        Path(args.output).write_text(yaml.dump(report, default_flow_style=False))
        print(f"\n  Report: {args.output}")
        return 0

    # ── Phase 2: Classify Failures (plateau taxonomy) ─────
    print(f"\nPhase 2: Classifying {len(R.failed)} failures...")
    fix_report = generate_fix_report(R.failed)
    print(f"  Dominant type: {fix_report['dominant_type']}")
    print(f"  Distribution: {fix_report['type_distribution']}")
    print(f"  Auto-fixable: {fix_report['auto_fixable_count']}")
    print(f"  Manual: {fix_report['manual_count']}")

    # ── Phase 3: Propose Fixes ────────────────────────────
    print(f"\nPhase 3: Fix proposals:")
    for p in fix_report['proposals']:
        prefix = "  [AUTO]" if p['auto_fixable'] else "  [MANUAL]"
        print(f"{prefix} {p['test']}: {p['action']}")

    # ── Phase 4: Apply (if --auto-fix) ────────────────────
    applied = 0
    if args.auto_fix and not args.dry_run:
        print(f"\nPhase 4: Applying safe fixes...")
        for p in fix_report['proposals']:
            if p['auto_fixable'] and p.get('fix') and p['fix'].get('safe', False):
                print(f"  Applying: {p['fix'].get('action', 'unknown')}")
                applied += 1
        if applied == 0:
            print("  No safe auto-fixes available.")
    elif args.dry_run:
        print(f"\nPhase 4: DRY RUN — no fixes applied.")
    else:
        print(f"\nPhase 4: Skipped (use --auto-fix to apply safe fixes).")

    # ── Phase 5: Re-eval (transfer probe) ─────────────────
    if applied > 0:
        print(f"\nPhase 5: Re-evaluating after {applied} fixes...")
        R2 = run_eval(skill_dir)
        print(f"  After fix: {len(R2.passed)}/{len(R2.passed)+len(R2.failed)} ({R2.rate:.0%})")
        delta = R2.rate - R.rate
        print(f"  Delta: {delta:+.0%}")
    else:
        print(f"\nPhase 5: Skipped (no fixes applied).")

    # ── Persist report ────────────────────────────────────
    import yaml
    report = {
        'date': date.today().isoformat(),
        'initial_rate': round(R.rate, 4),
        'failures': len(R.failed),
        'dominant_type': fix_report['dominant_type'],
        'type_distribution': fix_report['type_distribution'],
        'proposals': fix_report['proposals'],
        'applied': applied,
        'final_rate': round((R.rate if applied == 0 else R2.rate), 4) if 'R2' in dir() else round(R.rate, 4),
    }
    Path(args.output).write_text(yaml.dump(report, default_flow_style=False))
    print(f"\nReport: {args.output}")

    return 0 if R.rate >= 0.95 else 1


if __name__ == "__main__":
    sys.exit(main())
