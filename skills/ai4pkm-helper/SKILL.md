---
name: ai4pkm-helper
description: Configure AI4PKM orchestrator, agents, multi-worker AI comparisons, pollers, and automation. Triggers on: orchestrator setup, yaml config, agent creation, multi-worker comparison, AI model testing, claude vs gemini, poller sync, limitless integration, apple photos/notes, cron scheduling, workflow automation, task management, korean PKM, "에이전트 추가", "워커 설정", "limitless 연동", "스케줄 설정", file triggers, scheduled tasks, automation workflows, CLI commands, troubleshooting AI4PKM issues, or Korean language AI operations.
---

# AI4PKM Helper

Configure AI4PKM orchestrator for automated PKM workflows. Handles YAML configuration, multi-agent setups, AI model comparisons, and poller integrations with Korean language support.

## Core Capabilities

- **Orchestrator Setup**: File triggers and cron scheduling
- **Multi-Worker AI**: Compare Claude, Gemini, Codex outputs
- **Poller Integration**: Sync Limitless, Apple Photos/Notes
- **Korean PKM**: Bilingual workflow automation
- **Task Management**: Automated tracking and status updates

## Primary Workflows

### 1. First-Time Orchestrator Setup

**Process**:
1. Check current state: `ai4pkm --show-config`
2. Explain automation benefits and show basic structure
3. Create minimal orchestrator.yaml with one agent
4. Validate: `ai4pkm --validate-config && ai4pkm --status`
5. Test manually: `ai4pkm --run "Agent Name"`
6. Enable and monitor: `ai4pkm --enable "Agent Name"`

**Core Structure**:
```yaml
orchestrator:
  max_concurrent: 2
  poll_interval: 1
defaults:
  executor: claude_code
  timeout_minutes: 30
nodes:
  - type: agent
    name: Content Enricher
    input_path: Ingest/Articles
    output_path: AI/Enriched
    prompt: CE
```

### 2. Adding New Agents

**File-Triggered Agent** (processes files in input directory):
1. Choose trigger path and output path
2. Select executor (recommend claude_code)
3. Create corresponding prompt file
4. Add to orchestrator.yaml nodes section
5. Test: `ai4pkm --test "Agent Name"`

**Scheduled Agent** (runs on cron schedule):
1. Define cron expression (use quotes!)
2. Set output path for results
3. Configure any agent_params needed
4. Validate timing: `ai4pkm --status --detail`

**Management Commands**:
- `ai4pkm --list-agents` - View all configured
- `ai4pkm --run <name>` - Execute manually
- `ai4pkm --enable/disable <name>` - Toggle activation

### 3. Multi-Worker AI Comparison

**Setup Process**:
1. Identify content for comparison testing
2. Choose AI models (claude_code, gemini_cli, codex_cli)
3. Create separate output paths for each model
4. Configure workers array with unique labels
5. Test with small sample first
6. Compare outputs and performance

**Key Structure**:
```yaml
- name: Content Analysis Comparison
  input_path: Ingest/Test
  workers:
    - executor: claude_code
      label: Claude
      output_path: AI/Test/Claude
    - executor: gemini_cli
      label: Gemini
      output_path: AI/Test/Gemini
```

**Benefits**: Model quality comparison, A/B testing, performance benchmarking

### 4. External Data Sync (Pollers)

**Setup Process**:
1. Choose data source (limitless, apple_photos, apple_notes)
2. Create target directory for synced content
3. Configure poll_interval (recommend 300s = 5min)
4. Test sync: `ai4pkm --sync <poller_name>`
5. Monitor: `ai4pkm --pollers`

**Common Configurations**:
- **Limitless**: Voice recordings → `Ingest/Limitless`
- **Apple Photos**: Screenshots from specific albums
- **Apple Notes**: Quick notes and meeting notes

**Commands**:
- `ai4pkm --pollers` - Status of all pollers
- `ai4pkm --sync limitless` - Manual sync
- `ai4pkm --poller-logs <name>` - Troubleshoot issues

### 5. Task Workflow Management

**Process**:
1. Configure `task_create: true` in defaults
2. Agents auto-create tasks when processing content
3. Track progress: `ai4pkm --tasks`
4. Update status: `ai4pkm --complete-task <id>`

**Manual Task Management**:
- `ai4pkm --add-task "Description"` - Create task
- `ai4pkm --tasks --status pending` - Filter by status
- Categories: 🔍 Research, 📐 Design, 🛠️ Implement, ✍️ Write, 📝 Docs

## Korean Language Support

**Natural Conversation**: Mix Korean/English fluently
**Patient Listening**: `min_listen_duration=8`, avoid interrupting
**Progress Updates**: 
- "설정 확인 중이에요..." (checking configuration)
- "에이전트 추가하는 중입니다..." (adding agent)
- "완료되었습니다!" (completed)

**Common Triggers**:
- "에이전트 추가해줘" → Add new agent
- "워커 설정하고 싶어" → Multi-worker setup
- "limitless 연동해줘" → Connect limitless
- "스케줄 설정해줘" → Configure cron schedule

## Example Interactions

### Adding New Agent
**User**: "에이전트 추가해줘" / "Add new agent"
**Process**:
1. Ask for trigger type (file vs scheduled)
2. Get paths or cron expression
3. Select executor (recommend claude_code)
4. Create configuration
5. Test with sample execution

### Multi-Worker Comparison
**User**: "여러 AI로 비교하고 싶어" / "Compare multiple AI models"
**Process**:
1. Explain multi-worker benefits
2. Select models for comparison
3. Configure separate output paths
4. Set worker labels
5. Test with sample input

### Poller Setup
**User**: "limitless 연동해줘" / "Connect limitless"
**Process**:
1. Check current poller status
2. Configure target directory
3. Set poll interval (recommend 300s)
4. Enable poller
5. Test sync operation

## Implementation Guidelines

**Semi-Automatic Execution**: Require user confirmation for each step
- **Proceed**: "완료", "다음", "계속", "yes", "continue"
- **Pause**: "중단", "나중에", "stop", "cancel"

**Error Prevention**:
- Validate YAML syntax before saving
- Backup working configurations  
- Test with small input sets first
- Monitor execution logs: `ai4pkm --logs`

**Best Practices**:
- Use descriptive names with abbreviations
- Organize output paths by function
- Set appropriate timeouts for tasks
- Monitor with `ai4pkm --status`

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not running | `ai4pkm --status` → check logs → verify paths |
| Poller not syncing | Verify `enabled: true` and poll_interval |
| Multi-worker conflicts | Ensure unique output_path per worker |
| Config not applied | `ai4pkm --restart` |
| YAML syntax error | Validate indentation and format |

For detailed configuration options, CLI commands, examples, and troubleshooting, see the `references/` directory.

## Quick Reference

**Status Check**: `ai4pkm --status --detail`
**View Config**: `ai4pkm --show-config`
**Manual Run**: `ai4pkm --run "Agent Name"`
**Follow Logs**: `ai4pkm --logs --tail`
**Health Check**: `ai4pkm --health-check`

Always provide clear error messages in both Korean and English, with specific fix suggestions.