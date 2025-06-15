#!/bin/bash

# GitHub Pages Deployment Verification
# Run this after pushing to verify deployment is working

echo "🚀 GitHub Pages Deployment Verification"
echo "======================================="

# Get repository information
if git remote get-url origin >/dev/null 2>&1; then
    remote_url=$(git remote get-url origin)
    repo_path=$(echo $remote_url | sed 's/.*github\.com[:/]\([^.]*\)\.git.*/\1/' | sed 's/.*github\.com[:/]\([^.]*\)$/\1/')
    username=$(echo $repo_path | cut -d'/' -f1)
    repo_name=$(echo $repo_path | cut -d'/' -f2)

    echo "📂 Repository: $repo_path"
    echo "🌐 Pages URL: https://$username.github.io/$repo_name/"
    echo ""

    # Check if changes have been pushed
    echo "📊 Checking git status..."
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "✅ No uncommitted changes"

        # Check if we're ahead of origin
        if git rev-list --count @{u}..HEAD 2>/dev/null | grep -q "^0$"; then
            echo "✅ All changes pushed to origin"
        else
            unpushed=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "unknown")
            echo "⚠️  $unpushed commit(s) not yet pushed"
            echo "💡 Run: git push origin main"
        fi
    else
        echo "⚠️  Uncommitted changes detected"
        echo "💡 Run: git add . && git commit -m 'Update' && git push"
    fi

    echo ""
    echo "🔍 Deployment Checklist:"
    echo "========================"

    # Check workflow file
    if [ -f ".github/workflows/pages.yml" ]; then
        echo "✅ GitHub Pages workflow exists"
    else
        echo "❌ GitHub Pages workflow missing"
    fi

    # Check docs folder
    if [ -d "docs" ]; then
        file_count=$(find docs -type f | wc -l)
        echo "✅ docs/ folder exists ($file_count files)"

        # Check key files
        key_files=("docs/index.html" "docs/custom-llm-studio.html" "docs/.nojekyll")
        for file in "${key_files[@]}"; do
            if [ -f "$file" ]; then
                size=$(stat -c%s "$file" 2>/dev/null || echo "0")
                echo "  ✅ $(basename "$file") ($size bytes)"
            else
                echo "  ❌ $(basename "$file") missing"
            fi
        done
    else
        echo "❌ docs/ folder missing"
    fi

    echo ""
    echo "📋 Manual Steps Required:"
    echo "========================"
    echo "1. 🌐 Open: https://github.com/$repo_path/settings/pages"
    echo "2. ⚙️  Set 'Source' to 'GitHub Actions'"
    echo "3. 💾 Click 'Save'"
    echo "4. 🚀 Check: https://github.com/$repo_path/actions"
    echo "5. ⏱️  Wait for deployment to complete (green checkmark)"
    echo "6. 🌍 Visit: https://$username.github.io/$repo_name/"
    echo ""

    echo "🎯 Quick Links:"
    echo "==============="
    echo "Repository Settings: https://github.com/$repo_path/settings/pages"
    echo "GitHub Actions: https://github.com/$repo_path/actions"
    echo "Your Site: https://$username.github.io/$repo_name/"
    echo ""

    echo "📞 Troubleshooting:"
    echo "==================="
    echo "• If deployment fails, check the Actions tab for error logs"
    echo "• Ensure GitHub Pages is enabled in repository settings"
    echo "• Wait 5-10 minutes for first deployment to complete"
    echo "• Check that your repository is public (for free GitHub accounts)"
    echo ""

    echo "✅ Verification complete! Follow the manual steps above to enable GitHub Pages."

else
    echo "❌ No git remote found"
    exit 1
fi
