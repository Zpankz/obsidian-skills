#!/bin/bash
# vault-scan.sh — Standard structural scan used by almost every OBC command
# Outputs: vault stats, top 20 tags, orphan count, deadends, ranked unresolved links
set -euo pipefail

echo "=== VAULT OVERVIEW ==="
obsidian vault

echo ""
echo "=== TOP 20 TAGS ==="
obsidian tags counts sort=count format=json | jq '.[0:20]'

echo ""
echo "=== ORPHANS ==="
ORPHAN_COUNT=$(obsidian orphans total 2>/dev/null || echo "?")
echo "Orphan count: $ORPHAN_COUNT"
obsidian orphans

echo ""
echo "=== DEADENDS ==="
obsidian deadends

echo ""
echo "=== UNRESOLVED LINKS (ranked by frequency) ==="
obsidian unresolved counts verbose format=json
