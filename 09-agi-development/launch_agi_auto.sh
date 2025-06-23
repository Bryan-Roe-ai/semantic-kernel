#!/bin/bash

# AGI Auto File Update System Launcher
# Integrates with the Neural-Symbolic AGI for autonomous file operations

set -e

echo "🤖 Starting AGI Auto File Update System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[AGI-AUTO]${NC} $1"
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

# Check if we're in the right directory
if [ ! -f "AGI_CHAT_README.md" ]; then
    print_error "Please run this script from the semantic-kernel directory"
    exit 1
fi

# Check Python installation
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

# Check required packages
print_status "Checking required packages..."
python3 -c "
import sys
required_packages = ['torch', 'numpy', 'pathlib', 'asyncio']
missing = []
for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print('Missing packages:', ', '.join(missing))
    sys.exit(1)
else:
    print('All required packages are available')
"

if [ $? -ne 0 ]; then
    print_warning "Installing missing packages..."
    pip3 install torch numpy
fi

# Check AGI system status
print_status "Checking AGI system integration..."
if [ -f "agi_chat_integration.py" ]; then
    print_success "AGI Chat Integration found"
else
    print_warning "AGI Chat Integration not found, creating basic integration..."
fi

# Ensure backup directory exists
print_status "Setting up backup directory..."
mkdir -p .agi_backups
print_success "Backup directory ready"

# Check configuration
print_status "Checking AGI configuration..."
if [ -f ".agi_file_config.json" ]; then
    print_success "AGI configuration found"
else
    print_warning "AGI configuration not found - will be created on first run"
fi

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down AGI Auto File Update System..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if AGI backend is running
print_status "Checking AGI backend..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_status "Starting AGI backend server..."
    if [ -d "agi-backend-server" ]; then
        cd agi-backend-server
        python3 main.py &
        BACKEND_PID=$!
        cd ..
        print_success "AGI backend started (PID: $BACKEND_PID)"
    else
        print_warning "AGI backend server not found - some features may be limited"
    fi
else
    print_success "AGI backend already running"
fi

# Wait for backend to be ready
print_status "Waiting for AGI backend to be ready..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "AGI backend is ready!"
        break
    fi
    sleep 1
done

# Start the auto file update system
print_status "Starting AGI Auto File Update System..."
python3 agi_file_update_system.py &
AGI_FILE_PID=$!

# Wait a moment for startup
sleep 2

# Check if the system started successfully
if ps -p $AGI_FILE_PID > /dev/null; then
    print_success "AGI Auto File Update System started (PID: $AGI_FILE_PID)"
else
    print_error "Failed to start AGI Auto File Update System"
    exit 1
fi

# Start monitoring mode if requested
if [ "$1" = "--monitor" ]; then
    print_status "Starting in monitoring mode..."

    # Create monitoring loop
    while true; do
        sleep 300  # Check every 5 minutes

        # Check if processes are still running
        if ! ps -p $AGI_FILE_PID > /dev/null; then
            print_warning "AGI Auto File Update System stopped, restarting..."
            python3 agi_file_update_system.py &
            AGI_FILE_PID=$!
        fi

        # Log status
        echo "$(date): AGI Auto File Update System running (PID: $AGI_FILE_PID)" >> agi_auto_status.log
    done
fi

# Start in daemon mode if requested
if [ "$1" = "--daemon" ]; then
    print_status "Starting in daemon mode..."
    nohup python3 agi_file_update_system.py > agi_auto_daemon.log 2>&1 &
    print_success "AGI Auto File Update System running in daemon mode"
    exit 0
fi

# Interactive mode
print_status ""
print_success "🎯 AGI Auto File Update System is now running!"
print_status ""
print_status "✨ Features Available:"
print_status "   • Autonomous file creation and updates"
print_status "   • Neural-symbolic AI integration"
print_status "   • Automatic backups and safety checks"
print_status "   • Code enhancement and documentation"
print_status "   • Integration with Semantic Kernel"
print_status ""
print_status "🔧 System Status:"
print_status "   • AGI Backend: http://localhost:8000"
print_status "   • Auto File System: Active"
print_status "   • Configuration: .agi_file_config.json"
print_status "   • Backups: .agi_backups/"
print_status "   • Logs: agi_file_updates.log"
print_status ""
print_status "💡 Usage Options:"
print_status "   • ./launch_agi_auto.sh --monitor  (monitoring mode)"
print_status "   • ./launch_agi_auto.sh --daemon   (daemon mode)"
print_status "   • python3 agi_file_update_system.py (direct run)"
print_status ""
print_status "📖 For integration with VS Code, see AGI_CHAT_README.md"
print_status ""
print_status "Press Ctrl+C to stop all services"

# Wait for background processes
wait
