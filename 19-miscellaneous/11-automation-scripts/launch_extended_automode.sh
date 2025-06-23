#!/bin/bash

# Extended Operation AutoMode Launcher
# Optimized for months-long continuous operation with advanced monitoring and self-maintenance

set -e

echo "🚀 Starting Extended Operation AutoMode for Ultra-Long-Term Stability..."

# Enhanced colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
NC='\033[0m' # No Color

# Extended operation output functions
print_extended_status() {
    echo -e "${BOLD}${BLUE}[EXTENDED-MODE]${NC} $1"
}

print_extended_success() {
    echo -e "${BOLD}${GREEN}[EXTENDED-SUCCESS]${NC} $1"
}

print_extended_warning() {
    echo -e "${BOLD}${YELLOW}[EXTENDED-WARNING]${NC} $1"
}

print_extended_error() {
    echo -e "${BOLD}${RED}[EXTENDED-ERROR]${NC} $1"
}

print_extended_info() {
    echo -e "${BOLD}${CYAN}[EXTENDED-INFO]${NC} $1"
}

print_extended_analytics() {
    echo -e "${BOLD}${PURPLE}[EXTENDED-ANALYTICS]${NC} $1"
}

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENDED_LOG_DIR="$SCRIPT_DIR/logs/extended"
EXTENDED_STATE_DIR="$SCRIPT_DIR/.extended_automode"
EXTENDED_CONFIG="$SCRIPT_DIR/src/auto_mode_extended_config.json"
EXTENDED_SCRIPT="$SCRIPT_DIR/src/auto_mode_extended_operation.py"

# Create necessary directories
mkdir -p "$EXTENDED_LOG_DIR"
mkdir -p "$EXTENDED_STATE_DIR"
mkdir -p "$EXTENDED_STATE_DIR/analytics_reports"
mkdir -p "$EXTENDED_STATE_DIR/checkpoints"

# Function to check system requirements
check_extended_requirements() {
    print_extended_status "Checking extended operation requirements..."

    # Check Python version
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 8 ]; then
        print_extended_error "Python 3.8+ required for extended operation. Found: $PYTHON_VERSION"
        exit 1
    fi

    print_extended_success "Python version: $PYTHON_VERSION ✓"

    # Check required Python packages
    print_extended_status "Checking required packages..."

    REQUIRED_PACKAGES=(
        "psutil"
        "numpy"
        "scikit-learn"
        "schedule"
        "requests"
        "asyncio"
    )

    MISSING_PACKAGES=()

    for package in "${REQUIRED_PACKAGES[@]}"; do
        if ! python3 -c "import $package" 2>/dev/null; then
            MISSING_PACKAGES+=("$package")
        fi
    done

    if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
        print_extended_warning "Installing missing packages: ${MISSING_PACKAGES[*]}"
        pip3 install "${MISSING_PACKAGES[@]}" || {
            print_extended_error "Failed to install required packages"
            exit 1
        }
    fi

    print_extended_success "All required packages are available ✓"
}

# Function to optimize system for extended operation
optimize_extended_environment() {
    print_extended_status "Optimizing environment for extended operation..."

    # Set process limits for long-term operation
    ulimit -n 65536 2>/dev/null || print_extended_warning "Could not increase file descriptor limit"
    ulimit -u 32768 2>/dev/null || print_extended_warning "Could not increase process limit"

    # Set Python optimizations for extended operation
    export PYTHONOPTIMIZE=1
    export PYTHONUNBUFFERED=1
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONUTF8=1

    # Memory management optimizations
    export MALLOC_TRIM_THRESHOLD_=131072
    export MALLOC_MMAP_THRESHOLD_=131072

    print_extended_success "Environment optimized for extended operation ✓"
}

# Function to check system health before starting
pre_flight_health_check() {
    print_extended_status "Performing pre-flight health check..."

    # Check available memory
    AVAILABLE_MEMORY=$(free -m | awk 'NR==2{printf "%.1f", $7/1024}')
    if (( $(echo "$AVAILABLE_MEMORY < 2.0" | bc -l) )); then
        print_extended_warning "Low available memory: ${AVAILABLE_MEMORY}GB"
    else
        print_extended_success "Available memory: ${AVAILABLE_MEMORY}GB ✓"
    fi

    # Check disk space
    DISK_USAGE=$(df -h . | awk 'NR==2{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 85 ]; then
        print_extended_warning "High disk usage: ${DISK_USAGE}%"
    else
        print_extended_success "Disk usage: ${DISK_USAGE}% ✓"
    fi

    # Check CPU load
    CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    CPU_CORES=$(nproc)
    CPU_LOAD_PERCENT=$(echo "scale=2; $CPU_LOAD / $CPU_CORES * 100" | bc)

    if (( $(echo "$CPU_LOAD_PERCENT > 80" | bc -l) )); then
        print_extended_warning "High CPU load: ${CPU_LOAD_PERCENT}%"
    else
        print_extended_success "CPU load: ${CPU_LOAD_PERCENT}% ✓"
    fi

    print_extended_success "Pre-flight health check completed ✓"
}

# Function to setup monitoring and analytics
setup_extended_monitoring() {
    print_extended_status "Setting up extended monitoring and analytics..."

    # Create monitoring configuration
    cat > "$EXTENDED_STATE_DIR/monitoring_config.json" << EOF
{
    "start_time": $(date +%s),
    "operation_mode": "${OPERATION_MODE:-balanced}",
    "target_uptime_days": ${TARGET_UPTIME_DAYS:-30},
    "monitoring_enabled": true,
    "analytics_enabled": true,
    "predictive_alerts": true
}
EOF

    # Setup log rotation configuration
    cat > "$EXTENDED_LOG_DIR/logrotate.conf" << EOF
$EXTENDED_LOG_DIR/*.log {
    daily
    missingok
    rotate 90
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

    print_extended_success "Extended monitoring setup completed ✓"
}

# Function to create system health dashboard
create_health_dashboard() {
    print_extended_status "Creating health dashboard..."

    cat > "$SCRIPT_DIR/view_extended_health.sh" << 'EOF'
#!/bin/bash

# Extended AutoMode Health Dashboard
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENDED_STATE_DIR="$SCRIPT_DIR/.extended_automode"

echo "=== Extended AutoMode Health Dashboard ==="
echo "Timestamp: $(date)"
echo

# Check if metrics database exists
if [ -f "$EXTENDED_STATE_DIR/metrics.db" ]; then
    echo "📊 Metrics Database: Available"
    DB_SIZE=$(du -h "$EXTENDED_STATE_DIR/metrics.db" | cut -f1)
    echo "   Size: $DB_SIZE"
else
    echo "📊 Metrics Database: Not found"
fi

# Show recent analytics reports
echo
echo "📈 Recent Analytics Reports:"
if [ -d "$EXTENDED_STATE_DIR/analytics_reports" ]; then
    ls -la "$EXTENDED_STATE_DIR/analytics_reports" | tail -5
else
    echo "   No reports available"
fi

# Show system resources
echo
echo "💻 Current System Status:"
echo "   Memory: $(free -h | awk 'NR==2{printf "%.1f%% used", $3/$2*100}')"
echo "   Disk: $(df -h . | awk 'NR==2{print $5 " used"}')"
echo "   Load: $(uptime | awk -F'load average:' '{print $2}')"

# Show recent log entries
echo
echo "📝 Recent Log Entries:"
if [ -f "$SCRIPT_DIR/logs/extended/extended_automode.log" ]; then
    tail -10 "$SCRIPT_DIR/logs/extended/extended_automode.log"
else
    echo "   No log file found"
fi
EOF

    chmod +x "$SCRIPT_DIR/view_extended_health.sh"

    print_extended_success "Health dashboard created: ./view_extended_health.sh ✓"
}

# Function to start extended operation mode
start_extended_operation() {
    print_extended_status "Starting Extended Operation AutoMode..."

    # Create startup timestamp
    echo $(date +%s) > "$EXTENDED_STATE_DIR/startup_timestamp"

    # Start the extended operation
    cd "$SCRIPT_DIR"

    if [ "$DAEMON_MODE" = "true" ]; then
        print_extended_status "Starting in daemon mode..."
        nohup python3 "$EXTENDED_SCRIPT" \
            --mode "$OPERATION_MODE" \
            --config "$EXTENDED_CONFIG" \
            --base-dir "$SCRIPT_DIR" \
            > "$EXTENDED_LOG_DIR/startup.log" 2>&1 &

        EXTENDED_PID=$!
        echo $EXTENDED_PID > "$EXTENDED_STATE_DIR/extended.pid"

        print_extended_success "Extended AutoMode started in daemon mode (PID: $EXTENDED_PID)"
        print_extended_info "View status: ./view_extended_health.sh"
        print_extended_info "View logs: tail -f logs/extended/extended_automode.log"
    else
        print_extended_status "Starting in foreground mode..."
        python3 "$EXTENDED_SCRIPT" \
            --mode "$OPERATION_MODE" \
            --config "$EXTENDED_CONFIG" \
            --base-dir "$SCRIPT_DIR"
    fi
}

# Function to show status
show_status() {
    print_extended_status "Extended AutoMode Status:"

    if [ -f "$EXTENDED_STATE_DIR/extended.pid" ]; then
        PID=$(cat "$EXTENDED_STATE_DIR/extended.pid")
        if ps -p $PID > /dev/null 2>&1; then
            print_extended_success "Extended AutoMode is running (PID: $PID)"

            # Show uptime
            if [ -f "$EXTENDED_STATE_DIR/startup_timestamp" ]; then
                START_TIME=$(cat "$EXTENDED_STATE_DIR/startup_timestamp")
                CURRENT_TIME=$(date +%s)
                UPTIME=$((CURRENT_TIME - START_TIME))
                UPTIME_DAYS=$((UPTIME / 86400))
                UPTIME_HOURS=$(((UPTIME % 86400) / 3600))

                print_extended_info "Uptime: ${UPTIME_DAYS} days, ${UPTIME_HOURS} hours"
            fi

            # Show recent health metrics
            if [ -f "$EXTENDED_LOG_DIR/extended_performance.log" ]; then
                echo "Recent performance metrics:"
                tail -3 "$EXTENDED_LOG_DIR/extended_performance.log"
            fi
        else
            print_extended_warning "PID file exists but process not running"
            rm -f "$EXTENDED_STATE_DIR/extended.pid"
        fi
    else
        print_extended_info "Extended AutoMode is not running"
    fi
}

# Function to stop extended operation
stop_extended_operation() {
    print_extended_status "Stopping Extended AutoMode..."

    if [ -f "$EXTENDED_STATE_DIR/extended.pid" ]; then
        PID=$(cat "$EXTENDED_STATE_DIR/extended.pid")
        if ps -p $PID > /dev/null 2>&1; then
            print_extended_status "Sending graceful shutdown signal..."
            kill -TERM $PID

            # Wait for graceful shutdown
            for i in {1..30}; do
                if ! ps -p $PID > /dev/null 2>&1; then
                    print_extended_success "Extended AutoMode stopped gracefully"
                    break
                fi
                sleep 1
            done

            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                print_extended_warning "Force stopping Extended AutoMode..."
                kill -KILL $PID
            fi
        fi

        rm -f "$EXTENDED_STATE_DIR/extended.pid"
    else
        print_extended_info "Extended AutoMode is not running"
    fi
}

# Main execution
case "${1:-start}" in
    "start")
        OPERATION_MODE="${2:-balanced}"
        TARGET_UPTIME_DAYS="${3:-30}"
        DAEMON_MODE="${4:-true}"

        check_extended_requirements
        optimize_extended_environment
        pre_flight_health_check
        setup_extended_monitoring
        create_health_dashboard
        start_extended_operation
        ;;

    "stop")
        stop_extended_operation
        ;;

    "status")
        show_status
        ;;

    "restart")
        stop_extended_operation
        sleep 2
        OPERATION_MODE="${2:-balanced}"
        TARGET_UPTIME_DAYS="${3:-30}"
        DAEMON_MODE="true"

        check_extended_requirements
        optimize_extended_environment
        pre_flight_health_check
        setup_extended_monitoring
        start_extended_operation
        ;;

    "health")
        if [ -f "$SCRIPT_DIR/view_extended_health.sh" ]; then
            "$SCRIPT_DIR/view_extended_health.sh"
        else
            print_extended_error "Health dashboard not found. Run './launch_extended.sh start' first."
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|status|restart|health} [operation_mode] [target_uptime_days]"
        echo
        echo "Commands:"
        echo "  start     - Start Extended AutoMode (default: balanced mode, 30 days target)"
        echo "  stop      - Stop Extended AutoMode gracefully"
        echo "  status    - Show current status and uptime"
        echo "  restart   - Restart Extended AutoMode"
        echo "  health    - Show health dashboard"
        echo
        echo "Operation Modes:"
        echo "  conservative - Ultra-stable, minimal resource usage"
        echo "  balanced     - Balance between performance and stability (recommended)"
        echo "  aggressive   - Maximum performance with active monitoring"
        echo "  research     - Long-term data collection (1+ year operation)"
        echo
        echo "Examples:"
        echo "  $0 start balanced 60        # Start in balanced mode for 60 days"
        echo "  $0 start research 365       # Start in research mode for 1 year"
        echo "  $0 start conservative 90    # Start in conservative mode for 90 days"
        ;;
esac
