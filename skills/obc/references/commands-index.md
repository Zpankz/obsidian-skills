# OBC Commands Index

Complete reference for all 30 Obsidian vault commands. Each entry maps to a prompt file in `/Users/dev/obsidian/ObsidianCommands/`.

## Quick Reference

| # | Command | Category | Vault File | Shared Scripts Used |
|---|---------|----------|-----------|-------------------|
| 1 | `/context` | Daily Ops | Prompt - Context.md | vault-scan, daily-reader(7), context-loader |
| 2 | `/today` | Daily Ops | Prompt - Today.md | vault-scan, daily-reader(7), context-loader |
| 3 | `/close-day` | Daily Ops | Prompt - Close Day.md | daily-reader(1) |
| 4 | `/schedule` | Daily Ops | Prompt - Schedule.md | context-loader, daily-reader(5) |
| 5 | `/7plan` | Daily Ops | Prompt - 7plan.md | vault-scan, daily-reader(14), context-loader, hub-detect |
| 6 | `/map` | Intelligence | Prompt - Map.md | vault-scan, hub-detect(20) |
| 7 | `/emerge` | Intelligence | Prompt - Emerge.md | vault-scan, daily-reader(21), context-loader |
| 8 | `/connect` | Intelligence | Prompt - Connect.md | (domain-specific searches) |
| 9 | `/contradict` | Intelligence | Prompt - Contradict.md | context-loader, daily-reader(21), thread-search |
| 10 | `/drift` | Intelligence | Prompt - Drift.md | context-loader, daily-reader(30), thread-search |
| 11 | `/backlinks` | Intelligence | Prompt - Backlinks.md | vault-scan, hub-detect(20), context-loader |
| 12 | `/graduate` | Intelligence | Prompt - Graduate.md | daily-reader(14) |
| 13 | `/graph` | Intelligence | Prompt - Graph.md | vault-scan, hub-detect |
| 14 | `/audit` | Intelligence | Prompt - Audit.md | vault-scan, hub-detect, context-loader |
| 15 | `/ghost` | Thinking | Prompt - Ghost.md | daily-reader(14), context-loader |
| 16 | `/trace` | Thinking | Prompt - Trace.md | (topic-specific searches) |
| 17 | `/challenge` | Thinking | Prompt - Challenge.md | context-loader, daily-reader(14), thread-search |
| 18 | `/stranger` | Thinking | Prompt - Stranger.md | vault-scan, daily-reader(21), context-loader |
| 19 | `/compound` | Thinking | Prompt - Compound.md | context-loader, (temporal searches) |
| 20 | `/ideas` | Creation | Prompt - Ideas.md | vault-scan, daily-reader(30), context-loader, temporal-track |
| 21 | `/learned` | Creation | Prompt - Learned.md | daily-reader(3), context-loader |
| 22 | `/weekly-learnings` | Creation | Prompt - Weekly Learnings.md | daily-reader(7), context-loader |
| 23 | `/make` | Creation | Prompt - Make.md | vault-scan, temporal-track |
| 24 | `/xdaily` | Creation | Prompt - XDaily.md | daily-reader(1) |
| 25 | `/xarticle` | Creation | Prompt - XArticle.md | vault-scan, daily-reader(14), context-loader, temporal-track |
| 26 | `/synthesize` | Creation | Prompt - Synthesize.md | vault-scan, temporal-track |
| 27 | `/evolve` | Creation | Prompt - Evolve.md | vault-scan, context-loader, temporal-track |
| 28 | `/money` | Strategy | Prompt - Money.md | vault-scan, daily-reader(30), context-loader, temporal-track |
| 29 | `/leverage` | Strategy | Prompt - Leverage.md | vault-scan, daily-reader(30), context-loader, thread-search |
| 30 | `/guests` | Strategy | Prompt - Guests.md | daily-reader(30), context-loader |

## Category Descriptions

### Daily Operations (5 commands)
Routine workflows — morning planning, evening processing, scheduling, weekly reshaping. These are the "operating system" of the vault.

### Vault Intelligence (9 commands)
Discovery, structural analysis, and graph maintenance. These commands see the vault's shape and improve its structure.

### Thinking Tools (5 commands)
Reflection, challenge, and temporal analysis. These commands use the vault as a mirror — they show you your own thinking from the outside.

### Creation & Output (8 commands)
Producing content from vault material. These commands turn accumulated thinking into artifacts the world can see.

### Strategy (3 commands)
Big-picture decisions about money, leverage, and relationships. These commands go beyond the vault to find what you're not thinking about.

## Integration Points

### Google Calendar MCP
Used by: /today, /schedule, /7plan, /drift, /ideas, /weekly-learnings

### Google Tasks MCP
Used by: /today, /7plan

### Gmail MCP
Used by: /today, /7plan, /drift

### Browser Automation (for X/Twitter)
Used by: /xdaily
