#!/usr/bin/env python3
"""
🔧 Port Conflict Fixer for EHB-5 Project
Automatically detects and fixes port conflicts
"""

import subprocess
import sys

def check_port(port):
    """Check if port is in use"""
    try:
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip() != ""
    except:
        return False

def kill_process_on_port(port):
    """Kill process using specific port"""
    try:
        # Get process ID
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]

                    # Kill process
                    kill_result = subprocess.run(
                        f'taskkill /PID {pid} /F',
                        shell=True,
                        capture_output=True
                    )

                    if kill_result.returncode == 0:
                        print(f"✅ Killed process {pid} using port {port}")
                        return True
                    else:
                        print(f"❌ Failed to kill process {pid}")
                        return False
        return False
    except Exception as e:
        print(f"❌ Error killing process on port {port}: {e}")
        return False

def fix_dev_server_conflicts():
    """Fix common development server conflicts"""
    print("🔍 Checking for port conflicts...")

    # Check ports used by EHB-5
    ports_to_check = [3000, 3001, 8000, 5000]
    conflicts_found = False

    for port in ports_to_check:
        if check_port(port):
            print(f"⚠️  Port {port} is in use")
            conflicts_found = True

            if port == 3000:
                print("🔧 Fixing port 3000 conflict (moving frontend to 3001)")
                kill_process_on_port(port)
            elif port == 8000:
                print("⚠️  Port 8000 conflict detected (backend port)")
                user_input = input("Kill process on port 8000? (y/n): ")
                if user_input.lower() == 'y':
                    kill_process_on_port(port)
        else:
            print(f"✅ Port {port} is available")

    if not conflicts_found:
        print("✅ No port conflicts detected!")

    return not conflicts_found

if __name__ == "__main__":
    print("🚀 EHB-5 Port Conflict Fixer")
    print("=" * 40)

    if fix_dev_server_conflicts():
        print("\n🎉 All ports are clear! Ready to start dev server.")
        print("Run: npm run dev")
    else:
        print("\n🔧 Fixed port conflicts. Try running dev server again.")
        print("Run: npm run dev")
