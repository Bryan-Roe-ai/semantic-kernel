#!/bin/bash

# Script to find all README.md files and run them using enhanced_ai_runner.py
# Created by GitHub Copilot on June 24, 2025

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$ROOT_DIR/enhanced_ai_runner.py"

echo "🔍 Finding all README.md files in $ROOT_DIR..."

# Find all README.md files (case insensitive)
readmes=$(find "$ROOT_DIR" -type f -iname "README.md" | sort)

# Count total README files
total_count=$(echo "$readmes" | wc -l)
echo "📚 Found $total_count README files to process"
echo ""

# Check if enhanced_ai_runner.py exists
if [ ! -f "$RUNNER" ]; then
    echo "❌ Error: enhanced_ai_runner.py not found in the workspace!"
    exit 1
fi

CONCURRENCY=${CONCURRENCY:-1}

process_readme() {
    local file="$1"
    echo "🔄 Processing: $file"
    python3 "$RUNNER" "$file"
    echo "✅ Completed: $file"
}

export RUNNER
export -f process_readme

echo "$readmes" | xargs -r -n1 -P "$CONCURRENCY" bash -c 'process_readme "$0"'

echo "$readmes" | xargs -r -n1 -P "$CONCURRENCY" bash -c 'process_readme "$@"' _
wait
echo "🎉 All README files have been processed!"
