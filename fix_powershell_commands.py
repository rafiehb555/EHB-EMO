#!/usr/bin/env python3
"""
PowerShell Command Fixer
Fixes PowerShell syntax issues and provides proper command alternatives
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


class PowerShellFixer:
    def __init__(self):
        self.fixes = {
            '&&': ';',
            'cd /f%3A/ehb%205 &&': 'cd "F:\\ehb 5";',
            'cd /f%3A/ehb%205 && python': 'cd "F:\\ehb 5"; python',
            'cd /f%3A/ehb%205 && npm': 'cd "F:\\ehb 5"; npm',
            'timeout 5 &&': 'Start-Sleep 5;',
            'start http://localhost:3000': 'Start-Process "http://localhost:3000"',
            'start http://localhost:8000': 'Start-Process "http://localhost:8000"'
        }
        
    def create_powershell_scripts(self):
        """Create PowerShell scripts for common operations"""
        
        # Create start frontend script
        frontend_script = '''# Start Frontend Server
Write-Host "🚀 Starting EHB Frontend Server..." -ForegroundColor Green
cd "F:\\ehb 5"
npm run dev
'''
        with open("start_frontend.ps1", "w", encoding='utf-8') as f:
            f.write(frontend_script)
            
        # Create start backend script
        backend_script = '''# Start Backend Server
Write-Host "🚀 Starting EHB Backend Server..." -ForegroundColor Green
cd "F:\\ehb 5"
python api_server.py
'''
        with open("start_backend.ps1", "w", encoding='utf-8') as f:
            f.write(backend_script)
            
        # Create start both script
        both_script = '''# Start Both Servers
Write-Host "🚀 Starting EHB Complete System..." -ForegroundColor Green
cd "F:\\ehb 5"

# Start backend in background
Start-Job -ScriptBlock {
    cd "F:\\ehb 5"
    python api_server.py
} | Out-Null

Write-Host "✅ Backend started in background" -ForegroundColor Green

# Start frontend
npm run dev
'''
        with open("start_both.ps1", "w", encoding='utf-8') as f:
            f.write(both_script)
            
        # Create open browser script
        browser_script = '''# Open Browser
Write-Host "🌐 Opening EHB Application..." -ForegroundColor Green
Start-Sleep 5
Start-Process "http://localhost:3000"
Write-Host "✅ Browser opened successfully" -ForegroundColor Green
'''
        with open("open_browser.ps1", "w", encoding='utf-8') as f:
            f.write(browser_script)
            
        # Create health check script
        health_script = '''# Health Check
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
'''
        with open("health_check.ps1", "w", encoding='utf-8') as f:
            f.write(health_script)
            
        # Create complete deployment script
        deployment_script = '''# EHB Complete Deployment
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
cd "F:\\ehb 5"
npm install

# Start backend
Write-Host "🚀 Starting backend server..." -ForegroundColor Yellow
Start-Job -ScriptBlock {
    cd "F:\\ehb 5"
    python api_server.py
} | Out-Null

Write-Host "✅ Backend started in background" -ForegroundColor Green

# Wait for backend
Start-Sleep 5

# Start frontend
Write-Host "🚀 Starting frontend server..." -ForegroundColor Yellow
Start-Job -ScriptBlock {
    cd "F:\\ehb 5"
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
'''
        with open("deploy_ehb.ps1", "w", encoding='utf-8') as f:
            f.write(deployment_script)
            
        print("✅ PowerShell scripts created successfully")
        
    def create_batch_files(self):
        """Create batch files as alternatives"""
        
        # Start frontend batch
        frontend_batch = '''@echo off
echo 🚀 Starting EHB Frontend Server...
cd /d "F:\\ehb 5"
npm run dev
pause
'''
        with open("start_frontend.bat", "w", encoding='utf-8') as f:
            f.write(frontend_batch)
            
        # Start backend batch
        backend_batch = '''@echo off
echo 🚀 Starting EHB Backend Server...
cd /d "F:\\ehb 5"
python api_server.py
pause
'''
        with open("start_backend.bat", "w", encoding='utf-8') as f:
            f.write(backend_batch)
            
        # Start both batch
        both_batch = '''@echo off
echo 🚀 Starting EHB Complete System...
cd /d "F:\\ehb 5"

echo Starting backend...
start "EHB Backend" python api_server.py

echo Starting frontend...
start "EHB Frontend" npm run dev

echo Waiting for servers to start...
timeout /t 10 /nobreak

echo Opening browser...
start http://localhost:3000

echo 🎉 EHB AI Dev Agent is LIVE!
echo Press any key to stop...
pause
'''
        with open("start_both.bat", "w", encoding='utf-8') as f:
            f.write(both_batch)
            
        print("✅ Batch files created successfully")
        
    def create_command_guide(self):
        """Create a command reference guide"""
        
        guide = '''# PowerShell Command Fix Guide

## ❌ Problem Commands (Don't Use)
```powershell
cd /f%3A/ehb%205 && python api_server.py
cd /f%3A/ehb%205 && npm run dev
timeout 5 && start http://localhost:3000
```

## ✅ Fixed Commands (Use These)
```powershell
cd "F:\\ehb 5"; python api_server.py
cd "F:\\ehb 5"; npm run dev
Start-Sleep 5; Start-Process "http://localhost:3000"
```

## 🚀 Quick Start Commands

### Start Frontend Only
```powershell
.\\start_frontend.ps1
```

### Start Backend Only
```powershell
.\\start_backend.ps1
```

### Start Both Servers
```powershell
.\\start_both.ps1
```

### Complete Deployment
```powershell
.\\deploy_ehb.ps1
```

### Health Check
```powershell
.\\health_check.ps1
```

### Open Browser
```powershell
.\\open_browser.ps1
```

## 📋 Alternative Batch Files
- `start_frontend.bat`
- `start_backend.bat`
- `start_both.bat`

## 🔧 Manual Commands
```powershell
# Navigate to project
cd "F:\\ehb 5"

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
2. Use proper path format: `"F:\\ehb 5"`
3. Use `Start-Process` instead of `start`
4. Use `Start-Sleep` instead of `timeout`
5. Use `.\\script.ps1` to run PowerShell scripts

## 🚨 Emergency Commands
```powershell
# Kill processes on ports
netstat -ano | findstr :3000
taskkill /PID <PID> /F

netstat -ano | findstr :8000
taskkill /PID <PID> /F
```
'''
        
        with open("POWERSHELL_COMMANDS.md", "w", encoding='utf-8') as f:
            f.write(guide)
            
        print("✅ Command guide created successfully")
        
    def run_fix(self):
        """Run the complete fix"""
        print("🔧 Fixing PowerShell command issues...")
        
        # Create all scripts and guides
        self.create_powershell_scripts()
        self.create_batch_files()
        self.create_command_guide()
        
        print("\n✅ PowerShell command issues fixed!")
        print("📋 Available scripts:")
        print("   - deploy_ehb.ps1 (Complete deployment)")
        print("   - start_both.ps1 (Start both servers)")
        print("   - start_frontend.ps1 (Frontend only)")
        print("   - start_backend.ps1 (Backend only)")
        print("   - health_check.ps1 (System health)")
        print("   - open_browser.ps1 (Open browser)")
        print("\n📖 See POWERSHELL_COMMANDS.md for usage guide")

def main():
    """Main function"""
    fixer = PowerShellFixer()
    fixer.run_fix()

if __name__ == "__main__":
    main() 