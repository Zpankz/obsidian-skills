#!/usr/bin/env python3
"""
GKG Refine — Evolving Knowledge Graph from Learner Performance
===============================================================
F2: The "teacher" evolves with the learner. GKG difficulty values and
edges are refined based on accumulated session data.

Evidence: SDPO Fig 10-right (teacher improves during training),
SDFT EMA teacher ablation, HyperAgents archive evolution.

Cross-references:
  Uses: 02-pkg-gkg-differential (gap algebra), 08-self-distillation-integration (F2 spec)
  Input: compound_update (session_delta files), pkg_gkg_diff (GKG structure)
  Feeds: mcmc_traversal (recalibrated GKG), meta_compound (difficulty prediction errors),
         validate_vault (V14 difficulty calibration check)
  Theory: 01-theoretical-core (evolving teacher), self_eval (section 3: registry coherence)

Usage:
    python gkg_refine.py \
      --vault ./my_vault --gkg gkg.json \
      --history session_history/ --output gkg_refined.json
"""

import json, yaml, argparse
from pathlib import Path
from statistics import mean, variance


def clamp(v, lo, hi): return max(lo, min(hi, v))


def load_session_history(history_dir: Path) -> dict:
    """Load all session delta reports and aggregate per-node performance."""
    node_history = {}
    for f in sorted(history_dir.glob("session_delta*.yaml")):
        report = yaml.safe_load(f.read_text()) or {}
        for d in report.get("deltas", []):
            nid = d["node"]
            if nid not in node_history:
                node_history[nid] = []
            node_history[nid].append({
                'date': report.get("session_date"),
                'mastery_new': d.get("mastery_new", 0),
                'delta': d.get("delta", 0),
                'error_types': d.get("error_types", []),
                'concept_scores': d.get("concept_scores", {}),
                'misconceptions': d.get("misconceptions", []),
            })
    return node_history


def refine_gkg(gkg_nodes: list, history: dict) -> dict:
    """
    Evolve GKG from accumulated performance data.
    
    Three refinement operations:
    1. Difficulty recalibration — if learners systematically over/under-perform
    2. Edge discovery — if feedback shows cross-references not in graph
    3. Node splitting candidates — if concept_scores show high within-node variance
    """
    refinements = {
        'difficulty_recalibrated': [],
        'edges_suggested': [],
        'split_candidates': [],
        'nodes_unchanged': 0,
    }

    for node in gkg_nodes:
        nid = node.get("id", "")
        h = history.get(nid, [])

        if len(h) < 3:
            refinements['nodes_unchanged'] += 1
            continue

        # ── 1. DIFFICULTY RECALIBRATION ──────────────────────────
        # Use session-level concept_scores (dense signal) when available,
        # fall back to mastery_new (coarser). Concept scores reflect single-
        # session performance; mastery_new is accumulated state.
        session_scores = []
        for s in h:
            cs = s.get('concept_scores', {})
            if cs:
                session_scores.append(mean(cs.values()))
            else:
                session_scores.append(s.get('mastery_new', 0.5))
        
        avg_score = mean(session_scores)
        old_diff = node.get("difficulty", 0.5)
        expected_score = 1.0 - old_diff
        error = avg_score - expected_score

        if abs(error) > 0.15:
            new_diff = clamp(old_diff - 0.5 * error, 0.05, 0.95)
            node["difficulty"] = round(new_diff, 3)
            if 'difficulty_original' not in node or node['difficulty_original'] is None:
                node['difficulty_original'] = old_diff
            refinements['difficulty_recalibrated'].append({
                'node': nid,
                'old_difficulty': old_diff,
                'new_difficulty': node["difficulty"],
                'avg_session_score': round(avg_score, 3),
                'correction': round(error, 3),
                'score_source': 'concept_scores' if any(s.get('concept_scores') for s in h) else 'mastery_new',
            })

        # ── 2. EDGE DISCOVERY ────────────────────────────────────
        # Deduplicate: track unique (from, to) pairs with occurrence count
        all_misconceptions = []
        for s in h:
            all_misconceptions.extend(s.get('misconceptions', []))
        
        existing_prereqs = set(node.get("prerequisites", []))
        all_node_ids = {n.get("id", ""): n.get("title", "") for n in gkg_nodes}
        
        seen_edges = set()
        edge_counts = {}
        for misc in all_misconceptions:
            misc_lower = misc.lower()
            for other_id, other_title in all_node_ids.items():
                if other_id != nid and other_title.lower() in misc_lower:
                    if other_id not in existing_prereqs:
                        edge_key = (other_id, nid)
                        edge_counts[edge_key] = edge_counts.get(edge_key, 0) + 1
                        if edge_key not in seen_edges:
                            seen_edges.add(edge_key)
                            refinements['edges_suggested'].append({
                                'from': other_id,
                                'to': nid,
                                'evidence': f"Misconception references '{other_title}'",
                                'occurrences': 0,  # patched below
                            })
        
        # Patch occurrence counts
        for edge in refinements['edges_suggested']:
            key = (edge['from'], edge['to'])
            if key in edge_counts:
                edge['occurrences'] = edge_counts[key]

        # ── 3. NODE SPLITTING CANDIDATES ─────────────────────────
        # High variance in concept_scores across sessions → node too coarse
        if len(h) >= 5:
            all_concept_scores = [s.get('concept_scores', {}) for s in h if s.get('concept_scores')]
            if all_concept_scores:
                # Compute per-concept mean, then variance across concepts
                concept_means = {}
                for cs in all_concept_scores:
                    for k, v in cs.items():
                        concept_means.setdefault(k, []).append(v)
                
                if len(concept_means) >= 2:
                    per_concept_avg = [mean(vs) for vs in concept_means.values()]
                    concept_var = variance(per_concept_avg) if len(per_concept_avg) > 1 else 0
                    
                    if concept_var > 0.04:  # significant divergence
                        refinements['split_candidates'].append({
                            'node': nid,
                            'concept_variance': round(concept_var, 4),
                            'concept_means': {k: round(mean(v), 3) for k, v in concept_means.items()},
                            'reason': "High within-node concept divergence suggests splitting",
                        })

    return refinements


def main():
    ap = argparse.ArgumentParser(description="GKG Refinement (F2)")
    ap.add_argument("--gkg", required=True, help="Current gkg.json")
    ap.add_argument("--vault", required=True, help="Vault path")
    ap.add_argument("--history", default=".", help="Directory with session_delta*.yaml files")
    ap.add_argument("--output", default="gkg_refined.json")
    ap.add_argument("--report", default="gkg_refinement_report.yaml")
    args = ap.parse_args()

    gkg = json.loads(Path(args.gkg).read_text())
    history = load_session_history(Path(args.history))
    
    refinements = refine_gkg(gkg, history)

    Path(args.output).write_text(json.dumps(gkg, indent=2))
    Path(args.report).write_text(yaml.dump(refinements, default_flow_style=False))

    n_recal = len(refinements['difficulty_recalibrated'])
    n_edges = len(refinements['edges_suggested'])
    n_split = len(refinements['split_candidates'])

    print(f"✅ GKG refinement complete")
    print(f"   Difficulty recalibrated: {n_recal}")
    print(f"   Edges suggested:         {n_edges}")
    print(f"   Split candidates:        {n_split}")
    print(f"   Unchanged:               {refinements['nodes_unchanged']}")

    if n_edges > 0:
        print(f"\n   ⚠ Suggested edges require manual review before adding to GKG")
    if n_split > 0:
        print(f"   ⚠ Split candidates require domain expert decision")


if __name__ == "__main__":
    main()
