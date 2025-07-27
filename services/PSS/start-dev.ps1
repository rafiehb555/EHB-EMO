# PowerShell script to start PSS development server
# This script handles the directory change and npm run dev command properly

Write-Host "Starting PSS Development Server..." -ForegroundColor Green

# Change to pss directory
Set-Location -Path "pss"

# Check if we're in the correct directory
if (Test-Path "package.json") {
    Write-Host "Found package.json, starting development server..." -ForegroundColor Yellow
    
    # Run npm run dev
    npm run dev
} else {
    Write-Host "Error: package.json not found in pss directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Red
    exit 1
} 