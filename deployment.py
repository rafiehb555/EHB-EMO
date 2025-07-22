#!/usr/bin/env python3
"""
EHB-5 Deployment Script
Handles production deployment and environment setup
"""

import os
import sys
import subprocess
import json
import shutil
from datetime import datetime
from pathlib import Path


class DeploymentManager:
    """Manages deployment of EHB-5 system"""

    def __init__(self) -> None:
        self.project_root = Path(__file__).parent
        self.deployment_dir = self.project_root / "deployment"
        self.backup_dir = self.project_root / "backups"

    def create_deployment_package(self) -> None:
        """Create deployment package"""
        try:
            print("📦 Creating deployment package...")

            # Create deployment directory
            if not self.deployment_dir.exists():
                self.deployment_dir.mkdir()

            # Files to include in deployment
            deployment_files = [
                "main.py",
                "api_server.py",
                "database.py",
                "auth_manager.py",
                "data_processor.py",
                "ai_agents.py",
                "config.json",
                "requirements.txt",
                "index.html",
                "styles.css",
                "script.js",
                "README.md"]

            # Copy files to deployment directory
            for file in deployment_files:
                src = self.project_root / file
                dst = self.deployment_dir / file

                if src.exists():
                    shutil.copy2(src, dst)
                    print("✅ Copied: {file}")
                else:
                    print("⚠️  Missing: {file}")

            # Create deployment script
            self._create_deployment_script()

            print("✅ Deployment package created successfully")
            return True

        except Exception as e:
            print("❌ Deployment package creation failed: {e}")
            return False

    def _create_deployment_script(self) -> None:
        """Create deployment script for different platforms"""

        # Windows deployment script
        windows_script = """@echo off
echo Starting EHB-5 Deployment...
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting EHB-5 Application...
python main.py

pause
"""

        with open(self.deployment_dir / "deploy.bat", "w") as f:
            f.write(windows_script)

        # Linux/Mac deployment script
        linux_script = """#!/bin/bash
echo "Starting EHB-5 Deployment..."
echo

echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Starting EHB-5 Application..."
python main.py
"""

        with open(self.deployment_dir / "deploy.sh", "w") as f:
            f.write(linux_script)

        # Make Linux script executable
        os.chmod(self.deployment_dir / "deploy.sh", 0o755)

    def create_backup(self) -> None:
        """Create backup of current system"""
        try:
            print("💾 Creating system backup...")

            if not self.backup_dir.exists():
                self.backup_dir.mkdir()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = "ehb5_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name

            # Create backup
            shutil.copytree(
                self.project_root,
                backup_path,
                ignore=shutil.ignore_patterns(
                    '__pycache__',
                    '.git',
                    '*.pyc'))

            print("✅ Backup created: {backup_name}")
            return True

        except Exception as e:
            print("❌ Backup creation failed: {e}")
            return False

    def check_deployment_requirements(self) -> None:
        """Check if system meets deployment requirements"""
        try:
            print("🔍 Checking deployment requirements...")

            requirements = {
                "python_version": sys.version_info >= (3, 8),
                "required_files": [],
                "dependencies": []
            }

            # Check required files
            required_files = [
                "main.py", "api_server.py", "database.py", "auth_manager.py",
                "data_processor.py", "config.json", "requirements.txt"
            ]

            for file in required_files:
                if os.path.exists(file):
                    requirements["required_files"].append(
                        {"file": file, "status": "present"})
                else:
                    requirements["required_files"].append(
                        {"file": file, "status": "missing"})

            # Check dependencies
            try:
                import flask
                requirements["dependencies"].append(
                    {"package": "flask", "status": "installed"})
            except ImportError:
                requirements["dependencies"].append(
                    {"package": "flask", "status": "missing"})

            try:
                import jwt
                requirements["dependencies"].append(
                    {"package": "PyJWT", "status": "installed"})
            except ImportError:
                requirements["dependencies"].append(
                    {"package": "PyJWT", "status": "missing"})

            # Calculate readiness
            missing_files = len(
                [f for f in requirements["required_files"] if f["status"] == "missing"])
            missing_deps = len(
                [d for d in requirements["dependencies"] if d["status"] == "missing"])

            requirements["ready_for_deployment"] = (
                requirements["python_version"] and
                missing_files == 0 and
                missing_deps == 0
            )

            requirements["readiness_score"] = (
                (1 if requirements["python_version"] else 0) +
                (1 if missing_files == 0 else 0) +
                (1 if missing_deps == 0 else 0)
            ) / 3 * 100

            print("✅ Deployment requirements check completed")
            print("📊 Readiness Score: {requirements['readiness_score']:.1f}%")

            return requirements

        except Exception as e:
            print("❌ Requirements check failed: {e}")
            return None

    def deploy_to_production(self, target_dir: str = None) -> None:
        """Deploy system to production"""
        try:
            print("🚀 Starting production deployment...")

            # Check requirements
            requirements = self.check_deployment_requirements()
            if not requirements or not requirements["ready_for_deployment"]:
                print("❌ System not ready for deployment")
                return False

            # Create backup
            if not self.create_backup():
                print("❌ Backup creation failed")
                return False

            # Create deployment package
            if not self.create_deployment_package():
                print("❌ Deployment package creation failed")
                return False

            print("✅ Production deployment completed successfully")
            print("📁 Deployment package: {self.deployment_dir}")
            print("💾 Backup location: {self.backup_dir}")

            return True

        except Exception as e:
            print("❌ Production deployment failed: {e}")
            return False

    def generate_deployment_report(self) -> None:
        """Generate deployment report"""
        try:
            print("📊 Generating deployment report...")

            requirements = self.check_deployment_requirements()

            report = {
                "deployment_info": {
                    "timestamp": datetime.now().isoformat(),
                    "project": "EHB-5",
                    "version": "2.0.0"},
                "requirements": requirements,
                "deployment_package": {
                    "location": str(
                        self.deployment_dir),
                    "files": list(
                        self.deployment_dir.glob("*")) if self.deployment_dir.exists() else []},
                "backup_info": {
                    "location": str(
                        self.backup_dir),
                    "backups": list(
                        self.backup_dir.glob("*")) if self.backup_dir.exists() else []}}

            # Save report
            report_file = self.project_root / "deployment_report.json"
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2, default=str)

            print("✅ Deployment report saved: {report_file}")
            return report

        except Exception as e:
            print("❌ Deployment report generation failed: {e}")
            return None


def main() -> None:
    """Main deployment function"""
    print("=" * 60)
    print("🚀 EHB-5 DEPLOYMENT MANAGER")
    print("=" * 60)

    deployer = DeploymentManager()

    # Check requirements
    requirements = deployer.check_deployment_requirements()
    if requirements:
        print("📊 Readiness Score: {requirements['readiness_score']:.1f}%")

        if requirements["ready_for_deployment"]:
            print("✅ System ready for deployment")

            # Deploy to production
            if deployer.deploy_to_production():
                # Generate report
                deployer.generate_deployment_report()
                print("🎉 Deployment completed successfully!")
            else:
                print("❌ Deployment failed")
        else:
            print("❌ System not ready for deployment")
            print("Please fix the issues above before deploying")
    else:
        print("❌ Could not check deployment requirements")


if __name__ == "__main__":
    main()
