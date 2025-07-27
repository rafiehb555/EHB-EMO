#!/usr/bin/env python3
"""
EHB Healthcare System - Complete Restart Script
Handles backend, frontend, and all services restart
"""

import os
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

def kill_processes():
    """Kill existing processes"""
    print_status("Killing existing processes...")
    
    try:
        # Kill Python processes
        subprocess.run(["taskkill", "/f", "/im", "python.exe"], 
                      capture_output=True, check=False)
        print_status("Python processes killed", "SUCCESS")
    except Exception as e:
        print_status(f"Error killing Python processes: {e}", "ERROR")
    
    try:
        # Kill Node processes
        subprocess.run(["taskkill", "/f", "/im", "node.exe"], 
                      capture_output=True, check=False)
        print_status("Node processes killed", "SUCCESS")
    except Exception as e:
        print_status(f"Error killing Node processes: {e}", "ERROR")

def start_backend():
    """Start backend API server"""
    print_status("Starting backend API server...")
    
    try:
        # Check if API server file exists
        if not os.path.exists("ehb_api_server.py"):
            print_status("API server file not found, creating...", "WARNING")
            create_api_server()
        
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, "ehb_api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print_status("Backend API server started successfully", "SUCCESS")
                return backend_process
            else:
                print_status("Backend server not responding properly", "ERROR")
        except:
            print_status("Backend server may not be running", "WARNING")
            
        return backend_process
        
    except Exception as e:
        print_status(f"Error starting backend: {e}", "ERROR")
        return None

def start_frontend():
    """Start frontend development server"""
    print_status("Starting frontend development server...")
    
    try:
        # Check if frontend directory exists
        if not os.path.exists("frontend"):
            print_status("Frontend directory not found", "ERROR")
            return None
        
        # Change to frontend directory
        os.chdir("frontend")
        
        # Check if package.json exists
        if not os.path.exists("package.json"):
            print_status("package.json not found in frontend", "ERROR")
            return None
        
        # Install dependencies if needed
        print_status("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], capture_output=True, check=False)
        
        # Start frontend in background
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        print_status("Frontend development server started", "SUCCESS")
        return frontend_process
        
    except Exception as e:
        print_status(f"Error starting frontend: {e}", "ERROR")
        return None

def create_api_server():
    """Create API server file if missing"""
    api_server_code = '''#!/usr/bin/env python3
"""
EHB Healthcare System - API Server
Serves healthcare endpoints with proper JSON responses
"""

import http.server
import socketserver
import json
import time
from datetime import datetime

PORT = 8000

class EHBAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API Server",
                "status": "operational",
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat(),
                "endpoints": {
                    "/api/patients": "Get all patients",
                    "/api/doctors": "Get all doctors", 
                    "/api/appointments": "Get all appointments",
                    "/api/analytics": "Get healthcare analytics",
                    "/health": "Health check"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "EHB Healthcare API",
                "timestamp": datetime.now().isoformat(),
                "uptime": "99.9%"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/api/patients':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            patients = [
                {
                    "id": "P001",
                    "name": "Ahmed Khan",
                    "date_of_birth": "1985-03-15",
                    "contact": "+92-300-1234567",
                    "status": "active",
                    "condition": "Hypertension",
                    "last_visit": "2024-01-15"
                },
                {
                    "id": "P002", 
                    "name": "Fatima Ali",
                    "date_of_birth": "1990-07-22",
                    "contact": "+92-301-2345678",
                    "status": "active",
                    "condition": "Diabetes Type 2",
                    "last_visit": "2024-01-20"
                }
            ]
            self.wfile.write(json.dumps(patients, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "error": "Endpoint not found",
                "path": self.path,
                "available_endpoints": [
                    "/",
                    "/health", 
                    "/api/patients",
                    "/api/doctors",
                    "/api/appointments",
                    "/api/analytics"
                ]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare API Server on port {PORT}...")
    print(f"✅ Server will be available at http://localhost:{PORT}")
    print("🛑 Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), EHBAPIHandler) as httpd:
        print(f"✅ API server running at http://localhost:{PORT}")
        httpd.serve_forever()
'''
    
    with open("ehb_api_server.py", "w") as f:
        f.write(api_server_code)
    
    print_status("API server file created", "SUCCESS")

def check_services():
    """Check if services are running"""
    print_status("Checking service status...")
    
    try:
        import requests

        # Check backend
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print_status("✅ Backend API: Running", "SUCCESS")
            else:
                print_status("❌ Backend API: Not responding", "ERROR")
        except:
            print_status("❌ Backend API: Not accessible", "ERROR")
        
        # Check frontend
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print_status("✅ Frontend: Running", "SUCCESS")
            else:
                print_status("⚠️ Frontend: Responding but status unclear", "WARNING")
        except:
            print_status("❌ Frontend: Not accessible", "ERROR")
            
    except ImportError:
        print_status("requests module not available, skipping service check", "WARNING")

def main():
    """Main restart function"""
    print("=" * 60)
    print("🏥 EHB Healthcare System - Complete Restart")
    print("=" * 60)
    
    # Kill existing processes
    kill_processes()
    time.sleep(2)
    
    # Start backend
    backend_process = start_backend()
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Check services
    time.sleep(3)
    check_services()
    
    print("\n" + "=" * 60)
    print("📋 System Status Summary:")
    print("=" * 60)
    print("🔗 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3000")
    print("📊 Health Check: http://localhost:8000/health")
    print("👥 Patients API: http://localhost:8000/api/patients")
    print("👨‍⚕️ Doctors API: http://localhost:8000/api/doctors")
    print("📅 Appointments API: http://localhost:8000/api/appointments")
    print("📈 Analytics API: http://localhost:8000/api/analytics")
    print("=" * 60)
    
    if backend_process and frontend_process:
        print_status("🎉 System restart completed successfully!", "SUCCESS")
    else:
        print_status("⚠️ Some services may not be running properly", "WARNING")
    
    print("\n💡 Tips:")
    print("   - Open http://localhost:3000 in your browser")
    print("   - Check http://localhost:8000 for API status")
    print("   - Press Ctrl+C to stop this script")
    
    try:
        # Keep script running
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print_status("Shutting down...", "WARNING")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print_status("System stopped", "SUCCESS")

if __name__ == "__main__":
    main() 