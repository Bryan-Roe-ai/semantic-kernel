#!/bin/bash

# Comprehensive GitHub Pages Deployment Status Checker
# This script checks all aspects of GitHub Pages deployment

set -e

echo "🔍 GitHub Pages Deployment Status Check"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "success") echo -e "${GREEN}✅ $message${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "error") echo -e "${RED}❌ $message${NC}" ;;
        "info") echo -e "${BLUE}ℹ️  $message${NC}" ;;
    esac
}

# Get repository information
print_status "info" "Checking repository configuration..."

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if git remote get-url origin >/dev/null 2>&1; then
        remote_url=$(git remote get-url origin)
        repo_path=$(echo $remote_url | sed 's/.*github\.com[:/]\([^.]*\)\.git.*/\1/' | sed 's/.*github\.com[:/]\([^.]*\)$/\1/')
        username=$(echo $repo_path | cut -d'/' -f1)
        repo_name=$(echo $repo_path | cut -d'/' -f2)

        print_status "success" "Repository: $repo_path"
        print_status "info" "Expected GitHub Pages URL: https://$username.github.io/$repo_name/"
    else
        print_status "error" "No git remote configured"
        exit 1
    fi
else
    print_status "error" "Not in a git repository"
    exit 1
fi

echo ""
echo "📁 File System Checks"
echo "===================="

# Check essential files
essential_files=(
    ".github/workflows/pages.yml"
    "docs/index.html"
    "docs/custom-llm-studio.html"
    "docs/.nojekyll"
    "ai-workspace/05-samples-demos/index.html"
    "ai-workspace/05-samples-demos/custom-llm-studio.html"
)

all_files_ok=true
for file in "${essential_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file" 2>/dev/null || echo "0")
        if [ "$size" -gt 100 ]; then
            print_status "success" "Found: $file ($size bytes)"
        else
            print_status "warning" "Found but small: $file ($size bytes)"
        fi
    else
        print_status "error" "Missing: $file"
        all_files_ok=false
    fi
done

# Check docs folder contents
echo ""
echo "📋 Docs Folder Contents"
echo "======================"

if [ -d "docs" ]; then
    print_status "success" "docs/ directory exists"

    doc_files=$(find docs -type f | wc -l)
    print_status "info" "Contains $doc_files files"

    # List key files
    for file in docs/*.html docs/*.js; do
        if [ -f "$file" ]; then
            size=$(stat -c%s "$file")
            print_status "success" "$(basename "$file"): $size bytes"
        fi
    done
else
    print_status "error" "docs/ directory missing"
    all_files_ok=false
fi

echo ""
echo "⚙️  Workflow Configuration"
echo "=========================="

# Check GitHub Actions workflow
if [ -f ".github/workflows/pages.yml" ]; then
    print_status "success" "GitHub Pages workflow exists"

    # Check workflow syntax
    if grep -q "Deploy AI Workspace to GitHub Pages" ".github/workflows/pages.yml"; then
        print_status "success" "Workflow has correct name"
    else
        print_status "warning" "Workflow name might be incorrect"
    fi

    if grep -q "actions/configure-pages@v5" ".github/workflows/pages.yml"; then
        print_status "success" "Uses correct Pages action version"
    elif grep -q "actions/configure-pages" ".github/workflows/pages.yml"; then
        print_status "warning" "Pages action version might be outdated"
    else
        print_status "error" "Missing configure-pages action"
    fi
else
    print_status "error" "GitHub Pages workflow missing"
    all_files_ok=false
fi

# Check for conflicting workflows
echo ""
echo "🔄 Workflow Conflicts"
echo "===================="

conflicting_workflows=$(find .github/workflows -name "*.yml" | grep -E "(deploy|pages|jekyll)" | grep -v "pages.yml" | grep -v "\.disabled$" || true)

if [ -z "$conflicting_workflows" ]; then
    print_status "success" "No conflicting workflows found"
else
    print_status "warning" "Found potential conflicting workflows:"
    echo "$conflicting_workflows"
fi

echo ""
echo "📊 Git Status"
echo "============"

# Check git status
if git diff-index --quiet HEAD -- 2>/dev/null; then
    print_status "success" "No uncommitted changes"
else
    print_status "warning" "Uncommitted changes detected"
    print_status "info" "Run: git add . && git commit -m 'Update GitHub Pages' && git push"
fi

# Check if we're ahead of origin
if git rev-list --count @{u}..HEAD 2>/dev/null | grep -q "^0$"; then
    print_status "success" "All changes pushed to origin"
else
    unpushed=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "unknown")
    print_status "warning" "$unpushed commit(s) not yet pushed"
    print_status "info" "Run: git push origin main"
fi

echo ""
echo "🌐 Deployment Validation"
echo "======================="

# Test if the site might be accessible
pages_url="https://$username.github.io/$repo_name/"
print_status "info" "Testing site accessibility: $pages_url"

if command -v curl >/dev/null 2>&1; then
    if curl -s --head "$pages_url" | head -n 1 | grep -q "200 OK"; then
        print_status "success" "Site is accessible!"
    elif curl -s --head "$pages_url" | head -n 1 | grep -q "404"; then
        print_status "warning" "Site returns 404 (might still be deploying)"
    else
        print_status "warning" "Site not yet accessible (GitHub Pages may need time to deploy)"
    fi
else
    print_status "warning" "curl not available, cannot test site accessibility"
fi

echo ""
echo "📋 Summary"
echo "=========="

if [ "$all_files_ok" = true ]; then
    print_status "success" "All essential files are present"
    echo ""
    echo "✨ Next Steps:"
    echo "1. Ensure you've pushed all changes: git push origin main"
    echo "2. Go to repository Settings > Pages"
    echo "3. Set source to 'GitHub Actions'"
    echo "4. Wait 1-5 minutes for deployment"
    echo "5. Visit: $pages_url"
    echo ""
    echo "🔗 Quick Links:"
    echo "   Repository: https://github.com/$repo_path"
    echo "   Actions: https://github.com/$repo_path/actions"
    echo "   Settings: https://github.com/$repo_path/settings/pages"
    echo "   Your Site: $pages_url"
else
    print_status "error" "Some essential files are missing or invalid"
    echo ""
    echo "🔧 To fix issues:"
    echo "1. Run: ./setup-github-pages.sh"
    echo "2. Commit and push changes"
    echo "3. Run this script again"
fi
