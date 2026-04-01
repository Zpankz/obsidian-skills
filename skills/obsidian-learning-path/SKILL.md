---
name: obsidian-learning-path
description: |
  Generating optimal learning paths as Obsidian knowledge graph vaults by unifying
  Zeigarnik Effect tension threading, ZPD-calibrated edge sequencing, PKG/GKG gap
  differential analysis, RPP L0-L3 Pareto compression, MCMC-Hamiltonian path
  traversal with eigenvector centrality, compound learning self-improvement loops,
  BCME theorem-grounded plateau escape with 7-axis mechanism injection, and
  homoiconic architectural self-assessment with self-topology measurement (η≥4).
  Produces .md + .canvas + .base vault files with injected graph analytics.
  Adapted for the obsidian-skills ecosystem: integrates with obsidian-cli for live
  vault operations, ob for headless sync, obsidian-vault-manager for vault registry,
  dataview for querying, obsidian-yaml-frontmatter for property formatting,
  obsidian-dream for memory consolidation, and obsidian-canvas/json-canvas for
  visual maps. Use /olp build, /olp scan, /olp gap, /olp traverse, /olp compound,
  /olp status, /olp verify, /olp refine, /olp meta, /olp self-eval, /olp improve,
  /olp consolidate. Use when generating study curricula, knowledge graph vaults,
  adaptive learning systems, exam prep paths, or any domain requiring optimal
  traversal of a knowledge space.
tags: [pkm, learning, knowledge-graph, obsidian, mcmc, zpd, zeigarnik, spaced-repetition]
---

<!--
DIRECTORY TREE (schema-level orientation — always readable at head)
obsidian-learning-path/
├── SKILL.md                          ← you are here (entry + routing)
├── references/
│   ├── 01-theoretical-core.md        ← Zeigarnik · ZPD · MCMC-H theory
│   ├── 02-pkg-gkg-differential.md    ← gap algebra · priority formula
│   ├── 03-mcmc-hamiltonian.md        ← traversal kernel · burn-in · thinning
│   ├── 04-node-schema.md             ← frontmatter spec · base queries
│   ├── 05-agent-orchestration.md     ← subagent roles · S2 background agents
│   ├── 06-canvas-base-spec.md        ← .canvas JSON · .base filter syntax
│   ├── 07-validation-checklist.md    ← topology · ZPD · Zeigarnik audit
│   ├── 08-self-distillation-integration.md ← F1-F9 findings
│   └── 09-obsidian-integration.md    ← obsidian-cli · ob · vault-manager · dataview hooks
├── scripts/
│   ├── pkg_gkg_diff.py               ← gap computation + path sequencing
│   ├── mcmc_traversal.py             ← Hamiltonian kernel · criticality metrics
│   ├── generate_vault.py             ← .md + .canvas + .base emitter
│   ├── compound_update.py            ← post-session PKG update + resequence (v2: rich feedback)
│   ├── gkg_refine.py                 ← evolving GKG: difficulty recalibration + edge discovery
│   ├── meta_compound.py              ← meta-level mechanism injection + parameter tuning (BCME)
│   ├── self_eval.py                  ← intrinsic skill self-assessment v3 (13 sections + topology)
│   ├── self_improve.py               ← BCME loop applied to skill itself (/olp improve)
│   ├── memory_consolidate.py         ← Pareto compress session history (v4)
│   ├── validate_vault.py             ← topology · ZPD · Zeigarnik · retention audit
│   └── vault_bridge.py               ← obsidian-cli / ob / vault-manager adapter layer
├── agents/
│   ├── gkg-builder.md                ← RPP domain decomposition agent
│   ├── pkg-scanner.md                ← vault mastery state extractor
│   ├── gap-analyzer.md               ← Δ computation + centrality ranking
│   ├── path-planner.md               ← ZPD + Zeigarnik sequencer
│   ├── s2-comparator.md              ← background System-2 comparative agent
│   └── vault-emitter.md              ← parallel .md/.canvas/.base writer
└── assets/
    ├── node-template.md              ← Zeigarnik-compliant note template
    ├── canvas-template.json          ← color-coded canvas scaffold
    └── base-template.base            ← progress tracker base template
-->

```
λ.in: "domain | syllabus | vault_path | goal"
λ.out: "obsidian vault: .md + .canvas + .base + analytics"
τ.goal: "MCMC-Hamiltonian optimal path through knowledge space"
ο.class: "occurrent"
```

# Obsidian Learning Path

> **λ(PKG, GKG, H, Σ).τ** — Gap → Hamiltonian optimal path → Vault → Compound mastery

---

## Routing

| CLI Command | What It Does | Agents Spawned | Ref |
|---|---|---|---|
| `/olp build <domain>` | Full pipeline: GKG → PKG → gap → path → vault | GKG-Builder ∥ PKG-Scanner → Gap-Analyzer → Path-Planner | [01-08] |
| `/olp scan <vault>` | Scan vault for mastery state (PKG extraction) | PKG-Scanner | [02] |
| `/olp gap` | Compute and rank knowledge gaps | Gap-Analyzer | [02] |
| `/olp traverse` | Generate MCMC-H optimal path | Path-Planner + S2-Comparator | [03] |
| `/olp compound <session>` | Post-session mastery update + resequence | — | [02][03][08] |
| `/olp status` | Coverage %, next nodes, burn-in estimate | Gap-Analyzer | [02] |
| `/olp verify` | Topology · ZPD · Zeigarnik · retention audit | validate_vault.py | [07] |
| `/olp refine` | GKG difficulty recalibration + edge discovery | — | [08] |
| `/olp meta` | Parameter auto-tuning from prediction errors | — | [08] |
| `/olp self-eval` | Skill health: pass rate + failures + corrections | self_eval.py | [08] |
| `/olp improve` | Self-referential: gap-detect → classify → inject → re-eval | self_improve.py | [08] |
| `/olp consolidate` | Pareto compress old sessions → epoch summaries | memory_consolidate.py | [08] |
| `/olp sync` | Sync vault via `ob` or `obsidian-cli` | — | [09] |

**Load only what the command requires.** Routing table is the context boundary.

---

## Core Model (schema-level, always in context)

```
GKG = RPP(domain)          L0→L1→L2→L3 Pareto hierarchy (evolves via /olp refine)
PKG = scan(vault)          mastery ∈ [0,1] per node, multi-signal feedback
Δ   = GKG \ PKG            gap nodes, ranked by Priority(mechanism)
r   = log P(n|context) − log P(n)  implicit reward = self-referential gap signal
H   = Hamiltonian(Δ, ZPD)  energy-conserving traversal kernel
Path= MCMC(H, burn_in=50)  sample with thinning + retention probes + tabu filter
Vault= emit(Path, Obsidian) .md + .canvas + .base
K'  = compound(K, session)  self-improving loop with structured feedback
Σ'  = meta(Σ, errors, stall) mechanism injection + parameter tuning + tabu update
E   = self_eval(skill)     intrinsic assessment: pass_rate + corrections
H'  = consolidate(H, keep) Pareto compress old sessions → epoch summaries
I   = improve(E, skill)   BCME loop: gap-detect → classify → inject → re-eval
η   = |edges|/|nodes|     self-topology: skill measures its own graph structure
```

**Priority(node)** = selected mechanism from registry (default: Centrality × Impact × (1 − Mastery))

**ZPD constraint**: ∀ edge (u→v): 0.10 ≤ difficulty(v) − mastery(u) ≤ 0.40

**Zeigarnik constraint**: ∀ node n: open_question(n) resolved by successor(n)

**Retention constraint**: ∀ path of length K: insert retention_probe(random mastered predecessor)

**Self-demo constraint**: ∀ gap node n: scaffold from learner's own mastered prerequisites

**Tabu constraint**: ∀ failed strategy s: s ∉ proposal_set for tabu_horizon sessions

**Orthogonal constraint**: ∀ traversal: cluster coverage variance < threshold (force diversity)

### Self-Distillation Findings (ref [08])

| Tag | Finding | Integration |
|---|---|---|
| F1 | Dense credit > scalar score | Multi-signal session feedback → weighted EMA |
| F2 | GKG must evolve with learner | `/olp refine` recalibrates difficulty from data |
| F3 | Self-as-teacher via mastered nodes | Scaffold context drawn from own mastery |
| F4 | On-policy retention probes | Retention check inserted every K nodes |
| F5 | Rich structured feedback schema | concept_scores + error_types + calibration |
| F6 | Meta-compound self-modification | `/olp meta` auto-tunes α, Δ_target, probe_freq |
| F7 | Mechanism injection > param tuning | 7-axis registry: S=(X,G,T,Q,P,A,M) |
| F8 | Tabu memory for failed strategies | Failed mechanisms excluded for tabu_horizon |
| F9 | Orthogonal exploration forcing | Cluster rotation when coverage skewed |

---

## Obsidian Ecosystem Integration

This skill is adapted from the standalone `/paths` skill to work within the `obsidian-skills` ecosystem. It delegates to sibling skills for vault operations rather than reimplementing them.

### Skill Dependencies

| Capability | Delegated To | When Used |
|---|---|---|
| Live vault read/write/search | `obsidian-cli` | `/olp scan`, `/olp compound` — read frontmatter mastery via `obsidian read`, search via `obsidian search`, set properties via `obsidian property:set` |
| Headless vault sync | `ob` (obsidian-headless) | `/olp sync` — push generated vault files to Obsidian Sync |
| Vault registry & discovery | `obsidian-vault-manager` | Vault path resolution, active vault detection |
| Frontmatter formatting | `obsidian-yaml-frontmatter` | Node .md generation — ensures property names, types, dates conform to vault standards |
| Dataview queries | `dataview` | PKG scanning — query mastery state via DQL instead of raw file parsing when vault is open |
| Canvas & Base files | `obsidian-canvas`, `json-canvas` | `/olp build` emit phase — canvas layout and base view generation |
| Memory consolidation | `obsidian-dream` | Session history pruning feeds into `/olp consolidate`; dream consolidates meta-level while /olp handles learning-level |
| Breadcrumbs graph | `breadcrumbs-nav` | Optional: typed link edges (`up`, `down`, `next`) can represent path dependencies |

### Vault Bridge: How Integration Works

The vault bridge (`scripts/vault_bridge.py`) abstracts vault operations behind a unified interface. It auto-detects which method is available and uses the best one:

```
Vault operation needed
  ├── Obsidian running? → obsidian-cli (richest: live search, property set, backlinks)
  ├── ob configured? → ob sync (push/pull after generation)
  └── Fallback → direct file I/O (always works, skill-internal)
```

#### PKG Scanning via obsidian-cli + Dataview

When Obsidian is running, PKG scanning uses the live app rather than parsing files:

```bash
# Query mastery state for all learning-path notes via Dataview
obsidian eval code="
  const dv = app.plugins.plugins.dataview?.api;
  if (!dv) throw 'Dataview not installed';
  const pages = dv.pages('#learning-path');
  const pkg = pages.map(p => ({
    id: p.file.name,
    mastery: p.mastery ?? 0,
    status: p.status ?? 'gap',
    last_reviewed: p.last_reviewed ?? null,
    review_count: p.review_count ?? 0
  }));
  JSON.stringify(pkg);
"
```

**Fallback**: When Obsidian is not running, scan frontmatter directly from .md files using `scripts/pkg_gkg_diff.py --vault <path>`.

#### Compound Update via obsidian-cli

After a study session, update mastery in the live vault:

```bash
# Update mastery for a specific node
obsidian property:set file="Fick Principle" name="mastery" value="0.85" silent
obsidian property:set file="Fick Principle" name="status" value="mastered" silent
obsidian property:set file="Fick Principle" name="last_reviewed" value="2026-04-01" silent
obsidian property:set file="Fick Principle" name="review_count" value="4" silent
```

**Fallback**: Edit frontmatter directly using the Edit tool, following `obsidian-yaml-frontmatter` conventions.

#### Canvas Generation

Learning path canvases use the `json-canvas` spec. The vault-emitter agent writes:
1. `path.canvas` — color-coded visual map with analytics overlay (ref [06])
2. `progress.base` — 6-view Bases progress tracker (ref [06])

Both formats follow the specs defined in `obsidian-canvas` and `json-canvas` skills.

#### Sync After Generation

After `/olp build` completes, if `ob` is configured:

```bash
# Push generated vault to Obsidian Sync
ob sync --path <vault_path>
```

This ensures the generated learning path appears on all devices immediately.

### Memory Integration: Dream + Consolidate

Two complementary consolidation systems:

| System | Scope | What It Compresses | Trigger |
|---|---|---|---|
| `/olp consolidate` | Learning sessions | Mastery trajectories, error aggregates, mechanism effectiveness | Manual or when session_history/ > 20 files |
| `/obsidian-dream` | Cross-session meta | Preferences, corrections, decisions, vault conventions | Auto every 24hrs |

**Data flow**: Dream reads `/olp consolidate` epoch summaries as already-processed signal — it does not re-extract learning-level data. Dream handles corrections like "don't use scaffold strategy X" while consolidate handles mastery scores.

### Breadcrumbs Typed Links (Optional)

When Breadcrumbs is installed, path dependencies can be expressed as typed links:

```yaml
# In node frontmatter
up: "[[Receptor Theory]]"
next: "[[Hill Equation]]"
down:
  - "[[Spare Receptors]]"
  - "[[Receptor Desensitization]]"
```

This enables Breadcrumbs Tree View and Matrix View to visualize the learning path hierarchy alongside the canvas. The vault-emitter agent adds typed links when Breadcrumbs is detected via:

```bash
obsidian eval code="!!app.plugins.plugins['breadcrumbs']"
```

---

## Quick Start

```bash
# Full pipeline from scratch
python scripts/pkg_gkg_diff.py --domain "CICM Pharmacology" --output gap.json
python scripts/mcmc_traversal.py --gap gap.json --output path.json
python scripts/generate_vault.py --path path.json --vault ./my_vault
python scripts/validate_vault.py --vault ./my_vault

# With live vault (Obsidian running)
python scripts/vault_bridge.py scan --vault "Study Vault" --output pkg.json
python scripts/pkg_gkg_diff.py --domain "CICM Pharmacology" --pkg pkg.json --output gap.json

# Post-session compound update
python scripts/compound_update.py --path path.json --session session.json --vault ./my_vault

# Sync generated vault to all devices
ob sync --path ./my_vault

# Evolve GKG (every 5-10 sessions)
python scripts/gkg_refine.py --vault ./my_vault --gkg gkg.json --output gkg_refined.json

# Auto-tune parameters (every 10+ sessions)
python scripts/meta_compound.py --vault ./my_vault --output meta_report.yaml

# Self-evaluate skill health
python scripts/self_eval.py --skill-dir . --output eval_report.yaml

# Full self-improvement loop
python scripts/self_improve.py --skill-dir . --output improve_report.yaml

# Compress old sessions
python scripts/memory_consolidate.py --history session_history/ --keep-recent 10
```

---

## Progressive Loading Map

```
Query type                 → Load these references
─────────────────────────────────────────────────
Theory / Why it works      → [01-theoretical-core]
Gap computation / PKG/GKG  → [02-pkg-gkg-differential]
Path traversal / MCMC      → [03-mcmc-hamiltonian]
Node schema / frontmatter  → [04-node-schema]
Agent orchestration        → [05-agent-orchestration]
Canvas / Base file format  → [06-canvas-base-spec]
Validation / debugging     → [07-validation-checklist]
Self-distillation / meta   → [08-self-distillation-integration]
Obsidian integration       → [09-obsidian-integration]
```

---

## Differences from Standalone /paths

| Aspect | Standalone `/paths` | This skill (`/olp`) |
|---|---|---|
| Vault operations | Direct file I/O only | obsidian-cli → ob → file I/O (cascading fallback) |
| PKG scanning | File parsing only | Dataview DQL query when Obsidian running |
| Property updates | Edit frontmatter YAML | `obsidian property:set` when live, Edit fallback |
| Canvas generation | Internal JSON writer | Delegates to `json-canvas` skill spec |
| Sync | None | `ob sync` after generation |
| Memory | Self-contained consolidate | Coordinates with `obsidian-dream` |
| Graph visualization | Canvas only | Canvas + optional Breadcrumbs typed links |
| Vault discovery | Explicit path required | `obsidian-vault-manager` registry lookup |
| Frontmatter format | Internal spec | Defers to `obsidian-yaml-frontmatter` conventions |
