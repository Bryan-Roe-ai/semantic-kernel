#!/bin/bash

# Script to find all README.md files and run them using enhanced_ai_runner.py
# Created by GitHub Copilot on June 24, 2025

echo "🔍 Finding all README.md files in the workspace..."

# Find all README.md files (case insensitive)
readmes=$(find /home/broe/semantic-kernel -type f -iname "README.md" | sort)

# Count total README files
total_count=$(echo "$readmes" | wc -l)
echo "📚 Found $total_count README files to process"
echo ""

# Check if enhanced_ai_runner.py exists
if [ ! -f "/home/broe/semantic-kernel/enhanced_ai_runner.py" ]; then
    echo "❌ Error: enhanced_ai_runner.py not found in the workspace!"
    exit 1
fi

# Process each README file
count=0
for readme in $readmes; do
    count=$((count + 1))
    echo "🔄 [$count/$total_count] Processing: $readme"
    python3 /home/broe/semantic-kernel/enhanced_ai_runner.py "$readme"
    echo "✅ Completed: $readme"
    echo "-----------------------------------------"
    
    # Optional: add a small delay between processing files
    sleep 1
done

echo "🎉 All README files have been processed!"
echo "Total files processed: $count"
