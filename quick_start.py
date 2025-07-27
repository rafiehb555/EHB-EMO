#!/usr/bin/env python3
"""
Quick Start Script for EHB Healthcare System
"""

import os
import subprocess
import sys
import time


def run_command(command, description):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    print("🏥 EHB Healthcare System - Quick Start")
    print("=" * 50)
    
    # Kill existing processes
    print("🛑 Stopping existing processes...")
    run_command("taskkill /f /im python.exe", "Killing Python processes")
    run_command("taskkill /f /im node.exe", "Killing Node processes")
    time.sleep(2)
    
    # Start backend
    print("\n🚀 Starting Backend API Server...")
    if os.path.exists("ehb_api_server.py"):
        backend_process = subprocess.Popen([sys.executable, "ehb_api_server.py"])
        print("✅ Backend server started (PID: {})".format(backend_process.pid))
        time.sleep(3)
    else:
        print("❌ Backend server file not found")
        return
    
    # Start frontend
    print("\n🌐 Starting Frontend Development Server...")
    if os.path.exists("frontend"):
        os.chdir("frontend")
        if os.path.exists("package.json"):
            frontend_process = subprocess.Popen(["npm", "run", "dev"])
            print("✅ Frontend server started")
            time.sleep(5)
        else:
            print("❌ package.json not found in frontend")
            return
    else:
        print("❌ Frontend directory not found")
        return
    
    print("\n" + "=" * 50)
    print("🎉 System Started Successfully!")
    print("=" * 50)
    print("🔗 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3000")
    print("📊 Health Check: http://localhost:8000/health")
    print("👥 Patients: http://localhost:8000/api/patients")
    print("👨‍⚕️ Doctors: http://localhost:8000/api/doctors")
    print("=" * 50)
    print("💡 Open http://localhost:3000 in your browser")
    print("🛑 Press Ctrl+C to stop servers")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main() 