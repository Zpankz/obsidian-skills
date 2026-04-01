<!--
DIRECTORY TREE (orientation)
references/05-agent-orchestration.md
  Covers: parallel agent roles · S2 background comparator · orchestration protocol
  Depends on: none
  Used by: /path build (orchestration layer)
-->

# Multi-Agent Orchestration

## Contents
- [Agent Roster](#agent-roster)
- [Orchestration Protocol](#orchestration-protocol)
- [System-2 Background Agents](#system-2-agents)
- [Context Boundary Rules](#context-boundary-rules)
- [Agent Spec Files](#agent-spec-files)

---

## Agent Roster

| Agent | Model | Role | Context Budget |
|---|---|---|---|
| `gkg-builder` | Sonnet | RPP L0–L3 domain decomposition | 2000 tok |
| `pkg-scanner` | Haiku | Vault frontmatter mastery extraction | 500 tok |
| `gap-analyzer` | Sonnet | Δ computation + centrality ranking | 1000 tok |
| `path-planner` | Sonnet | ZPD + Zeigarnik sequencing | 1500 tok |
| `s2-comparator` | Haiku | Background alternative path evaluation | 800 tok |
| `vault-emitter` | Haiku | Parallel .md/.canvas/.base file writer | 500 tok |

**Total max context**: ~6300 tokens across all agents (vs. ~20k+ for monolithic approach)

---

## Orchestration Protocol

```
PHASE 1: Parallel (independent inputs)
  ┌─────────────────┐    ┌─────────────────┐
  │  gkg-builder    │    │  pkg-scanner    │
  │  RPP(domain)→   │    │  scan(vault)→   │
  │  GKG.json       │    │  PKG.json       │
  └────────┬────────┘    └────────┬────────┘
           │                      │
           └──────────┬───────────┘
                      ▼
PHASE 2: Sequential (dependent on Phase 1)
           ┌──────────────────┐
           │   gap-analyzer   │
           │ Δ = GKG \ PKG   │
           │ rank by priority │
           └────────┬─────────┘
                    │
           ┌────────┴──────────────────┐
           ▼                           ▼  (parallel)
  ┌──────────────────┐      ┌──────────────────────┐
  │  path-planner    │      │   s2-comparator       │
  │  Main path:      │      │   Background:         │
  │  MCMC-H sequence │      │   Alt hypothesis paths│
  │  + Zeigarnik     │      │   (3 alternatives)    │
  └────────┬─────────┘      └────────────┬──────────┘
           │                             │
           └──────────┬──────────────────┘
                      ▼  (merge: pick best path)
PHASE 3: Parallel (independent outputs)
  ┌───────────┬──────────────┬────────────┐
  ▼           ▼              ▼            ▼
.md files  .canvas        .base        lessons.md
(vault-emitter × N workers)
```

**Main context never sees agent internals.** Each agent returns only its output
artifact. The orchestrator merges artifacts; reasoning traces stay in subagent contexts.

---

## System-2 Background Agents

**Design principle**: S2 agents run alternative hypotheses in parallel with the main
reasoning agent. They evaluate paths that are plausible but not the primary choice,
without polluting the main context.

### S2-Comparator Role

```
Task: Given gap_priority_queue.yaml and path.json (primary path),
      generate 3 alternative path orderings and evaluate:
        1. Coverage-optimised path  (max nodes mastered by exam date)
        2. Risk-minimised path      (lowest variance, safest progression)
        3. Vertex-compression path  (minimum nodes, maximum LO coverage via vertices)

Output: comparison_report.yaml
  primary:       MCMC-H path score
  coverage_alt:  coverage-optimised score
  risk_alt:      risk-minimised score
  vertex_alt:    compression score
  recommendation: which path or hybrid to adopt
```

**S2 runs in Haiku** (fast, cheap) while Sonnet runs the main MCMC traversal.
Results merged by orchestrator; if S2 finds superior path, path-planner is
re-invoked with the alternative as warm start.

### S2 Trigger Conditions

```python
s2_conditions = [
    # Coverage feasibility mismatch
    lambda: status.estimated_hours > 1.5 × available_hours,
    
    # High variance in MCMC acceptance rate
    lambda: hmc.acceptance_rate < 0.50,
    
    # Multiple critical nodes in sequence (risky cluster)
    lambda: sum(1 for n in path if n.criticality) > 3,
    
    # Path position 1-3 all have high ZPD delta (cold start zone)
    lambda: all(path[i].zpd_delta > 0.30 for i in range(3)),
]
# Any condition True → spawn s2-comparator
```

---

## Context Boundary Rules

**Rule 1: One task per agent** — agents never cross-call each other.
**Rule 2: Artifacts only** — agents pass JSON/YAML, never raw reasoning text.
**Rule 3: Context budget enforced** — each agent has hard token limits.
**Rule 4: Main context stays clean** — only final artifacts enter main context.
**Rule 5: S2 is background** — s2-comparator output injected only if triggered.

```python
class AgentBoundary:
    """Enforces context isolation between agents."""
    
    def run_agent(self, agent_name: str, input_artifact: dict) -> dict:
        # Each agent gets fresh context
        context = {
            'skill_head': self.load_skill_head(agent_name),  # schema tree only
            'input': input_artifact,
            'budget': AGENT_BUDGETS[agent_name],
        }
        result = self.invoke(agent_name, context)
        return result['output_artifact']  # only artifact returned, not trace
```

---

## Agent Spec Files

Agent spec files in `agents/` follow the sub-skill pattern:

```markdown
---
name: gap-analyzer
description: Computes PKG/GKG gap Δ and ranks nodes by centrality × impact × (1−mastery).
  Input: gkg.json + pkg.json. Output: gap_priority_queue.yaml + centrality_scores.yaml.
allowed-tools: "bash"
---
<!--
DIRECTORY TREE
agents/gap-analyzer.md (this file — complete agent spec)
-->

# Gap Analyzer Agent

Input artifacts:
  - gkg.json (from gkg-builder)
  - pkg.json (from pkg-scanner)

Process:
  1. python scripts/pkg_gkg_diff.py --gkg gkg.json --pkg pkg.json --output gap.json
  2. Inject centrality scores into gap node metadata
  3. Emit gap_priority_queue.yaml

Output artifacts:
  - gap.json
  - gap_priority_queue.yaml
  - centrality_scores.yaml
```

Each agent spec is ≤50 lines (minimal context load), executing via bash scripts
rather than in-context reasoning wherever possible.
