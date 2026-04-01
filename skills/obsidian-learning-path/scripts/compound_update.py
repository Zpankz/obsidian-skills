#!/usr/bin/env python3
"""
Compound Update v2 — Post-Session PKG Propagation with Self-Distillation
=========================================================================
Integrates F1 (dense credit), F3 (self-demo capture), F5 (rich feedback),
F6 (prediction error tracking for meta-compound).

Session JSON supports two formats:
  - Legacy: [{"node_id": X, "score": 0.75}]                  → scalar EMA fallback
  - Rich:   [{"node_id": X, "feedback": {concept_scores, ...}}]  → dense multi-signal

Cross-references:
  Uses: 04-node-schema (frontmatter fields), 02-pkg-gkg-differential (gap algebra)
  Feeds: meta_compound (prediction_errors), gkg_refine (performance_history),
         validate_vault (V8 status, V12 retention_alert, V13 self_demo_sources),
         memory_consolidate (session_delta files)
  Schema: 08-self-distillation-integration (F1, F3, F5 specs)

Usage:
    python compound_update.py \\
      --path path.json --session session.json \\
      --vault ./my_vault --output path_updated.json
"""

import json, yaml, math, argparse
from pathlib import Path
from datetime import date, timedelta

# ── Default Parameters (overridden by meta_lessons.yaml if present) ──
DEFAULTS = {
    'alpha': 0.30,
    'mastered_threshold': 0.85,
    'retention_probe_freq': 5,
    'zpd_delta_target': 0.22,
}

ERROR_WEIGHTS = {
    'retrieval_failure': -0.30, 'misconception': -0.25,
    'incomplete_mechanism': -0.15, 'false_connection': -0.15,
    'integration_failure': -0.10, 'calculation_error': -0.05,
    'partial_retrieval': -0.05, 'overcondensation': -0.02,
}

CONCEPT_WEIGHTS = {
    'core_mechanism': 0.35, 'clinical_application': 0.25,
    'quantitative_relationships': 0.25, 'integration_with_prerequisites': 0.15,
}


def load_params(vault_path: Path) -> dict:
    meta_path = vault_path / 'meta_lessons.yaml'
    if meta_path.exists():
        meta = yaml.safe_load(meta_path.read_text()) or {}
        params = dict(DEFAULTS)
        if 'current_params' in meta:
            params.update(meta['current_params'])
        return params
    return dict(DEFAULTS)


def clamp(v, lo, hi): return max(lo, min(hi, v))


def feedback_to_score(fb: dict) -> float:
    """F1/F5: Dense multi-signal mastery update."""
    cs = fb.get('concept_scores', {})
    if cs:
        w = sum(CONCEPT_WEIGHTS.get(k, 0.25) * v for k, v in cs.items())
        tw = sum(CONCEPT_WEIGHTS.get(k, 0.25) for k in cs)
        base = w / max(tw, 0.01)
    else:
        base = fb.get('score', 0.5)

    err_pen = sum(ERROR_WEIGHTS.get(e, -0.05) for e in fb.get('error_types', []))
    calibration = max(0, 1.0 - 2 * abs(fb.get('confidence_before', 0.5) - base))
    exp_bonus = 0.05 * fb.get('self_explanation_quality', 0.5)

    return clamp(base + err_pen + 0.1 * calibration + exp_bonus, 0.0, 1.0)


def ema(old, new, alpha): return round((1 - alpha) * old + alpha * new, 4)


def next_review(mastery, review_count):
    easiness = 1.3 + 0.9 * mastery
    interval = min(int(math.pow(easiness, max(review_count, 1))), 21)
    return (date.today() + timedelta(days=max(1, interval))).isoformat()


def update_vault_fm(vault_path, node_id, updates):
    for md in vault_path.rglob("*.md"):
        txt = md.read_text(encoding="utf-8", errors="ignore")
        if not txt.startswith("---"):
            continue
        try:
            end = txt.index("---", 3)
        except ValueError:
            continue
        try:
            fm = yaml.safe_load(txt[3:end]) or {}
        except yaml.YAMLError:
            continue
        if fm.get("id") == node_id:
            fm.update(updates)
            md.write_text(f"---\n{yaml.dump(fm, default_flow_style=False, allow_unicode=True)}---{txt[end+3:]}", encoding="utf-8")
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="Compound Update v2")
    ap.add_argument("--path", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--vault", required=True)
    ap.add_argument("--output", default="path_updated.json")
    ap.add_argument("--delta-report", default="session_delta.yaml")
    args = ap.parse_args()

    nodes = json.loads(Path(args.path).read_text())
    session = json.loads(Path(args.session).read_text())
    vp = Path(args.vault)
    params = load_params(vp)
    alpha = params['alpha']
    threshold = params['mastered_threshold']

    deltas, newly_mastered, pred_errors, all_errors = [], [], [], []

    for entry in session:
        nid = entry["node_id"]
        node = next((n for n in nodes if n["id"] == nid), None)
        if not node:
            continue

        old_m = node.get("mastery", 0.0)

        # ── Detect rich vs scalar ─────────────────────────────────
        if "feedback" in entry:
            score = feedback_to_score(entry["feedback"])
            fb = entry["feedback"]
        else:
            score, fb = entry.get("score", 0.0), None

        new_m = ema(old_m, score, alpha)
        rc = node.get("review_count", 0) + 1

        # ── F6: prediction error tracking ─────────────────────────
        # Compare STORED mastery (from previous session) against CURRENT
        # performance. Positive = overestimated mastery (forgetting/over-optimistic).
        # Negative = underestimated (consolidated better than expected).
        pred_errors.append({
            'node': nid,
            'stored_mastery': old_m,
            'session_score': round(score, 4),
            'prediction_error': round(old_m - score, 4),
        })

        node.update({
            "mastery": new_m, "review_count": rc,
            "last_reviewed": date.today().isoformat(),
            "next_review": next_review(new_m, rc),
            "status": "mastered" if new_m >= threshold else ("in-progress" if new_m >= 0.3 else "gap"),
            "zpd_delta": round(max(0.0, node.get("difficulty", 0.5) - new_m), 3),
        })

        if new_m >= threshold and old_m < threshold:
            newly_mastered.append(node.get("title", nid))

        d = {"node": nid, "title": node.get("title", nid),
             "mastery_old": old_m, "mastery_new": new_m,
             "delta": round(new_m - old_m, 4), "status": node["status"],
             "next_review": node["next_review"],
             "feedback_type": "rich" if fb else "scalar"}

        if fb:
            d["error_types"] = fb.get("error_types", [])
            d["misconceptions"] = fb.get("misconceptions_identified", [])
            d["concept_scores"] = fb.get("concept_scores", {})
            all_errors.extend(d["error_types"])

        deltas.append(d)

        # ── F3: Self-demo eligibility on mastery ──────────────────
        fm_up = {
            "mastery": new_m, "review_count": rc,
            "last_reviewed": node["last_reviewed"], "next_review": node["next_review"],
            "status": node["status"], "zpd_delta": node["zpd_delta"],
        }
        if fb:
            fm_up["last_error_types"] = fb.get("error_types", [])
            fm_up["last_misconceptions"] = fb.get("misconceptions_identified", [])
            if new_m >= threshold and fb.get("self_explanation_quality", 0) >= 0.7:
                fm_up["scaffold_strategy"] = "self_demo"
            # N4: Schema quality decomposition
            cs = fb.get("concept_scores", {})
            if cs:
                # correctness: fraction of concept_scores above 0.7
                fm_up["correctness"] = round(sum(1 for v in cs.values() if v >= 0.7) / max(len(cs), 1), 2)
            if not fb.get("error_types"):
                # No errors = high correctness on this attempt
                fm_up["correctness"] = max(fm_up.get("correctness", 0), 0.9)
            # transferability estimated from integration_with_prerequisites score
            if "integration_with_prerequisites" in cs:
                fm_up["transferability"] = round(cs["integration_with_prerequisites"], 2)

        if vp.exists():
            update_vault_fm(vp, nid, fm_up)

    # ── Resequence ────────────────────────────────────────────────
    active = sorted([n for n in nodes if n.get("status") != "mastered"], key=lambda n: -n.get("priority", 0))
    done = [n for n in nodes if n.get("status") == "mastered"]
    seq = active + done
    for i, n in enumerate(seq):
        n["path_position"] = i + 1

    Path(args.output).write_text(json.dumps(seq, indent=2))

    coverage = round(len(done) / max(len(nodes), 1) * 100, 1)
    err_dist = {}
    for e in all_errors:
        err_dist[e] = err_dist.get(e, 0) + 1

    report = {
        "session_date": date.today().isoformat(),
        "nodes_studied": len(deltas), "newly_mastered": newly_mastered,
        "coverage_after": coverage, "mastered_count": len(done), "gap_count": len(active),
        "feedback_type_breakdown": {
            "rich": sum(1 for d in deltas if d["feedback_type"] == "rich"),
            "scalar": sum(1 for d in deltas if d["feedback_type"] == "scalar"),
        },
        "error_distribution": err_dist,
        "prediction_errors": pred_errors,
        "deltas": sorted(deltas, key=lambda d: -abs(d["delta"])),
    }
    Path(args.delta_report).write_text(yaml.dump(report, default_flow_style=False))

    print(f"✅ Compound update v2")
    print(f"   Nodes: {len(deltas)} | Mastered: +{len(newly_mastered)} | Coverage: {coverage}%")
    if err_dist:
        top = sorted(err_dist.items(), key=lambda x: -x[1])[:3]
        print(f"   Top errors: {', '.join(f'{e}({c})' for e,c in top)}")


if __name__ == "__main__":
    main()
