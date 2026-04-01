<!--
DIRECTORY TREE (orientation)
references/03-mcmc-hamiltonian.md
  Covers: HMC kernel · burn-in · thinning · criticality · fractal propagation · Lagrangian
  Depends on: 01-theoretical-core (Hamiltonian definition)
  Used by: /path traverse, /path build (path sequencing phase)
-->

# MCMC-Hamiltonian Traversal

## Contents
- [Why MCMC for Knowledge Paths](#why-mcmc)
- [Lagrangian Kernel](#lagrangian-kernel)
- [Hamiltonian Monte Carlo (HMC) Algorithm](#hmc-algorithm)
- [Burn-In Protocol](#burn-in)
- [Thinning: Intelligible Trace Extraction](#thinning)
- [Criticality Detection](#criticality-detection)
- [Eigenvector Centrality Integration](#eigenvector-centrality)
- [Fractal Path Propagation](#fractal-propagation)
- [Implementation Notes](#implementation)

---

## Why MCMC for Knowledge Paths

A user query is treated as a **probability distribution** P(node | query) over the
knowledge graph. The optimal learning path is the sequence of nodes that maximally
satisfies this distribution while respecting ZPD constraints and Zeigarnik structure.

Direct optimisation is NP-hard on large graphs. MCMC samples from the posterior
distribution efficiently, with Hamiltonian dynamics providing:
1. **Low rejection rate** — proposals follow energy-conserving trajectories
2. **Long-range mixing** — escapes local optima (isolated clusters)
3. **ZPD compliance** — energy constraints embed the ZPD filter naturally
4. **Burn-in** — handles cold start (no clear entry point in the query)

---

## Lagrangian Kernel

The Lagrangian formulation treats path traversal as a variational problem:

```
L(q, q̇) = T(q̇) − V(q)

Where:
  q   = current position in knowledge space (node embedding)
  q̇   = traversal velocity (rate of conceptual change between nodes)
  T   = kinetic energy = (1/2)|q̇|²    (cognitive processing load)
  V   = potential energy = −log P(node | query)  (relevance landscape)

Action integral:
  S[path] = ∫ L(q, q̇) dt

Optimal path = argmin S[path] subject to:
  ZPD constraint:    0.10 ≤ Δ(edge) ≤ 0.40
  Zeigarnik closure: ∀n: open_question(n) ∈ domain(successor(n))
  Topology:          η(path subgraph) ≥ 0.80
```

The **Euler-Lagrange equations** give the equations of motion for path traversal,
which the HMC leapfrog integrator solves numerically.

---

## HMC Algorithm

```python
def hamiltonian_path_sampler(
    graph: KnowledgeGraph,
    query_embedding: np.ndarray,
    n_samples: int = 200,
    burn_in: int = 50,
    thinning: int = 3,
    step_size: float = 0.1,
    n_leapfrog: int = 10,
) -> list[PathSample]:
    """
    Hamiltonian Monte Carlo over knowledge graph node space.
    Returns thinned posterior samples of optimal traversal paths.
    """
    
    def potential_energy(node_seq):
        """V(q) = negative log-likelihood of path given query."""
        relevance = sum(cosine_sim(n.embedding, query_embedding) for n in node_seq)
        zpd_penalty = sum(
            max(0, delta - 0.40) ** 2  # soft constraint
            for delta in zpd_deltas(node_seq)
        )
        return -relevance + 10 * zpd_penalty
    
    def kinetic_energy(momentum):
        return 0.5 * np.dot(momentum, momentum)
    
    def leapfrog(q, p, epsilon, L):
        """Leapfrog integrator for HMC dynamics."""
        p = p - (epsilon/2) * grad_potential(q)
        for _ in range(L - 1):
            q = q + epsilon * p
            p = p - epsilon * grad_potential(q)
        q = q + epsilon * p
        p = p - (epsilon/2) * grad_potential(q)
        return q, -p  # negate for reversibility
    
    samples = []
    current_path = initialise_path(graph, query_embedding)  # warm start or burn-in
    
    for i in range(n_samples + burn_in):
        momentum = np.random.normal(0, 1, size=len(current_path))
        proposed_path, proposed_momentum = leapfrog(
            current_path, momentum, step_size, n_leapfrog
        )
        
        # Metropolis-Hastings acceptance
        H_current = potential_energy(current_path) + kinetic_energy(momentum)
        H_proposed = potential_energy(proposed_path) + kinetic_energy(proposed_momentum)
        
        if np.log(np.random.uniform()) < H_current - H_proposed:
            current_path = proposed_path
        
        # Collect after burn-in, with thinning
        if i >= burn_in and (i - burn_in) % thinning == 0:
            samples.append(current_path)
    
    return samples
```

---

## Burn-In Protocol

Burn-in discards early MCMC samples where the chain has not yet converged to the
stationary distribution. Critical for "cold start" queries with no obvious entry.

```
Cold start detection:
  IF query has no direct match in GKG with P(node|query) > 0.3:
    → cold_start = True
    → burn_in = max(50, 0.25 × n_samples)  # longer burn-in
    → initialise from L0 nodes (governing principles)
    → use diffuse prior: P₀(node) ∝ centrality(node)

Warm start (clear entry point):
  burn_in = 10
  initialise from highest P(node|query) node

Convergence diagnostics:
  Gelman-Rubin R̂ < 1.1 across 4 parallel chains
  Effective sample size (ESS) > 50
```

**Knowledge graph cold start** = query that maps to a structural gap (learner
has no anchor node). The burn-in traverses high-centrality L0 nodes first,
letting the chain find the relevant cluster before sampling begins.

---

## Thinning: Intelligible Trace Extraction

Thinning keeps every k-th MCMC sample to reduce autocorrelation. In knowledge
graph traversal, this maps to removing redundant reasoning steps while preserving
**relational dependency** — the chain between kept nodes is *genuine*, not artificial.

```
Thinning factor k = 3 (default)
  → keeps steps with maximum conceptual distance between consecutive nodes
  → discards steps where Δ_embedding(n, n+1) < threshold (redundant micro-steps)

Zeigarnik preservation during thinning:
  RULE: Never thin a node that:
    (a) resolves an open question from a kept predecessor, OR
    (b) is the SOLE opener for a successor's question
  → Zeigarnik structure is topologically preserved across thinning

Result: The thinned chain is a parsimonious, intelligible reasoning trace
where every step is justified by relational dependency — not artifically
simplified, but genuinely compressed.
```

---

## Criticality Detection

A learning path is at **criticality** when the energy landscape has an inflection
point — equivalent to a phase transition in the learner's conceptual development.

```python
def detect_criticality(node: KnowledgeNode, graph: KnowledgeGraph) -> CriticalityReport:
    """
    Detects phase transitions in the energy landscape around a node.
    Uses discrete Hessian approximation on the graph energy function.
    """
    neighbors = graph.neighbors(node, depth=2)
    energies = {n: energy(n) for n in neighbors}
    
    # Discrete Laplacian ≈ second derivative
    laplacian = sum(energies[n] - energies[node] for n in graph.direct_neighbors(node))
    laplacian /= len(graph.direct_neighbors(node))
    
    # Criticality: |Laplacian| near zero = flat energy = phase transition
    is_critical = abs(laplacian) < 0.05
    
    # Deviation from criticality metric (σ_c)
    sigma_c = abs(laplacian)  # 0 = critical, >0.2 = stable, <0 = unstable
    
    return CriticalityReport(
        node=node.id,
        is_critical=is_critical,
        sigma_c=sigma_c,
        action="increase_tension_and_reduce_zpd_delta" if is_critical else "proceed"
    )
```

**At critical nodes**: 
- Increase Zeigarnik tension to `high`
- Reduce ZPD delta to 0.15 (smaller steps through the phase transition)
- Add explicit scaffold if mastery < 0.3

**Injected into context as**: `criticality_report.yaml` when running `/path traverse`

---

## Eigenvector Centrality Integration

Eigenvector centrality captures recursive importance — a node is central if its
neighbors are also central. In the knowledge graph this identifies **gateway concepts**
that unlock exponentially many downstream nodes.

```python
import networkx as nx

def compute_centrality_landscape(graph: KnowledgeGraph) -> dict[str, float]:
    G = nx.DiGraph()
    for node in graph.nodes:
        for successor in node.unlocks:
            G.add_edge(node.id, successor, weight=1.0)
    
    centrality = nx.eigenvector_centrality_numpy(G, weight='weight')
    
    # Normalise to [0, 1] energy scale
    max_c = max(centrality.values())
    return {k: v / max_c for k, v in centrality.items()}
```

**Energy landscape** = eigenvector centrality × (1 − mastery)

High-energy nodes = high priority, high leverage. The Hamiltonian naturally
routes through high-energy nodes first (descending the gradient).

---

## Fractal Path Propagation

The knowledge graph has small-world topology (dense local clusters, sparse
long-range connections). The MCMC proposal distribution exploits this:

```
Proposal strategy (adaptive):
  Local exploration (p=0.7):  propose swap within same cluster (dense region)
  Long-range jump (p=0.3):    propose jump to high-centrality node in different cluster

Scale invariance:
  At each cluster scale, the same Hamiltonian kernel applies.
  Dense clusters → small step_size (ε = 0.05)
  Sparse connections → large step_size (ε = 0.20)
  Adaptation: dual averaging on acceptance rate target = 0.65
```

**Tabu integration (F8)**: The proposal distribution excludes strategies in the
active tabu list. If a traversal direction (cluster, concept type) was recently
tried and produced no improvement, the Metropolis-Hastings acceptance step
rejects proposals that revisit it, regardless of energy. See [08] for details.

**Orthogonal exploration (F9)**: When cluster coverage variance exceeds 3x,
the proposal strategy shifts from 70/30 local/long-range to forced rotation
through underexplored clusters. This breaks the path dependence that standard
MCMC inherits from its initialisation. See [08] for protocol.

This fractal propagation means the MCMC naturally explores the graph at the
correct resolution — fine-grained within knowledge clusters, coarse-grained
between them — without manual tuning.

---

## Implementation Notes

```bash
# Run MCMC traversal
python scripts/mcmc_traversal.py \
  --gap gap.json \
  --query "CICM pharmacology exam preparation" \
  --n-samples 200 \
  --burn-in 50 \
  --thinning 3 \
  --output path.json \
  --criticality-report criticality.yaml

# Analytics injected into context:
#   path.json              → ordered node sequence
#   criticality.yaml       → phase transition locations
#   centrality_scores.yaml → energy landscape
#   acceptance_rate.yaml   → HMC convergence diagnostic
```

**Context injection format** (auto-generated YAML injected by CLI):
```yaml
# analytics-context.yaml — injected at /path traverse
mcmc_diagnostics:
  n_effective_samples: 67
  acceptance_rate: 0.64
  gelman_rubin: 1.04
  convergence: PASS

criticality_report:
  critical_nodes: ["time_constant", "hill_equation"]
  action: increase tension at these nodes, reduce ZPD delta to 0.15

energy_landscape_top5:
  - node: fick_principle       centrality: 0.91  mastery: 0.10  energy: 0.82
  - node: time_constant        centrality: 0.87  mastery: 0.15  energy: 0.74
  - node: henderson_hasselbalch centrality: 0.79  mastery: 0.30  energy: 0.55
```
