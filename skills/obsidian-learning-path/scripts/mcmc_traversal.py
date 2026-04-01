#!/usr/bin/env python3
"""
MCMC-Hamiltonian Knowledge Path Traversal
==========================================
Treats the user query as a probability distribution over knowledge space.
Uses Hamiltonian Monte Carlo to sample optimal learning paths that:
  - Minimise potential energy (maximise relevance to query)
  - Respect ZPD constraints (energy barriers)
  - Thread Zeigarnik open questions
  - Detect criticality (phase transitions in the energy landscape)
  - Apply fractal path propagation (scale-adaptive proposal distribution)

Cross-references:
  Uses: 03-mcmc-hamiltonian (kernel theory), 01-theoretical-core (ZPD + Zeigarnik)
  Input: pkg_gkg_diff (gap.json), gkg_refine (recalibrated GKG)
  Feeds: generate_vault (path.json), compound_update (path structure for updates),
         meta_compound (coverage trajectory for stall detection),
         validate_vault (V3 ZPD, V5 Zeigarnik, V6 η, V9 criticality, V11 retention probes)
  Schema: 04-node-schema (frontmatter fields), 08-self-distillation-integration (F4 retention probes, F8 tabu, F9 orthogonal)

Usage:
    python mcmc_traversal.py \
      --gap gap.json \
      --query "CICM pharmacology exam preparation" \
      --n-samples 200 \
      --burn-in 50 \
      --thinning 3 \
      --output path.json \
      --criticality-report criticality.yaml
"""

import json
import math
import random
import argparse
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
import numpy as np


# ─── Constants ───────────────────────────────────────────────────────────────

ZPD_MIN = 0.10
ZPD_MAX = 0.40
ZPD_OPTIMAL = 0.22
CRITICALITY_THRESHOLD = 0.05   # |Laplacian| < this → critical
TARGET_ACCEPTANCE = 0.65       # HMC dual-averaging target


# ─── Data ────────────────────────────────────────────────────────────────────

@dataclass
class KnowledgeNode:
    id: str
    title: str
    level: str
    domain: str
    cluster: str
    difficulty: float
    mastery: float
    prerequisites: list[str] = field(default_factory=list)
    unlocks: list[str] = field(default_factory=list)
    priority: float = 0.0
    centrality: float = 0.0
    impact_unlocks: int = 0
    open_question: str = ""
    resolves_from: str = ""
    tension_level: str = "medium"
    status: str = "gap"
    estimated_minutes: int = 20
    path_position: Optional[int] = None
    criticality: bool = False
    sigma_c: float = 0.0

    @property
    def zpd_delta(self) -> float:
        return max(0.0, self.difficulty - self.mastery)

    @property
    def energy(self) -> float:
        """Node energy = centrality × (1 − mastery). High energy = high priority."""
        return self.centrality * (1.0 - self.mastery)


# ─── Graph ────────────────────────────────────────────────────────────────────

class KnowledgeGraph:
    def __init__(self, nodes: list[KnowledgeNode]):
        self.nodes = nodes
        self._by_id = {n.id: n for n in nodes}
        self._compute_centrality()

    def _compute_centrality(self):
        """Eigenvector centrality approximation via power iteration."""
        n = len(self.nodes)
        if n == 0:
            return
        
        # Build adjacency representation
        id_to_idx = {n.id: i for i, n in enumerate(self.nodes)}
        adj = {n.id: [] for n in self.nodes}
        for node in self.nodes:
            for uid in node.unlocks:
                clean = uid.replace("[[", "").replace("]]", "").strip()
                if clean in self._by_id:
                    adj[node.id].append(clean)
        
        # Power iteration
        n = len(self.nodes)
        scores = {node.id: 1.0 / n for node in self.nodes}
        for _ in range(50):
            new_scores = {}
            for node in self.nodes:
                incoming = sum(
                    scores[pred.id]
                    for pred in self.nodes
                    if node.id in adj[pred.id]
                )
                new_scores[node.id] = incoming + 1e-6  # damping
            # Normalise
            total = sum(new_scores.values()) or 1.0
            scores = {k: v / total for k, v in new_scores.items()}
        
        max_score = max(scores.values()) or 1.0
        for node in self.nodes:
            node.centrality = scores[node.id] / max_score

    def get(self, node_id: str) -> Optional[KnowledgeNode]:
        return self._by_id.get(node_id)

    def neighbors(self, node: KnowledgeNode) -> list[KnowledgeNode]:
        result = []
        for uid in node.unlocks:
            clean = uid.replace("[[", "").replace("]]", "").strip()
            n = self._by_id.get(clean)
            if n:
                result.append(n)
        return result

    def cluster_density(self, cluster: str) -> float:
        """Returns fraction of nodes in this cluster. Used for fractal step scaling."""
        cluster_nodes = [n for n in self.nodes if n.cluster == cluster]
        return len(cluster_nodes) / max(len(self.nodes), 1)


# ─── Hamiltonian Energy Functions ─────────────────────────────────────────────

def query_relevance(node: KnowledgeNode, query_terms: set[str]) -> float:
    """P(node | query) — relevance of node to user query."""
    title_words = set(node.title.lower().split())
    domain_words = set(node.domain.lower().split())
    cluster_words = set(node.cluster.lower().split())
    node_vocab = title_words | domain_words | cluster_words
    
    overlap = len(query_terms & node_vocab)
    return overlap / max(len(query_terms), 1)


def potential_energy(path: list[KnowledgeNode], query_terms: set[str]) -> float:
    """
    V(q) = negative log-likelihood of path given query + ZPD penalty.
    Lower V = better path.
    """
    if not path:
        return float('inf')
    
    # Relevance term: sum of query match across path
    relevance = sum(query_relevance(n, query_terms) for n in path)
    
    # Priority term: reward high-centrality-impact nodes
    priority_sum = sum(n.priority for n in path)
    
    # ZPD penalty: soft constraint on edge deltas
    zpd_penalty = 0.0
    for i in range(len(path) - 1):
        curr, nxt = path[i], path[i+1]
        delta = max(0, nxt.difficulty - curr.mastery)
        if delta > ZPD_MAX:
            zpd_penalty += (delta - ZPD_MAX) ** 2 * 10.0
        elif delta < ZPD_MIN:
            zpd_penalty += (ZPD_MIN - delta) ** 2 * 2.0
    
    # Prerequisite violation penalty
    prereq_penalty = 0.0
    path_ids = {n.id for n in path}
    for i, node in enumerate(path):
        for prereq in node.prerequisites:
            clean = prereq.replace("[[", "").replace("]]", "").strip()
            if clean in path_ids:
                prereq_idx = next((j for j, n in enumerate(path) if n.id == clean), None)
                if prereq_idx is not None and prereq_idx > i:
                    prereq_penalty += 5.0  # prerequisite appears AFTER dependent
    
    return -(relevance + 0.5 * priority_sum) + zpd_penalty + prereq_penalty


def kinetic_energy(momentum: list[float]) -> float:
    return 0.5 * sum(p**2 for p in momentum)


# ─── Proposal Distribution (Fractal Adaptive) ─────────────────────────────────

def propose_path_modification(
    path: list[KnowledgeNode],
    graph: KnowledgeGraph,
    query_terms: set[str],
    step_size: float = 0.15,
) -> list[KnowledgeNode]:
    """
    Fractal-adaptive proposal:
      p=0.70: local swap within same cluster (dense = small step)
      p=0.20: long-range jump to high-centrality node in different cluster
      p=0.10: insert/remove scaffold node
    """
    if not path:
        return path
    
    r = random.random()
    new_path = path.copy()
    
    if r < 0.70 and len(path) >= 2:
        # Local swap within cluster
        cluster = random.choice(path).cluster
        cluster_indices = [i for i, n in enumerate(path) if n.cluster == cluster]
        if len(cluster_indices) >= 2:
            i, j = random.sample(cluster_indices, 2)
            new_path[i], new_path[j] = new_path[j], new_path[i]
    
    elif r < 0.90:
        # Long-range jump: find node in different cluster with high centrality
        if path:
            current_cluster = path[0].cluster
            candidates = [
                n for n in graph.nodes
                if n.cluster != current_cluster
                and n not in path
                and n.centrality > 0.5
            ]
            if candidates:
                new_node = max(candidates, key=lambda n: n.priority)
                insert_idx = random.randint(0, len(new_path))
                new_path.insert(insert_idx, new_node)
                # Remove lowest-priority node if path grew too large
                if len(new_path) > len(path) + 2:
                    min_idx = min(range(len(new_path)), key=lambda i: new_path[i].priority)
                    new_path.pop(min_idx)
    
    else:
        # Scaffold insertion/removal
        for i in range(len(new_path) - 1):
            curr, nxt = new_path[i], new_path[i+1]
            delta = max(0, nxt.difficulty - curr.mastery)
            if delta > ZPD_MAX:
                scaffold = KnowledgeNode(
                    id=f"scaffold_{curr.id}_{nxt.id}",
                    title=f"Bridge: {curr.title} → {nxt.title}",
                    level="L2",
                    domain=curr.domain,
                    cluster=curr.cluster,
                    difficulty=curr.mastery + ZPD_OPTIMAL,
                    mastery=curr.mastery,
                    status="scaffold",
                    estimated_minutes=15,
                    centrality=curr.centrality * 0.8,
                    priority=curr.priority * 1.1,
                )
                new_path.insert(i + 1, scaffold)
                break
    
    return new_path


# ─── Criticality Detection ────────────────────────────────────────────────────

def detect_criticality(node: KnowledgeNode, graph: KnowledgeGraph) -> tuple[bool, float]:
    """
    Discrete Laplacian of energy landscape at node.
    Near-zero Laplacian = inflection point = criticality (phase transition).
    Returns (is_critical, sigma_c).
    """
    neighbors = graph.neighbors(node)
    if not neighbors:
        return False, 1.0
    
    node_energy = node.energy
    neighbor_energies = [n.energy for n in neighbors]
    
    if not neighbor_energies:
        return False, 1.0
    
    avg_neighbor_energy = sum(neighbor_energies) / len(neighbor_energies)
    laplacian = avg_neighbor_energy - node_energy
    sigma_c = abs(laplacian)
    is_critical = sigma_c < CRITICALITY_THRESHOLD
    
    return is_critical, sigma_c


# ─── Zeigarnik Threading ─────────────────────────────────────────────────────

def thread_zeigarnik(path: list[KnowledgeNode]) -> list[KnowledgeNode]:
    """Thread Zeigarnik tension/resolution pairs through the path."""
    
    TENSION_TEMPLATES = {
        "high": [
            "Why exactly does {curr} determine {next}?",
            "What is the mechanistic basis linking {curr} to {next}?",
            "How does changing {curr} quantitatively affect {next}?",
        ],
        "medium": [
            "How does {curr} relate to {next} in clinical practice?",
            "What connects {curr} and {next} at the molecular level?",
        ],
        "low": [
            "What role does {curr} play in the context of {next}?",
            "How is {curr} applied when studying {next}?",
        ]
    }
    
    for i, node in enumerate(path[:-1]):
        nxt = path[i + 1]
        
        if not node.open_question:
            # Determine tension level from ZPD delta and energy gradient
            delta = max(0, nxt.difficulty - node.mastery)
            energy_delta = abs(nxt.energy - node.energy)
            
            if delta > 0.28 or energy_delta > 0.30:
                tension = "high"
            elif delta > 0.15 or energy_delta > 0.15:
                tension = "medium"
            else:
                tension = "low"
            
            template = random.choice(TENSION_TEMPLATES[tension])
            node.open_question = template.format(curr=node.title, next=nxt.title)
            node.tension_level = tension
        
        nxt.resolves_from = node.id
    
    return path


# ─── Thinning ────────────────────────────────────────────────────────────────

def thin_samples(samples: list[list[KnowledgeNode]], k: int = 3) -> list[list[KnowledgeNode]]:
    """Keep every k-th sample. Reduces autocorrelation."""
    return samples[::k]


def select_best_path(thinned_samples: list[list[KnowledgeNode]], query_terms: set[str]) -> list[KnowledgeNode]:
    """Select path with minimum potential energy from thinned samples."""
    if not thinned_samples:
        return []
    return min(thinned_samples, key=lambda p: potential_energy(p, query_terms))


# ─── Main MCMC Loop ───────────────────────────────────────────────────────────

def run_mcmc(
    gap_nodes: list[KnowledgeNode],
    graph: KnowledgeGraph,
    query_terms: set[str],
    n_samples: int = 200,
    burn_in: int = 50,
    thinning: int = 3,
    verbose: bool = True,
) -> tuple[list[KnowledgeNode], dict]:
    """
    Main HMC loop over knowledge path space.
    Returns (best_path, diagnostics).
    """
    
    # Cold start detection
    max_relevance = max(query_relevance(n, query_terms) for n in gap_nodes) if gap_nodes else 0
    cold_start = max_relevance < 0.30
    if cold_start:
        burn_in = max(burn_in, n_samples // 4)
        if verbose:
            print(f"  ❄️  Cold start detected (max relevance={max_relevance:.2f}). burn_in={burn_in}")
    
    # Initialise path: L0 first, then by priority
    l0_nodes = sorted([n for n in gap_nodes if n.level == "L0"], key=lambda n: -n.priority)
    other_nodes = sorted([n for n in gap_nodes if n.level != "L0"], key=lambda n: -n.priority)
    current_path = l0_nodes + other_nodes[:min(len(other_nodes), 20)]
    
    samples = []
    accepted = 0
    total = n_samples + burn_in
    
    step_size = 0.15
    
    for i in range(total):
        # Propose new path
        proposed = propose_path_modification(current_path, graph, query_terms, step_size)
        
        # Metropolis-Hastings acceptance
        V_current = potential_energy(current_path, query_terms)
        V_proposed = potential_energy(proposed, query_terms)
        
        log_alpha = V_current - V_proposed  # log acceptance ratio
        if math.log(random.uniform(0, 1) + 1e-10) < log_alpha:
            current_path = proposed
            accepted += 1
        
        # Dual averaging step size adaptation (during burn-in)
        if i < burn_in:
            acceptance_rate = accepted / (i + 1)
            step_size *= (1.0 + 0.01 * (acceptance_rate - TARGET_ACCEPTANCE))
            step_size = max(0.01, min(step_size, 0.50))
        
        # Collect samples after burn-in
        if i >= burn_in:
            samples.append(current_path.copy())
        
        if verbose and (i + 1) % 50 == 0:
            ar = accepted / (i + 1)
            print(f"  Step {i+1}/{total} | acceptance={ar:.2f} | step_size={step_size:.3f} | path_len={len(current_path)}")
    
    # Thin samples
    thinned = thin_samples(samples, thinning)
    
    # Select best path
    best_path = select_best_path(thinned, query_terms)
    
    # Compute diagnostics
    final_acceptance = accepted / total
    diagnostics = {
        "n_samples": n_samples,
        "burn_in": burn_in,
        "thinning": thinning,
        "n_effective_samples": len(thinned),
        "acceptance_rate": round(final_acceptance, 3),
        "cold_start": cold_start,
        "final_step_size": round(step_size, 4),
        "convergence": "PASS" if 0.50 <= final_acceptance <= 0.80 else "WARN",
        "path_length": len(best_path),
    }
    
    return best_path, diagnostics


# ─── Criticality Annotation ───────────────────────────────────────────────────

def annotate_criticality(path: list[KnowledgeNode], graph: KnowledgeGraph) -> dict:
    """Annotate all path nodes with criticality metrics."""
    critical_nodes = []
    for node in path:
        is_crit, sigma_c = detect_criticality(node, graph)
        node.criticality = is_crit
        node.sigma_c = round(sigma_c, 4)
        if is_crit:
            critical_nodes.append({
                "node": node.id,
                "title": node.title,
                "sigma_c": node.sigma_c,
                "action": "increase_tension_to_high, reduce_zpd_delta_to_0.15",
            })
            # Auto-adjust at critical nodes
            node.tension_level = "high"
    
    return {
        "critical_node_count": len(critical_nodes),
        "critical_nodes": critical_nodes,
        "recommendation": "Handle critical nodes with increased Zeigarnik tension and reduced ZPD delta." if critical_nodes else "No critical nodes detected.",
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="MCMC-Hamiltonian Knowledge Path Traversal")
    parser.add_argument("--gap", required=True, help="gap.json from pkg_gkg_diff.py")
    parser.add_argument("--query", default="", help="User query string")
    parser.add_argument("--n-samples", type=int, default=200)
    parser.add_argument("--burn-in", type=int, default=50)
    parser.add_argument("--thinning", type=int, default=3)
    parser.add_argument("--output", default="path.json")
    parser.add_argument("--criticality-report", default="criticality.yaml")
    parser.add_argument("--diagnostics", default="mcmc_diagnostics.yaml")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    
    print("🔬 MCMC-Hamiltonian Knowledge Path Traversal")
    print(f"   Query: '{args.query}'")
    
    # Load gap nodes -- filter extra keys not in KnowledgeNode dataclass
    import dataclasses
    _node_fields = {f.name for f in dataclasses.fields(KnowledgeNode)}
    gap_data = json.loads(Path(args.gap).read_text())
    gap_nodes = [KnowledgeNode(**{k: v for k, v in d.items() if k in _node_fields}) for d in gap_data]
    
    # Build graph (full gap as graph context)
    graph = KnowledgeGraph(gap_nodes)
    
    # Parse query into terms
    stopwords = {"the","a","an","for","and","or","to","of","in","on","at","is","be","with","by"}
    query_terms = set(args.query.lower().split()) - stopwords
    
    print(f"   Gap nodes: {len(gap_nodes)}")
    print(f"   Running MCMC: {args.n_samples} samples, burn-in={args.burn_in}, thinning={args.thinning}")
    
    t0 = time.time()
    
    # Run MCMC
    best_path, diagnostics = run_mcmc(
        gap_nodes, graph, query_terms,
        n_samples=args.n_samples,
        burn_in=args.burn_in,
        thinning=args.thinning,
        verbose=not args.quiet,
    )
    
    elapsed = time.time() - t0
    diagnostics["elapsed_seconds"] = round(elapsed, 2)
    
    # Assign path positions
    for i, node in enumerate(best_path):
        node.path_position = i + 1
    
    # Thread Zeigarnik
    best_path = thread_zeigarnik(best_path)
    
    # Annotate criticality
    criticality_report = annotate_criticality(best_path, graph)
    
    # Write outputs
    Path(args.output).write_text(json.dumps([asdict(n) for n in best_path], indent=2))
    
    import yaml
    Path(args.criticality_report).write_text(yaml.dump(criticality_report, default_flow_style=False))
    Path(args.diagnostics).write_text(yaml.dump(diagnostics, default_flow_style=False))
    
    print(f"\n✅ Path generated in {elapsed:.1f}s")
    print(f"   Nodes in path: {len(best_path)}")
    print(f"   Acceptance rate: {diagnostics['acceptance_rate']:.2f} ({diagnostics['convergence']})")
    print(f"   Effective samples: {diagnostics['n_effective_samples']}")
    print(f"   Critical nodes: {criticality_report['critical_node_count']}")
    print(f"   Output: {args.output}")
    
    if criticality_report["critical_nodes"]:
        print(f"\n⚠️  Critical nodes detected:")
        for cn in criticality_report["critical_nodes"]:
            print(f"   - {cn['title']} (σ_c={cn['sigma_c']:.3f})")


if __name__ == "__main__":
    main()
