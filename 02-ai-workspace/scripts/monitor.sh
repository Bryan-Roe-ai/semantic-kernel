#!/bin/bash
# 🤖 Quick AI Monitor Launcher
# Easy one-command startup for AI activity monitoring

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "🤖 AI Activity Monitor - Quick Start"
echo "======================================"
echo "📁 Workspace: $WORKSPACE_ROOT"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

# Check if monitoring is set up
if [ ! -f "$SCRIPT_DIR/ai_monitor_launcher.py" ]; then
    echo "❌ Error: Monitoring scripts not found"
    echo "   Please run setup first: python setup_monitoring.py"
    exit 1
fi

# Default action
ACTION=${1:-dashboard}

case $ACTION in
    "dashboard"|"d")
        echo "🎯 Starting AI Activity Dashboard..."
        echo "   Press Ctrl+C to stop"
        echo
        cd "$SCRIPT_DIR"
        python3 ai_monitor_launcher.py dashboard
        ;;
    "feed"|"f")
        echo "📡 Starting Live Activity Feed..."
        echo "   Press Ctrl+C to stop"
        echo
        cd "$SCRIPT_DIR"
        python3 ai_monitor_launcher.py feed
        ;;
    "report"|"r")
        HOURS=${2:-24}
        echo "📊 Generating $HOURS-hour Activity Report..."
        cd "$SCRIPT_DIR"
        python3 ai_monitor_launcher.py report --hours $HOURS
        ;;
    "test"|"t")
        echo "🧪 Testing AI Monitoring System..."
        cd "$SCRIPT_DIR"
        python3 ai_monitor_launcher.py test
        ;;
    "status"|"s")
        echo "📊 Checking System Status..."
        cd "$SCRIPT_DIR"
        python3 ai_monitor_launcher.py status
        ;;
    "setup")
        echo "🔧 Setting up AI Monitoring System..."
        cd "$SCRIPT_DIR"
        python3 setup_monitoring.py
        ;;
    "help"|"h")
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  dashboard (d)     - Start real-time dashboard (default)"
        echo "  feed (f)          - Show live activity feed"
        echo "  report (r) [hours]- Generate activity report (default: 24 hours)"
        echo "  test (t)          - Test the monitoring system"
        echo "  status (s)        - Show system status"
        echo "  setup             - Set up the monitoring system"
        echo "  help (h)          - Show this help"
        echo
        echo "Examples:"
        echo "  $0                    # Start dashboard"
        echo "  $0 dashboard          # Start dashboard"
        echo "  $0 feed               # Live activity feed"
        echo "  $0 report 48          # 48-hour report"
        echo "  $0 test               # Test system"
        ;;
    *)
        echo "❌ Unknown command: $ACTION"
        echo "   Run '$0 help' for usage information"
        exit 1
        ;;
esac
