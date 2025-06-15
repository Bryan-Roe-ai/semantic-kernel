#!/bin/bash
# Docker Entrypoint Script for AI Workspace
# Handles initialization, cleanup, and service startup

set -e

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# ASCII Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🤖 AI WORKSPACE DOCKER CONTAINER STARTING 🤖         ║
║                                                           ║
║  Semantic Kernel • Automated • Production Ready          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Environment setup
export PYTHONPATH="/app:$PYTHONPATH"
export AI_WORKSPACE_ROOT="/app"

log "🚀 Starting AI Workspace Container Initialization..."

# =============================================================================
# Cleanup and Preparation
# =============================================================================
cleanup_workspace() {
    log "🧹 Cleaning up workspace..."
    
    # Remove broken symlinks
    find /app -type l -! -exec test -e {} \; -delete 2>/dev/null || true
    
    # Clean up temporary files
    find /app -name "*.pyc" -delete 2>/dev/null || true
    find /app -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find /app -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Create necessary directories
    mkdir -p /app/logs /app/data /app/uploads /app/models /app/cache
    
    # Set proper permissions
    chmod -R 755 /app/scripts 2>/dev/null || true
    chmod +x /app/*.sh 2>/dev/null || true
    
    log "✅ Workspace cleanup completed"
}

# =============================================================================
# Environment Configuration
# =============================================================================
setup_environment() {
    log "⚙️  Setting up environment configuration..."
    
    # Create .env file if it doesn't exist
    if [ ! -f "/app/.env" ] && [ -f "/app/.env.template" ]; then
        cp /app/.env.template /app/.env
        log "📝 Created .env file from template"
    fi
    
    # Set default environment variables if not provided
    export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
    export AZURE_OPENAI_API_KEY="${AZURE_OPENAI_API_KEY:-}"
    export AZURE_OPENAI_ENDPOINT="${AZURE_OPENAI_ENDPOINT:-}"
    export DEBUG="${DEBUG:-true}"
    export LOG_LEVEL="${LOG_LEVEL:-INFO}"
    export ENVIRONMENT="${ENVIRONMENT:-production}"
    
    # Configure Jupyter
    export JUPYTER_CONFIG_DIR="/app/.jupyter"
    mkdir -p "$JUPYTER_CONFIG_DIR"
    
    # Configure Python path
    export PYTHONPATH="/app:$PYTHONPATH"
    
    log "✅ Environment configuration completed"
}

# =============================================================================
# Service Health Checks
# =============================================================================
check_services() {
    log "🔍 Performing service health checks..."
    
    # Check Python environment
    python --version
    pip list --format=freeze | head -5
    
    # Check Semantic Kernel installation
    python -c "import semantic_kernel; print(f'Semantic Kernel version: {semantic_kernel.__version__}')" 2>/dev/null || log_warn "Semantic Kernel not available"
    
    # Check GPU availability
    python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')" 2>/dev/null || log_warn "PyTorch/CUDA not available"
    
    log "✅ Health checks completed"
}

# =============================================================================
# Initialize AI Workspace
# =============================================================================
initialize_workspace() {
    log "🔧 Initializing AI workspace..."
    
    # Run workspace organization if needed
    if [ -f "/app/organize_files.py" ]; then
        python /app/organize_files.py || log_warn "Workspace organization failed"
    fi
    
    # Setup workspace manager
    if [ -f "/app/ai_workspace_manager.py" ]; then
        python /app/ai_workspace_manager.py --setup || log_warn "Workspace setup failed"
    fi
    
    log "✅ Workspace initialization completed"
}

# =============================================================================
# Service Startup
# =============================================================================
start_services() {
    log "🚀 Starting services..."
    
    # Start Nginx (reverse proxy)
    sudo service nginx start || log_warn "Nginx start failed"
    
    # The actual services will be started by supervisord
    log "✅ Base services started, supervisord will handle the rest"
}

# =============================================================================
# Main Execution
# =============================================================================
main() {
    log "🎯 Starting main initialization process..."
    
    cleanup_workspace
    setup_environment
    check_services
    initialize_workspace
    start_services
    
    log "🎉 AI Workspace container initialization complete!"
    log "🌐 Services available on:"
    log "   - Jupyter Lab: http://localhost:8888"
    log "   - Backend API: http://localhost:8000"
    log "   - Web Interface: http://localhost:3000"
    log "   - Main Portal: http://localhost:80"
    
    # Execute the command passed to docker run
    exec "$@"
}

# =============================================================================
# Signal Handlers
# =============================================================================
cleanup_on_exit() {
    log "🛑 Shutting down AI workspace..."
    # Graceful shutdown logic here
    exit 0
}

trap cleanup_on_exit SIGTERM SIGINT

# Run main function
main "$@"
