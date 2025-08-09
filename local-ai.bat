@echo off
REM Local AI Quick Launch Script for Windows
REM
REM Copyright (c) 2025 Bryan Roe
REM Licensed under the MIT License
REM
REM This file is part of the Semantic Kernel - Advanced AI Development Framework.
REM Original work by Bryan Roe.
REM
REM Author: Bryan Roe
REM Created: 2025
REM License: MIT

setlocal EnableDelayedExpansion

REM Configuration
set "WORKSPACE_ROOT=%~dp0"
set "BACKEND_DIR=%WORKSPACE_ROOT%19-miscellaneous\src"
set "FRONTEND_DIR=%WORKSPACE_ROOT%07-resources\public"
set "LM_STUDIO_URL=http://localhost:1234"
set "BACKEND_URL=http://localhost:8000"

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                           🚀 LOCAL AI QUICK LAUNCH 🚀                        ║
echo ║                        Semantic Kernel Local AI System                      ║
echo ║                             by Bryan Roe (2025)                            ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

if "%1"=="stop" goto stop
if "%1"=="status" goto status
if "%1"=="help" goto help

:start
echo 🚀 Starting Local AI System...
echo.

echo 🔍 Checking LM Studio...
curl -s %LM_STUDIO_URL%/v1/models >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ LM Studio is running
) else (
    echo   ✗ LM Studio is not running
    echo   💡 Please start LM Studio and enable the API server
    echo.
    pause
    goto end
)

echo.
echo 📦 Installing dependencies...
pip install fastapi uvicorn requests pydantic starlette >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Dependencies installed
) else (
    echo   ✗ Failed to install dependencies
    pause
    goto end
)

echo.
echo ⚙️ Setting up environment...

REM Create directories
if not exist "%BACKEND_DIR%\plugins" mkdir "%BACKEND_DIR%\plugins"
if not exist "%BACKEND_DIR%\uploads" mkdir "%BACKEND_DIR%\uploads"

REM Create .env file
echo LM_STUDIO_URL="%LM_STUDIO_URL%/v1/chat/completions" > "%BACKEND_DIR%\.env"
echo   ✓ Environment configured

echo.
echo 🚀 Starting backend server...

REM Check if backend is already running
curl -s %BACKEND_URL%/ping >nul 2>&1
if %errorlevel% equ 0 (
    echo   ℹ Backend server is already running
) else (
    REM Start backend
    cd /d "%BACKEND_DIR%"
    start /b python -m uvicorn backend:app --reload --host 127.0.0.1 --port 8000 > backend.log 2>&1

    echo   ⏳ Waiting for backend to start...
    timeout /t 5 /nobreak >nul

    curl -s %BACKEND_URL%/ping >nul 2>&1
    if %errorlevel% equ 0 (
        echo   ✓ Backend server started successfully
    ) else (
        echo   ✗ Backend server failed to start
        echo   📋 Check backend.log for details
        pause
        goto end
    )
)

echo.
echo 🌐 Opening chat interface...
start "" "file:///%FRONTEND_DIR%/ai-chat-launcher.html"
echo   ✓ Chat interface opened in browser

echo.
echo 🎉 Local AI system is ready!
echo.
echo Available interfaces:
echo   • Advanced Chat: file:///%FRONTEND_DIR%/ai-chat-launcher.html
echo   • Plugin Chat:   file:///%FRONTEND_DIR%/plugin-chat.html
echo   • Simple Chat:   file:///%FRONTEND_DIR%/simple-chat.html
echo.
echo API Documentation: %BACKEND_URL%/docs
echo Backend Logs: %BACKEND_DIR%\backend.log
echo.
echo To stop the system, run: %~nx0 stop
echo.
pause
goto end

:stop
echo 🛑 Stopping backend server...
taskkill /f /im python.exe /fi "WINDOWTITLE eq *uvicorn*" >nul 2>&1
echo   ✓ Backend processes stopped
pause
goto end

:status
echo System Status:
echo.

echo System Dependencies:
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Python
) else (
    echo   ✗ Python (not found)
)

pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ pip
) else (
    echo   ✗ pip (not found)
)

echo.
echo AI Providers:
curl -s %LM_STUDIO_URL%/v1/models >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ LM Studio is running
) else (
    echo   ✗ LM Studio is not running
)

echo.
echo Backend Service:
curl -s %BACKEND_URL%/ping >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Backend server is running
) else (
    echo   ✗ Backend server is not running
)

echo.
pause
goto end

:help
echo Usage: %~nx0 [COMMAND]
echo.
echo Commands:
echo   start     - Start the local AI system (default)
echo   stop      - Stop the backend server
echo   status    - Show system status
echo   help      - Show this help message
echo.
echo Examples:
echo   %~nx0 start    # Start everything and open chat interface
echo   %~nx0 stop     # Stop the backend server
echo   %~nx0 status   # Check if everything is working
echo.
pause
goto end

:end
endlocal
