#!/bin/bash
# AI Workspace Launcher
# Quick setup and launch script for the organized AI workspace

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
     _    ___   __        __         _
    / \  |_ _|  \ \      / /__  _ __| | _____ _ __   __ _  ___ ___
   / _ \  | |    \ \ /\ / / _ \| '__| |/ / __| '_ \ / _` |/ __/ _ \
  / ___ \ | |     \ V  V / (_) | |  |   <\__ \ |_) | (_| | (_|  __/
 /_/   \_\___|     \_/\_/ \___/|_|  |_|\_\___/ .__/ \__,_|\___\___|
                                            |_|
EOF
echo -e "${NC}"

echo -e "${GREEN}🤖 Semantic Kernel AI Workspace${NC}"
echo -e "${YELLOW}Organized for optimal AI development workflow${NC}"
echo ""

WORKSPACE_DIR="/workspaces/semantic-kernel/ai-workspace"
ROOT_DIR="/workspaces/semantic-kernel"

# Check if workspace exists
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo -e "${RED}❌ AI workspace not found!${NC}"
    echo "Please run the organization script first."
    exit 1
fi

# Function to display menu
show_menu() {
    echo -e "${BLUE}📋 Available Actions:${NC}"
    echo "1. 📊 Show workspace status"
    echo "2. 📓 Launch Jupyter Lab"
    echo "3. 🚀 Start backend services"
    echo "4. 🔧 Setup development environment"
    echo "5. 📖 Open documentation"
    echo "6. 🧪 Run tests"
    echo "7. 📁 Open workspace in VS Code"
    echo "8. 🌐 Launch web interface"
    echo "9. ⚙️  Environment configuration"
    echo "10. 🐳 Docker management"
    echo "11. 🧹 Cleanup workspace"
    echo "0. ❌ Exit"
    echo ""
}

# Function to show workspace status
show_status() {
    echo -e "${GREEN}📊 Workspace Status${NC}"
    cd "$WORKSPACE_DIR"
    python ai_workspace_manager.py --status
    echo ""
}

# Function to launch Jupyter Lab
launch_jupyter() {
    echo -e "${GREEN}🚀 Launching Jupyter Lab...${NC}"
    cd "$WORKSPACE_DIR/01-notebooks"

    # Check if jupyter is installed
    if ! command -v jupyter &> /dev/null; then
        echo -e "${YELLOW}Installing Jupyter Lab...${NC}"
        pip install jupyterlab
    fi

    echo -e "${BLUE}Starting Jupyter Lab on port 8888...${NC}"
    jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
}

# Function to start backend services
start_backend() {
    echo -e "${GREEN}🚀 Starting Backend Services...${NC}"
    cd "$WORKSPACE_DIR/06-backend-services"

    if [ -f "start_backend.py" ]; then
        python start_backend.py
    elif [ -f "app.py" ]; then
        python app.py
    elif [ -f "backend.py" ]; then
        python backend.py
    else
        echo -e "${YELLOW}No backend entry point found. Available Python files:${NC}"
        ls *.py 2>/dev/null || echo "No Python files found"
    fi
}

# Function to setup development environment
setup_dev_env() {
    echo -e "${GREEN}🔧 Setting up development environment...${NC}"
    cd "$WORKSPACE_DIR"

    # Install requirements
    if [ -f "requirements.txt" ]; then
        echo -e "${BLUE}Installing Python dependencies...${NC}"
        pip install -r requirements.txt
    fi

    # Setup pre-commit hooks if available
    if [ -f ".pre-commit-config.yaml" ]; then
        echo -e "${BLUE}Setting up pre-commit hooks...${NC}"
        pre-commit install
    fi

    # Create .env file if it doesn't exist
    if [ ! -f ".env" ] && [ -f ".env.template" ]; then
        echo -e "${BLUE}Creating .env file from template...${NC}"
        cp .env.template .env
        echo -e "${YELLOW}Please edit .env file to add your API keys${NC}"
    fi

    echo -e "${GREEN}✅ Development environment setup complete!${NC}"
}

# Function to open documentation
open_docs() {
    echo -e "${GREEN}📖 Opening documentation...${NC}"
    cd "$WORKSPACE_DIR/08-documentation"

    if command -v code &> /dev/null; then
        code README.md
    else
        echo -e "${BLUE}Documentation files:${NC}"
        ls -la
    fi
}

# Function to run tests
run_tests() {
    echo -e "${GREEN}🧪 Running tests...${NC}"
    cd "$ROOT_DIR"

    # Try different test runners
    if [ -d "tests" ]; then
        if command -v pytest &> /dev/null; then
            pytest tests/
        elif [ -f "test_*.py" ]; then
            python -m unittest discover
        else
            echo -e "${YELLOW}No tests found or test runner not available${NC}"
        fi
    else
        echo -e "${YELLOW}No tests directory found${NC}"
    fi
}

# Function to open in VS Code
open_vscode() {
    echo -e "${GREEN}📁 Opening workspace in VS Code...${NC}"
    if command -v code &> /dev/null; then
        code "$WORKSPACE_DIR"
    else
        echo -e "${RED}VS Code not found in PATH${NC}"
    fi
}

# Function to launch web interface
launch_web() {
    echo -e "${GREEN}🌐 Launching web interface...${NC}"
    cd "$WORKSPACE_DIR/06-backend-services"

    # Try to find and run a web server
    if [ -f "server.js" ]; then
        if command -v node &> /dev/null; then
            node server.js
        else
            echo -e "${RED}Node.js not found${NC}"
        fi
    elif [ -f "app.py" ]; then
        if command -v streamlit &> /dev/null; then
            streamlit run app.py
        else
            python app.py
        fi
    else
        echo -e "${YELLOW}No web server found${NC}"
    fi
}

# Function to configure environment
configure_env() {
    echo -e "${GREEN}⚙️  Environment Configuration${NC}"
    cd "$WORKSPACE_DIR"

    echo -e "${BLUE}Current environment files:${NC}"
    ls -la .env* 2>/dev/null || echo "No environment files found"

    if [ -f ".env.template" ]; then
        echo -e "${YELLOW}Template file available: .env.template${NC}"
        echo "Copy this to .env and configure your API keys"
    fi

    echo -e "${BLUE}Key environment variables to set:${NC}"
    echo "- OPENAI_API_KEY"
    echo "- AZURE_OPENAI_API_KEY"
    echo "- AZURE_OPENAI_ENDPOINT"
    echo "- HUGGINGFACE_API_KEY"
}

# Function to manage Docker
manage_docker() {
    echo -e "${GREEN}🐳 Docker Management${NC}"
    echo "1. 🏗️  Build Docker image"
    echo "2. 🚀 Start with Docker Compose"
    echo "3. 🛑 Stop Docker services"
    echo "4. 📊 Show Docker status"
    echo "5. 📝 Show Docker logs"
    echo "6. 🧹 Clean up Docker resources"
    echo "7. 🛠️  Development mode"
    echo "8. 🚀 Production deploy"
    echo "0. ↩️  Back to main menu"
    echo ""

    read -p "Select Docker action (0-8): " docker_choice

    case $docker_choice in
        1)
            echo -e "${GREEN}🏗️  Building Docker image...${NC}"
            ./scripts/docker_manager.sh build
            ;;
        2)
            echo -e "${GREEN}🚀 Starting with Docker Compose...${NC}"
            ./scripts/docker_manager.sh compose
            ;;
        3)
            echo -e "${GREEN}🛑 Stopping Docker services...${NC}"
            ./scripts/docker_manager.sh stop
            ;;
        4)
            echo -e "${GREEN}📊 Docker Status...${NC}"
            ./scripts/docker_manager.sh status
            ;;
        5)
            echo -e "${GREEN}📝 Docker Logs...${NC}"
            read -p "Service name (or press Enter for main): " service_name
            ./scripts/docker_manager.sh logs "${service_name:-ai-workspace}"
            ;;
        6)
            echo -e "${GREEN}🧹 Cleaning up Docker resources...${NC}"
            ./scripts/docker_manager.sh cleanup
            ;;
        7)
            echo -e "${GREEN}🛠️  Starting development mode...${NC}"
            ./scripts/docker_manager.sh dev
            ;;
        8)
            echo -e "${GREEN}🚀 Production deployment...${NC}"
            ./scripts/docker_manager.sh deploy
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Invalid option${NC}"
            ;;
    esac
}

# Function to cleanup workspace
cleanup_workspace() {
    echo -e "${GREEN}🧹 Workspace Cleanup${NC}"
    echo "1. 🐍 Clean Python cache"
    echo "2. 📝 Clean logs"
    echo "3. 🗑️  Clean temporary files"
    echo "4. 🔗 Fix broken links"
    echo "5. 🏗️  Optimize structure"
    echo "6. 📦 Update dependencies"
    echo "7. 💾 Backup configuration"
    echo "8. 🔍 Run health checks"
    echo "9. 🐳 Prepare for Docker"
    echo "10. 🎯 Run all cleanup tasks"
    echo "0. ↩️  Back to main menu"
    echo ""

    read -p "Select cleanup action (0-10): " cleanup_choice

    case $cleanup_choice in
        1)
            ./scripts/cleanup_and_automate.sh --cleanup
            ;;
        2)
            find logs/ -name "*.log" -mtime +7 -delete 2>/dev/null || true
            echo "✅ Logs cleaned"
            ;;
        3)
            ./scripts/cleanup_and_automate.sh --cleanup
            ;;
        4)
            find . -type l -! -exec test -e {} \; -delete 2>/dev/null || true
            echo "✅ Broken links fixed"
            ;;
        5)
            ./scripts/cleanup_and_automate.sh --optimize
            ;;
        6)
            ./scripts/cleanup_and_automate.sh --update
            ;;
        7)
            ./scripts/cleanup_and_automate.sh --backup
            ;;
        8)
            ./scripts/cleanup_and_automate.sh --health
            ;;
        9)
            ./scripts/cleanup_and_automate.sh --docker
            ;;
        10)
            ./scripts/cleanup_and_automate.sh --all
            ;;
        0)
            return
            ;;
        *)
            echo -e "${RED}❌ Invalid option${NC}"
            ;;
    esac
}

# Main loop
while true; do
    echo ""
    show_menu
    read -p "Enter your choice (0-11): " choice

    case $choice in
        1) show_status ;;
        2) launch_jupyter ;;
        3) start_backend ;;
        4) setup_dev_env ;;
        5) open_docs ;;
        6) run_tests ;;
        7) open_vscode ;;
        8) launch_web ;;
        9) configure_env ;;
        10) manage_docker ;;
        11) cleanup_workspace ;;
        0) echo -e "${GREEN}👋 Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}❌ Invalid option. Please try again.${NC}" ;;
    esac
done
