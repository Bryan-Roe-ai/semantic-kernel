@echo off
echo Starting AI Chat Application...
echo.

REM Check if Python is in the PATH
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH. Please install Python 3.8 or higher.
    echo Visit https://www.python.org/downloads/ to download and install Python.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Run the unified startup script
python start_chat_unified.py

REM If script execution fails
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running startup script. Please see error message above.
    pause
)
