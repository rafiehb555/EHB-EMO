#!/usr/bin/env python3
"""
EHB AI Dev Agent Live Deployment
Complete deployment script for EHB Healthcare Platform
"""

import json
import logging
import os
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ehb_live_deployment.log'),
        logging.StreamHandler()
    ]
)

class EHBLiveDeployment:
    def __init__(self):
        self.running = True
        self.frontend_process = None
        self.backend_process = None
        self.ports = {
            'frontend': 3000,
            'backend': 8000
        }
        self.services = {}
        
    def check_dependencies(self):
        """Check and install required dependencies"""
        logging.info("🔍 Checking dependencies...")
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"✅ Node.js found: {result.stdout.strip()}")
            else:
                logging.error("❌ Node.js not found!")
                return False
        except FileNotFoundError:
            logging.error("❌ Node.js not found!")
            return False
            
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"✅ npm found: {result.stdout.strip()}")
            else:
                logging.error("❌ npm not found!")
                return False
        except FileNotFoundError:
            logging.error("❌ npm not found!")
            return False
            
        # Check Python
        try:
            result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"✅ Python found: {result.stdout.strip()}")
            else:
                logging.error("❌ Python not found!")
                return False
        except FileNotFoundError:
            logging.error("❌ Python not found!")
            return False
            
        return True
        
    def install_dependencies(self):
        """Install npm dependencies"""
        logging.info("📦 Installing npm dependencies...")
        try:
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("✅ Dependencies installed successfully")
                return True
            else:
                logging.error(f"❌ Failed to install dependencies: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Error installing dependencies: {e}")
            return False
            
    def create_backend_server(self):
        """Create backend server"""
        backend_content = """from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "EHB Backend",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "healthy", 
        "api": "EHB API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/agents')
def get_agents():
    return jsonify({
        "agents": [
            {"id": 1, "name": "Healthcare Agent", "status": "active"},
            {"id": 2, "name": "Security Agent", "status": "active"},
            {"id": 3, "name": "Deployment Agent", "status": "active"},
            {"id": 4, "name": "Testing Agent", "status": "active"}
        ]
    })

@app.route('/api/status')
def get_status():
    return jsonify({
        "platform": "EHB Healthcare Platform",
        "version": "1.0.0",
        "status": "running",
        "services": {
            "frontend": "active",
            "backend": "active",
            "database": "connected"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/')
def home():
    return jsonify({
        "message": "EHB Healthcare Platform Backend",
        "version": "1.0.0",
        "status": "running"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting EHB Backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
"""
        
        with open("api_server.py", "w", encoding='utf-8') as f:
            f.write(backend_content)
        logging.info("✅ Backend server created")
        
    def start_backend(self):
        """Start backend server"""
        logging.info("🚀 Starting backend server...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "api_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(3)  # Wait for server to start
            
            # Test backend
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    logging.info("✅ Backend server started successfully")
                    return True
                else:
                    logging.error(f"❌ Backend health check failed: {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                logging.error(f"❌ Backend health check failed: {e}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Failed to start backend: {e}")
            return False
            
    def start_frontend(self):
        """Start frontend development server"""
        logging.info("🚀 Starting frontend server...")
        try:
            self.frontend_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(10)  # Wait for Next.js to start
            
            # Test frontend
            try:
                response = requests.get("http://localhost:3000", timeout=10)
                if response.status_code == 200:
                    logging.info("✅ Frontend server started successfully")
                    return True
                else:
                    logging.error(f"❌ Frontend health check failed: {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                logging.error(f"❌ Frontend health check failed: {e}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Failed to start frontend: {e}")
            return False
            
    def open_browser(self):
        """Open application in browser"""
        logging.info("🌐 Opening application in browser...")
        try:
            webbrowser.open("http://localhost:3000")
            logging.info("✅ Browser opened successfully")
        except Exception as e:
            logging.error(f"❌ Failed to open browser: {e}")
            
    def health_monitor(self):
        """Monitor health of services"""
        while self.running:
            try:
                # Check backend
                try:
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    if response.status_code != 200:
                        logging.warning("⚠️ Backend health check failed")
                except:
                    logging.warning("⚠️ Backend not responding")
                    
                # Check frontend
                try:
                    response = requests.get("http://localhost:3000", timeout=5)
                    if response.status_code != 200:
                        logging.warning("⚠️ Frontend health check failed")
                except:
                    logging.warning("⚠️ Frontend not responding")
                    
            except Exception as e:
                logging.error(f"❌ Health monitor error: {e}")
                
            time.sleep(30)  # Check every 30 seconds
            
    def run(self):
        """Main deployment process"""
        logging.info("🚀 Starting EHB AI Dev Agent Live Deployment...")
        
        # Check dependencies
        if not self.check_dependencies():
            logging.error("❌ Dependencies check failed")
            return False
            
        # Install dependencies
        if not self.install_dependencies():
            logging.error("❌ Dependency installation failed")
            return False
            
        # Create backend server
        self.create_backend_server()
        
        # Start backend
        if not self.start_backend():
            logging.error("❌ Backend startup failed")
            return False
            
        # Start frontend
        if not self.start_frontend():
            logging.error("❌ Frontend startup failed")
            return False
            
        # Start health monitor
        health_thread = threading.Thread(target=self.health_monitor, daemon=True)
        health_thread.start()
        
        # Open browser
        time.sleep(5)  # Wait a bit more
        self.open_browser()
        
        logging.info("🎉 EHB AI Dev Agent is now LIVE!")
        logging.info("📱 Frontend: http://localhost:3000")
        logging.info("🔧 Backend: http://localhost:8000")
        logging.info("📊 Health: http://localhost:8000/health")
        logging.info("🛑 Press Ctrl+C to stop")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("🛑 Shutting down...")
            self.running = False
            if self.frontend_process:
                self.frontend_process.terminate()
            if self.backend_process:
                self.backend_process.terminate()
                
        return True

def main():
    """Main function"""
    deployment = EHBLiveDeployment()
    success = deployment.run()
    
    if success:
        print("\n🎉 EHB AI Dev Agent successfully deployed!")
        print("🌐 Open http://localhost:3000 in your browser")
        print("📊 Monitor health at http://localhost:8000/health")
    else:
        print("\n❌ Deployment failed. Check logs for details.")
        
if __name__ == "__main__":
    main() 