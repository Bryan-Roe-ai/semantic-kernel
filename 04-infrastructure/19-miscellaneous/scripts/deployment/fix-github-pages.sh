#!/bin/bash

# GitHub Pages Deployment Fixer
# This script fixes common deployment issues and ensures GitHub Pages works

set -e

echo "🔧 GitHub Pages Deployment Fixer"
echo "================================"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Ensure we're in the right directory
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run from the repository root."
    exit 1
fi

echo "✅ Git repository detected"

# 1. Ensure docs folder is properly set up
echo ""
echo "📁 Setting up docs folder..."

# Sync content from ai-workspace
if [ -d "ai-workspace/05-samples-demos" ]; then
    echo "🔄 Syncing content from ai-workspace..."

    # Copy main files
    cp "ai-workspace/05-samples-demos/index.html" docs/ 2>/dev/null || echo "⚠️  Could not copy index.html"
    cp "ai-workspace/05-samples-demos/custom-llm-studio.html" docs/ 2>/dev/null || echo "⚠️  Could not copy custom-llm-studio.html"
    cp "ai-workspace/05-samples-demos/server.js" docs/ 2>/dev/null || echo "⚠️  Could not copy server.js"
    cp "ai-workspace/05-samples-demos/express-rate.js" docs/ 2>/dev/null || echo "⚠️  Could not copy express-rate.js"

    # Copy samples with symlink resolution
    if [ -d "ai-workspace/05-samples-demos/samples" ]; then
        rm -rf docs/samples 2>/dev/null || true
        cp -rL "ai-workspace/05-samples-demos/samples" docs/ 2>/dev/null || cp -r "ai-workspace/05-samples-demos/samples" docs/
        echo "✅ Synced samples directory"
    fi

    echo "✅ Content sync completed"
else
    echo "⚠️  ai-workspace/05-samples-demos not found"
fi

# Ensure critical files exist
touch docs/.nojekyll
echo "✅ Created .nojekyll file"

# Create deployment timestamp
echo "Last deployment: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" > docs/last-deployment.txt
echo "✅ Updated deployment timestamp"

# 2. Validate workflow files
echo ""
echo "⚙️  Validating GitHub Actions workflows..."

if [ -f ".github/workflows/pages.yml" ]; then
    echo "✅ Main deployment workflow exists"

    # Check for syntax issues
    if grep -q "actions/configure-pages@v5" .github/workflows/pages.yml; then
        echo "✅ Using latest Pages action version"
    else
        echo "⚠️  Consider updating to actions/configure-pages@v5"
    fi
else
    echo "❌ Main deployment workflow missing"
    exit 1
fi

# Disable conflicting workflows
conflicting_workflows=(
    ".github/workflows/deploy-ai-workspace-pages.yml"
    ".github/workflows/sync-to-github-pages.yml"
    ".github/workflows/ai-workspace-deploy.yml"
)

for workflow in "${conflicting_workflows[@]}"; do
    if [ -f "$workflow" ]; then
        mv "$workflow" "$workflow.disabled" 2>/dev/null || true
        echo "🚫 Disabled conflicting workflow: $(basename "$workflow")"
    fi
done

# 3. Validate content
echo ""
echo "🔍 Validating content..."

required_files=("docs/index.html" "docs/custom-llm-studio.html" "docs/.nojekyll")
all_good=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file" 2>/dev/null || echo "0")
        echo "✅ $file ($size bytes)"

        # Validate HTML files
        if [[ "$file" == *.html ]]; then
            if grep -q "<!DOCTYPE html>" "$file"; then
                echo "  ✅ Valid HTML DOCTYPE"
            else
                echo "  ⚠️  Missing DOCTYPE declaration"
            fi
        fi
    else
        echo "❌ Missing: $file"
        all_good=false
    fi
done

# 4. Check git status
echo ""
echo "📊 Checking git status..."

if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "✅ No uncommitted changes"
else
    echo "⚠️  Uncommitted changes detected:"
    git status --porcelain | head -5
    echo ""
    echo "💡 Ready to commit and push!"
fi

# 5. Repository information
echo ""
echo "📂 Repository Information:"

if git remote get-url origin >/dev/null 2>&1; then
    remote_url=$(git remote get-url origin)
    echo "🔗 Remote: $remote_url"

    if [[ $remote_url == *"github.com"* ]]; then
        repo_path=$(echo $remote_url | sed 's/.*github\.com[:/]\([^.]*\)\.git.*/\1/' | sed 's/.*github\.com[:/]\([^.]*\)$/\1/')
        username=$(echo $repo_path | cut -d'/' -f1)
        repo_name=$(echo $repo_path | cut -d'/' -f2)

        echo "👤 Username: $username"
        echo "📁 Repository: $repo_name"
        echo "🌐 Pages URL: https://$username.github.io/$repo_name/"
        echo "⚙️  Settings URL: https://github.com/$repo_path/settings/pages"
        echo "🚀 Actions URL: https://github.com/$repo_path/actions"
    fi
fi

# Final recommendations
echo ""
echo "🎯 Next Steps:"
echo "=============="

if [ "$all_good" = true ]; then
    echo "1. ✅ All files are properly configured"
else
    echo "1. ❌ Fix the missing files above"
fi

echo "2. 📤 Commit and push changes:"
echo "   git add ."
echo "   git commit -m 'Fix GitHub Pages deployment'"
echo "   git push origin main"
echo ""
echo "3. ⚙️  Enable GitHub Pages:"
echo "   - Go to repository Settings > Pages"
echo "   - Set Source to 'GitHub Actions'"
echo "   - Save settings"
echo ""
echo "4. 🚀 Monitor deployment:"
echo "   - Check Actions tab for workflow runs"
echo "   - Wait for green checkmark"
echo "   - Visit your Pages URL"
echo ""

if [ "$all_good" = true ]; then
    echo "🎉 GitHub Pages deployment is ready!"
else
    echo "❌ Please fix the issues above before deploying."
    exit 1
fi
