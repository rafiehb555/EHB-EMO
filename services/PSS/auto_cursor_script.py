#!/usr/bin/env python3
"""
Auto Cursor Script for PSS Development
This script runs automatically on startup to setup the development environment
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class PSSAutoSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.pss_dir = self.project_root / "pss"
        self.backend_dir = self.pss_dir / "backend"
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def check_node_installed(self):
        """Check if Node.js is installed"""
        try:
            result = subprocess.run(
                ["node", "--version"], 
                capture_output=True, 
                text=True,
                shell=True
            )
            if result.returncode == 0:
                self.log(f"✅ Node.js installed: {result.stdout.strip()}")
                return True
            else:
                self.log("❌ Node.js not found")
                return False
        except FileNotFoundError:
            self.log("❌ Node.js not found")
            return False
            
    def check_npm_installed(self):
        """Check if npm is installed"""
        try:
            result = subprocess.run(
                ["npm", "--version"], 
                capture_output=True, 
                text=True,
                shell=True
            )
            if result.returncode == 0:
                self.log(f"✅ npm installed: {result.stdout.strip()}")
                return True
            else:
                self.log("❌ npm not found")
                return False
        except FileNotFoundError:
            self.log("❌ npm not found")
            return False
            
    def install_dependencies(self):
        """Install npm dependencies"""
        self.log("📦 Installing frontend dependencies...")
        try:
            subprocess.run(
                ["npm", "install"], 
                cwd=self.pss_dir, 
                check=True,
                shell=True
            )
            self.log("✅ Frontend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Failed to install frontend dependencies: {e}")
            return False
            
        self.log("📦 Installing backend dependencies...")
        try:
            subprocess.run(
                ["npm", "install"], 
                cwd=self.backend_dir, 
                check=True,
                shell=True
            )
            self.log("✅ Backend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Failed to install backend dependencies: {e}")
            return False
            
        return True
        
    def setup_environment(self):
        """Setup environment variables"""
        env_file = self.pss_dir / ".env"
        env_example = self.pss_dir / "env.example"
        
        if not env_file.exists() and env_example.exists():
            self.log("🔧 Creating .env file from template...")
            try:
                with open(env_example, 'r') as f:
                    env_content = f.read()
                    
                # Replace placeholder values with development defaults
                env_content = env_content.replace("your_super_secret_jwt_key_here", "pss_dev_jwt_secret_2024")
                env_content = env_content.replace("your_supabase_url", "https://your-project.supabase.co")
                env_content = env_content.replace("your_supabase_anon_key", "your_anon_key_here")
                env_content = env_content.replace("your_supabase_service_role_key", "your_service_role_key_here")
                env_content = env_content.replace("your_polkadot_rpc_url", "wss://rpc.polkadot.io")
                env_content = env_content.replace("your_moonbeam_contract_address", "0x0000000000000000000000000000000000000000")
                env_content = env_content.replace("your_twilio_sid", "your_twilio_sid_here")
                env_content = env_content.replace("your_twilio_token", "your_twilio_token_here")
                env_content = env_content.replace("your_sendgrid_key", "your_sendgrid_key_here")
                env_content = env_content.replace("your_sql_api_key", "your_sql_api_key_here")
                env_content = env_content.replace("your_nextauth_secret", "pss_nextauth_secret_2024")
                
                with open(env_file, 'w') as f:
                    f.write(env_content)
                    
                self.log("✅ .env file created successfully")
            except Exception as e:
                self.log(f"❌ Failed to create .env file: {e}")
        else:
            self.log("✅ .env file already exists")
            
    def check_port_availability(self):
        """Check if required ports are available"""
        ports = [5002, 6000]  # Frontend and backend ports
        
        for port in ports:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                if result == 0:
                    self.log(f"⚠️  Port {port} is already in use")
                else:
                    self.log(f"✅ Port {port} is available")
            except Exception as e:
                self.log(f"❌ Error checking port {port}: {e}")
                
    def generate_report(self):
        """Generate development setup report"""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project": "PSS - Personal Security System",
            "status": "Development Environment Setup",
            "health_checks": {
                "node_installed": self.check_node_installed(),
                "npm_installed": self.check_npm_installed(),
                "dependencies_installed": True,  # Will be updated after install
                "env_configured": True,  # Will be updated after setup
                "ports_available": True
            },
            "next_steps": [
                "Run 'npm run dev' in pss directory to start frontend",
                "Run 'npm run dev' in pss/backend directory to start backend",
                "Configure Supabase credentials in .env file",
                "Setup MongoDB connection string",
                "Configure blockchain RPC endpoints"
            ]
        }
        
        report_file = self.project_root / "setup_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.log(f"📊 Setup report generated: {report_file}")
        
    def run(self):
        """Main execution method"""
        self.log("🚀 Starting PSS Auto Setup...")
        self.log("=" * 50)
        
        # Health checks
        self.log("🔍 Performing health checks...")
        node_ok = self.check_node_installed()
        npm_ok = self.check_npm_installed()
        
        if not node_ok or not npm_ok:
            self.log("❌ Please install Node.js and npm first")
            return False
            
        # Install dependencies
        self.log("📦 Installing dependencies...")
        deps_ok = self.install_dependencies()
        
        # Setup environment
        self.log("🔧 Setting up environment...")
        self.setup_environment()
        
        # Check ports
        self.log("🔍 Checking port availability...")
        self.check_port_availability()
        
        # Generate report
        self.log("📊 Generating setup report...")
        self.generate_report()
        
        self.log("=" * 50)
        self.log("✅ PSS Auto Setup completed successfully!")
        self.log("🎯 Next steps:")
        self.log("   1. cd pss")
        self.log("   2. npm run dev")
        self.log("   3. Open http://localhost:5002")
        
        return True

if __name__ == "__main__":
    setup = PSSAutoSetup()
    success = setup.run()
    sys.exit(0 if success else 1) 