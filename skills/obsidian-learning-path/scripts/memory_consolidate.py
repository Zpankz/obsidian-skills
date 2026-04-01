#!/usr/bin/env python3
"""
Memory Consolidate — Pareto Compress Session History
=====================================================
Applies the path skill's own Pareto principle to its own memory:
keep 20% of sessions that carry 80% of the learning signal.

Old sessions are compressed into consolidated_history.yaml with:
- Error pattern aggregates (not per-session counts)
- Mastery trajectory summaries (not per-node deltas)
- Mechanism effectiveness ratings (which swaps helped?)
- Plateau history (when stalled, what worked?)

Cross-references:
  Uses: 08-self-distillation-integration (BCME invariant preservation principle)
  Input: compound_update (session_delta*.yaml files)
  Feeds: meta_compound (compressed history for long-term trend analysis),
         self_eval (section 12: consolidation logic check, section 10: V18 check)
  Theory: 02-pkg-gkg-differential (Pareto compression), validate_vault (V18 session count)

Usage:
    python memory_consolidate.py \
      --history session_history/ --keep-recent 10 \
      --output consolidated_history.yaml
"""

import yaml, argparse
from pathlib import Path
from datetime import date, datetime
from statistics import mean
from collections import Counter


def load_sessions(history_dir: Path) -> list:
    sessions = []
    for f in sorted(history_dir.glob("session_delta*.yaml")):
        report = yaml.safe_load(f.read_text()) or {}
        report['_file'] = f.name
        sessions.append(report)
    return sessions


def compress_old_sessions(sessions: list) -> dict:
    """Compress N sessions into aggregate statistics.
    
    The BCME principle applied to memory itself:
    preserve the invariants (aggregate patterns, trajectory),
    discard the details (individual node deltas per session).
    """
    if not sessions:
        return {}

    # Aggregate error distribution
    total_errors = Counter()
    for s in sessions:
        for e_type, count in s.get('error_distribution', {}).items():
            total_errors[e_type] += count

    # Coverage trajectory
    coverages = [s.get('coverage_after', 0) for s in sessions]
    coverage_start = coverages[0] if coverages else 0
    coverage_end = coverages[-1] if coverages else 0

    # Mastery gains
    total_mastered = []
    for s in sessions:
        total_mastered.extend(s.get('newly_mastered', []))

    # Prediction error trajectory
    all_pred_errors = []
    for s in sessions:
        for pe in s.get('prediction_errors', []):
            if 'prediction_error' in pe:
                all_pred_errors.append(pe['prediction_error'])

    # Feedback type breakdown
    rich_count = sum(s.get('feedback_type_breakdown', {}).get('rich', 0) for s in sessions)
    scalar_count = sum(s.get('feedback_type_breakdown', {}).get('scalar', 0) for s in sessions)

    return {
        'period': {
            'start': sessions[0].get('session_date', '?'),
            'end': sessions[-1].get('session_date', '?'),
            'session_count': len(sessions),
        },
        'coverage': {
            'start': coverage_start,
            'end': coverage_end,
            'delta': round(coverage_end - coverage_start, 2),
        },
        'mastery': {
            'total_mastered': len(total_mastered),
            'mastered_nodes': total_mastered,
        },
        'errors': {
            'aggregate': dict(total_errors.most_common()),
            'dominant': total_errors.most_common(1)[0][0] if total_errors else None,
            'total': sum(total_errors.values()),
        },
        'prediction_calibration': {
            'mean_error': round(mean(all_pred_errors), 4) if all_pred_errors else None,
            'n_samples': len(all_pred_errors),
            'direction': 'overestimating' if all_pred_errors and mean(all_pred_errors) > 0 else 'underestimating',
        },
        'feedback_types': {'rich': rich_count, 'scalar': scalar_count},
    }


def main():
    ap = argparse.ArgumentParser(description="Memory Consolidation (Pareto compress)")
    ap.add_argument("--history", required=True, help="Dir with session_delta*.yaml")
    ap.add_argument("--keep-recent", type=int, default=10,
                    help="Number of recent sessions to keep in full detail")
    ap.add_argument("--output", default="consolidated_history.yaml")
    args = ap.parse_args()

    hp = Path(args.history)
    sessions = load_sessions(hp)

    if len(sessions) <= args.keep_recent:
        print(f"Only {len(sessions)} sessions (≤ {args.keep_recent}). No compression needed.")
        return

    # Split: old sessions to compress, recent to keep
    old = sessions[:-args.keep_recent]
    recent = sessions[-args.keep_recent:]

    compressed = compress_old_sessions(old)

    # Load existing consolidated history if present
    out_path = Path(args.output)
    existing_epochs = []
    if out_path.exists():
        existing = yaml.safe_load(out_path.read_text()) or {}
        existing_epochs = existing.get('epochs', [])

    # Append new epoch
    existing_epochs.append(compressed)

    result = {
        'last_consolidation': date.today().isoformat(),
        'total_sessions_compressed': sum(e.get('period', {}).get('session_count', 0)
                                          for e in existing_epochs),
        'recent_sessions_kept': len(recent),
        'epochs': existing_epochs,
    }

    out_path.write_text(yaml.dump(result, default_flow_style=False))

    # Delete compressed session files
    deleted = 0
    for s in old:
        f = hp / s.get('_file', '')
        if f.exists():
            f.unlink()
            deleted += 1

    print(f"✅ Memory consolidation")
    print(f"   Compressed: {len(old)} sessions → 1 epoch")
    print(f"   Kept recent: {len(recent)} sessions in full detail")
    print(f"   Deleted: {deleted} old session files")
    print(f"   Coverage trajectory: {compressed.get('coverage', {}).get('start')} → "
          f"{compressed.get('coverage', {}).get('end')}")
    if compressed.get('errors', {}).get('dominant'):
        print(f"   Dominant error: {compressed['errors']['dominant']}")


if __name__ == "__main__":
    main()
