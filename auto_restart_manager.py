
import os
import sys
import time
import subprocess
import signal
from pathlib import Path

class AutoRestartManager:
    """Auto-restart manager for EHB agents"""
    
    def __init__(self):
        self.processes = {}
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down auto-restart manager...")
        self.running = False
        self.stop_all_processes()
        sys.exit(0)
    
    def start_process(self, name: str, command: str, cwd: str = None):
        """Start a process with auto-restart"""
        try:
            print(f"🚀 Starting {name}...")
            
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            
            self.processes[name] = {
                'process': process,
                'command': command,
                'cwd': cwd,
                'start_time': time.time(),
                'restart_count': 0
            }
            
            print(f"✅ {name} started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return False
    
    def stop_process(self, name: str):
        """Stop a process"""
        if name in self.processes:
            process_info = self.processes[name]
            process = process_info['process']
            
            try:
                process.terminate()
                process.wait(timeout=10)
                print(f"✅ {name} stopped successfully")
            except:
                process.kill()
                process.wait()
            
            del self.processes[name]
    
    def stop_all_processes(self):
        """Stop all processes"""
        for name in list(self.processes.keys()):
            self.stop_process(name)
    
    def monitor_processes(self):
        """Monitor and restart processes if needed"""
        while self.running:
            try:
                for name, process_info in list(self.processes.items()):
                    process = process_info['process']
                    
                    if process.poll() is not None:
                        print(f"⚠️ {name} has stopped, restarting...")
                        
                        if process_info['restart_count'] < 5:
                            process_info['restart_count'] += 1
                            self.start_process(name, process_info['command'], process_info['cwd'])
                        else:
                            print(f"❌ {name} exceeded max restarts")
                            del self.processes[name]
                
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error in process monitoring: {e}")
                time.sleep(5)
    
    def run(self):
        """Run the auto-restart manager"""
        print("🔄 Auto-restart manager starting...")
        
        # Start essential processes
        self.start_process("frontend", "npm run dev", "frontend")
        self.start_process("backend", "python api_server.py")
        self.start_process("agent", "python robust_agent_manager.py")
        
        # Start monitoring
        self.monitor_processes()

if __name__ == "__main__":
    manager = AutoRestartManager()
    manager.run()
