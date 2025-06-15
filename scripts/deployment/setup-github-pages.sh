#!/bin/bash

# GitHub Pages Setup Script
# This script ensures your docs folder is properly configured for GitHub Pages

set -e

echo "🚀 Setting up GitHub Pages for Semantic Kernel..."
echo "=================================================="

# Create docs directory if it doesn't exist
mkdir -p docs

# Copy AI workspace content to docs
echo "📁 Copying AI workspace content to docs folder..."

# Copy main HTML files
if [ -f "ai-workspace/05-samples-demos/index.html" ]; then
    cp "ai-workspace/05-samples-demos/index.html" docs/
    echo "✅ Copied index.html ($(stat -c%s "docs/index.html") bytes)"
else
    echo "❌ ai-workspace/05-samples-demos/index.html not found"
    exit 1
fi

if [ -f "ai-workspace/05-samples-demos/custom-llm-studio.html" ]; then
    cp "ai-workspace/05-samples-demos/custom-llm-studio.html" docs/
    echo "✅ Copied custom-llm-studio.html ($(stat -c%s "docs/custom-llm-studio.html") bytes)"
else
    echo "❌ ai-workspace/05-samples-demos/custom-llm-studio.html not found"
    exit 1
fi

# Copy JavaScript files
if [ -f "ai-workspace/05-samples-demos/server.js" ]; then
    cp "ai-workspace/05-samples-demos/server.js" docs/
    echo "✅ Copied server.js"
fi

if [ -f "ai-workspace/05-samples-demos/express-rate.js" ]; then
    cp "ai-workspace/05-samples-demos/express-rate.js" docs/
    echo "✅ Copied express-rate.js"
fi

# Copy samples directory (resolve symlinks if they exist)
if [ -d "ai-workspace/05-samples-demos/samples" ]; then
    rm -rf docs/samples 2>/dev/null || true
    # Try to copy with symlink resolution first, fall back to regular copy
    cp -rL "ai-workspace/05-samples-demos/samples" docs/ 2>/dev/null || cp -r "ai-workspace/05-samples-demos/samples" docs/
    echo "✅ Copied samples directory"
fi

# Create .nojekyll file to disable Jekyll processing
touch docs/.nojekyll
echo "✅ Created .nojekyll file"

# Create a simple README for the docs folder
cat > docs/README.md << 'EOF'
# AI Workspace Documentation

This directory contains the GitHub Pages site for the AI Workspace.

## Files

- `index.html` - Main AI workspace homepage
- `custom-llm-studio.html` - Custom LLM Studio interface
- `server.js` - Server-side functionality
- `express-rate.js` - Rate limiting features
- `samples/` - Code samples and demonstrations
- `.nojekyll` - Disables Jekyll processing for GitHub Pages

## Deployment

This site is automatically deployed via GitHub Actions when changes are made to:
- `docs/` folder
- `ai-workspace/` folder

The deployment workflow copies content from `ai-workspace/05-samples-demos/` to the `docs/` folder.

## Access

The site will be available at: `https://[username].github.io/semantic-kernel/`
EOF

echo "✅ Created docs/README.md"

# Create deployment timestamp
echo "Last updated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")" > docs/last-deployment.txt
echo "✅ Created deployment timestamp"

# Validate the setup
echo ""
echo "🔍 Validating GitHub Pages setup..."

# Check required files
required_files=("index.html" "custom-llm-studio.html" ".nojekyll")
all_good=true

for file in "${required_files[@]}"; do
    if [ -f "docs/$file" ]; then
        echo "✅ Found: docs/$file"
    else
        echo "❌ Missing: docs/$file"
        all_good=false
    fi
done

# Check HTML validity
if grep -q "<!DOCTYPE html>" docs/index.html; then
    echo "✅ index.html has valid DOCTYPE"
else
    echo "❌ index.html missing DOCTYPE"
    all_good=false
fi

# Check file sizes
if [ -f "docs/index.html" ]; then
    index_size=$(stat -c%s "docs/index.html")
    if [ $index_size -gt 1000 ]; then
        echo "✅ index.html size: $index_size bytes (good)"
    else
        echo "⚠️  index.html size: $index_size bytes (might be too small)"
    fi
fi

echo ""
if [ "$all_good" = true ]; then
    echo "🎉 GitHub Pages setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Commit and push these changes to the main branch"
    echo "2. Go to your repository Settings > Pages"
    echo "3. Set source to 'GitHub Actions'"
    echo "4. The site will be available at: https://[your-username].github.io/semantic-kernel/"
    echo ""
    echo "The GitHub Actions workflow will automatically deploy updates when you:"
    echo "- Push changes to the main branch"
    echo "- Modify files in docs/ or ai-workspace/ folders"
else
    echo "❌ Setup completed with some issues. Please review the errors above."
    exit 1
fi
