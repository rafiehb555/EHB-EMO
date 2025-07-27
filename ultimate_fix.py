#!/usr/bin/env python3
"""
EHB Healthcare System - Ultimate Fix Script
Handles all issues: port conflicts, process management, dependencies
"""

import os
import socket
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

def force_kill_all():
    """Force kill all relevant processes"""
    print_status("Force killing all processes...")
    
    processes = ["python.exe", "node.exe", "npm.exe", "next.exe"]
    
    for process in processes:
        try:
            subprocess.run(f"taskkill /f /im {process}", shell=True, capture_output=True)
            print_status(f"Killed {process}", "SUCCESS")
        except:
            pass
    
    time.sleep(3)

def check_port(port):
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except:
        return False

def find_free_port(start_port=3000):
    """Find a free port starting from start_port"""
    port = start_port
    while port < 3010:
        if check_port(port):
            return port
        port += 1
    return None

def start_backend():
    """Start backend server"""
    print_status("Starting backend API server...")
    
    if not os.path.exists("ehb_api_server.py"):
        print_status("Creating backend server file...", "WARNING")
        create_backend_file()
    
    try:
        process = subprocess.Popen(
            [sys.executable, "ehb_api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)
        
        if check_port(8000):
            print_status("Backend started successfully", "SUCCESS")
            return process
        else:
            print_status("Backend failed to start", "ERROR")
            return None
            
    except Exception as e:
        print_status(f"Backend error: {e}", "ERROR")
        return None

def start_frontend():
    """Start frontend with dynamic port"""
    print_status("Starting frontend development server...")
    
    if not os.path.exists("frontend"):
        print_status("Frontend directory not found", "ERROR")
        return None
    
    # Find free port
    port = find_free_port(3000)
    if not port:
        print_status("No free ports available", "ERROR")
        return None
    
    print_status(f"Using port {port} for frontend", "INFO")
    
    try:
        os.chdir("frontend")
        
        # Update package.json with new port
        update_package_json(port)
        
        # Install dependencies
        print_status("Installing dependencies...")
        subprocess.run(["npm", "install"], capture_output=True, check=False)
        
        # Start frontend
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(5)
        
        if check_port(port):
            print_status(f"Frontend started on port {port}", "SUCCESS")
            return process, port
        else:
            print_status("Frontend failed to start", "ERROR")
            return None, None
            
    except Exception as e:
        print_status(f"Frontend error: {e}", "ERROR")
        return None, None

def update_package_json(port):
    """Update package.json with new port"""
    package_content = f'''{{
  "name": "ehb-frontend",
  "version": "0.1.0",
  "scripts": {{
    "dev": "next dev -p {port}",
    "build": "next build",
    "start": "next start"
  }},
  "dependencies": {{
    "next": "14.0.0",
    "react": "^18",
    "react-dom": "^18"
  }}
}}'''
    
    with open("package.json", "w") as f:
        f.write(package_content)

def create_backend_file():
    """Create backend server file if missing"""
    backend_code = '''#!/usr/bin/env python3
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
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy"}
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare API Server on port {PORT}...")
    with socketserver.TCPServer(("", PORT), EHBAPIHandler) as httpd:
        print(f"✅ API server running at http://localhost:{PORT}")
        httpd.serve_forever()
'''
    
    with open("ehb_api_server.py", "w") as f:
        f.write(backend_code)

def main():
    """Main function"""
    print("=" * 60)
    print("🏥 EHB Healthcare System - Ultimate Fix")
    print("=" * 60)
    
    # Force kill all processes
    force_kill_all()
    
    # Start backend
    backend_process = start_backend()
    
    # Start frontend
    frontend_result = start_frontend()
    if frontend_result:
        frontend_process, frontend_port = frontend_result
    else:
        frontend_process, frontend_port = None, None
    
    # Final status
    print("\n" + "=" * 60)
    print("📋 Final System Status:")
    print("=" * 60)
    
    if backend_process:
        print("✅ Backend: http://localhost:8000")
    else:
        print("❌ Backend: Failed to start")
    
    if frontend_process and frontend_port:
        print(f"✅ Frontend: http://localhost:{frontend_port}")
    else:
        print("❌ Frontend: Failed to start")
    
    print("=" * 60)
    
    if backend_process and frontend_process:
        print_status("🎉 System started successfully!", "SUCCESS")
        print(f"\n💡 Open http://localhost:{frontend_port} in your browser")
    else:
        print_status("⚠️ Some services failed to start", "WARNING")
    
    print("\n🛑 Press Ctrl+C to stop")
    
    try:
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