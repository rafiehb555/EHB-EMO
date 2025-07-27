#!/usr/bin/env python3
"""
🚀 EHB-5 Development Server Starter
Properly starts backend (FastAPI) and frontend (Next.js) servers
"""

import subprocess
import time
import sys
import signal
import threading

class DevServerManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🐍 Starting Backend (FastAPI) on port 8000...")
        try:
            self.backend_process = subprocess.Popen(
                ["python", "backend/app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Monitor backend output
            def monitor_backend():
                for line in iter(self.backend_process.stdout.readline, ''):
                    if line:
                        print(f"[BACKEND] {line.strip()}")
                    if not self.running:
                        break

            backend_thread = threading.Thread(target=monitor_backend)
            backend_thread.daemon = True
            backend_thread.start()

            print("✅ Backend server started successfully!")
            return True

        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start the Next.js frontend server"""
        print("⚛️ Starting Frontend (Next.js) on port 3003...")
        try:
            self.frontend_process = subprocess.Popen(
                ["npm.cmd", "run", "dev"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )

            # Monitor frontend output
            def monitor_frontend():
                for line in iter(self.frontend_process.stdout.readline, ''):
                    if line:
                        print(f"[FRONTEND] {line.strip()}")
                    if not self.running:
                        break

            frontend_thread = threading.Thread(target=monitor_frontend)
            frontend_thread.daemon = True
            frontend_thread.start()

            print("✅ Frontend server started successfully!")
            return True

        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False

    def start_servers(self):
        """Start both servers"""
        print("🚀 Starting EHB-5 Development Servers...")
        print("=" * 50)

        # Start backend first
        if not self.start_backend():
            return False

        # Wait a moment for backend to initialize
        time.sleep(2)

        # Start frontend
        if not self.start_frontend():
            self.stop_servers()
            return False

        print("\n🎉 Development servers started successfully!")
        print("📊 Backend API: http://localhost:8000")
        print("🌐 Frontend UI: http://localhost:3003")
        print("📖 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop servers...")

        return True

    def stop_servers(self):
        """Stop both servers"""
        print("\n🛑 Stopping development servers...")
        self.running = False

        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            print("✅ Backend server stopped")

        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            print("✅ Frontend server stopped")

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        self.stop_servers()
        sys.exit(0)

def main():
    manager = DevServerManager()

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, manager.signal_handler)

    try:
        if manager.start_servers():
            # Keep the script running
            while manager.running:
                time.sleep(1)
        else:
            print("❌ Failed to start development servers")
            sys.exit(1)

    except KeyboardInterrupt:
        manager.stop_servers()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        manager.stop_servers()
        sys.exit(1)

if __name__ == "__main__":
    main()
