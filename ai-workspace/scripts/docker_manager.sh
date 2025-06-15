#!/bin/bash
# Docker Management Script for AI Workspace
# Handles Docker build, deployment, and management operations

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
WORKSPACE_ROOT="/workspaces/semantic-kernel/ai-workspace"
IMAGE_NAME="semantic-kernel-ai-workspace"
CONTAINER_NAME="ai-workspace"

# Logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# =============================================================================
# Docker Operations
# =============================================================================

build_image() {
    log "🏗️  Building Docker image..."
    
    cd "$WORKSPACE_ROOT"
    
    # Run cleanup first
    ./scripts/cleanup_and_automate.sh --docker
    
    # Build the image
    docker build -t "$IMAGE_NAME:latest" -t "$IMAGE_NAME:$(date +%Y%m%d)" .
    
    # Show image info
    docker images "$IMAGE_NAME"
    
    log "✅ Docker image built successfully"
}

run_container() {
    log "🚀 Starting Docker container..."
    
    # Stop existing container if running
    stop_container 2>/dev/null || true
    
    # Run new container
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p 8000:8000 \
        -p 8888:8888 \
        -p 3000:3000 \
        -p 80:80 \
        -v ai_workspace_data:/app/data \
        -v ai_workspace_models:/app/models \
        -v ai_workspace_logs:/app/logs \
        --env-file .env \
        --restart unless-stopped \
        "$IMAGE_NAME:latest"
    
    log "✅ Container started successfully"
    show_container_info
}

run_with_compose() {
    log "🐳 Starting with Docker Compose..."
    
    cd "$WORKSPACE_ROOT"
    
    # Stop any existing services
    docker-compose down 2>/dev/null || true
    
    # Start services
    docker-compose up -d
    
    log "✅ Docker Compose services started"
    show_compose_status
}

stop_container() {
    log "🛑 Stopping Docker container..."
    
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    
    log "✅ Container stopped"
}

stop_compose() {
    log "🛑 Stopping Docker Compose services..."
    
    cd "$WORKSPACE_ROOT"
    docker-compose down
    
    log "✅ Docker Compose services stopped"
}

cleanup_docker() {
    log "🧹 Cleaning up Docker resources..."
    
    # Stop and remove containers
    stop_container 2>/dev/null || true
    stop_compose 2>/dev/null || true
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes (be careful with this)
    read -p "Remove unused Docker volumes? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
    fi
    
    log "✅ Docker cleanup completed"
}

# =============================================================================
# Monitoring and Debugging
# =============================================================================

show_container_info() {
    log "📊 Container Information:"
    echo
    docker ps -f "name=$CONTAINER_NAME"
    echo
    log "🌐 Service URLs:"
    echo "  - Main Portal: http://localhost"
    echo "  - Jupyter Lab: http://localhost/jupyter"
    echo "  - Backend API: http://localhost/api"
    echo "  - Direct Jupyter: http://localhost:8888"
    echo "  - Direct Backend: http://localhost:8000"
    echo "  - Direct Web App: http://localhost:3000"
}

show_compose_status() {
    log "📊 Docker Compose Status:"
    echo
    cd "$WORKSPACE_ROOT"
    docker-compose ps
    echo
    log "🌐 Service URLs:"
    echo "  - AI Workspace: http://localhost"
    echo "  - Jupyter Lab: http://localhost:8888"
    echo "  - Backend API: http://localhost:8000"
    echo "  - Web Interface: http://localhost:3000"
    echo "  - ChromaDB: http://localhost:8001"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3001"
}

show_logs() {
    local service="${1:-$CONTAINER_NAME}"
    
    log "📝 Showing logs for: $service"
    
    if docker-compose ps "$service" &>/dev/null; then
        cd "$WORKSPACE_ROOT"
        docker-compose logs -f "$service"
    else
        docker logs -f "$service"
    fi
}

exec_into_container() {
    local service="${1:-$CONTAINER_NAME}"
    
    log "🔧 Executing into container: $service"
    
    if docker-compose ps "$service" &>/dev/null; then
        cd "$WORKSPACE_ROOT"
        docker-compose exec "$service" /bin/bash
    else
        docker exec -it "$service" /bin/bash
    fi
}

health_check() {
    log "🔍 Running health checks..."
    
    # Check if services are running
    if docker ps -f "name=$CONTAINER_NAME" --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        log "✅ Container is running"
        
        # Check service endpoints
        curl -s http://localhost/health >/dev/null && log "✅ Main portal is responding" || log_warn "❌ Main portal not responding"
        curl -s http://localhost:8000/health >/dev/null && log "✅ Backend API is responding" || log_warn "❌ Backend API not responding"
        curl -s http://localhost:8888 >/dev/null && log "✅ Jupyter Lab is responding" || log_warn "❌ Jupyter Lab not responding"
    else
        log_error "❌ Container is not running"
        return 1
    fi
}

# =============================================================================
# Development Helpers
# =============================================================================

dev_mode() {
    log "🛠️  Starting in development mode..."
    
    cd "$WORKSPACE_ROOT"
    
    # Stop production containers
    docker-compose down 2>/dev/null || true
    
    # Start with development overrides
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    
    log "✅ Development mode started"
    show_compose_status
}

production_deploy() {
    log "🚀 Deploying to production..."
    
    # Build optimized image
    build_image
    
    # Start production services
    run_with_compose
    
    # Run health checks
    sleep 10
    health_check
    
    log "✅ Production deployment completed"
}

# =============================================================================
# Main Interface
# =============================================================================

show_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  build                Build Docker image"
    echo "  run                  Run single container"
    echo "  compose              Start with Docker Compose"
    echo "  stop                 Stop containers"
    echo "  restart              Restart containers"
    echo "  logs [service]       Show logs for service"
    echo "  exec [service]       Execute into container"
    echo "  health               Run health checks"
    echo "  cleanup              Clean up Docker resources"
    echo "  dev                  Start in development mode"
    echo "  deploy               Deploy to production"
    echo "  status               Show status information"
    echo ""
    echo "Examples:"
    echo "  $0 build            # Build the Docker image"
    echo "  $0 compose          # Start all services"
    echo "  $0 logs jupyter     # Show Jupyter logs"
    echo "  $0 exec ai-workspace # Shell into main container"
}

main() {
    case "${1:-}" in
        build)
            build_image
            ;;
        run)
            run_container
            ;;
        compose)
            run_with_compose
            ;;
        stop)
            stop_compose
            stop_container
            ;;
        restart)
            stop_compose
            stop_container
            run_with_compose
            ;;
        logs)
            show_logs "${2:-}"
            ;;
        exec)
            exec_into_container "${2:-}"
            ;;
        health)
            health_check
            ;;
        cleanup)
            cleanup_docker
            ;;
        dev)
            dev_mode
            ;;
        deploy)
            production_deploy
            ;;
        status)
            show_compose_status
            ;;
        ""|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Change to workspace directory
cd "$WORKSPACE_ROOT" || exit 1

# Run main function
main "$@"
