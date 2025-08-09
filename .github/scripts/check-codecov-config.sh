#!/bin/bash

# Codecov Configuration Checker
# This script helps verify your Codecov setup

echo "🔍 Codecov Configuration Checker"
echo "================================="
echo

# Check if we're in a Git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a Git repository"
    exit 1
fi

# Get repository information
REPO_URL=$(git config --get remote.origin.url)
REPO_NAME=$(basename -s .git "$REPO_URL")
REPO_OWNER=$(basename $(dirname "$REPO_URL"))

echo "📁 Repository: $REPO_OWNER/$REPO_NAME"
echo

# Check for workflow file
WORKFLOW_FILE=".github/workflows/enhanced-ci-cd.yml"
if [[ -f "$WORKFLOW_FILE" ]]; then
    echo "✅ Enhanced CI/CD workflow found"

    # Check for Codecov configuration in workflow
    if grep -q "ENABLE_CODECOV" "$WORKFLOW_FILE"; then
        echo "✅ Codecov configuration found in workflow"
    else
        echo "❌ Codecov configuration not found in workflow"
    fi

    if grep -q "codecov/codecov-action" "$WORKFLOW_FILE"; then
        echo "✅ Codecov action configured"
    else
        echo "❌ Codecov action not found"
    fi
else
    echo "❌ Enhanced CI/CD workflow not found at $WORKFLOW_FILE"
fi

echo

# Check for Codecov configuration file
if [[ -f ".codecov.yml" ]]; then
    echo "✅ Codecov configuration file (.codecov.yml) found"
elif [[ -f "codecov.yml" ]]; then
    echo "✅ Codecov configuration file (codecov.yml) found"
else
    echo "ℹ️  No Codecov configuration file found (optional)"
fi

echo

# Check for coverage configuration in project files
echo "🔍 Checking for coverage configuration in project files:"

# .NET coverage
if find . -name "*.csproj" -exec grep -l "coverlet\|XPlat Code Coverage" {} \; | head -1 > /dev/null; then
    echo "✅ .NET coverage collection configured"
else
    echo "ℹ️  .NET coverage collection not explicitly configured (may use default)"
fi

# Python coverage
if [[ -f "pyproject.toml" ]] && grep -q "pytest-cov\|coverage" pyproject.toml; then
    echo "✅ Python coverage collection configured"
elif [[ -f "requirements.txt" ]] && grep -q "pytest-cov\|coverage" requirements.txt; then
    echo "✅ Python coverage collection configured"
else
    echo "ℹ️  Python coverage collection not found in common config files"
fi

# TypeScript/JavaScript coverage
if [[ -f "package.json" ]] && grep -q "jest\|nyc\|c8" package.json; then
    echo "✅ TypeScript/JavaScript coverage collection configured"
else
    echo "ℹ️  TypeScript/JavaScript coverage collection not found in package.json"
fi

echo

# Provide setup instructions
echo "🚀 Next Steps:"
echo "=============+"
echo
echo "1. Set up repository variable:"
echo "   - Go to Settings → Secrets and variables → Actions → Variables"
echo "   - Add: ENABLE_CODECOV = true"
echo
echo "2. (Optional) Add Codecov token:"
echo "   - Sign up at https://codecov.io"
echo "   - Add your repository"
echo "   - Go to Settings → Secrets and variables → Actions → Secrets"
echo "   - Add: CODECOV_TOKEN = [your-token]"
echo
echo "3. The workflow will automatically:"
echo "   - Skip Codecov uploads if ENABLE_CODECOV != 'true'"
echo "   - Continue building even if Codecov fails"
echo "   - Collect coverage from all test suites"
echo
echo "📖 For detailed instructions, see .github/CODECOV_SETUP.md"
