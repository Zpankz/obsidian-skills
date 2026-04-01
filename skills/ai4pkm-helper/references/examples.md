# AI4PKM Configuration Examples

## Complete orchestrator.yaml Examples

### Basic Single-Agent Setup

Perfect for getting started with AI4PKM:

```yaml
version: "1.0"

orchestrator:
  prompts_dir: _Settings_/Prompts
  tasks_dir: _Settings_/Tasks
  logs_dir: _Settings_/Logs
  max_concurrent: 2
  poll_interval: 1

defaults:
  executor: claude_code
  timeout_minutes: 30
  task_create: true

nodes:
  - type: agent
    name: Enrich Articles (EA)
    input_path: Ingest/Articles
    output_path: AI/Enriched
    executor: claude_code
    prompt: EA
    enabled: true
```

### Multi-Agent Workflow

Comprehensive setup with multiple specialized agents:

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
  max_parallel: 2
  task_create: true

nodes:
  # File-triggered agents
  - type: agent
    name: Enrich Ingested Content (EIC)
    input_path: Ingest/Clippings
    output_path: AI/Articles
    executor: claude_code
    prompt: EIC
    enabled: true
    completion_status: DONE

  - type: agent
    name: Summarize Research (SR)
    input_path: Ingest/Research
    output_path: AI/Summaries
    executor: claude_code
    prompt: SR
    enabled: true
    timeout_minutes: 45

  - type: agent
    name: Meeting Notes Processor (MNP)
    input_path: Ingest/Meetings
    output_path: AI/Meetings
    executor: claude_code
    prompt: MNP
    enabled: true

  # Scheduled agents
  - type: agent
    name: Daily Driver Workflow (DDW)
    cron: "15,45 * * * *"
    output_path: Journal
    executor: claude_code
    prompt: DDW
    enabled: true
    agent_params:
      calendars:
        - Default
        - Work
      past_hours: 24
      future_days: 3
      goals_file: _Settings_/Goals & Principles.md
      roundup_lookback_days: 7

  - type: agent
    name: Weekly Review (WR)
    cron: "0 9 * * 1"  # Mondays at 9 AM
    output_path: Journal/Weekly
    executor: claude_code
    prompt: WR
    enabled: true

pollers:
  limitless:
    enabled: true
    target_dir: "Ingest/Limitless"
    poll_interval: 300

  apple_photos:
    enabled: false
    target_dir: "Ingest/Photos"
    albums:
      - "Screenshots"
      - "PKM"

  apple_notes:
    enabled: false
    target_dir: "Ingest/Notes"
    folders:
      - "Quick Notes"
```

### Multi-Worker AI Comparison

Setup for comparing different AI models:

```yaml
version: "1.0"

orchestrator:
  prompts_dir: _Settings_/Prompts
  tasks_dir: _Settings_/Tasks
  logs_dir: _Settings_/Logs
  max_concurrent: 5
  poll_interval: 1

defaults:
  executor: claude_code
  timeout_minutes: 30
  task_create: true

nodes:
  # Single model agents
  - type: agent
    name: Quick Content Process (QCP)
    input_path: Ingest/Quick
    output_path: AI/Quick
    executor: claude_code
    prompt: QCP
    enabled: true

  # Multi-worker comparison agents
  - type: agent
    name: Article Analysis Comparison
    input_path: Ingest/Analysis
    enabled: true
    workers:
      - executor: claude_code
        label: Claude
        output_path: AI/Analysis/Claude
        prompt: ARTICLE_ANALYSIS
      - executor: gemini_cli
        label: Gemini
        output_path: AI/Analysis/Gemini
        prompt: ARTICLE_ANALYSIS
      - executor: codex_cli
        label: Codex
        output_path: AI/Analysis/Codex
        prompt: ARTICLE_ANALYSIS

  - type: agent
    name: Content Summarization Test
    input_path: Ingest/Test
    enabled: true
    workers:
      - executor: claude_code
        label: Claude_Detailed
        output_path: AI/Test/Claude_Detailed
        agent_params:
          style: detailed
      - executor: claude_code
        label: Claude_Concise
        output_path: AI/Test/Claude_Concise
        agent_params:
          style: concise

pollers:
  limitless:
    enabled: true
    target_dir: "Ingest/Limitless"
    poll_interval: 180  # 3 minutes for testing
```

### Korean Language Optimized

Configuration optimized for Korean PKM workflows:

```yaml
version: "1.0"

orchestrator:
  prompts_dir: _Settings_/Prompts
  tasks_dir: _Settings_/Tasks  
  logs_dir: _Settings_/Logs
  max_concurrent: 2
  poll_interval: 1

defaults:
  executor: claude_code
  timeout_minutes: 45  # Longer for Korean processing
  task_create: true

nodes:
  - type: agent
    name: 한국어 콘텐츠 정리 (KCP)
    input_path: Ingest/Korean
    output_path: AI/Korean
    executor: claude_code
    prompt: KCP
    enabled: true
    agent_params:
      language: korean
      output_format: markdown

  - type: agent
    name: 일일 업무 정리 (DWO)
    cron: "30 18 * * *"  # 6:30 PM daily
    output_path: Journal/Daily
    executor: claude_code
    prompt: DWO
    enabled: true
    agent_params:
      timezone: Asia/Seoul
      language: korean

  - type: agent
    name: 회의록 처리 (MRP)
    input_path: Ingest/회의록
    output_path: AI/회의록
    executor: claude_code
    prompt: MRP
    enabled: true

pollers:
  apple_notes:
    enabled: true
    target_dir: "Ingest/Apple_Notes"
    folders:
      - "빠른 메모"
      - "업무 노트"
      - "아이디어"
```

### Development and Testing

Configuration for testing and development:

```yaml
version: "1.0"

orchestrator:
  prompts_dir: _Settings_/Prompts
  tasks_dir: _Settings_/Tasks
  logs_dir: _Settings_/Logs
  max_concurrent: 1  # Single execution for testing
  poll_interval: 5   # Frequent polling for development

defaults:
  executor: claude_code
  timeout_minutes: 15  # Short timeout for testing
  task_create: false   # Don't create tasks during testing

nodes:
  - type: agent
    name: Test Agent (TA)
    input_path: Ingest/Test
    output_path: AI/Test
    executor: claude_code
    prompt: TA
    enabled: true
    agent_params:
      debug: true
      verbose: true

  - type: agent
    name: Scheduled Test (ST)
    cron: "*/5 * * * *"  # Every 5 minutes
    output_path: AI/Scheduled_Test
    executor: claude_code
    prompt: ST
    enabled: false  # Disabled by default

# No pollers during development
pollers: {}
```

## Agent Parameter Examples

### Daily Driver Workflow Parameters
```yaml
agent_params:
  calendars:
    - Default
    - Work
    - Personal
  past_hours: 24
  future_days: 7
  goals_file: _Settings_/Goals & Principles.md
  roundup_lookback_days: 14
  include_weekends: false
  time_format: 24h
```

### Content Processing Parameters
```yaml
agent_params:
  min_content_length: 100
  max_content_length: 50000
  extract_keywords: true
  generate_summary: true
  language_detection: true
  output_format: markdown
  include_metadata: true
```

### Research Analysis Parameters
```yaml
agent_params:
  analysis_depth: detailed
  include_citations: true
  fact_checking: true
  bias_analysis: true
  confidence_scores: true
  related_topics: 5
```

## Cron Expression Examples

```yaml
# Every 15 and 45 minutes past each hour
cron: "15,45 * * * *"

# Daily at 9:00 AM
cron: "0 9 * * *"

# Weekdays at 6:30 PM
cron: "30 18 * * 1-5"

# Weekly on Mondays at 9:00 AM
cron: "0 9 * * 1"

# Monthly on the 1st at midnight
cron: "0 0 1 * *"

# Every 30 minutes during work hours (9 AM - 6 PM)
cron: "*/30 9-18 * * 1-5"
```

## Directory Structure Examples

### Basic Structure
```
vault/
├── Ingest/
│   ├── Articles/
│   ├── Clippings/
│   ├── Research/
│   └── Meetings/
├── AI/
│   ├── Articles/
│   ├── Summaries/
│   └── Meetings/
├── Journal/
│   ├── Daily/
│   └── Weekly/
└── _Settings_/
    ├── Prompts/
    ├── Tasks/
    ├── Logs/
    └── Skills/
```

### Multi-Worker Structure
```
vault/
├── Ingest/
│   ├── Analysis/
│   └── Test/
├── AI/
│   ├── Analysis/
│   │   ├── Claude/
│   │   ├── Gemini/
│   │   └── Codex/
│   └── Test/
│       ├── Claude_Detailed/
│       └── Claude_Concise/
└── _Settings_/
    └── Prompts/
```

### Korean Optimized Structure
```
vault/
├── Ingest/
│   ├── Korean/
│   ├── 회의록/
│   └── Apple_Notes/
├── AI/
│   ├── Korean/
│   └── 회의록/
├── Journal/
│   └── Daily/
└── _Settings_/
    └── Prompts/
```

## Testing Workflows

### New Configuration Testing
1. Start with minimal config (1 agent)
2. Test manually: `ai4pkm --run "Agent Name"`
3. Check output and logs
4. Add agents incrementally
5. Test pollers last

### Multi-Worker Testing
1. Configure single worker first
2. Test with small input files
3. Add second worker
4. Compare outputs
5. Scale up gradually

### Korean Language Testing
1. Test with simple Korean input
2. Verify encoding in outputs
3. Test mixed Korean/English content
4. Validate voice recognition
5. Check task creation in Korean