@echo off
echo ======================================
echo    Starting FastAPI Backend Server
echo ======================================
echo.

cd %~dp0

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check for required packages
echo Checking for required packages...
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing FastAPI...
    pip install fastapi
)

python -c "import uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Uvicorn...
    pip install uvicorn
)

python -c "import pydantic" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pydantic...
    pip install pydantic
)

echo.
echo Starting the backend server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend:app --reload --host 127.0.0.1 --port 8000

:: This will only execute if uvicorn is stopped
echo.
echo Backend server stopped.
pause
