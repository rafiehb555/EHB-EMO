# EHB Complete Deployment
Write-Host "🚀 Starting EHB AI Dev Agent Deployment..." -ForegroundColor Green

# Check dependencies
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found!" -ForegroundColor Red
    exit 1
}

try {
    $npmVersion = npm --version
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found!" -ForegroundColor Red
    exit 1
}

try {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
cd "F:\ehb 5"
npm install

# Start backend
Write-Host "🚀 Starting backend server..." -ForegroundColor Yellow
Start-Job -ScriptBlock {
    cd "F:\ehb 5"
    python api_server.py
} | Out-Null

Write-Host "✅ Backend started in background" -ForegroundColor Green

# Wait for backend
Start-Sleep 5

# Start frontend
Write-Host "🚀 Starting frontend server..." -ForegroundColor Yellow
Start-Job -ScriptBlock {
    cd "F:\ehb 5"
    npm run dev
} | Out-Null

Write-Host "✅ Frontend started in background" -ForegroundColor Green

# Wait for frontend
Start-Sleep 10

# Open browser
Write-Host "🌐 Opening application..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host "🎉 EHB AI Dev Agent is LIVE!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 Health: http://localhost:8000/health" -ForegroundColor Cyan

# Keep running
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
while ($true) {
    Start-Sleep 1
}
