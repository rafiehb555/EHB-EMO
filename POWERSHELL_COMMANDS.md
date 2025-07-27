# PowerShell Command Fix Guide

## ❌ Problem Commands (Don't Use)
```powershell
cd /f%3A/ehb%205 && python api_server.py
cd /f%3A/ehb%205 && npm run dev
timeout 5 && start http://localhost:3000
```

## ✅ Fixed Commands (Use These)
```powershell
cd "F:\ehb 5"; python api_server.py
cd "F:\ehb 5"; npm run dev
Start-Sleep 5; Start-Process "http://localhost:3000"
```

## 🚀 Quick Start Commands

### Start Frontend Only
```powershell
.\start_frontend.ps1
```

### Start Backend Only
```powershell
.\start_backend.ps1
```

### Start Both Servers
```powershell
.\start_both.ps1
```

### Complete Deployment
```powershell
.\deploy_ehb.ps1
```

### Health Check
```powershell
.\health_check.ps1
```

### Open Browser
```powershell
.\open_browser.ps1
```

## 📋 Alternative Batch Files
- `start_frontend.bat`
- `start_backend.bat`
- `start_both.bat`

## 🔧 Manual Commands
```powershell
# Navigate to project
cd "F:\ehb 5"

# Start backend
python api_server.py

# Start frontend (in new terminal)
npm run dev

# Open browser
Start-Process "http://localhost:3000"

# Check ports
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

## 🎯 Key Points
1. Use `;` instead of `&&` in PowerShell
2. Use proper path format: `"F:\ehb 5"`
3. Use `Start-Process` instead of `start`
4. Use `Start-Sleep` instead of `timeout`
5. Use `.\script.ps1` to run PowerShell scripts

## 🚨 Emergency Commands
```powershell
# Kill processes on ports
netstat -ano | findstr :3000
taskkill /PID <PID> /F

netstat -ano | findstr :8000
taskkill /PID <PID> /F
```
