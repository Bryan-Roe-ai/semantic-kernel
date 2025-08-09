#!/bin/bash
# AGI Backend Server Startup Script

echo "🧠 Starting AGI Backend Server..."

cd /workspaces/semantic-kernel/19-miscellaneous/agi-backend-server

# Kill any existing server on port 8080
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "🔄 Stopping existing server on port 8080..."
    kill $(lsof -t -i:8080) 2>/dev/null || true
    sleep 2
fi

echo "🚀 Starting new AGI backend server..."
python3 agi_backend.py &
SERVER_PID=$!

echo "✅ AGI Backend Server started with PID: $SERVER_PID"
echo "🌐 Server running at: http://localhost:8080"
echo "📡 Status endpoint: http://localhost:8080/api/status"
echo ""
echo "To stop the server, run: kill $SERVER_PID"
echo "To check status, run: curl http://localhost:8080/api/status"

# Wait a moment to let the server start
sleep 3

# Test the server
echo ""
echo "🧪 Testing server connection..."
if curl -s http://localhost:8080/api/status >/dev/null; then
    echo "✅ AGI Backend Server is running successfully!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Open the AGI website (if not already open)"
    echo "2. Click the ⚙️ Config button in the chat interface"
    echo "3. Ensure Server URL is set to: http://localhost:8080"
    echo "4. Click 'Test Connection' to verify"
    echo "5. Start chatting with the real AGI backend!"
else
    echo "❌ Server may not be responding yet. Please wait a moment and try again."
fi
