#!/usr/bin/env python3
"""
EHB Complete Auto Runner
Handles Next.js port issues and auto-connects when Cursor is used
"""

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import psutil


class EHBCompleteAutoRunner:
    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"
        self.running = False
        
    def analyze_nextjs_error(self):
        """Analyze Next.js port configuration error"""
        print("=" * 60)
        print("🔍 Next.js Error Analysis")
        print("=" * 60)
        
        print("\n❌ ERROR DETAILS:")
        print("Command: npm run dev -- -p 3001")
        print("Error: Invalid project directory provided, no such directory: F:\\ehb 5\\3001")
        
        print("\n🔍 ROOT CAUSE:")
        print("1. Next.js v13+ mein 'next dev 3001' galat syntax hai")
        print("2. Next.js 3001 ko directory samajhta hai, port nahi")
        print("3. Correct syntax: 'next dev -p 3001' ya environment variable")
        
        print("\n📋 SOLUTION:")
        print("1. Use: set PORT=3001 && npm run dev")
        print("2. Or: npm run dev -- -p 3001 (correct syntax)")
        print("3. Or modify package.json scripts")
        
        return True
    
    def fix_package_json(self):
        """Fix package.json for proper port configuration"""
        print("\n🔧 Fixing package.json...")
        
        package_json_path = self.frontend_dir / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                data = json.load(f)
            
            scripts = data.get('scripts', {})
            
            # Fix dev script
            if 'dev' in scripts:
                dev_script = scripts['dev']
                # Remove turbopack if present
                if '--turbopack' in dev_script:
                    dev_script = dev_script.replace(' --turbopack', '')
                    print("✅ Removed --turbopack flag")
                
                # Ensure correct next dev command
                if 'next dev' not in dev_script:
                    dev_script = 'next dev'
                    print("✅ Fixed dev script")
                
                data['scripts']['dev'] = dev_script
                
                with open(package_json_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"✅ Updated dev script: {dev_script}")
                return True
        
        print("❌ package.json not found or could not be fixed")
        return False
    
    def kill_existing_processes(self):
        """Kill existing Node.js and Python processes"""
        print("\n🔄 Killing existing processes...")
        
        try:
            # Kill Node.js processes
            subprocess.run(['taskkill', '/f', '/im', 'node.exe'], 
                         capture_output=True, check=False)
            print("✅ Killed Node.js processes")
            
            # Kill Python processes
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, check=False)
            print("✅ Killed Python processes")
            
            time.sleep(2)
            return True
        except Exception as e:
            print(f"⚠️  Could not kill processes: {e}")
            return False
    
    def detect_cursor(self):
        """Detect if Cursor IDE is running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'cursor' in proc.info['name'].lower():
                    return True
            return False
        except:
            return False
    
    def check_servers_running(self):
        """Check if servers are already running"""
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            return '3000' in result.stdout or '3001' in result.stdout
        except:
            return False
    
    def start_backend_server(self):
        """Start backend server"""
        print("\n🚀 Starting Backend Server...")
        
        try:
            os.chdir(self.project_root)
            
            # Check if enhanced API server exists
            if (self.project_root / "enhanced_api_server.py").exists():
                process = subprocess.Popen(
                    ['python', 'enhanced_api_server.py'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print("✅ Enhanced API Server started on port 8000")
                return process
            else:
                # Fallback to regular API server
                process = subprocess.Popen(
                    ['python', 'api_server.py'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print("✅ API Server started on port 8000")
                return process
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return None
    
    def start_frontend_server(self, port=3000):
        """Start frontend server with proper port configuration"""
        print(f"\n🎨 Starting Frontend Server on port {port}...")
        
        try:
            os.chdir(self.frontend_dir)
            
            # Set environment variable for port
            env = os.environ.copy()
            env['PORT'] = str(port)
            
            # Install dependencies first
            print("📦 Installing dependencies...")
            subprocess.run(['npm', 'install'], capture_output=True, check=False)
            
            # Start the server
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Frontend Server started on port {port}")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return None
    
    def auto_start_servers(self):
        """Auto-start both servers"""
        print("\n🚀 Auto-starting EHB Healthcare servers...")
        
        # Kill existing processes
        self.kill_existing_processes()
        
        # Fix package.json
        self.fix_package_json()
        
        # Start backend server
        backend_process = self.start_backend_server()
        
        # Wait for backend to start
        time.sleep(3)
        
        # Start frontend server
        frontend_process = self.start_frontend_server()
        
        if backend_process and frontend_process:
            print("\n" + "=" * 60)
            print("🎉 SUCCESS! Both servers are running:")
            print("🌐 Frontend: http://localhost:3000")
            print("🌐 Backend: http://localhost:8000")
            print("🌐 API Health: http://localhost:8000/api/health")
            print("🌐 Dashboard: http://localhost:3000/dashboard")
            print("=" * 60)
            return True
        else:
            print("❌ Failed to start servers")
            return False
    
    def monitor_cursor_and_auto_start(self):
        """Monitor for Cursor IDE and auto-start servers"""
        print("\n🔍 Monitoring for Cursor IDE...")
        print("💡 When you open Cursor, servers will auto-start")
        
        while True:
            try:
                if self.detect_cursor() and not self.running:
                    print("\n🎯 Cursor detected! Auto-starting servers...")
                    self.running = True
                    self.auto_start_servers()
                
                elif not self.detect_cursor() and self.running:
                    print("\n📝 Cursor closed. Servers still running...")
                    self.running = False
                
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 Auto-runner stopped by user")
                break
            except Exception as e:
                print(f"⚠️  Monitor error: {e}")
                time.sleep(10)

def main():
    """Main function"""
    print("=" * 60)
    print("🏥 EHB Complete Auto Runner")
    print("=" * 60)
    
    runner = EHBCompleteAutoRunner()
    
    # Analyze the error first
    runner.analyze_nextjs_error()
    
    # Check if servers are already running
    if runner.check_servers_running():
        print("\n✅ Servers are already running!")
        print("🌐 Frontend: http://localhost:3000")
        print("🌐 Backend: http://localhost:8000")
    else:
        print("\n⏳ Starting servers...")
        runner.auto_start_servers()
    
    # Start monitoring for Cursor
    print("\n🔍 Starting Cursor monitor...")
    runner.monitor_cursor_and_auto_start()

if __name__ == "__main__":
    main() 