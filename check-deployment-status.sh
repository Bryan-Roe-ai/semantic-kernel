#!/bin/bash

# GitHub Pages Deployment Status Checker
# This script helps monitor the deployment status

echo "🚀 GitHub Pages Deployment Status"
echo "=================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check git status
echo "📊 Repository Status:"
if git status >/dev/null 2>&1; then
    echo "✅ Git repository detected"
    
    # Check for uncommitted changes
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "✅ No uncommitted changes"
    else
        echo "⚠️  Uncommitted changes detected:"
        git status --porcelain | head -10
        echo ""
        echo "💡 Run: git add . && git commit -m 'Setup GitHub Pages' && git push"
    fi
    
    # Check current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    echo "📍 Current branch: $current_branch"
    
    # Check remote
    if git remote get-url origin >/dev/null 2>&1; then
        remote_url=$(git remote get-url origin)
        echo "🔗 Remote URL: $remote_url"
        
        # Extract username/repo from URL
        if [[ $remote_url == *"github.com"* ]]; then
            repo_path=$(echo $remote_url | sed 's/.*github\.com[:/]\([^.]*\)\.git.*/\1/' | sed 's/.*github\.com[:/]\([^.]*\)$/\1/')
            echo "📂 Repository: $repo_path"
            echo "🌐 Expected Pages URL: https://${repo_path%/*}.github.io/${repo_path#*/}/"
        fi
    else
        echo "❌ No remote origin found"
    fi
else
    echo "❌ Not a git repository"
    exit 1
fi

echo ""
echo "📁 Files Status:"

# Check docs folder
if [ -d "docs" ]; then
    file_count=$(find docs -type f | wc -l)
    echo "✅ docs/ folder exists with $file_count files"
    
    # Check key files
    key_files=("index.html" "custom-llm-studio.html" ".nojekyll")
    for file in "${key_files[@]}"; do
        if [ -f "docs/$file" ]; then
            size=$(stat -c%s "docs/$file" 2>/dev/null || stat -f%z "docs/$file" 2>/dev/null || echo "unknown")
            echo "✅ docs/$file ($size bytes)"
        else
            echo "❌ docs/$file missing"
        fi
    done
else
    echo "❌ docs/ folder not found"
fi

echo ""
echo "⚙️  Workflow Status:"

# Check workflows
if [ -f ".github/workflows/pages.yml" ]; then
    echo "✅ Main GitHub Pages workflow exists"
else
    echo "❌ Main workflow missing"
fi

if [ -f ".github/workflows/deploy-ai-workspace-pages.yml" ]; then
    echo "✅ AI workspace deployment workflow exists"
else
    echo "⚠️  AI workspace workflow missing (optional)"
fi

echo ""
echo "🔧 GitHub Pages Configuration:"
echo "1. Go to: https://github.com/[username]/[repo]/settings/pages"
echo "2. Under 'Source', select 'GitHub Actions'"
echo "3. Save the settings"
echo ""
echo "📈 Monitor Deployment:"
echo "1. Check Actions tab: https://github.com/[username]/[repo]/actions"
echo "2. Look for 'Deploy to GitHub Pages' workflow"
echo "3. Wait for green checkmark ✅"
echo ""
echo "🎯 Test Your Site:"
echo "1. Wait 5-10 minutes after first deployment"
echo "2. Visit your GitHub Pages URL"
echo "3. Verify all pages load correctly"

echo ""
echo "✅ Deployment status check complete!"
