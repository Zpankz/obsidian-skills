#!/usr/bin/env python3
"""
Obsidian Vault Emitter
======================
Generates .md + .canvas + .base files from an ordered path.json.

Cross-references:
  Uses: 04-node-schema (frontmatter spec), 06-canvas-base-spec (.canvas/.base format),
        node-template (assets/node-template.md), canvas-template (assets/canvas-template.json),
        base-template (assets/base-template.base)
  Input: mcmc_traversal (path.json), pkg_gkg_diff (gap analytics)
  Feeds: validate_vault (V1-V10 checks), compound_update (vault .md files to update)
  Schema: 01-theoretical-core (Zeigarnik threading), 03-mcmc-hamiltonian (path ordering)

Usage:
    python generate_vault.py --path path.json --vault ./my_vault --domain "CICM Pharmacology"

Outputs:
    ./my_vault/concepts/         ← .md files per node (Zeigarnik-threaded)
    ./my_vault/path.canvas       ← color-coded visual map
    ./my_vault/progress.base     ← 6-view progress tracker
    ./my_vault/meta/lessons.md   ← self-improvement log
    ./my_vault/analytics/        ← injected analytics YAML
"""

import json
import argparse
import re
import math
from dataclasses import dataclass, field
from pathlib import Path
from datetime import date, timedelta


# ─── Canvas Color Constants ────────────────────────────────────────────────────

LEVEL_COLORS = {"L0": "6", "L1": "1", "L2": "4", "L3": "5"}
STATUS_COLORS = {"gap": "1", "in-progress": "3", "mastered": "4", "scaffold": "5"}
ZPD_EDGE_COLORS = {
    "optimal": "4",   # Δ ≤ 0.22
    "acceptable": "3", # Δ ∈ (0.22, 0.40]
    "violation": "1",  # Δ > 0.40
    "critical": "6",   # criticality override
}

ZPD_OPTIMAL = 0.22
NODE_W, NODE_H = 280, 160
H_GAP, V_GAP = 40, 80
COLS_PER_ROW = 5
LEVEL_Y = {"L0": 0, "L1": 300, "L2": 650, "L3": 1000}


# ─── Markdown Generation ───────────────────────────────────────────────────────

def safe_filename(title: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", title)[:60]


def spaced_repetition_date(mastery: float, review_count: int) -> str:
    easiness = 1.3 + 0.9 * mastery
    interval = min(int(math.pow(easiness, review_count)), 21)
    interval = max(1, interval)
    next_date = date.today() + timedelta(days=interval)
    return next_date.isoformat()


def generate_md(node: dict, domain: str) -> str:
    """Generate Obsidian-compliant .md with full frontmatter + structured body."""

    # Recompute zpd_delta from source (overrides stale stored value)
    node["zpd_delta"] = round(max(0.1, node.get("difficulty", 0.5) - node.get("mastery", 0.0)), 3)
    # Quote wikilinks so YAML parses as strings, not nested flow sequences
    prereq_links = "\n".join(f'  - "[[{p.replace("[[","").replace("]]","").strip()}]]"' for p in (node.get("prerequisites") or []))
    unlock_links  = "\n".join(f'  - "[[{u.replace("[[","").replace("]]","").strip()}]]"' for u in (node.get("unlocks") or []))
    next_review   = spaced_repetition_date(node.get("mastery", 0), node.get("review_count", 0))

    frontmatter = f"""---
id: "{node['id']}"
title: "{node['title']}"
aliases: []

# Graph Position
level: {node['level']}
domain: "{domain}"
cluster: "{node['cluster']}"
path_position: {node.get('path_position', 0)}

# PKG State
mastery: {node.get('mastery', 0.0)}
last_reviewed: null
review_count: 0
next_review: "{next_review}"
status: {node.get('status', 'gap')}

# ZPD Calibration
difficulty: {node['difficulty']}
prerequisites:
{prereq_links or "  []"}
unlocks:
{unlock_links or "  []"}
zpd_delta: {round(node.get('zpd_delta', 0), 3)}

# Zeigarnik Loop
open_question: "{node.get('open_question', '')}"
resolves_question_from: "{node.get('resolves_from', '')}"
tension_level: {node.get('tension_level', 'medium')}

# MCMC Analytics
priority: {node.get('priority', 0.0)}
centrality: {node.get('centrality', 0.0)}
impact_unlocks: {node.get('impact_unlocks', 0)}
criticality: {str(node.get('criticality', False)).lower()}
sigma_c: {node.get('sigma_c', 0.0)}

# Workflow
estimated_minutes: {node.get('estimated_minutes', 20)}
verified: false
tags:
  - learning-path
  - {node['level']}
  - {domain.lower().replace(' ', '-')}
  - {node.get('status', 'gap')}
---"""

    # Status badge
    status = node.get("status", "gap")
    badges = {
        "gap":         "🔴 **GAP** — Not yet started",
        "in-progress": "🟡 **IN PROGRESS** — Partially learned",
        "mastered":    "🔵 **MASTERED** — Consolidated",
        "scaffold":    "🟣 **SCAFFOLD** — Bridge node",
    }
    status_badge = badges.get(status, "")

    # Criticality warning
    criticality_block = ""
    if node.get("criticality"):
        criticality_block = f"""
> [!warning] ⚠️ Critical Node (σ_c = {node.get('sigma_c', 0):.3f})
> This node is at a **phase transition** in the energy landscape.
> Study with increased attention. Reduce step size. Maximise Zeigarnik tension.
"""

    # Zeigarnik block
    open_q = node.get("open_question", "")
    resolves = node.get("resolves_from", "")
    zeigarnik_block = ""
    if resolves:
        zeigarnik_block += f"\n> [!note] ✅ Resolves: *\"{resolves}\"*\n"
    if open_q:
        tension = node.get("tension_level", "medium")
        tension_icons = {"high": "🔥", "medium": "⚡", "low": "💭"}
        icon = tension_icons.get(tension, "⚡")
        zeigarnik_block += f"\n> [!question] {icon} Open Question ({tension} tension)\n> {open_q}\n"

    body = f"""
# {node['title']}

{status_badge}

**Path position**: {node.get('path_position', '?')} | **Level**: {node['level']} | **Cluster**: {node['cluster']}
**Priority**: {node.get('priority', 0):.3f} | **Centrality**: {node.get('centrality', 0):.3f} | **Unlocks**: {node.get('impact_unlocks', 0)} nodes
**ZPD Δ**: {node.get('zpd_delta', 0):.2f} | **Est. time**: {node.get('estimated_minutes', 20)} min
{criticality_block}
---

## Core Concept

<!-- 
  Write your notes on "{node['title']}" here.
  Aim to explain in your own words — this drives the Zeigarnik loop.
-->

{zeigarnik_block}

---

## Prerequisites

{"None (entry point)" if not node.get('prerequisites') else chr(10).join(f"- {p}" for p in node['prerequisites'])}

## Unlocks

{"No direct successors" if not node.get('unlocks') else chr(10).join(f"- {u}" for u in node['unlocks'])}

---

## Review

**Mastery self-rating** (update after study):
- [ ] 0.00 — No recall
- [ ] 0.25 — Partial recall, major gaps
- [ ] 0.50 — Reasonable recall, some gaps
- [ ] 0.75 — Good recall, minor gaps
- [ ] 1.00 — Full mastery, can teach it

**Next review**: {next_review}
"""

    return frontmatter + body


# ─── Canvas Generation ─────────────────────────────────────────────────────────

def generate_canvas(path_nodes: list[dict], analytics: dict) -> str:
    """Generate Obsidian-compatible .canvas JSON."""
    canvas_nodes = []
    canvas_edges = []

    # Group nodes by level for layout
    by_level: dict[str, list[dict]] = {"L0": [], "L1": [], "L2": [], "L3": []}
    for node in path_nodes:
        lvl = node.get("level", "L2")
        by_level.setdefault(lvl, []).append(node)

    node_to_canvas_id: dict[str, str] = {}

    # Group containers
    for level, level_nodes in by_level.items():
        if not level_nodes:
            continue
        row_count = math.ceil(len(level_nodes) / COLS_PER_ROW)
        group_w = COLS_PER_ROW * (NODE_W + H_GAP) + H_GAP
        group_h = row_count * (NODE_H + V_GAP) + V_GAP + 40
        y_base = LEVEL_Y.get(level, 0)

        canvas_nodes.append({
            "id": f"group_{level}",
            "type": "group",
            "label": f"{level}: {'Governing Principles' if level=='L0' else 'Atomic Concepts' if level=='L1' else 'Composite Topics' if level=='L2' else 'Detail'}",
            "x": -40,
            "y": y_base - 60,
            "width": group_w,
            "height": group_h + 60,
            "color": LEVEL_COLORS.get(level, "4"),
        })

        for idx, node in enumerate(level_nodes):
            col = idx % COLS_PER_ROW
            row = idx // COLS_PER_ROW
            x = col * (NODE_W + H_GAP)
            y = y_base + row * (NODE_H + V_GAP) + (20 if node.get("criticality") else 0)

            canvas_id = f"node_{node['id']}"
            node_to_canvas_id[node["id"]] = canvas_id
            safe_name = safe_filename(node["title"])

            canvas_nodes.append({
                "id": canvas_id,
                "type": "file",
                "file": f"concepts/{safe_name}.md",
                "x": x,
                "y": y,
                "width": NODE_W,
                "height": NODE_H,
                "color": STATUS_COLORS.get(node.get("status", "gap"), "1"),
            })

    # Edges (sequential path)
    for i in range(len(path_nodes) - 1):
        curr = path_nodes[i]
        nxt  = path_nodes[i + 1]
        curr_cid = node_to_canvas_id.get(curr["id"])
        nxt_cid  = node_to_canvas_id.get(nxt["id"])
        if not curr_cid or not nxt_cid:
            continue

        delta = nxt.get("zpd_delta", 0)
        is_critical = curr.get("criticality") or nxt.get("criticality")

        if is_critical:
            edge_color = ZPD_EDGE_COLORS["critical"]
        elif delta <= ZPD_OPTIMAL:
            edge_color = ZPD_EDGE_COLORS["optimal"]
        elif delta <= 0.40:
            edge_color = ZPD_EDGE_COLORS["acceptable"]
        else:
            edge_color = ZPD_EDGE_COLORS["violation"]

        tension_icon = {"high": "🔥", "medium": "⚡", "low": "💭"}.get(curr.get("tension_level", "medium"), "⚡")

        canvas_edges.append({
            "id": f"edge_{curr['id']}_{nxt['id']}",
            "fromNode": curr_cid,
            "toNode": nxt_cid,
            "fromSide": "right",
            "toSide": "left",
            "label": f"Δ={delta:.2f} {tension_icon}",
            "color": edge_color,
        })

    # Analytics panel
    coverage = analytics.get("coverage", "?")
    gap_count = analytics.get("gap_count", "?")
    est_hours = analytics.get("estimated_hours", "?")
    critical_titles = analytics.get("critical_node_titles", [])
    crit_str = ", ".join(critical_titles[:3]) if critical_titles else "None"

    canvas_nodes.append({
        "id": "analytics_panel",
        "type": "text",
        "text": f"## 📊 Analytics\n\n**Coverage**: {coverage}%\n**Gap nodes**: {gap_count}\n**Est. hours**: {est_hours}h\n**Critical**: {crit_str}\n\n---\n\n### Legend\n🔴 Gap  🟡 In Progress  🔵 Mastered  🟣 Scaffold\n🔥 High tension  ⚡ Medium  💭 Low\nEdge color: 🟦 Optimal  🟨 Acceptable  🟥 Violation  🟪 Critical",
        "x": (COLS_PER_ROW * (NODE_W + H_GAP)) + 80,
        "y": 0,
        "width": 380,
        "height": 400,
        "color": "6",
    })

    return json.dumps({"nodes": canvas_nodes, "edges": canvas_edges}, indent=2)


# ─── Base Generation ───────────────────────────────────────────────────────────

BASE_JSON = {
    "filters": {"and": [{"file.hasTag": "learning-path"}]},
    "views": [
        {
            "type": "table", "name": "🔴 Gap Priority Queue",
            "sort": [{"property": "priority", "direction": "desc"}],
            "filter": {"property": "status", "operator": "in", "value": ["gap", "in-progress"]},
            "columns": ["title", "level", "mastery", "difficulty", "zpd_delta", "priority", "criticality", "estimated_minutes", "open_question"],
        },
        {
            "type": "table", "name": "⚡ Today's Session",
            "sort": [{"property": "priority", "direction": "desc"}],
            "filter": {"or": [
                {"property": "next_review", "operator": "lte", "value": "today"},
                {"and": [
                    {"property": "status", "operator": "eq", "value": "gap"},
                    {"property": "path_position", "operator": "lte", "value": 3},
                ]},
            ]},
            "columns": ["title", "open_question", "tension_level", "zpd_delta", "estimated_minutes", "criticality", "sigma_c"],
        },
        {
            "type": "cards", "name": "🌀 Zeigarnik Board",
            "groupBy": "tension_level",
            "filter": {"property": "open_question", "operator": "ne", "value": ""},
            "cardFields": ["title", "open_question", "resolves_question_from", "mastery", "path_position"],
        },
        {
            "type": "table", "name": "⚠️ Critical Nodes",
            "sort": [{"property": "sigma_c", "direction": "asc"}],
            "filter": {"and": [
                {"property": "criticality", "operator": "eq", "value": True},
                {"property": "status", "operator": "ne", "value": "mastered"},
            ]},
            "columns": ["title", "sigma_c", "tension_level", "zpd_delta", "priority", "mastery"],
        },
        {
            "type": "table", "name": "✅ Spaced Repetition",
            "sort": [{"property": "next_review", "direction": "asc"}],
            "filter": {"property": "status", "operator": "eq", "value": "mastered"},
            "columns": ["title", "mastery", "review_count", "next_review", "last_reviewed"],
        },
        {
            "type": "table", "name": "📍 Full Path",
            "sort": [{"property": "path_position", "direction": "asc"}],
            "columns": ["path_position", "title", "level", "status", "mastery", "zpd_delta", "tension_level", "criticality", "estimated_minutes"],
        },
    ],
}


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Obsidian Vault Emitter")
    parser.add_argument("--path", required=True, help="path.json from mcmc_traversal.py")
    parser.add_argument("--vault", required=True, help="Output vault directory")
    parser.add_argument("--domain", default="Knowledge Domain")
    args = parser.parse_args()

    vault = Path(args.vault)
    concepts_dir = vault / "concepts"
    meta_dir     = vault / "meta"
    analytics_dir = vault / "analytics"

    for d in [concepts_dir, meta_dir, analytics_dir]:
        d.mkdir(parents=True, exist_ok=True)

    path_nodes: list[dict] = json.loads(Path(args.path).read_text())
    print(f"📦 Emitting vault: {len(path_nodes)} nodes → {vault}")

    # Pre-filter: wikilinks must resolve within this path slice
    path_ids = {n["id"] for n in path_nodes}
    for node in path_nodes:
        node["prerequisites"] = [p for p in (node.get("prerequisites") or [])
                                   if p.replace("[[","").replace("]]","").strip() in path_ids]
        node["unlocks"] = [u for u in (node.get("unlocks") or [])
                           if u.replace("[[","").replace("]]","").strip() in path_ids]

    # ── Write .md files ────────────────────────────────────────────────────────
    for node in path_nodes:
        md_content = generate_md(node, args.domain)
        filename = safe_filename(node["title"]) + ".md"
        (concepts_dir / filename).write_text(md_content, encoding="utf-8")

    print(f"   ✅ {len(path_nodes)} concept notes written")

    # ── Compute analytics for canvas ────────────────────────────────────────────
    mastered = sum(1 for n in path_nodes if n.get("status") == "mastered")
    coverage = round(mastered / max(len(path_nodes), 1) * 100, 1)
    gap_count = len(path_nodes) - mastered
    est_hours = round(sum(n.get("estimated_minutes", 20) for n in path_nodes if n.get("status") != "mastered") / 60, 1)
    critical_nodes = [n for n in path_nodes if n.get("criticality")]

    analytics = {
        "coverage": coverage,
        "gap_count": gap_count,
        "estimated_hours": est_hours,
        "critical_node_titles": [n["title"] for n in critical_nodes],
    }

    # ── Write .canvas ──────────────────────────────────────────────────────────
    canvas_json = generate_canvas(path_nodes, analytics)
    (vault / "path.canvas").write_text(canvas_json, encoding="utf-8")
    print(f"   ✅ Canvas written: path.canvas")

    # ── Write .base ────────────────────────────────────────────────────────────
    (vault / "progress.base").write_text(json.dumps(BASE_JSON, indent=2), encoding="utf-8")
    print(f"   ✅ Base tracker written: progress.base")

    # ── Write lessons.md ───────────────────────────────────────────────────────
    lessons = f"""---
title: Meta Learning Log
domain: "{args.domain}"
created: "{date.today().isoformat()}"
tags: [meta, self-improvement, learning-path]
---

# Self-Improvement Log: {args.domain}

## Session Log

| Date | Nodes Studied | Mastery Δ | Notes |
|---|---|---|---|
| {date.today().isoformat()} | (initial generation) | — | Vault created |

## Calibration History

| Date | Parameter | Old Value | New Value | Reason |
|---|---|---|---|---|
| {date.today().isoformat()} | ZPD optimal | — | 0.22 | Default |
| {date.today().isoformat()} | EMA alpha | — | 0.30 | Default |
| {date.today().isoformat()} | MASTERED threshold | — | 0.85 | Default |

## Recurring Errors

<!-- Track systematic gaps or misconceptions here -->

## Path Quality Notes

<!-- Record if MCMC path ordering felt wrong — helps recalibrate -->
"""
    (meta_dir / "lessons.md").write_text(lessons, encoding="utf-8")
    print(f"   ✅ Lessons log written: meta/lessons.md")

    # ── Write analytics YAML ───────────────────────────────────────────────────
    import yaml
    full_analytics = {
        "generation_date": date.today().isoformat(),
        "domain": args.domain,
        "total_nodes": len(path_nodes),
        "mastered": mastered,
        "coverage_pct": coverage,
        "gap_count": gap_count,
        "estimated_study_hours": est_hours,
        "critical_nodes": [n["id"] for n in critical_nodes],
        "next_3_nodes": [
            {"node": n["title"], "est_minutes": n.get("estimated_minutes", 20), "tension": n.get("tension_level", "medium")}
            for n in path_nodes[:3] if n.get("status") != "mastered"
        ],
    }
    (analytics_dir / "status_report.yaml").write_text(yaml.dump(full_analytics, default_flow_style=False))
    print(f"   ✅ Analytics written: analytics/status_report.yaml")

    print(f"\n🎉 Vault ready: {vault}")
    print(f"   Coverage: {coverage}% ({mastered}/{len(path_nodes)} mastered)")
    print(f"   Est. study: {est_hours}h")
    if critical_nodes:
        print(f"   ⚠️  Critical nodes: {', '.join(n['title'] for n in critical_nodes[:3])}")


if __name__ == "__main__":
    main()
