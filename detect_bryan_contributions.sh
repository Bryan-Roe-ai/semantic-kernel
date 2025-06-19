#!/usr/bin/env bash
# Script: detect_bryan_contributions.sh
# Purpose: Automate detection of commits and files contributed by Bryan Roe

set -euo pipefail

# Configuration
AUTHOR="Bryan‑Roe"                             # Author name or email to filter
OUTPUT_LOG="bryan_contributions.log"           # Detailed commit log output
OUTPUT_FILES="bryan_files.txt"                 # Unique list of files contributed

# Ensure we're running inside a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: This script must be run inside a git repository." >&2
  exit 1
fi

# Step 1: Export detailed commit information (SHA, date, message, files changed)
git log \
  --author="$AUTHOR" \
  --pretty=format:"Commit: %H%nDate: %ad%nMessage: %s%n" \
  --date=short \
  --name-status \
  > "$OUTPUT_LOG"

echo "Detailed log written to $OUTPUT_LOG"

# Step 2: Extract and dedupe file paths touched by the author
git log \
  --author="$AUTHOR" \
  --name-only \
  --pretty=format:"" \
  | grep -v '^$' \
  | sort -u \
  > "$OUTPUT_FILES"

echo "Unique file list written to $OUTPUT_FILES"

# Step 3: Display summary counts with error handling for empty logs
COMMIT_COUNT=$(grep -c '^Commit:' "$OUTPUT_LOG" || echo 0)
FILE_COUNT=$(wc -l < "$OUTPUT_FILES" | tr -d ' ')

echo "Total commits by $AUTHOR: $COMMIT_COUNT"
echo "Total unique files modified by $AUTHOR: $FILE_COUNT"
