#!/usr/bin/env python3
"""
Meta-Compound v3 — BCME Theorem Integration
=============================================
Implements the Bounded Contextual Monotone Escape algorithm for learning.

F6: Parameter auto-tuning (HyperAgents, SDPO, SDFT)
F7: Mechanism injection > parameter tuning (Bilevel AutoResearch)
F8: Tabu memory for failed strategies (Bilevel: Tabu Search)
F9: Orthogonal exploration (Bilevel: dimensional diversity)
G1: Formal stall = low mean + low variance (BCME Definition 2.5)
G2: Candidate scoring J(c) with multi-criteria (BCME Section 7.7)
G3: Invariant extraction before mechanism swap (BCME Claim 3)
G4: Transfer probing after injection (BCME Section 7.9)
G5: Forced revision fallback when registry exhausted (BCME Section 7.8)
G6: Plateau taxonomy with typed diagnosis (BCME Section 8.3)
G7: 7-slot mechanism registry: repr + generator + traversal + eval + pruning + abstraction + modality

Cross-references:
  Spec: 08-self-distillation-integration (F6-F9, G1-G7 detailed specs)
  Uses: 01-theoretical-core (compound learning theory), 02-pkg-gkg-differential (coverage metrics)
  Input: compound_update (session_delta*.yaml prediction_errors + error_distribution),
         memory_consolidate (consolidated epoch history for long-term trends)
  Feeds: mcmc_traversal (mechanism selection → traversal policy), gkg_refine (difficulty errors),
         validate_vault (V15 tabu exhaustion, V16 cluster coverage),
         self_eval (section 3: registry coherence, section 4: plateau detection)
  Theory: 03-mcmc-hamiltonian (MCMC kernel affected by mechanism swaps),
          04-node-schema (frontmatter fields affected by param tuning)

Usage:
    python meta_compound.py --vault ./my_vault --history . --output meta_report.yaml
"""

import yaml, json, argparse
from pathlib import Path
from statistics import mean, variance as stat_variance
from datetime import date
from collections import Counter


def clamp(v, lo, hi): return max(lo, min(hi, v))


# ═══════════════════════════════════════════════════════════
# PARAMETER BOUNDS (F6)
# ═══════════════════════════════════════════════════════════
PARAM_BOUNDS = {
    'alpha': (0.10, 0.50),
    'zpd_delta_target': (0.15, 0.35),
    'retention_probe_freq': (3, 10),
}

DEFAULTS = {
    'alpha': 0.30,
    'zpd_delta_target': 0.22,
    'retention_probe_freq': 5,
    'mastered_threshold': 0.85,
    'active_mechanisms': {
        'representation': 'repr_causal_graph',
        'generator': 'gen_mechanism_chain',
        'traversal': 'trav_centrality_first',
        'evaluation': 'eval_mastery_delta',
        'pruning': 'prune_zpd_bound',
        'abstraction': 'abs_primitive',
        'modality': 'mod_verbal',
    },
    'tabu_list': [],
    'tabu_horizon': 5,
    'stall_window': 5,
    'stall_epsilon': 0.02,
    'stall_variance_max': 0.01,
}

# ═══════════════════════════════════════════════════════════
# G7: 7-SLOT MECHANISM REGISTRY (BCME search law S = X,G,T,Q,P,A,M)
# ═══════════════════════════════════════════════════════════
MECHANISM_REGISTRY = {
    'representation': {
        'repr_causal_graph': 'Organise by mechanism chains and causal links (default)',
        'repr_comparison_table': 'Organise by paired contrast between similar concepts',
        'repr_equation_first': 'Start from governing equation, derive all concepts from terms',
        'repr_clinical_scenario': 'Anchor each concept in a clinical case requiring it',
    },
    'generator': {
        'gen_mechanism_chain': 'Produce answers by tracing causal mechanism step by step (default)',
        'gen_retrieval_practice': 'Closed-book recall before any review; score attempts',
        'gen_elaborative_interrogation': 'Ask "why does this work?" for every claim',
        'gen_teach_back': 'Explain the concept as if teaching a peer',
    },
    'traversal': {
        'trav_centrality_first': 'MCMC weighted toward high-centrality gateway nodes (default)',
        'trav_cluster_rotation': 'Force rotation through ALL clusters before revisiting',
        'trav_weakest_first': 'Target lowest-mastery nodes regardless of centrality',
        'trav_interleaved': 'Alternate high-centrality and low-mastery; mix clusters',
    },
    'evaluation': {
        'eval_mastery_delta': 'Score by mastery improvement after session (default)',
        'eval_transfer_probe': 'Score by performance on novel items not previously studied',
        'eval_explanation_depth': 'Score by quality of self-explanation / mechanism trace',
        'eval_discrimination': 'Score by ability to distinguish similar concepts',
    },
    'pruning': {
        'prune_zpd_bound': 'Skip nodes outside ZPD range [0.10, 0.40] (default)',
        'prune_diminishing_returns': 'Skip nodes where last 3 sessions showed < 0.02 gain',
        'prune_prerequisite_gate': 'Skip nodes whose prerequisites are not yet mastered',
        'prune_time_aware': 'Skip nodes that exceed remaining time budget',
    },
    'abstraction': {
        'abs_primitive': 'Work at molecular/cellular/first-principles level (default for L1)',
        'abs_systems': 'Work at organ-system/integrated-physiology level',
        'abs_clinical': 'Work at bedside/clinical-decision level',
        'abs_governing_equation': 'Work at the single governing equation that unifies the domain',
    },
    'modality': {
        'mod_verbal': 'Text-based study: reading, writing, self-explanation (default)',
        'mod_visual': 'Diagram-based: draw mechanisms, concept maps, flowcharts',
        'mod_symbolic': 'Equation-based: derive quantitative relationships, solve problems',
        'mod_multimodal': 'Combine verbal + visual + symbolic in each session',
    },
}


def load_current_params(vault_path: Path) -> dict:
    meta_path = vault_path / 'meta_lessons.yaml'
    if meta_path.exists():
        meta = yaml.safe_load(meta_path.read_text()) or {}
        params = dict(DEFAULTS)
        if 'current_params' in meta:
            for k, v in meta['current_params'].items():
                params[k] = v
        return params
    return dict(DEFAULTS)


def load_session_history(history_dir: Path) -> list:
    sessions = []
    for f in sorted(history_dir.glob("session_delta*.yaml")):
        report = yaml.safe_load(f.read_text()) or {}
        sessions.append(report)
    return sessions


# ═══════════════════════════════════════════════════════════
# G1: FORMAL STALL DETECTION (mean + variance)
# ═══════════════════════════════════════════════════════════
def detect_stall(sessions, window=5, epsilon=0.02, variance_max=0.01):
    """BCME Definition 2.5: stall = low mean delta AND low variance.
    
    Low mean alone could be noise. Low variance confirms stable plateau.
    Returns (is_stalled, diagnostics).
    """
    if len(sessions) < window + 1:
        return False, {'reason': 'insufficient_history'}

    coverages = [s.get('coverage_after', 0) for s in sessions[-(window + 1):]]
    deltas = [coverages[i + 1] - coverages[i] for i in range(len(coverages) - 1)]

    mean_delta = mean(deltas)
    var_delta = stat_variance(deltas) if len(deltas) > 1 else 0.0

    is_stalled = (mean_delta <= epsilon) and (var_delta <= variance_max)

    return is_stalled, {
        'mean_delta': round(mean_delta, 4),
        'var_delta': round(var_delta, 6),
        'window': window,
        'stalled': is_stalled,
        'reason': 'stable_plateau' if is_stalled else (
            'noisy_but_progressing' if mean_delta > epsilon else 'noisy_stall'
        ),
    }


# ═══════════════════════════════════════════════════════════
# G6: PLATEAU TAXONOMY
# ═══════════════════════════════════════════════════════════
PLATEAU_TYPES = {
    'fluency': {
        'signature': 'high confidence_before but low actual scores',
        'revision_slots': ['generator', 'evaluation'],
        'recommended': {'generator': 'gen_retrieval_practice', 'evaluation': 'eval_transfer_probe'},
    },
    'recall': {
        'signature': 'retrieval_failure dominant in error_types',
        'revision_slots': ['representation', 'generator'],
        'recommended': {'representation': 'repr_causal_graph', 'generator': 'gen_elaborative_interrogation'},
    },
    'application': {
        'signature': 'integration_failure dominant; concept_scores high on core but low on clinical',
        'revision_slots': ['representation', 'traversal'],
        'recommended': {'representation': 'repr_clinical_scenario', 'traversal': 'trav_interleaved'},
    },
    'explanation': {
        'signature': 'low self_explanation_quality across sessions',
        'revision_slots': ['generator', 'evaluation'],
        'recommended': {'generator': 'gen_teach_back', 'evaluation': 'eval_explanation_depth'},
    },
    'discrimination': {
        'signature': 'false_connection or misconception dominant; confusion between similar nodes',
        'revision_slots': ['representation', 'evaluation'],
        'recommended': {'representation': 'repr_comparison_table', 'evaluation': 'eval_discrimination'},
    },
    'speed': {
        'signature': 'high time_spent_minutes with adequate accuracy',
        'revision_slots': ['pruning', 'abstraction'],
        'recommended': {'pruning': 'prune_time_aware', 'abstraction': 'abs_governing_equation'},
    },
    'calibration': {
        'signature': 'systematic overconfidence: confidence_before >> actual score',
        'revision_slots': ['evaluation', 'generator'],
        'recommended': {'evaluation': 'eval_transfer_probe', 'generator': 'gen_retrieval_practice'},
    },
}


def classify_plateau(sessions, n_recent=5):
    """G6: Identify plateau type from error patterns + concept scores + time + calibration."""
    if len(sessions) < n_recent:
        return 'unknown', {}

    recent = sessions[-n_recent:]
    error_counts = Counter()
    concept_profile = {'core': [], 'clinical': []}
    conf_errors = []    # N2: confidence_before - actual_score
    time_spent = []     # N6: time per node

    for s in recent:
        for e_type, count in s.get('error_distribution', {}).items():
            error_counts[e_type] += count
        for d in s.get('deltas', []):
            fb = d if isinstance(d, dict) else {}
            cs = fb.get('concept_scores', {})
            if 'core_mechanism' in cs:
                concept_profile['core'].append(cs['core_mechanism'])
            if 'clinical_application' in cs:
                concept_profile['clinical'].append(cs['clinical_application'])
        # Collect prediction errors for calibration detection
        for pe in s.get('prediction_errors', []):
            if 'prediction_error' in pe:
                conf_errors.append(pe['prediction_error'])

    total_errors = sum(error_counts.values())

    # N2: Calibration plateau — systematic overconfidence
    if conf_errors and len(conf_errors) >= 5:
        mean_conf_err = mean(conf_errors)
        if mean_conf_err > 0.15:
            return 'calibration', {'mean_overconfidence': round(mean_conf_err, 3),
                                   'n_samples': len(conf_errors)}

    if total_errors == 0:
        return 'unknown', {'reason': 'no_errors_recorded'}

    top_error = error_counts.most_common(1)[0][0] if error_counts else None

    if top_error == 'retrieval_failure' and error_counts['retrieval_failure'] > total_errors * 0.4:
        return 'recall', {'dominant_error': 'retrieval_failure',
                          'rate': error_counts['retrieval_failure'] / total_errors}

    if top_error in ('false_connection', 'misconception'):
        return 'discrimination', {'dominant_error': top_error}

    if top_error == 'integration_failure':
        if concept_profile['core'] and concept_profile['clinical']:
            core_mean = mean(concept_profile['core'])
            clin_mean = mean(concept_profile['clinical'])
            if core_mean > 0.6 and clin_mean < 0.4:
                return 'application', {'core': round(core_mean, 2),
                                       'clinical': round(clin_mean, 2)}

    if top_error == 'incomplete_mechanism':
        return 'explanation', {'dominant_error': 'incomplete_mechanism'}

    # N6: Speed plateau — adequate accuracy but excessive time
    for s in recent:
        for d in s.get('deltas', []):
            t = d.get('time_spent_minutes', 0)
            score = d.get('mastery_new', 0)
            if t > 0:
                time_spent.append((t, score))
    if time_spent and len(time_spent) >= 3:
        avg_time = mean([t for t, _ in time_spent])
        avg_score = mean([s for _, s in time_spent])
        if avg_time > 20 and avg_score > 0.65:
            return 'speed', {'avg_time_minutes': round(avg_time, 1),
                             'avg_score': round(avg_score, 2)}

    # N7: Fluency plateau — high confidence but poor actual performance
    fluency_signals = []
    for s in recent:
        for d in s.get('deltas', []):
            fb = d if isinstance(d, dict) else {}
            cb = fb.get('confidence_before', None)
            actual = fb.get('mastery_new', fb.get('score', None))
            if cb is not None and actual is not None:
                fluency_signals.append((cb, actual))
    if fluency_signals and len(fluency_signals) >= 3:
        avg_conf = mean([c for c, _ in fluency_signals])
        avg_actual = mean([a for _, a in fluency_signals])
        if avg_conf > 0.6 and avg_actual < 0.5:
            return 'fluency', {'avg_confidence': round(avg_conf, 2),
                               'avg_actual': round(avg_actual, 2)}

    return 'recall', {'fallback': True, 'top_error': top_error}


# ═══════════════════════════════════════════════════════════
# G3: INVARIANT EXTRACTION
# ═══════════════════════════════════════════════════════════
def extract_invariants(sessions, current_mechanisms):
    """Identify what's currently working BEFORE proposing changes.
    
    BCME Claim 3: each step must preserve useful invariants.
    Returns set of mechanism slots + clusters that should NOT be changed.
    """
    protected = {'mechanisms': set(), 'clusters': set()}

    if len(sessions) < 3:
        return protected

    recent = sessions[-3:]

    # Identify clusters with positive improvement trajectory
    cluster_deltas = Counter()
    cluster_counts = Counter()
    for s in recent:
        for d in s.get('deltas', []):
            node = d.get('node', '')
            parts = node.split('_')
            if len(parts) >= 2:
                cluster = parts[1]
                cluster_deltas[cluster] += d.get('delta', 0)
                cluster_counts[cluster] += 1

    for cluster, total_delta in cluster_deltas.items():
        if cluster_counts[cluster] >= 2 and total_delta > 0.05:
            protected['clusters'].add(cluster)

    # Identify mechanism slots that are producing gains
    # If coverage improved in last 3 sessions, current mechanisms are partly working
    coverages = [s.get('coverage_after', 0) for s in recent]
    if len(coverages) >= 2 and coverages[-1] > coverages[0]:
        # Some progress — protect the currently active mechanism in the slot
        # that corresponds to the improving clusters
        if protected['clusters']:
            protected['mechanisms'].add('traversal')  # traversal is working

    return protected


# ═══════════════════════════════════════════════════════════
# G2: CANDIDATE SCORING J(c)
# ═══════════════════════════════════════════════════════════
def score_candidate(candidate, invariants, plateau_type,
                    gain_weight=0.40, preservation_weight=0.25,
                    contextual_weight=0.20, risk_weight=0.15):
    """BCME Section 7.7: multi-criteria candidate selection.
    
    J(c) = alpha*gain + beta*preservation + gamma*context - lambda*risk
    """
    # Expected gain: how well does this mechanism match the plateau type?
    if plateau_type in PLATEAU_TYPES:
        pt = PLATEAU_TYPES[plateau_type]
        if candidate['slot'] in pt['revision_slots']:
            expected_gain = 0.8  # high match
        else:
            expected_gain = 0.3  # low match — wrong axis
    else:
        expected_gain = 0.5

    # Preservation: does this change break any protected invariants?
    preservation = 1.0
    if candidate['slot'] in invariants.get('mechanisms', set()):
        preservation = 0.3  # changing a working mechanism — risky

    # Contextual gain: is this mechanism new (high context) or recently tried (low)?
    contextual = 0.7  # default moderate

    # Risk: is this a large change (switching representation) or small (switching pruning)?
    slot_risk = {'representation': 0.8, 'generator': 0.6, 'traversal': 0.4,
                 'evaluation': 0.3, 'pruning': 0.2, 'abstraction': 0.5, 'modality': 0.3}
    risk = slot_risk.get(candidate['slot'], 0.5)

    score = (gain_weight * expected_gain +
             preservation_weight * preservation +
             contextual_weight * contextual -
             risk_weight * risk)

    return round(score, 4)


# ═══════════════════════════════════════════════════════════
# F6: PARAMETER TUNING
# ═══════════════════════════════════════════════════════════
def tune_alpha(sessions, current_alpha):
    errors = []
    for s in sessions:
        for pe in s.get('prediction_errors', []):
            if 'prediction_error' in pe:
                errors.append(pe['prediction_error'])
    if len(errors) < 10:
        return {'adjusted': False, 'reason': f'Insufficient data ({len(errors)} < 10)'}
    me = mean(errors)
    if abs(me) > 0.08:
        lo, hi = PARAM_BOUNDS['alpha']
        new = clamp(current_alpha + 0.3 * me, lo, hi)
        return {'adjusted': True, 'old': current_alpha, 'new': round(new, 3),
                'mean_error': round(me, 4), 'n': len(errors)}
    return {'adjusted': False, 'reason': f'|{me:.4f}| <= 0.08'}


def tune_zpd(sessions, current_target):
    total, trivial = 0, 0
    for s in sessions:
        for d in s.get('deltas', []):
            if d.get('status') in ('gap', 'in-progress'):
                total += 1
                if d.get('mastery_new', 0) > 0.80 and d.get('mastery_old', 0) < 0.3:
                    trivial += 1
    if total < 10:
        return {'adjusted': False, 'reason': f'Insufficient data ({total} < 10)'}
    rate = trivial / total
    lo, hi = PARAM_BOUNDS['zpd_delta_target']
    if rate > 0.50:
        return {'adjusted': True, 'old': current_target,
                'new': round(min(hi, current_target + 0.03), 3),
                'reason': f'Trivial rate {rate:.0%} > 50%'}
    return {'adjusted': False, 'reason': f'Trivial rate {rate:.0%} within range'}


# ═══════════════════════════════════════════════════════════
# F7+G2+G3+G6: MECHANISM EVALUATION + INJECTION (BCME-aware)
# ═══════════════════════════════════════════════════════════
def evaluate_mechanisms(sessions, current_mechanisms, tabu_list, plateau_type, invariants):
    """Generate, score, and rank candidate mechanism swaps.
    
    BCME pipeline: classify_plateau -> extract_invariants -> generate candidates
    -> score with J(c) -> filter admissible -> rank -> select best.
    """
    if plateau_type == 'unknown':
        return []

    tabu_set = set(t.get('mechanism', '') for t in tabu_list)
    active_set = set(current_mechanisms.values()) if isinstance(current_mechanisms, dict) else set(current_mechanisms)

    # Generate candidates from plateau-recommended mechanisms
    candidates = []
    if plateau_type in PLATEAU_TYPES:
        pt = PLATEAU_TYPES[plateau_type]
        for slot, recommended_mech in pt['recommended'].items():
            current_in_slot = current_mechanisms.get(slot, '') if isinstance(current_mechanisms, dict) else ''
            if recommended_mech != current_in_slot and recommended_mech not in tabu_set:
                candidates.append({
                    'slot': slot,
                    'current': current_in_slot,
                    'proposed': recommended_mech,
                    'reason': f'{plateau_type} plateau -> {slot} revision',
                })

    # Also generate non-plateau-specific candidates from registry
    for slot, mechanisms in MECHANISM_REGISTRY.items():
        current_in_slot = current_mechanisms.get(slot, '') if isinstance(current_mechanisms, dict) else ''
        for mech_name in mechanisms:
            if mech_name != current_in_slot and mech_name not in tabu_set:
                if not any(c['proposed'] == mech_name for c in candidates):
                    candidates.append({
                        'slot': slot,
                        'current': current_in_slot,
                        'proposed': mech_name,
                        'reason': f'registry exploration for {slot}',
                    })

    # G2: Score all candidates
    for c in candidates:
        c['score'] = score_candidate(c, invariants, plateau_type)

    # Filter admissible: score > 0.3
    admissible = [c for c in candidates if c['score'] > 0.3]

    # Rank by score descending
    admissible.sort(key=lambda c: -c['score'])

    # Return top 2 (minimal revision principle — BCME Corollary 2)
    return admissible[:2]


# ═══════════════════════════════════════════════════════════
# G5: FORCED REVISION FALLBACK
# ═══════════════════════════════════════════════════════════
def forced_revision(current_mechanisms, tabu_list, plateau_type):
    """When no admissible candidate exists, force a revision.
    
    BCME Section 7.8: select the most-likely-blocking axis and mutate.
    Strategy: reset tabu for the slot most relevant to the plateau type,
    then try the mechanism with the oldest tabu entry.
    """
    if plateau_type in PLATEAU_TYPES:
        target_slots = PLATEAU_TYPES[plateau_type]['revision_slots']
    else:
        target_slots = list(MECHANISM_REGISTRY.keys())

    # Find oldest tabu entry in target slots
    oldest = None
    oldest_age = -1
    for entry in tabu_list:
        mech = entry.get('mechanism', '')
        for slot in target_slots:
            if mech in MECHANISM_REGISTRY.get(slot, {}):
                age = entry.get('added_at', 0)
                if oldest is None or age < oldest_age:
                    oldest = entry
                    oldest_age = age

    if oldest:
        # Remove the oldest entry from tabu (give it another chance)
        mech = oldest['mechanism']
        slot = None
        for s in target_slots:
            if mech in MECHANISM_REGISTRY.get(s, {}):
                slot = s
                break

        return {
            'action': 'forced_revision',
            'removed_from_tabu': mech,
            'slot': slot,
            'proposed': mech,
            'reason': f'All candidates exhausted; retrying oldest tabu entry for {slot}',
        }

    return {'action': 'no_revision_possible', 'reason': 'Registry exhausted and no tabu to clear'}


# ═══════════════════════════════════════════════════════════
# F8: TABU LIST MANAGEMENT
# ═══════════════════════════════════════════════════════════
def update_tabu_list(tabu_list, new_entries, tabu_horizon, session_count):
    active = [t for t in tabu_list if session_count - t.get('added_at', 0) < tabu_horizon]
    for entry in new_entries:
        entry['added_at'] = session_count
        active.append(entry)
    return active


# ═══════════════════════════════════════════════════════════
# G4: TRANSFER PROBE SCHEDULING
# ═══════════════════════════════════════════════════════════
def schedule_transfer_probes(mechanism_recently_swapped, sessions):
    """After a mechanism swap, schedule 4-type probe suite for next session.
    
    BCME PROBE_TRANSFER: retention + transfer + inversion + explanation.
    - Retention: can you still recall previously mastered material?
    - Transfer: can you apply the concept to a novel context?
    - Inversion: can you work the concept backwards? (given output, derive input)
    - Explanation: can you explain WHY the mechanism works, not just WHAT it does?
    """
    if not mechanism_recently_swapped:
        return None

    return {
        'transfer_probes_scheduled': True,
        'probe_types': ['retention', 'transfer', 'inversion', 'explanation'],
        'reason': f'Mechanism swap detected; next session includes 4-type probe suite',
        'swapped_mechanisms': mechanism_recently_swapped,
        'probe_descriptions': {
            'retention': 'Re-test 2 random mastered nodes from prior sessions',
            'transfer': 'Apply concept to a novel clinical scenario not previously studied',
            'inversion': 'Given the output/effect, derive the mechanism that produces it',
            'explanation': 'Explain WHY (not just WHAT) — trace causal chain to first principles',
        },
    }


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(description="Meta-Compound v3 (BCME)")
    ap.add_argument("--vault", required=True)
    ap.add_argument("--history", default=".", help="Dir with session_delta*.yaml")
    ap.add_argument("--output", default="meta_report.yaml")
    args = ap.parse_args()

    vp = Path(args.vault)
    hp = Path(args.history)
    params = load_current_params(vp)
    sessions = load_session_history(hp)
    session_count = len(sessions)
    current_mechanisms = params.get('active_mechanisms', DEFAULTS['active_mechanisms'])

    # ── G1: Formal stall detection ────────────────────────
    is_stalled, stall_diag = detect_stall(
        sessions,
        window=params.get('stall_window', 5),
        epsilon=params.get('stall_epsilon', 0.02),
        variance_max=params.get('stall_variance_max', 0.01),
    )

    # ── F6: Parameter tuning (always runs) ────────────────
    alpha_result = tune_alpha(sessions, params['alpha'])
    zpd_result = tune_zpd(sessions, params['zpd_delta_target'])

    # ── G6: Plateau classification (only if stalled) ──────
    plateau_type = 'unknown'
    plateau_diag = {}
    mechanism_suggestions = []
    forced = None
    transfer_schedule = None

    if is_stalled:
        plateau_type, plateau_diag = classify_plateau(sessions)

        # ── G3: Invariant extraction ──────────────────────
        invariants = extract_invariants(sessions, current_mechanisms)

        # ── F7+G2: Mechanism evaluation + scoring ─────────
        tabu_names = [t.get('mechanism', '') for t in params.get('tabu_list', [])]
        mechanism_suggestions = evaluate_mechanisms(
            sessions, current_mechanisms, params.get('tabu_list', []),
            plateau_type, invariants
        )

        # ── G5: Forced revision if no candidates ─────────
        if not mechanism_suggestions:
            forced = forced_revision(current_mechanisms, params.get('tabu_list', []), plateau_type)

    # ── F8: Tabu update ───────────────────────────────────
    tabu_new = []
    if session_count >= 2 and is_stalled:
        for m in params.get('recently_swapped', []):
            tabu_new.append({'mechanism': m, 'reason': 'No improvement after injection'})

    tabu_list = update_tabu_list(
        params.get('tabu_list', []), tabu_new,
        params.get('tabu_horizon', 5), session_count
    )

    # ── Apply changes ─────────────────────────────────────
    new_params = dict(params)
    changes = []

    for name, result in [('alpha', alpha_result), ('zpd_delta_target', zpd_result)]:
        if result.get('adjusted'):
            new_params[name] = result['new']
            changes.append(f"PARAM {name}: {result.get('old')} -> {result['new']}")

    recently_swapped = []
    if mechanism_suggestions:
        # Apply top candidate (highest J(c) score)
        best = mechanism_suggestions[0]
        if isinstance(new_params['active_mechanisms'], dict):
            new_params['active_mechanisms'][best['slot']] = best['proposed']
        recently_swapped.append(best['proposed'])
        changes.append(
            f"MECHANISM {best['slot']}: {best['current']} -> {best['proposed']} "
            f"(score={best['score']}, reason={best['reason']})"
        )
    elif forced and forced.get('action') == 'forced_revision':
        # Apply forced revision
        if isinstance(new_params['active_mechanisms'], dict):
            new_params['active_mechanisms'][forced['slot']] = forced['proposed']
        recently_swapped.append(forced['proposed'])
        # Remove from tabu
        tabu_list = [t for t in tabu_list if t.get('mechanism') != forced['removed_from_tabu']]
        changes.append(f"FORCED {forced['slot']}: -> {forced['proposed']} ({forced['reason']})")

    # ── G4: Schedule transfer probes ──────────────────────
    transfer_schedule = schedule_transfer_probes(recently_swapped, sessions)

    # ── N5: Consolidation check (when NOT stalled + sustained gain) ──
    consolidation = None
    if not is_stalled and len(sessions) >= 3:
        recent_3 = [s.get('coverage_after', 0) for s in sessions[-3:]]
        if len(recent_3) == 3 and recent_3[2] > recent_3[1] > recent_3[0]:
            consolidation = {
                'recommended': True,
                'reason': '3+ consecutive sessions with monotone coverage gain',
                'actions': [
                    'Merge related mastered nodes that are always recalled together',
                    'Compress context model: remove redundant scaffolding from mastered nodes',
                    'Extract invariants from newly mastered material into Sigma',
                    'Run gkg_refine to update difficulty estimates from new data',
                ],
                'coverage_trajectory': recent_3,
            }
            changes.append(f"CONSOLIDATE: sustained gain detected ({recent_3})")

    new_params['tabu_list'] = tabu_list
    new_params['recently_swapped'] = recently_swapped

    # ── Persist ───────────────────────────────────────────
    meta = {
        'last_meta_compound': date.today().isoformat(),
        'current_params': new_params,
        'bcme_diagnostics': {
            'stall': stall_diag,
            'plateau_type': plateau_type,
            'plateau_details': plateau_diag,
            'invariants_protected': {
                'mechanisms': list(extract_invariants(sessions, current_mechanisms).get('mechanisms', set())),
                'clusters': list(extract_invariants(sessions, current_mechanisms).get('clusters', set())),
            } if is_stalled else {},
        },
        'tuning_results': {
            'alpha': alpha_result,
            'zpd_delta_target': zpd_result,
            'mechanism_suggestions': mechanism_suggestions,
            'forced_revision': forced,
            'transfer_probes': transfer_schedule,
            'consolidation': consolidation,
            'tabu_list': tabu_list,
            'tabu_new': tabu_new,
        },
        'history': [],
    }

    existing_meta_path = vp / 'meta_lessons.yaml'
    if existing_meta_path.exists():
        existing = yaml.safe_load(existing_meta_path.read_text()) or {}
        old_history = existing.get('history', [])
        old_history.append({
            'date': date.today().isoformat(),
            'session_count': session_count,
            'stalled': is_stalled,
            'plateau_type': plateau_type,
            'changes': changes,
        })
        meta['history'] = old_history[-20:]

    existing_meta_path.write_text(yaml.dump(meta, default_flow_style=False))
    Path(args.output).write_text(yaml.dump(meta, default_flow_style=False))

    print(f"{'STALL' if is_stalled else 'OK'} Meta-compound v3 (BCME)")
    if is_stalled:
        print(f"   Plateau: {plateau_type} ({stall_diag.get('reason', '')})")
        print(f"   Mean delta: {stall_diag.get('mean_delta', '?')}, Var: {stall_diag.get('var_delta', '?')}")
    if changes:
        for c in changes:
            print(f"   {c}")
    else:
        print(f"   No changes needed")
    if transfer_schedule:
        print(f"   Transfer probes scheduled for next session")
    if consolidation:
        print(f"   CONSOLIDATE: {consolidation['reason']}")
    if tabu_list:
        print(f"   Tabu: {[t['mechanism'] for t in tabu_list]}")


if __name__ == "__main__":
    main()
