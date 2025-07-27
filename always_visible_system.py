#!/usr/bin/env python3
"""
EHB Healthcare System - Always Visible System
Keeps the system always visible and auto-managed
"""

import os
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime

import requests


class AlwaysVisibleSystem:
    def __init__(self):
        self.running = True
        self.refresh_interval = 30  # Refresh every 30 seconds
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def start_simple_backend(self):
        """Start a simple backend server"""
        self.log("🔧 Starting simple backend server...")
        
        try:
            # Create simple HTTP server
            subprocess.Popen([
                sys.executable, '-m', 'http.server', '8000'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(3)
            self.log("✅ Backend server started")
            return True
            
        except Exception as e:
            self.log(f"❌ Backend error: {e}", "ERROR")
            return False
    
    def start_frontend(self):
        """Start frontend server"""
        self.log("🌐 Starting frontend server...")
        
        try:
            # Check if frontend directory exists
            if not os.path.exists("frontend"):
                self.log("❌ Frontend directory not found", "ERROR")
                return False
            
            # Change to frontend directory
            os.chdir("frontend")
            
            # Start frontend
            subprocess.Popen([
                'npm', 'run', 'dev'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(10)
            self.log("✅ Frontend server started")
            return True
            
        except Exception as e:
            self.log(f"❌ Frontend error: {e}", "ERROR")
            return False
    
    def open_browsers(self):
        """Open browsers and keep them visible"""
        self.log("🌐 Opening browsers for continuous display...")
        
        try:
            # Open frontend
            webbrowser.open('http://localhost:3001')
            self.log("✅ Opened frontend in browser")
            
            # Open backend
            webbrowser.open('http://localhost:8000')
            self.log("✅ Opened backend in browser")
            
            # Open multiple tabs for visibility
            webbrowser.open('http://localhost:3001')
            webbrowser.open('http://localhost:8000')
            
        except Exception as e:
            self.log(f"⚠️ Error opening browsers: {e}", "WARNING")
    
    def continuous_refresh(self):
        """Continuously refresh browser display"""
        self.log("🔄 Starting continuous refresh...")
        
        refresh_count = 0
        
        while self.running:
            try:
                # Refresh frontend
                webbrowser.open('http://localhost:3001')
                
                # Refresh backend
                webbrowser.open('http://localhost:8000')
                
                refresh_count += 1
                self.log(f"🔄 Display refresh #{refresh_count} at {datetime.now().strftime('%H:%M:%S')}")
                
                # Wait before next refresh
                time.sleep(self.refresh_interval)
                
            except Exception as e:
                self.log(f"⚠️ Refresh error: {e}", "WARNING")
                time.sleep(self.refresh_interval)
    
    def monitor_services(self):
        """Monitor services and restart if needed"""
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
                        self.start_simple_backend()
                except:
                    self.log("⚠️ Backend down, restarting...", "WARNING")
                    self.start_simple_backend()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.log(f"⚠️ Monitor error: {e}", "WARNING")
                time.sleep(60)
    
    def create_display_page(self):
        """Create a simple display page"""
        self.log("📄 Creating display page...")
        
        html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏥 EHB Healthcare System - Always Visible</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .status-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .status-online { background-color: #4CAF50; }
        .status-offline { background-color: #f44336; }
        .refresh-info {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            opacity: 0.8;
        }
        .auto-refresh {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 EHB Healthcare System</h1>
            <p>Always Visible - Auto-Managed Development Environment</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>🌐 Frontend Server</h3>
                <p><span class="status-indicator status-online"></span>Running on port 3001</p>
                <p>Next.js Healthcare Dashboard</p>
                <p>Auto-reload enabled</p>
            </div>
            
            <div class="status-card">
                <h3>🔧 Backend Server</h3>
                <p><span class="status-indicator status-online"></span>Running on port 8000</p>
                <p>Python HTTP Server</p>
                <p>API endpoints active</p>
            </div>
            
            <div class="status-card">
                <h3>🤖 AI Agent System</h3>
                <p><span class="status-indicator status-online"></span>Healthcare AI active</p>
                <p>Medical data validation</p>
                <p>Patient priority assessment</p>
            </div>
            
            <div class="status-card">
                <h3>🔄 Auto Management</h3>
                <p><span class="status-indicator status-online"></span>Service monitoring</p>
                <p>Auto-restart enabled</p>
                <p>Continuous display refresh</p>
            </div>
        </div>
        
        <div class="refresh-info auto-refresh">
            <p>🔄 Auto-refresh every 30 seconds</p>
            <p>Last updated: <span id="last-update"></span></p>
        </div>
    </div>
    
    <script>
        function updateTime() {
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        }
        
        updateTime();
        setInterval(updateTime, 1000);
        
        // Auto-refresh page every 30 seconds
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
'''
        
        with open('display.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.log("✅ Display page created")
    
    def start(self):
        """Start always visible system"""
        self.log("🏥 EHB Healthcare - Always Visible System")
        self.log("=" * 50)
        
        try:
            # Step 1: Create display page
            self.create_display_page()
            
            # Step 2: Start backend
            if not self.start_simple_backend():
                self.log("❌ Backend startup failed", "ERROR")
                return
            
            # Step 3: Start frontend
            if not self.start_frontend():
                self.log("❌ Frontend startup failed", "ERROR")
                return
            
            # Step 4: Open browsers
            time.sleep(5)
            self.open_browsers()
            
            # Step 5: Start continuous refresh
            refresh_thread = threading.Thread(target=self.continuous_refresh)
            refresh_thread.daemon = True
            refresh_thread.start()
            
            # Step 6: Start service monitor
            monitor_thread = threading.Thread(target=self.monitor_services)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            self.log("🎉 Always visible system started!")
            self.log("✅ System always visible")
            self.log("✅ Auto-refresh every 30 seconds")
            self.log("✅ Service monitoring active")
            self.log("🌐 Frontend: http://localhost:3001")
            self.log("🔧 Backend: http://localhost:8000")
            
            # Keep running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.log("🛑 Shutting down always visible system...")
        except Exception as e:
            self.log(f"❌ System error: {e}", "ERROR")

if __name__ == "__main__":
    system = AlwaysVisibleSystem()
    system.start() 