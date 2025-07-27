#!/usr/bin/env python3
"""
EHB Start Servers Fixed - Start servers on different ports to avoid conflicts
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class EHBStartServersFixed:
    def __init__(self):
        self.servers = [
            {
                "name": "http_server",
                "command": "python http_server.py",
                "port": 8000,
                "health_check": "http://localhost:8000/health"
            },
            {
                "name": "simple_server", 
                "command": "python simple_server.py",
                "port": 8001,
                "health_check": "http://localhost:8001/health"
            },
            {
                "name": "main_server",
                "command": "python main.py",
                "port": 8002,
                "health_check": "http://localhost:8002/health"
            },
            {
                "name": "frontend",
                "command": "npm run dev",
                "port": 3000,
                "health_check": "http://localhost:3000"
            }
        ]
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "servers_started": [],
            "servers_failed": [],
            "health_checks": {},
            "summary": {}
        }
    
    def kill_existing_processes(self):
        """Kill existing processes on ports"""
        print("🛑 Killing existing processes...")
        
        ports_to_kill = [8000, 8001, 8002, 3000, 3001]
        
        for port in ports_to_kill:
            try:
                # Find process using port
                result = subprocess.run(
                    f"netstat -ano | findstr :{port}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.stdout:
                    # Extract PID and kill
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if f":{port}" in line:
                            parts = line.split()
                            if len(parts) > 4:
                                pid = parts[-1]
                                try:
                                    subprocess.run(f"taskkill /f /pid {pid}", shell=True)
                                    print(f"✅ Killed process on port {port}")
                                except:
                                    pass
                                    
            except Exception as e:
                print(f"⚠️ Could not kill process on port {port}: {e}")
        
        time.sleep(2)  # Wait for processes to be killed
    
    def start_server(self, server_config):
        """Start a single server"""
        server_name = server_config["name"]
        command = server_config["command"]
        port = server_config["port"]
        
        print(f"🚀 Starting {server_name} on port {port}...")
        
        try:
            # Start server in background
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(5)
            
            # Check if process is still running
            if process.poll() is None:
                print(f"✅ {server_name}: Started successfully")
                self.results["servers_started"].append(server_name)
                
                # Test health check
                self.test_health_check(server_config)
                
                return True
            else:
                print(f"❌ {server_name}: Failed to start")
                self.results["servers_failed"].append(server_name)
                return False
                
        except Exception as e:
            print(f"❌ {server_name}: Error - {e}")
            self.results["servers_failed"].append(server_name)
            return False
    
    def test_health_check(self, server_config):
        """Test server health check"""
        server_name = server_config["name"]
        health_url = server_config["health_check"]
        
        try:
            import requests
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {server_name}: Health check passed")
                self.results["health_checks"][server_name] = "healthy"
            else:
                print(f"⚠️ {server_name}: Health check failed (status: {response.status_code})")
                self.results["health_checks"][server_name] = "unhealthy"
                
        except Exception as e:
            print(f"❌ {server_name}: Health check error - {e}")
            self.results["health_checks"][server_name] = "error"
    
    def start_all_servers(self):
        """Start all servers"""
        print("🚀 EHB Start Servers Fixed")
        print("=" * 50)
        print("Starting servers on different ports...")
        print("=" * 50)
        
        try:
            # Step 1: Kill existing processes
            self.kill_existing_processes()
            
            # Step 2: Start servers
            for server in self.servers:
                self.start_server(server)
                time.sleep(2)  # Wait between servers
            
            # Step 3: Generate summary
            self.generate_summary()
            
            print("✅ All servers started")
            
        except Exception as e:
            print(f"❌ Server startup failed: {e}")
            self.results["summary"]["status"] = "failed"
            self.results["summary"]["error"] = str(e)
        
        return self.results
    
    def generate_summary(self):
        """Generate server startup summary"""
        print("\n" + "=" * 50)
        print("📊 SERVER STARTUP SUMMARY")
        print("=" * 50)
        
        # Servers started
        if self.results["servers_started"]:
            print(f"✅ Servers Started: {len(self.results['servers_started'])}")
            for server in self.results["servers_started"]:
                health = self.results["health_checks"].get(server, "unknown")
                print(f"  ✅ {server}: {health}")
        
        # Servers failed
        if self.results["servers_failed"]:
            print(f"\n❌ Servers Failed: {len(self.results['servers_failed'])}")
            for server in self.results["servers_failed"]:
                print(f"  ❌ {server}")
        
        # Port assignments
        print(f"\n🌐 Port Assignments:")
        for server in self.servers:
            status = "✅ Running" if server["name"] in self.results["servers_started"] else "❌ Failed"
            print(f"  {server['name']}: http://localhost:{server['port']} - {status}")
        
        # Save results
        report_file = f"reports/server_startup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Report saved: {report_file}")
        print("=" * 50)
        
        self.results["summary"] = {
            "total_servers": len(self.servers),
            "started": len(self.results["servers_started"]),
            "failed": len(self.results["servers_failed"]),
            "success_rate": (len(self.results["servers_started"]) / len(self.servers)) * 100,
            "report_file": report_file
        }

def main():
    """Main function"""
    try:
        starter = EHBStartServersFixed()
        results = starter.start_all_servers()
        
        if results["summary"]["success_rate"] >= 75:
            print("\n🎉 Servers started successfully!")
            return 0
        else:
            print(f"\n⚠️ Some servers failed. Success rate: {results['summary']['success_rate']:.1f}%")
            return 1
            
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 