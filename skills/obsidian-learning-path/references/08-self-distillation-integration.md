<!--
DIRECTORY TREE (orientation)
references/08-self-distillation-integration.md
  Covers: F1 dense credit · F2 evolving GKG · F3 self-as-teacher ·
          F4 retention probes · F5 rich feedback · F6 meta-compound
  Depends on: 01-theoretical-core (compound loop), 02-pkg-gkg-differential (gap algebra)
  Used by: /path compound · /path refine · /path meta · /path traverse
-->

# Self-Distillation Integration

> Cross-integration of SDFT, SDPO, HyperAgents, Karpathy AutoResearch, and Bilevel
> AutoResearch into the learning path framework.
> All findings experimentally validated with STRONG consensus across ≥2/3 papers.

## Contents
- [Theoretical Foundation](#theoretical-foundation)
- [F1: Dense Credit Assignment](#f1-dense-credit)
- [F2: Evolving GKG](#f2-evolving-gkg)
- [F3: Self-As-Teacher](#f3-self-as-teacher)
- [F4: On-Policy Retention Probes](#f4-retention-probes)
- [F5: Rich Structured Feedback](#f5-rich-feedback)
- [F6: Meta-Compound Loop](#f6-meta-compound)
- [F7: Mechanism Injection > Parameter Tuning](#f7-mechanism-injection--parameter-tuning)
- [F8: Tabu Memory for Failed Strategies](#f8-tabu-memory-for-failed-strategies)
- [F9: Orthogonal Exploration](#f9-orthogonal-exploration)
- [Morphological Mapping](#morphological-mapping)

---

## Theoretical Foundation

The on-policy context-distillation update operator:

```
F(π, C) = argmin_π' KL(π(·|x) ‖ π(·|x, C))
```

maps onto the path skill's compound learning loop as:

```
Learning Signal  = Enriched(Self) − Self
                 = log P(node | context, mastery) − log P(node | mastery)
                 ≅ GKG \ PKG  (gap as self-referential difference)
```

The four-level operator hierarchy (across all 7 systems):
```
Level 4 [Bilevel AutoRes]:  F_inject(F_meta, mechanisms) -- new search strategies
Level 3 [HyperAgents]:      F_meta(H, A)                -- modify improvement procedure
Level 2 [SDPO]:              F_rl(pi, f)                 -- modify policy via feedback
Level 1 [SDFT/AutoRes]:      F_demo(pi, c)               -- modify policy via demos/ratchet
```

The four invariant components of effective learning:
1. **Self-referential gap detection** — Δ between context-enriched and context-free self
2. **On-policy traversal** — learning from where you actually are, not idealised trajectories
3. **Proximity-bounded update** — ZPD ∈ [0.10, 0.40] ≅ trust-region / EMA stabiliser
4. **Iterative compounding** — K' ⊇ K, monotonic knowledge accumulation

---

## F1: Dense Credit Assignment

**Paper evidence**: SDPO demonstrates logit-level > token-level > sequence-level
advantages. 4× fewer generations to reach GRPO accuracy. SDFT provides per-position
KL signal. HyperAgents tracks per-modification causal attribution.

**Previous state**: `session.json` = `[{"node_id": X, "score": 0.75}]` — single scalar.

**New session schema**:

```json
{
  "node_id": "L2_receptor_theory_03",
  "feedback": {
    "concept_scores": {
      "core_mechanism": 0.85,
      "clinical_application": 0.60,
      "quantitative_relationships": 0.40,
      "integration_with_prerequisites": 0.70
    },
    "error_types": ["calculation_error", "incomplete_mechanism"],
    "retrieval_success": true,
    "self_explanation_quality": 0.65,
    "confidence_before": 0.50,
    "confidence_after": 0.70,
    "misconceptions_identified": ["confused Kd with Ki"],
    "time_spent_minutes": 18
  }
}
```

**Multi-signal mastery EMA**:

```python
def dense_ema_update(old_mastery, feedback, alpha=0.30):
    """Weighted multi-signal mastery update replacing scalar EMA."""
    weights = {
        'core_mechanism': 0.35,
        'clinical_application': 0.25,
        'quantitative_relationships': 0.25,
        'integration_with_prerequisites': 0.15
    }
    concept_scores = feedback['concept_scores']
    weighted_score = sum(
        weights.get(k, 0.25) * v 
        for k, v in concept_scores.items()
    ) / sum(weights.values())
    
    # Calibration adjustment: penalise overconfidence, reward accurate self-assessment
    calibration = 1.0 - abs(feedback['confidence_before'] - old_mastery)
    
    effective_score = weighted_score * (0.8 + 0.2 * calibration)
    return round((1 - alpha) * old_mastery + alpha * effective_score, 4)
```

**Backward compatibility**: If session.json contains plain `{"node_id": X, "score": Y}`,
compound_update.py falls back to scalar EMA. No breaking change.

---

## F2: Evolving GKG

**Paper evidence**: SDPO Fig 10-right — self-teacher improves during training, final
student surpasses initial teacher. SDFT EMA teacher tracks improvement (ablation:
EMA > frozen > raw student). HyperAgents archive quality improves across generations.

**Previous state**: `GKG = RPP(domain)` computed once, frozen. Difficulty values static.

**GKG refinement protocol** (triggered by `/path refine`, recommended every 5-10 sessions):

```python
def refine_gkg(gkg, vault_performance_history):
    """Evolve the GKG from accumulated learner performance data."""
    
    refinements = {'difficulty_recalibrated': [], 'edges_added': [], 
                   'nodes_split': [], 'nodes_merged': []}
    
    for node in gkg.nodes:
        history = vault_performance_history.get(node.id, [])
        if len(history) < 3:
            continue
        
        # 1. DIFFICULTY RECALIBRATION
        #    If learners consistently score higher/lower than difficulty predicts,
        #    recalibrate. This is the "teacher improves" mechanism.
        avg_score = mean([h['score'] for h in history])
        predicted_difficulty = node.difficulty
        error = avg_score - (1.0 - predicted_difficulty)  # expected_score = 1 - difficulty
        
        if abs(error) > 0.15:  # significant miscalibration
            node.difficulty = clamp(predicted_difficulty - 0.5 * error, 0.05, 0.95)
            refinements['difficulty_recalibrated'].append(node.id)
        
        # 2. EDGE DISCOVERY
        #    If learner's feedback shows consistent cross-references between nodes
        #    that aren't connected in GKG, add edge.
        for h in history:
            for prereq_mentioned in h.get('helpful_prerequisites', []):
                if prereq_mentioned not in node.prerequisites:
                    gkg.add_edge(prereq_mentioned, node.id)
                    refinements['edges_added'].append((prereq_mentioned, node.id))
        
        # 3. NODE SPLITTING
        #    If concept_scores show systematic divergence (some subconcepts mastered,
        #    others not), the node is too coarse.
        if len(history) >= 5:
            concept_variance = variance_of_concept_scores(history)
            if concept_variance > 0.15:  # high within-node divergence
                refinements['nodes_split'].append(node.id)
    
    return refinements
```

**Critical constraint**: GKG refinement preserves RPP level structure. L0 nodes
never split. L3 nodes never merge upward. Refinement operates within-level.

---

## F3: Self-As-Teacher

**Paper evidence**: SDFT — demonstration-conditioned self as teacher. SDPO — successful
rollouts as implicit feedback for failures. HyperAgents — archive stepping stones.

**Previous state**: Gap nodes scaffold from abstract definitions. No mechanism to use
the learner's own mastered understanding as teaching context.

**New frontmatter fields**:

```yaml
# ── Self-Demonstration (F3) ────────────────────────────
self_demo_sources: []          # [[mastered node]] IDs to scaffold from
best_attempt_summary: ""       # learner's own best explanation (captured post-mastery)
scaffold_strategy: "abstract"  # abstract | self_demo | hybrid
```

**Self-demo selection algorithm**:

```python
def select_self_demos(gap_node, pkg, gkg, max_demos=3):
    """Select learner's own mastered nodes as teaching context for a gap node.
    
    Analogous to SDFT's π(·|x,c) where c is the learner's own past success,
    not an external expert demonstration.
    """
    mastered = [n for n in gkg.nodes if pkg.mastery(n.id) >= 0.85]
    
    # Score by: (1) prerequisite relevance, (2) recency, (3) best_attempt quality
    candidates = []
    for m in mastered:
        relevance = 1.0 if m.id in gap_node.prerequisites else (
            0.5 if share_cluster(m, gap_node) else 0.2
        )
        recency = days_since_mastered(m)
        recency_weight = 1.0 / (1.0 + recency / 7.0)  # decay over weeks
        
        has_summary = 1.0 if m.best_attempt_summary else 0.3
        
        candidates.append((m, relevance * recency_weight * has_summary))
    
    candidates.sort(key=lambda x: -x[1])
    return [c[0] for c in candidates[:max_demos]]
```

**In the generated note template**, self-demos appear as:

```markdown
## Scaffold: Your Own Understanding

> Before studying this concept, recall what you already know:
{% for demo in self_demo_sources %}
- **[[{{ demo.title }}]]**: {{ demo.best_attempt_summary }}
{% endfor %}

Now, using this as your foundation, the new concept extends it by...
```

---

## F4: On-Policy Retention Probes

**Paper evidence**: SDFT 3-task sequential experiment — on-policy prevents catastrophic
forgetting; off-policy SFT causes severe regression. SDPO on-policy distribution
matching preserves capabilities. HyperAgents archive prevents regression.

**Previous state**: Spaced repetition exists but decoupled from path traversal.
During active path traversal, mastered nodes never revisited. Resequencing pushes
mastered nodes to end.

**Retention probe protocol**:

```python
RETENTION_PROBE_FREQUENCY = 5  # every K new nodes in path
RETENTION_THRESHOLD = 0.70     # below this triggers re-consolidation

def insert_retention_probes(path, mastered_nodes, freq=RETENTION_PROBE_FREQUENCY):
    """Insert retention checks INTO the traversal path.
    
    Analogous to on-policy sampling: periodically verify that forward
    traversal hasn't caused distribution shift on previously mastered material.
    """
    probed_path = []
    new_node_count = 0
    
    for node in path:
        probed_path.append(node)
        
        if node.status in ('gap', 'in-progress'):
            new_node_count += 1
        
        if new_node_count >= freq and mastered_nodes:
            # Select probe: prefer high-centrality mastered nodes
            # (losing a gateway concept is catastrophic)
            probe = select_probe(mastered_nodes, strategy='centrality_weighted')
            probed_path.append({
                'type': 'retention_probe',
                'node_id': probe.id,
                'title': probe.title,
                'expected_mastery': probe.mastery,
                'action_if_failed': 're-consolidation'
            })
            new_node_count = 0
    
    return probed_path

def process_retention_result(probe_node, actual_score, vault):
    """Handle retention probe outcome."""
    if actual_score < RETENTION_THRESHOLD:
        # Forgetting detected — on-policy correction
        # 1. Boost priority (re-enter active path)
        probe_node.status = 'in-progress'
        probe_node.priority *= 1.5
        # 2. Shorten review interval
        probe_node.next_review = date.today().isoformat()
        # 3. Flag for re-consolidation in next compound update
        probe_node.retention_alert = True
        return 'RE-CONSOLIDATION TRIGGERED'
    else:
        # Retention confirmed — reinforce with EMA
        probe_node.mastery = ema_update(probe_node.mastery, actual_score, alpha=0.15)
        return 'RETENTION CONFIRMED'
```

**Validation check** (added to V-checklist):

```
V11 | Retention probes present every K nodes in path | MAJOR | re-run mcmc_traversal
V12 | No mastered node has retention_alert=True for >7 days | MINOR | run compound_update
```

---

## F5: Rich Structured Feedback

**Paper evidence**: SDPO rich textual feedback (runtime errors, judge evaluations)
dramatically outperforms scalar outcome reward — core RLRF formalization. SDFT
demonstration context outperforms answer-only (89% vs 75%). HyperAgents develop
their own rich feedback infrastructure autonomously.

**Previous state**: `session_score from: self-assessment: [0.0, 0.25, 0.50, 0.75, 1.0]`

**Feedback taxonomy** (standardised error categories for learning):

```yaml
error_types:
  retrieval_failure:     "Could not recall the relevant concept at all"
  partial_retrieval:     "Retrieved concept but missing key details"
  calculation_error:     "Mechanism correct but quantitative error"
  incomplete_mechanism:  "Missing steps in the causal chain"
  false_connection:      "Incorrectly linked to wrong prerequisite"
  overcondensation:      "Correct but insufficient detail for exam standard"
  misconception:         "Held a factually incorrect belief"
  integration_failure:   "Understood parts but couldn't synthesise"
  
confidence_scale:
  0.0: "No idea — pure guess"
  0.25: "Vague familiarity — couldn't explain"
  0.50: "Partial understanding — could outline but not detail"
  0.75: "Good understanding — could explain to peer"
  1.0: "Expert fluency — could teach and handle edge cases"
```

**Feedback → mastery signal mapping**:

```python
ERROR_WEIGHTS = {
    'retrieval_failure': -0.30,     # severe — concept not encoded
    'misconception': -0.25,         # severe — wrong encoding
    'incomplete_mechanism': -0.15,  # moderate — partial encoding
    'false_connection': -0.15,      # moderate — wrong links
    'integration_failure': -0.10,   # moderate — isolated encoding
    'calculation_error': -0.05,     # mild — encoding OK, execution off
    'partial_retrieval': -0.05,     # mild — encoding present but weak
    'overcondensation': -0.02,      # minor — encoding OK, expression brief
}

def feedback_to_mastery_adjustment(feedback):
    """Convert structured feedback into mastery adjustment signal.
    
    Replaces single scalar with weighted multi-signal, analogous to SDPO's
    dense logit-level advantages replacing sparse sequence-level reward.
    """
    base_score = mean(feedback['concept_scores'].values())
    
    # Error penalty (dense credit assignment — specific errors penalised specifically)
    error_penalty = sum(
        ERROR_WEIGHTS.get(e, -0.05) for e in feedback.get('error_types', [])
    )
    
    # Calibration bonus (metacognitive accuracy)
    confidence_error = abs(feedback['confidence_before'] - base_score)
    calibration = max(0, 1.0 - 2 * confidence_error)
    
    # Self-explanation bonus (SDFT: richer context → better signal)
    explanation_bonus = 0.05 * feedback.get('self_explanation_quality', 0.5)
    
    return clamp(base_score + error_penalty + 0.1 * calibration + explanation_bonus, 0.0, 1.0)
```

---

## F6: Meta-Compound Loop

**Paper evidence**: HyperAgents — core contribution: meta-agent modifies its own
modification procedure. Autonomously develops performance tracking, persistent memory,
compute-aware planning. SDPO teacher quality bootstraps. SDFT EMA implicitly adapts.

**Previous state**: Parameters hardcoded or manual in `lessons.md`:
- `α = 0.30` (EMA learning rate)
- `Δ_target = 0.22` (ZPD midpoint)
- `burn_in = 50` (MCMC cold start)
- `RETENTION_PROBE_FREQUENCY = 5`

**Meta-compound protocol** (triggered by `/path meta`, recommended every 10+ sessions):

```python
def meta_compound(vault, history, current_params):
    """Auto-tune learning parameters from accumulated prediction errors.
    
    Analogous to HyperAgents' metacognitive self-modification:
    the improvement procedure improves itself.
    """
    adjustments = {}
    
    # 1. EMA ALPHA TUNING
    #    prediction_error = stored_mastery - session_score at next visit
    #    positive = overestimated mastery (forgetting) → increase alpha
    #    negative = underestimated mastery (consolidated) → decrease alpha
    prediction_errors = []
    for session in history:
        for pe in session.get('prediction_errors', []):
            if 'prediction_error' in pe:
                prediction_errors.append(pe['prediction_error'])
    
    if len(prediction_errors) >= 10:
        mean_error = mean(prediction_errors)
        if abs(mean_error) > 0.08:
            # Systematic bias: adjust alpha
            # Overestimating (mean_error > 0) → increase alpha (faster correction)
            # Underestimating (mean_error < 0) → decrease alpha (trust EMA more)
            alpha_new = clamp(current_params['alpha'] + 0.3 * mean_error, 0.10, 0.50)
            adjustments['alpha'] = alpha_new
    
    # 2. ZPD DELTA TARGET TUNING
    #    If too many scaffold insertions → Δ_target too high
    #    If progression feels trivial (high scores on first attempt) → Δ_target too low
    scaffold_rate = count_scaffolds_inserted(history) / max(count_new_nodes(history), 1)
    trivial_rate = count_first_attempt_above_80(history) / max(count_new_nodes(history), 1)
    
    if scaffold_rate > 0.30:  # more than 30% of edges need scaffolds
        adjustments['zpd_delta_target'] = max(0.15, current_params['zpd_delta_target'] - 0.03)
    elif trivial_rate > 0.50:  # more than 50% trivially easy
        adjustments['zpd_delta_target'] = min(0.35, current_params['zpd_delta_target'] + 0.03)
    
    # 3. RETENTION PROBE FREQUENCY TUNING
    #    If retention probes consistently pass → reduce frequency (less interruption)
    #    If retention failures detected → increase frequency
    probe_results = get_retention_probe_history(history)
    if len(probe_results) >= 5:
        failure_rate = sum(1 for r in probe_results if r < 0.70) / len(probe_results)
        if failure_rate > 0.20:
            adjustments['retention_probe_freq'] = max(3, current_params['retention_probe_freq'] - 1)
        elif failure_rate < 0.05:
            adjustments['retention_probe_freq'] = min(10, current_params['retention_probe_freq'] + 1)
    
    return adjustments
```

**Parameter governance**: All auto-tuned parameters have hard bounds:
- `α ∈ [0.10, 0.50]` — never overfit (>0.50) or underfit (<0.10)
- `Δ_target ∈ [0.15, 0.35]` — always within ZPD bounds
- `retention_probe_freq ∈ [3, 10]` — never too sparse or too frequent
- All changes logged to `meta_lessons.yaml` with timestamp and reason

---

## F7: Mechanism Injection > Parameter Tuning

**Paper evidence**: Bilevel AutoResearch four-group ablation -- Group B (parameter
tuning only via Level 1.5) achieves "essentially zero improvement." Group C
(mechanism injection via Level 2) achieves 5x improvement (-0.045 vs -0.009 val_bpb).
HyperAgents modifies its modification procedure, not just parameters.

**Previous state**: F6 meta_compound.py only tunes alpha, delta_target, retention_probe_freq.

**New state**: Mechanism registry with selectable strategies per pipeline slot:
- **Priority mechanisms**: standard, error-weighted, zpd-proximity, retention-risk
- **Scaffold mechanisms**: abstract, self-demo, error-targeted
- **Traversal mechanisms**: centrality-first, cluster-rotation, weakest-first, interleaved

When the meta-compound detects stall (< 2% coverage improvement over 5 sessions),
it diagnoses the cause from error patterns and cluster coverage, then selects an
alternative mechanism from the registry. Failed mechanisms enter the tabu list.

---

## F8: Tabu Memory for Failed Strategies

**Paper evidence**: Bilevel AutoResearch -- the LLM always tries "larger batch" first
(implicit bias). After failure, Group A repeats the same direction; Group B freezes
the dimension entirely. Only Tabu Search prevents revisiting failed directions and
forces new exploration. HyperAgents archive prevents regression via stepping stones.

**Previous state**: No tabu mechanism. MCMC kernel can revisit failed proposals
indefinitely. When a prerequisite chain does not improve mastery, nothing prevents
reproposing the same chain.

**Tabu protocol**: After each meta-compound cycle, if coverage stalled and a mechanism
was recently swapped, that mechanism enters the tabu list. Tabu entries expire after
tabu_horizon sessions (default 5). Mechanism selection excludes tabu entries.

**Tabu horizon**: Default 5 sessions. If tabu list exhausts all mechanisms in a slot,
reset tabu for that slot and retry with fresh evaluation.

---

## F9: Orthogonal Exploration

**Paper evidence**: Bilevel AutoResearch -- Orthogonal Exploration mechanism forces
the agent to explore dimensions it systematically avoids. Karpathy AutoResearch:
ratchet + single-track loop creates path dependence on early successful directions.

**Previous state**: MCMC proposal strategy is fixed 70/30 local/long-range.
Priority formula always weights same dimensions. No detection of systematic
traversal biases.

**Orthogonal exploration protocol**: Detect skew in cluster/domain coverage across
recent sessions. If one cluster is studied 3x more than another, the traversal has
a bias analogous to the LLM's "larger batch" prior. When bias detected, meta_compound
injects traversal_cluster_rotation mechanism, which forces the MCMC proposal to
rotate through ALL clusters before revisiting any.

---

## v4: Homoiconic Self-Assessment

The skill's own architecture is subject to the same evaluation loop it prescribes
for learners. `self_eval.py` treats the skill's files as a knowledge graph and
tests cross-referential consistency — the same operation the skill performs on
a learner's vault via `validate_vault.py`.

**Correspondence**:
- Learner's vault nodes ↔ Skill's scripts + reference files
- Learner's mastery scores ↔ Self-eval pass/fail rates
- Learner's gap set (GKG \ PKG) ↔ Self-eval failure list
- Learner's compound update ↔ Fix prescription + application
- Learner's session history ↔ Skill's version history
- Learner's memory consolidation ↔ Session history Pareto compression

**Self-correction protocol**:
1. `self_eval.py` runs 141 architectural checks
2. Failures carry typed fix prescriptions (safe/manual)
3. Safe fixes: parameter adjustments applied automatically
4. Structural fixes: flagged for human review
5. Pass rate is the skill's own "mastery score"
6. Rate < 95% = DEGRADED health → triggers investigation

This closes the homoiconic loop: the skill is a node in its own learning graph.

---

## Morphological Mapping

The isomorphisms between the ML papers and path skill that ground these changes:

| ML Papers | Path Skill | Invariant |
|---|---|---|
| Implicit reward: gap between enriched and current self | Gap algebra: GKG \\ PKG | Gap = enriched self - current self |
| Trust-region / EMA | ZPD bounds [0.10, 0.40] | Bounded update step size |
| On-policy sampling | Zeigarnik: tension from current position | Learn from where you are |
| Dense logit-level advantages (SDPO) | Per-concept structured feedback (F1/F5) | Dense > sparse credit |
| Teacher evolves during training (SDPO) | GKG refines from performance data (F2) | Target improves with learner |
| Successful rollouts as self-demos (all 3) | Mastered nodes as scaffold context (F3) | Own successes teach gaps |
| On-policy prevents forgetting (SDFT) | Retention probes during traversal (F4) | Verify no regression |
| Meta-agent modifies itself (HyperAgents) | Meta-compound: params + mechanisms (F6/F7) | Improvement procedure improves |
| Mechanism injection > params (Bilevel) | Strategy registry + stall detection (F7) | New mechanisms > tuned params |
| Tabu Search breaks traps (Bilevel) | Tabu list for failed strategies (F8) | Forbid revisiting failures |
| Orthogonal Exploration (Bilevel) | Cluster rotation forcing (F9) | Force dimensional diversity |
| Ratchet: keep/discard (AutoResearch) | Compound: K' supseteq K | Monotonic knowledge accumulation |