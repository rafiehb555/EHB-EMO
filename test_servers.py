#!/usr/bin/env python3
"""
Test script to verify both servers are working
"""

import requests
import time
import subprocess
import os

def test_backend():
    """Test backend server"""
    print("🔧 Testing Backend Server...")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Working - Version: {data.get('version', 'N/A')}")
            print(f"📊 Data Sources: {data.get('data_loaded', 'N/A')}")
            return True
        else:
            print(f"❌ Backend Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Connection Failed: {e}")
        return False

def test_frontend():
    """Test frontend server"""
    print("\n🎨 Testing Frontend Server...")
    
    # Try different ports
    ports = [3000, 3001, 3002]
    
    for port in ports:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Frontend Working on port {port}")
                return True, port
            else:
                print(f"⚠️  Frontend on port {port}: {response.status_code}")
        except Exception as e:
            print(f"❌ Frontend on port {port}: Connection failed")
    
    return False, None

def start_servers():
    """Start both servers"""
    print("🚀 Starting servers...")
    
    # Start backend
    try:
        subprocess.Popen(['python', 'enhanced_api_server.py'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Backend server started")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
    
    # Wait for backend
    time.sleep(3)
    
    # Start frontend
    try:
        os.chdir('frontend')
        subprocess.Popen(['npm', 'run', 'dev'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Frontend server started")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main test function"""
    print("=" * 60)
    print("🏥 EHB Healthcare System - Server Test")
    print("=" * 60)
    
    # Test existing servers
    backend_ok = test_backend()
    frontend_ok, frontend_port = test_frontend()
    
    if not backend_ok or not frontend_ok:
        print("\n🔄 Starting servers...")
        start_servers()
        time.sleep(5)
        
        # Test again
        backend_ok = test_backend()
        frontend_ok, frontend_port = test_frontend()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"Backend: {'✅ Working' if backend_ok else '❌ Failed'}")
    print(f"Frontend: {'✅ Working' if frontend_ok else '❌ Failed'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 SUCCESS! Both servers are working!")
        print(f"🌐 Backend: http://localhost:8000")
        print(f"🌐 Frontend: http://localhost:{frontend_port}")
        print(f"🌐 API Health: http://localhost:8000/api/health")
        print(f"🌐 Dashboard: http://localhost:{frontend_port}/dashboard")
    else:
        print("\n❌ Some servers failed. Check error messages above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 