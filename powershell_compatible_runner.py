#!/usr/bin/env python3
"""
EHB Healthcare System - PowerShell Compatible Runner
Handles PowerShell command execution properly
"""

import os
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime


class PowerShellCompatibleRunner:
    def __init__(self):
        self.running = True
        self.frontend_process = None
        self.backend_process = None
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_powershell_command(self, command, cwd=None):
        """Run PowerShell command properly"""
        try:
            if cwd:
                os.chdir(cwd)
            
            # Use PowerShell executable
            result = subprocess.run(
                ['powershell', '-Command', command],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.log(f"❌ PowerShell command failed: {e}", "ERROR")
            return None
    
    def kill_processes_powershell(self):
        """Kill processes using PowerShell"""
        self.log("🛑 Killing processes using PowerShell...")
        
        commands = [
            "Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force",
            "Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force",
            "Get-Process npm -ErrorAction SilentlyContinue | Stop-Process -Force"
        ]
        
        for cmd in commands:
            try:
                self.run_powershell_command(cmd)
            except Exception as e:
                self.log(f"⚠️ Error killing process: {e}", "WARNING")
        
        self.log("✅ Processes killed using PowerShell")
    
    def start_backend_powershell(self):
        """Start backend using PowerShell"""
        self.log("🔧 Starting backend using PowerShell...")
        
        try:
            # Create backend server if not exists
            if not os.path.exists('ehb_api_server.py'):
                self.create_backend_server()
            
            # Start backend using PowerShell
            command = "python ehb_api_server.py"
            self.backend_process = subprocess.Popen(
                ['powershell', '-Command', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(3)
            self.log("✅ Backend started using PowerShell")
            return True
            
        except Exception as e:
            self.log(f"❌ Backend error: {e}", "ERROR")
            return False
    
    def start_frontend_powershell(self):
        """Start frontend using PowerShell"""
        self.log("🌐 Starting frontend using PowerShell...")
        
        try:
            # Change to frontend directory
            if os.path.exists("frontend"):
                os.chdir("frontend")
                
                # Install dependencies
                self.run_powershell_command("npm install")
                
                # Start frontend
                command = "npm run dev"
                self.frontend_process = subprocess.Popen(
                    ['powershell', '-Command', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                time.sleep(10)
                self.log("✅ Frontend started using PowerShell")
                return True
            else:
                self.log("❌ Frontend directory not found", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Frontend error: {e}", "ERROR")
            return False
    
    def create_backend_server(self):
        """Create backend server file"""
        self.log("📄 Creating backend server...")
        
        backend_code = '''
import http.server
import socketserver
import json
from datetime import datetime

PORT = 8000

class EHBAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API Server",
                "status": "operational",
                "timestamp": datetime.now().isoformat()
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
            
        elif self.path == '/api/doctors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            doctors = [
                {"id": "D001", "name": "Dr. Sarah Ahmed", "specialization": "Cardiology"},
                {"id": "D002", "name": "Dr. Ali Hassan", "specialization": "Endocrinology"},
                {"id": "D003", "name": "Dr. Fatima Khan", "specialization": "Pediatrics"}
            ]
            self.wfile.write(json.dumps(doctors, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": self.path}
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare API Server on port {PORT}...")
    with socketserver.TCPServer(("", PORT), EHBAPIHandler) as httpd:
        print(f"✅ API server running at http://localhost:{PORT}")
        httpd.serve_forever()
'''
        
        with open('ehb_api_server.py', 'w') as f:
            f.write(backend_code)
        
        self.log("✅ Backend server created")
    
    def open_browsers_powershell(self):
        """Open browsers using PowerShell"""
        self.log("🌐 Opening browsers using PowerShell...")
        
        try:
            # Open browsers using PowerShell
            commands = [
                "Start-Process 'http://localhost:3001'",
                "Start-Process 'http://localhost:8000'",
                "Start-Process 'http://localhost:8000/api/patients'"
            ]
            
            for cmd in commands:
                self.run_powershell_command(cmd)
                time.sleep(1)
            
            self.log("✅ Browsers opened using PowerShell")
            
        except Exception as e:
            self.log(f"⚠️ Error opening browsers: {e}", "WARNING")
    
    def continuous_monitor_powershell(self):
        """Monitor services using PowerShell"""
        self.log("🔍 Starting PowerShell monitor...")
        
        while self.running:
            try:
                # Check if processes are running
                check_commands = [
                    "Get-Process python -ErrorAction SilentlyContinue | Select-Object ProcessName",
                    "Get-Process node -ErrorAction SilentlyContinue | Select-Object ProcessName"
                ]
                
                for cmd in check_commands:
                    result = self.run_powershell_command(cmd)
                    if not result:
                        self.log("⚠️ Process not found, restarting...", "WARNING")
                        self.start_backend_powershell()
                        self.start_frontend_powershell()
                
                time.sleep(30)
                
            except Exception as e:
                self.log(f"⚠️ Monitor error: {e}", "WARNING")
                time.sleep(30)
    
    def start(self):
        """Start PowerShell compatible runner"""
        self.log("🏥 EHB Healthcare - PowerShell Compatible Runner")
        self.log("=" * 50)
        
        try:
            # Step 1: Kill existing processes
            self.kill_processes_powershell()
            
            # Step 2: Start backend
            if not self.start_backend_powershell():
                self.log("❌ Backend startup failed", "ERROR")
                return
            
            # Step 3: Start frontend
            if not self.start_frontend_powershell():
                self.log("❌ Frontend startup failed", "ERROR")
                return
            
            # Step 4: Open browsers
            time.sleep(5)
            self.open_browsers_powershell()
            
            # Step 5: Start monitor
            monitor_thread = threading.Thread(target=self.continuous_monitor_powershell)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            self.log("🎉 PowerShell compatible runner started!")
            self.log("✅ All commands using PowerShell")
            self.log("✅ No more && operator errors")
            self.log("🌐 Frontend: http://localhost:3001")
            self.log("🔧 Backend: http://localhost:8000")
            
            # Keep running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.log("🛑 Shutting down PowerShell runner...")
        except Exception as e:
            self.log(f"❌ System error: {e}", "ERROR")

if __name__ == "__main__":
    runner = PowerShellCompatibleRunner()
    runner.start() 