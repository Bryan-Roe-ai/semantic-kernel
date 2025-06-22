#!/bin/bash

# AGI Auto File Updates - Status Monitor
# Quick status check for the autonomous file update system

echo "🤖 AGI Auto File Updates Status"
echo "==============================="
echo ""

# Check if launch script is running
if ps aux | grep -q "[l]aunch_agi_auto.sh"; then
    echo "✅ Launch Script: RUNNING"
else
    echo "❌ Launch Script: NOT RUNNING"
fi

# Check if main process is running
if ps aux | grep -q "[a]gi_file_update_system.py"; then
    echo "✅ AGI File System: RUNNING"
else
    echo "❌ AGI File System: STOPPED"
fi

# Check configuration
if [ -f ".agi_file_config.json" ]; then
    echo "✅ Configuration: FOUND"
    safe_dirs=$(jq -r '.safe_directories | length' .agi_file_config.json 2>/dev/null || echo "unknown")
    echo "   📁 Safe directories: $safe_dirs"
else
    echo "❌ Configuration: MISSING"
fi

# Check backup directory
if [ -d ".agi_backups" ]; then
    backup_count=$(ls -1 .agi_backups/ 2>/dev/null | wc -l)
    echo "✅ Backup Directory: EXISTS ($backup_count files)"
else
    echo "❌ Backup Directory: MISSING"
fi

# Check log file
if [ -f "agi_file_updates.log" ]; then
    echo "✅ Log File: ACTIVE"
    last_entry=$(tail -n 1 agi_file_updates.log 2>/dev/null | cut -d' ' -f1-2)
    echo "   📝 Last activity: $last_entry"
else
    echo "❌ Log File: MISSING"
fi

# Check AGI backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ AGI Backend: ONLINE"
else
    echo "⚠️  AGI Backend: OFFLINE (limited functionality)"
fi

echo ""
echo "🎯 Quick Actions:"
echo "   Start System: ./launch_agi_auto.sh --monitor"
echo "   Stop System:  pkill -f agi_file_update_system"
echo "   View Logs:    tail -f agi_file_updates.log"
echo "   Edit Config:  code .agi_file_config.json"
echo ""
