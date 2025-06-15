#!/bin/bash

echo "🚀 AI Workspace Deployment Status Check"
echo "========================================"
echo ""

# Check the expected GitHub Pages URL
URL="https://bryan-roe-ai.github.io/semantic-kernel/"
echo "🔍 Checking deployment at: $URL"
echo ""

# Use curl to check if the site is responding
if curl -s -o /dev/null -w "%{http_code}" "$URL" | grep -q "200"; then
    echo "✅ SUCCESS: Website is live and accessible!"
    echo "🌐 Visit: $URL"
else
    echo "⏳ PENDING: Website not yet accessible (this is normal during initial deployment)"
    echo "📝 Possible reasons:"
    echo "   - GitHub Actions workflow is still running"
    echo "   - GitHub Pages is propagating the deployment"
    echo "   - First-time setup may take longer"
    echo ""
    echo "💡 What to do:"
    echo "   1. Wait 5-10 minutes for workflow completion"
    echo "   2. Check GitHub Actions tab for workflow status"
    echo "   3. Verify GitHub Pages settings in repository"
fi

echo ""
echo "📊 Additional Information:"
echo "   - Repository: Bryan-Roe-ai/semantic-kernel"
echo "   - Branch: main"
echo "   - Source: ai-workspace/ directory"
echo "   - Workflow: .github/workflows/ai-workspace-deploy.yml"
echo ""
echo "🔗 Useful Links:"
echo "   - Actions: https://github.com/Bryan-Roe-ai/semantic-kernel/actions"
echo "   - Settings: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages"
echo "   - Repository: https://github.com/Bryan-Roe-ai/semantic-kernel"
