# LM Studio Chat Interface

This is a simple web interface that connects to LM Studio for AI chatting.

## Setup Instructions

1. **Prerequisites:**
   - Install Python (if not already installed)
   - Install LM Studio and have it running with the API server enabled
   - Install required Python packages:
     ```
     pip install fastapi uvicorn requests
     ```

2. **Start the Backend Server:**
   - Open a terminal in this directory
   - Run the command:
     ```
     python -m uvicorn backend:app --reload
     ```
   - Make sure LM Studio is running with the API server enabled on port 1234

3. **Access the Chat Interface:**
   - Open `ai-chat-launcher.html` or `simple-chat.html` in your web browser
   - The interface should connect to the backend automatically
   - If connection fails, click "Check Connection" button

## Features

- Multiple model selection (Phi, Llama, Mistral)
- Adjustable temperature and max tokens
- Optional system prompt for customizing responses
- Simple and clean chat interface

## Troubleshooting

- **Cannot connect to backend:** Ensure the Python backend is running on port 8000
- **AI not responding:** Verify LM Studio is running with API server enabled on port 1234
- **Strange responses:** Try a different model or adjust the temperature setting

## Environment Variables

- `LM_STUDIO_URL` - Set this to override the default LM Studio API URL (default: http://localhost:1234/v1/chat/completions)

## Files

- `backend.py` - FastAPI server that communicates with LM Studio
- `ai-chat-launcher.html` - Full-featured chat interface
- `simple-chat.html` - Minimal chat interface for testing
