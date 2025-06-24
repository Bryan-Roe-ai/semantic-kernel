#!/bin/bash

# Enhanced AGI Auto File Update System Launcher
# Optimized for high-performance operation

set -e

echo "🚀 Starting Enhanced AGI Auto File Update System..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[ENHANCED-AGI]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check Python version and performance packages
print_status "Checking performance requirements..."
python3 -c "
import sys
if sys.version_info < (3.8):
    print('❌ Python 3.8+ required for optimal performance')
    sys.exit(1)

try:
    import psutil
    print('✅ psutil available for performance monitoring')
except ImportError:
    print('⚠️  Installing psutil for performance monitoring...')
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'])
"

# Set performance environment variables
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false

# Start enhanced system
print_status "Launching enhanced AGI system..."
if [ "$1" = "--monitor" ]; then
    python3 agi_enhanced_file_update_system.py --monitor
elif [ "$1" = "--daemon" ]; then
    nohup python3 agi_enhanced_file_update_system.py --daemon > agi_enhanced_daemon.log 2>&1 &
    print_success "Enhanced AGI system running in daemon mode"
else
    python3 agi_enhanced_file_update_system.py
fi

print_success "Enhanced AGI Auto File Update System ready!"
