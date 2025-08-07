# Enhanced start script for AI Chat Application

# Set window title
$Host.UI.RawUI.WindowTitle = "LM Studio Chat Launcher"

Write-Host "===============================" -ForegroundColor Cyan
Write-Host "  AI Chat Application Launcher" -ForegroundColor Cyan 
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = (python --version 2>&1)
    if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
        Write-Host "✅ Python $($Matches[1]) detected" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Python not found or not responding correctly" -ForegroundColor Red
        Write-Host "Please install Python 3.8 or higher from https://www.python.org/downloads/"
        Write-Host "Make sure to check 'Add Python to PATH' during installation."
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}
catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation."
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if LM Studio is running
Write-Host "Step 2: Checking if LM Studio is running..." -ForegroundColor Yellow
$lmStudioRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:1234/v1/models" -Method GET -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $lmStudioRunning = $true
        $modelsData = $response.Content | ConvertFrom-Json
        $modelCount = $modelsData.data.Count
        Write-Host "✅ LM Studio is running! API server detected with $modelCount models available." -ForegroundColor Green
    }
}
catch {
    $lmStudioRunning = $false
    Write-Host "⚠️ LM Studio API server not detected! Please:" -ForegroundColor Red
    Write-Host "  1. Start LM Studio" -ForegroundColor Red
    Write-Host "  2. Go to the 'API' tab" -ForegroundColor Red
    Write-Host "  3. Click 'Start server'" -ForegroundColor Red
    Write-Host ""
    $continue = Read-Host "Continue anyway? Chat functionality will be limited (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

Write-Host ""

# Ask if user wants to run setup first
Write-Host "Step 3: Checking dependencies..." -ForegroundColor Yellow
$runSetup = Read-Host "Run setup script to check/install dependencies? (Recommended for first use) (y/N)"

if ($runSetup -eq "y" -or $runSetup -eq "Y") {
    Write-Host "Running setup script..." -ForegroundColor Cyan
    python setup.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Setup script encountered an error" -ForegroundColor Red
        $continueAnyway = Read-Host "Continue anyway? (y/N)"
        if ($continueAnyway -ne "y" -and $continueAnyway -ne "Y") {
            exit 1
        }
    }
    else {
        Write-Host "✅ Setup completed successfully" -ForegroundColor Green
    }
    
    Write-Host ""
}

# Start the unified script which handles all startup logic
Write-Host "Step 4: Starting AI Chat Application..." -ForegroundColor Yellow
Write-Host "(Keep this window open to maintain the server connection)" -ForegroundColor Yellow

# Set environment variable for LM Studio URL
$env:LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

# Start the application using the unified script
python start_chat_unified.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error starting AI Chat Application. See error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "Step 3: Opening chat interface..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "simple-chat.html"
Write-Host "✅ Chat interface launched!" -ForegroundColor Green
Write-Host ""

Write-Host "Ready! Both backend and chat interface should be running." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to shut down the server when you're done." -ForegroundColor Yellow
Write-Host ""

try {
    # Keep script running until user presses Ctrl+C
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    # Cleanup when script is interrupted
    if ($backendProcess -ne $null -and -not $backendProcess.HasExited) {
        Write-Host "Shutting down backend server..." -ForegroundColor Yellow
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    }
}
