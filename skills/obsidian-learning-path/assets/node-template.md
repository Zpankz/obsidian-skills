---
# ── Identity ──────────────────────────────────────────────────
id: "node_{{uuid}}"
title: "{{TITLE}}"
aliases: []

# ── Graph Position ─────────────────────────────────────────────
level: L2
domain: "{{DOMAIN}}"
cluster: "{{CLUSTER}}"
path_position: {{POSITION}}

# ── PKG State ──────────────────────────────────────────────────
mastery: 0.0
last_reviewed: null
review_count: 0
next_review: "{{NEXT_REVIEW}}"
status: gap

# ── ZPD Calibration ────────────────────────────────────────────
difficulty: 0.50
prerequisites:
  - "[[{{PREREQ}}]]"
unlocks:
  - "[[{{UNLOCK}}]]"
zpd_delta: 0.50

# ── Zeigarnik Loop ─────────────────────────────────────────────
open_question: "{{OPEN_QUESTION}}"
resolves_question_from: "{{RESOLVES_FROM}}"
tension_level: medium

# ── MCMC Analytics ─────────────────────────────────────────────
priority: 0.0
centrality: 0.0
impact_unlocks: 0
criticality: false
sigma_c: 0.0

# ── Workflow ───────────────────────────────────────────────────
estimated_minutes: 20
verified: false
tags:
  - learning-path
  - L2
  - {{DOMAIN_TAG}}
  - gap
---

# {{TITLE}}

🔴 **GAP** — Not yet started

**Path**: {{POSITION}} | **Level**: L2 | **Cluster**: {{CLUSTER}}

> [!question] ⚡ Open Question (medium tension)
> {{OPEN_QUESTION}}

---

## Core Concept

<!-- Write your notes here. Explain in your own words. -->

---

## Prerequisites

- [[{{PREREQ}}]]

## Unlocks

- [[{{UNLOCK}}]]

---

## Review

- [ ] 0.00 — No recall
- [ ] 0.25 — Partial recall
- [ ] 0.50 — Reasonable recall
- [ ] 0.75 — Good recall
- [ ] 1.00 — Full mastery

**Next review**: {{NEXT_REVIEW}}
