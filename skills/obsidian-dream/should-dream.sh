#!/usr/bin/env bash
#
# should-dream.sh - Check if dream consolidation should run
#
# Returns exit code 0 if dream should run, 1 if not.
# Condition: 24+ hours since last consolidation.
#
# Scans all Claude Code project memory dirs for .last-dream timestamps.

set -euo pipefail

# Find the most recent .last-dream across all project memory dirs
LAST_DREAM_FILE=""
LATEST_TS=0

for dir in "$HOME/.claude/projects/"*/memory/; do
    if [[ -f "$dir/.last-dream" ]]; then
        TS=$(cat "$dir/.last-dream" 2>/dev/null || echo "0")
        if (( TS > LATEST_TS )); then
            LATEST_TS=$TS
            LAST_DREAM_FILE="$dir/.last-dream"
        fi
    fi
done

# If no .last-dream found anywhere, dream has never run
if [[ -z "$LAST_DREAM_FILE" ]]; then
    echo "Dream conditions met: first-run (no .last-dream found)"
    exit 0
fi

# Check: 24+ hours since last consolidation
NOW=$(date +%s)
ELAPSED=$(( NOW - LATEST_TS ))
HOURS_ELAPSED=$(( ELAPSED / 3600 ))

if (( HOURS_ELAPSED < 24 )); then
    exit 1  # Too soon
fi

echo "Dream conditions met: ${HOURS_ELAPSED}h since last dream"
exit 0
