@echo off
echo Starting AI Chat with LM Studio...
echo.
echo Step 1: Checking if LM Studio is running...
curl -s http://localhost:1234/v1/models > nul 2>&1
if %errorlevel% neq 0 (
    echo LM Studio is NOT running! Please:
    echo   1. Start LM Studio
    echo   2. Go to the "API" tab
    echo   3. Click "Start server"
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)
echo LM Studio is running! API server detected.
echo.

echo Step 2: Starting backend server...
echo (Keep this window open to maintain the server connection)
set LM_STUDIO_URL=http://localhost:1234/v1/chat/completions
start /b python -m uvicorn backend:app --reload
echo Backend starting on http://localhost:8000
echo.

echo Step 3: Opening chat interface...
timeout /t 2 > nul
start "" simple-chat.html
echo.

echo Ready! Both backend and chat interface should be running.
echo.
echo Press Ctrl+C to shut down the server when you're done.
echo.
pause
