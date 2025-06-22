#!/bin/bash

# Simple Auto Test Runner using existing VS Code tasks
# This script leverages the workspace's existing task definitions

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info() { echo -e "${CYAN}$1${NC}"; }
log_success() { echo -e "${GREEN}$1${NC}"; }
log_warning() { echo -e "${YELLOW}$1${NC}"; }
log_error() { echo -e "${RED}$1${NC}"; }

# Check if we're in the correct workspace
if [ ! -f "LICENSE" ] || [ ! -d "01-core-implementations" ]; then
    log_error "❌ Not in Semantic Kernel workspace root"
    exit 1
fi

show_usage() {
    cat << EOF
🧪 Semantic Kernel Simple Auto Test Runner

Usage: $0 <command> [options]

Commands:
    discover    Discover all test projects
    dotnet      Run .NET tests
    python      Run Python tests
    python-unit Run Python unit tests only
    python-int  Run Python integration tests only
    all         Run all tests
    help        Show this help

Options:
    --verbose   Enable verbose output
    --parallel  Enable parallel execution (default)
    --coverage  Collect code coverage

Examples:
    $0 discover
    $0 dotnet --coverage
    $0 python-unit --verbose
    $0 all
EOF
}

discover_tests() {
    log_info "🔍 Discovering test projects in Semantic Kernel workspace..."
    
    # Count .NET test projects
    dotnet_count=$(find 01-core-implementations/dotnet -name "*Tests.csproj" -type f 2>/dev/null | wc -l)
    
    # Check Python tests
    python_dirs=()
    for dir in "python/tests/unit" "python/tests/integration" "python/tests/end-to-end"; do
        if [ -d "$dir" ]; then
            python_dirs+=("$dir")
        fi
    done
    
    log_success "📊 Test Discovery Results:"
    echo "  🏗️  .NET Projects: $dotnet_count"
    echo "  🐍 Python Test Dirs: ${#python_dirs[@]}"
    
    if [ $dotnet_count -gt 0 ]; then
        log_info "📦 Sample .NET Test Projects:"
        find 01-core-implementations/dotnet -name "*Tests.csproj" -type f | head -5 | while read project; do
            name=$(basename "$project" .csproj)
            echo "  • $name"
        done
    fi
    
    if [ ${#python_dirs[@]} -gt 0 ]; then
        log_info "🐍 Python Test Directories:"
        for dir in "${python_dirs[@]}"; do
            echo "  • $dir"
        done
    fi
}

run_dotnet_tests() {
    local verbose=$1
    local coverage=$2
    
    log_info "🏗️ Running .NET tests..."
    
    # Find all .NET test projects
    local test_projects
    test_projects=$(find 01-core-implementations/dotnet -name "*Tests.csproj" -type f)
    local project_count
    project_count=$(echo "$test_projects" | wc -l)
    
    if [ -z "$test_projects" ] || [ $project_count -eq 0 ]; then
        log_warning "⚠️ No .NET test projects found"
        return 0
    fi
    
    log_info "📊 Found $project_count .NET test projects"
    
    local passed=0
    local failed=0
    local start_time=$(date +%s)
    
    echo "$test_projects" | while read -r project; do
        if [ -z "$project" ]; then continue; fi
        
        local project_name=$(basename "$project" .csproj)
        log_info "▶️ Running: $project_name"
        
        # Build test arguments
        local args=("test" "$project" "--configuration" "Release" "--logger" "console;verbosity=normal")
        
        if [ "$coverage" = true ]; then
            args+=("--collect:XPlat Code Coverage")
        fi
        
        # Run the test
        local project_start=$(date +%s)
        if dotnet "${args[@]}" > /tmp/dotnet_test_$$.log 2>&1; then
            local project_end=$(date +%s)
            local duration=$((project_end - project_start))
            log_success "✅ $project_name PASSED (${duration}s)"
            ((passed++))
        else
            local project_end=$(date +%s)
            local duration=$((project_end - project_start))
            log_error "❌ $project_name FAILED (${duration}s)"
            if [ "$verbose" = true ]; then
                cat /tmp/dotnet_test_$$.log
            fi
            ((failed++))
        fi
        
        rm -f /tmp/dotnet_test_$$.log
    done
    
    local end_time=$(date +%s)
    local total_duration=$((end_time - start_time))
    
    log_info "📊 .NET Summary: $passed passed, $failed failed (${total_duration}s total)"
}

run_python_tests() {
    local test_type=$1
    local verbose=$2
    local coverage=$3
    
    if [ ! -d "python" ]; then
        log_warning "⚠️ Python directory not found"
        return 0
    fi
    
    log_info "🐍 Running Python tests ($test_type)..."
    
    cd python
    
    # Check if poetry is available
    if ! command -v poetry &> /dev/null; then
        log_error "❌ Poetry not found. Please install poetry first."
        cd ..
        return 1
    fi
    
    # Build test arguments
    local args=("run" "pytest" "-v")
    
    case "$test_type" in
        "unit")
            args+=("tests/unit")
            ;;
        "integration")
            args+=("tests/integration")
            ;;
        "end-to-end")
            args+=("tests/end-to-end")
            ;;
        "all")
            args+=("tests")
            ;;
    esac
    
    if [ "$coverage" = true ]; then
        args+=("--cov=semantic_kernel" "--cov-report=xml" "--cov-report=html")
    fi
    
    local start_time=$(date +%s)
    
    if poetry "${args[@]}"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_success "✅ Python tests ($test_type) PASSED (${duration}s)"
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_error "❌ Python tests ($test_type) FAILED (${duration}s)"
    fi
    
    cd ..
}

# Parse arguments
COMMAND=""
VERBOSE=false
COVERAGE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        discover|dotnet|python|python-unit|python-int|all|help)
            COMMAND="$1"
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        *)
            log_error "❌ Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

if [ -z "$COMMAND" ]; then
    log_error "❌ No command specified"
    show_usage
    exit 1
fi

# Main execution
log_info "🧪 Semantic Kernel Auto Test Runner"

case "$COMMAND" in
    "discover")
        discover_tests
        ;;
    "dotnet")
        run_dotnet_tests "$VERBOSE" "$COVERAGE"
        ;;
    "python")
        run_python_tests "all" "$VERBOSE" "$COVERAGE"
        ;;
    "python-unit")
        run_python_tests "unit" "$VERBOSE" "$COVERAGE"
        ;;
    "python-int")
        run_python_tests "integration" "$VERBOSE" "$COVERAGE"
        ;;
    "all")
        log_info "🚀 Running all tests..."
        run_dotnet_tests "$VERBOSE" "$COVERAGE"
        run_python_tests "all" "$VERBOSE" "$COVERAGE"
        ;;
    "help")
        show_usage
        ;;
esac

log_success "✨ Test execution completed!"
