#!/bin/bash
"""
AGI MCP Setup Script

Sets up the Python virtual environment and installs dependencies for the AGI MCP server.
"""

set -e

echo "🚀 Setting up AGI Model Context Protocol Server..."
echo "================================================="

# Check if we're in the right directory
if [ ! -f "mcp-agi-server.py" ]; then
    echo "❌ Error: Please run this script from the ai-workspace directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "agi-venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv agi-venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source agi-venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing MCP AGI dependencies..."
pip install -r requirements-mcp.txt

# Test the server
echo "🧪 Testing AGI MCP Server..."
python simple-mcp-client.py

echo ""
echo "✅ AGI MCP Server setup complete!"
echo ""
echo "🎯 Usage:"
echo "   1. Activate environment: source agi-venv/bin/activate"
echo "   2. Start server: python mcp-agi-server.py"
echo "   3. Test with client: python simple-mcp-client.py"
echo ""
echo "📚 Available AGI Tools:"
echo "   • reasoning_engine - Advanced reasoning capabilities"
echo "   • multimodal_processor - Process multi-modal content"
echo "   • autonomous_task_executor - Execute autonomous tasks"
echo "   • knowledge_synthesizer - Synthesize knowledge from sources"
echo "   • creative_generator - Generate creative content"
echo "   • ethical_evaluator - Evaluate ethical scenarios"
echo "   • meta_cognitive_analyzer - Analyze thinking processes"
echo "   • system_status - Get system status"
echo ""
echo "🔗 The AGI MCP server is ready for client connections!"
