# AI4PKM Configuration Reference

## Complete orchestrator.yaml Structure

```yaml
version: "1.0"

orchestrator:
  prompts_dir: _Settings_/Prompts
  tasks_dir: _Settings_/Tasks  
  logs_dir: _Settings_/Logs
  skills_dir: _Settings_/Skills
  max_concurrent: 3
  poll_interval: 1

defaults:
  executor: claude_code
  timeout_minutes: 30
  max_parallel: 3
  task_create: true

nodes:
  - type: agent
    name: Enrich Ingested Content (EIC)
    input_path: Ingest/Clippings
    output_path: AI/Articles
    executor: claude_code

pollers:
  limitless:
    enabled: true
    target_dir: "Ingest/Limitless"
    poll_interval: 300
```

## Node Configuration Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `type` | ✓ | Node type | `agent` |
| `name` | ✓ | Agent display name | `Enrich Ingested Content (EIC)` |
| `prompt` | | Prompt file reference (ABBR) | `EIC` |
| `input_path` | | Input directory for file triggers | `Ingest/Clippings` |
| `output_path` | | Output directory | `AI/Articles` |
| `executor` | | Execution engine | `claude_code`, `codex_cli`, `gemini_cli` |
| `cron` | | Schedule expression | `"15,45 * * * *"` |
| `enabled` | | Enable/disable agent | `true` / `false` |
| `timeout_minutes` | | Execution timeout | `30` |
| `completion_status` | | Post-completion status | `DONE`, `IGNORE` |
| `agent_params` | | Agent-specific parameters | (object) |
| `workers` | | Multi-worker configuration | (list) |

## Worker Configuration Fields

For multi-worker setups (AI model comparison):

| Field | Description | Example |
|-------|-------------|---------|
| `executor` | AI execution engine | `claude_code`, `gemini_cli` |
| `label` | Worker identification | `Claude`, `Gemini` |
| `output_path` | Worker-specific output | `AI/Summary/Claude` |
| `agent_params` | Worker-specific parameters | (object) |

## Node Types

### File-Triggered Agents
- Triggered by new/updated files in `input_path`
- Requires `input_path` and `output_path`
- Example: Content enrichment, summarization

### Scheduled Agents  
- Time-based execution using cron expressions
- Requires `cron` and `output_path`
- Example: Daily workflows, periodic reports

## Poller Configuration

### Limitless
```yaml
limitless:
  enabled: true
  target_dir: "Ingest/Limitless"
  poll_interval: 300  # 5 minutes
```

### Apple Photos
```yaml
apple_photos:
  enabled: true
  target_dir: "Ingest/Photos"
  albums:
    - "Screenshots"
    - "PKM"
    - "Important"
```

### Apple Notes
```yaml
apple_notes:
  enabled: true
  target_dir: "Ingest/Notes"
  folders:
    - "Quick Notes"
    - "Meeting Notes"
```

## Defaults Section

Global settings applied to all nodes unless overridden:

```yaml
defaults:
  executor: claude_code        # Default AI engine
  timeout_minutes: 30         # Default timeout
  max_parallel: 3             # Max concurrent workers
  task_create: true           # Auto-create tasks
```

## Agent Parameters

Common `agent_params` configurations:

### Daily Driver Workflow (DDW)
```yaml
agent_params:
  calendars:
    - Default
    - Work
  past_hours: 24
  future_days: 3
  goals_file: _Settings_/Goals & Principles.md
  roundup_lookback_days: 7
```

### Content Enrichment
```yaml
agent_params:
  min_content_length: 100
  max_content_length: 10000
  extract_keywords: true
  generate_summary: true
```