# Start Both Servers
Write-Host "🚀 Starting EHB Complete System..." -ForegroundColor Green
cd "F:\ehb 5"

# Start backend in background
Start-Job -ScriptBlock {
    cd "F:\ehb 5"
    python api_server.py
} | Out-Null

Write-Host "✅ Backend started in background" -ForegroundColor Green

# Start frontend
npm run dev
