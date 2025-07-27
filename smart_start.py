#!/usr/bin/env python3
"""
EHB Healthcare System - Smart Start Script
Automatically handles port conflicts and process management
"""

import os
import socket
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

def is_port_in_use(port):
    """Check if port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill process using specific port"""
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(
                f'netstat -ano | findstr ":{port}"',
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if f':{port}' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            subprocess.run(f'taskkill /f /pid {pid}', shell=True)
                            print_status(f"Killed process {pid} on port {port}", "SUCCESS")
        else:
            # Linux/Mac
            subprocess.run(f'lsof -ti:{port} | xargs kill -9', shell=True)
            print_status(f"Killed process on port {port}", "SUCCESS")
    except Exception as e:
        print_status(f"Error killing process on port {port}: {e}", "ERROR")

def kill_all_processes():
    """Kill all relevant processes"""
    print_status("Killing all existing processes...")
    
    try:
        if sys.platform == "win32":
            # Windows
            subprocess.run("taskkill /f /im python.exe", shell=True, capture_output=True)
            subprocess.run("taskkill /f /im node.exe", shell=True, capture_output=True)
            subprocess.run("taskkill /f /im npm.exe", shell=True, capture_output=True)
        else:
            # Linux/Mac
            subprocess.run("pkill -f python", shell=True, capture_output=True)
            subprocess.run("pkill -f node", shell=True, capture_output=True)
            subprocess.run("pkill -f npm", shell=True, capture_output=True)
        
        print_status("All processes killed", "SUCCESS")
        time.sleep(2)
    except Exception as e:
        print_status(f"Error killing processes: {e}", "ERROR")

def start_backend():
    """Start backend with port conflict handling"""
    print_status("Starting backend API server...")
    
    # Check if port 8000 is in use
    if is_port_in_use(8000):
        print_status("Port 8000 is in use, killing existing process", "WARNING")
        kill_process_on_port(8000)
        time.sleep(2)
    
    if not os.path.exists("ehb_api_server.py"):
        print_status("Backend file not found", "ERROR")
        return None
    
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "ehb_api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)
        
        # Verify backend is running
        if is_port_in_use(8000):
            print_status("Backend server started successfully", "SUCCESS")
            return backend_process
        else:
            print_status("Backend server failed to start", "ERROR")
            return None
        
    except Exception as e:
        print_status(f"Error starting backend: {e}", "ERROR")
        return None

def start_frontend():
    """Start frontend with port conflict handling"""
    print_status("Starting frontend development server...")
    
    # Check if port 3001 is in use
    if is_port_in_use(3001):
        print_status("Port 3001 is in use, killing existing process", "WARNING")
        kill_process_on_port(3001)
        time.sleep(2)
    
    if not os.path.exists("frontend"):
        print_status("Frontend directory not found", "ERROR")
        return None
    
    try:
        # Change to frontend directory
        original_dir = os.getcwd()
        os.chdir("frontend")
        
        if not os.path.exists("package.json"):
            print_status("package.json not found", "ERROR")
            os.chdir(original_dir)
            return None
        
        # Install dependencies
        print_status("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], capture_output=True, check=False)
        
        # Start frontend
        print_status("Starting Next.js development server...")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(5)
        
        # Verify frontend is running
        if is_port_in_use(3001):
            print_status("Frontend server started successfully", "SUCCESS")
            return frontend_process
        else:
            print_status("Frontend server failed to start", "ERROR")
            return None
        
    except Exception as e:
        print_status(f"Error starting frontend: {e}", "ERROR")
        return None

def check_services():
    """Check if services are running"""
    print_status("Checking service status...")
    
    backend_ok = is_port_in_use(8000)
    frontend_ok = is_port_in_use(3001)
    
    if backend_ok:
        print_status("✅ Backend API: Running on port 8000", "SUCCESS")
    else:
        print_status("❌ Backend API: Not running", "ERROR")
    
    if frontend_ok:
        print_status("✅ Frontend: Running on port 3001", "SUCCESS")
    else:
        print_status("❌ Frontend: Not running", "ERROR")
    
    return backend_ok and frontend_ok

def main():
    """Main function"""
    print("=" * 60)
    print("🏥 EHB Healthcare System - Smart Start")
    print("=" * 60)
    
    # Kill all processes first
    kill_all_processes()
    
    # Start backend
    backend_process = start_backend()
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Check services
    time.sleep(3)
    services_ok = check_services()
    
    print("\n" + "=" * 60)
    print("📋 System Status Summary:")
    print("=" * 60)
    print("🔗 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3001")
    print("📊 Health Check: http://localhost:8000/health")
    print("👥 Patients API: http://localhost:8000/api/patients")
    print("👨‍⚕️ Doctors API: http://localhost:8000/api/doctors")
    print("=" * 60)
    
    if services_ok:
        print_status("🎉 System started successfully!", "SUCCESS")
        print("\n💡 Open http://localhost:3001 in your browser")
    else:
        print_status("⚠️ Some services failed to start", "WARNING")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if ports 8000 and 3001 are free")
        print("   2. Restart the script")
        print("   3. Check firewall settings")
    
    print("\n🛑 Press Ctrl+C to stop all servers")
    
    try:
        while True:
            time.sleep(10)
            # Periodic health check
            if not check_services():
                print_status("⚠️ Some services stopped, restarting...", "WARNING")
                if backend_process:
                    backend_process.terminate()
                if frontend_process:
                    frontend_process.terminate()
                time.sleep(2)
                backend_process = start_backend()
                frontend_process = start_frontend()
    except KeyboardInterrupt:
        print_status("Shutting down...", "WARNING")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print_status("System stopped", "SUCCESS")

if __name__ == "__main__":
    main() 