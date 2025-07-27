#!/usr/bin/env python3
"""
EHB Auto Full Stack Developer
Automatically sets up frontend (Next.js/React), backend (FastAPI), installs all required tools/SDKs, and manages dashboard/admin panel.
"""

import os
import subprocess
import sys
from pathlib import Path

def run(cmd, cwd=None):
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        return False
    return True

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def setup_frontend():
    print("\n🚀 Setting up Next.js frontend...")
    ensure_dir('frontend')
    if not Path('frontend/package.json').exists():
        print("Creating Next.js app...")
        run('npx create-next-app@latest frontend --typescript --use-npm --yes')
    else:
        print("✅ Next.js frontend already exists.")
    
    # Install additional dependencies
    if Path('frontend/package.json').exists():
        run('npm install @mui/material @emotion/react @emotion/styled', cwd='frontend')
        run('npm install @mui/icons-material', cwd='frontend')
        print("✅ Frontend setup complete.")
    else:
        print("⚠️ Frontend setup incomplete - package.json not found")

def setup_backend():
    print("\n🚀 Setting up FastAPI backend...")
    ensure_dir('backend')
    if not Path('backend/main.py').exists():
        with open('backend/main.py', 'w') as f:
            f.write('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
def status():
    return {"status": "ok"}

@app.get("/api/health")
def health():
    return {"health": "ok", "service": "backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
    if not Path('backend/requirements.txt').exists():
        with open('backend/requirements.txt', 'w') as f:
            f.write('fastapi\nuvicorn[standard]\npydantic\n')
    
    # Install Python dependencies
    if run('python -m pip install --upgrade pip'):
        run('pip install -r requirements.txt', cwd='backend')
        print("✅ Backend setup complete.")
    else:
        print("⚠️ Backend setup incomplete - pip upgrade failed")

def setup_dashboard():
    print("\n🚀 Setting up dashboard and admin panel...")
    ensure_dir('frontend/pages')
    
    # Dashboard page
    dashboard_path = Path('frontend/pages/dashboard.tsx')
    if not dashboard_path.exists():
        with open(dashboard_path, 'w') as f:
            f.write('''import React from "react";
import { Box, Typography, Grid, Card, CardContent } from "@mui/material";

export default function Dashboard() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        EHB Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Welcome to EHB Dashboard</Typography>
              <Typography variant="body2">
                This is your main dashboard. Add your content here.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Quick Stats</Typography>
              <Typography variant="body2">
                Your statistics will appear here.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
''')
    
    # Admin panel page
    admin_path = Path('frontend/pages/admin.tsx')
    if not admin_path.exists():
        with open(admin_path, 'w') as f:
            f.write('''import React from "react";
import { Box, Typography, Grid, Card, CardContent, Button } from "@mui/material";

export default function Admin() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        EHB Admin Panel
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Admin Controls</Typography>
              <Button variant="contained" sx={{ mt: 2 }}>
                Manage Users
              </Button>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">System Status</Typography>
              <Typography variant="body2" color="success.main">
                All systems operational
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
''')
    
    print("✅ Dashboard and admin panel setup complete.")

def install_global_tools():
    print("\n🔧 Installing global tools/SDKs...")
    
    # Install Node.js tools
    run('npm install -g typescript')
    run('npm install -g markdownlint-cli')
    run('npm install -g create-next-app')
    
    # Install Python tools (Windows compatible)
    run('python -m pip install --upgrade pip')
    run('pip install fastapi uvicorn pydantic')
    
    print("✅ Global tools/SDKs installed.")

def create_startup_scripts():
    print("\n📝 Creating startup scripts...")
    
    # Windows batch file for starting both servers
    with open('start_dev.bat', 'w') as f:
        f.write('''@echo off
echo Starting EHB Development Environment...
echo.
echo Starting Backend (FastAPI)...
start cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"
echo.
echo Starting Frontend (Next.js)...
start cmd /k "cd frontend && npm run dev"
echo.
echo Development servers started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Dashboard: http://localhost:3000/dashboard
echo Admin: http://localhost:3000/admin
pause
''')
    
    # PowerShell script
    with open('start_dev.ps1', 'w') as f:
        f.write('''Write-Host "Starting EHB Development Environment..." -ForegroundColor Green
Write-Host ""

Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn main:app --reload --port 8000"

Write-Host "Starting Frontend (Next.js)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "Development servers started!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Dashboard: http://localhost:3000/dashboard" -ForegroundColor Cyan
Write-Host "Admin: http://localhost:3000/admin" -ForegroundColor Cyan
''')
    
    print("✅ Startup scripts created.")

def main():
    print("\n==============================")
    print("EHB Auto Full Stack Developer")
    print("==============================\n")
    
    install_global_tools()
    setup_frontend()
    setup_backend()
    setup_dashboard()
    create_startup_scripts()
    
    print("\n🎉 All setup complete!")
    print("\n📁 Project Structure:")
    print("  ├── frontend/     (Next.js app)")
    print("  ├── backend/      (FastAPI server)")
    print("  ├── start_dev.bat (Windows startup)")
    print("  └── start_dev.ps1 (PowerShell startup)")
    
    print("\n🚀 To start development:")
    print("  1. Double-click: start_dev.bat")
    print("  2. Or run: .\\start_dev.ps1")
    print("  3. Or manually:")
    print("     - Backend: cd backend && python -m uvicorn main:app --reload")
    print("     - Frontend: cd frontend && npm run dev")
    
    print("\n🌐 URLs:")
    print("  - Backend API: http://localhost:8000")
    print("  - Frontend: http://localhost:3000")
    print("  - Dashboard: http://localhost:3000/dashboard")
    print("  - Admin Panel: http://localhost:3000/admin")

if __name__ == "__main__":
    main() 