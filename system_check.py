#!/usr/bin/env python3
"""
EHB System Check
Comprehensive check for all required tools and services
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path
from datetime import datetime

class EHBSystemCheck:
    def __init__(self):
        self.results = {
            "docker": {},
            "mongodb": {},
            "aws": {},
            "openai": {},
            "python_packages": {},
            "system_info": {}
        }
    
    def check_docker(self):
        """Check Docker installation and status"""
        try:
            # Check Docker version
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check if Docker daemon is running
                ps_result = subprocess.run(['docker', 'ps'], 
                                         capture_output=True, text=True)
                
                self.results["docker"] = {
                    "installed": True,
                    "version": result.stdout.strip(),
                    "daemon_running": ps_result.returncode == 0,
                    "containers": len(ps_result.stdout.strip().split('\n')) - 1 if ps_result.stdout.strip() else 0
                }
            else:
                self.results["docker"] = {
                    "installed": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            self.results["docker"] = {
                "installed": False,
                "error": str(e)
            }
    
    def check_mongodb(self):
        """Check MongoDB installation and status"""
        try:
            # Check MongoDB version
            result = subprocess.run(['mongod', '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check if MongoDB service is running
                try:
                    import pymongo
                    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
                    client.server_info()
                    self.results["mongodb"] = {
                        "installed": True,
                        "version": result.stdout.strip(),
                        "service_running": True,
                        "connection": "successful"
                    }
                except Exception as e:
                    self.results["mongodb"] = {
                        "installed": True,
                        "version": result.stdout.strip(),
                        "service_running": False,
                        "connection": "failed",
                        "error": str(e)
                    }
            else:
                self.results["mongodb"] = {
                    "installed": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            self.results["mongodb"] = {
                "installed": False,
                "error": str(e)
            }
    
    def check_aws(self):
        """Check AWS CLI installation and configuration"""
        try:
            # Check AWS CLI version
            result = subprocess.run(['aws', '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check AWS configuration
                config_result = subprocess.run(['aws', 'configure', 'list'], 
                                            capture_output=True, text=True)
                
                self.results["aws"] = {
                    "installed": True,
                    "version": result.stdout.strip(),
                    "configured": "AWS_ACCESS_KEY_ID" in config_result.stdout or "default" in config_result.stdout
                }
            else:
                self.results["aws"] = {
                    "installed": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            self.results["aws"] = {
                "installed": False,
                "error": str(e)
            }
    
    def check_openai(self):
        """Check OpenAI API availability"""
        try:
            import openai
            
            # Check if API key is set
            api_key = os.getenv('OPENAI_API_KEY')
            
            if api_key:
                # Test API connection
                try:
                    openai.api_key = api_key
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=5
                    )
                    
                    self.results["openai"] = {
                        "available": True,
                        "api_key_set": True,
                        "connection": "successful",
                        "model": "gpt-3.5-turbo"
                    }
                except Exception as e:
                    self.results["openai"] = {
                        "available": True,
                        "api_key_set": True,
                        "connection": "failed",
                        "error": str(e)
                    }
            else:
                self.results["openai"] = {
                    "available": False,
                    "api_key_set": False,
                    "error": "OPENAI_API_KEY not found"
                }
                
        except ImportError:
            self.results["openai"] = {
                "available": False,
                "api_key_set": False,
                "error": "OpenAI package not installed"
            }
        except Exception as e:
            self.results["openai"] = {
                "available": False,
                "api_key_set": False,
                "error": str(e)
            }
    
    def check_python_packages(self):
        """Check required Python packages"""
        required_packages = [
            "flask", "pytest", "bandit", "safety", "black", "flake8", 
            "mypy", "pylint", "docker", "pymongo", "boto3", "openai",
            "requests", "json", "subprocess", "pathlib"
        ]
        
        installed_packages = []
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                installed_packages.append(package)
            except ImportError:
                missing_packages.append(package)
        
        self.results["python_packages"] = {
            "installed": installed_packages,
            "missing": missing_packages,
            "total_installed": len(installed_packages),
            "total_missing": len(missing_packages)
        }
    
    def check_system_info(self):
        """Check system information"""
        import platform
        
        self.results["system_info"] = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version,
            "python_path": sys.executable,
            "working_directory": str(Path.cwd())
        }
    
    def install_missing_packages(self):
        """Install missing Python packages"""
        missing = self.results["python_packages"]["missing"]
        
        if missing:
            print(f"📦 Installing missing packages: {missing}")
            
            for package in missing:
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", package
                    ], check=True)
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to install {package}: {e}")
    
    def setup_mongodb_docker(self):
        """Setup MongoDB using Docker"""
        if self.results["docker"]["installed"] and not self.results["mongodb"]["installed"]:
            print("🐳 Setting up MongoDB using Docker...")
            
            try:
                # Pull MongoDB image
                subprocess.run(['docker', 'pull', 'mongo:latest'], check=True)
                
                # Run MongoDB container
                subprocess.run([
                    'docker', 'run', '-d',
                    '--name', 'ehb-mongodb',
                    '-p', '27017:27017',
                    '-e', 'MONGO_INITDB_ROOT_USERNAME=ehb',
                    '-e', 'MONGO_INITDB_ROOT_PASSWORD=ehb',
                    'mongo:latest'
                ], check=True)
                
                print("✅ MongoDB container started successfully")
                self.results["mongodb"]["installed"] = True
                self.results["mongodb"]["service_running"] = True
                self.results["mongodb"]["connection"] = "docker"
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to setup MongoDB: {e}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = {
            "timestamp": str(datetime.now()),
            "system_check": self.results,
            "summary": self.generate_summary()
        }
        
        # Save report
        with open('system_check_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_summary(self):
        """Generate summary of system check"""
        docker_ok = self.results["docker"].get("installed", False)
        mongodb_ok = self.results["mongodb"].get("installed", False)
        aws_ok = self.results["aws"].get("installed", False)
        openai_ok = self.results["openai"].get("available", False)
        packages_ok = self.results["python_packages"]["total_missing"] == 0
        
        total_checks = 5
        passed_checks = sum([docker_ok, mongodb_ok, aws_ok, openai_ok, packages_ok])
        
        return {
            "docker_status": "✅" if docker_ok else "❌",
            "mongodb_status": "✅" if mongodb_ok else "❌",
            "aws_status": "✅" if aws_ok else "❌",
            "openai_status": "✅" if openai_ok else "❌",
            "packages_status": "✅" if packages_ok else "❌",
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "overall_status": "ready" if passed_checks >= 4 else "needs_setup"
        }
    
    def run_complete_check(self):
        """Run complete system check"""
        print("🔍 EHB System Check Starting...")
        print("=" * 50)
        
        # Check all components
        print("🐳 Checking Docker...")
        self.check_docker()
        
        print("🍃 Checking MongoDB...")
        self.check_mongodb()
        
        print("☁️ Checking AWS...")
        self.check_aws()
        
        print("🤖 Checking OpenAI...")
        self.check_openai()
        
        print("📦 Checking Python packages...")
        self.check_python_packages()
        
        print("💻 Checking system info...")
        self.check_system_info()
        
        # Generate report
        report = self.generate_report()
        
        return report

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EHB System Check")
    parser.add_argument("--install-missing", action="store_true", help="Install missing packages")
    parser.add_argument("--setup-mongodb", action="store_true", help="Setup MongoDB using Docker")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🔍 EHB System Check")
    print("=" * 50)
    
    checker = EHBSystemCheck()
    report = checker.run_complete_check()
    
    # Print results
    print("\n📊 SYSTEM CHECK RESULTS:")
    print("=" * 50)
    
    summary = report["summary"]
    print(f"Docker: {summary['docker_status']}")
    print(f"MongoDB: {summary['mongodb_status']}")
    print(f"AWS: {summary['aws_status']}")
    print(f"OpenAI: {summary['openai_status']}")
    print(f"Python Packages: {summary['packages_status']}")
    print(f"Overall Status: {summary['overall_status']}")
    
    # Install missing packages if requested
    if args.install_missing:
        checker.install_missing_packages()
    
    # Setup MongoDB if requested
    if args.setup_mongodb:
        checker.setup_mongodb_docker()
    
    print("\n📄 Report saved: system_check_report.json")

if __name__ == "__main__":
    main() 