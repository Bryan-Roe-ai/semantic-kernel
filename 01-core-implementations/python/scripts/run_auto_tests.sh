#!/bin/bash

# Auto Test Script for Semantic Kernel Python
# This script provides a simple interface to run automated tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default values
TEST_TYPE="all"
COVERAGE=true
PARALLEL=true
VERBOSE=false

# Help function
show_help() {
    echo "Auto Test Runner for Semantic Kernel Python"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE        Test type: unit, integration, samples, all (default: all)"
    echo "  -f, --fast            Run fast tests (no coverage, no parallel)"
    echo "  -c, --no-coverage     Disable coverage reporting"
    echo "  -s, --sequential      Disable parallel execution"
    echo "  -v, --verbose         Enable verbose output"
    echo "  -w, --watch           Watch for file changes and run tests"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run all tests with coverage"
    echo "  $0 -t unit            # Run only unit tests"
    echo "  $0 -f                 # Run fast tests"
    echo "  $0 -w                 # Watch mode"
    echo "  $0 -t integration -v  # Run integration tests with verbose output"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -f|--fast)
            TEST_TYPE="fast"
            COVERAGE=false
            PARALLEL=false
            shift
            ;;
        -c|--no-coverage)
            COVERAGE=false
            shift
            ;;
        -s|--sequential)
            PARALLEL=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -w|--watch)
            TEST_TYPE="watch"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -d "semantic_kernel" ]]; then
    print_error "Please run this script from the python directory of the Semantic Kernel project"
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    print_warning "uv not found, falling back to python/pip"
    PYTHON_CMD="python"
    PYTEST_CMD="python -m pytest"
else
    PYTHON_CMD="uv run python"
    PYTEST_CMD="uv run pytest"
fi

print_status "Starting Semantic Kernel Python tests..."
print_status "Test type: $TEST_TYPE"
print_status "Coverage: $COVERAGE"
print_status "Parallel: $PARALLEL"
print_status "Verbose: $VERBOSE"

# Create reports directory
mkdir -p test_reports

# Set up environment
export PYTHONPATH="${PYTHONPATH}:."

# Function to run tests with appropriate options
run_pytest() {
    local test_path="$1"
    local extra_args=("${@:2}")

    local args=("$test_path" "-v" "--tb=short")

    # Add coverage if enabled
    if [[ "$COVERAGE" == "true" ]]; then
        args+=(
            "--cov=semantic_kernel"
            "--cov-report=term-missing"
            "--cov-report=xml:test_reports/coverage.xml"
            "--cov-report=html:test_reports/htmlcov"
        )
    fi

    # Add parallel execution if enabled
    if [[ "$PARALLEL" == "true" ]]; then
        args+=("-n" "auto")
    fi

    # Add verbose output if enabled
    if [[ "$VERBOSE" == "true" ]]; then
        args+=("--verbose")
    else
        args+=("-q")
    fi

    # Add timeout
    args+=("--timeout=300")

    # Add JUnit XML output
    args+=("--junit-xml=test_reports/junit.xml")

    # Add extra arguments
    args+=("${extra_args[@]}")

    print_status "Running: $PYTEST_CMD ${args[*]}"
    $PYTEST_CMD "${args[@]}"
}

# Main test execution
case "$TEST_TYPE" in
    "unit")
        print_status "Running unit tests..."
        run_pytest "tests/unit"
        ;;
    "integration")
        print_status "Running integration tests..."
        run_pytest "tests/integration" "--timeout=600"
        ;;
    "samples")
        print_status "Running sample tests..."
        run_pytest "tests/samples"
        ;;
    "fast")
        print_status "Running fast unit tests..."
        $PYTEST_CMD tests/unit -v --tb=short -x -q -k "not slow" --maxfail=5
        ;;
    "watch")
        print_status "Starting test watcher..."
        if [[ -f "scripts/test_watcher.py" ]]; then
            $PYTHON_CMD scripts/test_watcher.py
        else
            print_error "Test watcher script not found"
            exit 1
        fi
        ;;
    "all")
        print_status "Running all test suites..."

        # Run unit tests
        print_status "1/3 Running unit tests..."
        run_pytest "tests/unit"

        # Run integration tests (if they exist)
        if [[ -d "tests/integration" ]]; then
            print_status "2/3 Running integration tests..."
            run_pytest "tests/integration" "--timeout=600"
        fi

        # Run sample tests (if they exist)
        if [[ -d "tests/samples" ]]; then
            print_status "3/3 Running sample tests..."
            run_pytest "tests/samples"
        fi

        # Run quality checks
        print_status "Running quality checks..."

        # Linting
        if command -v ruff &> /dev/null; then
            print_status "Running linting..."
            uv run ruff check semantic_kernel tests scripts || true
        fi

        # Type checking
        if command -v mypy &> /dev/null; then
            print_status "Running type checking..."
            uv run mypy semantic_kernel --strict --show-error-codes || true
        fi

        ;;
    *)
        print_error "Invalid test type: $TEST_TYPE"
        show_help
        exit 1
        ;;
esac

# Check if tests passed
if [[ $? -eq 0 ]]; then
    print_success "All tests completed successfully!"

    # Show coverage summary if coverage was enabled
    if [[ "$COVERAGE" == "true" ]] && [[ -f "test_reports/coverage.xml" ]]; then
        print_status "Coverage report generated at test_reports/htmlcov/index.html"
    fi

    # Show test reports location
    print_status "Test reports available in test_reports/"

else
    print_error "Some tests failed!"
    exit 1
fi
