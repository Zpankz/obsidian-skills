# AI4PKM Troubleshooting Guide

## Common Issues and Solutions

### Configuration Problems

#### YAML Syntax Errors
**Symptoms**: Config not loading, validation errors
**Solutions**:
- Check indentation (use spaces, not tabs)
- Validate quotes around strings with special characters
- Use `ai4pkm --validate-config` before applying
- Common mistake: Missing quotes around cron expressions

```yaml
# ❌ Wrong
cron: 15,45 * * * *

# ✅ Correct  
cron: "15,45 * * * *"
```

#### Agent Not Found
**Symptoms**: "Agent not found" when running commands
**Solutions**:
- Check agent name exactly matches config (case-sensitive)
- Use `ai4pkm --list-agents` to verify names
- Reload config: `ai4pkm --reload-config`

#### Prompts Not Found
**Symptoms**: Agent runs but fails to find prompt file
**Solutions**:
- Verify prompt file exists in `prompts_dir`
- Check filename matches agent's `prompt` field + ".md"
- Example: `prompt: EIC` → needs `EIC.md` file

### Execution Issues

#### Agent Not Triggering
**Symptoms**: Files added to input_path but agent doesn't run
**Check List**:
1. Agent enabled: `ai4pkm --status`
2. Orchestrator running: `ai4pkm --status`
3. File permissions: Agent can read input directory
4. Path format: Use forward slashes, relative to vault root

**Debug Steps**:
```bash
ai4pkm --test "Agent Name"    # Dry run
ai4pkm --debug --run "Agent Name"  # Verbose logging
ai4pkm --logs --agent "Agent Name"  # Check recent logs
```

#### Scheduled Agent Not Running
**Symptoms**: Cron-based agents not executing at scheduled times
**Solutions**:
- Verify cron expression: Use online cron validator
- Check system timezone vs cron timezone
- Ensure orchestrator is running continuously
- Test manually first: `ai4pkm --run "Agent Name"`

#### Multi-Worker Conflicts
**Symptoms**: Workers interfering with each other, missing outputs
**Solutions**:
- Ensure unique `output_path` for each worker
- Check concurrent limits in orchestrator config
- Stagger execution if needed
- Monitor with `ai4pkm --status --detail`

### Poller Issues

#### Limitless Not Syncing
**Check List**:
1. Limitless app running and accessible
2. `enabled: true` in poller config
3. Target directory exists and writable
4. Network connectivity to Limitless API

**Debug Steps**:
```bash
ai4pkm --pollers              # Check poller status
ai4pkm --sync limitless       # Manual sync test
ai4pkm --poller-logs limitless # Check sync logs
```

#### Apple Photos/Notes Integration
**Common Issues**:
- Permission denied: Grant accessibility permissions
- Albums/folders not found: Check exact names (case-sensitive)
- No new content: Verify album/folder contains new items
- Sync delay: Apple APIs have rate limits

### Performance Issues

#### Slow Execution
**Causes**: Large files, complex prompts, API rate limits
**Solutions**:
- Reduce file size or split large inputs
- Optimize prompts for efficiency
- Increase timeout: `timeout_minutes: 60`
- Monitor with `ai4pkm --metrics`

#### High Resource Usage
**Solutions**:
- Reduce `max_concurrent` in orchestrator config
- Stagger scheduled agents
- Use `ai4pkm --pause` during high-load periods
- Check disk space for output directories

#### Memory Issues
**Symptoms**: Orchestrator crashes, out of memory errors
**Solutions**:
- Restart orchestrator: `ai4pkm --restart`
- Clear caches: `ai4pkm --clear-cache`
- Reduce concurrent workers
- Archive old logs and outputs

### Korean Language Issues

#### Encoding Problems
**Symptoms**: Korean text appears garbled in outputs
**Solutions**:
- Ensure UTF-8 encoding in all config files
- Check system locale settings
- Verify Korean text properly saved in prompt files

#### Voice Recognition
**Symptoms**: Korean speech not recognized properly
**Solutions**:
- Speak clearly with natural pauses
- Use `min_listen_duration=8` for better capture
- Mix languages naturally (don't force pure Korean)
- Check microphone permissions

### Emergency Procedures

#### Complete Reset
```bash
ai4pkm --stop                 # Stop orchestrator
ai4pkm --backup-config        # Backup current config
ai4pkm --validate-config      # Check for issues
ai4pkm --start                # Restart fresh
```

#### Rollback Configuration
```bash
# Restore from backup
cp ~/.ai4pkm/config/orchestrator.yaml.backup orchestrator.yaml
ai4pkm --reload-config
```

#### Log Analysis
```bash
ai4pkm --logs --tail          # Follow real-time logs
ai4pkm --export-logs          # Export for analysis
ai4pkm --health-check         # System diagnostics
```

## Error Code Reference

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue normally |
| 1 | General error | Check logs for details |
| 2 | Configuration error | Fix orchestrator.yaml |
| 3 | Agent execution error | Check agent config/prompts |
| 4 | Poller error | Check poller configuration |
| 5 | Permission error | Check file permissions |

## Getting Help

1. **Check logs first**: `ai4pkm --logs`
2. **Validate configuration**: `ai4pkm --validate-config`
3. **Test health**: `ai4pkm --health-check`
4. **Provide context**: Include error messages, config snippets, and logs when asking for help

## Prevention Tips

- **Regular backups**: `ai4pkm --backup-config` before major changes
- **Test changes**: Use `--test` and `--dry-run` flags
- **Monitor health**: Regular `ai4pkm --status` checks
- **Update gradually**: Change one agent at a time
- **Document changes**: Note what works for future reference