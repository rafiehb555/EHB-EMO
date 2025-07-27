#!/usr/bin/env python3
"""
Install Missing NPM Tools and Test Them
"""

import json
import subprocess
import sys
from datetime import datetime


class NPMToolsInstaller:
    def __init__(self):
        self.installation_log = []
        self.successful_installations = []
        self.failed_installations = []
        
    def check_node_npm(self):
        """Check if Node.js and npm are available"""
        print("🔍 Checking Node.js and npm availability...")
        
        try:
            # Check Node.js
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js available: {result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
                
            # Check npm
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm available: {result.stdout.strip()}")
            else:
                print("❌ npm not found")
                return False
                
            return True
        except FileNotFoundError:
            print("❌ Node.js or npm not found in PATH")
            return False
    
    def install_npm_packages(self):
        """Install missing NPM packages"""
        print("\n📦 Installing Missing NPM Packages...")
        
        npm_packages = [
            # Testing
            "jest", "@testing-library/react", "@testing-library/jest-dom", "cypress",
            
            # Build Tools
            "webpack", "vite", "parcel", "esbuild", "rollup",
            
            # State Management
            "zustand", "recoil", "jotai", "valtio",
            
            # Development
            "typescript", "eslint", "prettier", "husky", "lint-staged",
            
            # UI Components
            "@mui/x-data-grid", "@mui/x-date-pickers", "@mui/x-charts",
            
            # Data Fetching
            "react-query", "swr",
            
            # Charts
            "recharts", "d3", "chart.js", "react-chartjs-2",
            
            # Validation
            "zod",
            
            # Icons
            "react-icons", "lucide-react",
            
            # Utilities
            "lodash", "date-fns", "axios"
        ]
        
        for package in npm_packages:
            try:
                print(f"Installing {package}...")
                result = subprocess.run(["npm", "install", package], 
                                      capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    self.successful_installations.append(f"NPM: {package}")
                    print(f"✅ {package} installed successfully")
                else:
                    self.failed_installations.append(f"NPM: {package} - {result.stderr}")
                    print(f"❌ {package} failed: {result.stderr}")
                    
            except Exception as e:
                self.failed_installations.append(f"NPM: {package} - {str(e)}")
                print(f"❌ {package} error: {str(e)}")
    
    def install_global_tools(self):
        """Install global NPM tools"""
        print("\n🛠️ Installing Global NPM Tools...")
        
        global_tools = [
            "typescript", "eslint", "prettier", "nodemon", "concurrently",
            "webpack-cli", "vite", "parcel-bundler", "esbuild",
            "jest", "cypress", "playwright", "yarn", "pnpm", "npm-check-updates",
            "http-server", "live-server", "browser-sync", "stylelint", "tsc",
            "cross-env", "rimraf"
        ]
        
        for tool in global_tools:
            try:
                print(f"Installing {tool} globally...")
                result = subprocess.run(["npm", "install", "-g", tool], 
                                      capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    self.successful_installations.append(f"Global: {tool}")
                    print(f"✅ {tool} installed successfully")
                else:
                    self.failed_installations.append(f"Global: {tool} - {result.stderr}")
                    print(f"❌ {tool} failed: {result.stderr}")
                    
            except Exception as e:
                self.failed_installations.append(f"Global: {tool} - {str(e)}")
                print(f"❌ {tool} error: {str(e)}")
    
    def test_installed_tools(self):
        """Test installed tools"""
        print("\n🧪 Testing Installed Tools...")
        
        test_commands = [
            ("Node.js", ["node", "--version"]),
            ("npm", ["npm", "--version"]),
            ("TypeScript", ["tsc", "--version"]),
            ("ESLint", ["eslint", "--version"]),
            ("Prettier", ["prettier", "--version"]),
            ("Jest", ["jest", "--version"]),
            ("Webpack", ["webpack", "--version"]),
            ("Vite", ["vite", "--version"])
        ]
        
        test_results = {}
        
        for tool_name, command in test_commands:
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    test_results[tool_name] = {"status": "✅ Working", "version": result.stdout.strip()}
                    print(f"✅ {tool_name}: {result.stdout.strip()}")
                else:
                    test_results[tool_name] = {"status": "❌ Failed", "error": result.stderr}
                    print(f"❌ {tool_name}: {result.stderr}")
            except Exception as e:
                test_results[tool_name] = {"status": "❌ Error", "error": str(e)}
                print(f"❌ {tool_name}: {str(e)}")
        
        return test_results
    
    def create_test_project(self):
        """Create a test project to verify everything works"""
        print("\n🚀 Creating Test Project...")
        
        try:
            # Create test directory
            subprocess.run(["mkdir", "test-project"], check=True)
            subprocess.run(["cd", "test-project"], check=True)
            
            # Initialize npm project
            subprocess.run(["npm", "init", "-y"], check=True)
            
            # Install test dependencies
            test_deps = ["react", "react-dom", "typescript", "jest", "eslint"]
            for dep in test_deps:
                subprocess.run(["npm", "install", dep], check=True)
            
            # Create test files
            with open("test-project/test.js", "w") as f:
                f.write("console.log('Test project created successfully!');")
            
            with open("test-project/package.json", "w") as f:
                f.write("""
{
  "name": "test-project",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "lint": "eslint .",
    "build": "tsc"
  }
}
""")
            
            print("✅ Test project created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create test project: {str(e)}")
            return False
    
    def generate_report(self, test_results):
        """Generate installation and test report"""
        print("\n" + "=" * 80)
        print("📋 NPM TOOLS INSTALLATION & TEST REPORT")
        print("=" * 80)
        
        total_successful = len(self.successful_installations)
        total_failed = len(self.failed_installations)
        total_attempted = total_successful + total_failed
        success_rate = round((total_successful / total_attempted) * 100, 1) if total_attempted > 0 else 0
        
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ Successful Installations: {total_successful}")
        print(f"❌ Failed Installations: {total_failed}")
        print(f"📊 Success Rate: {success_rate}%")
        
        print("\n✅ SUCCESSFULLY INSTALLED:")
        for item in self.successful_installations:
            print(f"  ✅ {item}")
        
        if self.failed_installations:
            print("\n❌ FAILED INSTALLATIONS:")
            for item in self.failed_installations:
                print(f"  ❌ {item}")
        
        print("\n🧪 TEST RESULTS:")
        for tool, result in test_results.items():
            print(f"  {result['status']} {tool}")
        
        print("\n" + "=" * 80)
        print("🎯 SUMMARY:")
        print(f"✅ Successfully Installed: {total_successful} tools")
        print(f"❌ Failed Installations: {total_failed} tools")
        print(f"📈 Installation Success Rate: {success_rate}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Most NPM tools are installed and working!")
        elif success_rate >= 70:
            print("👍 GOOD! Most essential NPM tools are installed!")
        else:
            print("⚠️  NEEDS ATTENTION! Many NPM tools failed to install!")
        
        print("=" * 80)
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "successful_installations": self.successful_installations,
            "failed_installations": self.failed_installations,
            "test_results": test_results,
            "summary": {
                "total_successful": total_successful,
                "total_failed": total_failed,
                "success_rate": success_rate
            }
        }
        
        with open("npm_installation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: npm_installation_report.json")
    
    def run_complete_installation(self):
        """Run complete NPM installation and testing"""
        print("🚀 Starting NPM Tools Installation and Testing...")
        print("=" * 60)
        
        # Check Node.js and npm
        if not self.check_node_npm():
            print("❌ Node.js or npm not available. Please install them first.")
            return
        
        # Install packages
        self.install_npm_packages()
        self.install_global_tools()
        
        # Test installed tools
        test_results = self.test_installed_tools()
        
        # Create test project
        self.create_test_project()
        
        # Generate report
        self.generate_report(test_results)
        
        print("\n🎉 NPM Tools Installation Complete!")
        print("🚀 Ready to run EHB AI Development System!")

if __name__ == "__main__":
    installer = NPMToolsInstaller()
    installer.run_complete_installation() 