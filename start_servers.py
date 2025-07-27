"""
Start EHB Healthcare Servers
Start both backend and frontend servers
"""

import logging
import os
import subprocess
import sys
import time
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerManager:
    """Manage backend and frontend servers"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.backend_process = None
        self.frontend_process = None
    
    def start_backend_server(self):
        """Start the backend server"""
        logger.info("🚀 Starting backend server...")
        
        try:
            # Check if api_server.py exists
            api_server = self.project_root / "api_server.py"
            if api_server.exists():
                self.backend_process = subprocess.Popen([
                    sys.executable, str(api_server)
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                logger.info("✅ Backend server started")
                return True
            else:
                logger.error("❌ api_server.py not found")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to start backend server: {e}")
            return False
    
    def start_frontend_server(self):
        """Start the frontend server"""
        logger.info("🚀 Starting frontend server...")
        
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            logger.error("❌ Frontend directory not found")
            return False
        
        try:
            # Check if package.json exists
            package_json = frontend_dir / "package.json"
            if not package_json.exists():
                logger.error("❌ package.json not found in frontend directory")
                return False
            
            # Install dependencies if node_modules doesn't exist
            node_modules = frontend_dir / "node_modules"
            if not node_modules.exists():
                logger.info("📦 Installing frontend dependencies...")
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            
            # Start the development server
            self.frontend_process = subprocess.Popen([
                "npm", "run", "dev"
            ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            logger.info("✅ Frontend server started")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start frontend server: {e}")
            return False
    
    def check_server_status(self, url, name):
        """Check if server is responding"""
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ {name} server is responding")
                return True
            else:
                logger.warning(f"⚠️ {name} server returned status {response.status_code}")
                return False
        except:
            logger.warning(f"⚠️ {name} server is not responding")
            return False
    
    def wait_for_servers(self):
        """Wait for servers to start"""
        logger.info("⏳ Waiting for servers to start...")
        
        backend_ready = False
        frontend_ready = False
        
        for i in range(30):  # Wait up to 30 seconds
            if not backend_ready:
                backend_ready = self.check_server_status("http://localhost:8000/", "Backend")
            
            if not frontend_ready:
                frontend_ready = self.check_server_status("http://localhost:3001/", "Frontend")
            
            if backend_ready and frontend_ready:
                break
            
            time.sleep(1)
        
        return backend_ready, frontend_ready
    
    def run_servers(self):
        """Start both servers"""
        logger.info("🚀 Starting EHB Healthcare System...")
        
        print("\n" + "="*60)
        print("🏥 EHB Healthcare System - Server Startup")
        print("="*60)
        
        # Start backend server
        print("\n1️⃣ Starting backend server...")
        backend_started = self.start_backend_server()
        
        # Start frontend server
        print("\n2️⃣ Starting frontend server...")
        frontend_started = self.start_frontend_server()
        
        # Wait for servers to be ready
        print("\n3️⃣ Waiting for servers to be ready...")
        backend_ready, frontend_ready = self.wait_for_servers()
        
        print("\n" + "="*60)
        print("📊 Server Status:")
        print(f"Backend Server: {'✅ Running' if backend_ready else '❌ Not responding'}")
        print(f"Frontend Server: {'✅ Running' if frontend_ready else '❌ Not responding'}")
        
        if backend_ready and frontend_ready:
            print("\n🎉 All servers are running!")
            print("🌐 Access URLs:")
            print("   Frontend: http://localhost:3001")
            print("   Backend API: http://localhost:8000")
            print("   API Docs: http://localhost:8000/docs")
        else:
            print("\n⚠️ Some servers may not be running properly")
            if not backend_ready:
                print("   - Backend server may need manual start")
            if not frontend_ready:
                print("   - Frontend server may need manual start")
        
        print("="*60)
        
        # Keep the script running
        try:
            while True:
                time.sleep(10)
                backend_ready = self.check_server_status("http://localhost:8000/", "Backend")
                frontend_ready = self.check_server_status("http://localhost:3001/", "Frontend")
                
                if not backend_ready or not frontend_ready:
                    logger.warning("⚠️ Some servers stopped responding")
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down servers...")
            if self.backend_process:
                self.backend_process.terminate()
            if self.frontend_process:
                self.frontend_process.terminate()

def main():
    """Main function"""
    manager = ServerManager()
    manager.run_servers()

if __name__ == "__main__":
    main() 