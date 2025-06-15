#!/bin/bash

# GitHub Pages Validation Script
# Checks if all required files are properly configured

echo "🔍 Validating GitHub Pages Configuration..."
echo "============================================="

# Check if we're in the right directory
if [ ! -d ".github/workflows" ]; then
    echo "❌ Not in repository root (no .github/workflows found)"
    exit 1
fi

echo "✅ Found repository structure"

# Check workflow files
workflows_found=0
if [ -f ".github/workflows/pages.yml" ]; then
    echo "✅ Found GitHub Pages workflow: .github/workflows/pages.yml"
    workflows_found=$((workflows_found + 1))
fi

if [ -f ".github/workflows/deploy-ai-workspace-pages.yml" ]; then
    echo "✅ Found AI workspace deployment workflow"
    workflows_found=$((workflows_found + 1))
fi

if [ $workflows_found -eq 0 ]; then
    echo "❌ No GitHub Pages workflows found"
    exit 1
fi

# Check docs folder
if [ ! -d "docs" ]; then
    echo "❌ docs folder not found"
    exit 1
fi

echo "✅ Found docs folder"

# Check required files in docs
required_files=("index.html" "custom-llm-studio.html" ".nojekyll")
missing_files=0

for file in "${required_files[@]}"; do
    if [ -f "docs/$file" ]; then
        size=$(stat -c%s "docs/$file" 2>/dev/null || stat -f%z "docs/$file" 2>/dev/null || echo "unknown")
        echo "✅ Found docs/$file ($size bytes)"
    else
        echo "❌ Missing docs/$file"
        missing_files=$((missing_files + 1))
    fi
done

# Check optional files
optional_files=("server.js" "express-rate.js" "README.md" "last-deployment.txt")
for file in "${optional_files[@]}"; do
    if [ -f "docs/$file" ]; then
        echo "✅ Found docs/$file (optional)"
    else
        echo "ℹ️  Missing docs/$file (optional)"
    fi
done

# Check samples directory
if [ -d "docs/samples" ]; then
    sample_count=$(find docs/samples -type f | wc -l)
    echo "✅ Found docs/samples with $sample_count files"
else
    echo "ℹ️  No docs/samples directory found"
fi

# Validate HTML structure
if [ -f "docs/index.html" ]; then
    if grep -q "<!DOCTYPE html>" docs/index.html; then
        echo "✅ index.html has proper DOCTYPE"
    else
        echo "⚠️  index.html missing DOCTYPE declaration"
    fi
    
    if grep -q "<title>" docs/index.html; then
        title=$(grep -o '<title>[^<]*</title>' docs/index.html | sed 's/<[^>]*>//g')
        echo "✅ index.html has title: '$title'"
    else
        echo "⚠️  index.html missing title tag"
    fi
fi

# Check for source files in ai-workspace
if [ -d "ai-workspace/05-samples-demos" ]; then
    echo "✅ Found source files in ai-workspace/05-samples-demos"
    
    if [ -f "ai-workspace/05-samples-demos/index.html" ]; then
        source_size=$(stat -c%s "ai-workspace/05-samples-demos/index.html" 2>/dev/null || stat -f%z "ai-workspace/05-samples-demos/index.html" 2>/dev/null)
        docs_size=$(stat -c%s "docs/index.html" 2>/dev/null || stat -f%z "docs/index.html" 2>/dev/null)
        
        if [ "$source_size" = "$docs_size" ]; then
            echo "✅ Source and docs index.html files are in sync"
        else
            echo "⚠️  Source ($source_size bytes) and docs ($docs_size bytes) index.html files differ"
        fi
    fi
else
    echo "⚠️  Source directory ai-workspace/05-samples-demos not found"
fi

# Summary
echo ""
echo "📊 Validation Summary"
echo "===================="

if [ $missing_files -eq 0 ]; then
    echo "✅ All required files present"
    echo "✅ GitHub Pages is ready to deploy!"
    echo ""
    echo "🚀 Next Steps:"
    echo "1. Commit and push changes: git add . && git commit -m 'Setup GitHub Pages' && git push"
    echo "2. Go to repository Settings > Pages"
    echo "3. Set source to 'GitHub Actions'"
    echo "4. Wait for deployment (check Actions tab)"
    echo "5. Visit your site at: https://[username].github.io/semantic-kernel/"
else
    echo "❌ $missing_files required files missing"
    echo "Run ./setup-github-pages.sh to fix missing files"
    exit 1
fi
