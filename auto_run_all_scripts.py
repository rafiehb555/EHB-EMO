#!/usr/bin/env python3
"""
EHB Auto Run All Scripts - Automatically runs all working scripts
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def run_script(script_name):
    """Run a single script and return result"""
    print(f"🔄 Running: {script_name}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name}: Success")
            return True
        else:
            print(f"❌ {script_name}: Failed")
            return False
            
    except Exception as e:
        print(f"❌ {script_name}: Error - {e}")
        return False

def main():
    """Main function to run all auto scripts"""
    print("🚀 EHB Auto Run All Scripts")
    print("=" * 50)
    print("Running all working auto scripts...")
    print("=" * 50)
    
    # List of working scripts
    working_scripts = [
        "auto_cursor_script.py",
        "startup_auto.py"
    ]
    
    # List of optimization scripts (run separately)
    optimization_scripts = [
        "optimize_performance.py",
        "memory_optimizer.py", 
        "fast_agent_optimizer.py"
    ]
    
    # List of monitoring scripts (run in background)
    monitoring_scripts = [
        "performance_monitor.py",
        "auto_restart_agent.py"
    ]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "working_scripts": {"total": 0, "successful": 0, "failed": 0},
        "optimization_scripts": {"total": 0, "successful": 0, "failed": 0},
        "monitoring_scripts": {"total": 0, "successful": 0, "failed": 0}
    }
    
    # Run working scripts
    print("\n📋 Running Working Scripts:")
    print("-" * 30)
    
    for script in working_scripts:
        results["working_scripts"]["total"] += 1
        if run_script(script):
            results["working_scripts"]["successful"] += 1
        else:
            results["working_scripts"]["failed"] += 1
    
    # Run optimization scripts
    print("\n⚡ Running Optimization Scripts:")
    print("-" * 30)
    
    for script in optimization_scripts:
        results["optimization_scripts"]["total"] += 1
        if run_script(script):
            results["optimization_scripts"]["successful"] += 1
        else:
            results["optimization_scripts"]["failed"] += 1
    
    # Run monitoring scripts in background
    print("\n📊 Starting Monitoring Scripts (Background):")
    print("-" * 30)
    
    for script in monitoring_scripts:
        results["monitoring_scripts"]["total"] += 1
        try:
            # Run in background
            subprocess.Popen([sys.executable, script])
            print(f"✅ {script}: Started in background")
            results["monitoring_scripts"]["successful"] += 1
        except Exception as e:
            print(f"❌ {script}: Failed to start - {e}")
            results["monitoring_scripts"]["failed"] += 1
    
    # Generate summary
    print("\n" + "=" * 50)
    print("📊 AUTO SCRIPT RUN SUMMARY")
    print("=" * 50)
    
    # Working scripts summary
    working = results["working_scripts"]
    if working["total"] > 0:
        success_rate = (working["successful"] / working["total"]) * 100
        print(f"Working Scripts: {working['successful']}/{working['total']} ({success_rate:.1f}%)")
    
    # Optimization scripts summary
    optimization = results["optimization_scripts"]
    if optimization["total"] > 0:
        success_rate = (optimization["successful"] / optimization["total"]) * 100
        print(f"Optimization Scripts: {optimization['successful']}/{optimization['total']} ({success_rate:.1f}%)")
    
    # Monitoring scripts summary
    monitoring = results["monitoring_scripts"]
    if monitoring["total"] > 0:
        success_rate = (monitoring["successful"] / monitoring["total"]) * 100
        print(f"Monitoring Scripts: {monitoring['successful']}/{monitoring['total']} ({success_rate:.1f}%)")
    
    # Save results
    report_file = f"reports/auto_run_all_scripts_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path("reports").mkdir(exist_ok=True)
    
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed report saved: {report_file}")
    print("=" * 50)
    
    # Final status
    total_successful = (working["successful"] + optimization["successful"] + monitoring["successful"])
    total_scripts = (working["total"] + optimization["total"] + monitoring["total"])
    
    if total_scripts > 0:
        overall_success_rate = (total_successful / total_scripts) * 100
        print(f"\nOverall Success Rate: {overall_success_rate:.1f}%")
        
        if overall_success_rate >= 80:
            print("🎉 Auto script run completed successfully!")
            return 0
        else:
            print("⚠️  Some scripts failed, but core functionality is working.")
            return 1
    else:
        print("❌ No scripts were run.")
        return 1

if __name__ == "__main__":
    exit(main()) 