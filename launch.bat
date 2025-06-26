@echo off
REM Unified Launcher Batch Script for Windows
REM Quick access to the Semantic Kernel workspace functionality

echo.
echo ================================
echo 🚀 SEMANTIC KERNEL UNIFIED LAUNCHER
echo ================================
echo.

REM Get script directory
set "WORKSPACE_ROOT=%~dp0"
set "UNIFIED_LAUNCHER=%WORKSPACE_ROOT%unified_launcher.py"

echo Workspace: %WORKSPACE_ROOT%
echo Making everything runnable from one place!
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Check for unified launcher
if not exist "%UNIFIED_LAUNCHER%" (
    echo ❌ Unified launcher not found!
    echo Looking for: %UNIFIED_LAUNCHER%
    pause
    exit /b 1
)

REM Run the unified launcher
if "%~1"=="" (
    echo 🚀 Starting interactive mode...
    python "%UNIFIED_LAUNCHER%"
) else if "%~1"=="help" (
    echo Usage: %~nx0 [command] [options]
    echo.
    echo Commands:
    echo   fix      - Fix all files in the workspace
    echo   setup    - Setup environment and dependencies
    echo   install  - Install dependencies only
    echo   list     - List all available scripts
    echo   help     - Show this help message
    echo.
    echo Examples:
    echo   %~nx0                    # Interactive mode
    echo   %~nx0 fix               # Fix all files
    echo   %~nx0 setup             # Full setup
    echo   %~nx0 --script demo     # Run specific script
) else (
    echo 🚀 Running: python unified_launcher.py %*
    python "%UNIFIED_LAUNCHER%" %*
)

echo.
echo 👋 Thanks for using Semantic Kernel!
pause
