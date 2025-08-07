# PowerShell Script to start the FastAPI backend server
Write-Host "Starting FastAPI Backend Server..." -ForegroundColor Green

# Get the directory where the script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to that directory
Set-Location $scriptPath

# Start the FastAPI backend server using uvicorn
try {
    python -m uvicorn backend:app --reload --host 127.0.0.1 --port 8000
}
catch {
    Write-Host "Error starting the backend server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure you have Python and the required packages installed:" -ForegroundColor Yellow
    Write-Host "pip install fastapi uvicorn" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
}
