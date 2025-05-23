# Set window title
$Host.UI.RawUI.WindowTitle = "LM Studio Chat Launcher"

Write-Host "Starting AI Chat with LM Studio..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Checking if LM Studio is running..." -ForegroundColor Yellow
$lmStudioRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:1234/v1/models" -Method GET -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $lmStudioRunning = $true
    }
}
catch {
    $lmStudioRunning = $false
}

if (-not $lmStudioRunning) {
    Write-Host "LM Studio is NOT running! Please:" -ForegroundColor Red
    Write-Host "  1. Start LM Studio" -ForegroundColor Red
    Write-Host "  2. Go to the 'API' tab" -ForegroundColor Red
    Write-Host "  3. Click 'Start server'" -ForegroundColor Red
    Write-Host "  4. Run this script again" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ LM Studio is running! API server detected." -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Starting backend server..." -ForegroundColor Yellow
Write-Host "(Keep this window open to maintain the server connection)" -ForegroundColor Yellow
$env:LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

# Start the backend server in a new process
$backendProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "backend:app", "--reload" -PassThru -NoNewWindow
Write-Host "✅ Backend starting on http://localhost:8000" -ForegroundColor Green
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
