#!/usr/bin/env python3
"""
Auto Next.js Port Configuration Fixer
Automatically fixes Next.js port configuration issues
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path


class AutoNextJSFixer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"
        
    def fix_package_json(self):
        """Fix package.json dev script"""
        print("🔧 Fixing package.json...")
        
        package_json_path = self.frontend_dir / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                data = json.load(f)
            
            scripts = data.get('scripts', {})
            dev_script = scripts.get('dev', '')
            
            # Remove turbopack flag if present
            if '--turbopack' in dev_script:
                dev_script = dev_script.replace(' --turbopack', '')
                print("✅ Removed --turbopack flag")
            
            # Ensure correct dev script
            if 'next dev' not in dev_script:
                dev_script = 'next dev'
                print("✅ Fixed dev script")
            
            data['scripts']['dev'] = dev_script
            
            with open(package_json_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Updated dev script: {dev_script}")
            return True
        else:
            print("❌ package.json not found")
            return False
    
    def create_next_config(self):
        """Create proper Next.js configuration"""
        print("⚙️  Creating Next.js configuration...")
        
        next_config_path = self.frontend_dir / "next.config.ts"
        
        config_content = '''import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    appDir: true,
  },
  // Add custom port configuration
  server: {
    port: process.env.PORT ? parseInt(process.env.PORT) : 3000,
  },
};

export default nextConfig;
'''
        
        with open(next_config_path, 'w') as f:
            f.write(config_content)
        
        print("✅ Created next.config.ts with port configuration")
        return True
    
    def kill_existing_processes(self):
        """Kill existing Node.js processes"""
        print("🔄 Killing existing Node.js processes...")
        
        try:
            # Kill Node.js processes
            subprocess.run(['taskkill', '/f', '/im', 'node.exe'], 
                         capture_output=True, check=False)
            print("✅ Killed existing Node.js processes")
            
            # Kill Python processes (if any)
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, check=False)
            print("✅ Killed existing Python processes")
            
            time.sleep(2)  # Wait for processes to terminate
            return True
        except Exception as e:
            print(f"⚠️  Could not kill processes: {e}")
            return False
    
    def check_port_availability(self, port):
        """Check if port is available"""
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            return str(port) not in result.stdout
        except:
            return True
    
    def find_available_port(self):
        """Find an available port"""
        for port in [3000, 3001, 3002, 3003, 3004, 3005]:
            if self.check_port_availability(port):
                return port
        return 3000
    
    def start_frontend_server(self, port=None):
        """Start frontend server with proper configuration"""
        if not port:
            port = self.find_available_port()
        
        print(f"🚀 Starting frontend server on port {port}...")
        
        # Set environment variable
        env = os.environ.copy()
        env['PORT'] = str(port)
        
        try:
            # Change to frontend directory
            os.chdir(self.frontend_dir)
            
            # Start the server
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Frontend server started on port {port}")
            print(f"🌐 Access URL: http://localhost:{port}")
            
            return process, port
        except Exception as e:
            print(f"❌ Failed to start frontend server: {e}")
            return None, None
    
    def start_backend_server(self):
        """Start backend server"""
        print("🚀 Starting backend server...")
        
        try:
            # Change back to project root
            os.chdir(self.project_root)
            
            # Start enhanced API server
            process = subprocess.Popen(
                ['python', 'enhanced_api_server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ Backend server started on port 8000")
            print("🌐 API URL: http://localhost:8000")
            
            return process
        except Exception as e:
            print(f"❌ Failed to start backend server: {e}")
            return None
    
    def auto_fix_and_start(self):
        """Main auto-fix and start function"""
        print("=" * 60)
        print("🔧 Auto Next.js Fixer & Starter")
        print("=" * 60)
        
        # Step 1: Kill existing processes
        self.kill_existing_processes()
        
        # Step 2: Fix package.json
        if not self.fix_package_json():
            print("❌ Failed to fix package.json")
            return False
        
        # Step 3: Create/update Next.js config
        self.create_next_config()
        
        # Step 4: Install dependencies
        print("📦 Installing dependencies...")
        os.chdir(self.frontend_dir)
        subprocess.run(['npm', 'install'], check=False)
        
        # Step 5: Start backend server
        backend_process = self.start_backend_server()
        
        # Step 6: Start frontend server
        frontend_process, port = self.start_frontend_server()
        
        if frontend_process and backend_process:
            print("\n" + "=" * 60)
            print("🎉 SUCCESS! Both servers are running:")
            print(f"🌐 Frontend: http://localhost:{port}")
            print("🌐 Backend: http://localhost:8000")
            print("🌐 API Health: http://localhost:8000/api/health")
            print("🌐 Dashboard: http://localhost:{port}/dashboard")
            print("=" * 60)
            
            return True
        else:
            print("❌ Failed to start servers")
            return False

def main():
    """Main function"""
    fixer = AutoNextJSFixer()
    success = fixer.auto_fix_and_start()
    
    if success:
        print("\n✅ Auto-fix completed successfully!")
        print("💡 Tip: Use Ctrl+C to stop servers")
    else:
        print("\n❌ Auto-fix failed. Check error messages above.")

if __name__ == "__main__":
    main() 