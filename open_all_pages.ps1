# EHB Auto Page Opener PowerShell Script
# Automatically opens all project pages in the browser

Write-Host "EHB Auto Page Opener" -ForegroundColor Green
Write-Host "====================" -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the Python script
Write-Host "🚀 Starting Auto Page Opener..." -ForegroundColor Cyan
python auto_open_all_pages.py

Write-Host ""
Write-Host "Press Enter to exit..." -ForegroundColor Yellow
Read-Host 