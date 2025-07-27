# EHB Auto Runner PowerShell Script
Write-Host "================================================" -ForegroundColor Green
Write-Host "🚀 EHB Auto Runner - Starting Both Servers" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔧 Backend Server will run on port 8000" -ForegroundColor Yellow
Write-Host "🎨 Frontend Server will run on port 3000" -ForegroundColor Yellow
Write-Host "🔄 Auto-monitoring and restart enabled" -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting EHB Auto Runner..." -ForegroundColor Cyan
Write-Host ""

python auto_ehb_runner.py

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 