#!/bin/bash

echo "🚀 Starting AGI Chat System..."

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down AGI Chat System..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if backend is already running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "🧠 Starting AGI backend server..."
    cd agi-backend-server
    python3 main.py &
    BACKEND_PID=$!
    cd ..

    # Wait for backend to start
    echo "⏳ Waiting for backend to start..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Backend server is ready!"
            break
        fi
        sleep 1
    done
else
    echo "✅ Backend server already running"
fi

# Start AGI integration
echo "🔗 Starting AGI integration..."
python3 agi_chat_integration.py &
AGI_PID=$!

# Wait a moment
sleep 2

echo "🌐 Opening AGI Chat Interface..."

# Try to open in browser
if command -v xdg-open > /dev/null; then
    xdg-open "file://$(pwd)/agi-chat-interface.html"
elif command -v open > /dev/null; then
    open "file://$(pwd)/agi-chat-interface.html"
elif command -v start > /dev/null; then
    start "file://$(pwd)/agi-chat-interface.html"
else
    echo "📝 Please open this file in your browser:"
    echo "   file://$(pwd)/agi-chat-interface.html"
fi

echo ""
echo "✅ AGI Chat System is running!"
echo "📡 Backend API: http://localhost:8000"
echo "🤖 AGI Integration: Active"
echo "🌐 Chat Interface: Opened in browser"
echo ""
echo "💡 You can also:"
echo "   • Use @agi in VS Code chat (if extension is installed)"
echo "   • Access the API directly at http://localhost:8000"
echo "   • Run 'python3 test_agi_chat.py' to test the system"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for background processes
wait
