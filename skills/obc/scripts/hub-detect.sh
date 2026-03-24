#!/bin/bash
# hub-detect.sh — Find the top N most-connected notes by backlink count
# Usage: hub-detect.sh <N>  (default: 15)
# Output: JSON array of {file, count} sorted by count descending
set -euo pipefail

TOP_N=${1:-15}

echo "=== TOP $TOP_N HUB NOTES (by backlink count) ==="

# Get all files, then check backlinks for each
# This is approximate — for large vaults, sample the most likely hubs
obsidian files ext=md format=json | jq -r '.[].file' | while read -r f; do
  COUNT=$(obsidian backlinks path="$f" counts format=json 2>/dev/null | jq 'length' 2>/dev/null || echo "0")
  echo "$COUNT $f"
done | sort -rn | head -n "$TOP_N" | while read -r count file; do
  echo "  $count  $file"
done
