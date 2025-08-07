#!/bin/bash
# GitHub Actions Workflow Fixer Script

echo "🔧 Fixing GitHub Actions workflow files..."

# Function to fix common issues in workflow files
fix_workflow() {
    local file="$1"
    echo "Processing: $file"

    # Create backup
    cp "$file" "$file.backup"

    # Fix environment variable spacing
    sed -i.tmp 's/\${\{\s*\([^}]*\)\s*\}}/\${{ \1 }}/g' "$file"

    # Fix specific reference errors
    sed -i.tmp 's/\${{ env\.REFERENCE }}/\${{ env.REFERENCE_POLICY }}/g' "$file"
    sed -i.tmp 's/\${{env\.REGION }}/\${{ env.REGION }}/g' "$file"

    # Remove .tmp files
    rm -f "$file.tmp"
}

# Find and fix workflow files
find /workspaces/semantic-kernel -name "*.yml" -path "*/.github/workflows/*" | while read -r file; do
    if [[ -f "$file" ]]; then
        fix_workflow "$file"
    fi
done

# Fix specific files with known issues
echo "🎯 Applying specific fixes..."

# Fix azure login action version
find /workspaces/semantic-kernel -name "*.yml" -path "*/.github/workflows/*" -exec sed -i.tmp 's/azure\/login@v4/azure\/login@v2/g' {} \;

# Clean up temporary files
find /workspaces/semantic-kernel -name "*.tmp" -delete

echo "✅ Workflow fixes completed!"
echo "📝 Backup files created with .backup extension"
