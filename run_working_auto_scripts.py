#!/usr/bin/env python3
"""
EHB Working Auto Script Runner - Runs only working auto scripts
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class EHBWorkingAutoScriptRunner:
    def __init__(self):
        # Only working scripts that we know work
        self.working_scripts = [
            "auto_cursor_script.py",
            "startup_auto.py",
            "optimize_performance.py",
            "memory_optimizer.py",
            "fast_agent_optimizer.py"
        ]
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_scripts": 0,
            "successful_scripts": 0,
            "failed_scripts": 0,
            "script_results": {},
            "summary": {}
        }
    
    def run_working_scripts(self):
        """Run only working auto scripts"""
        print("🚀 EHB Working Auto Script Runner")
        print("=" * 50)
        print("Running working auto scripts...")
        print("=" * 50)
        
        for script in self.working_scripts:
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
            # Run Python script
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout
            )
            
            if result.returncode == 0:
                print(f"✅ {script_name}: Success")
                self.results["script_results"][script_name] = {
                    "status": "success",
                    "returncode": result.returncode,
                    "stdout": result.stdout[:200],  # First 200 chars
                    "stderr": result.stderr[:200] if result.stderr else ""
                }
                self.results["successful_scripts"] += 1
            else:
                print(f"❌ {script_name}: Failed (return code: {result.returncode})")
                self.results["script_results"][script_name] = {
                    "status": "failed",
                    "returncode": result.returncode,
                    "stdout": result.stdout[:200],
                    "stderr": result.stderr[:200] if result.stderr else ""
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
        """Generate summary of script runs"""
        print("\n" + "=" * 50)
        print("📊 WORKING AUTO SCRIPT SUMMARY")
        print("=" * 50)
        
        total = self.results["total_scripts"]
        successful = self.results["successful_scripts"]
        failed = self.results["failed_scripts"]
        
        print(f"Total Scripts: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(successful/total*100):.1f}%" if total > 0 else "N/A")
        
        # Show successful scripts
        successful_scripts = [name for name, result in self.results["script_results"].items() 
                            if result["status"] == "success"]
        
        if successful_scripts:
            print(f"\n✅ Successful Scripts:")
            for script in successful_scripts:
                print(f"  - {script}")
        
        # Show failed scripts
        failed_scripts = [name for name, result in self.results["script_results"].items() 
                         if result["status"] in ["failed", "error", "timeout"]]
        
        if failed_scripts:
            print(f"\n❌ Failed Scripts:")
            for script in failed_scripts:
                result = self.results["script_results"][script]
                print(f"  - {script}: {result.get('error', 'Unknown error')}")
        
        # Save results
        report_file = f"reports/working_auto_script_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Report saved: {report_file}")
        print("=" * 50)
        
        self.results["summary"] = {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful/total*100) if total > 0 else 0,
            "report_file": report_file
        }

def main():
    """Main function"""
    try:
        runner = EHBWorkingAutoScriptRunner()
        results = runner.run_working_scripts()
        
        if results["summary"]["success_rate"] >= 80:
            print("\n🎉 Working auto scripts completed successfully!")
            return 0
        else:
            print(f"\n⚠️  Some scripts failed. Success rate: {results['summary']['success_rate']:.1f}%")
            return 1
            
    except Exception as e:
        print(f"❌ Working auto script runner failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 