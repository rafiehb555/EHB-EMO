#!/usr/bin/env python3
"""
EHB Auto Development Script
Automatically runs when cursor is started
"""

import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cursor_agent.log'),
        logging.StreamHandler()
    ]
)

class CursorLiveAgent:
    def __init__(self):
        self.running = True
        self.frontend_process = None
        self.backend_process = None
        self.health_check_thread = None
        self.auto_fix_thread = None
        self.ports = {
            'frontend': 3000,
            'backend': 8000
        }
        self.setup_signal_handlers()
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logging.info("Shutdown signal received, cleaning up...")
        self.running = False
        self.cleanup()
        sys.exit(0)
        
    def cleanup(self):
        """Clean up processes"""
        if self.frontend_process:
            self.frontend_process.terminate()
        if self.backend_process:
            self.backend_process.terminate()
            
    def check_port_available(self, port):
        """Check if port is available"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except:
            return False
            
    def kill_process_on_port(self, port):
        """Kill process using specific port"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    for conn in proc.connections():
                        if conn.laddr.port == port:
                            proc.terminate()
                            logging.info(f"Killed process on port {port}")
                            time.sleep(2)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            logging.error(f"Error killing process on port {port}: {e}")
            
    def start_backend(self):
        """Start backend server"""
        try:
            if not self.check_port_available(self.ports['backend']):
                self.kill_process_on_port(self.ports['backend'])
                time.sleep(2)
                
            logging.info("Starting backend server...")
            self.backend_process = subprocess.Popen(
                [sys.executable, "api_server.py"],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to start
            time.sleep(5)
            if self.backend_process.poll() is None:
                logging.info("Backend server started successfully")
                return True
            else:
                logging.error("Backend server failed to start")
                return False
        except Exception as e:
            logging.error(f"Error starting backend: {e}")
            return False
            
    def start_frontend(self):
        """Start frontend server"""
        try:
            if not self.check_port_available(self.ports['frontend']):
                self.kill_process_on_port(self.ports['frontend'])
                time.sleep(2)
                
            logging.info("Starting frontend server...")
            
            # Check if we're in the frontend directory
            frontend_dir = "frontend" if os.path.exists("frontend") else "."
            
            # Install dependencies if needed
            if os.path.exists(os.path.join(frontend_dir, "package.json")):
                logging.info("Installing frontend dependencies...")
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for frontend to start
            time.sleep(10)
            if self.frontend_process.poll() is None:
                logging.info("Frontend server started successfully")
                return True
            else:
                logging.error("Frontend server failed to start")
                return False
        except Exception as e:
            logging.error(f"Error starting frontend: {e}")
            return False
            
    def health_check(self):
        """Continuous health check for servers"""
        while self.running:
            try:
                # Check backend
                try:
                    response = requests.get(f"http://localhost:{self.ports['backend']}/health", timeout=5)
                    if response.status_code != 200:
                        logging.warning("Backend health check failed, restarting...")
                        self.restart_backend()
                except:
                    logging.warning("Backend not responding, restarting...")
                    self.restart_backend()
                    
                # Check frontend
                try:
                    response = requests.get(f"http://localhost:{self.ports['frontend']}", timeout=5)
                    if response.status_code != 200:
                        logging.warning("Frontend health check failed, restarting...")
                        self.restart_frontend()
                except:
                    logging.warning("Frontend not responding, restarting...")
                    self.restart_frontend()
                    
            except Exception as e:
                logging.error(f"Health check error: {e}")
                
            time.sleep(30)  # Check every 30 seconds
            
    def restart_backend(self):
        """Restart backend server"""
        if self.backend_process:
            self.backend_process.terminate()
            time.sleep(3)
        self.start_backend()
        
    def restart_frontend(self):
        """Restart frontend server"""
        if self.frontend_process:
            self.frontend_process.terminate()
            time.sleep(3)
        self.start_frontend()
        
    def auto_fix_errors(self):
        """Automatically fix common errors"""
        while self.running:
            try:
                # Check for common error patterns
                self.fix_common_errors()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logging.error(f"Auto-fix error: {e}")
                
    def fix_common_errors(self):
        """Fix common development errors"""
        try:
            # Fix missing dependencies
            self.install_missing_deps()
            
            # Fix environment issues
            self.setup_environment()
            
            # Fix port conflicts
            self.resolve_port_conflicts()
            
            # Fix file permission issues
            self.fix_permissions()
            
        except Exception as e:
            logging.error(f"Error in auto-fix: {e}")
            
    def install_missing_deps(self):
        """Install missing dependencies"""
        try:
            # Install Python dependencies
            if os.path.exists("requirements.txt"):
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
                
            # Install Node.js dependencies
            if os.path.exists("package.json"):
                subprocess.run(["npm", "install"], check=True)
                
            if os.path.exists("frontend/package.json"):
                subprocess.run(["npm", "install"], cwd="frontend", check=True)
                
        except Exception as e:
            logging.error(f"Error installing dependencies: {e}")
            
    def setup_environment(self):
        """Setup environment files"""
        try:
            # Create .env.local if it doesn't exist
            if not os.path.exists(".env.local") and os.path.exists(".env.example"):
                import shutil
                shutil.copy(".env.example", ".env.local")
                logging.info("Created .env.local from .env.example")
                
        except Exception as e:
            logging.error(f"Error setting up environment: {e}")
            
    def resolve_port_conflicts(self):
        """Resolve port conflicts"""
        for port_name, port in self.ports.items():
            if not self.check_port_available(port):
                logging.info(f"Port {port} is in use, killing process...")
                self.kill_process_on_port(port)
                
    def fix_permissions(self):
        """Fix file permission issues"""
        try:
            # Make sure log files are writable
            log_files = ["cursor_agent.log", "api_server.log", "auto_agent.log"]
            for log_file in log_files:
                if os.path.exists(log_file):
                    os.chmod(log_file, 0o666)
                    
        except Exception as e:
            logging.error(f"Error fixing permissions: {e}")
            
    def open_browser(self):
        """Open browser to the application"""
        try:
            import webbrowser
            webbrowser.open(f"http://localhost:{self.ports['frontend']}")
            logging.info("Opened browser to application")
        except Exception as e:
            logging.error(f"Error opening browser: {e}")
            
    def run(self):
        """Main run method"""
        logging.info("🚀 Cursor Live Agent Starting...")
        
        # Start servers
        if not self.start_backend():
            logging.error("Failed to start backend")
            return
            
        if not self.start_frontend():
            logging.error("Failed to start frontend")
            return
            
        # Start health check thread
        self.health_check_thread = threading.Thread(target=self.health_check, daemon=True)
        self.health_check_thread.start()
        
        # Start auto-fix thread
        self.auto_fix_thread = threading.Thread(target=self.auto_fix_errors, daemon=True)
        self.auto_fix_thread.start()
        
        # Open browser
        time.sleep(5)
        self.open_browser()
        
        logging.info("✅ Cursor Live Agent is running! App will stay live automatically.")
        logging.info("🔧 Auto-fix is enabled - errors will be fixed automatically")
        logging.info("📊 Health monitoring is active")
        logging.info("🔄 Servers will restart automatically if they crash")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Shutdown requested...")
            self.running = False
            self.cleanup()

def main():
    """Main function"""
    agent = CursorLiveAgent()
    agent.run()

if __name__ == "__main__":
    main()
