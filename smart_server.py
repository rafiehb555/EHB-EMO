import os
import sys
import subprocess
from pathlib import Path

#!/usr/bin/env python3
"""
EHB AI Dev Agent - Smart Server Launcher
Automatically finds server.py and starts it from any directory
"""



class SmartServerLauncher:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.server_found = False
        self.server_path = None
        self.server_dir = None

    def find_server_file(self):
        """Find server.py file in current directory or subdirectories"""
        print("SEARCH Searching for server.py file...")

        # Check current directory
        if (self.current_dir / "server.py").exists():
            self.server_path = self.current_dir / "server.py"
            self.server_dir = self.current_dir
            self.server_found = True
            print(f"SUCCESS Found server.py in current directory: {self.server_dir}")
            return True

        # Check ehb-ai-dev-agent subdirectory
        ehb_dir = self.current_dir / "ehb-ai-dev-agent"
        if (ehb_dir / "server.py").exists():
            self.server_path = ehb_dir / "server.py"
            self.server_dir = ehb_dir
            self.server_found = True
            print(f"SUCCESS Found server.py in: {self.server_dir}")
            return True

        # Search recursively in all subdirectories
        for root, dirs, files in os.walk(self.current_dir):
            if "server.py" in files:
                self.server_path = Path(root) / "server.py"
                self.server_dir = Path(root)
                self.server_found = True
                print(f"SUCCESS Found server.py in: {self.server_dir}")
                return True

        print("ERROR Error: server.py file not found!")
        print("💡 Please make sure you're in the correct project directory")
        return False

    def find_free_port(self, start_port=8000, max_attempts=10):
        """Find a free port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("localhost", port))
                    return port
            except OSError:
                continue
        return None

    def start_server(self, port=None):
        """Start the server with smart port detection"""
        if not self.find_server_file():
            return False

        # Ensure server_dir is found
        if self.server_dir is None:
            print("ERROR Error: Server directory not found")
            return False

        # Find free port if not specified
        if port is None:
            print("SEARCH Checking for available port...")
            port = self.find_free_port()
            if not port:
                print("ERROR Error: No free ports available")
                return False

        print(f"SUCCESS Using port: {port}")

        # Change to server directory
        os.chdir(self.server_dir)
        print(f"📁 Changed to directory: {os.getcwd()}")

        # Start the server
        print("ROCKET Starting EHB AI Dev Agent Server...")
        try:
            # Run the server
            subprocess.run(
                [sys.executable, "server.py", "--port", str(port)], check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"ERROR Server failed to start: {e}")
            return False
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            return True

        return True

    def open_browser(self, port):
        """Open browser to dashboard"""
        try:
            url = f"http://localhost:{port}/dashboard.html"
            print(f"WEB Opening browser to: {url}")
            webbrowser.open(url)
        except Exception as e:
            print(f"WARNING Could not open browser automatically: {e}")
            print(f"💡 Please open manually: http://localhost:{port}/dashboard.html")


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="EHB AI Dev Agent - Smart Server Launcher"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port to run server on (auto-detected if not specified)",
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="Don't open browser automatically"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("EHB AI EHB AI Dev Agent - Smart Server Launcher")
    print("=" * 60)

    launcher = SmartServerLauncher()

    # Start server
    success = launcher.start_server(args.port)

    if success and not args.no_browser:
        # Open browser after a short delay
        time.sleep(2)
        launcher.open_browser(args.port or 8000)

    if not success:
        print("\nERROR Failed to start server")
        print("💡 Please check the error messages above")
        sys.exit(1)


if __name__ == "__main__":
    main()
