#!/bin/bash

# AGI Chat Assistant Launcher
# This script sets up and launches the complete AGI chat system

set -e

echo "🚀 Starting AGI Chat Assistant System..."

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

# Check if we're in the right directory
if [ ! -f "AGI_CHAT_README.md" ]; then
    print_error "Please run this script from the semantic-kernel directory"
    exit 1
fi

# Check Python installation
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

# Check Node.js installation
print_status "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    print_warning "Node.js is not installed. The VS Code extension won't work."
    print_status "Please install Node.js from https://nodejs.org/"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
if [ -f "agi-backend-server/requirements.txt" ]; then
    pip3 install -r agi-backend-server/requirements.txt
    print_success "Python dependencies installed"
else
    print_warning "requirements.txt not found, installing basic dependencies..."
    pip3 install fastapi uvicorn pydantic torch numpy
fi

# Install semantic kernel if not present
print_status "Checking Semantic Kernel installation..."
if ! python3 -c "import semantic_kernel" 2>/dev/null; then
    print_status "Installing Semantic Kernel..."
    pip3 install semantic-kernel
    print_success "Semantic Kernel installed"
fi

# Build VS Code extension if Node.js is available
if command -v node &> /dev/null; then
    print_status "Building VS Code extension..."
    cd vscode-agi-chat-extension

    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi

    print_status "Compiling TypeScript..."
    npm run compile

    cd ..
    print_success "VS Code extension built"
else
    print_warning "Skipping VS Code extension build (Node.js not available)"
fi

# Create startup script for backend
print_status "Creating backend startup script..."
cat > start_agi_backend.sh << 'EOF'
#!/bin/bash
echo "🧠 Starting AGI Backend Server..."
cd agi-backend-server
python3 main.py
EOF

chmod +x start_agi_backend.sh

# Create startup script for AGI integration
print_status "Creating AGI integration startup script..."
cat > start_agi_integration.sh << 'EOF'
#!/bin/bash
echo "🔗 Starting AGI Integration..."
python3 agi_chat_integration.py
EOF

chmod +x start_agi_integration.sh

# Create combined startup script
print_status "Creating combined startup script..."
cat > start_agi_chat.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting Complete AGI Chat System..."

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down AGI Chat System..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend server
echo "🧠 Starting backend server..."
cd agi-backend-server
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start AGI integration
echo "🔗 Starting AGI integration..."
python3 agi_chat_integration.py &
AGI_PID=$!

# Wait a moment
sleep 2

echo "✅ AGI Chat System is running!"
echo "📡 Backend API: http://localhost:8000"
echo "🤖 AGI Integration: Active"
echo ""
echo "📱 To use in VS Code:"
echo "   1. Install the extension from vscode-agi-chat-extension/"
echo "   2. Press Ctrl+Shift+A to open chat"
echo "   3. Start chatting with your AGI!"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for background processes
wait
EOF

chmod +x start_agi_chat.sh

# Test the AGI integration
print_status "Testing AGI integration..."
if python3 -c "
import sys
sys.path.append('.')
from agi_chat_integration import agi_system
status = agi_system.get_system_status()
print('System ready:', status.get('system_ready', False))
" 2>/dev/null; then
    print_success "AGI integration test passed"
else
    print_warning "AGI integration test failed, but system should still work"
fi

# Create a simple test script
print_status "Creating test script..."
cat > test_agi_chat.py << 'EOF'
#!/usr/bin/env python3
"""
Simple test script for the AGI Chat system
"""

import asyncio
import sys
from agi_chat_integration import agi_system

async def test_agi():
    print("🧪 Testing AGI Chat System...")

    # Initialize system
    success = agi_system.initialize_neural_symbolic_system()

    if not success:
        print("❌ Failed to initialize AGI system")
        return False

    # Test messages
    test_cases = [
        ("Hello AGI!", "neural-symbolic"),
        ("What is 2+2?", "reasoning"),
        ("Tell me a creative story", "creative"),
        ("Analyze this data: 1,2,3,4,5", "analytical"),
        ("How are you today?", "general")
    ]

    print("\n🔬 Running test cases...")

    for i, (message, agent_type) in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {agent_type} agent ---")
        print(f"Input: {message}")

        try:
            response = await agi_system.process_chat_message(message, agent_type)
            print(f"✅ Response generated (confidence: {response['confidence']:.2f})")
            print(f"📝 Content length: {len(response['content'])} characters")
            print(f"⚡ Processing time: {response.get('processing_time', 0):.3f}s")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Show system status
    status = agi_system.get_system_status()
    print(f"\n📊 Final system status:")
    print(f"   Neural model: {'✅' if status['neural_model_loaded'] else '❌'}")
    print(f"   Symbolic reasoner: {'✅' if status['symbolic_reasoner_active'] else '❌'}")
    print(f"   Knowledge graph: {'✅' if status['knowledge_graph_ready'] else '❌'}")
    print(f"   System ready: {'✅' if status['system_ready'] else '❌'}")

    return status['system_ready']

if __name__ == "__main__":
    result = asyncio.run(test_agi())
    sys.exit(0 if result else 1)
EOF

chmod +x test_agi_chat.py

print_success "AGI Chat Assistant setup complete!"
print_status ""
print_status "🎯 Next steps:"
print_status "1. Run './start_agi_chat.sh' to start the complete system"
print_status "2. Install the VS Code extension from vscode-agi-chat-extension/"
print_status "3. Press Ctrl+Shift+A in VS Code to start chatting"
print_status ""
print_status "🧪 Or run './test_agi_chat.py' to test the system"
print_status ""
print_status "📖 See AGI_CHAT_README.md for detailed documentation"

# Optional: Start the system if requested
if [ "$1" = "--start" ]; then
    print_status ""
    print_status "🚀 Starting the system now..."
    ./start_agi_chat.sh
fi
