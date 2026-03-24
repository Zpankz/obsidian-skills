#!/bin/bash
# daily-reader.sh — Read the past N days of daily notes
# Usage: daily-reader.sh <N>  (default: 7)
set -euo pipefail

DAYS=${1:-7}

echo "=== TODAY'S DAILY NOTE ==="
obsidian daily:read

echo ""
echo "=== PAST $((DAYS - 1)) DAYS ==="
for i in $(seq 1 $((DAYS - 1))); do
  DATE=$(date -v-${i}d +%Y-%m-%d 2>/dev/null || date -d "-${i} days" +%Y-%m-%d 2>/dev/null)
  if [ -n "$DATE" ]; then
    echo ""
    echo "--- $DATE ---"
    obsidian read path="Daily Notes/${DATE}.md" 2>/dev/null || echo "(no note for $DATE)"
  fi
done

echo ""
echo "=== RECENTLY MODIFIED (non-daily) ==="
obsidian recents
