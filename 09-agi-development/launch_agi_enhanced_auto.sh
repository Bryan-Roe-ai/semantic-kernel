#!/bin/bash

# Enhanced AGI Auto File Update System Launcher
# Optimized for high-performance operation with advanced monitoring

set -e

echo "🚀 Starting Enhanced AGI Auto File Update System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Enhanced output functions
print_status() {
    echo -e "${BLUE}[ENHANCED-AGI]${NC} $1"
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

print_performance() {
    echo -e "${PURPLE}[PERFORMANCE]${NC} $1"
}

# Performance optimization settings
optimize_environment() {
    print_performance "Applying performance optimizations..."

    # Python optimizations
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONUNBUFFERED=1
    export TOKENIZERS_PARALLELISM=false
    export PYTHONHASHSEED=0

    # Memory optimizations
    export MALLOC_ARENA_MAX=2
    export MALLOC_MMAP_THRESHOLD_=131072

    print_success "Environment optimized for performance"
}

# Check system requirements
check_performance_requirements() {
    print_status "Checking performance requirements..."

    # Check Python version
    python3 -c "
import sys
if sys.version_info < (3.8):
    print('❌ Python 3.8+ required for optimal performance')
    sys.exit(1)
else:
    print('✅ Python version: {}.{}.{}'.format(*sys.version_info[:3]))
"

    # Check and install performance packages
    python3 -c "
import sys
import subprocess

required_packages = ['psutil']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f'✅ {package} available')
    except ImportError:
        missing_packages.append(package)
        print(f'⚠️  {package} missing')

if missing_packages:
    print(f'📦 Installing missing packages: {missing_packages}')
    for package in missing_packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                         check=True, capture_output=True)
            print(f'✅ {package} installed')
        except subprocess.CalledProcessError:
            print(f'❌ Failed to install {package}')
"
}

# Parse command line arguments
DAEMON_MODE=false
MONITOR_MODE=false
PERFORMANCE_PROFILE="balanced"

while [[ $# -gt 0 ]]; do
    case $1 in
        --daemon)
            DAEMON_MODE=true
            shift
            ;;
        --monitor)
            MONITOR_MODE=true
            shift
            ;;
        --performance-profile)
            PERFORMANCE_PROFILE="$2"
            shift 2
            ;;
        --help)
            echo "Enhanced AGI Auto File Update System Launcher"
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --daemon              Run in daemon mode"
            echo "  --monitor             Run in continuous monitoring mode"
            echo "  --performance-profile Profile: fast|balanced|conservative"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Apply performance profile settings
case $PERFORMANCE_PROFILE in
    "fast")
        print_performance "Using FAST performance profile"
        export AGI_MAX_WORKERS=10
        export AGI_BATCH_SIZE=20
        export AGI_CACHE_SIZE=2000
        ;;
    "balanced")
        print_performance "Using BALANCED performance profile"
        export AGI_MAX_WORKERS=5
        export AGI_BATCH_SIZE=10
        export AGI_CACHE_SIZE=1000
        ;;
    "conservative")
        print_performance "Using CONSERVATIVE performance profile"
        export AGI_MAX_WORKERS=2
        export AGI_BATCH_SIZE=5
        export AGI_CACHE_SIZE=500
        ;;
esac

# Cleanup function
cleanup() {
    print_status "Cleaning up enhanced AGI system..."
    pkill -f "agi_enhanced_file_update_system" 2>/dev/null || true
    print_success "Cleanup completed"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Run system checks
check_performance_requirements
optimize_environment

# Check if enhanced system file exists
if [ ! -f "agi_enhanced_file_update_system.py" ]; then
    print_error "Enhanced AGI system file not found!"
    exit 1
fi

# Launch the enhanced system
print_status "Launching Enhanced AGI Auto File Update System..."

if [ "$DAEMON_MODE" = true ]; then
    print_status "Starting in daemon mode..."
    nohup python3 agi_enhanced_file_update_system.py --daemon > agi_enhanced_daemon.log 2>&1 &
    ENHANCED_PID=$!
    echo $ENHANCED_PID > .agi_enhanced.pid
    print_success "Enhanced AGI system running in daemon mode (PID: $ENHANCED_PID)"

elif [ "$MONITOR_MODE" = true ]; then
    print_status "Starting in continuous monitoring mode..."
    while true; do
        python3 agi_enhanced_file_update_system.py --monitor
        sleep 300  # 5 minutes between cycles
    done

else
    # Single run mode
    print_status "Running single enhanced cycle..."
    python3 agi_enhanced_file_update_system.py
fi

print_success "🎯 Enhanced AGI Auto File Update System is operational!"
print_status "✨ Enhanced Features: Batch processing, caching, parallel execution"
print_status "🔧 Profile: $PERFORMANCE_PROFILE | Workers: ${AGI_MAX_WORKERS:-5} | Batch: ${AGI_BATCH_SIZE:-10}"
print_success "Enhanced AGI system ready for autonomous operation! 🚀"
