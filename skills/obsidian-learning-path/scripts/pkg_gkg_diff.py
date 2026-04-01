#!/usr/bin/env python3
"""
PKG/GKG Differential Analysis
==============================
Computes the gap = GKG minus PKG and ranks nodes by:
  Priority = Centrality x Impact x (1 - Mastery)

Cross-references:
  Uses: 01-theoretical-core (Zeigarnik, ZPD theory), 02-pkg-gkg-differential (gap algebra)
  Feeds: mcmc_traversal (gap.json input), generate_vault (path topology source),
         meta_compound (coverage metrics for stall detection),
         gkg_refine (performance_history structure)
  Validates: validate_vault (V1 node existence, V6 topology η, V7 orphan detection)

Usage:
    # Build GKG from domain description
    python pkg_gkg_diff.py --domain "CICM Pharmacology" --output gap.json

    # Scan existing vault for PKG mastery state
    python pkg_gkg_diff.py --domain "CICM Pharmacology" --vault ./my_vault --output gap.json

    # Use pre-built GKG + vault scan
    python pkg_gkg_diff.py --gkg gkg.json --vault ./my_vault --output gap.json

Outputs:
    gap.json                gap nodes ranked by priority
    gap_priority_queue.yaml context-ready analytics
    centrality_scores.yaml  full centrality landscape
"""

import json
import math
import argparse
import yaml
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


MASTERED_THRESHOLD = 0.85
ZPD_OPTIMAL = 0.22


# ─── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class GKGNode:
    id: str
    title: str
    level: str           # L0 | L1 | L2 | L3
    domain: str
    cluster: str
    difficulty: float    # 0.0–1.0
    prerequisites: list[str] = field(default_factory=list)
    unlocks: list[str] = field(default_factory=list)
    estimated_minutes: int = 20
    centrality: float = 0.0
    impact_unlocks: int = 0
    priority: float = 0.0

    def to_gap_node(self, mastery: float) -> dict:
        return {
            **asdict(self),
            "mastery": mastery,
            "status": self._status(mastery),
            "zpd_delta": max(0.0, self.difficulty - mastery),
            "open_question": "",
            "resolves_from": "",
            "tension_level": "medium",
            "path_position": None,
            "criticality": False,
            "sigma_c": 0.0,
        }

    def _status(self, mastery: float) -> str:
        if mastery >= MASTERED_THRESHOLD:
            return "mastered"
        elif mastery >= 0.3:
            return "in-progress"
        else:
            return "gap"


# ─── GKG Builder (RPP Decomposition) ──────────────────────────────────────────

def build_gkg_from_domain(domain: str) -> list[GKGNode]:
    """
    Build a Global Knowledge Graph via RPP L0-L3 decomposition.
    In production: calls LLM or syllabus parser.
    This scaffold generates a representative structure for any domain.
    """
    domain_slug = domain.lower().replace(" ", "_")

    nodes = []

    # L0: Governing principles (5–8 nodes, 0.8% of graph → 51% coverage)
    l0_titles = [
        f"First Principles of {domain}",
        f"Core Governing Equation: {domain}",
        f"Fundamental Conservation Laws: {domain}",
        f"Master Framework: {domain}",
        f"Unifying Theorem: {domain}",
    ]
    l0_nodes = []
    for i, title in enumerate(l0_titles):
        node = GKGNode(
            id=f"L0_{domain_slug}_{i:02d}",
            title=title,
            level="L0",
            domain=domain,
            cluster="governing_principles",
            difficulty=0.30 + i * 0.05,
            estimated_minutes=25,
        )
        l0_nodes.append(node)
        nodes.append(node)

    # L1: Atomic concepts (20–25 nodes, 4% of graph → 64% coverage)
    clusters = ["receptor_theory", "kinetics", "dynamics", "transport", "regulation"]
    l1_nodes = []
    for ci, cluster in enumerate(clusters):
        for j in range(4):
            node = GKGNode(
                id=f"L1_{domain_slug}_{cluster}_{j:02d}",
                title=f"{cluster.replace('_',' ').title()} — Concept {j+1}",
                level="L1",
                domain=domain,
                cluster=cluster,
                difficulty=0.40 + j * 0.08,
                prerequisites=[f"[[{l0_nodes[min(ci, len(l0_nodes)-1)].id}]]"],
                estimated_minutes=20,
            )
            l1_nodes.append(node)
            nodes.append(node)

    # L2: Composite topics (80–100 nodes, 20% of graph → 80% coverage)
    l2_nodes = []
    for ci, cluster in enumerate(clusters):
        cluster_l1 = [n for n in l1_nodes if n.cluster == cluster]
        for j in range(16):
            prereq_l1 = cluster_l1[j % len(cluster_l1)] if cluster_l1 else None
            node = GKGNode(
                id=f"L2_{domain_slug}_{cluster}_{j:02d}",
                title=f"{cluster.replace('_',' ').title()}: Application {j+1}",
                level="L2",
                domain=domain,
                cluster=cluster,
                difficulty=0.50 + (j % 5) * 0.07,
                prerequisites=[f"[[{prereq_l1.id}]]"] if prereq_l1 else [],
                estimated_minutes=15,
            )
            if prereq_l1:
                prereq_l1.unlocks.append(f"[[{node.id}]]")
            l2_nodes.append(node)
            nodes.append(node)

    # Wire L0 → L1 unlocks
    for i, l0 in enumerate(l0_nodes):
        cluster = clusters[i % len(clusters)]
        for l1 in l1_nodes:
            if l1.cluster == cluster:
                l0.unlocks.append(f"[[{l1.id}]]")

    return nodes


# ─── PKG Scanner ──────────────────────────────────────────────────────────────

def scan_vault(vault_path: Path, gkg_ids: set[str]) -> dict[str, float]:
    """
    Scan Obsidian vault for mastery values in frontmatter.
    Returns {node_id: mastery} for all found nodes.
    """
    mastery_map: dict[str, float] = {}

    for md_file in vault_path.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="ignore")

        # Extract YAML frontmatter
        if not content.startswith("---"):
            continue
        try:
            end = content.index("---", 3)
            fm_text = content[3:end]
            fm = yaml.safe_load(fm_text) or {}
        except (ValueError, yaml.YAMLError):
            continue

        node_id = fm.get("id", "")
        mastery = fm.get("mastery", None)

        if node_id and mastery is not None:
            try:
                mastery_map[node_id] = float(mastery)
            except (TypeError, ValueError):
                pass

        # Fallback: match by title slug
        title = fm.get("title", "")
        if title and mastery is not None:
            title_slug = re.sub(r"[^a-z0-9_]", "_", title.lower())
            for gid in gkg_ids:
                if title_slug in gid.lower():
                    mastery_map[gid] = float(mastery)

    return mastery_map


# ─── Centrality Computation ────────────────────────────────────────────────────

def compute_eigenvector_centrality(nodes: list[GKGNode]) -> dict[str, float]:
    """Power iteration eigenvector centrality."""
    by_id = {n.id: n for n in nodes}
    scores = {n.id: 1.0 / len(nodes) for n in nodes}

    for _ in range(100):
        new_scores: dict[str, float] = {}
        for node in nodes:
            incoming = sum(
                scores[pred.id]
                for pred in nodes
                if any(node.id in u for u in pred.unlocks)
            )
            new_scores[node.id] = incoming + 1e-6
        total = sum(new_scores.values()) or 1.0
        scores = {k: v / total for k, v in new_scores.items()}

    max_score = max(scores.values()) or 1.0
    return {k: v / max_score for k, v in scores.items()}


def compute_transitively_unlocked(node: GKGNode, by_id: dict[str, "GKGNode"]) -> int:
    """BFS count of transitively reachable nodes."""
    visited = set()
    queue = [node.id]
    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        visited.add(current_id)
        current = by_id.get(current_id)
        if current:
            for uid in current.unlocks:
                clean = uid.replace("[[", "").replace("]]", "").strip()
                if clean not in visited:
                    queue.append(clean)
    return len(visited) - 1  # exclude self


# ─── Priority Formula ─────────────────────────────────────────────────────────

def compute_priority(node: GKGNode, mastery: float) -> float:
    """
    Priority = Centrality × log(1 + impact_unlocks) × (1 − mastery)
    Log-scaled impact avoids over-weighting high-connectivity hubs.
    """
    impact = math.log1p(node.impact_unlocks)
    return node.centrality * impact * (1.0 - mastery)


# ─── Gap Computation ──────────────────────────────────────────────────────────

def compute_gap(
    gkg: list[GKGNode],
    mastery_map: dict[str, float],
) -> list[dict]:
    """
    Returns ranked gap nodes: GKG nodes with mastery < MASTERED_THRESHOLD.
    """
    by_id = {n.id: n for n in gkg}

    # Centrality
    centrality = compute_eigenvector_centrality(gkg)
    for node in gkg:
        node.centrality = round(centrality[node.id], 4)
        node.impact_unlocks = compute_transitively_unlocked(node, by_id)

    gap = []
    for node in gkg:
        mastery = mastery_map.get(node.id, 0.0)
        if mastery < MASTERED_THRESHOLD:
            node.priority = round(compute_priority(node, mastery), 4)
            gap.append(node.to_gap_node(mastery))

    # Sort: L0 always first (orientation priority), then by priority desc
    l0 = [n for n in gap if n["level"] == "L0"]
    rest = sorted([n for n in gap if n["level"] != "L0"], key=lambda n: -n["priority"])
    return l0 + rest


# ─── Analytics Output ─────────────────────────────────────────────────────────

def emit_gap_priority_queue(gap: list[dict], output_dir: Path):
    """Emit gap_priority_queue.yaml for CLI context injection."""
    top_10 = gap[:10]
    total_minutes = sum(n["estimated_minutes"] for n in gap)

    report = {
        "gap_analysis": {
            "total_gap_nodes": len(gap),
            "estimated_hours": round(total_minutes / 60, 1),
            "top_10_by_priority": [
                {
                    "rank": i + 1,
                    "node": n["id"],
                    "title": n["title"],
                    "level": n["level"],
                    "cluster": n["cluster"],
                    "priority": n["priority"],
                    "centrality": n["centrality"],
                    "impact_unlocks": n["impact_unlocks"],
                    "mastery": n["mastery"],
                    "zpd_delta": n["zpd_delta"],
                }
                for i, n in enumerate(top_10)
            ],
        }
    }
    (output_dir / "gap_priority_queue.yaml").write_text(yaml.dump(report, default_flow_style=False))


def emit_centrality_scores(gkg: list[GKGNode], output_dir: Path):
    """Emit centrality_scores.yaml sorted by centrality desc."""
    scores = sorted(
        [{"node": n.id, "title": n.title, "centrality": n.centrality, "impact_unlocks": n.impact_unlocks}
         for n in gkg],
        key=lambda x: -x["centrality"]
    )
    (output_dir / "centrality_scores.yaml").write_text(yaml.dump({"centrality_landscape": scores}, default_flow_style=False))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PKG/GKG Gap Differential Analysis")
    parser.add_argument("--domain", default="", help="Domain name for GKG construction")
    parser.add_argument("--gkg", default="", help="Pre-built GKG JSON path")
    parser.add_argument("--vault", default="", help="Obsidian vault path for PKG scan")
    parser.add_argument("--output", default="gap.json")
    parser.add_argument("--output-dir", default=".", help="Directory for analytics YAML files")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build or load GKG
    if args.gkg:
        raw = json.loads(Path(args.gkg).read_text())
        gkg = [GKGNode(**d) for d in raw]
        print(f"✅ Loaded GKG: {len(gkg)} nodes from {args.gkg}")
    elif args.domain:
        print(f"🔬 Building GKG for domain: '{args.domain}'")
        gkg = build_gkg_from_domain(args.domain)
        print(f"   GKG nodes: {len(gkg)} (L0:{sum(1 for n in gkg if n.level=='L0')} | L1:{sum(1 for n in gkg if n.level=='L1')} | L2:{sum(1 for n in gkg if n.level=='L2')})")
    else:
        raise ValueError("Provide either --domain or --gkg")

    # Scan vault for PKG
    mastery_map: dict[str, float] = {}
    if args.vault:
        vault_path = Path(args.vault)
        if vault_path.exists():
            gkg_ids = {n.id for n in gkg}
            mastery_map = scan_vault(vault_path, gkg_ids)
            print(f"📚 PKG scan: {len(mastery_map)} nodes with mastery data in vault")
        else:
            print(f"⚠️  Vault not found: {args.vault}. Using zero mastery.")
    else:
        print("ℹ️  No vault provided. Using zero mastery (cold start).")

    # Compute gap
    gap = compute_gap(gkg, mastery_map)
    mastered_count = len(gkg) - len(gap)
    coverage = round(mastered_count / max(len(gkg), 1) * 100, 1)

    print(f"\n📊 Gap Analysis:")
    print(f"   Total GKG nodes:  {len(gkg)}")
    print(f"   Mastered:         {mastered_count} ({coverage}%)")
    print(f"   Gap:              {len(gap)}")
    print(f"   Est. study time:  {sum(n['estimated_minutes'] for n in gap) / 60:.1f}h")

    if gap:
        print(f"\n🎯 Top 5 Priority Gaps:")
        for i, n in enumerate(gap[:5]):
            print(f"   {i+1}. {n['title'][:50]:<50} priority={n['priority']:.3f} mastery={n['mastery']:.2f}")

    # Write outputs
    Path(args.output).write_text(json.dumps(gap, indent=2))
    emit_gap_priority_queue(gap, output_dir)
    emit_centrality_scores(gkg, output_dir)

    print(f"\n✅ Gap written to {args.output}")
    print(f"   Analytics: {output_dir}/gap_priority_queue.yaml")
    print(f"   Analytics: {output_dir}/centrality_scores.yaml")


if __name__ == "__main__":
    main()
