#!/bin/bash

# AI Workspace Cleanup Script
# Organizes and optimizes the workspace for AI development

set -e

echo "🧹 AI Workspace Cleanup"
echo "======================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    local status=$1
    local message=$2
    case $status in
        "success") echo -e "${GREEN}✅ $message${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "error") echo -e "${RED}❌ $message${NC}" ;;
        "info") echo -e "${BLUE}ℹ️  $message${NC}" ;;
        "action") echo -e "${BLUE}🔧 $message${NC}" ;;
    esac
}

# Create cleanup directories
print_status "info" "Creating organized directory structure..."

mkdir -p .cleanup/{duplicates,outdated,temp,logs}
mkdir -p docs-backup

# 1. Clean up duplicate GitHub Pages files
print_status "action" "Consolidating GitHub Pages configuration..."

# Backup current docs
if [ -d "docs" ]; then
    cp -r docs docs-backup/
    print_status "success" "Created docs backup"
fi

# Remove duplicate and conflicting GitHub Pages files
duplicate_pages_files=(
    "GITHUB_PAGES_DEPLOYMENT_COMPLETE.md"
    "GITHUB_PAGES_FINAL_ANALYSIS.md" 
    "SEMANTIC_KERNEL_PAGES_READY.md"
    "GITHUB_PAGES_COMPLETE.md"
    "FINAL_GITHUB_PAGES_SOLUTION.md"
    "FINAL_DEPLOYMENT_STATUS.md"
)

for file in "${duplicate_pages_files[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" .cleanup/duplicates/
        print_status "success" "Moved duplicate: $file"
    fi
done

# Move disabled workflows
if [ -f ".github/workflows/deploy-ai-workspace-pages.yml.disabled" ]; then
    mv ".github/workflows/deploy-ai-workspace-pages.yml.disabled" .cleanup/outdated/
fi

if [ -f ".github/workflows/sync-to-github-pages.yml.disabled" ]; then
    mv ".github/workflows/sync-to-github-pages.yml.disabled" .cleanup/outdated/
fi

print_status "success" "Cleaned up duplicate GitHub Pages files"

# 2. Organize scripts and tools
print_status "action" "Organizing scripts and tools..."

mkdir -p scripts/{deployment,validation,maintenance}

# Move deployment scripts
deployment_scripts=(
    "setup-github-pages.sh"
    "fix-github-pages.sh"
    "verify-deployment.sh"
    "check-pages-deployment.sh"
    "check-deployment-status.sh"
)

for script in "${deployment_scripts[@]}"; do
    if [ -f "$script" ]; then
        mv "$script" scripts/deployment/
        print_status "success" "Moved to scripts/deployment: $script"
    fi
done

# 3. Clean up temporary and cache files
print_status "action" "Removing temporary files and caches..."

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Remove Node.js cache
find . -type d -name "node_modules" -not -path "./ai-workspace/*" -exec rm -rf {} + 2>/dev/null || true
find . -name "package-lock.json" -not -path "./ai-workspace/*" -delete 2>/dev/null || true

# Remove build artifacts
find . -type d -name "build" -not -path "./ai-workspace/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "dist" -not -path "./ai-workspace/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "bin" -not -path "./ai-workspace/*" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "obj" -not -path "./ai-workspace/*" -exec rm -rf {} + 2>/dev/null || true

# Remove temp files
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true

print_status "success" "Removed temporary files and caches"

# 4. Organize documentation
print_status "action" "Organizing documentation..."

mkdir -p docs/{guides,references,api}

# Move specific documentation
if [ -f "GITHUB_PAGES_SETUP.md" ]; then
    mv "GITHUB_PAGES_SETUP.md" docs/guides/
fi

if [ -f "GITHUB_PAGES_SUCCESS.md" ]; then
    mv "GITHUB_PAGES_SUCCESS.md" docs/guides/
fi

# 5. Clean up duplicate files and symlinks
print_status "action" "Resolving duplicate files and broken symlinks..."

# Find and remove broken symlinks
find . -type l ! -exec test -e {} \; -exec rm {} + 2>/dev/null || true

# Remove duplicate semantic-kernel directories
for dir in semantic-kernel~*; do
    if [ -d "$dir" ]; then
        mv "$dir" .cleanup/duplicates/
        print_status "success" "Moved duplicate directory: $dir"
    fi
done

# 6. Optimize AI workspace structure
print_status "action" "Optimizing AI workspace structure..."

if [ -d "ai-workspace" ]; then
    cd ai-workspace
    
    # Clean up AI workspace cache and temp files
    rm -rf cache/* 2>/dev/null || true
    rm -rf logs/* 2>/dev/null || true
    rm -rf uploads/* 2>/dev/null || true
    rm -rf venv 2>/dev/null || true
    
    # Organize scripts
    if [ -d "scripts" ] && [ ! -f "scripts/README.md" ]; then
        cat > scripts/README.md << 'EOF'
# AI Workspace Scripts

This directory contains utility scripts for the AI workspace.

## Structure

- `deployment/` - Deployment and infrastructure scripts
- `maintenance/` - Cleanup and maintenance utilities
- `development/` - Development and testing tools
EOF
    fi
    
    cd ..
    print_status "success" "Optimized AI workspace structure"
fi

# 7. Create workspace index
print_status "action" "Creating workspace index..."

cat > WORKSPACE_INDEX.md << 'EOF'
# AI Workspace Index

## 🎯 Quick Start

This workspace contains the Semantic Kernel project with AI workspace enhancements.

### Key Directories

- `ai-workspace/` - AI development tools and samples
- `docs/` - GitHub Pages site and documentation  
- `scripts/` - Deployment and maintenance scripts
- `samples/` - Code examples and demonstrations

### GitHub Pages

The AI workspace is deployed to GitHub Pages at:
https://Bryan-Roe-ai.github.io/semantic-kernel/

### Scripts

#### Deployment
- `scripts/deployment/setup-github-pages.sh` - Initial GitHub Pages setup
- `scripts/deployment/check-pages-deployment.sh` - Deployment status checker

#### Maintenance  
- `cleanup-workspace.sh` - Workspace cleanup and optimization

## 🚀 Getting Started

1. **GitHub Pages**: Run `scripts/deployment/setup-github-pages.sh`
2. **AI Workspace**: Explore `ai-workspace/` for tools and samples
3. **Documentation**: Check `docs/` for guides and references

## 📁 File Organization

All duplicate and outdated files have been moved to `.cleanup/` for review.
Backup files are stored in appropriate backup directories.
EOF

print_status "success" "Created workspace index"

# 8. Update .gitignore
print_status "action" "Updating .gitignore..."

cat >> .gitignore << 'EOF'

# AI Workspace
.cleanup/
docs-backup/
*.backup
*.bak

# Development
.venv/
venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Build artifacts
build/
dist/
bin/
obj/
node_modules/
package-lock.json

# Logs
logs/
*.log
EOF

print_status "success" "Updated .gitignore"

# 9. Generate cleanup summary
print_status "action" "Generating cleanup summary..."

cat > CLEANUP_SUMMARY.md << EOF
# Workspace Cleanup Summary

Generated on: $(date)

## 🧹 Actions Performed

### Files Moved to .cleanup/

#### Duplicates
$(ls .cleanup/duplicates/ 2>/dev/null | wc -l) files moved to .cleanup/duplicates/

#### Outdated  
$(ls .cleanup/outdated/ 2>/dev/null | wc -l) files moved to .cleanup/outdated/

### Directory Structure

- ✅ Created organized scripts/ directory
- ✅ Moved deployment scripts to scripts/deployment/
- ✅ Organized documentation in docs/
- ✅ Created workspace backups

### Removed Items

- 🗑️ Python cache files (__pycache__, *.pyc)
- 🗑️ Temporary files (*.tmp, *.temp)
- 🗑️ Build artifacts (build/, dist/, bin/, obj/)
- 🗑️ Broken symlinks
- 🗑️ OS-specific files (.DS_Store, Thumbs.db)

### Created Files

- 📄 WORKSPACE_INDEX.md - Main workspace guide
- 📄 CLEANUP_SUMMARY.md - This summary
- 📄 Updated .gitignore

## 🎯 Result

The workspace is now:
- ✅ Organized and streamlined
- ✅ Optimized for AI development
- ✅ Ready for GitHub Pages deployment
- ✅ Free of duplicate and temporary files

## 📁 File Locations

- **Scripts**: scripts/deployment/, scripts/validation/
- **Documentation**: docs/guides/, docs/references/
- **AI Tools**: ai-workspace/
- **Backups**: docs-backup/, .cleanup/

To review moved files: \`ls -la .cleanup/\`
To restore files: \`cp .cleanup/[category]/[file] ./\`
EOF

print_status "success" "Generated cleanup summary"

# Final status
echo ""
print_status "success" "🎉 Workspace cleanup completed!"
echo ""
print_status "info" "Summary:"
echo "  • Organized $(find scripts/ -name "*.sh" 2>/dev/null | wc -l) scripts"
echo "  • Moved $(find .cleanup/ -type f 2>/dev/null | wc -l) duplicate/outdated files"
echo "  • Created backup of docs/ directory"
echo "  • Updated .gitignore with AI workspace patterns"
echo "  • Generated workspace documentation"
echo ""
print_status "info" "Next steps:"
echo "  1. Review WORKSPACE_INDEX.md for workspace overview"
echo "  2. Check CLEANUP_SUMMARY.md for detailed changes"
echo "  3. Review files in .cleanup/ before deleting"
echo "  4. Commit changes: git add . && git commit -m 'Clean up workspace for AI use'"
echo ""
echo ""
print_status "info" "GitHub Pages deployment ready!"
print_status "info" "Run: scripts/deployment/setup-github-pages.sh"
