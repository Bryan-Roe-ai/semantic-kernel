#!/bin/bash

# Final GitHub Pages Deployment Script
# This script sets up, commits, and deploys GitHub Pages

set -e

echo "🚀 Final GitHub Pages Deployment for Semantic Kernel"
echo "===================================================="

# Step 1: Setup GitHub Pages files
echo "📁 Step 1: Setting up GitHub Pages files..."
./setup-github-pages.sh

echo ""
echo "🔧 Step 2: Configuring deployment..."

# Ensure .nojekyll has content
echo "# Disable Jekyll processing for GitHub Pages" > docs/.nojekyll

# Create a proper CNAME file if needed (commented out for now)
# echo "your-custom-domain.com" > docs/CNAME

# Step 3: Git operations
echo ""
echo "📝 Step 3: Committing changes..."

# Add all changes
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    # Commit changes
    git commit -m "🚀 Deploy AI Workspace to GitHub Pages

- Set up GitHub Pages deployment workflow
- Copy AI workspace content to docs/ folder
- Disable conflicting Jekyll workflows
- Configure .nojekyll to disable Jekyll processing
- Ready for GitHub Pages deployment via GitHub Actions

Files updated:
- .github/workflows/pages.yml (main deployment workflow)
- docs/ folder (all static files)
- AI workspace content synced
- Deployment scripts and validation tools"

    echo "✅ Changes committed successfully"
fi

# Step 4: Push to origin
echo ""
echo "📤 Step 4: Pushing to GitHub..."

current_branch=$(git branch --show-current)
echo "Current branch: $current_branch"

if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
    git push origin $current_branch
    echo "✅ Pushed to $current_branch branch"
else
    echo "⚠️  Current branch is '$current_branch', not 'main' or 'master'"
    echo "💡 GitHub Pages typically deploys from 'main' branch"
    echo "📝 Consider switching: git checkout main && git merge $current_branch"
fi

echo ""
echo "🔍 Step 5: Deployment status check..."
./check-pages-deployment.sh

echo ""
echo "🎉 Deployment Process Complete!"
echo "==============================="

# Get repository info for final URLs
if git remote get-url origin >/dev/null 2>&1; then
    remote_url=$(git remote get-url origin)
    repo_path=$(echo $remote_url | sed 's/.*github\.com[:/]\([^.]*\)\.git.*/\1/' | sed 's/.*github\.com[:/]\([^.]*\)$/\1/')
    username=$(echo $repo_path | cut -d'/' -f1)
    repo_name=$(echo $repo_path | cut -d'/' -f2)

    echo ""
    echo "🌐 Your GitHub Pages site will be available at:"
    echo "   https://$username.github.io/$repo_name/"
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to: https://github.com/$repo_path/settings/pages"
    echo "2. Set 'Source' to 'GitHub Actions'"
    echo "3. Wait 1-5 minutes for first deployment"
    echo "4. Visit your site!"
    echo ""
    echo "🔗 Monitor deployment at:"
    echo "   https://github.com/$repo_path/actions"
    echo ""
    echo "📱 Quick test (after deployment):"
    echo "   curl -I https://$username.github.io/$repo_name/"
fi

echo ""
echo "✨ GitHub Pages setup complete! ✨"
