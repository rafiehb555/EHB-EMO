#!/usr/bin/env python3
"""
EHB Healthcare System - Auto Development Manager
Automatically manages servers, ports, and real-time updates
"""

import json
import os
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class AutoDevManager:
    def __init__(self):
        self.frontend_process = None
        self.backend_process = None
        self.observer = None
        self.running = True
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def start_frontend(self):
        """Start frontend with auto-reload"""
        self.log("🚀 Starting frontend with auto-reload...")
        
        try:
            os.chdir("frontend")
            
            # Install nodemon if not exists
            try:
                subprocess.run(['npm', 'install', '-g', 'nodemon'], check=True, capture_output=True)
            except:
                pass
            
            # Start with nodemon for auto-reload
            self.frontend_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.log("✅ Frontend started with auto-reload")
            return True
            
        except Exception as e:
            self.log(f"❌ Frontend error: {e}", "ERROR")
            return False
    
    def start_backend(self):
        """Start backend with auto-reload"""
        self.log("🔧 Starting backend with auto-reload...")
        
        try:
            # Create auto-reload backend server
            backend_code = '''
import http.server
import socketserver
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PORT = 8000

class AutoReloadHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server
        self.last_modified = time.time()
    
    def on_modified(self, event):
        if time.time() - self.last_modified > 1:  # Debounce
            self.last_modified = time.time()
            print(f"🔄 File changed: {event.src_path}")
            # Auto-reload logic here

class EHBHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API (Auto-Reload)",
                "status": "operational",
                "auto_reload": True,
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "auto_reload": True,
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/api/patients':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            patients = [
                {"id": "P001", "name": "Ahmed Khan", "status": "active"},
                {"id": "P002", "name": "Fatima Ali", "status": "active"},
                {"id": "P003", "name": "Muhammad Hassan", "status": "critical"}
            ]
            self.wfile.write(json.dumps(patients, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": self.path}
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare Auto-Reload Server on port {PORT}...")
    
    # Setup file watcher
    event_handler = AutoReloadHandler(None)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    with socketserver.TCPServer(("", PORT), EHBHandler) as httpd:
        print(f"✅ Auto-reload server running at http://localhost:{PORT}")
        httpd.serve_forever()
'''
            
            # Write backend server
            with open('auto_backend_server.py', 'w') as f:
                f.write(backend_code)
            
            # Start backend with auto-reload
            self.backend_process = subprocess.Popen(
                [sys.executable, 'auto_backend_server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.log("✅ Backend started with auto-reload")
            return True
            
        except Exception as e:
            self.log(f"❌ Backend error: {e}", "ERROR")
            return False
    
    def setup_file_watcher(self):
        """Setup file system watcher for auto-reload"""
        self.log("👀 Setting up file watcher...")
        
        class FileChangeHandler(FileSystemEventHandler):
            def __init__(self, manager):
                self.manager = manager
                self.last_modified = time.time()
            
            def on_modified(self, event):
                if time.time() - self.last_modified > 2:  # Debounce
                    self.last_modified = time.time()
                    if event.src_path.endswith(('.py', '.js', '.tsx', '.ts', '.json')):
                        self.manager.log(f"🔄 File changed: {event.src_path}")
                        self.manager.auto_reload()
        
        event_handler = FileChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, path='.', recursive=True)
        self.observer.start()
        
        self.log("✅ File watcher started")
    
    def auto_reload(self):
        """Auto reload servers when files change"""
        self.log("🔄 Auto-reloading servers...")
        
        # Restart backend if needed
        if self.backend_process:
            self.backend_process.terminate()
            time.sleep(2)
            self.start_backend()
        
        # Frontend auto-reloads with Next.js hot reload
    
    def open_browsers(self):
        """Open development browsers"""
        self.log("🌐 Opening development browsers...")
        
        try:
            # Open frontend
            webbrowser.open('http://localhost:3001')
            self.log("✅ Opened frontend in browser")
            
            # Open backend
            webbrowser.open('http://localhost:8000')
            self.log("✅ Opened backend in browser")
            
        except Exception as e:
            self.log(f"⚠️ Error opening browsers: {e}", "WARNING")
    
    def monitor_services(self):
        """Monitor services and auto-restart if needed"""
        self.log("🔍 Starting service monitor...")
        
        while self.running:
            try:
                # Check frontend
                try:
                    response = requests.get('http://localhost:3001', timeout=5)
                    if response.status_code != 200:
                        self.log("⚠️ Frontend not responding, restarting...", "WARNING")
                        self.start_frontend()
                except:
                    self.log("⚠️ Frontend down, restarting...", "WARNING")
                    self.start_frontend()
                
                # Check backend
                try:
                    response = requests.get('http://localhost:8000', timeout=5)
                    if response.status_code != 200:
                        self.log("⚠️ Backend not responding, restarting...", "WARNING")
                        self.start_backend()
                except:
                    self.log("⚠️ Backend down, restarting...", "WARNING")
                    self.start_backend()
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log(f"⚠️ Monitor error: {e}", "WARNING")
                time.sleep(30)
    
    def start(self):
        """Start auto-managed development environment"""
        self.log("🏥 EHB Healthcare - Auto Development Manager")
        self.log("=" * 50)
        
        try:
            # Step 1: Start frontend
            if not self.start_frontend():
                return
            
            # Step 2: Start backend
            if not self.start_backend():
                return
            
            # Step 3: Setup file watcher
            self.setup_file_watcher()
            
            # Step 4: Open browsers
            time.sleep(5)
            self.open_browsers()
            
            # Step 5: Start service monitor
            monitor_thread = threading.Thread(target=self.monitor_services)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            self.log("🎉 Auto-managed development environment started!")
            self.log("✅ Real-time development active")
            self.log("✅ Auto-reload enabled")
            self.log("✅ Service monitoring active")
            self.log("🌐 Frontend: http://localhost:3001")
            self.log("🔧 Backend: http://localhost:8000")
            
            # Keep running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.log("🛑 Shutting down auto-managed environment...")
        except Exception as e:
            self.log(f"❌ System error: {e}", "ERROR")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup processes"""
        if self.frontend_process:
            self.frontend_process.terminate()
        if self.backend_process:
            self.backend_process.terminate()
        if self.observer:
            self.observer.stop()
            self.observer.join()

if __name__ == "__main__":
    manager = AutoDevManager()
    manager.start() 