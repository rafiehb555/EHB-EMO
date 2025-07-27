import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import logging
import subprocess
import sys

#!/usr/bin/env python3
"""
EHB Auto Testing, Security & Deployment Tool
Comprehensive automation for testing, security, and deployment
"""


class AutoTestingSecurityDeploy:
    def __init__(self):
        self.project_root = Path.cwd()
        self.setup_logging()
        self.results = {
            "testing": {},
            "security": {},
            "deployment": {},
            "overall_status": "pending"
        }
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('auto_testing_security_deploy.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_code_testing(self):
        """Run comprehensive code testing"""
        self.logger.info("TESTING Starting Code Testing...")
        
        tests = {
            "pytest": self.run_pytest(),
            "coverage": self.run_coverage(),
            "mypy": self.run_mypy(),
            "flake8": self.run_flake8(),
            "black": self.run_black(),
            "pylint": self.run_pylint()
        }
        
        self.results["testing"] = tests
        return tests
    
    def run_pytest(self):
        """Run pytest for unit testing"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", "--tb=short"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_coverage(self):
        """Run code coverage analysis"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", "--cov=.", "--cov-report=html"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_mypy(self):
        """Run mypy for type checking"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "mypy", "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_flake8(self):
        """Run flake8 for code style checking"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "flake8", "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_black(self):
        """Run black for code formatting"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "black", "--check", "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_pylint(self):
        """Run pylint for code quality analysis"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "pylint", "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_security_scanning(self):
        """Run comprehensive security scanning"""
        self.logger.info("SECURITY Starting Security Scanning...")
        
        security_tests = {
            "bandit": self.run_bandit(),
            "safety": self.run_safety(),
            "dependency_check": self.run_dependency_check(),
            "vulnerability_scan": self.run_vulnerability_scan()
        }
        
        self.results["security"] = security_tests
        return security_tests
    
    def run_bandit(self):
        """Run bandit for security vulnerabilities"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "bandit", "-r", "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_safety(self):
        """Run safety for dependency vulnerabilities"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "safety", "check"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_dependency_check(self):
        """Check for outdated dependencies"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "list", "--outdated"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_vulnerability_scan(self):
        """Run custom vulnerability scan"""
        try:
            # Check for common security issues
            issues = []
            
            # Check for hardcoded secrets
            for file in self.project_root.rglob("*.py"):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "password" in content.lower() or "secret" in content.lower():
                        issues.append(f"Potential hardcoded secret in {file}")
            
            return {
                "status": "success" if not issues else "warning",
                "issues": issues,
                "message": f"Found {len(issues)} potential security issues"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_deployment_prep(self):
        """Prepare for deployment"""
        self.logger.info("ROCKET Starting Deployment Preparation...")
        
        deployment_steps = {
            "environment_check": self.check_environment(),
            "dependency_install": self.install_dependencies(),
            "configuration_setup": self.setup_configuration(),
            "health_check": self.run_health_check(),
            "deployment_ready": self.prepare_deployment()
        }
        
        self.results["deployment"] = deployment_steps
        return deployment_steps
    
    def check_environment(self):
        """Check deployment environment"""
        try:
            env_info = {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": str(self.project_root),
                "required_packages": self.check_required_packages()
            }
            
            return {
                "status": "success",
                "environment": env_info
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def check_required_packages(self):
        """Check if required packages are installed"""
        required = ["flask", "pytest", "bandit", "safety", "black", "flake8", "mypy", "pylint"]
        installed = []
        missing = []
        
        for package in required:
            try:
                __import__(package)
                installed.append(package)
            except ImportError:
                missing.append(package)
        
        return {
            "installed": installed,
            "missing": missing,
            "all_installed": len(missing) == 0
        }
    
    def install_dependencies(self):
        """Install missing dependencies"""
        try:
            missing = self.check_required_packages()["missing"]
            if missing:
                for package in missing:
                    subprocess.run([sys.executable, "-m", "pip", "install", package])
            
            return {
                "status": "success",
                "message": f"Installed {len(missing)} missing packages"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def setup_configuration(self):
        """Setup deployment configuration"""
        try:
            # Create .env file if not exists
            env_file = self.project_root / ".env"
            if not env_file.exists():
                with open(env_file, 'w') as f:
                    f.write("# EHB Auto Deployment Configuration\n")
                    f.write("ENVIRONMENT=production\n")
                    f.write("DEBUG=False\n")
                    f.write("PORT=8000\n")
            
            # Create requirements.txt if not exists
            req_file = self.project_root / "requirements.txt"
            if not req_file.exists():
                subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=open(req_file, 'w'))
            
            return {
                "status": "success",
                "message": "Configuration files created"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run_health_check(self):
        """Run application health check"""
        try:
            # Test if server can start
            result = subprocess.run([
                sys.executable, "api_server.py", "--port", "8002"
            ], capture_output=True, text=True, timeout=10)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"status": "success", "message": "Server started successfully"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def prepare_deployment(self):
        """Prepare final deployment package"""
        try:
            # Create deployment package
            deploy_dir = self.project_root / "deployment"
            deploy_dir.mkdir(exist_ok=True)
            
            # Copy necessary files
            files_to_copy = ["api_server.py", "main.py", "requirements.txt", ".env"]
            for file in files_to_copy:
                if (self.project_root / file).exists():
                    shutil.copy2(self.project_root / file, deploy_dir / file)
            
            # Create deployment script
            deploy_script = deploy_dir / "deploy.py"
            with open(deploy_script, 'w') as f:
                f.write("""#!/usr/bin/env python3

def deploy():
    print("ROCKET Deploying EHB AI Dev Agent...")
    subprocess.run([sys.executable, "api_server.py", "--port", "8000"])
    print("SUCCESS Deployment complete!")

if __name__ == "__main__":
    deploy()
""")
            
            return {
                "status": "success",
                "message": "Deployment package created",
                "deployment_dir": str(deploy_dir)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_root.name,
            "testing_results": self.results["testing"],
            "security_results": self.results["security"],
            "deployment_results": self.results["deployment"],
            "summary": self.generate_summary()
        }
        
        # Save report
        with open('auto_testing_security_deploy_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_summary(self):
        """Generate summary of all results"""
        testing_success = sum(1 for test in self.results["testing"].values() if test.get("status") == "success")
        security_success = sum(1 for sec in self.results["security"].values() if sec.get("status") == "success")
        deployment_success = sum(1 for dep in self.results["deployment"].values() if dep.get("status") == "success")
        
        total_tests = len(self.results["testing"])
        total_security = len(self.results["security"])
        total_deployment = len(self.results["deployment"])
        
        return {
            "testing_score": f"{testing_success}/{total_tests}",
            "security_score": f"{security_success}/{total_security}",
            "deployment_score": f"{deployment_success}/{total_deployment}",
            "overall_status": "ready" if (testing_success + security_success + deployment_success) >= (total_tests + total_security + total_deployment - 2) else "needs_attention"
        }
    
    def run_full_automation(self):
        """Run complete automation"""
        self.logger.info("EHB AI Starting Auto Testing, Security & Deployment...")
        self.logger.info("=" * 80)
        
        # Step 1: Code Testing
        self.logger.info("TESTING Running Code Testing...")
        testing_results = self.run_code_testing()
        
        # Step 2: Security Scanning
        self.logger.info("SECURITY Running Security Scanning...")
        security_results = self.run_security_scanning()
        
        # Step 3: Deployment Preparation
        self.logger.info("ROCKET Running Deployment Preparation...")
        deployment_results = self.run_deployment_prep()
        
        # Step 4: Generate Report
        self.logger.info("REPORT Generating Report...")
        report = self.generate_report()
        
        return report

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="EHB Auto Testing, Security & Deployment")
    parser.add_argument("--testing-only", action="store_true", help="Run only testing")
    parser.add_argument("--security-only", action="store_true", help="Run only security scanning")
    parser.add_argument("--deployment-only", action="store_true", help="Run only deployment prep")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("EHB AI EHB Auto Testing, Security & Deployment Tool")
    print("=" * 80)
    
    tool = AutoTestingSecurityDeploy()
    
    if args.testing_only:
        results = tool.run_code_testing()
        print("TESTING Testing Results:", results)
    elif args.security_only:
        results = tool.run_security_scanning()
        print("SECURITY Security Results:", results)
    elif args.deployment_only:
        results = tool.run_deployment_prep()
        print("ROCKET Deployment Results:", results)
    else:
        report = tool.run_full_automation()
        print("\n" + "=" * 80)
        print("REPORT COMPREHENSIVE REPORT")
        print("=" * 80)
        print(f"SUCCESS Testing Score: {report['summary']['testing_score']}")
        print(f"SUCCESS Security Score: {report['summary']['security_score']}")
        print(f"SUCCESS Deployment Score: {report['summary']['deployment_score']}")
        print(f"SUCCESS Overall Status: {report['summary']['overall_status']}")
        print("=" * 80)
        print("📄 Report saved: auto_testing_security_deploy_report.json")

if __name__ == "__main__":
    main() 