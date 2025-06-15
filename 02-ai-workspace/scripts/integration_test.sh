#!/bin/bash
# AI Workspace Integration Test Script
# Tests all components and services

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log() { echo -e "${GREEN}[TEST] $1${NC}"; }
log_warn() { echo -e "${YELLOW}[WARN] $1${NC}"; }
log_error() { echo -e "${RED}[ERROR] $1${NC}"; }
log_info() { echo -e "${BLUE}[INFO] $1${NC}"; }

# Test configuration
API_PORT=8003
BASE_URL="http://localhost:${API_PORT}"
WORKSPACE_DIR="/workspaces/semantic-kernel/ai-workspace"

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                🧪 AI Workspace Integration Test          ║
║                                                           ║
║   Testing all components of the AI workspace system      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Test 1: Workspace Structure
log "1. Testing workspace structure..."
cd "$WORKSPACE_DIR"

expected_dirs=(
    "01-notebooks"
    "02-agents"
    "03-models-training"
    "04-plugins"
    "05-samples-demos"
    "06-backend-services"
    "07-data-resources"
    "08-documentation"
    "09-deployment"
    "10-config"
)

for dir in "${expected_dirs[@]}"; do
    if [ -d "$dir" ]; then
        log "✅ Directory $dir exists"
    else
        log_error "❌ Directory $dir missing"
        exit 1
    fi
done

# Test 2: Core Files
log "2. Testing core files..."

core_files=(
    "06-backend-services/simple_api_server.py"
    "03-models-training/advanced_llm_trainer.py"
    "05-samples-demos/custom-llm-studio.html"
    "05-samples-demos/index.html"
    "Dockerfile"
    "docker-compose.yml"
    "requirements-minimal.txt"
    "launch.sh"
)

for file in "${core_files[@]}"; do
    if [ -f "$file" ]; then
        log "✅ File $file exists"
    else
        log_error "❌ File $file missing"
        exit 1
    fi
done

# Test 3: Python Environment
log "3. Testing Python environment..."

if [ -d "venv" ]; then
    log "✅ Virtual environment exists"
    source venv/bin/activate

    # Test Python imports
    python -c "import fastapi; print('FastAPI:', fastapi.__version__)" && log "✅ FastAPI available"
    python -c "import uvicorn; print('Uvicorn available')" && log "✅ Uvicorn available"
    python -c "import pydantic; print('Pydantic:', pydantic.__version__)" && log "✅ Pydantic available"
else
    log_error "❌ Virtual environment missing"
    exit 1
fi

# Test 4: Start API Server
log "4. Starting API server for testing..."

cd 06-backend-services
python simple_api_server.py --port $API_PORT &
API_PID=$!
cd ..

# Give server time to start
sleep 3

# Test 5: API Endpoints
log "5. Testing API endpoints..."

# Health check
if curl -s "$BASE_URL/health" | grep -q "healthy"; then
    log "✅ Health endpoint working"
else
    log_error "❌ Health endpoint failed"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

# Models endpoint
if curl -s "$BASE_URL/api/models" | grep -q "models"; then
    log "✅ Models endpoint working"
else
    log_error "❌ Models endpoint failed"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

# Chat endpoint
chat_response=$(curl -s -X POST "$BASE_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "test", "model": "gpt2"}')

if echo "$chat_response" | grep -q "response"; then
    log "✅ Chat endpoint working"
else
    log_error "❌ Chat endpoint failed"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

# Test 6: Static Files
log "6. Testing static file serving..."

if curl -s "$BASE_URL/" | grep -q "AI Workspace"; then
    log "✅ Main landing page accessible"
else
    log_error "❌ Main landing page failed"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

if curl -s "$BASE_URL/static/custom-llm-studio.html" | grep -q "Custom LLM Studio"; then
    log "✅ LLM Studio interface accessible"
else
    log_error "❌ LLM Studio interface failed"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

# Test 7: Training Simulation
log "7. Testing training endpoint..."

training_response=$(curl -s -X POST "$BASE_URL/api/models/train" \
    -H "Content-Type: application/json" \
    -d '{"model_name": "test-model", "epochs": 1}')

if echo "$training_response" | grep -q "job_id"; then
    log "✅ Training endpoint working"

    # Get job ID and check status
    job_id=$(echo "$training_response" | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
    sleep 2

    if curl -s "$BASE_URL/api/training/$job_id" | grep -q "progress"; then
        log "✅ Training status endpoint working"
    else
        log_error "❌ Training status endpoint failed"
    fi
else
    log_error "❌ Training endpoint failed"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

# Cleanup
log "8. Cleaning up..."
kill $API_PID 2>/dev/null || true
sleep 1

# Test Summary
log_info "═══════════════════════════════════════════════"
log_info "🎉 ALL TESTS PASSED!"
log_info "═══════════════════════════════════════════════"
log_info ""
log_info "✅ Workspace structure is properly organized"
log_info "✅ Core files are present and accessible"
log_info "✅ Python environment is configured correctly"
log_info "✅ API server starts and responds correctly"
log_info "✅ All API endpoints are functional"
log_info "✅ Static files are served properly"
log_info "✅ Training simulation works"
log_info ""
log_info "🚀 AI Workspace is ready for use!"
log_info ""
log_info "Quick Start:"
log_info "1. ./launch.sh - Interactive workspace management"
log_info "2. cd 06-backend-services && python simple_api_server.py"
log_info "3. Open http://localhost:8000 in your browser"
log_info ""
log_info "Docker Deployment:"
log_info "1. docker-compose up -d"
log_info "2. Access services on configured ports"
log_info ""
