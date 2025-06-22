#!/bin/bash

# VS Code Task Runner for Semantic Kernel Tests
# This script integrates with the existing VS Code task definitions

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${CYAN}$1${NC}"; }
log_success() { echo -e "${GREEN}$1${NC}"; }
log_warning() { echo -e "${YELLOW}$1${NC}"; }

show_available_tasks() {
    log_info "📋 Available VS Code Tasks:"
    echo "  🐍 test (Semantic-Kernel-Python) - Run Python unit tests"
    echo "  🔗 test (Semantic-Kernel-Python Integration) - Run Python integration tests"
    echo "  🧪 test (Semantic-Kernel-Python ALL) - Run all Python tests"
    echo "  🏗️  install python packages - Setup Python environment"
    echo "  📦 install poetry - Install Poetry dependency manager"
    echo ""
    log_info "🎯 Quick Commands:"
    echo "  $0 python-unit     - Run Python unit tests"
    echo "  $0 python-int      - Run Python integration tests"
    echo "  $0 python-all      - Run all Python tests"
    echo "  $0 setup-python    - Setup Python environment"
    echo "  $0 discover        - Show test project discovery"
}

run_vscode_task() {
    local task_label="$1"
    local workspace_folder="/home/broe/semantic-kernel"

    log_info "🎯 Running VS Code task: $task_label"

    case "$task_label" in
        "test (Semantic-Kernel-Python)")
            cd "$workspace_folder/python"
            log_info "📍 Working directory: $(pwd)"
            poetry run pytest tests/unit
            ;;
        "test (Semantic-Kernel-Python Integration)")
            cd "$workspace_folder/python"
            log_info "📍 Working directory: $(pwd)"
            # Note: This task expects a filter input, we'll skip the filter for now
            poetry run pytest tests/integration
            ;;
        "test (Semantic-Kernel-Python ALL)")
            cd "$workspace_folder/python"
            log_info "📍 Working directory: $(pwd)"
            # Note: This task expects a filter input, we'll skip the filter for now
            poetry run pytest tests
            ;;
        "install python packages")
            cd "$workspace_folder/python"
            log_info "📍 Working directory: $(pwd)"
            poetry install
            ;;
        "install poetry")
            cd "$workspace_folder/python"
            log_info "📍 Working directory: $(pwd)"
            pip3 install poetry
            ;;
        *)
            log_warning "⚠️  Unknown task: $task_label"
            return 1
            ;;
    esac
}

run_quick_command() {
    local command="$1"

    case "$command" in
        "python-unit")
            run_vscode_task "test (Semantic-Kernel-Python)"
            ;;
        "python-int")
            run_vscode_task "test (Semantic-Kernel-Python Integration)"
            ;;
        "python-all")
            run_vscode_task "test (Semantic-Kernel-Python ALL)"
            ;;
        "setup-python")
            run_vscode_task "install poetry"
            run_vscode_task "install python packages"
            ;;
        "discover")
            /home/broe/semantic-kernel/simple-auto-tests.sh discover
            ;;
        *)
            log_warning "⚠️  Unknown command: $command"
            show_available_tasks
            return 1
            ;;
    esac
}

# Main execution
if [ $# -eq 0 ]; then
    show_available_tasks
    exit 0
fi

log_info "🧪 Semantic Kernel VS Code Task Runner"

run_quick_command "$1"

log_success "✨ Task execution completed!"
