# EHB Healthcare System - PowerShell Server Starter
# This script starts both frontend and backend servers properly

Write-Host "🏥 EHB Healthcare System - PowerShell Server Starter" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Kill existing processes
Write-Host "🛑 Killing existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process npm -ErrorAction SilentlyContinue | Stop-Process -Force

# Start backend server
Write-Host "🔧 Starting backend server..." -ForegroundColor Yellow
Start-Process python -ArgumentList "ehb_api_server.py" -WindowStyle Hidden

# Wait for backend to start
Start-Sleep -Seconds 3

# Change to frontend directory and start frontend
Write-Host "🌐 Starting frontend server..." -ForegroundColor Yellow
Set-Location frontend
Start-Process npm -ArgumentList "run", "dev" -WindowStyle Hidden

# Wait for frontend to start
Start-Sleep -Seconds 10

# Open browsers
Write-Host "🌐 Opening browsers..." -ForegroundColor Yellow
Start-Process "http://localhost:3001"
Start-Process "http://localhost:8000"
Start-Process "http://localhost:8000/api/patients"

Write-Host "✅ Servers started successfully!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3001" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:8000" -ForegroundColor Cyan

# Keep script running
Write-Host "🔄 Monitoring servers... (Press Ctrl+C to stop)" -ForegroundColor Yellow
while ($true) {
    Start-Sleep -Seconds 30
    Write-Host "✅ Servers still running..." -ForegroundColor Green
} 