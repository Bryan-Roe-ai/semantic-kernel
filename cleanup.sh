#!/bin/bash
# Repository Cleanup Script
# This script removes temporary files and directories that shouldn't be in the repository

set -e

echo "🧹 Semantic Kernel Repository Cleanup"
echo "======================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to safely remove directory
safe_remove_dir() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo -e "${YELLOW}Removing directory: $dir${NC}"
        rm -rf "$dir"
        echo -e "${GREEN}✓ Removed $dir${NC}"
    else
        echo -e "Directory not found (skipping): $dir"
    fi
}

# Function to safely remove file
safe_remove_file() {
    local file=$1
    if [ -f "$file" ]; then
        echo -e "${YELLOW}Removing file: $file${NC}"
        rm -f "$file"
        echo -e "${GREEN}✓ Removed $file${NC}"
    else
        echo -e "File not found (skipping): $file"
    fi
}

echo "1. Cleaning up Python build directories..."
safe_remove_dir "Python-3.12.4"
safe_remove_dir "Python-3.12.5"
safe_remove_dir "tmp/Python-3.12.5"

echo ""
echo "2. Cleaning up virtual environments..."
safe_remove_dir "agi-venv"
safe_remove_dir "clean-venv"
safe_remove_dir "python-clean"
safe_remove_dir ".venv-1"

echo ""
echo "3. Cleaning up Python cache files..."
safe_remove_dir "__pycache__"
safe_remove_dir ".mypy_cache"
safe_remove_dir ".pytest_cache"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo ""
echo "4. Cleaning up temporary directories..."
safe_remove_dir "tmp"

echo ""
echo "5. Cleaning up build artifacts..."
safe_remove_dir "19-miscellaneous/bin"
safe_remove_dir "19-miscellaneous/obj"

echo ""
echo "6. Checking for large files..."
echo "Files larger than 1MB (excluding git objects):"
find . -type f -size +1M ! -path "./.git/*" -exec ls -lh {} \; 2>/dev/null | awk '{print $9, $5}' || echo "None found"

echo ""
echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo ""
echo "Recommendations:"
echo "  • Run 'git status' to see what was removed"
echo "  • Run 'git add -A' to stage changes"
echo "  • Consider adding .venv to your active virtual environment"
echo "  • Run 'pre-commit install' to set up pre-commit hooks"
echo ""
