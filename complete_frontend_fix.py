#!/usr/bin/env python3
"""
Complete Frontend Fix Script
Fixes all issues and starts both servers
"""

import os
import subprocess
import time
from pathlib import Path

import requests


def run_command(command, cwd=None):
    """Run command and return success status"""
    try:
        cwd = cwd or Path.cwd()
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def kill_process_on_port(port):
    """Kill process running on specific port"""
    print(f"Killing process on port {port}...")
    run_command(f'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :{port}\') do taskkill /F /PID %a')
    time.sleep(2)

def clean_frontend():
    """Clean frontend completely"""
    print("Cleaning frontend...")
    
    frontend_dir = Path.cwd() / "frontend"
    
    # Kill any running processes
    kill_process_on_port(3000)
    kill_process_on_port(8000)
    
    # Remove node_modules and lock files
    if frontend_dir.exists():
        # Remove node_modules
        if (frontend_dir / "node_modules").exists():
            print("Removing node_modules...")
            run_command("Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue", cwd=frontend_dir)
        
        # Remove lock files
        for lock_file in ["package-lock.json", "yarn.lock"]:
            if (frontend_dir / lock_file).exists():
                print(f"Removing {lock_file}...")
                run_command(f"Remove-Item -Force {lock_file} -ErrorAction SilentlyContinue", cwd=frontend_dir)
        
        # Fresh install
        print("Installing dependencies...")
        success, _, _ = run_command("npm install", cwd=frontend_dir)
        return success
    
    return False

def fix_config_files():
    """Fix all configuration files"""
    print("Fixing configuration files...")
    
    frontend_dir = Path.cwd() / "frontend"
    
    # Fix next.config.js
    next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
'''
    
    with open(frontend_dir / "next.config.js", "w", encoding='utf-8') as f:
        f.write(next_config)
    
    # Fix postcss.config.js
    postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
    
    with open(frontend_dir / "postcss.config.js", "w", encoding='utf-8') as f:
        f.write(postcss_config)
    
    # Fix tailwind.config.js
    tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        healthcare: {
          primary: '#2563eb',
          secondary: '#059669',
          warning: '#f59e0b',
          danger: '#ef4444',
        }
      }
    },
  },
  plugins: [],
}
'''
    
    with open(frontend_dir / "tailwind.config.js", "w", encoding='utf-8') as f:
        f.write(tailwind_config)
    
    print("Configuration files fixed")

def start_backend():
    """Start backend server"""
    print("Starting backend server...")
    
    # Kill any existing process on port 8000
    kill_process_on_port(8000)
    
    # Start backend
    backend_process = subprocess.Popen(
        ["python", "enhanced_api_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a bit for server to start
    time.sleep(3)
    
    # Test if server is running
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("Backend server started successfully")
            return True
        else:
            print("Backend server failed to start")
            return False
    except:
        print("Backend server failed to start")
        return False

def start_frontend():
    """Start frontend server"""
    print("Starting frontend server...")
    
    # Kill any existing process on port 3000
    kill_process_on_port(3000)
    
    # Change to frontend directory
    frontend_dir = Path.cwd() / "frontend"
    
    # Start frontend
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=frontend_dir
    )
    
    # Wait a bit for server to start
    time.sleep(5)
    
    # Test if server is running
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("Frontend server started successfully")
            return True
        else:
            print("Frontend server failed to start")
            return False
    except:
        print("Frontend server failed to start")
        return False

def test_servers():
    """Test both servers"""
    print("\nTesting servers...")
    
    # Test backend
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("Backend API: http://localhost:8000")
        else:
            print("Backend API failed")
    except:
        print("Backend API not responding")
    
    # Test frontend
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("Frontend App: http://localhost:3000")
        else:
            print("Frontend App failed")
    except:
        print("Frontend App not responding")

def main():
    print("EHB Healthcare System - Complete Fix")
    print("=" * 50)
    
    # Step 1: Clean frontend
    if not clean_frontend():
        print("Failed to clean frontend")
        return
    
    # Step 2: Fix configuration
    fix_config_files()
    
    # Step 3: Start backend
    if not start_backend():
        print("Failed to start backend")
        return
    
    # Step 4: Start frontend
    if not start_frontend():
        print("Failed to start frontend")
        return
    
    # Step 5: Test servers
    test_servers()
    
    print("\n" + "=" * 50)
    print("System is ready!")
    print("Backend API: http://localhost:8000")
    print("Frontend App: http://localhost:3000")
    print("Healthcare Dashboard: http://localhost:3000/healthcare-dashboard")
    print("=" * 50)

if __name__ == "__main__":
    main() 