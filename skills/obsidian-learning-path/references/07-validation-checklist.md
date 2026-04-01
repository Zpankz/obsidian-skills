<!--
DIRECTORY TREE (orientation)
references/07-validation-checklist.md
  Covers: all validation checks · fix procedures · pass/fail criteria
  Depends on: 04-node-schema (field constraints)
  Used by: /path verify · validate_vault.py
-->

# Validation Checklist

Run: `python scripts/validate_vault.py --vault ./my_vault`

## Check Categories

| # | Check | Severity | Fix |
|---|---|---|---|
| V1 | All gap nodes have .md files | CRITICAL | re-run generate_vault.py |
| V2 | All [[wikilinks]] resolve | CRITICAL | re-run compound_update.py |
| V3 | ZPD Δ ∈ [0.10, 0.40] for all non-scaffold edges | MAJOR | insert scaffold nodes |
| V4 | All non-terminal nodes have open_question | MAJOR | derive_tension() |
| V5 | All open_questions resolved by a reachable successor | MAJOR | re-thread Zeigarnik |
| V6 | Topology η ≥ 0.80 (edges/nodes for path subgraph) | MAJOR | merge orphan clusters |
| V7 | No orphan nodes (all have path_position) | MAJOR | re-run path-planner |
| V8 | Status matches mastery threshold | MINOR | compound_update.py |
| V9 | Criticality annotations current (< 7 days old) | MINOR | re-run mcmc_traversal.py |
| V10 | Canvas renders without overlapping nodes | MINOR | re-run generate_vault.py |
| V11 | Retention probes present every K nodes in path | MAJOR | re-run mcmc_traversal.py |
| V12 | No mastered node has retention_alert=True >7 days | MINOR | run compound_update |
| V13 | Self-demo sources resolve to mastered nodes | MINOR | re-run compound_update |
| V14 | GKG difficulty within 0.20 of empirical difficulty | MINOR | run gkg_refine.py |
| V15 | Tabu list not exhausted for any mechanism slot | MINOR | reset tabu for slot |
| V16 | Cluster coverage variance < 3x across recent path | MINOR | inject cluster_rotation |
| V17 | self_eval pass rate >= 95% | MAJOR | run self_eval --auto-fix |
| V18 | Session history <= 20 files (consolidate if more) | MINOR | run memory_consolidate |

## Pass Criteria
- All CRITICAL: PASS
- MAJOR violations: 0
- MINOR violations: ≤ 3

## Validation Output Format

```yaml
# validation_report.yaml
validation:
  timestamp: "2026-02-20T10:30:00"
  vault_path: "./my_vault"
  overall: PASS | FAIL
  
  checks:
    V1_all_nodes_have_md:     {status: PASS, count: 87}
    V2_wikilinks_resolve:     {status: PASS, broken: []}
    V3_zpd_in_range:          {status: FAIL, violations: [{node: "spare_receptors", delta: 0.47}]}
    V4_open_questions_set:    {status: PASS}
    V5_zeigarnik_closed:      {status: PASS}
    V6_topology_eta:          {status: PASS, eta: 0.94}
    V7_no_orphans:            {status: PASS}
    V8_status_consistent:     {status: PASS}
    V9_criticality_current:   {status: PASS}
    V10_canvas_layout:        {status: PASS}
  
  action_required:
    - "V3: Insert scaffold before spare_receptors (delta=0.47 > 0.40)"
```

## Auto-Fix Protocol

```bash
# Attempt automatic fixes (safe operations only)
python scripts/validate_vault.py --vault ./my_vault --auto-fix

# Auto-fixable:
#   V3: insert scaffold nodes where Δ > 0.40
#   V5: re-derive open_questions using derive_tension()
#   V8: recompute status from mastery values

# Auto-fixable (self-distillation):
#   V12: clear retention_alert after compound_update
#   V13: recompute self_demo_sources from current mastery state
#   V14: run gkg_refine.py to recalibrate difficulty

# NOT auto-fixable (require human decision):
#   V1: missing nodes (may indicate GKG scope error)
#   V2: broken wikilinks (may indicate renamed notes)
#   V6: topology violations (may require domain restructure)
#   V11: retention probe placement (may require path restructure)
```
