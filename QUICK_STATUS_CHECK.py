"""
Quick Status Check
Check if all systems are working properly
"""

import subprocess
import sys
import time
from pathlib import Path

import requests


def check_server(url, name):
    """Check if server is responding"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: {url} - ONLINE")
            return True
        else:
            print(f"⚠️ {name}: {url} - Status {response.status_code}")
            return False
    except:
        print(f"❌ {name}: {url} - OFFLINE")
        return False

def check_processes():
    """Check if processes are running"""
    print("\n🔍 Checking running processes...")
    
    # Check Python processes
    try:
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], 
                              capture_output=True, text=True)
        if "python.exe" in result.stdout:
            print("✅ Python processes are running")
        else:
            print("❌ No Python processes found")
    except:
        print("⚠️ Could not check Python processes")
    
    # Check Node.js processes
    try:
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq node.exe"], 
                              capture_output=True, text=True)
        if "node.exe" in result.stdout:
            print("✅ Node.js processes are running")
        else:
            print("❌ No Node.js processes found")
    except:
        print("⚠️ Could not check Node.js processes")

def main():
    """Main status check"""
    print("🏥 EHB Healthcare System - Quick Status Check")
    print("="*50)
    
    # Check servers
    print("\n🌐 Checking servers...")
    backend_ok = check_server("http://localhost:8000/", "Backend API")
    frontend_ok = check_server("http://localhost:3001/", "Frontend App")
    
    # Check processes
    check_processes()
    
    print("\n" + "="*50)
    if backend_ok and frontend_ok:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n📱 Access URLs:")
        print("   Frontend: http://localhost:3001")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("⚠️ Some systems may need attention")
        if not backend_ok:
            print("   - Backend server needs to be started")
        if not frontend_ok:
            print("   - Frontend server needs to be started")
    print("="*50)

if __name__ == "__main__":
    main() 