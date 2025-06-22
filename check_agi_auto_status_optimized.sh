#!/bin/bash

# Optimized AGI Auto File Updates - Performance Status Monitor
# Advanced status checking with performance metrics and optimization insights

echo "🚀 Optimized AGI Auto File Updates Status"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Performance monitoring functions
get_process_memory() {
    local pid=$1
    ps -p $pid -o rss= 2>/dev/null | awk '{print $1/1024}' || echo "0"
}

get_process_cpu() {
    local pid=$1
    ps -p $pid -o %cpu= 2>/dev/null | tr -d ' ' || echo "0"
}

check_performance_status() {
    echo -e "${PURPLE}📊 Performance Metrics${NC}"
    echo "====================="

    # Check if performance log exists
    if [ -f "agi_performance.log" ]; then
        local log_entries=$(wc -l < agi_performance.log 2>/dev/null || echo "0")
        echo -e "${GREEN}✅ Performance Log: $log_entries entries${NC}"

        # Show recent performance data
        if [ "$log_entries" -gt 0 ]; then
            local last_entry=$(tail -n 1 agi_performance.log 2>/dev/null)
            echo -e "   📈 Latest: $last_entry"
        fi
    else
        echo -e "${YELLOW}⚠️  Performance Log: No data${NC}"
    fi

    # Memory usage analysis
    local total_memory_mb=$(free -m | awk '/^Mem:/{print $2}')
    local available_memory_mb=$(free -m | awk '/^Mem:/{print $7}')
    local memory_usage_percent=$(( (total_memory_mb - available_memory_mb) * 100 / total_memory_mb ))

    echo -e "${CYAN}   💾 System Memory: ${memory_usage_percent}% used (${available_memory_mb}MB available)${NC}"

    # CPU load
    local cpu_load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')
    echo -e "${CYAN}   🖥️  CPU Load: $cpu_load${NC}"

    # Disk space for workspace
    local disk_usage=$(df . | awk 'NR==2 {print $5}' | tr -d '%')
    local disk_available=$(df -h . | awk 'NR==2 {print $4}')
    echo -e "${CYAN}   💿 Disk Usage: ${disk_usage}% (${disk_available} available)${NC}"

    echo ""
}

# Check if optimized launch script is running
echo -e "${BLUE}🔍 Process Status Check${NC}"
echo "======================"

if ps aux | grep -q "[l]aunch_agi_enhanced_auto.sh"; then
    opt_pid=$(ps aux | grep "[l]aunch_agi_enhanced_auto.sh" | awk '{print $2}' | head -1)
    opt_memory=$(get_process_memory $opt_pid)
    opt_cpu=$(get_process_cpu $opt_pid)
    echo -e "${GREEN}✅ Enhanced Launch Script: RUNNING (PID: $opt_pid)${NC}"
    echo -e "   📊 Memory: ${opt_memory}MB, CPU: ${opt_cpu}%"
elif ps aux | grep -q "[l]aunch_agi_auto.sh"; then
    echo -e "${YELLOW}⚠️  Standard Launch Script: RUNNING (consider upgrading to enhanced)${NC}"
else
    echo -e "${RED}❌ Launch Script: NOT RUNNING${NC}"
fi

# Check if enhanced main process is running
if ps aux | grep -q "[a]gi_enhanced_file_update_system.py"; then
    main_pid=$(ps aux | grep "[a]gi_enhanced_file_update_system.py" | awk '{print $2}' | head -1)
    main_memory=$(get_process_memory $main_pid)
    main_cpu=$(get_process_cpu $main_pid)
    echo -e "${GREEN}✅ Enhanced AGI System: RUNNING (PID: $main_pid)${NC}"
    echo -e "   📊 Memory: ${main_memory}MB, CPU: ${main_cpu}%"
elif ps aux | grep -q "[a]gi_file_update_system.py"; then
    echo -e "${YELLOW}⚠️  Standard AGI System: RUNNING (consider upgrading to enhanced)${NC}"
else
    echo -e "${RED}❌ AGI File System: STOPPED${NC}"
fi

echo ""

# Configuration analysis
echo -e "${BLUE}⚙️  Configuration Analysis${NC}"
echo "========================="

if [ -f ".agi_file_config.json" ]; then
    echo -e "${GREEN}✅ Configuration: FOUND${NC}"

    # Check for optimization settings
    if command -v jq &> /dev/null; then
        safe_dirs=$(jq -r '.safe_directories | length' .agi_file_config.json 2>/dev/null || echo "unknown")
        max_tasks=$(jq -r '.performance_settings.max_concurrent_tasks // "not set"' .agi_file_config.json 2>/dev/null)
        cache_ttl=$(jq -r '.performance_settings.cache_ttl_seconds // "not set"' .agi_file_config.json 2>/dev/null)
        parallel_enabled=$(jq -r '.performance_settings.enable_parallel_processing // "not set"' .agi_file_config.json 2>/dev/null)
        compression=$(jq -r '.optimization_flags.compress_backups // "not set"' .agi_file_config.json 2>/dev/null)
        caching=$(jq -r '.optimization_flags.cache_file_analysis // "not set"' .agi_file_config.json 2>/dev/null)

        echo -e "   📁 Safe directories: $safe_dirs"
        echo -e "   🔧 Max concurrent tasks: $max_tasks"
        echo -e "   ⏱️  Cache TTL: ${cache_ttl}s"
        echo -e "   ⚡ Parallel processing: $parallel_enabled"
        echo -e "   🗜️  Backup compression: $compression"
        echo -e "   💾 File analysis caching: $caching"

        # Configuration optimization score
        opt_score=0
        [ "$max_tasks" != "not set" ] && opt_score=$((opt_score + 1))
        [ "$parallel_enabled" = "true" ] && opt_score=$((opt_score + 1))
        [ "$compression" = "true" ] && opt_score=$((opt_score + 1))
        [ "$caching" = "true" ] && opt_score=$((opt_score + 1))

        opt_percentage=$((opt_score * 25))
        echo -e "   📈 Optimization level: ${opt_percentage}% (${opt_score}/4 features enabled)"

    else
        echo -e "   ⚠️  Install 'jq' for detailed configuration analysis"
    fi
else
    echo -e "${RED}❌ Configuration: MISSING${NC}"
fi

echo ""

# Backup and cache analysis
echo -e "${BLUE}💾 Storage Analysis${NC}"
echo "=================="

if [ -d ".agi_backups" ]; then
    backup_count=$(ls -1 .agi_backups/ 2>/dev/null | wc -l)
    backup_size=$(du -sh .agi_backups/ 2>/dev/null | cut -f1 || echo "0B")
    echo -e "${GREEN}✅ Backup Directory: EXISTS ($backup_count files, $backup_size)${NC}"

    # Check for compressed backups
    compressed_count=$(ls -1 .agi_backups/*.gz 2>/dev/null | wc -l || echo "0")
    if [ "$compressed_count" -gt 0 ]; then
        echo -e "   🗜️  Compressed backups: $compressed_count (space optimized)"
    fi
else
    echo -e "${RED}❌ Backup Directory: MISSING${NC}"
fi

# Cache directory
if [ -d ".agi_cache" ]; then
    cache_size=$(du -sh .agi_cache/ 2>/dev/null | cut -f1 || echo "0B")
    echo -e "${GREEN}✅ Cache Directory: EXISTS ($cache_size)${NC}"
else
    echo -e "${YELLOW}⚠️  Cache Directory: MISSING (performance may be reduced)${NC}"
fi

echo ""

# Log file analysis
echo -e "${BLUE}📝 Log Analysis${NC}"
echo "==============="

if [ -f "agi_file_updates.log" ]; then
    echo -e "${GREEN}✅ Main Log File: ACTIVE${NC}"
    last_entry=$(tail -n 1 agi_file_updates.log 2>/dev/null | cut -d' ' -f1-2)
    total_lines=$(wc -l < agi_file_updates.log 2>/dev/null || echo "0")
    echo -e "   📝 Last activity: $last_entry"
    echo -e "   📊 Total entries: $total_lines"

    # Analyze recent activity (last hour)
    recent_activity=$(grep "$(date '+%Y-%m-%d %H:')" agi_file_updates.log 2>/dev/null | wc -l || echo "0")
    echo -e "   ⏰ Recent activity (last hour): $recent_activity entries"

    # Error analysis
    error_count=$(grep -c "ERROR" agi_file_updates.log 2>/dev/null || echo "0")
    warning_count=$(grep -c "WARNING" agi_file_updates.log 2>/dev/null || echo "0")

    if [ "$error_count" -gt 0 ]; then
        echo -e "   ${RED}❌ Errors found: $error_count${NC}"
    fi

    if [ "$warning_count" -gt 0 ]; then
        echo -e "   ${YELLOW}⚠️  Warnings found: $warning_count${NC}"
    fi

    if [ "$error_count" -eq 0 ] && [ "$warning_count" -eq 0 ]; then
        echo -e "   ${GREEN}✅ No errors or warnings${NC}"
    fi
else
    echo -e "${RED}❌ Log File: MISSING${NC}"
fi

echo ""

# Performance monitoring
check_performance_status

# Backend status
echo -e "${BLUE}🌐 Backend Status${NC}"
echo "================"

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ AGI Backend: ONLINE${NC}"

    # Try to get backend info
    local backend_info=$(curl -s http://localhost:8000/api/status 2>/dev/null || echo "")
    if [ -n "$backend_info" ]; then
        echo -e "   📡 Backend API: Responding"
    fi
else
    echo -e "${YELLOW}⚠️  AGI Backend: OFFLINE (limited functionality)${NC}"
fi

echo ""

# Optimization recommendations
echo -e "${PURPLE}🔧 Optimization Recommendations${NC}"
echo "==============================="

# Check if using optimized version
if ! ps aux | grep -q "[a]gi_enhanced_file_update_system.py"; then
    echo -e "${YELLOW}📈 Upgrade to optimized version:${NC}"
    echo -e "   ./launch_agi_enhanced_auto.sh --daemon"
fi

# Check configuration optimizations
if [ -f ".agi_file_config.json" ] && command -v jq &> /dev/null; then
    parallel_enabled=$(jq -r '.performance_settings.enable_parallel_processing // false' .agi_file_config.json 2>/dev/null)
    if [ "$parallel_enabled" != "true" ]; then
        echo -e "${YELLOW}⚡ Enable parallel processing for better performance${NC}"
    fi

    compression=$(jq -r '.optimization_flags.compress_backups // false' .agi_file_config.json 2>/dev/null)
    if [ "$compression" != "true" ]; then
        echo -e "${YELLOW}🗜️  Enable backup compression to save disk space${NC}"
    fi
fi

# Memory usage check
memory_usage=$(free | awk '/^Mem:/ {printf "%.1f", ($3/$2)*100}')
if command -v bc &> /dev/null && (( $(echo "$memory_usage > 80" | bc -l) )); then
    echo -e "${YELLOW}💾 High memory usage detected (${memory_usage}%) - consider reducing cache size${NC}"
fi

echo ""
echo -e "${GREEN}🎯 Quick Actions:${NC}"
echo "   Start Optimized:  ./launch_agi_enhanced_auto.sh --monitor"
echo "   Stop System:      pkill -f agi_file_update_system"
echo "   View Logs:        tail -f agi_file_updates.log"
echo "   Performance:      tail -f agi_performance.log"
echo "   Edit Config:      code .agi_file_config.json"
echo ""
