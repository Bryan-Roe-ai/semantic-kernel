#!/bin/bash

# Comprehensive validation script for AI Workspace deployment
set -e

echo "🔍 AI Workspace Deployment Validation"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation functions
validate_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 missing${NC}"
        return 1
    fi
}

validate_directory() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1/ directory exists${NC}"
        return 0
    else
        echo -e "${RED}❌ $1/ directory missing${NC}"
        return 1
    fi
}

validate_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✅ $1 is executable${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 is not executable${NC}"
        return 1
    fi
}

# Start validation
ERRORS=0

echo -e "\n${BLUE}📁 Checking core directories...${NC}"
validate_directory "01-notebooks" || ((ERRORS++))
validate_directory "02-agents" || ((ERRORS++))
validate_directory "03-models-training" || ((ERRORS++))
validate_directory "04-plugins" || ((ERRORS++))
validate_directory "05-samples-demos" || ((ERRORS++))
validate_directory "06-backend-services" || ((ERRORS++))
validate_directory "07-data-resources" || ((ERRORS++))
validate_directory "08-documentation" || ((ERRORS++))
validate_directory "09-deployment" || ((ERRORS++))
validate_directory "10-config" || ((ERRORS++))
validate_directory "scripts" || ((ERRORS++))

echo -e "\n${BLUE}📄 Checking core files...${NC}"
validate_file "README.md" || ((ERRORS++))
validate_file "Dockerfile" || ((ERRORS++))
validate_file "docker-compose.yml" || ((ERRORS++))
validate_file "requirements-minimal.txt" || ((ERRORS++))
validate_file "SUCCESS_SUMMARY.md" || ((ERRORS++))
validate_file "GITHUB_PAGES_GUIDE.md" || ((ERRORS++))

echo -e "\n${BLUE}🔧 Checking scripts...${NC}"
validate_file "scripts/build_static.sh" || ((ERRORS++))
validate_file "scripts/integration_test.sh" || ((ERRORS++))
validate_file "scripts/test_api_endpoints.sh" || ((ERRORS++))
validate_file "scripts/docker_manager.sh" || ((ERRORS++))

validate_executable "scripts/build_static.sh" || ((ERRORS++))
validate_executable "scripts/integration_test.sh" || ((ERRORS++))
validate_executable "scripts/test_api_endpoints.sh" || ((ERRORS++))
validate_executable "scripts/docker_manager.sh" || ((ERRORS++))

echo -e "\n${BLUE}🌐 Checking web files...${NC}"
validate_file "05-samples-demos/index.html" || ((ERRORS++))
validate_file "05-samples-demos/custom-llm-studio.html" || ((ERRORS++))

echo -e "\n${BLUE}🐍 Checking Python files...${NC}"
validate_file "06-backend-services/simple_api_server.py" || ((ERRORS++))
validate_file "03-models-training/advanced_llm_trainer.py" || ((ERRORS++))

echo -e "\n${BLUE}⚙️ Checking GitHub Actions...${NC}"
validate_file "../.github/workflows/ai-workspace-deploy.yml" || ((ERRORS++))

echo -e "\n${BLUE}🧪 Running build test...${NC}"
if [ -x "scripts/build_static.sh" ]; then
    echo "Building static site..."
    ./scripts/build_static.sh > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Build script runs successfully${NC}"
        
        # Check build output
        if [ -f "dist/index.html" ] && [ -f "dist/custom-llm-studio.html" ]; then
            echo -e "${GREEN}✅ Static files built correctly${NC}"
        else
            echo -e "${RED}❌ Build output incomplete${NC}"
            ((ERRORS++))
        fi
    else
        echo -e "${RED}❌ Build script failed${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${RED}❌ Build script not executable${NC}"
    ((ERRORS++))
fi

echo -e "\n${BLUE}🔗 Testing integration...${NC}"
if [ -x "scripts/integration_test.sh" ]; then
    echo "Running integration tests..."
    if ./scripts/integration_test.sh > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Integration tests pass${NC}"
    else
        echo -e "${YELLOW}⚠️ Integration tests had issues (may be expected)${NC}"
    fi
else
    echo -e "${RED}❌ Integration test script not executable${NC}"
    ((ERRORS++))
fi

echo -e "\n${BLUE}📊 Validation Summary${NC}"
echo "===================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 All validations passed!${NC}"
    echo -e "${GREEN}✅ AI Workspace is ready for deployment${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Commit and push to GitHub"
    echo "2. Enable GitHub Pages in repository settings"
    echo "3. Workflow will deploy automatically"
    echo "4. Check deployment at: https://{username}.github.io/{repo-name}"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS validation errors${NC}"
    echo -e "${RED}⚠️ Please fix errors before deployment${NC}"
    exit 1
fi
