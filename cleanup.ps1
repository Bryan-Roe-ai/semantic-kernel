# Repository Cleanup Script for Windows
# This script removes temporary files and directories that shouldn't be in the repository

Write-Host "🧹 Semantic Kernel Repository Cleanup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Function to safely remove directory
function Safe-Remove-Dir {
    param($dir)
    if (Test-Path $dir) {
        Write-Host "Removing directory: $dir" -ForegroundColor Yellow
        Remove-Item -Path $dir -Recurse -Force
        Write-Host "✓ Removed $dir" -ForegroundColor Green
    } else {
        Write-Host "Directory not found (skipping): $dir"
    }
}

# Function to safely remove file
function Safe-Remove-File {
    param($file)
    if (Test-Path $file) {
        Write-Host "Removing file: $file" -ForegroundColor Yellow
        Remove-Item -Path $file -Force
        Write-Host "✓ Removed $file" -ForegroundColor Green
    } else {
        Write-Host "File not found (skipping): $file"
    }
}

Write-Host "1. Cleaning up Python build directories..."
Safe-Remove-Dir "Python-3.12.4"
Safe-Remove-Dir "Python-3.12.5"
Safe-Remove-Dir "tmp\Python-3.12.5"

Write-Host ""
Write-Host "2. Cleaning up virtual environments..."
Safe-Remove-Dir "agi-venv"
Safe-Remove-Dir "clean-venv"
Safe-Remove-Dir "python-clean"
Safe-Remove-Dir ".venv-1"

Write-Host ""
Write-Host "3. Cleaning up Python cache files..."
Safe-Remove-Dir "__pycache__"
Safe-Remove-Dir ".mypy_cache"
Safe-Remove-Dir ".pytest_cache"
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Filter "*.pyc" -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force

Write-Host ""
Write-Host "4. Cleaning up temporary directories..."
Safe-Remove-Dir "tmp"

Write-Host ""
Write-Host "5. Cleaning up build artifacts..."
Safe-Remove-Dir "19-miscellaneous\bin"
Safe-Remove-Dir "19-miscellaneous\obj"

Write-Host ""
Write-Host "6. Checking for large files..."
Write-Host "Files larger than 1MB (excluding git objects):"
Get-ChildItem -Path . -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { $_.Length -gt 1MB -and $_.FullName -notlike "*\.git\*" } | 
    Select-Object FullName, @{Name="Size";Expression={"{0:N2} MB" -f ($_.Length / 1MB)}} |
    ForEach-Object { Write-Host "$($_.FullName) - $($_.Size)" }

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Recommendations:"
Write-Host "  • Run 'git status' to see what was removed"
Write-Host "  • Run 'git add -A' to stage changes"
Write-Host "  • Consider adding .venv to your active virtual environment"
Write-Host "  • Run 'pre-commit install' to set up pre-commit hooks"
Write-Host ""
