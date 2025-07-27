# Health Check
Write-Host "🔍 Checking EHB System Health..." -ForegroundColor Green

# Check frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5
    Write-Host "✅ Frontend: ACTIVE (Port 3000)" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend: NOT RESPONDING" -ForegroundColor Red
}

# Check backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "✅ Backend: ACTIVE (Port 8000)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend: NOT RESPONDING" -ForegroundColor Red
}

# Check ports
$ports = @(3000, 8000)
foreach ($port in $ports) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "✅ Port $port: IN USE" -ForegroundColor Green
    } else {
        Write-Host "❌ Port $port: NOT IN USE" -ForegroundColor Red
    }
}
