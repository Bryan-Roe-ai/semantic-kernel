#!/bin/bash
# Health check script for Semantic Kernel development container

set -e

echo "🩺 Running container health check..."

# Check if essential tools are available
TOOLS=("dotnet" "python3.12" "node" "npm" "git" "curl")
FAILED=0

for tool in "${TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool is available"
    else
        echo "❌ $tool is not available"
        FAILED=1
    fi
done

# Check .NET version
if command -v dotnet &> /dev/null; then
    DOTNET_VERSION=$(dotnet --version)
    echo "📦 .NET version: $DOTNET_VERSION"
fi

# Check Python version
if command -v python3.12 &> /dev/null; then
    PYTHON_VERSION=$(python3.12 --version)
    echo "🐍 Python version: $PYTHON_VERSION"
fi

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "🟢 Node.js version: $NODE_VERSION"
fi

# Check if workspace is accessible
if [ -d "/workspaces/semantic-kernel" ]; then
    echo "📁 Workspace directory is accessible"
else
    echo "❌ Workspace directory is not accessible"
    FAILED=1
fi

# Test basic HTTP connectivity
if curl -s --max-time 5 http://httpbin.org/get > /dev/null 2>&1; then
    echo "🌐 HTTP connectivity is working"
else
    echo "⚠️  HTTP connectivity test failed (might be network-related)"
fi

if [ $FAILED -eq 0 ]; then
    echo "✅ Health check passed!"
    exit 0
else
    echo "❌ Health check failed!"
    exit 1
fi
