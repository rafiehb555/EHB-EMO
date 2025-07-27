#!/usr/bin/env python3
"""
EHB AI Dev Agent - Complete Deployment Script
Sets up database, starts API server, and frontend with all missing components
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

# Setup logging without emojis to avoid encoding issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('complete_deployment.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class CompleteDeployment:
    def __init__(self):
        self.running = True
        self.frontend_process = None
        self.backend_process = None
        self.ports = {
            'frontend': 3000,
            'backend': 8000
        }

    def check_dependencies(self):
        """Check and install required dependencies"""
        logging.info("Checking dependencies...")

        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Node.js found: {result.stdout.strip()}")
            else:
                logging.error("Node.js not found!")
                return False
        except FileNotFoundError:
            logging.error("Node.js not found!")
            return False

        # Check npm with full path
        try:
            # Try different npm paths
            npm_paths = ['npm', 'npm.cmd', r'C:\Program Files\nodejs\npm.cmd']
            npm_found = False

            for npm_path in npm_paths:
                try:
                    result = subprocess.run([npm_path, '--version'], capture_output=True, text=True)
                    if result.returncode == 0:
                        logging.info(f"npm found: {result.stdout.strip()}")
                        npm_found = True
                        break
                except FileNotFoundError:
                    continue

            if not npm_found:
                logging.error("npm not found!")
                return False
        except Exception as e:
            logging.error(f"Error checking npm: {e}")
            return False

        # Check Python
        try:
            result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Python found: {result.stdout.strip()}")
            else:
                logging.error("Python not found!")
                return False
        except FileNotFoundError:
            logging.error("Python not found!")
            return False

        return True

    def install_python_dependencies(self):
        """Install Python dependencies"""
        logging.info("Installing Python dependencies...")

        dependencies = [
            'fastapi',
            'uvicorn',
            'websockets',
            'bcrypt',
            'PyJWT',
            'requests'
        ]

        for dep in dependencies:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep],
                             capture_output=True, check=True)
                logging.info(f"Installed {dep}")
            except subprocess.CalledProcessError:
                logging.warning(f"Failed to install {dep}")

    def setup_database(self):
        """Setup complete database"""
        logging.info("Setting up database...")

        try:
            # Run database setup script
            result = subprocess.run([sys.executable, 'complete_database_setup.py'],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                logging.info("Database setup completed")
                return True
            else:
                logging.error(f"Database setup failed: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"Database setup error: {e}")
            return False

    def install_frontend_dependencies(self):
        """Install frontend dependencies"""
        logging.info("Installing frontend dependencies...")
        try:
            # Try different npm commands
            npm_commands = [
                ['npm', 'install'],
                ['npm.cmd', 'install'],
                [r'C:\Program Files\nodejs\npm.cmd', 'install']
            ]

            for cmd in npm_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        logging.info("Frontend dependencies installed successfully")
                        return True
                    else:
                        logging.warning(f"Failed with command {cmd}: {result.stderr}")
                except FileNotFoundError:
                    continue

            logging.error("Failed to install frontend dependencies")
            return False
        except Exception as e:
            logging.error(f"Error installing frontend dependencies: {e}")
            return False

    def start_backend_server(self):
        """Start backend API server"""
        logging.info("Starting backend API server...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "complete_api_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(5)  # Wait for server to start

            # Test backend
            try:
                response = requests.get("http://localhost:8000/health", timeout=10)
                if response.status_code == 200:
                    logging.info("Backend API server started successfully")
                    return True
                else:
                    logging.error(f"Backend health check failed: {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                logging.error(f"Backend health check failed: {e}")
                return False

        except Exception as e:
            logging.error(f"Failed to start backend: {e}")
            return False

    def start_frontend_server(self):
        """Start frontend development server"""
        logging.info("Starting frontend server...")
        try:
            # Try different npm commands
            npm_commands = [
                ['npm', 'run', 'dev'],
                ['npm.cmd', 'run', 'dev'],
                [r'C:\Program Files\nodejs\npm.cmd', 'run', 'dev']
            ]

            for cmd in npm_commands:
                try:
                    self.frontend_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    break
                except FileNotFoundError:
                    continue

            time.sleep(15)  # Wait for Next.js to start

            # Test frontend
            try:
                response = requests.get("http://localhost:3000", timeout=15)
                if response.status_code == 200:
                    logging.info("Frontend server started successfully")
                    return True
                else:
                    logging.error(f"Frontend health check failed: {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                logging.error(f"Frontend health check failed: {e}")
                return False

        except Exception as e:
            logging.error(f"Failed to start frontend: {e}")
            return False

    def open_browser(self):
        """Open application in browser"""
        logging.info("Opening application in browser...")
        try:
            webbrowser.open("http://localhost:3000")
            logging.info("Browser opened successfully")
        except Exception as e:
            logging.error(f"Failed to open browser: {e}")

    def health_monitor(self):
        """Monitor health of services"""
        while self.running:
            try:
                # Check backend
                try:
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    if response.status_code != 200:
                        logging.warning("Backend health check failed")
                except:
                    logging.warning("Backend not responding")

                # Check frontend
                try:
                    response = requests.get("http://localhost:3000", timeout=5)
                    if response.status_code != 200:
                        logging.warning("Frontend health check failed")
                except:
                    logging.warning("Frontend not responding")

            except Exception as e:
                logging.error(f"Health monitor error: {e}")

            time.sleep(30)  # Check every 30 seconds

    def create_deployment_report(self):
        """Create deployment report"""
        report = {
            "deployment_status": "completed",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "services": {
                "backend": {
                    "status": "running",
                    "url": "http://localhost:8000",
                    "health": "http://localhost:8000/health",
                    "docs": "http://localhost:8000/docs"
                },
                "frontend": {
                    "status": "running",
                    "url": "http://localhost:3000",
                    "pages": [
                        "http://localhost:3000/",
                        "http://localhost:3000/ai-dashboard",
                        "http://localhost:3000/ai-agents",
                        "http://localhost:3000/ai-projects"
                    ]
                },
                "database": {
                    "status": "connected",
                    "file": "ehb_ai_dev_agent.db",
                    "tables": [
                        "users",
                        "ai_agents",
                        "projects",
                        "agent_memory",
                        "agent_tasks",
                        "agent_communications",
                        "analytics",
                        "errors",
                        "notifications",
                        "settings"
                    ]
                }
            },
            "authentication": {
                "status": "ready",
                "default_users": {
                    "admin": "admin@ehb.com / admin123",
                    "developer": "dev@ehb.com / dev123",
                    "user": "user@ehb.com / user123"
                }
            },
            "features": {
                "real_time": "WebSocket enabled",
                "api_endpoints": "Complete REST API",
                "authentication": "JWT-based auth",
                "database": "SQLite with sample data",
                "frontend": "React/Next.js with real API"
            }
        }

        with open("DEPLOYMENT_REPORT.json", "w") as f:
            json.dump(report, f, indent=2)

        logging.info("Deployment report created: DEPLOYMENT_REPORT.json")

    def run(self):
        """Main deployment process"""
        logging.info("Starting EHB AI Dev Agent Complete Deployment...")

        # Check dependencies
        if not self.check_dependencies():
            logging.error("Dependencies check failed")
            return False

        # Install Python dependencies
        self.install_python_dependencies()

        # Setup database
        if not self.setup_database():
            logging.error("Database setup failed")
            return False

        # Install frontend dependencies
        if not self.install_frontend_dependencies():
            logging.error("Frontend dependency installation failed")
            return False

        # Start backend
        if not self.start_backend_server():
            logging.error("Backend startup failed")
            return False

        # Start frontend
        if not self.start_frontend_server():
            logging.error("Frontend startup failed")
            return False

        # Start health monitor
        health_thread = threading.Thread(target=self.health_monitor, daemon=True)
        health_thread.start()

        # Create deployment report
        self.create_deployment_report()

        # Open browser
        time.sleep(5)  # Wait a bit more
        self.open_browser()

        logging.info("EHB AI Dev Agent is now LIVE!")
        logging.info("Frontend: http://localhost:3000")
        logging.info("Backend: http://localhost:8000")
        logging.info("API Docs: http://localhost:8000/docs")
        logging.info("Health: http://localhost:8000/health")
        logging.info("Database: ehb_ai_dev_agent.db")
        logging.info("Default users:")
        logging.info("   - Admin: admin@ehb.com / admin123")
        logging.info("   - Developer: dev@ehb.com / dev123")
        logging.info("   - User: user@ehb.com / user123")
        logging.info("Press Ctrl+C to stop")

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Shutting down...")
            self.running = False
            if self.frontend_process:
                self.frontend_process.terminate()
            if self.backend_process:
                self.backend_process.terminate()

        return True

def main():
    """Main function"""
    deployment = CompleteDeployment()
    success = deployment.run()

    if success:
        print("\nEHB AI Dev Agent successfully deployed!")
        print("Open http://localhost:3000 in your browser")
        print("API Documentation: http://localhost:8000/docs")
        print("Health Check: http://localhost:8000/health")
        print("Deployment Report: DEPLOYMENT_REPORT.json")
    else:
        print("\nDeployment failed. Check logs for details.")

if __name__ == "__main__":
    main()
