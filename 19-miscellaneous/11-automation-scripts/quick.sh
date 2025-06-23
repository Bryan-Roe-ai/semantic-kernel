#!/bin/bash

# AI Workspace - Quick Commands
# Simple interface for common workspace tasks

echo "🤖 AI Workspace - Quick Commands"
echo "================================"

echo ""
echo "🚀 Deployment Commands:"
echo "  ./deploy.sh                      - Deploy to GitHub Pages"
echo "  scripts/deployment/setup-github-pages.sh  - Full setup"
echo ""
echo "📊 Status & Monitoring:"
echo "  ./status.sh                      - Workspace status check"
echo "  scripts/deployment/check-pages-deployment.sh  - Deployment status"
echo ""
echo "🧹 Maintenance:"
echo "  ./cleanup-workspace.sh           - Clean and organize workspace"
echo ""
echo "📚 Documentation:"
echo "  WORKSPACE_INDEX.md               - Main workspace guide"
echo "  WORKSPACE_CLEANUP_COMPLETE.md    - Cleanup summary"
echo "  docs/guides/                     - Setup and deployment guides"
echo ""
echo "🌐 GitHub Pages URL:"
echo "  https://Bryan-Roe-ai.github.io/semantic-kernel/"
echo ""
echo "⚙️  Repository Settings:"
echo "  https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages"
echo ""
echo "📈 Actions Monitoring:"
echo "  https://github.com/Bryan-Roe-ai/semantic-kernel/actions"
echo ""

# Check if any command is requested
if [ "$1" != "" ]; then
    case "$1" in
        "deploy"|"d")
            echo "🚀 Running deployment..."
            ./deploy.sh
            ;;
        "status"|"s")
            echo "📊 Checking status..."
            ./status.sh
            ;;
        "cleanup"|"c")
            echo "🧹 Running cleanup..."
            ./cleanup-workspace.sh
            ;;
        "help"|"h"|"--help")
            echo "Usage: ./quick.sh [command]"
            echo ""
            echo "Commands:"
            echo "  deploy, d      - Deploy to GitHub Pages"
            echo "  status, s      - Check workspace status"
            echo "  cleanup, c     - Clean workspace"
            echo "  help, h        - Show this help"
            ;;
        *)
            echo "❌ Unknown command: $1"
            echo "Run './quick.sh help' for available commands"
            ;;
    esac
fi
