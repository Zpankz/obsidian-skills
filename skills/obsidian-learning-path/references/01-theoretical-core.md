<!--
DIRECTORY TREE (orientation)
references/01-theoretical-core.md
  Covers: Zeigarnik · ZPD · RPP · Compound Learning · Hyperspatial Geometry
  Depends on: none
  Used by: /path build, /path traverse, any "why" query
-->

# Theoretical Core

## Contents
- [Zeigarnik Effect](#zeigarnik-effect)
- [Zone of Proximal Development](#zpd)
- [RPP Hierarchical Compression](#rpp)
- [Compound Learning Loop](#compound-learning)
- [Hyperspatial Knowledge Geometry](#hyperspatial-geometry)
- [Synthesis: Unified Framework](#synthesis)

---

## Zeigarnik Effect

**Source**: Zeigarnik (1927) — incomplete tasks recalled ~90% better than complete.

Cognitive tension from incompletion drives memory consolidation and continued
engagement. The knowledge graph exploits this by structuring every node as a
tension/resolution pair: node_N poses an open question that only node_N+1 resolves.

```
Loop structure:
  Node_N ──[open: "Why does X behave as Y?"]──► Node_N+1 ──[resolves: ✓]──► new tension...

Tension levels:
  high   → "why" / "how exactly" / "what determines" (strongest pull)
  medium → "how does X relate to Y"
  low    → "what is the role of X in Y"
```

**Critical rule**: Tension must be *genuinely unresolvable* without the next node.
Artificial or answerable tensions collapse the Zeigarnik loop. The question must
require knowledge the current node does not contain.

---

## ZPD

**Source**: Vygotsky (1978) — learning occurs between solo capability and scaffolded capability.

```
ZPD_delta(edge u→v) = difficulty(v) − mastery(u)

Constraints:
  Δ < 0.10  → skip edge (trivially easy, no growth)
  Δ ∈ [0.10, 0.40]  → valid ZPD zone (optimal learning)
  Δ > 0.40  → insert scaffold node S where:
              difficulty(S) = mastery(u) + 0.22  (target optimal Δ)
              difficulty(v) = mastery(u) + 0.22 + Δ_remainder

Optimal Δ target: 0.22 (empirically calibrated, see lessons.md for updates)
```

ZPD is applied **per edge**, not globally. Every transition in the path is
individually validated. Scaffold nodes are auto-generated, not user-defined.

**Mastery(prerequisites)** uses geometric mean when multiple prereqs exist:
```
mastery(u) = geometric_mean([mastery(p) for p in prerequisites(v)])
```

---

## RPP

**Recursive Pareto Principle** — hierarchical knowledge compression.

```
L0 (meta-graph)     0.8% nodes → 51% coverage   governing principles
L1 (logic-graph)    4%   nodes → 64% coverage   atomic concepts
L2 (concept-graph)  20%  nodes → 80% coverage   composite topics
L3 (detail-graph)   100% nodes → 100% coverage  full ground truth
```

**Learning path navigation rule:**
- ALL learners start at L0 (schema orientation before content)
- Gap priority determines L1/L2 drilling order
- L3 loaded ONLY for nodes with high exam probability AND low mastery
- Cross-level vertex sharing (same concept appearing L0→L3) = compression vertex

**Target node counts** for a ~120-objective domain:
```yaml
L0: 5–8 nodes    (governing equations / first principles)
L1: 20–25 nodes  (atomic mechanisms)
L2: 80–100 nodes (clinical/applied topics)
L3: 200+ nodes   (detail, only for high-priority gaps)
```

---

## Compound Learning

**λ(ο,Κ).τ → λ(ο,Κ').τ where Κ' ⊃ Κ** — knowledge strictly grows.

```
Session_t:
  study nodes {n₁...nₖ} → score each → update PKG

PKG_update (EMA, v2 multi-signal):
  mastery_t+1(n) = (1 − α) × mastery_t(n) + α × dense_score(n)
  dense_score = f(concept_scores, error_types, calibration, explanation)  [F1/F5]
  α = 0.30 (auto-tuned by meta_compound.py — see F6)

Spaced repetition:
  interval(n) = base × easiness_factor^review_count
  easiness(n) = 1.3 + 0.9 × mastery(n)  [range: 1.3–2.2]
  max_interval = 21 days

Post-session pipeline:
  PKG_t+1 = PKG_t ∪ {n: mastery_t+1(n) ≥ 0.85}  (mastered set grows)
  Δ_t+1   = GKG \ PKG_t+1                          (gap shrinks)
  self_demos(Δ_t+1) = select from PKG_t+1           (own mastery scaffolds)  [F3]
  Path_t+1 = MCMC(Hamiltonian(Δ_t+1, ZPD), burn_in=20)  (resequence)
  insert_retention_probes(Path_t+1, freq)            (anti-forgetting)       [F4]
  error_patterns = aggregate(session.error_types)    (dense analytics)       [F5]
  IF t mod N == 0: GKG = refine(GKG, history)        (evolving teacher)      [F2]
  IF t mod M == 0: Σ = meta_compound(Σ, pred_errors) (mechanism injection + param tuning) [F6/F7/F8/F9]
```

---

## Hyperspatial Knowledge Geometry

The knowledge graph is embedded in a high-dimensional Riemannian manifold where:

**Nodes** = points in ℝⁿ (n = embedding dimension, typically 128–512)
**Edges** = geodesics on the manifold
**Eigenvector centrality** = energy landscape (high-centrality nodes = energy peaks)
**Learning path** = gradient descent on the energy landscape subject to ZPD constraints

```
Energy function:
  E(node) = eigenvector_centrality(node) × (1 − mastery(node))

Hamiltonian:
  H(q, p) = KE(p) + PE(q)
  KE(p) = (1/2) × |p|²            (momentum = learning velocity)
  PE(q) = −log P(node | query)     (potential = relevance to query)

Criticality detection:
  A path is at criticality when: ∂²E/∂q² ≈ 0
  (inflection point in the energy landscape = phase transition in learning)
  Detection: compute Hessian eigenvalues; near-zero = critical region
  Action: increase Zeigarnik tension, reduce ZPD delta at critical nodes
```

**Fractal path propagation**: At each MCMC step, the proposal distribution
scales self-similarly with the local graph topology (small-world property).
This means the Markov chain explores the graph at the correct resolution
automatically — dense clusters explored finely, sparse regions coarsely.

---

## Self-Distillation Correspondence

**Source**: Cross-integration of SDFT (arXiv:2601.19897), SDPO (arXiv:2601.20802),
HyperAgents (arXiv:2603.19461) — Jan-Mar 2026.

The on-policy context-distillation update operator from ML maps isomorphically
onto the learning path framework:

```
ML Operator:   F(π, C) = argmin KL(π(·|x) ‖ π(·|x, C))
Path Operator: F(PKG, GKG) = compound(PKG, session on Δ)

Correspondence:
  log π(·|x,c) − log π(·|x)  ≅  GKG \ PKG           (gap as self-referential difference)
  Trust-region / EMA          ≅  ZPD ∈ [0.10, 0.40]   (bounded step size)
  On-policy sampling          ≅  Zeigarnik constraint  (learn from where you are)
  Iterative self-distillation ≅  Compound loop K'⊇K    (monotonic accumulation)
```

**Core invariant** (natural language):
> Effective learning = regulated closure of a self-referential gap, traversed on
> the learner's own distribution, under bounded step size, with iterative compounding.

This correspondence grounds six experimental findings (F1–F6) now integrated
into the skill. See [08-self-distillation-integration] for full details.

**Key experimental validations**:
- Dense credit > sparse (SDPO: 4x fewer generations) -> F1/F5 rich feedback
- Teacher evolves with learner (SDPO Fig 10) -> F2 evolving GKG
- Own successes as teaching context (all 3 papers) -> F3 self-demo scaffolding
- On-policy prevents forgetting (SDFT 3-task seq.) -> F4 retention probes
- Meta-level self-modification (HyperAgents) -> F6 meta-compound parameter tuning
- Mechanism injection 5x > parameter tuning (Bilevel AutoResearch) -> F7 strategy registry
- Tabu Search breaks deterministic traps (Bilevel) -> F8 tabu list
- Orthogonal Exploration forces avoided dimensions (Bilevel) -> F9 cluster rotation
- Ratchet monotonicity (Karpathy AutoResearch) -> compound loop K' supseteq K

---

## Synthesis: Unified Framework

```
λ(PKG, GKG, H, Zeigarnik, ZPD, RPP, Compound, Σ).τ_obsidian

Step 1:  GKG = RPP(domain)                    hierarchical compression
Step 2:  PKG = scan(vault) or initialise(0)   mastery state
Step 3:  Δ = GKG \ PKG                        gap algebra
Step 3b: r = log P(n|C) − log P(n)           implicit reward (gap signal)  [F1]
Step 4:  rank(Δ) by Priority                  centrality × impact × (1−mastery)
Step 4b: select_self_demos(Δ, PKG)            scaffold from own mastery    [F3]
Step 5:  H = Hamiltonian(Δ, ZPD_constraints)  energy landscape
Step 6:  Path = MCMC(H,
           burn_in = 50 if cold_start else 10,
           thinning = 3,
           criticality_check = True)
Step 6b: insert_retention_probes(Path, freq)  on-policy anti-forgetting    [F4]
Step 7:  thread_zeigarnik(Path)               tension/resolution pairs
Step 8:  emit_vault(Path)                     .md + .canvas + .base
Step 9:  validate(vault)                      topology · ZPD · retention
Step 10: compound(session, rich_feedback)     multi-signal EMA update      [F1/F5]
Step 11: IF sessions_since_refine >= N:
           GKG' = refine(GKG, history)        evolving teacher             [F2]
Step 12: IF sessions_since_meta >= M:
           Σ' = meta_compound(Σ, errors, stall) mechanism injection + param tuning [F6/F7]
Step 12b: update_tabu(failed_mechanisms)       forbid revisiting failures         [F8]
Step 12c: IF cluster_skew > threshold:
           inject(traversal_cluster_rotation)  force dimensional diversity         [F9]
Step 14: E = self_eval(skill)                  intrinsic architectural assessment     [v4]
Step 15: H' = consolidate(H, keep_recent=10)  Pareto compress old session history     [v4]
Step 16: goto Step 2                          self-improving loop
```

**Emergent property**: The combination produces a living curriculum that
is simultaneously theoretically optimal (Hamiltonian energy minimisation),
cognitively calibrated (ZPD per edge), motivationally engineered (Zeigarnik
loops), hierarchically structured (RPP), self-improving (compound loop),
anti-fragile (retention probes), self-scaffolding (own mastery as teacher),
meta-adaptive (mechanisms injected on stall, not just parameters tuned),
trap-breaking (tabu memory forbids revisiting failed strategies),
dimensionally diverse (orthogonal exploration forces coverage balance),
and self-assessing (architectural introspection detects its own degradation).
