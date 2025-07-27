#!/usr/bin/env python3
"""
Next.js Port Configuration Error Analyzer
Analyzes and fixes Next.js port configuration issues
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class NextJSErrorAnalyzer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"
        
    def analyze_error(self):
        """Analyze the Next.js port configuration error"""
        print("=" * 60)
        print("🔍 Next.js Port Configuration Error Analysis")
        print("=" * 60)
        
        # Error Analysis
        print("\n❌ ERROR ANALYSIS:")
        print("Command: npm run dev -- -p 3001")
        print("Error: Invalid project directory provided, no such directory: F:\\ehb 5\\3001")
        
        print("\n🔍 ROOT CAUSE:")
        print("1. Next.js v13+ mein 'next dev 3001' command galat hai")
        print("2. Next.js 3001 ko directory samajhta hai, port nahi")
        print("3. Correct syntax: 'next dev -p 3001' ya environment variable use karna")
        
        print("\n📋 CORRECT COMMANDS:")
        print("Windows PowerShell:")
        print("  set PORT=3001")
        print("  npm run dev")
        print("\nWindows CMD:")
        print("  set PORT=3001 && npm run dev")
        print("\nLinux/Mac:")
        print("  PORT=3001 npm run dev")
        
        return True
    
    def check_package_json(self):
        """Check package.json configuration"""
        print("\n📦 PACKAGE.JSON ANALYSIS:")
        
        package_json_path = self.frontend_dir / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                data = json.load(f)
            
            scripts = data.get('scripts', {})
            dev_script = scripts.get('dev', '')
            
            print(f"Current dev script: {dev_script}")
            
            if '--turbopack' in dev_script:
                print("⚠️  Turbopack flag detected - may cause issues")
            
            if 'next dev' in dev_script:
                print("✅ Next.js dev script found")
            else:
                print("❌ Next.js dev script not found")
        else:
            print("❌ package.json not found in frontend directory")
    
    def check_next_config(self):
        """Check Next.js configuration"""
        print("\n⚙️  NEXT.JS CONFIGURATION:")
        
        next_config_path = self.frontend_dir / "next.config.ts"
        if next_config_path.exists():
            print("✅ next.config.ts found")
            with open(next_config_path, 'r') as f:
                content = f.read()
                if 'port' in content.lower():
                    print("⚠️  Port configuration found in next.config.ts")
                else:
                    print("ℹ️  No port configuration in next.config.ts")
        else:
            print("ℹ️  No next.config.ts found")
    
    def check_port_usage(self):
        """Check current port usage"""
        print("\n🔌 PORT USAGE ANALYSIS:")
        
        try:
            # Check if port 3000 is in use
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            if '3000' in result.stdout:
                print("⚠️  Port 3000 is in use")
            else:
                print("✅ Port 3000 is available")
                
            if '3001' in result.stdout:
                print("⚠️  Port 3001 is in use")
            else:
                print("✅ Port 3001 is available")
        except Exception as e:
            print(f"❌ Could not check port usage: {e}")

def main():
    """Main analysis function"""
    analyzer = NextJSErrorAnalyzer()
    
    print("🚀 Starting Next.js Error Analysis...")
    
    # Run all analyses
    analyzer.analyze_error()
    analyzer.check_package_json()
    analyzer.check_next_config()
    analyzer.check_port_usage()
    
    print("\n" + "=" * 60)
    print("📋 RECOMMENDATIONS:")
    print("1. Use environment variable: set PORT=3001")
    print("2. Or modify package.json dev script")
    print("3. Or use: npm run dev -- -p 3001 (correct syntax)")
    print("4. Check for port conflicts")
    print("=" * 60)

if __name__ == "__main__":
    main() 