#!/usr/bin/env python3
"""
EHB Auto Runner - Automatically runs frontend and backend on separate ports
Real-time monitoring and auto-restart functionality
"""

import json
import logging
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import requests


class EHBAutoRunner:
    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_port = 3000
        self.backend_port = 8000
        self.frontend_process = None
        self.backend_process = None
        self.running = True
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('auto_runner.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def start_backend_server(self):
        """Start backend API server"""
        try:
            self.logger.info("🚀 Starting Backend Server on port 8000...")
            
            # Change to project root
            os.chdir(self.project_root)
            
            # Start backend server
            self.backend_process = subprocess.Popen([
                sys.executable, "api_server.py", "--port", str(self.backend_port), "--debug"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.logger.info("✅ Backend Server started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start backend server: {e}")
            return False

    def start_frontend_server(self):
        """Start frontend development server"""
        try:
            self.logger.info("🎨 Starting Frontend Server on port 3000...")
            
            # Change to frontend directory
            frontend_dir = self.project_root / "frontend"
            os.chdir(frontend_dir)
            
            # First, fix the Heroicons issue
            self.logger.info("🔧 Fixing Heroicons dependency...")
            try:
                # Remove problematic heroicons
                subprocess.run(["npm", "uninstall", "@heroicons/react"], 
                             capture_output=True, text=True)
                # Install a working version
                subprocess.run(["npm", "install", "@heroicons/react@2.0.18"], 
                             capture_output=True, text=True)
                self.logger.info("✅ Heroicons fixed successfully")
            except Exception as e:
                self.logger.warning(f"⚠️ Heroicons fix warning: {e}")
            
            # Start frontend server with full npm path
            npm_path = "npm"  # Try to find npm in PATH
            try:
                # Try to find npm in common locations
                import shutil
                npm_path = shutil.which("npm")
                if not npm_path:
                    npm_path = "npm"  # Fallback
            except:
                npm_path = "npm"
            
            self.logger.info(f"🔧 Using npm path: {npm_path}")
            
            # Start frontend server
            self.frontend_process = subprocess.Popen([
                npm_path, "run", "dev"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.logger.info("✅ Frontend Server started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start frontend server: {e}")
            return False

    def check_server_health(self, port, server_name):
        """Check if server is healthy"""
        try:
            if port == self.backend_port:
                response = requests.get(f"http://localhost:{port}/api/health", timeout=5)
            else:
                response = requests.get(f"http://localhost:{port}", timeout=5)
            
            if response.status_code == 200:
                self.logger.info(f"✅ {server_name} is healthy")
                return True
            else:
                self.logger.warning(f"⚠️ {server_name} returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ {server_name} health check failed: {e}")
            return False

    def monitor_servers(self):
        """Monitor both servers and restart if needed"""
        while self.running:
            try:
                # Check backend
                backend_healthy = self.check_server_health(self.backend_port, "Backend Server")
                
                # Check frontend
                frontend_healthy = self.check_server_health(self.frontend_port, "Frontend Server")
                
                # If any server is down, restart it
                if not backend_healthy and self.backend_process:
                    self.logger.warning("🔄 Restarting Backend Server...")
                    self.backend_process.terminate()
                    time.sleep(2)
                    self.start_backend_server()
                
                if not frontend_healthy and self.frontend_process:
                    self.logger.warning("🔄 Restarting Frontend Server...")
                    self.frontend_process.terminate()
                    time.sleep(2)
                    self.start_frontend_server()
                
                # Wait before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Stopping server monitoring...")
                break
            except Exception as e:
                self.logger.error(f"❌ Monitoring error: {e}")
                time.sleep(10)

    def open_browsers(self):
        """Open browsers to both servers"""
        try:
            import webbrowser

            # Wait a bit for servers to start
            time.sleep(5)
            
            # Open backend API docs
            webbrowser.open(f"http://localhost:{self.backend_port}/api/health")
            self.logger.info(f"🌐 Opened Backend API: http://localhost:{self.backend_port}")
            
            # Open frontend app
            webbrowser.open(f"http://localhost:{self.frontend_port}")
            self.logger.info(f"🌐 Opened Frontend App: http://localhost:{self.frontend_port}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to open browsers: {e}")

    def generate_status_report(self):
        """Generate status report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "backend": {
                "port": self.backend_port,
                "url": f"http://localhost:{self.backend_port}",
                "health_url": f"http://localhost:{self.backend_port}/api/health",
                "status": "running" if self.backend_process else "stopped"
            },
            "frontend": {
                "port": self.frontend_port,
                "url": f"http://localhost:{self.frontend_port}",
                "status": "running" if self.frontend_process else "stopped"
            },
            "system": {
                "project_root": str(self.project_root),
                "auto_restart": True,
                "monitoring": True
            }
        }
        
        with open("auto_runner_status.json", "w") as f:
            json.dump(report, f, indent=2)
        
        self.logger.info("📊 Status report generated: auto_runner_status.json")
        return report

    def run(self):
        """Main run method"""
        print("=" * 60)
        print("🚀 EHB Auto Runner - Starting Both Servers")
        print("=" * 60)
        
        # Start backend server
        if not self.start_backend_server():
            self.logger.error("❌ Failed to start backend server")
            return False
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Start frontend server
        if not self.start_frontend_server():
            self.logger.error("❌ Failed to start frontend server")
            return False
        
        # Wait a bit for frontend to start
        time.sleep(5)
        
        # Open browsers
        self.open_browsers()
        
        # Generate status report
        status = self.generate_status_report()
        
        print("=" * 60)
        print("✅ EHB Auto Runner Started Successfully!")
        print("=" * 60)
        print(f"🔧 Backend Server: http://localhost:{self.backend_port}")
        print(f"🎨 Frontend Server: http://localhost:{self.frontend_port}")
        print(f"📊 Health Check: http://localhost:{self.backend_port}/api/health")
        print("=" * 60)
        print("🔄 Auto-monitoring enabled - servers will restart automatically")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Start monitoring in separate thread
        monitor_thread = threading.Thread(target=self.monitor_servers)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("🛑 Stopping EHB Auto Runner...")
            self.running = False
            
            # Stop servers
            if self.backend_process:
                self.backend_process.terminate()
            if self.frontend_process:
                self.frontend_process.terminate()
            
            print("✅ EHB Auto Runner stopped successfully")

def main():
    """Main function"""
    runner = EHBAutoRunner()
    runner.run()

if __name__ == "__main__":
    main() 