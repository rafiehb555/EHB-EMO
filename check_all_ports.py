"""
Check All Ports
Check all possible ports where servers might be running
"""

import time

import requests


def check_port(port, name):
    """Check if server is running on specific port"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=3)
        if response.status_code == 200:
            print(f"✅ {name} on port {port}: ONLINE")
            return True
        else:
            print(f"⚠️ {name} on port {port}: Status {response.status_code}")
            return False
    except:
        print(f"❌ {name} on port {port}: OFFLINE")
        return False

def main():
    """Check all possible ports"""
    print("🔍 Checking all possible server ports...")
    print("="*50)
    
    # Check backend ports
    backend_ports = [8000, 8001, 8002, 8003, 8004, 8005, 5000, 5001, 5002]
    frontend_ports = [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010]
    
    print("\n🌐 Backend API Servers:")
    backend_found = False
    for port in backend_ports:
        if check_port(port, f"Backend API"):
            backend_found = True
            break
    
    print("\n🌐 Frontend Servers:")
    frontend_found = False
    for port in frontend_ports:
        if check_port(port, f"Frontend App"):
            frontend_found = True
            break
    
    print("\n" + "="*50)
    if backend_found and frontend_found:
        print("🎉 Servers found and running!")
    elif backend_found:
        print("⚠️ Only backend server found")
    elif frontend_found:
        print("⚠️ Only frontend server found")
    else:
        print("❌ No servers found running")
    print("="*50)

if __name__ == "__main__":
    main() 