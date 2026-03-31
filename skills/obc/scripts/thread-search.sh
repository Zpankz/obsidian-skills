#!/bin/bash
# thread-search.sh — Search daily notes for intention/belief/decision patterns
# Usage: thread-search.sh "<pattern>"
# Example: thread-search.sh "I believe"
#          thread-search.sh "decided|chose|going to"
set -euo pipefail

PATTERN=${1:?"Usage: thread-search.sh '<pattern>'"}

echo "=== SEARCHING DAILY NOTES FOR: $PATTERN ==="
obsidian search:context query="$PATTERN" path="Daily Notes" format=json | jq '.' 2>/dev/null || \
  obsidian search query="$PATTERN" path="Daily Notes" format=json
