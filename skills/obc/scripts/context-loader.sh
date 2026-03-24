#!/bin/bash
# context-loader.sh — Discover and read all context files in the vault
# Searches for files with "Context" in the name, then reads each one
set -euo pipefail

echo "=== DISCOVERING CONTEXT FILES ==="
CONTEXT_FILES=$(obsidian search query="Context" format=json 2>/dev/null | jq -r '.[].file' | grep -i "context" || true)

if [ -z "$CONTEXT_FILES" ]; then
  echo "No context files found. Searching by tag..."
  CONTEXT_FILES=$(obsidian tag name="context" verbose format=json 2>/dev/null | jq -r '.[].file' || true)
fi

if [ -z "$CONTEXT_FILES" ]; then
  echo "No context files found in vault."
  exit 0
fi

echo "Found context files:"
echo "$CONTEXT_FILES"
echo ""

echo "$CONTEXT_FILES" | while read -r f; do
  echo ""
  echo "=== $f ==="
  obsidian read path="$f" 2>/dev/null || obsidian read file="$(basename "$f" .md)" 2>/dev/null || echo "(could not read $f)"
done
