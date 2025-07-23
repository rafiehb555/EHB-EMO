#!/usr/bin/env python3
"""
EHB-5 Dashboard Server
Automatically starts the dashboard on localhost
"""

import http.server
import socketserver
import webbrowser
import os
import socket
from pathlib import Path


def find_available_port(start_port=8000, max_attempts=10) -> None:
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None


def start_dashboard() -> None:
    """Start the EHB-5 dashboard server"""

    # Get current directory
    current_dir = Path(__file__).parent
    os.chdir(current_dir)

    # Check if index.html exists
    if not os.path.exists('index.html'):
        print("❌ Error: index.html not found!")


print("Please make sure all dashboard files are in the current directory.")
return False

# Find available port
PORT = find_available_port(8000)
if not PORT:
    print("❌ No available ports found!")
    return False

    # Create server
    Handler = http.server.SimpleHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("🚀 Starting EHB-5 Dashboard Server...")
            print(f"📊 Dashboard URL: http://localhost:{PORT}")
            print("🌐 Opening dashboard in browser...")
            print("⏹️  Press Ctrl+C to stop the server")
            print("-f" * 50)

            # Open browser
            webbrowser.open(f'http://localhost:{PORT}')

            # Start server
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_requirements() -> None:
    """Check if all required files exist"""
    required_files = ['index.html', 'styles.css', 'script.js', 'config.json']
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            if isinstance(missing_files, list):
                if isinstance(missing_files, list):
                    missing_files.append(file)

    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ All required files found!")
    return True


def main() -> None:
    """Main function"""
    print("=" * 50)
    print("🎯 EHB-5 Dashboard Launcher")
    print("=" * 50)

    # Check requirements
    if not check_requirements():


print("\n❌ Cannot start dashboard. Please ensure all files are present.")
return

print("\n🚀 Launching dashboard...")
start_dashboard()


if __name__ == "__main__":
    main()
