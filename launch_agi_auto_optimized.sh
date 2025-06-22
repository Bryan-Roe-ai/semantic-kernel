#!/bin/bash

# Optimized AGI Auto File Update System Launcher
# High-performance AGI file operations with advanced optimization

set -e

echo "🚀 Starting Optimized AGI Auto File Update System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Performance settings
MAX_MEMORY_MB=${AGI_MAX_MEMORY:-512}
PARALLEL_WORKERS=${AGI_WORKERS:-5}
CACHE_SIZE=${AGI_CACHE_SIZE:-1000}

# Function to print colored output
print_status() {
    echo -e "${BLUE}[AGI-OPT]${NC} $1"
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

print_perf() {
    echo -e "${PURPLE}[PERF]${NC} $1"
}

# Performance monitoring function
monitor_performance() {
    local pid=$1
    while kill -0 $pid 2>/dev/null; do
        # Monitor memory usage
        local memory_mb=$(ps -p $pid -o rss= | awk '{print $1/1024}')
        local cpu_percent=$(ps -p $pid -o %cpu= | tr -d ' ')
        
        if (( $(echo "$memory_mb > $MAX_MEMORY_MB" | bc -l) )); then
            print_warning "Memory usage: ${memory_mb}MB (limit: ${MAX_MEMORY_MB}MB)"
        fi
        
        echo "$(date): PID=$pid MEM=${memory_mb}MB CPU=${cpu_percent}%" >> agi_performance.log
        sleep 30
    done
}

# Optimize Python environment
optimize_python_env() {
    print_perf "Optimizing Python environment..."
    
    # Set performance environment variables
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONUNBUFFERED=1
    export PYTHONOPTIMIZE=2
    export TOKENIZERS_PARALLELISM=false
    export OMP_NUM_THREADS=${PARALLEL_WORKERS}
    export MKL_NUM_THREADS=${PARALLEL_WORKERS}
    
    # Set memory limits
    ulimit -v $((MAX_MEMORY_MB * 1024)) 2>/dev/null || print_warning "Could not set memory limit"
    
    print_success "Python environment optimized"
}

# Check system requirements
check_system_requirements() {
    print_status "Checking system requirements for optimization..."
    
    # Check available memory
    local available_memory_mb=$(free -m | awk '/^Mem:/{print $7}')
    if [ "$available_memory_mb" -lt 256 ]; then
        print_warning "Low available memory: ${available_memory_mb}MB"
    else
        print_success "Available memory: ${available_memory_mb}MB"
    fi
    
    # Check CPU cores
    local cpu_cores=$(nproc)
    print_success "CPU cores available: $cpu_cores"
    
    # Adjust workers based on CPU cores
    if [ "$PARALLEL_WORKERS" -gt "$cpu_cores" ]; then
        PARALLEL_WORKERS=$cpu_cores
        print_warning "Adjusted workers to match CPU cores: $PARALLEL_WORKERS"
    fi
    
    # Check disk space
    local disk_space_gb=$(df . | awk 'NR==2 {print $4/1024/1024}')
    if (( $(echo "$disk_space_gb < 1" | bc -l) )); then
        print_warning "Low disk space: ${disk_space_gb}GB"
    else
        print_success "Available disk space: ${disk_space_gb}GB"
    fi
}

# Check if we're in the right directory
if [ ! -f "AGI_CHAT_README.md" ]; then
    print_error "Please run this script from the semantic-kernel directory"
    exit 1
fi

# System optimization
print_perf "Performing system optimization checks..."
check_system_requirements
optimize_python_env

# Check Python installation
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

# Check required packages with performance focus
print_status "Checking optimized package requirements..."
python3 -c "
import sys
required_packages = ['asyncio', 'concurrent.futures', 'multiprocessing', 'threading']
optional_packages = ['torch', 'numpy']
missing_required = []
missing_optional = []

for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        missing_required.append(pkg)

for pkg in optional_packages:
    try:
        __import__(pkg)
    except ImportError:
        missing_optional.append(pkg)

if missing_required:
    print('Missing required packages:', ', '.join(missing_required))
    sys.exit(1)

if missing_optional:
    print('Missing optional packages (performance may be reduced):', ', '.join(missing_optional))

print('All core packages available for optimized operation')
"

if [ $? -ne 0 ]; then
    print_warning "Installing missing packages for optimization..."
    pip3 install asyncio concurrent.futures
fi

# Check AGI system status with optimization
print_status "Checking optimized AGI system integration..."
if [ -f "agi_chat_integration.py" ]; then
    print_success "AGI Chat Integration found"
else
    print_warning "AGI Chat Integration not found - performance may be limited"
fi

# Setup optimized directories
print_status "Setting up optimized backup and cache directories..."
mkdir -p .agi_backups
mkdir -p .agi_cache
mkdir -p .agi_performance_logs
print_success "Optimized directories ready"

# Check configuration with performance settings
print_status "Checking optimized AGI configuration..."
if [ -f ".agi_file_config.json" ]; then
    # Validate performance settings exist
    if jq -e '.performance_settings' .agi_file_config.json > /dev/null 2>&1; then
        print_success "Optimized AGI configuration found"
        
        # Display performance settings
        local max_tasks=$(jq -r '.performance_settings.max_concurrent_tasks // 5' .agi_file_config.json)
        local cache_ttl=$(jq -r '.performance_settings.cache_ttl_seconds // 300' .agi_file_config.json)
        local parallel_enabled=$(jq -r '.performance_settings.enable_parallel_processing // true' .agi_file_config.json)
        
        print_perf "Max concurrent tasks: $max_tasks"
        print_perf "Cache TTL: ${cache_ttl}s"
        print_perf "Parallel processing: $parallel_enabled"
    else
        print_warning "Configuration missing performance settings - will use defaults"
    fi
else
    print_warning "AGI configuration not found - will be created with optimized defaults"
fi

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down Optimized AGI Auto File Update System..."
    kill $(jobs -p) 2>/dev/null || true
    
    # Kill any remaining AGI processes
    pkill -f "agi_file_update_system" 2>/dev/null || true
    
    # Save performance summary
    if [ -f "agi_performance.log" ]; then
        local total_lines=$(wc -l < agi_performance.log)
        print_perf "Performance log saved: $total_lines entries"
    fi
    
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if optimized AGI backend is available
print_status "Checking optimized AGI backend..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_status "Starting optimized AGI backend server..."
    if [ -d "agi-backend-server" ]; then
        cd agi-backend-server
        PYTHONOPTIMIZE=2 python3 main.py &
        BACKEND_PID=$!
        cd ..
        print_success "Optimized AGI backend started (PID: $BACKEND_PID)"
        
        # Start performance monitoring for backend
        monitor_performance $BACKEND_PID &
    else
        print_warning "AGI backend server not found - using optimized standalone mode"
    fi
else
    print_success "AGI backend already running"
fi

# Wait for backend to be ready with timeout
print_status "Waiting for optimized AGI backend to be ready..."
for i in {1..15}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Optimized AGI backend is ready!"
        break
    fi
    sleep 1
done

# Determine which AGI system to start
AGI_SCRIPT="agi_file_update_system_optimized.py"
if [ ! -f "$AGI_SCRIPT" ]; then
    print_warning "Optimized script not found, falling back to standard version"
    AGI_SCRIPT="agi_file_update_system.py"
fi

# Start the optimized auto file update system
print_status "Starting Optimized AGI Auto File Update System..."
print_perf "Using script: $AGI_SCRIPT"
print_perf "Performance mode: Enabled"
print_perf "Workers: $PARALLEL_WORKERS"
print_perf "Memory limit: ${MAX_MEMORY_MB}MB"
print_perf "Cache size: $CACHE_SIZE"

# Export performance settings
export AGI_MAX_CONCURRENT_TASKS=$PARALLEL_WORKERS
export AGI_CACHE_SIZE=$CACHE_SIZE
export AGI_MEMORY_LIMIT_MB=$MAX_MEMORY_MB

# Start based on mode
if [ "$1" = "--monitor" ]; then
    print_status "Starting in optimized monitoring mode..."
    
    # Start AGI system
    python3 "$AGI_SCRIPT" &
    AGI_FILE_PID=$!
    
    # Start performance monitoring
    monitor_performance $AGI_FILE_PID &
    MONITOR_PID=$!
    
    # Create monitoring loop
    while true; do
        sleep 300  # Check every 5 minutes
        
        # Check if processes are still running
        if ! ps -p $AGI_FILE_PID > /dev/null; then
            print_warning "Optimized AGI Auto File Update System stopped, restarting..."
            python3 "$AGI_SCRIPT" &
            AGI_FILE_PID=$!
            
            # Restart monitoring
            kill $MONITOR_PID 2>/dev/null || true
            monitor_performance $AGI_FILE_PID &
            MONITOR_PID=$!
        fi
        
        # Log status with performance metrics
        local memory_mb=$(ps -p $AGI_FILE_PID -o rss= 2>/dev/null | awk '{print $1/1024}' || echo "0")
        echo "$(date): Optimized AGI running (PID: $AGI_FILE_PID, MEM: ${memory_mb}MB)" >> agi_auto_status.log
    done

elif [ "$1" = "--daemon" ]; then
    print_status "Starting in optimized daemon mode..."
    nohup python3 "$AGI_SCRIPT" > agi_auto_optimized_daemon.log 2>&1 &
    AGI_PID=$!
    print_success "Optimized AGI Auto File Update System running in daemon mode (PID: $AGI_PID)"
    
    # Start background performance monitoring
    monitor_performance $AGI_PID > /dev/null 2>&1 &
    
    echo $AGI_PID > .agi_optimized_daemon.pid
    exit 0

elif [ "$1" = "--performance" ]; then
    print_status "Starting in performance analysis mode..."
    
    # Enable detailed performance logging
    export AGI_PERFORMANCE_MODE=1
    export PYTHONPROFILE=1
    
    python3 -m cProfile -o agi_performance_profile.prof "$AGI_SCRIPT" &
    AGI_FILE_PID=$!
    
    print_success "Performance profiling enabled - results will be saved to agi_performance_profile.prof"
    monitor_performance $AGI_FILE_PID &
    
    wait $AGI_FILE_PID

else
    # Interactive optimized mode
    print_status "Starting in interactive optimized mode..."
    
    python3 "$AGI_SCRIPT" &
    AGI_FILE_PID=$!
    
    # Start performance monitoring
    monitor_performance $AGI_FILE_PID &
    MONITOR_PID=$!
    
    # Wait a moment for startup
    sleep 3
    
    # Check if the system started successfully
    if ps -p $AGI_FILE_PID > /dev/null; then
        print_success "Optimized AGI Auto File Update System started (PID: $AGI_FILE_PID)"
    else
        print_error "Failed to start Optimized AGI Auto File Update System"
        exit 1
    fi
fi

# Interactive mode information
if [ "$1" != "--daemon" ]; then
    print_status ""
    print_success "🎯 Optimized AGI Auto File Update System is now running!"
    print_status ""
    print_perf "✨ Optimization Features Active:"
    print_perf "   • High-performance parallel processing"
    print_perf "   • Advanced file caching system"
    print_perf "   • Compressed backup storage"
    print_perf "   • Batch operation optimization"
    print_perf "   • Memory-efficient processing"
    print_perf "   • Real-time performance monitoring"
    print_status ""
    print_status "🔧 System Status:"
    print_status "   • AGI Backend: http://localhost:8000"
    print_status "   • Optimized File System: Active (PID: $AGI_FILE_PID)"
    print_status "   • Configuration: .agi_file_config.json"
    print_status "   • Optimized Backups: .agi_backups/"
    print_status "   • Performance Logs: agi_file_updates.log"
    print_status "   • System Monitor: agi_performance.log"
    print_status ""
    print_status "💡 Performance Usage Options:"
    print_status "   • ./launch_agi_auto_optimized.sh --monitor     (monitoring mode)"
    print_status "   • ./launch_agi_auto_optimized.sh --daemon      (daemon mode)"
    print_status "   • ./launch_agi_auto_optimized.sh --performance (profiling mode)"
    print_status "   • python3 agi_file_update_system_optimized.py  (direct run)"
    print_status ""
    print_status "📊 Performance Monitoring:"
    print_status "   • tail -f agi_performance.log     (system metrics)"
    print_status "   • tail -f agi_file_updates.log    (operation logs)"
    print_status "   • ./check_agi_auto_status.sh      (quick status)"
    print_status ""
    print_status "📖 For VS Code integration, see AGI_AUTO_SETUP_COMPLETE.md"
    print_status ""
    print_status "Press Ctrl+C to stop all services"
    
    # Wait for background processes
    wait
fi
