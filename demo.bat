@echo off
echo Starting LM Studio Chat Server with Plugin Support...

echo.
echo 1. Checking Python installation...
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python not found! Please install Python 3.9 or higher.
    exit /b 1
)

echo.
echo 2. Installing required packages...
pip install -q fastapi uvicorn requests matplotlib numpy

echo.
echo 3. Creating test data (if needed)...
if not exist "uploads\employees.csv" (
    mkdir uploads 2>NUL
)

echo.
echo 4. Starting the backend server...
start "LM Studio Chat Backend" cmd /c python -m uvicorn backend:app --reload

echo.
echo 5. Waiting for server to start...
timeout /t 5 /nobreak > NUL

echo.
echo 6. Opening the plugin chat interface...
start "" "plugin-chat.html"

echo.
echo Server started and interface launched!
echo.
echo TIPS:
echo - Make sure LM Studio API server is running at http://localhost:1234
echo - Upload a file by clicking the paperclip icon (automatic analysis will be performed)
echo - Click on a file in the sidebar to see its analysis
echo - Try commands like:
echo   - "Analyze the employees.csv file"
echo   - "Generate a bar chart from employees.csv with city as x-axis and salary as y-axis"
echo   - "Parse the company.json file and extract the products"
echo   - "Summarize the text from the uploaded file"
echo.
echo Press Ctrl+C to stop the server when finished
echo.

pause
