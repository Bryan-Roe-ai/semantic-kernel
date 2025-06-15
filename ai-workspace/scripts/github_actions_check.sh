#!/bin/bash

# Final GitHub Actions Deployment Readiness Check
set -e

echo "🚀 GitHub Actions Deployment Readiness Check"
echo "============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

success_count=0
total_checks=0

check_item() {
    local description="$1"
    local condition="$2"
    total_checks=$((total_checks + 1))
    
    if eval "$condition"; then
        echo -e "  ${GREEN}✅${NC} $description"
        success_count=$((success_count + 1))
    else
        echo -e "  ${RED}❌${NC} $description"
    fi
}

warning_item() {
    local description="$1"
    echo -e "  ${YELLOW}⚠️${NC} $description"
}

info_item() {
    local description="$1"
    echo -e "  ${BLUE}ℹ️${NC} $description"
}

echo ""
echo "📋 Checking GitHub Actions Configuration..."

# Check workflow file exists
check_item "GitHub Actions workflow file exists" "[ -f '../.github/workflows/ai-workspace-deploy.yml' ]"

# Check if we're in a git repository
check_item "Git repository detected" "[ -d '../.git' ]"

# Check required files
echo ""
echo "📄 Checking Required Files..."
check_item "README.md exists" "[ -f 'README.md' ]"
check_item "Dockerfile exists" "[ -f 'Dockerfile' ]"
check_item "docker-compose.yml exists" "[ -f 'docker-compose.yml' ]"
check_item "requirements-minimal.txt exists" "[ -f 'requirements-minimal.txt' ]"

# Check scripts
echo ""
echo "🔧 Checking Build Scripts..."
check_item "build_static.sh exists and executable" "[ -x 'scripts/build_static.sh' ]"
check_item "integration_test.sh exists and executable" "[ -x 'scripts/integration_test.sh' ]"
check_item "test_api_endpoints.sh exists and executable" "[ -x 'scripts/test_api_endpoints.sh' ]"

# Check web files
echo ""
echo "🌐 Checking Web Interface Files..."
check_item "index.html exists" "[ -f '05-samples-demos/index.html' ]"
check_item "custom-llm-studio.html exists" "[ -f '05-samples-demos/custom-llm-studio.html' ]"

# Check backend files
echo ""
echo "🐍 Checking Backend Files..."
check_item "simple_api_server.py exists" "[ -f '06-backend-services/simple_api_server.py' ]"
check_item "advanced_llm_trainer.py exists" "[ -f '03-models-training/advanced_llm_trainer.py' ]"

# Test build process
echo ""
echo "🔨 Testing Build Process..."
if ./scripts/build_static.sh > /dev/null 2>&1; then
    check_item "Static site builds successfully" "true"
else
    check_item "Static site builds successfully" "false"
fi

# Check build output
if [ -f "dist/index.html" ] && [ -f "dist/custom-llm-studio.html" ]; then
    check_item "Build output contains required HTML files" "true"
else
    check_item "Build output contains required HTML files" "false"
fi

# Git status check
echo ""
echo "📊 Git Repository Status..."
if git status > /dev/null 2>&1; then
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    info_item "Current branch: $current_branch"
    
    if [ "$current_branch" = "main" ]; then
        info_item "On main branch (deployment will trigger on push)"
    else
        warning_item "Not on main branch (switch to main for deployment)"
    fi
    
    # Check for uncommitted changes
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        info_item "Working directory is clean"
    else
        warning_item "Uncommitted changes detected"
    fi
else
    warning_item "Could not check git status"
fi

# GitHub remote check
echo ""
echo "🔗 GitHub Remote Configuration..."
if git remote -v 2>/dev/null | grep -q "github.com"; then
    remote_url=$(git remote get-url origin 2>/dev/null || echo "unknown")
    info_item "GitHub remote detected: $remote_url"
    
    # Extract repository info
    if [[ $remote_url =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
        username="${BASH_REMATCH[1]}"
        repo="${BASH_REMATCH[2]}"
        info_item "Repository: $username/$repo"
        info_item "Deployment URL will be: https://$username.github.io/$repo"
    fi
else
    warning_item "No GitHub remote detected"
fi

echo ""
echo "=" * 50
echo "📊 Summary"
echo "=" * 50

# Calculate success rate
if [ $total_checks -gt 0 ]; then
    success_rate=$((success_count * 100 / total_checks))
    echo "Checks passed: $success_count/$total_checks ($success_rate%)"
else
    echo "No checks performed"
fi

echo ""
if [ $success_count -eq $total_checks ]; then
    echo -e "${GREEN}🎉 All checks passed! Ready for GitHub Actions deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Ensure GitHub Pages is enabled in repository settings"
    echo "2. Commit and push to main branch:"
    echo "   git add ."
    echo "   git commit -m 'Deploy AI Workspace'"
    echo "   git push origin main"
    echo "3. Monitor deployment in GitHub Actions tab"
    echo ""
    echo "🌐 Your site will be live at: https://{username}.github.io/{repo}"
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above before deploying.${NC}"
    exit 1
fi
