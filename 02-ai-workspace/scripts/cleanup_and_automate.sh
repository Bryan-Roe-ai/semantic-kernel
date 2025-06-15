#!/bin/bash
# Workspace Cleanup and Automation Script
# Handles cleanup, optimization, and automation tasks

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
WORKSPACE_ROOT="/workspaces/semantic-kernel/ai-workspace"
CLEANUP_LOG="$WORKSPACE_ROOT/logs/cleanup.log"

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$CLEANUP_LOG"
}

log_warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$CLEANUP_LOG"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$CLEANUP_LOG"
}

# Create logs directory if it doesn't exist
mkdir -p "$(dirname "$CLEANUP_LOG")"

# =============================================================================
# Cleanup Functions
# =============================================================================

cleanup_python_cache() {
    log "🧹 Cleaning Python cache files..."

    find "$WORKSPACE_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    find "$WORKSPACE_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$WORKSPACE_ROOT" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find "$WORKSPACE_ROOT" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

    log "✅ Python cache cleanup completed"
}

cleanup_logs() {
    log "📝 Cleaning old log files..."

    # Keep only last 7 days of logs
    find "$WORKSPACE_ROOT/logs" -name "*.log" -mtime +7 -delete 2>/dev/null || true

    # Rotate large log files
    find "$WORKSPACE_ROOT/logs" -name "*.log" -size +100M -exec truncate -s 0 {} \; 2>/dev/null || true

    log "✅ Log cleanup completed"
}

cleanup_temporary_files() {
    log "🗑️  Cleaning temporary files..."

    # Remove temporary files
    find "$WORKSPACE_ROOT" -name "*.tmp" -delete 2>/dev/null || true
    find "$WORKSPACE_ROOT" -name "*.bak" -delete 2>/dev/null || true
    find "$WORKSPACE_ROOT" -name "*~" -delete 2>/dev/null || true
    find "$WORKSPACE_ROOT" -name ".DS_Store" -delete 2>/dev/null || true

    # Clean Jupyter checkpoints
    find "$WORKSPACE_ROOT" -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true

    log "✅ Temporary files cleanup completed"
}

cleanup_broken_symlinks() {
    log "🔗 Cleaning broken symbolic links..."

    find "$WORKSPACE_ROOT" -type l -! -exec test -e {} \; -delete 2>/dev/null || true

    log "✅ Broken symlinks cleanup completed"
}

optimize_workspace_structure() {
    log "🏗️  Optimizing workspace structure..."

    # Ensure all directories exist
    local directories=(
        "01-notebooks" "02-agents" "03-models-training" "04-plugins"
        "05-samples-demos" "06-backend-services" "07-data-resources"
        "08-documentation" "09-deployment" "10-config"
        "logs" "data" "uploads" "models" "cache"
    )

    for dir in "${directories[@]}"; do
        mkdir -p "$WORKSPACE_ROOT/$dir"
    done

    # Set proper permissions
    chmod -R 755 "$WORKSPACE_ROOT/scripts" 2>/dev/null || true
    chmod +x "$WORKSPACE_ROOT"/*.sh 2>/dev/null || true

    log "✅ Workspace structure optimization completed"
}

# =============================================================================
# Automation Functions
# =============================================================================

update_dependencies() {
    log "📦 Updating Python dependencies..."

    if [ -f "$WORKSPACE_ROOT/requirements.txt" ]; then
        pip install --upgrade -r "$WORKSPACE_ROOT/requirements.txt" || log_warn "Dependency update failed"
    fi

    log "✅ Dependencies updated"
}

backup_configuration() {
    log "💾 Backing up configuration files..."

    local backup_dir="$WORKSPACE_ROOT/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"

    # Backup important files
    [ -f "$WORKSPACE_ROOT/.env" ] && cp "$WORKSPACE_ROOT/.env" "$backup_dir/"
    [ -f "$WORKSPACE_ROOT/requirements.txt" ] && cp "$WORKSPACE_ROOT/requirements.txt" "$backup_dir/"
    [ -d "$WORKSPACE_ROOT/.vscode" ] && cp -r "$WORKSPACE_ROOT/.vscode" "$backup_dir/"

    # Keep only last 5 backups
    ls -dt "$WORKSPACE_ROOT/backups"/*/ 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true

    log "✅ Configuration backup completed"
}

run_health_checks() {
    log "🔍 Running system health checks..."

    # Check Python environment
    python --version || log_error "Python not available"

    # Check key packages
    python -c "import semantic_kernel" 2>/dev/null || log_warn "Semantic Kernel not available"
    python -c "import openai" 2>/dev/null || log_warn "OpenAI package not available"

    # Check disk space
    local disk_usage=$(df "$WORKSPACE_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 80 ]; then
        log_warn "Disk usage is ${disk_usage}% - consider cleanup"
    fi

    # Check memory usage
    local mem_usage=$(free | awk 'NR==2{print ($3/$2)*100}')
    if (( $(echo "$mem_usage > 80" | bc -l) )); then
        log_warn "Memory usage is ${mem_usage}% - consider optimization"
    fi

    log "✅ Health checks completed"
}

# =============================================================================
# Docker-specific Functions
# =============================================================================

prepare_for_docker() {
    log "🐳 Preparing workspace for Docker deployment..."

    # Ensure Docker files exist
    [ ! -f "$WORKSPACE_ROOT/Dockerfile" ] && log_error "Dockerfile not found"
    [ ! -f "$WORKSPACE_ROOT/docker-compose.yml" ] && log_error "docker-compose.yml not found"

    # Create .dockerignore if it doesn't exist
    if [ ! -f "$WORKSPACE_ROOT/.dockerignore" ]; then
        cat > "$WORKSPACE_ROOT/.dockerignore" << EOF
.git
.gitignore
.env
logs/
cache/
backups/
*.log
__pycache__/
*.pyc
.pytest_cache/
.ipynb_checkpoints/
node_modules/
.vscode/
README.md
EOF
    fi

    # Validate environment file
    if [ ! -f "$WORKSPACE_ROOT/.env" ] && [ -f "$WORKSPACE_ROOT/.env.template" ]; then
        cp "$WORKSPACE_ROOT/.env.template" "$WORKSPACE_ROOT/.env"
        log_warn "Created .env from template - please configure your API keys"
    fi

    log "✅ Docker preparation completed"
}

# =============================================================================
# Main Execution
# =============================================================================

show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --cleanup, -c        Run complete cleanup"
    echo "  --optimize, -o       Optimize workspace structure"
    echo "  --update, -u         Update dependencies"
    echo "  --backup, -b         Backup configuration"
    echo "  --health, -h         Run health checks"
    echo "  --docker, -d         Prepare for Docker deployment"
    echo "  --all, -a           Run all operations"
    echo "  --help              Show this help message"
}

main() {
    log "🚀 Starting workspace automation script..."

    case "${1:-}" in
        --cleanup|-c)
            cleanup_python_cache
            cleanup_logs
            cleanup_temporary_files
            cleanup_broken_symlinks
            ;;
        --optimize|-o)
            optimize_workspace_structure
            ;;
        --update|-u)
            update_dependencies
            ;;
        --backup|-b)
            backup_configuration
            ;;
        --health|-h)
            run_health_checks
            ;;
        --docker|-d)
            prepare_for_docker
            ;;
        --all|-a)
            cleanup_python_cache
            cleanup_logs
            cleanup_temporary_files
            cleanup_broken_symlinks
            optimize_workspace_structure
            update_dependencies
            backup_configuration
            run_health_checks
            prepare_for_docker
            ;;
        --help|"")
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac

    log "🎉 Workspace automation completed successfully!"
}

# Change to workspace directory
cd "$WORKSPACE_ROOT" || exit 1

# Run main function
main "$@"
