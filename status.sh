#!/bin/bash

# AI Workspace Status Checker
# Quick validation of workspace organization and deployment readiness

set -e

echo "🔍 AI Workspace Status Check"
echo "============================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m' 
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

status_ok() { echo -e "${GREEN}✅ $1${NC}"; }
status_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
status_error() { echo -e "${RED}❌ $1${NC}"; }
status_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Check workspace organization
echo ""
status_info "Checking workspace organization..."

if [ -f "WORKSPACE_INDEX.md" ]; then
    status_ok "Workspace index exists"
else
    status_error "Missing WORKSPACE_INDEX.md"
fi

if [ -d "scripts/deployment" ]; then
    script_count=$(find scripts/deployment -name "*.sh" | wc -l)
    status_ok "Deployment scripts organized ($script_count scripts)"
else
    status_error "Missing scripts/deployment directory"
fi

if [ -d ".cleanup" ]; then
    cleanup_count=$(find .cleanup -type f | wc -l)
    status_ok "Cleanup completed ($cleanup_count files moved)"
else
    status_warn "No cleanup directory found"
fi

# Check GitHub Pages setup
echo ""
status_info "Checking GitHub Pages configuration..."

if [ -f ".github/workflows/pages.yml" ]; then
    status_ok "GitHub Pages workflow exists"
else
    status_error "Missing GitHub Pages workflow"
fi

if [ -d "docs" ]; then
    docs_files=$(find docs -name "*.html" | wc -l)
    status_ok "Docs folder ready ($docs_files HTML files)"
    
    # Check key files
    if [ -f "docs/index.html" ]; then
        status_ok "Homepage ready ($(stat -c%s "docs/index.html") bytes)"
    else
        status_error "Missing docs/index.html"
    fi
    
    if [ -f "docs/.nojekyll" ]; then
        status_ok "Jekyll disabled"
    else
        status_error "Missing .nojekyll file"
    fi
else
    status_error "Missing docs directory"
fi

# Check AI workspace
echo ""
status_info "Checking AI workspace..."

if [ -d "ai-workspace" ]; then
    status_ok "AI workspace directory exists"
    
    if [ -d "ai-workspace/05-samples-demos" ]; then
        status_ok "Sample demos available"
    else
        status_warn "Missing sample demos"
    fi
    
    if [ -f "ai-workspace/README.md" ]; then
        status_ok "AI workspace documented"
    else
        status_warn "Missing AI workspace README"
    fi
else
    status_error "Missing ai-workspace directory"
fi

# Check git status
echo ""
status_info "Checking repository status..."

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    status_ok "Git repository detected"
    
    if git remote get-url origin >/dev/null 2>&1; then
        remote_url=$(git remote get-url origin)
        status_ok "Remote configured: $(basename "$remote_url" .git)"
    else
        status_error "No git remote"
    fi
    
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        status_ok "No uncommitted changes"
    else
        status_warn "Uncommitted changes detected"
    fi
else
    status_error "Not a git repository"
fi

# Summary and recommendations
echo ""
status_info "Workspace Summary:"
echo "=================="

file_counts() {
    local dir=$1
    local pattern=$2
    find "$dir" -name "$pattern" 2>/dev/null | wc -l
}

echo "📁 Structure:"
echo "   • Scripts: $(file_counts scripts "*.sh")"
echo "   • Docs: $(file_counts docs "*")" 
echo "   • AI Workspace: $(file_counts ai-workspace "*")"
echo "   • Cleanup: $(file_counts .cleanup "*")"

echo ""
echo "🚀 Quick Actions:"
echo "   • Deploy: ./deploy.sh"
echo "   • Status: ./scripts/deployment/check-pages-deployment.sh"
echo "   • Setup: ./scripts/deployment/setup-github-pages.sh"

echo ""
status_info "Repository ready for AI development! 🎉"
