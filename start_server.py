import os
import sys
import subprocess
from pathlib import Path

#!/usr/bin/env python3
"""
EHB AI Dev Agent - Auto Start Script
Automatically navigates to correct directory and starts server
"""



def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue
    return None


def find_server_file():
    """Find the server.py file in the project"""
    current_dir = Path.cwd()

    # Check if server.py exists in current directory
    if (current_dir / "server.py").exists():
        return current_dir

    # Check in ehb-ai-dev-agent subdirectory
    server_dir = current_dir / "ehb-ai-dev-agent"
    if (server_dir / "server.py").exists():
        return server_dir

    # Search recursively
    for root, dirs, files in os.walk(current_dir):
        if "server.py" in files:
            return Path(root)

    return None


def start_server():
    """Start the EHB AI Dev Agent server"""
    print("SEARCH Searching for server.py file...")

    server_dir = find_server_file()

    if not server_dir:
        print("ERROR Error: server.py file not found!")
        print("💡 Please make sure you're in the correct project directory")
        return False

    print(f"SUCCESS Found server.py in: {server_dir}")

    # Change to server directory
    os.chdir(server_dir)
    print(f"📁 Changed to directory: {os.getcwd()}")

    # Find free port
    print("SEARCH Checking for available port...")
    free_port = find_free_port()
    if not free_port:
        print("ERROR Error: No free ports available")
        return False

    print(f"SUCCESS Using port: {free_port}")

    # Start the server
    print("ROCKET Starting EHB AI Dev Agent Server...")
    try:
        # Run the server with specific port
        subprocess.run(
            [sys.executable, "server.py", "--port", str(free_port)], check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR Server failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("EHB AI EHB AI Dev Agent - Auto Start")
    print("=" * 50)

    success = start_server()

    if not success:
        print("\nERROR Failed to start server")
        print("💡 Please check the error messages above")
        sys.exit(1)
