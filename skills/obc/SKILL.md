---
name: obc
description: "30 Obsidian vault commands for AI-augmented PKM — daily ops, vault intelligence, thinking tools, creation, strategy. Triggers on /context /today /close-day /schedule /7plan /map /emerge /connect /contradict /drift /backlinks /graduate /graph /audit /ghost /trace /challenge /stranger /compound /ideas /learned /weekly-learnings /make /xdaily /xarticle /synthesize /evolve /money /leverage /guests, or any request to read/analyze an Obsidian vault, plan a day/week, find connections, generate ideas from vault patterns, challenge beliefs, trace idea evolution, or any structured vault interaction. Trigger proactively — turns a passive vault into an active thinking partner."
---

# OBC — Obsidian Commands

30 vault commands for AI-augmented personal knowledge management. Every command reads from an Obsidian vault in real time using the `obsidian` CLI at `/usr/local/bin/obsidian`.

## Requirements

- **Obsidian must be running** (the CLI talks to the running app)
- `obsidian` CLI installed at `/usr/local/bin/obsidian`
- Some commands integrate with Google Calendar, Google Tasks, and Gmail MCPs (optional)

## How This Skill Works

1. **Match** the user's request to a command using the router below
2. **Run shared scripts** from `scripts/` to gather structural data (avoid repeating the same 5-6 CLI commands in every prompt)
3. **Read the prompt file** from the vault at `references/Prompt - <Name>.md` for full command instructions
4. **Execute** the command following the prompt's step-by-step workflow

The prompt files in the vault are the source of truth. This skill is the orchestration layer — routing, shared tooling, workflow chains, and agents.

## Command Router

### Daily Operations — Routine workflows

| Command | Vault File | When to Use |
|---------|-----------|-------------|
| `/context` | `Prompt - Context.md` | Before starting any work — loads full vault context |
| `/today` | `Prompt - Today.md` | Morning planning — calendar + tasks + vault patterns |
| `/close-day` | `Prompt - Close Day.md` | Evening — extract, categorize, file insights from today |
| `/schedule` | `Prompt - Schedule.md` | Scheduling decisions — evaluates against priorities |
| `/7plan` | `Prompt - 7plan.md` | Weekly planning — reshapes 7 days around live threads |

### Vault Intelligence — Discovery and structural analysis

| Command | Vault File | When to Use |
|---------|-----------|-------------|
| `/map` | `Prompt - Map.md` | Topological view — clusters, themes, gaps, shape of thinking |
| `/emerge` | `Prompt - Emerge.md` | Surface ideas the vault implies but never states |
| `/connect` | `Prompt - Connect.md` | Find bridges between two specific domains |
| `/contradict` | `Prompt - Contradict.md` | Find incompatible beliefs held simultaneously |
| `/drift` | `Prompt - Drift.md` | Compare stated intentions vs. actual behavior |
| `/backlinks` | `Prompt - Backlinks.md` | Wire missing connections in the vault graph |
| `/graduate` | `Prompt - Graduate.md` | Promote daily note ideas to standalone notes |
| `/graph` | `Prompt - Graph.md` | Quantitative graph analytics — centrality, communities |
| `/audit` | `Prompt - Audit.md` | Vault health check — KPIs + prioritized action plan |

### Thinking Tools — Reflection, challenge, temporal analysis

| Command | Vault File | When to Use |
|---------|-----------|-------------|
| `/ghost` | `Prompt - Ghost.md` | Answer a question AS the vault's author |
| `/trace` | `Prompt - Trace.md` | Track how an idea evolved over weeks/months |
| `/challenge` | `Prompt - Challenge.md` | Pressure-test beliefs using vault evidence |
| `/stranger` | `Prompt - Stranger.md` | Portrait of who you are from an outsider reading cold |
| `/compound` | `Prompt - Compound.md` | Same question at 3 time periods — shows context compounding |

### Creation & Output — Producing content from vault material

| Command | Vault File | When to Use |
|---------|-----------|-------------|
| `/ideas` | `Prompt - Ideas.md` | Generate ideas across domains from vault patterns |
| `/learned` | `Prompt - Learned.md` | Turn a topic into writing at 3 levels (post/essay/universal) |
| `/weekly-learnings` | `Prompt - Weekly Learnings.md` | Compile week's insights for a team email |
| `/make` | `Prompt - Make.md` | Score vault ideas on readiness to become real work |
| `/xdaily` | `Prompt - XDaily.md` | Pull X/Twitter posts into daily notes |
| `/xarticle` | `Prompt - XArticle.md` | Find what to write next — graph density x energy x synthesis |
| `/synthesize` | `Prompt - Synthesize.md` | Weave 3+ vault threads into coherent narratives |
| `/evolve` | `Prompt - Evolve.md` | Find ideas at the intersection of readiness x leverage |

### Strategy — Big-picture decisions

| Command | Vault File | When to Use |
|---------|-----------|-------------|
| `/money` | `Prompt - Money.md` | Revenue diagnosis — asset inventory, opportunities, builds |
| `/leverage` | `Prompt - Leverage.md` | Find 3-7 skills where concentrated investment = breakthrough |
| `/guests` | `Prompt - Guests.md` | Derive podcast guests from questions the vault is asking |

## Shared Scripts

Every command reuses the same building blocks. Run these scripts from `${SKILL_DIR}/scripts/` to avoid repeating boilerplate.

### `vault-scan.sh`
Structural overview used by almost every command. Outputs vault stats, top tags, orphans, deadends, unresolved links.
```bash
bash "${SKILL_DIR}/scripts/vault-scan.sh"
```

### `daily-reader.sh <N>`
Read the past N days of daily notes. Outputs today's note + N-1 previous days.
```bash
bash "${SKILL_DIR}/scripts/daily-reader.sh" 7    # Past 7 days
bash "${SKILL_DIR}/scripts/daily-reader.sh" 14   # Past 14 days
bash "${SKILL_DIR}/scripts/daily-reader.sh" 30   # Past 30 days
```

### `hub-detect.sh <N>`
Find the top N most-connected notes by backlink count. Outputs JSON with note name and count.
```bash
bash "${SKILL_DIR}/scripts/hub-detect.sh" 15     # Top 15 hubs
```

### `context-loader.sh`
Find and read all context files. Discovers them by searching for "Context" in filenames.
```bash
bash "${SKILL_DIR}/scripts/context-loader.sh"
```

### `thread-search.sh <pattern>`
Search daily notes for intention/belief/decision patterns. Used by Contradict, Challenge, Drift, Emerge, Leverage.
```bash
bash "${SKILL_DIR}/scripts/thread-search.sh" "I believe"
bash "${SKILL_DIR}/scripts/thread-search.sh" "decided|chose|going to"
```

### `temporal-track.sh <command-name>`
Check for prior runs of a command in daily notes. Used by Ideas, Make, Money, Leverage, XArticle, Guests, Synthesize, Evolve, Audit.
```bash
bash "${SKILL_DIR}/scripts/temporal-track.sh" "/ideas"
```

## Execution Pattern

For any command:

1. **Run `vault-scan.sh`** unless the command explicitly skips it (XDaily, Weekly Learnings)
2. **Run `daily-reader.sh N`** with N appropriate to the command (7 for daily ops, 14-21 for vault intelligence, 30+ for strategy)
3. **Read the prompt file** from the vault: `Read file="references/Prompt - <Name>.md"`
4. **Follow the prompt's steps** — use the shared scripts where the prompt calls for vault scans, daily note reads, or hub detection
5. **Run `temporal-track.sh`** if the prompt has a "Temporal Tracking" section (prevents redundant suggestions across runs)

## Workflow Chains

Commands work together. Common chains:

**Morning ritual**: `/context` → `/today`
**Evening ritual**: `/close-day`
**Weekly planning**: `/7plan` → `/drift`
**Deep discovery**: `/emerge` → `/connect` → `/synthesize` → `/make`
**Content pipeline**: `/ideas` → `/xarticle` → `/learned`
**Strategy session**: `/money` → `/leverage` → `/evolve`
**Vault maintenance**: `/map` → `/graph` → `/audit` → `/backlinks` → `/graduate`

When a user asks for a chain (e.g., "plan my week"), run the commands in sequence, passing context forward.

## Command Disambiguation

When it's unclear which command the user needs:

| User wants... | Use | Not |
|---------------|-----|-----|
| Connections between 2 specific domains | `/connect` | `/emerge` (implicit patterns) |
| Ideas the vault implies but never states | `/emerge` | `/ideas` (generates new ones) |
| Weave 3+ threads into a narrative | `/synthesize` | `/connect` (only 2 domains) |
| Incompatible beliefs held now | `/contradict` | `/challenge` (pressure-tests) |
| How thinking changed over time | `/trace` | `/contradict` (simultaneous beliefs) |
| Vault structure narrative | `/map` | `/graph` (quantitative metrics) |
| Vault health + action plan | `/audit` | `/map` (no action plan) |
| Fix missing links | `/backlinks` | `/map` (only analyzes) |
| Score idea readiness to ship | `/make` | `/ideas` (generates, doesn't score) |
| Readiness x strategic leverage | `/evolve` | `/make` (readiness only) |
| What to write next for X | `/xarticle` | `/ideas` (all domains, not X-specific) |
| Daily note ideas → standalone | `/graduate` | `/emerge` (vault-wide, not daily notes) |
| Quantitative graph metrics | `/graph` | `/map` (qualitative narrative) |

## CLI Conventions

All commands use the `obsidian` CLI (lowercase). These conventions apply everywhere:

- `format=json` — Always use for machine-readable output when processing results
- `counts format=json` — On `backlinks` for quantitative hub detection
- `jq` — Slice/filter JSON output (e.g., `| jq '.[0:20]'`)
- `obsidian vault` — Quick stats before any deep analysis
- `obsidian recents` — Catch recently modified non-daily notes
- `obsidian tasks todo verbose format=json` — Vault-embedded tasks
- `obsidian wordcount file="X"` — Measure thinking density (words, not just links)
- `obsidian outline file="X" format=json` — Structure before reading full content
- `obsidian search:context` — Use instead of `search` when you need matching lines
- `obsidian backlinks file="X" counts format=json` — Ranked connections, not just a list

## Confidence Markers

Many commands reference confidence markers in context files:
- `[solid]` — High confidence, tested through experience
- `[evolving]` — Active development, changing
- `[hypothesis]` — Untested, speculative
- `[questioning]` — Under review, may change

## Agents

For expensive operations, use the agents in `agents/`:

- **vault-scanner** (`agents/vault-scanner.md`) — Runs structural analysis in parallel. Use when a command needs vault scan + daily notes + context files simultaneously.
- **thread-tracer** (`agents/thread-tracer.md`) — Follows backlink chains 3+ hops deep. Use when Connect, Emerge, or 7plan need deep graph traversal.

## Hooks

The `hooks/hooks.json` configures:
- **SessionStart** — Suggests relevant commands based on time of day and recent vault activity
- **PostToolUse (Bash)** — After `obsidian` CLI commands, suggests related OBC commands that could use the data
