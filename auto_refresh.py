#!/usr/bin/env python3
"""
EHB Healthcare System - Auto Refresh Script
Continuously keeps the system visible
"""

import time
import webbrowser
import requests
import threading
from datetime import datetime

def log(message):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_service(url, name):
    """Check if service is running"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            log(f"✅ {name} is running")
            return True
        else:
            log(f"⚠️ {name} status: {response.status_code}")
            return False
    except:
        log(f"❌ {name} is not responding")
        return False

def refresh_browsers():
    """Refresh browsers to keep system visible"""
    try:
        # Refresh frontend
        webbrowser.open('http://localhost:3001')
        log("🔄 Refreshed frontend browser")
        
        # Refresh backend
        webbrowser.open('http://localhost:8000')
        log("🔄 Refreshed backend browser")
        
        # Open API endpoints
        webbrowser.open('http://localhost:8000/api/patients')
        log("🔄 Refreshed API endpoints")
        
    except Exception as e:
        log(f"⚠️ Browser refresh error: {e}")

def main():
    """Main function"""
    log("🏥 EHB Healthcare - Auto Refresh System")
    log("=" * 40)
    log("🔄 Starting continuous display refresh...")
    
    refresh_count = 0
    
    while True:
        try:
            # Check services
            frontend_ok = check_service('http://localhost:3001', 'Frontend')
            backend_ok = check_service('http://localhost:8000', 'Backend')
            
            # Refresh browsers
            refresh_browsers()
            refresh_count += 1
            
            log(f"📊 Refresh #{refresh_count} completed")
            log(f"⏰ Next refresh in 30 seconds...")
            
            # Wait 30 seconds before next refresh
            time.sleep(30)
            
        except KeyboardInterrupt:
            log("🛑 Auto refresh stopped by user")
            break
        except Exception as e:
            log(f"❌ Auto refresh error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main() 