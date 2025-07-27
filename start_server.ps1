# EHB AI Dev Agent - Auto Start PowerShell Script
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🤖 EHB AI Dev Agent - Auto Start" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

try {
    python start_server.py
}
catch {
    Write-Host ""
    Write-Host "❌ Server failed to start" -ForegroundColor Red
    Write-Host "💡 Please check the error messages above" -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
} 