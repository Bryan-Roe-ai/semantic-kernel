#!/bin/bash

# Simple GitHub Pages Deploy Command
# One-command deployment for GitHub Pages

set -e

echo "🚀 Deploying to GitHub Pages"
echo "============================"

# Check if we're in the right directory
if [ ! -f "WORKSPACE_INDEX.md" ]; then
    echo "❌ Please run from the repository root"
    exit 1
fi

# Run the comprehensive deployment setup
if [ -f "scripts/deployment/setup-github-pages.sh" ]; then
    echo "📦 Running GitHub Pages setup..."
    chmod +x scripts/deployment/setup-github-pages.sh
    ./scripts/deployment/setup-github-pages.sh
else
    echo "❌ Deployment script not found"
    exit 1
fi

# Commit and push changes
echo ""
echo "📤 Committing and pushing changes..."

git add .
git commit -m "Deploy AI workspace to GitHub Pages" || echo "Nothing to commit"
git push origin main

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "🌐 Your site will be available at:"
echo "   https://Bryan-Roe-ai.github.io/semantic-kernel/"
echo ""
echo "⚙️  To complete setup:"
echo "   1. Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages"
echo "   2. Set Source to 'GitHub Actions'"
echo "   3. Save settings"
echo ""
echo "🔍 Monitor deployment:"
echo "   https://github.com/Bryan-Roe-ai/semantic-kernel/actions"
