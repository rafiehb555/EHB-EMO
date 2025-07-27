#!/usr/bin/env python3
"""
💀 Kill All Development Servers
Comprehensive cleanup for EHB-5 project
"""

import subprocess
import time

def kill_process_on_port(port):
    """Kill all processes on a specific port"""
    try:
        # Find processes on port
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )

        killed_any = False
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) > 0:
                        pid = parts[-1]
                        print(f"🔫 Killing process {pid} on port {port}")

                        kill_result = subprocess.run(
                            f'taskkill /PID {pid} /F',
                            shell=True,
                            capture_output=True
                        )

                        if kill_result.returncode == 0:
                            print(f"✅ Killed process {pid}")
                            killed_any = True
                        else:
                            print(f"❌ Failed to kill process {pid}")

        return killed_any
    except Exception as e:
        print(f"❌ Error killing processes on port {port}: {e}")
        return False

def kill_node_python_processes():
    """Kill all node and python processes that might be development servers"""
    try:
        # Kill node processes
        subprocess.run('taskkill /F /IM node.exe', shell=True, capture_output=True)
        print("🔫 Killed all node.exe processes")

        # Kill python processes (be careful here)
        result = subprocess.run('tasklist | findstr python', shell=True, capture_output=True, text=True)
        if result.stdout:
            print("⚠️  Found python processes - being selective")
            # Don't kill all python processes as it might kill important ones

        time.sleep(2)  # Wait for processes to die
        return True
    except:
        return False

def main():
    print("💀 EHB-5 Development Server Killer")
    print("=" * 40)

    # Kill specific ports
    ports = [3000, 3001, 3002, 8000, 5000]
    for port in ports:
        print(f"\n🔍 Checking port {port}...")
        if kill_process_on_port(port):
            print(f"✅ Port {port} cleared")
        else:
            print(f"✅ Port {port} was already free")

    print(f"\n🔫 Killing development server processes...")
    kill_node_python_processes()

    # Final verification
    print(f"\n🔍 Final port check...")
    for port in ports:
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f"⚠️  Port {port} still in use")
        else:
            print(f"✅ Port {port} is free")

    print(f"\n🎉 Cleanup complete! Now run: npm run dev")

if __name__ == "__main__":
    main()
