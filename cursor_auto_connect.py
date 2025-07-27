#!/usr/bin/env python3
"""
Cursor Auto-Connect Script
Automatically starts servers when Cursor IDE is detected
"""

import os
import subprocess
import threading
import time
from pathlib import Path

import psutil


class CursorAutoConnect:
    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"
        self.running = False
        
    def detect_cursor(self):
        """Detect if Cursor IDE is running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'cursor' in proc.info['name'].lower():
                    return True
            return False
        except:
            return False
    
    def check_servers_running(self):
        """Check if servers are already running"""
        try:
            # Check if port 3000 or 3001 is in use
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            return '3000' in result.stdout or '3001' in result.stdout
        except:
            return False
    
    def start_servers(self):
        """Start both frontend and backend servers"""
        print("🚀 Auto-starting EHB Healthcare servers...")
        
        # Start backend server
        backend_thread = threading.Thread(target=self._start_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend server
        frontend_thread = threading.Thread(target=self._start_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()
        
        print("✅ Servers started in background")
        print("🌐 Frontend: http://localhost:3000")
        print("🌐 Backend: http://localhost:8000")
    
    def _start_backend(self):
        """Start backend server in background"""
        try:
            os.chdir(self.project_root)
            subprocess.run(['python', 'enhanced_api_server.py'], 
                         capture_output=True, check=False)
        except Exception as e:
            print(f"❌ Backend error: {e}")
    
    def _start_frontend(self):
        """Start frontend server in background"""
        try:
            os.chdir(self.frontend_dir)
            env = os.environ.copy()
            env['PORT'] = '3000'
            subprocess.run(['npm', 'run', 'dev'], 
                         env=env, capture_output=True, check=False)
        except Exception as e:
            print(f"❌ Frontend error: {e}")
    
    def monitor_and_auto_start(self):
        """Monitor for Cursor and auto-start servers"""
        print("🔍 Monitoring for Cursor IDE...")
        print("💡 When you open Cursor, servers will auto-start")
        
        while True:
            try:
                if self.detect_cursor() and not self.running:
                    print("\n🎯 Cursor detected! Starting servers...")
                    self.running = True
                    self.start_servers()
                
                elif not self.detect_cursor() and self.running:
                    print("\n📝 Cursor closed. Servers still running...")
                    self.running = False
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\n🛑 Auto-connect stopped by user")
                break
            except Exception as e:
                print(f"⚠️  Monitor error: {e}")
                time.sleep(10)

def main():
    """Main function"""
    print("=" * 60)
    print("🎯 Cursor Auto-Connect for EHB Healthcare")
    print("=" * 60)
    
    auto_connect = CursorAutoConnect()
    
    # Check if servers are already running
    if auto_connect.check_servers_running():
        print("✅ Servers are already running!")
        print("🌐 Frontend: http://localhost:3000")
        print("🌐 Backend: http://localhost:8000")
    else:
        print("⏳ Waiting for Cursor IDE to start...")
        print("💡 Open Cursor IDE to auto-start servers")
    
    # Start monitoring
    auto_connect.monitor_and_auto_start()

if __name__ == "__main__":
    main() 