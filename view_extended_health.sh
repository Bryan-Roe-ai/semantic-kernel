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
