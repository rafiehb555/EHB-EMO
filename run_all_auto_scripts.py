#!/usr/bin/env python3
"""
EHB Auto Script Runner - Runs all auto scripts in the project
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class EHBAutoScriptRunner:
    def __init__(self):
        self.scripts_to_run = [
            "auto_cursor_script.py",
            "startup_auto.py", 
            "auto_setup_simple.py",
            "auto_dev_setup_simple.py",
            "auto_dev_setup.py",
            "auto_dev_setup_fixed.py",
            "start_server.py",
            "cursor_auto_connect.py",
            "optimize_performance.py",
            "memory_optimizer.py",
            "fast_agent_optimizer.py",
            "auto_restart_agent.py",
            "performance_monitor.py"
        ]
        
        self.agent_scripts = [
            "agents/cursor_auto_integration.py",
            "agents/cursor_config_optimizer.py",
            "agents/watchdog/agentMonitor.js"
        ]
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_scripts": 0,
            "successful_scripts": 0,
            "failed_scripts": 0,
            "script_results": {},
            "summary": {}
        }
    
    def run_all_scripts(self):
        """Run all auto scripts in the project"""
        print("🚀 EHB Auto Script Runner")
        print("=" * 50)
        print("Running all auto scripts in the project...")
        print("=" * 50)
        
        # Run main scripts
        for script in self.scripts_to_run:
            self.run_script(script)
        
        # Run agent scripts
        for script in self.agent_scripts:
            self.run_script(script)
        
        # Generate summary
        self.generate_summary()
        
        return self.results
    
    def run_script(self, script_name):
        """Run a single script"""
        script_path = Path(script_name)
        
        if not script_path.exists():
            print(f"⚠️  Script not found: {script_name}")
            self.results["script_results"][script_name] = {
                "status": "not_found",
                "error": "Script file not found"
            }
            return
        
        print(f"🔄 Running: {script_name}")
        
        try:
            # Determine script type and run accordingly
            if script_name.endswith('.js'):
                # Node.js script
                result = subprocess.run(
                    ['node', script_name],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            else:
                # Python script
                result = subprocess.run(
                    [sys.executable, script_name],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            
            if result.returncode == 0:
                print(f"✅ {script_name}: Success")
                self.results["script_results"][script_name] = {
                    "status": "success",
                    "returncode": result.returncode,
                    "stdout": result.stdout[:500],  # First 500 chars
                    "stderr": result.stderr[:500] if result.stderr else ""
                }
                self.results["successful_scripts"] += 1
            else:
                print(f"❌ {script_name}: Failed (return code: {result.returncode})")
                self.results["script_results"][script_name] = {
                    "status": "failed",
                    "returncode": result.returncode,
                    "stdout": result.stdout[:500],
                    "stderr": result.stderr[:500] if result.stderr else ""
                }
                self.results["failed_scripts"] += 1
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {script_name}: Timeout")
            self.results["script_results"][script_name] = {
                "status": "timeout",
                "error": "Script execution timed out"
            }
            self.results["failed_scripts"] += 1
            
        except Exception as e:
            print(f"❌ {script_name}: Error - {e}")
            self.results["script_results"][script_name] = {
                "status": "error",
                "error": str(e)
            }
            self.results["failed_scripts"] += 1
        
        self.results["total_scripts"] += 1
    
    def generate_summary(self):
        """Generate summary of all script runs"""
        print("\n" + "=" * 50)
        print("📊 AUTO SCRIPT RUN SUMMARY")
        print("=" * 50)
        
        total = self.results["total_scripts"]
        successful = self.results["successful_scripts"]
        failed = self.results["failed_scripts"]
        
        print(f"Total Scripts: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(successful/total*100):.1f}%" if total > 0 else "N/A")
        
        # Show failed scripts
        failed_scripts = [name for name, result in self.results["script_results"].items() 
                         if result["status"] in ["failed", "error", "timeout"]]
        
        if failed_scripts:
            print(f"\n❌ Failed Scripts:")
            for script in failed_scripts:
                result = self.results["script_results"][script]
                print(f"  - {script}: {result.get('error', 'Unknown error')}")
        
        # Show successful scripts
        successful_scripts = [name for name, result in self.results["script_results"].items() 
                            if result["status"] == "success"]
        
        if successful_scripts:
            print(f"\n✅ Successful Scripts:")
            for script in successful_scripts:
                print(f"  - {script}")
        
        # Save detailed results
        report_file = f"reports/auto_script_run_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("=" * 50)
        
        self.results["summary"] = {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful/total*100) if total > 0 else 0,
            "report_file": report_file
        }
    
    def run_optimization_scripts(self):
        """Run optimization scripts specifically"""
        print("\n⚡ Running Optimization Scripts...")
        
        optimization_scripts = [
            "optimize_performance.py",
            "memory_optimizer.py", 
            "fast_agent_optimizer.py"
        ]
        
        for script in optimization_scripts:
            self.run_script(script)
    
    def run_monitoring_scripts(self):
        """Run monitoring scripts specifically"""
        print("\n📊 Running Monitoring Scripts...")
        
        monitoring_scripts = [
            "performance_monitor.py",
            "auto_restart_agent.py"
        ]
        
        for script in monitoring_scripts:
            self.run_script(script)

def main():
    """Main function"""
    try:
        runner = EHBAutoScriptRunner()
        results = runner.run_all_scripts()
        
        if results["summary"]["success_rate"] >= 80:
            print("\n🎉 Auto script run completed successfully!")
            print("Most scripts ran successfully.")
            return 0
        else:
            print(f"\n⚠️  Auto script run completed with issues.")
            print(f"Success rate: {results['summary']['success_rate']:.1f}%")
            return 1
            
    except Exception as e:
        print(f"❌ Auto script runner failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 