#!/bin/bash
# temporal-track.sh — Check for prior runs of a command in daily notes
# Usage: temporal-track.sh "<command-name>"
# Example: temporal-track.sh "/ideas"
set -euo pipefail

COMMAND=${1:?"Usage: temporal-track.sh '<command-name>'"}

echo "=== PRIOR RUNS OF $COMMAND ==="
RESULTS=$(obsidian search query="$COMMAND" path="Daily Notes" format=json 2>/dev/null)
COUNT=$(echo "$RESULTS" | jq 'length' 2>/dev/null || echo "0")

if [ "$COUNT" = "0" ] || [ "$COUNT" = "null" ]; then
  echo "No prior runs found. This is the first run."
else
  echo "Found $COUNT daily notes mentioning $COMMAND:"
  echo "$RESULTS" | jq -r '.[].file' 2>/dev/null
  echo ""
  echo "Read these to check which suggestions were acted on vs. ignored."
fi
