#!/bin/bash
# Quick Start AI Development Environment
echo "🚀 Starting AI Development Environment..."

# Activate virtual environment
echo "🔧 Activating Python virtual environment..."
source ai_env/bin/activate

# Start MCP server in background
echo "📡 Starting MCP server..."
python3 mcp_server.py &
MCP_PID=$!

# Open VS Code with AI tasks
echo "💻 Opening VS Code..."
code .

# Wait for user input to stop
echo "Press any key to stop MCP server..."
read -n 1

# Cleanup
echo "🛑 Stopping MCP server..."
kill $MCP_PID

echo "✅ Environment stopped."
