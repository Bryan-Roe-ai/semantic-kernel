#!/bin/bash

# Semantic Kernel Environment Setup Script
# This script helps you set up environment files for different parts of the project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to check if a file exists
file_exists() {
    [ -f "$1" ]
}

# Function to create environment file from template
create_env_file() {
    local template_file="$1"
    local target_file="$2"
    local description="$3"

    if file_exists "$target_file"; then
        print_warning "$target_file already exists. Skipping..."
        return 0
    fi

    if file_exists "$template_file"; then
        cp "$template_file" "$target_file"
        print_success "Created $target_file from template ($description)"
        return 0
    else
        print_error "Template file $template_file not found"
        return 1
    fi
}

print_status "🚀 Setting up Semantic Kernel environment files..."
echo

# Main project environment
print_status "Setting up main project environment..."
create_env_file ".env.template" ".env.local" "Main project configuration"

# Python environment
print_status "Setting up Python environment..."
create_env_file "python.env.template" "python.env" "Python-specific configuration"

# .NET appsettings
print_status "Setting up .NET configuration..."
create_env_file "appsettings.template.json" "appsettings.Development.json" ".NET development configuration"

# Python core implementation
if [ -d "01-core-implementations/python" ]; then
    print_status "Setting up Python core implementation environment..."
    cd "01-core-implementations/python"
    if [ -f ".env.example" ]; then
        create_env_file ".env.example" ".env" "Python core implementation"
    fi
    cd - > /dev/null
fi

# Python samples
if [ -d "01-core-implementations/python/samples/getting_started" ]; then
    print_status "Setting up Python samples environment..."
    cd "01-core-implementations/python/samples/getting_started"
    if [ -f ".env.example" ]; then
        create_env_file ".env.example" ".env" "Python samples"
    fi
    cd - > /dev/null
fi

echo
print_status "📝 Environment files created. Next steps:"
echo
echo "1. Edit .env.local with your API keys and configuration"
echo "2. For Python development, also edit python.env"
echo "3. For .NET development, edit appsettings.Development.json"
echo
print_warning "⚠️  IMPORTANT: Never commit files containing real API keys to version control!"
echo
print_status "🔐 Required API keys to get started:"
echo
echo "  • OpenAI API Key (easiest to get started):"
echo "    → Sign up at https://platform.openai.com/"
echo "    → Go to API Keys section and create a new key"
echo "    → Add to OPENAI_API_KEY in your .env.local"
echo
echo "  • OR Azure OpenAI (for enterprise):"
echo "    → Set up Azure OpenAI service in Azure portal"
echo "    → Get endpoint, API key, and deployment names"
echo "    → Add to AZURE_OPENAI_* variables in your .env.local"
echo
print_status "📚 For more configuration options, see:"
echo "  • .env.template - Full configuration reference"
echo "  • python.env.template - Python-specific options"
echo "  • appsettings.template.json - .NET configuration"
echo
print_success "✅ Environment setup complete!"
