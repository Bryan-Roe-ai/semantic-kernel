#!/bin/bash

# Semantic Kernel Test Automation Setup & Usage Guide
# This script shows all available testing options

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GRAY='\033[0;37m'
NC='\033[0m'

log_info() { echo -e "${CYAN}$1${NC}"; }
log_success() { echo -e "${GREEN}$1${NC}"; }
log_warning() { echo -e "${YELLOW}$1${NC}"; }
log_error() { echo -e "${RED}$1${NC}"; }
log_header() { echo -e "${MAGENTA}$1${NC}"; }

show_banner() {
    log_header "🧪 ====================================="
    log_header "   SEMANTIC KERNEL TEST AUTOMATION   "
    log_header "===================================== 🧪"
    echo ""
}

show_test_stats() {
    log_info "📊 Test Project Statistics:"

    # Count .NET projects
    local dotnet_count=$(find 01-core-implementations/dotnet -name "*Tests.csproj" -type f 2>/dev/null | wc -l)
    echo "  🏗️  .NET Test Projects: $dotnet_count"

    # Count Python test directories
    local python_count=0
    for dir in "python/tests/unit" "python/tests/integration" "python/tests/end-to-end"; do
        if [ -d "$dir" ]; then
            ((python_count++))
        fi
    done
    echo "  🐍 Python Test Suites: $python_count"

    # Check for TypeScript
    local ts_count=$(find typescript -name "package.json" -type f 2>/dev/null | wc -l)
    echo "  📜 TypeScript Projects: $ts_count"

    echo ""
}

show_quick_start() {
    log_header "🚀 QUICK START GUIDE"
    echo ""

    log_info "1️⃣  Discover all tests:"
    echo "   ./simple-auto-tests.sh discover"
    echo ""

    log_info "2️⃣  Run Python unit tests:"
    echo "   ./vscode-task-runner.sh python-unit"
    echo ""

    log_info "3️⃣  Run all .NET tests:"
    echo "   ./simple-auto-tests.sh dotnet"
    echo ""

    log_info "4️⃣  Run everything:"
    echo "   ./simple-auto-tests.sh all"
    echo ""
}

show_available_scripts() {
    log_header "📋 AVAILABLE TEST SCRIPTS"
    echo ""

    log_info "🔧 simple-auto-tests.sh - Basic test runner"
    echo "   Commands:"
    echo "   • discover          - Find all test projects"
    echo "   • dotnet           - Run all .NET tests"
    echo "   • python           - Run all Python tests"
    echo "   • python-unit      - Run Python unit tests only"
    echo "   • python-int       - Run Python integration tests only"
    echo "   • all              - Run everything"
    echo "   Options: --verbose --coverage"
    echo ""

    log_info "🎯 vscode-task-runner.sh - VS Code task integration"
    echo "   Commands:"
    echo "   • python-unit      - Python unit tests"
    echo "   • python-int       - Python integration tests"
    echo "   • python-all       - All Python tests"
    echo "   • setup-python     - Setup Python environment"
    echo "   • discover         - Show test discovery"
    echo ""

    log_info "⚡ run-auto-tests.sh - Advanced runner (if fixed)"
    echo "   Commands:"
    echo "   • discover         - Advanced discovery"
    echo "   • run-all          - Run all with parallelism"
    echo "   • run <pattern>    - Run matching tests"
    echo "   • watch [pattern]  - Watch mode"
    echo ""

    log_info "🔨 run-auto-tests.ps1 - PowerShell version"
    echo "   Same commands as bash version"
    echo ""
}

show_examples() {
    log_header "💡 USAGE EXAMPLES"
    echo ""

    log_info "📈 Running with coverage:"
    echo "   ./simple-auto-tests.sh dotnet --coverage"
    echo "   ./simple-auto-tests.sh python --coverage"
    echo ""

    log_info "🔍 Verbose output:"
    echo "   ./simple-auto-tests.sh python-unit --verbose"
    echo ""

    log_info "🔧 Setup Python environment:"
    echo "   ./vscode-task-runner.sh setup-python"
    echo ""

    log_info "🎯 Using VS Code tasks directly:"
    echo "   cd python && poetry run pytest tests/unit"
    echo "   dotnet test --configuration Release"
    echo ""
}

show_github_actions() {
    log_header "🔄 GITHUB ACTIONS CI/CD"
    echo ""

    log_info "📁 Workflow file created:"
    echo "   .github/workflows/auto-tests.yml"
    echo ""

    log_info "🎯 Features:"
    echo "   • Multi-OS testing (Ubuntu, Windows, macOS)"
    echo "   • Matrix builds for .NET and Python"
    echo "   • Code coverage collection"
    echo "   • Integration tests with services"
    echo "   • Security scanning"
    echo "   • Performance benchmarks"
    echo "   • Automated reporting"
    echo ""

    log_info "🚀 Triggers:"
    echo "   • Push to main/develop branches"
    echo "   • Pull requests"
    echo "   • Daily scheduled runs"
    echo "   • Manual dispatch"
    echo ""
}

show_configuration() {
    log_header "⚙️ CONFIGURATION"
    echo ""

    log_info "📄 Configuration file:"
    echo "   auto-test-config.json - Comprehensive test settings"
    echo ""

    log_info "🔧 Environment variables:"
    echo "   SK_TEST_MODE=true        - Enable test mode"
    echo "   SK_COVERAGE_THRESHOLD=80 - Coverage threshold"
    echo "   SK_PARALLEL_TESTS=true   - Parallel execution"
    echo ""
}

show_troubleshooting() {
    log_header "🔧 TROUBLESHOOTING"
    echo ""

    log_info "❓ Common issues:"
    echo ""

    log_warning "Poetry not found:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    echo "   # or"
    echo "   pip3 install poetry"
    echo ""

    log_warning ".NET tests failing:"
    echo "   dotnet restore"
    echo "   dotnet build --configuration Release"
    echo ""

    log_warning "Permission denied:"
    echo "   chmod +x *.sh"
    echo ""

    log_warning "Test discovery issues:"
    echo "   Check project patterns in auto-test-config.json"
    echo ""
}

check_prerequisites() {
    log_header "✅ PREREQUISITES CHECK"
    echo ""

    local missing=()

    # Check .NET
    if command -v dotnet &> /dev/null; then
        local dotnet_version=$(dotnet --version 2>/dev/null || echo "unknown")
        log_success "✅ .NET SDK: $dotnet_version"
    else
        log_error "❌ .NET SDK not found"
        missing+=(".NET SDK")
    fi

    # Check Python
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version 2>/dev/null || echo "unknown")
        log_success "✅ Python: $python_version"
    else
        log_error "❌ Python3 not found"
        missing+=("Python 3")
    fi

    # Check Poetry
    if command -v poetry &> /dev/null; then
        local poetry_version=$(poetry --version 2>/dev/null || echo "unknown")
        log_success "✅ Poetry: $poetry_version"
    else
        log_warning "⚠️  Poetry not found (recommended for Python tests)"
        missing+=("Poetry")
    fi

    # Check Node.js
    if command -v node &> /dev/null; then
        local node_version=$(node --version 2>/dev/null || echo "unknown")
        log_success "✅ Node.js: $node_version"
    else
        log_warning "⚠️  Node.js not found (needed for TypeScript tests)"
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        echo ""
        log_warning "Missing tools: ${missing[*]}"
        log_info "Install missing tools to run all tests"
    fi

    echo ""
}

run_demo() {
    log_header "🎬 DEMO - Quick Test Run"
    echo ""

    log_info "Running test discovery..."
    if ./simple-auto-tests.sh discover; then
        log_success "✅ Discovery completed"
    else
        log_error "❌ Discovery failed"
    fi

    echo ""
    log_info "Demo completed! Use the commands above to run actual tests."
}

# Main menu
show_command_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  stats        - Show test project statistics"
    echo "  quick        - Show quick start guide"
    echo "  scripts      - Show available scripts"
    echo "  examples     - Show usage examples"
    echo "  github       - Show GitHub Actions info"
    echo "  config       - Show configuration options"
    echo "  troubleshoot - Show troubleshooting guide"
    echo "  check        - Check prerequisites"
    echo "  demo         - Run a quick demo"
    echo "  all          - Show everything"
    echo ""
}

# Check if we're in the right directory
if [ ! -f "LICENSE" ] || [ ! -d "01-core-implementations" ]; then
    log_error "❌ Not in Semantic Kernel workspace root"
    exit 1
fi

show_banner

if [ $# -eq 0 ]; then
    show_command_usage
    exit 0
fi

case "$1" in
    "stats")
        show_test_stats
        ;;
    "quick")
        show_quick_start
        ;;
    "scripts")
        show_available_scripts
        ;;
    "examples")
        show_examples
        ;;
    "github")
        show_github_actions
        ;;
    "config")
        show_configuration
        ;;
    "troubleshoot")
        show_troubleshooting
        ;;
    "check")
        check_prerequisites
        ;;
    "demo")
        run_demo
        ;;
    "all")
        show_test_stats
        show_quick_start
        show_available_scripts
        show_examples
        show_github_actions
        show_configuration
        check_prerequisites
        ;;
    *)
        log_error "❌ Unknown command: $1"
        show_command_usage
        exit 1
        ;;
esac
