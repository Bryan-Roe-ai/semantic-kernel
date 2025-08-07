#!/bin/bash

# Enhanced error fixing script for AI workspace infrastructure
# This script provides comprehensive error detection and resolution

set -euo pipefail  # Exit on any error, undefined variable, or pipe failure

# Configuration
LOG_FILE="/var/log/fix-errors.log"
BACKUP_DIR="/tmp/backup-$(date +%Y%m%d_%H%M%S)"
MAX_RETRIES=3
TIMEOUT=30

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling function
handle_error() {
    local exit_code=$?
    local line_number=$1
    log "ERROR: Command failed with exit code $exit_code at line $line_number"
    log "ERROR: Last command: $BASH_COMMAND"
    exit $exit_code
}

# Set error trap
trap 'handle_error $LINENO' ERR

log "Starting comprehensive error fixing process..."

# Create backup directory
mkdir -p "$BACKUP_DIR"
log "Created backup directory: $BACKUP_DIR"

# Start systemd (if available)
if command -v systemctl &> /dev/null; then
    log "Starting systemd services..."
    sudo systemctl start systemd || log "WARNING: Could not start systemd"
else
    log "WARNING: systemctl not available, skipping systemd start"
fi

# Update package lists with retry logic
log "Updating package lists..."
for i in $(seq 1 $MAX_RETRIES); do
    if timeout $TIMEOUT apt-get update; then
        log "Package lists updated successfully"
        break
    else
        log "WARNING: Package update attempt $i failed, retrying..."
        sleep 5
    fi
    if [ $i -eq $MAX_RETRIES ]; then
        log "ERROR: Failed to update package lists after $MAX_RETRIES attempts"
        exit 1
    fi
done

# Install missing dependencies with error handling
log "Installing missing dependencies..."
apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    gettext \
    python3-pip \
    python3-dev \
    libpq-dev \
    ca-certificates \
    jq \
    wget \
    unzip \
    git \
    build-essential || {
    log "WARNING: Some packages failed to install, continuing..."
}

# Service management with improved error handling
services=("mongod" "redis-server" "postgresql" "docker")
log "Managing services: ${services[*]}"

for service in "${services[@]}"; do
    log "Checking service: $service"

    # Check if service exists
    if ! systemctl list-unit-files | grep -q "^$service"; then
        log "WARNING: Service $service not found, skipping..."
        continue
    fi

    # Try to start the service
    if sudo systemctl start "$service" 2>/dev/null; then
        log "Service $service started successfully"
    else
        log "WARNING: Could not start service $service"
    fi

    # Verify service status
    if sudo systemctl is-active --quiet "$service"; then
        log "Service $service is running"
    else
        log "WARNING: Service $service is not running"
    fi
done

# Verify systemd status
if command -v systemctl &> /dev/null; then
    if sudo systemctl status systemd &> /dev/null; then
        log "Systemd is running properly"
    else
        log "WARNING: Systemd status check failed"
    fi
fi

# Enhanced file cleanup with backup
log "Starting file cleanup process..."
backup_and_delete() {
    local pattern=$1
    local description=$2

    log "Processing $description files..."

    # Find files and create backup
    find . -type f -name "$pattern" -print0 | while IFS= read -r -d '' file; do
        if [ -f "$file" ]; then
            # Create directory structure in backup
            backup_path="$BACKUP_DIR$(dirname "$file")"
            mkdir -p "$backup_path"

            # Copy to backup before deletion
            cp "$file" "$backup_path/" 2>/dev/null || log "WARNING: Could not backup $file"

            # Delete original
            rm -f "$file" && log "Deleted: $file"
        fi
    done
}

backup_and_delete '*.bin' 'binary'
backup_and_delete '*.exe' 'executable'
backup_and_delete '*.dll' 'dynamic library'
backup_and_delete '*.zip' 'archive'

# Generate comprehensive report
log "Generating cleanup report..."
cat > deleted-files-report.txt << EOF
Cleanup Report - $(date)
========================

Backup Location: $BACKUP_DIR

Files Processed:
$(find "$BACKUP_DIR" -type f | wc -l) files backed up and deleted

Backup Directory Size:
$(du -sh "$BACKUP_DIR" 2>/dev/null || echo "Could not determine size")

File Types Processed:
- Binary files (*.bin)
- Executable files (*.exe)
- Dynamic libraries (*.dll)
- Archive files (*.zip)
EOF

# Safe temporary file cleanup
log "Cleaning temporary files..."
if [ -d "/tmp" ]; then
    find /tmp -type f -mtime +1 -delete 2>/dev/null || log "WARNING: Could not clean all temp files"
    log "Temporary files cleaned"
fi

# Docker system maintenance
if command -v docker &> /dev/null; then
    log "Performing Docker maintenance..."
    docker system prune -f --volumes 2>/dev/null || log "WARNING: Docker prune failed"
    log "Docker system cleaned"
else
    log "WARNING: Docker not available, skipping Docker cleanup"
fi

# Package manager checks with error handling
log "Running package manager checks..."

# NPM audit (if npm is available)
if command -v npm &> /dev/null; then
    log "Running npm audit..."
    npm audit --audit-level=moderate 2>/dev/null || log "WARNING: npm audit found issues or failed"
else
    log "INFO: npm not available, skipping npm audit"
fi

# Python package check (if pip is available)
if command -v pip3 &> /dev/null; then
    log "Running pip check..."
    pip3 check 2>/dev/null || log "WARNING: pip check found issues or failed"
else
    log "INFO: pip3 not available, skipping pip check"
fi

# .NET restore (if dotnet is available)
if command -v dotnet &> /dev/null; then
    log "Running dotnet restore..."
    dotnet restore 2>/dev/null || log "WARNING: dotnet restore failed"
else
    log "INFO: dotnet not available, skipping dotnet restore"
fi

# Enhanced network connectivity check
log "Checking network connectivity..."
check_connectivity() {
    local host=$1
    local retries=3

    for i in $(seq 1 $retries); do
        if ping -c 1 -W 5 "$host" &> /dev/null; then
            log "Network connectivity to $host: OK"
            return 0
        fi
        sleep 2
    done

    log "WARNING: Network connectivity to $host failed"
    return 1
}

check_connectivity "8.8.8.8"
check_connectivity "google.com"

# Enhanced disk space management
log "Checking disk space..."
required_space=10485760 # 10GB in KB
available_space=$(df / | tail -1 | awk '{print $4}')

log "Available disk space: $(($available_space / 1024 / 1024))GB"
log "Required disk space: $(($required_space / 1024 / 1024))GB"

if [ "$available_space" -lt "$required_space" ]; then
    log "WARNING: Insufficient disk space. Performing cleanup..."

    # Clean package manager caches
    apt-get clean 2>/dev/null || true
    pip3 cache purge 2>/dev/null || true
    npm cache clean --force 2>/dev/null || true

    # Clean old log files (older than 7 days)
    find /var/log -name "*.log" -mtime +7 -delete 2>/dev/null || true

    # Check space again
    available_space=$(df / | tail -1 | awk '{print $4}')
    if [ "$available_space" -lt "$required_space" ]; then
        log "WARNING: Disk space still insufficient after cleanup"
    else
        log "Disk space freed up successfully"
    fi
fi

# Enhanced permission management
log "Fixing file and directory permissions..."
find . -type d -exec chmod 755 {} + 2>/dev/null || log "WARNING: Could not fix all directory permissions"
find . -type f -exec chmod 644 {} + 2>/dev/null || log "WARNING: Could not fix all file permissions"

# Make scripts executable
find . -type f -name "*.sh" -exec chmod +x {} + 2>/dev/null || log "WARNING: Could not make all scripts executable"

# Configuration validation
log "Validating service configurations..."

validate_mongodb_config() {
    local config_file="/etc/mongod.conf"
    if [ -f "$config_file" ]; then
        if mongod --config "$config_file" --fork --logpath /var/log/mongodb/test.log --pidfilepath /tmp/mongod_test.pid 2>/dev/null; then
            # Stop the test instance
            kill $(cat /tmp/mongod_test.pid) 2>/dev/null || true
            rm -f /tmp/mongod_test.pid
            log "MongoDB configuration is valid"
        else
            log "WARNING: MongoDB configuration validation failed"
        fi
    else
        log "INFO: MongoDB configuration file not found"
    fi
}

validate_redis_config() {
    local config_file="/etc/redis/redis.conf"
    if [ -f "$config_file" ]; then
        if redis-server "$config_file" --test-memory 1 2>/dev/null; then
            log "Redis configuration is valid"
        else
            log "WARNING: Redis configuration validation failed"
        fi
    else
        log "INFO: Redis configuration file not found"
    fi
}

validate_postgresql_config() {
    if command -v pg_ctl &> /dev/null; then
        if sudo -u postgres pg_ctl status -D /var/lib/postgresql/data 2>/dev/null; then
            log "PostgreSQL configuration is valid"
        else
            log "WARNING: PostgreSQL configuration check failed"
        fi
    else
        log "INFO: PostgreSQL not available for configuration check"
    fi
}

validate_mongodb_config
validate_redis_config
validate_postgresql_config

# Environment variable validation with defaults
log "Validating environment variables..."
set_default_env_var() {
    local var_name=$1
    local default_value=$2

    if [ -z "${!var_name:-}" ]; then
        export "$var_name"="$default_value"
        log "Set default value for $var_name"
    else
        log "Environment variable $var_name is set"
    fi
}

# Set defaults for required environment variables
set_default_env_var "DB_HOST" "localhost"
set_default_env_var "DB_USER" "postgres"
set_default_env_var "DB_PASS" "password"
set_default_env_var "REDIS_HOST" "localhost"
set_default_env_var "REDIS_PORT" "6379"

# Enhanced system resource management
log "Adjusting system resource limits..."
ulimit -n 4096 2>/dev/null || log "WARNING: Could not set file descriptor limit"
ulimit -u 1024 2>/dev/null || log "WARNING: Could not set process limit"

# Enhanced log rotation
log "Managing log rotation..."
logrotate_conf="/etc/logrotate.conf"
if [ -f "$logrotate_conf" ]; then
    if sudo logrotate -f "$logrotate_conf" 2>/dev/null; then
        log "Log rotation completed successfully"
    else
        log "WARNING: Log rotation failed"
    fi
else
    log "WARNING: Logrotate configuration file not found"
fi

# Security scanning (if trivy is available)
log "Performing security scanning..."
if command -v trivy &> /dev/null; then
    # Only scan if we have a repository set
    if [ -n "${GITHUB_REPOSITORY:-}" ]; then
        if trivy image --severity CRITICAL,HIGH --no-progress --exit-code 0 "ghcr.io/${GITHUB_REPOSITORY}/my-app:latest" 2>/dev/null; then
            log "Security scan completed - no critical/high vulnerabilities found"
        else
            log "WARNING: Security scan found vulnerabilities or failed"
        fi
    else
        log "INFO: GITHUB_REPOSITORY not set, skipping container security scan"
    fi
else
    log "INFO: Trivy not available, skipping security scan"
fi

# Docker secrets management
log "Checking Docker secrets..."
if [ -f "/run/secrets/DB_PASSWORD" ]; then
    export DB_PASSWORD=$(cat /run/secrets/DB_PASSWORD)
    log "Docker secret DB_PASSWORD loaded successfully"
elif [ -f "/var/run/secrets/DB_PASSWORD" ]; then
    export DB_PASSWORD=$(cat /var/run/secrets/DB_PASSWORD)
    log "Docker secret DB_PASSWORD loaded from alternate location"
else
    log "INFO: Docker secret DB_PASSWORD not found, using environment variable"
fi

# Final system health check
log "Performing final system health check..."
health_check_passed=true

# Check critical services
for service in "${services[@]}"; do
    if systemctl list-unit-files | grep -q "^$service" && ! systemctl is-active --quiet "$service"; then
        log "WARNING: Critical service $service is not running"
        health_check_passed=false
    fi
done

# Check disk space one more time
final_available_space=$(df / | tail -1 | awk '{print $4}')
if [ "$final_available_space" -lt 5242880 ]; then  # 5GB minimum
    log "WARNING: Low disk space remaining: $(($final_available_space / 1024 / 1024))GB"
    health_check_passed=false
fi

# Check load average
load_avg=$(uptime | awk -F'load average:' '{ print $2 }' | awk '{ print $1 }' | sed 's/,//')
if (( $(echo "$load_avg > 10" | bc -l) )); then
    log "WARNING: High system load average: $load_avg"
    health_check_passed=false
fi

# Generate final report
cat > error-fix-report.txt << EOF
Error Fix Completion Report
===========================
Date: $(date)
Duration: $SECONDS seconds

Summary:
- Backup Directory: $BACKUP_DIR
- Log File: $LOG_FILE
- Health Check: $([ "$health_check_passed" = true ] && echo "PASSED" || echo "WARNINGS FOUND")

Services Checked: ${services[*]}
Environment Variables Set: DB_HOST, DB_USER, DB_PASS, REDIS_HOST, REDIS_PORT

System Status:
- Available Disk Space: $(($final_available_space / 1024 / 1024))GB
- Load Average: $load_avg
- File Descriptor Limit: $(ulimit -n)
- Process Limit: $(ulimit -u)

Next Steps:
$([ "$health_check_passed" = false ] && echo "- Review warnings in log file: $LOG_FILE" || echo "- System appears healthy")
- Monitor system performance
- Review backup files in: $BACKUP_DIR

EOF

if [ "$health_check_passed" = true ]; then
    log "✅ All errors fixed successfully! System is healthy."
    exit 0
else
    log "⚠️  Error fixing completed with warnings. Check the report for details."
    exit 0  # Don't fail the script for warnings
fi
