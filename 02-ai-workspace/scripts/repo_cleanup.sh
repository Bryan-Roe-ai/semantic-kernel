#!/bin/bash

# Repository cleanup script
set -e

echo "🧹 Cleaning up AI Workspace repository..."

# Remove Python cache files
echo "Cleaning Python cache files..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Remove temporary files
echo "Cleaning temporary files..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.swo" -delete 2>/dev/null || true

# Remove OS-specific files
echo "Cleaning OS-specific files..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "desktop.ini" -delete 2>/dev/null || true

# Remove editor backup files
echo "Cleaning editor backup files..."
find . -name "*.orig" -delete 2>/dev/null || true
find . -name "*.rej" -delete 2>/dev/null || true
find . -name "*.bak" -delete 2>/dev/null || true

# Clean up logs (keep recent ones)
echo "Cleaning old log files..."
find ./logs -name "*.log" -mtime +7 -delete 2>/dev/null || true

# Clean up cache directories
echo "Cleaning cache directories..."
find ./cache -name "*" -mtime +1 -delete 2>/dev/null || true

# Create/update .gitignore if needed
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cp .gitignore.template .gitignore 2>/dev/null || true
fi

# Show summary
echo "✅ Repository cleanup completed!"

# Check git status
if command -v git &> /dev/null; then
    echo ""
    echo "📊 Git status:"
    git status --porcelain | head -10

    untracked_count=$(git status --porcelain | grep "^??" | wc -l)
    modified_count=$(git status --porcelain | grep "^ M" | wc -l)

    echo ""
    echo "Summary: $untracked_count untracked, $modified_count modified files"
fi

echo ""
echo "🎉 Repository is clean and ready!"
