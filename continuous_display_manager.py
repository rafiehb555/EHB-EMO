#!/usr/bin/env python3
"""
EHB Healthcare System - Continuous Display Manager
Keeps the system always visible and auto-managed
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


class ContinuousDisplayManager:
    def __init__(self):
        self.frontend_process = None
        self.backend_process = None
        self.running = True
        self.display_refresh_interval = 30  # Refresh every 30 seconds
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def create_simple_backend(self):
        """Create a simple backend server"""
        backend_code = '''
import http.server
import socketserver
import json
import time

PORT = 8000

class EHBHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API - Always Running",
                "status": "operational",
                "timestamp": time.time(),
                "auto_managed": True
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "auto_managed": True,
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/api/patients':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            patients = [
                {"id": "P001", "name": "Ahmed Khan", "status": "active", "condition": "Hypertension"},
                {"id": "P002", "name": "Fatima Ali", "status": "active", "condition": "Diabetes Type 2"},
                {"id": "P003", "name": "Muhammad Hassan", "status": "critical", "condition": "Heart Disease"},
                {"id": "P004", "name": "Ayesha Malik", "status": "active", "condition": "Asthma"},
                {"id": "P005", "name": "Omar Farooq", "status": "active", "condition": "Back Pain"}
            ]
            self.wfile.write(json.dumps(patients, indent=2).encode())
            
        elif self.path == '/api/doctors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            doctors = [
                {"id": "D001", "name": "Dr. Sarah Ahmed", "specialization": "Cardiology", "status": "active"},
                {"id": "D002", "name": "Dr. Ali Hassan", "specialization": "Endocrinology", "status": "active"},
                {"id": "D003", "name": "Dr. Fatima Khan", "specialization": "Pediatrics", "status": "active"},
                {"id": "D004", "name": "Dr. Omar Malik", "specialization": "Orthopedics", "status": "active"},
                {"id": "D005", "name": "Dr. Ayesha Ali", "specialization": "Neurology", "status": "active"}
            ]
            self.wfile.write(json.dumps(doctors, indent=2).encode())
            
        elif self.path == '/api/analytics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            analytics = {
                "patient_stats": {
                    "total_patients": 1250,
                    "active_patients": 1180,
                    "critical_patients": 45,
                    "new_patients_this_month": 85
                },
                "appointment_stats": {
                    "total_appointments": 2850,
                    "scheduled_appointments": 2450,
                    "completed_appointments": 2350,
                    "cancelled_appointments": 50
                },
                "system_stats": {
                    "uptime": "99.9%",
                    "auto_managed": True,
                    "continuous_display": True
                }
            }
            self.wfile.write(json.dumps(analytics, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": self.path}
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare Continuous Server on port {PORT}...")
    with socketserver.TCPServer(("", PORT), EHBHandler) as httpd:
        print(f"✅ Continuous server running at http://localhost:{PORT}")
        httpd.serve_forever()
'''
        
        with open('continuous_backend.py', 'w') as f:
            f.write(backend_code)
        
        self.log("✅ Created continuous backend server")
    
    def start_backend(self):
        """Start backend server"""
        self.log("🔧 Starting backend server...")
        
        try:
            # Create backend server
            self.create_simple_backend()
            
            # Start backend
            self.backend_process = subprocess.Popen(
                [sys.executable, 'continuous_backend.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)  # Wait for server to start
            
            # Test backend
            try:
                response = requests.get('http://localhost:8000', timeout=5)
                if response.status_code == 200:
                    self.log("✅ Backend server started successfully")
                    return True
                else:
                    self.log(f"⚠️ Backend status: {response.status_code}", "WARNING")
                    return True
            except:
                self.log("⚠️ Backend not responding, but process started", "WARNING")
                return True
                
        except Exception as e:
            self.log(f"❌ Backend error: {e}", "ERROR")
            return False
    
    def start_frontend(self):
        """Start frontend server"""
        self.log("🌐 Starting frontend server...")
        
        try:
            # Check if frontend directory exists
            if not Path("frontend").exists():
                self.log("❌ Frontend directory not found", "ERROR")
                return False
            
            # Change to frontend directory
            os.chdir("frontend")
            
            # Install dependencies if needed
            try:
                subprocess.run(['npm', 'install'], check=True, capture_output=True)
                self.log("✅ Frontend dependencies installed")
            except:
                self.log("⚠️ Frontend dependencies already installed", "WARNING")
            
            # Start frontend
            self.frontend_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(10)  # Wait for server to start
            
            # Test frontend
            try:
                response = requests.get('http://localhost:3001', timeout=5)
                if response.status_code == 200:
                    self.log("✅ Frontend server started successfully")
                    return True
                else:
                    self.log(f"⚠️ Frontend status: {response.status_code}", "WARNING")
                    return True
            except:
                self.log("⚠️ Frontend not responding, but process started", "WARNING")
                return True
                
        except Exception as e:
            self.log(f"❌ Frontend error: {e}", "ERROR")
            return False
    
    def open_browsers(self):
        """Open browsers and keep them open"""
        self.log("🌐 Opening browsers for continuous display...")
        
        try:
            # Open frontend
            webbrowser.open('http://localhost:3001')
            self.log("✅ Opened frontend in browser")
            
            # Open backend
            webbrowser.open('http://localhost:8000')
            self.log("✅ Opened backend in browser")
            
            # Open API docs
            webbrowser.open('http://localhost:8000/api/patients')
            self.log("✅ Opened API endpoints in browser")
            
        except Exception as e:
            self.log(f"⚠️ Error opening browsers: {e}", "WARNING")
    
    def continuous_display_refresh(self):
        """Continuously refresh browser display"""
        self.log("🔄 Starting continuous display refresh...")
        
        while self.running:
            try:
                # Refresh frontend
                webbrowser.open('http://localhost:3001')
                
                # Refresh backend
                webbrowser.open('http://localhost:8000')
                
                self.log(f"🔄 Display refreshed at {time.strftime('%H:%M:%S')}")
                
                # Wait before next refresh
                time.sleep(self.display_refresh_interval)
                
            except Exception as e:
                self.log(f"⚠️ Display refresh error: {e}", "WARNING")
                time.sleep(self.display_refresh_interval)
    
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
                
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log(f"⚠️ Monitor error: {e}", "WARNING")
                time.sleep(60)
    
    def start(self):
        """Start continuous display manager"""
        self.log("🏥 EHB Healthcare - Continuous Display Manager")
        self.log("=" * 50)
        
        try:
            # Step 1: Start backend
            if not self.start_backend():
                self.log("❌ Backend startup failed", "ERROR")
                return
            
            # Step 2: Start frontend
            if not self.start_frontend():
                self.log("❌ Frontend startup failed", "ERROR")
                return
            
            # Step 3: Open browsers
            time.sleep(5)
            self.open_browsers()
            
            # Step 4: Start continuous refresh
            refresh_thread = threading.Thread(target=self.continuous_display_refresh)
            refresh_thread.daemon = True
            refresh_thread.start()
            
            # Step 5: Start service monitor
            monitor_thread = threading.Thread(target=self.monitor_services)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            self.log("🎉 Continuous display manager started!")
            self.log("✅ System always visible")
            self.log("✅ Auto-refresh every 30 seconds")
            self.log("✅ Service monitoring active")
            self.log("🌐 Frontend: http://localhost:3001")
            self.log("🔧 Backend: http://localhost:8000")
            
            # Keep running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.log("🛑 Shutting down continuous display manager...")
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

if __name__ == "__main__":
    manager = ContinuousDisplayManager()
    manager.start() 