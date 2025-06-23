#!/bin/bash
# Quick Setup Script for Local AGI Agents

set -e

echo "🚀 Setting up Local AGI Agents..."
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "local_agent_launcher.py" ]; then
    print_error "Please run this script from the semantic-kernel directory"
    exit 1
fi

print_status "Checking Python environment..."
if [ ! -f ".venv/bin/python" ]; then
    print_error "Python virtual environment not found. Please activate your environment first."
    exit 1
fi

print_status "Checking semantic-kernel installation..."
if ! .venv/bin/python -c "import semantic_kernel" 2>/dev/null; then
    print_error "Semantic Kernel not found in environment"
    exit 1
fi

print_success "Environment check passed!"

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file for configuration..."
    cat > .env << 'EOL'
# AI Service Configuration
# Uncomment and fill in your preferred AI service

# OpenAI Configuration
# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_CHAT_MODEL_ID=gpt-4
# OPENAI_ORG_ID=your_org_id_here

# Azure OpenAI Configuration
# AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4
# AZURE_OPENAI_API_VERSION=2024-02-01

# Global LLM Service (OpenAI, AzureOpenAI, or HuggingFace)
GLOBAL_LLM_SERVICE=OpenAI

# AGI System Configuration
AGI_LOG_LEVEL=INFO
AGI_MAX_CONCURRENT_OPERATIONS=5
EOL
    print_success "Created .env file. Please edit it with your API keys."
fi

# Make launcher executable
chmod +x local_agent_launcher.py

print_success "Setup complete!"
echo ""
echo "🎯 Next Steps:"
echo "1. Edit .env file with your AI service credentials"
echo "2. Run: python local_agent_launcher.py"
echo "3. Or use quick commands:"
echo "   - List agents: python local_agent_launcher.py list"
echo "   - Start all: python local_agent_launcher.py start"
echo "   - Stop all: python local_agent_launcher.py stop"
echo "   - Check status: python local_agent_launcher.py status"
echo ""
echo "📚 Available AGI Systems:"
echo "   • AGI File Update System"
echo "   • Optimized AGI System"
echo "   • Ultra-Efficient AGI System"
echo "   • AGI Chat Integration"
echo "   • Performance Monitor"
echo "   • Semantic Kernel Agents"
echo ""
