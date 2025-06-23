#!/bin/bash

# Semantic Kernel Automated Test Runner
# This script provides easy access to run automated tests across the Semantic Kernel workspace.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Default values
VERBOSE=false
PARALLEL=true
COVERAGE=false
FILTER=""
TIMEOUT=10
PATTERN=""

# Helper functions
log_info() {
    echo -e "${CYAN}$1${NC}"
}

log_success() {
    echo -e "${GREEN}$1${NC}"
}

log_warning() {
    echo -e "${YELLOW}$1${NC}"
}

log_error() {
    echo -e "${RED}$1${NC}"
}

log_debug() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${GRAY}$1${NC}"
    fi
}

# Function to show usage
show_usage() {
    cat << EOF
🧪 Semantic Kernel Automated Test Runner

Usage: $0 <command> [options]

Commands:
    discover        Discover all test projects
    run-all         Run all tests
    run <pattern>   Run tests matching pattern
    watch [pattern] Run tests in watch mode

Options:
    -v, --verbose   Enable verbose logging
    -p, --parallel  Enable parallel execution (default: true)
    -c, --coverage  Collect code coverage
    -f, --filter    Test filter pattern
    -t, --timeout   Timeout in minutes per project (default: 10)
    -h, --help      Show this help message

Examples:
    $0 discover
    $0 run-all --verbose
    $0 run "Unit" --coverage
    $0 watch --pattern "OpenAI"
EOF
}

# Function to check prerequisites
check_prerequisites() {
    local missing_tools=()

    if ! command -v dotnet &> /dev/null; then
        missing_tools+=("dotnet")
    fi

    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi

    if ! command -v poetry &> /dev/null && [ -d "python" ]; then
        missing_tools+=("poetry")
    fi

    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "❌ Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
}

# Function to find workspace root
find_workspace_root() {
    local current_dir
    current_dir=$(pwd)

    while [ "$current_dir" != "/" ]; do
        if [ -f "$current_dir/LICENSE" ] && [ -d "$current_dir/dotnet" ] && [ -d "$current_dir/python" ]; then
            echo "$current_dir"
            return 0
        fi
        current_dir=$(dirname "$current_dir")
    done

    echo "$(pwd)"
}

# Function to run .NET tests
run_dotnet_tests() {
    local project_pattern="${1:-*}"
    local workspace_root="$2"

    log_info "🔍 Discovering .NET test projects..."

    local dotnet_root="$workspace_root/01-core-implementations/dotnet"
    if [ ! -d "$dotnet_root" ]; then
        log_warning "⚠️ .NET directory not found, skipping .NET tests"
        return 0
    fi

    local test_projects
    test_projects=$(find "$dotnet_root" -name "*Tests.csproj" -type f)

    if [ "$project_pattern" != "*" ]; then
        test_projects=$(echo "$test_projects" | grep -i "$project_pattern" || true)
    fi

    local project_count
    project_count=$(echo "$test_projects" | wc -l)
    if [ -z "$test_projects" ]; then
        project_count=0
    fi

    log_success "📊 Found $project_count .NET test projects"

    local total_passed=0
    local total_failed=0
    local start_time
    start_time=$(date +%s)

    while IFS= read -r project; do
        if [ -z "$project" ]; then
            continue
        fi

        local project_name
        project_name=$(basename "$project" .csproj)
        log_info "▶️ Running: $project_name"

        local args=(
            "test"
            "$project"
            "--configuration" "Release"
            "--logger" "console;verbosity=normal"
        )

        if [ "$COVERAGE" = true ]; then
            args+=("--collect:XPlat Code Coverage")
        fi

        if [ -n "$FILTER" ]; then
            args+=("--filter" "$FILTER")
        fi

        if [ "$PARALLEL" = true ]; then
            args+=("--parallel")
        fi

        local project_start
        project_start=$(date +%s)

        if dotnet "${args[@]}" > /tmp/test_output.log 2>&1; then
            local project_end
            project_end=$(date +%s)
            local duration=$((project_end - project_start))
            log_success "✅ $project_name PASSED ($(printf '%02d:%02d' $((duration/60)) $((duration%60))))"
            ((total_passed++))
        else
            local project_end
            project_end=$(date +%s)
            local duration=$((project_end - project_start))
            log_error "❌ $project_name FAILED ($(printf '%02d:%02d' $((duration/60)) $((duration%60))))"
            if [ "$VERBOSE" = true ]; then
                log_debug "Error output:"
                cat /tmp/test_output.log
            fi
            ((total_failed++))
        fi

        rm -f /tmp/test_output.log

    done <<< "$test_projects"

    local end_time
    end_time=$(date +%s)
    local total_duration=$((end_time - start_time))

    log_info "📊 .NET Tests Summary: $total_passed passed, $total_failed failed ($(printf '%02d:%02d' $((total_duration/60)) $((total_duration%60))))"
}

# Function to run Python tests
run_python_tests() {
    local test_type="${1:-all}"
    local workspace_root="$2"

    local python_path="$workspace_root/python"

    if [ ! -d "$python_path" ]; then
        log_warning "⚠️ Python directory not found, skipping Python tests"
        return 0
    fi

    log_info "🐍 Running Python tests..."

    cd "$python_path"

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
        *)
            args+=("tests")
            ;;
    esac

    if [ "$COVERAGE" = true ]; then
        args+=("--cov=semantic_kernel" "--cov-report=xml")
    fi

    if [ -n "$FILTER" ]; then
        args+=("-k" "$FILTER")
    fi

    if [ "$PARALLEL" = true ]; then
        args+=("-n" "auto")
    fi

    local start_time
    start_time=$(date +%s)

    if poetry "${args[@]}"; then
        local end_time
        end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_success "✅ Python tests PASSED ($(printf '%02d:%02d' $((duration/60)) $((duration%60))))"
    else
        local end_time
        end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_error "❌ Python tests FAILED ($(printf '%02d:%02d' $((duration/60)) $((duration%60))))"
    fi

    cd - > /dev/null
}

# Function to discover test projects
discover_projects() {
    local workspace_root="$1"

    log_info "🔍 Discovering test projects..."

    # .NET Projects
    local dotnet_root="$workspace_root/01-core-implementations/dotnet"
    if [ -d "$dotnet_root" ]; then
        local dotnet_projects
        dotnet_projects=$(find "$dotnet_root" -name "*Tests.csproj" -type f)
        local dotnet_count
        dotnet_count=$(echo "$dotnet_projects" | wc -l)
        if [ -z "$dotnet_projects" ]; then
            dotnet_count=0
        fi

        log_success "📦 .NET Test Projects ($dotnet_count):"
        while IFS= read -r project; do
            if [ -z "$project" ]; then
                continue
            fi
            local project_name
            project_name=$(basename "$project" .csproj)
            local relative_path
            relative_path=${project#$workspace_root/}
            echo "  • $project_name"
            echo "    $relative_path"
        done <<< "$dotnet_projects"
    fi

    # Python Projects
    local python_path="$workspace_root/python"
    if [ -d "$python_path" ]; then
        local python_test_dirs=()
        for dir in "tests/unit" "tests/integration" "tests/end-to-end"; do
            if [ -d "$python_path/$dir" ]; then
                python_test_dirs+=("$dir")
            fi
        done

        log_success "🐍 Python Test Projects (${#python_test_dirs[@]}):"
        for dir in "${python_test_dirs[@]}"; do
            local test_name
            test_name=$(basename "$dir")
            echo "  • Python.$test_name"
            echo "    python/$dir"
        done
    fi

    # TypeScript Projects
    local ts_root="$workspace_root/typescript"
    if [ -d "$ts_root" ]; then
        local ts_projects
        ts_projects=$(find "$ts_root" -name "package.json" -type f 2>/dev/null || true)
        local ts_test_projects=()

        while IFS= read -r package_file; do
            if [ -z "$package_file" ]; then
                continue
            fi
            local project_dir
            project_dir=$(dirname "$package_file")
            if [ -d "$project_dir/tests" ] || [ -d "$project_dir/test" ] || [ -n "$(find "$project_dir" -name "*.test.*" 2>/dev/null || true)" ]; then
                ts_test_projects+=("$package_file")
            fi
        done <<< "$ts_projects"

        log_success "📜 TypeScript Test Projects (${#ts_test_projects[@]}):"
        for project in "${ts_test_projects[@]}"; do
            local project_name
            project_name=$(basename "$(dirname "$project")")
            local relative_path
            relative_path=${project#$workspace_root/}
            echo "  • TypeScript.$project_name"
            echo "    $relative_path"
        done
    fi
}

# Function to run tests with pattern
run_tests() {
    local pattern="$1"
    local workspace_root="$2"

    local start_time
    start_time=$(date +%s)

    if [ -n "$pattern" ]; then
        log_info "🎯 Running tests matching pattern: $pattern"

        # Run matching .NET tests
        run_dotnet_tests "$pattern" "$workspace_root"

        # Run Python tests if pattern matches
        if [[ "$pattern" =~ python|unit|integration|end-to-end ]]; then
            local test_type="all"
            if [[ "$pattern" =~ unit ]]; then
                test_type="unit"
            elif [[ "$pattern" =~ integration ]]; then
                test_type="integration"
            elif [[ "$pattern" =~ end-to-end ]]; then
                test_type="end-to-end"
            fi
            run_python_tests "$test_type" "$workspace_root"
        fi
    else
        log_info "🚀 Running all tests..."

        # Run all .NET tests
        run_dotnet_tests "*" "$workspace_root"

        # Run all Python tests
        run_python_tests "all" "$workspace_root"
    fi

    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    echo -e "${MAGENTA}⏱️ Total execution time: $(printf '%02d:%02d' $((duration/60)) $((duration%60)))${NC}"
}

# Function to run in watch mode
run_watch_mode() {
    local pattern="$1"
    local workspace_root="$2"

    log_info "👀 Starting watch mode..."
    if [ -n "$pattern" ]; then
        log_warning "📍 Pattern: $pattern"
    fi
    log_debug "Press Ctrl+C to stop watching"

    # Simple watch implementation using inotify if available
    if command -v inotifywait &> /dev/null; then
        while true; do
            inotifywait -r -e modify,create,delete --timeout 30 "$workspace_root" > /dev/null 2>&1 || true
            log_info "📝 File changes detected, running tests..."
            run_tests "$pattern" "$workspace_root"
            sleep 2
        done
    else
        log_warning "⚠️ inotifywait not found, falling back to polling"
        local last_run=0
        while true; do
            local current_time
            current_time=$(date +%s)
            if [ $((current_time - last_run)) -gt 30 ]; then
                log_info "📝 Running periodic test check..."
                run_tests "$pattern" "$workspace_root"
                last_run=$current_time
            fi
            sleep 5
        done
    fi
}

# Parse command line arguments
COMMAND=""
while [[ $# -gt 0 ]]; do
    case $1 in
        discover|run-all|run|watch)
            COMMAND="$1"
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        --no-parallel)
            PARALLEL=false
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -f|--filter)
            FILTER="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --pattern)
            PATTERN="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            if [ -z "$COMMAND" ]; then
                log_error "❌ Unknown command: $1"
                show_usage
                exit 1
            elif [ "$COMMAND" = "run" ] && [ -z "$PATTERN" ]; then
                PATTERN="$1"
                shift
            elif [ "$COMMAND" = "watch" ] && [ -z "$PATTERN" ]; then
                PATTERN="$1"
                shift
            else
                log_error "❌ Unknown option: $1"
                show_usage
                exit 1
            fi
            ;;
    esac
done

# Validate command
if [ -z "$COMMAND" ]; then
    log_error "❌ No command specified"
    show_usage
    exit 1
fi

# Main execution
main() {
    log_info "🧪 Semantic Kernel Auto Test Runner"

    local workspace_root
    workspace_root=$(find_workspace_root)
    log_debug "Working Directory: $workspace_root"

    # Check if we're in the right directory
    if [ ! -f "$workspace_root/LICENSE" ]; then
        log_error "❌ Not in Semantic Kernel workspace root. Please run from the correct directory."
        exit 1
    fi

    # Check prerequisites
    check_prerequisites

    # Execute command
    case "$COMMAND" in
        "discover")
            discover_projects "$workspace_root"
            ;;
        "run-all")
            run_tests "" "$workspace_root"
            ;;
        "run")
            if [ -z "$PATTERN" ]; then
                log_error "❌ Pattern parameter is required for 'run' command"
                exit 1
            fi
            run_tests "$PATTERN" "$workspace_root"
            ;;
        "watch")
            run_watch_mode "$PATTERN" "$workspace_root"
            ;;
    esac

    log_success "✨ Auto test execution completed!"
}

# Run main function
main "$@"
