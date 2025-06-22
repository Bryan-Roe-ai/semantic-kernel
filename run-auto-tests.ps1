#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Semantic Kernel Automated Test Runner

.DESCRIPTION
    This script provides easy access to run automated tests across the Semantic Kernel workspace.
    It supports .NET, Python, and JavaScript/TypeScript test projects.

.PARAMETER Command
    The command to execute: discover, run-all, run, watch

.PARAMETER Pattern
    Pattern to match test projects (for 'run' command)

.PARAMETER Verbose
    Enable verbose logging

.PARAMETER Parallel
    Enable parallel execution (default: true)

.PARAMETER Coverage
    Collect code coverage

.PARAMETER Filter
    Test filter pattern

.PARAMETER Timeout
    Timeout in minutes per project (default: 10)

.EXAMPLE
    ./run-auto-tests.ps1 discover
    Discover all test projects

.EXAMPLE
    ./run-auto-tests.ps1 run-all --verbose
    Run all tests with verbose output

.EXAMPLE
    ./run-auto-tests.ps1 run "Unit" --coverage
    Run all unit tests with coverage

.EXAMPLE
    ./run-auto-tests.ps1 watch --pattern "OpenAI"
    Watch mode for OpenAI-related tests
#>

param(
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet("discover", "run-all", "run", "watch")]
    [string]$Command,
    
    [Parameter(Position = 1)]
    [string]$Pattern = "",
    
    [switch]$Verbose,
    [switch]$Parallel = $true,
    [switch]$Coverage,
    [string]$Filter = "",
    [int]$Timeout = 10
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = Split-Path -Parent $ScriptDir

Write-Host "🧪 Semantic Kernel Auto Test Runner" -ForegroundColor Cyan
Write-Host "Working Directory: $WorkspaceRoot" -ForegroundColor Gray

# Check if we're in the right directory
if (-not (Test-Path (Join-Path $WorkspaceRoot "LICENSE"))) {
    Write-Error "❌ Not in Semantic Kernel workspace root. Please run from the correct directory."
    exit 1
}

# Function to run .NET tests
function Invoke-DotNetTests {
    param($ProjectPattern = "*", $TestOptions = @{})
    
    Write-Host "🔍 Discovering .NET test projects..." -ForegroundColor Yellow
    
    $testProjects = Get-ChildItem -Path (Join-Path $WorkspaceRoot "01-core-implementations/dotnet") -Recurse -Filter "*Tests.csproj"
    
    if ($ProjectPattern -ne "*") {
        $testProjects = $testProjects | Where-Object { $_.Name -like "*$ProjectPattern*" }
    }
    
    Write-Host "📊 Found $($testProjects.Count) .NET test projects" -ForegroundColor Green
    
    foreach ($project in $testProjects) {
        Write-Host "▶️ Running: $($project.BaseName)" -ForegroundColor Blue
        
        $args = @("test", $project.FullName, "--configuration", "Release", "--logger", "console;verbosity=normal")
        
        if ($TestOptions.Coverage) {
            $args += "--collect:XPlat Code Coverage"
        }
        
        if ($TestOptions.Filter) {
            $args += "--filter", $TestOptions.Filter
        }
        
        if ($TestOptions.Parallel) {
            $args += "--parallel"
        }
        
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        try {
            & dotnet @args
            $exitCode = $LASTEXITCODE
            $stopwatch.Stop()
            
            if ($exitCode -eq 0) {
                Write-Host "✅ $($project.BaseName) PASSED ($($stopwatch.Elapsed.ToString("mm\:ss")))" -ForegroundColor Green
            } else {
                Write-Host "❌ $($project.BaseName) FAILED ($($stopwatch.Elapsed.ToString("mm\:ss")))" -ForegroundColor Red
            }
        }
        catch {
            $stopwatch.Stop()
            Write-Host "💥 $($project.BaseName) ERROR: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Function to run Python tests
function Invoke-PythonTests {
    param($TestType = "all", $TestOptions = @{})
    
    $pythonPath = Join-Path $WorkspaceRoot "python"
    
    if (-not (Test-Path $pythonPath)) {
        Write-Host "⚠️ Python directory not found, skipping Python tests" -ForegroundColor Yellow
        return
    }
    
    Write-Host "🐍 Running Python tests..." -ForegroundColor Yellow
    
    Push-Location $pythonPath
    
    try {
        $args = @("run", "pytest", "-v")
        
        switch ($TestType) {
            "unit" { $args += "tests/unit" }
            "integration" { $args += "tests/integration" }
            "end-to-end" { $args += "tests/end-to-end" }
            default { $args += "tests" }
        }
        
        if ($TestOptions.Coverage) {
            $args += "--cov=semantic_kernel", "--cov-report=xml"
        }
        
        if ($TestOptions.Filter) {
            $args += "-k", $TestOptions.Filter
        }
        
        if ($TestOptions.Parallel) {
            $args += "-n", "auto"
        }
        
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        & poetry @args
        $exitCode = $LASTEXITCODE
        $stopwatch.Stop()
        
        if ($exitCode -eq 0) {
            Write-Host "✅ Python tests PASSED ($($stopwatch.Elapsed.ToString("mm\:ss")))" -ForegroundColor Green
        } else {
            Write-Host "❌ Python tests FAILED ($($stopwatch.Elapsed.ToString("mm\:ss")))" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "💥 Python tests ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

# Function to discover all test projects
function Show-TestProjects {
    Write-Host "🔍 Discovering test projects..." -ForegroundColor Yellow
    
    # .NET Projects
    $dotnetProjects = Get-ChildItem -Path (Join-Path $WorkspaceRoot "01-core-implementations/dotnet") -Recurse -Filter "*Tests.csproj"
    Write-Host "📦 .NET Test Projects ($($dotnetProjects.Count)):" -ForegroundColor Green
    foreach ($project in $dotnetProjects) {
        $relativePath = $project.FullName.Replace($WorkspaceRoot, "").TrimStart("\", "/")
        Write-Host "  • $($project.BaseName)" -ForegroundColor White
        Write-Host "    $relativePath" -ForegroundColor Gray
    }
    
    # Python Projects
    $pythonPath = Join-Path $WorkspaceRoot "python"
    if (Test-Path $pythonPath) {
        $pythonTestDirs = @("tests/unit", "tests/integration", "tests/end-to-end") | 
            Where-Object { Test-Path (Join-Path $pythonPath $_) }
        
        Write-Host "🐍 Python Test Projects ($($pythonTestDirs.Count)):" -ForegroundColor Green
        foreach ($dir in $pythonTestDirs) {
            Write-Host "  • Python.$((Split-Path $dir -Leaf))" -ForegroundColor White
            Write-Host "    python/$dir" -ForegroundColor Gray
        }
    }
    
    # TypeScript Projects
    $tsProjects = Get-ChildItem -Path (Join-Path $WorkspaceRoot "typescript") -Recurse -Filter "package.json" -ErrorAction SilentlyContinue
    if ($tsProjects) {
        $tsTestProjects = $tsProjects | Where-Object { 
            $projectDir = Split-Path $_.FullName -Parent
            (Test-Path (Join-Path $projectDir "tests")) -or 
            (Test-Path (Join-Path $projectDir "test")) -or
            (Get-ChildItem $projectDir -Filter "*.test.*" -Recurse).Count -gt 0
        }
        
        Write-Host "📜 TypeScript Test Projects ($($tsTestProjects.Count)):" -ForegroundColor Green
        foreach ($project in $tsTestProjects) {
            $projectName = Split-Path (Split-Path $project.FullName -Parent) -Leaf
            $relativePath = $project.FullName.Replace($WorkspaceRoot, "").TrimStart("\", "/")
            Write-Host "  • TypeScript.$projectName" -ForegroundColor White
            Write-Host "    $relativePath" -ForegroundColor Gray
        }
    }
}

# Function to run tests in watch mode
function Start-WatchMode {
    param($Pattern = "")
    
    Write-Host "👀 Starting watch mode..." -ForegroundColor Cyan
    if ($Pattern) {
        Write-Host "📍 Pattern: $Pattern" -ForegroundColor Yellow
    }
    Write-Host "Press Ctrl+C to stop watching" -ForegroundColor Gray
    
    # Simple file watcher implementation
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $WorkspaceRoot
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    
    $lastRun = [DateTime]::MinValue
    $debounceMs = 2000
    
    $action = {
        $now = [DateTime]::Now
        if (($now - $script:lastRun).TotalMilliseconds -gt $script:debounceMs) {
            $script:lastRun = $now
            
            Write-Host "📝 File changes detected, running tests..." -ForegroundColor Cyan
            
            if ($script:Pattern) {
                Invoke-Tests -Pattern $script:Pattern -Quick
            } else {
                Invoke-Tests -Quick
            }
        }
    }
    
    Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action $action
    Register-ObjectEvent -InputObject $watcher -EventName "Created" -Action $action
    Register-ObjectEvent -InputObject $watcher -EventName "Deleted" -Action $action
    
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    }
    finally {
        $watcher.Dispose()
    }
}

# Function to run tests with pattern
function Invoke-Tests {
    param($Pattern = "", $Quick = $false)
    
    $testOptions = @{
        Coverage = $Coverage.IsPresent
        Filter = $Filter
        Parallel = $Parallel.IsPresent
        Verbose = $Verbose.IsPresent
    }
    
    $startTime = Get-Date
    
    if ($Pattern) {
        Write-Host "🎯 Running tests matching pattern: $Pattern" -ForegroundColor Cyan
        
        # Run matching .NET tests
        Invoke-DotNetTests -ProjectPattern $Pattern -TestOptions $testOptions
        
        # Run Python tests if pattern matches
        if ($Pattern -match "python|unit|integration|end-to-end") {
            $testType = if ($Pattern -match "unit") { "unit" } 
                       elseif ($Pattern -match "integration") { "integration" }
                       elseif ($Pattern -match "end-to-end") { "end-to-end" }
                       else { "all" }
            Invoke-PythonTests -TestType $testType -TestOptions $testOptions
        }
    } else {
        Write-Host "🚀 Running all tests..." -ForegroundColor Cyan
        
        # Run all .NET tests
        Invoke-DotNetTests -TestOptions $testOptions
        
        # Run all Python tests
        Invoke-PythonTests -TestOptions $testOptions
    }
    
    $duration = (Get-Date) - $startTime
    Write-Host "⏱️ Total execution time: $($duration.ToString("mm\:ss"))" -ForegroundColor Magenta
}

# Main execution logic
try {
    switch ($Command) {
        "discover" {
            Show-TestProjects
        }
        "run-all" {
            Invoke-Tests
        }
        "run" {
            if (-not $Pattern) {
                Write-Error "❌ Pattern parameter is required for 'run' command"
                exit 1
            }
            Invoke-Tests -Pattern $Pattern
        }
        "watch" {
            Start-WatchMode -Pattern $Pattern
        }
    }
    
    Write-Host "✨ Auto test execution completed!" -ForegroundColor Green
}
catch {
    Write-Host "💥 Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($Verbose) {
        Write-Host $_.ScriptStackTrace -ForegroundColor Red
    }
    exit 1
}
