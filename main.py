#!/usr/bin/env python3
"""
EHB-5 Main Application
Unified entry point for the EHB-5 project
"""

import os
import sys
import threading
import time
from pathlib import Path

from api_server import app as api_app
from auth_manager import AuthManager
from data_processor import DataProcessor
from database import DatabaseManager

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))


class EHB5Application:
    """Main EHB-5 application class"""

    def __init__(self) -> None:
        self.db = DatabaseManager()
        self.data_processor = DataProcessor()
        self.auth_manager = AuthManager()
        self.api_app = api_app

    def start_api_server(self, port: int = 5000) -> threading.Thread:
        """Start the API server in a separate thread"""
        def run_server() -> None:
            self.api_app.run(host='0.0.0.0', port=port, debug=False)

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        return server_thread

    def start_dashboard_server(self, port: int = 8000) -> bool:
        """Start the dashboard server"""
        import http.server
        import socketserver
        import webbrowser

        # Change to current directory
        os.chdir(current_dir)

        # Check if index.html exists
        if not os.path.exists('index.html'):
            print("❌ Error: index.html not found!")
            return False

        # Create server
        Handler = http.server.SimpleHTTPRequestHandler

        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                print(f"🚀 Starting EHB-5 Dashboard Server on port {port}...")
                print(f"📊 Dashboard URL: http://localhost:{port}")

                # Open browser
                webbrowser.open(f'http://localhost:{port}')

                # Start server
                httpd.serve_forever()

        except KeyboardInterrupt:
            print("\n🛑 Dashboard server stopped by user")
            return True
        except Exception as e:
            print(f"❌ Error starting dashboard server: {e}")
            return False

    def initialize_system(self) -> None:
        """Initialize the EHB-5 system"""
        print("=" * 50)
        print("🎯 EHB-5 System Initialization")
        print("=" * 50)

        # Initialize database
        print("📊 Initializing database...")
        self.db.init_database()

        # Create default admin user
        print("👤 Creating default admin user...")
        admin_password = "admin123"
        admin_password_hash = self.auth_manager.hash_password(admin_password)

        if self.db.create_user(
            "admin",
            "admin@ehb5.com",
            admin_password_hash,
                "admin"):
            print("✅ Admin user created successfully")
            print("   Username: admin")
            print(f"   Password: {admin_password}")
        else:
            print("ℹ️  Admin user already exists")

        # Log system startup
        self.db.log_system_event('INFO', 'EHB-5 System initialized')

        print("✅ System initialization completed!")
        print("=" * 50)

    def run(self) -> None:
        """Run the complete EHB-5 application"""
        try:
            # Initialize system
            self.initialize_system()

            # Start API server
            print("🚀 Starting API server...")
            self.start_api_server()
            time.sleep(2)  # Give API server time to start

            # Start dashboard server
            print("🌐 Starting dashboard server...")
            self.start_dashboard_server()

        except KeyboardInterrupt:
            print("\n🛑 EHB-5 application stopped by user")
        except Exception as e:
            print(f"❌ Application error: {e}")


def main() -> None:
    """Main function"""
    app = EHB5Application()
    app.run()


if __name__ == "__main__":
    main()
