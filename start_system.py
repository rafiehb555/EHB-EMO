#!/usr/bin/env python3
"""
EHB Healthcare System - Universal Start Script
Works on Windows, Linux, macOS
"""

import os
import subprocess
import sys
import time
from datetime import datetime


def print_status(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "SUCCESS":
        print(f"[{timestamp}] ✅ {message}")
    elif status == "ERROR":
        print(f"[{timestamp}] ❌ {message}")
    elif status == "WARNING":
        print(f"[{timestamp}] ⚠️ {message}")
    else:
        print(f"[{timestamp}] ℹ️ {message}")

def run_command(command, description, shell=True):
    """Run command with proper error handling"""
    print_status(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        if result.returncode == 0:
            print_status(f"{description} completed successfully", "SUCCESS")
            return True
        else:
            print_status(f"{description} failed: {result.stderr}", "ERROR")
            return False
    except Exception as e:
        print_status(f"{description} error: {e}", "ERROR")
        return False

def kill_processes():
    """Kill existing processes"""
    print_status("Killing existing processes...")
    
    if sys.platform == "win32":
        # Windows
        run_command("taskkill /f /im python.exe", "Killing Python processes")
        run_command("taskkill /f /im node.exe", "Killing Node processes")
    else:
        # Linux/Mac
        run_command("pkill -f python", "Killing Python processes")
        run_command("pkill -f node", "Killing Node processes")

def start_backend():
    """Start backend API server"""
    print_status("Starting backend API server...")
    
    if not os.path.exists("ehb_api_server.py"):
        print_status("Backend file not found", "ERROR")
        return None
    
    try:
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, "ehb_api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)
        print_status("Backend server started", "SUCCESS")
        return backend_process
        
    except Exception as e:
        print_status(f"Error starting backend: {e}", "ERROR")
        return None

def start_frontend():
    """Start frontend development server"""
    print_status("Starting frontend development server...")
    
    if not os.path.exists("frontend"):
        print_status("Frontend directory not found", "ERROR")
        return None
    
    try:
        # Change to frontend directory
        os.chdir("frontend")
        
        if not os.path.exists("package.json"):
            print_status("package.json not found", "ERROR")
            return None
        
        # Install dependencies
        print_status("Installing frontend dependencies...")
        run_command("npm install", "Installing npm packages")
        
        # Start frontend
        print_status("Starting Next.js development server...")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(5)
        print_status("Frontend server started", "SUCCESS")
        return frontend_process
        
    except Exception as e:
        print_status(f"Error starting frontend: {e}", "ERROR")
        return None

def check_services():
    """Check if services are running"""
    print_status("Checking service status...")
    
    try:
        import requests

        # Check backend
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print_status("✅ Backend API: Running", "SUCCESS")
            else:
                print_status("❌ Backend API: Not responding", "ERROR")
        except:
            print_status("❌ Backend API: Not accessible", "ERROR")
        
        # Check frontend
        try:
            response = requests.get("http://localhost:3001", timeout=5)
            if response.status_code == 200:
                print_status("✅ Frontend: Running", "SUCCESS")
            else:
                print_status("⚠️ Frontend: Responding but status unclear", "WARNING")
        except:
            print_status("❌ Frontend: Not accessible", "ERROR")
            
    except ImportError:
        print_status("requests module not available, skipping service check", "WARNING")

def main():
    """Main function"""
    print("=" * 60)
    print("🏥 EHB Healthcare System - Universal Start Script")
    print("=" * 60)
    
    # Kill existing processes
    kill_processes()
    time.sleep(2)
    
    # Start backend
    backend_process = start_backend()
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Check services
    time.sleep(3)
    check_services()
    
    print("\n" + "=" * 60)
    print("📋 System Status Summary:")
    print("=" * 60)
    print("🔗 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3001")
    print("📊 Health Check: http://localhost:8000/health")
    print("👥 Patients API: http://localhost:8000/api/patients")
    print("👨‍⚕️ Doctors API: http://localhost:8000/api/doctors")
    print("=" * 60)
    
    if backend_process and frontend_process:
        print_status("🎉 System started successfully!", "SUCCESS")
    else:
        print_status("⚠️ Some services may not be running properly", "WARNING")
    
    print("\n💡 Usage:")
    print("   - Run: python start_system.py")
    print("   - PowerShell: .\\start_frontend.ps1")
    print("   - CMD: start_frontend.bat")
    print("   - Browser: http://localhost:3001")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print_status("Shutting down...", "WARNING")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print_status("System stopped", "SUCCESS")

if __name__ == "__main__":
    main() 