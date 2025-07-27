#!/usr/bin/env python3
"""
EHB Healthcare System - Simple Start Script
Uses proper PowerShell commands without && operator
"""

import os
import subprocess
import time
import webbrowser
from datetime import datetime

def log(message):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_powershell_command(command):
    """Run PowerShell command properly"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        log(f"❌ Command failed: {e}")
        return None

def main():
    """Main function"""
    log("🏥 EHB Healthcare - Simple Start Script")
    log("=" * 40)
    
    # Step 1: Kill existing processes
    log("🛑 Killing existing processes...")
    run_powershell_command("Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force")
    run_powershell_command("Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force")
    run_powershell_command("Get-Process npm -ErrorAction SilentlyContinue | Stop-Process -Force")
    
    # Step 2: Start backend
    log("🔧 Starting backend server...")
    if os.path.exists('ehb_api_server.py'):
        subprocess.Popen(['python', 'ehb_api_server.py'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        time.sleep(3)
        log("✅ Backend server started")
    else:
        log("❌ Backend server file not found")
        return
    
    # Step 3: Start frontend
    log("🌐 Starting frontend server...")
    if os.path.exists('frontend'):
        os.chdir('frontend')
        
        # Install dependencies
        log("📦 Installing frontend dependencies...")
        run_powershell_command("npm install")
        
        # Start frontend
        subprocess.Popen(['npm', 'run', 'dev'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        time.sleep(10)
        log("✅ Frontend server started")
    else:
        log("❌ Frontend directory not found")
        return
    
    # Step 4: Open browsers
    log("🌐 Opening browsers...")
    time.sleep(5)
    
    # Open browsers using PowerShell
    run_powershell_command("Start-Process 'http://localhost:3001'")
    run_powershell_command("Start-Process 'http://localhost:8000'")
    run_powershell_command("Start-Process 'http://localhost:8000/api/patients'")
    
    log("✅ Browsers opened")
    
    # Step 5: Keep running
    log("🎉 System started successfully!")
    log("🌐 Frontend: http://localhost:3001")
    log("🔧 Backend: http://localhost:8000")
    log("🔄 System running... (Press Ctrl+C to stop)")
    
    try:
        while True:
            time.sleep(30)
            log("✅ System still running...")
    except KeyboardInterrupt:
        log("🛑 Shutting down...")

if __name__ == "__main__":
    main() 