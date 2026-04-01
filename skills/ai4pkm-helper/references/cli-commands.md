# AI4PKM CLI Commands Reference

## Core Commands

### Configuration Management
```bash
ai4pkm --show-config         # Display current configuration
ai4pkm --validate-config     # Check orchestrator.yaml syntax
ai4pkm --reload-config       # Reload configuration without restart
ai4pkm --backup-config       # Create timestamped config backup
```

### Agent Management  
```bash
ai4pkm --list-agents         # Show all configured agents
ai4pkm --list-agents --enabled  # Show only enabled agents
ai4pkm --run <agent_name>    # Execute specific agent manually
ai4pkm --enable <agent_name> # Activate agent
ai4pkm --disable <agent_name># Deactivate agent
ai4pkm --test <agent_name>   # Dry run (validate without execution)
```

### Status and Monitoring
```bash
ai4pkm --status              # Show orchestrator status
ai4pkm --status --detail     # Detailed status with next execution times
ai4pkm --logs                # Show recent execution logs
ai4pkm --logs --agent <name> # Logs for specific agent
ai4pkm --logs --tail         # Follow logs in real-time
ai4pkm --metrics             # Performance and execution metrics
```

### Orchestrator Control
```bash
ai4pkm --start               # Start orchestrator service
ai4pkm --stop                # Stop orchestrator service  
ai4pkm --restart             # Restart orchestrator service
ai4pkm --pause               # Pause all agents temporarily
ai4pkm --resume              # Resume paused agents
```

### Task Management
```bash
ai4pkm --tasks               # List all tasks
ai4pkm --tasks --status pending  # Filter by status
ai4pkm --add-task <description>  # Create new task
ai4pkm --complete-task <id>      # Mark task as completed
```

### Poller Management
```bash
ai4pkm --pollers             # Show poller status
ai4pkm --sync <poller_name>  # Manual sync for specific poller
ai4pkm --sync-all            # Force sync all enabled pollers
ai4pkm --poller-logs <name>  # Show poller-specific logs
```

### Development and Debug
```bash
ai4pkm --debug               # Enable debug logging
ai4pkm --dry-run             # Simulate execution without changes
ai4pkm --export-logs         # Export logs to file
ai4pkm --health-check        # System health validation
ai4pkm --clear-cache         # Clear temporary caches
```

## Command Examples

### Daily Workflow Management
```bash
# Check what's running
ai4pkm --status

# Run daily workflow manually  
ai4pkm --run "Daily Driver Workflow (DDW)"

# Check recent activity
ai4pkm --logs --tail

# Pause everything for maintenance
ai4pkm --pause
# ... do maintenance ...
ai4pkm --resume
```

### Troubleshooting
```bash
# Validate configuration
ai4pkm --validate-config

# Check specific agent
ai4pkm --test "Enrich Ingested Content (EIC)"

# Debug problematic agent
ai4pkm --debug --run "Problem Agent"

# Check system health
ai4pkm --health-check
```

### Multi-Worker Monitoring
```bash
# Check worker status
ai4pkm --status --detail

# Compare worker performance  
ai4pkm --metrics --workers

# Monitor specific comparison
ai4pkm --logs --agent "Article Summary Comparison"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Agent execution error |
| 4 | Poller error |
| 5 | Permission error |

## Configuration Paths

```bash
# Default locations
~/.ai4pkm/config/orchestrator.yaml    # User config
./orchestrator.yaml                   # Project config (takes precedence)
~/.ai4pkm/logs/                      # Log directory
~/.ai4pkm/cache/                     # Cache directory
```

## Environment Variables

```bash
export AI4PKM_CONFIG_PATH="/custom/path/orchestrator.yaml"
export AI4PKM_LOG_LEVEL="DEBUG"      # DEBUG, INFO, WARN, ERROR
export AI4PKM_MAX_WORKERS=5          # Override max concurrent workers
export AI4PKM_TIMEOUT=60             # Default timeout in minutes
```