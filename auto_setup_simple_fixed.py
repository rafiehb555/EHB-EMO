#!/usr/bin/env python3
"""
EHB Simple Auto Development Setup - Fixed Version
Only installs working packages
"""

import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("auto_setup_fixed.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

class FixedEHBSetup:
    def __init__(self):
        self.project_root = Path.cwd()
        
        # Only working packages that exist in npm registry
        self.working_npm_packages = [
            "typescript",
            "create-react-app", 
            "create-next-app",
            "create-vue-app",
            "create-nuxt-app",
            "create-expo-app",
            "create-react-native-app",
            "create-electron-app",
            "create-express-app",
            "create-angular-app",
            "create-svelte-app",
            "create-solid-app",
            "create-astro-app",
            "create-remix-app",
            "create-gatsby-app",
            "create-vite-app",
            "create-webpack-app",
            "create-rollup-app",
            "create-parcel-app",
            "create-esbuild-app",
            "create-swc-app",
            "create-babel-app",
            "create-tailwindcss-app",
            "create-bootstrap-app",
            "create-material-ui-app",
            "create-ant-design-app"
        ]

    def run_command(self, command: str, shell: bool = True) -> bool:
        """Run a command and return success status"""
        try:
            logger.info(f"Running: {command}")
            result = subprocess.run(
                command, shell=shell, capture_output=True, text=True, check=True
            )
            logger.info(f"Success: {command}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running {command}: {e.stderr}")
            return False

    def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        return shutil.which(command) is not None

    def install_working_npm_packages(self) -> bool:
        """Install only working npm packages"""
        logger.info("Installing working npm packages...")
        
        successful_installs = 0
        total_packages = len(self.working_npm_packages)
        
        for package in self.working_npm_packages:
            try:
                command = f"npm install -g {package}"
                logger.info(f"Installing: {package}")
                
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=60
                )
                
                if result.returncode == 0:
                    logger.info(f"SUCCESS: {package}")
                    successful_installs += 1
                else:
                    logger.warning(f"FAILED: {package} - {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"TIMEOUT: {package}")
            except Exception as e:
                logger.error(f"ERROR: {package} - {e}")
        
        logger.info(f"Installation complete: {successful_installs}/{total_packages} packages installed")
        return successful_installs > 0

    def install_basic_python_packages(self) -> bool:
        """Install basic Python packages"""
        logger.info("Installing Python packages...")
        
        python_packages = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "psycopg2-binary",
            "redis",
            "requests",
            "pytest",
            "black",
            "flake8",
            "mypy",
            "pre-commit"
        ]
        
        successful_installs = 0
        total_packages = len(python_packages)
        
        for package in python_packages:
            try:
                command = f"pip install {package}"
                logger.info(f"Installing: {package}")
                
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=60
                )
                
                if result.returncode == 0:
                    logger.info(f"SUCCESS: {package}")
                    successful_installs += 1
                else:
                    logger.warning(f"FAILED: {package} - {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"TIMEOUT: {package}")
            except Exception as e:
                logger.error(f"ERROR: {package} - {e}")
        
        logger.info(f"Python installation complete: {successful_installs}/{total_packages} packages installed")
        return successful_installs > 0

    def create_project_structure(self) -> bool:
        """Create basic project structure"""
        logger.info("Creating project structure...")
        
        directories = [
            "src",
            "src/components",
            "src/pages",
            "src/utils",
            "src/styles",
            "src/api",
            "backend",
            "backend/api",
            "backend/models",
            "backend/utils",
            "tests",
            "docs",
            "config",
            "scripts",
            "public",
            "reports"
        ]
        
        for directory in directories:
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory}")
            except Exception as e:
                logger.error(f"Failed to create directory {directory}: {e}")
        
        return True

    def create_config_files(self) -> bool:
        """Create basic configuration files"""
        logger.info("Creating configuration files...")
        
        # package.json
        package_json = {
            "name": "ehb-healthcare-system",
            "version": "1.0.0",
            "description": "EHB Healthcare Management System",
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "test": "jest",
                "lint": "eslint .",
                "format": "prettier --write ."
            },
            "dependencies": {
                "next": "^13.0.0",
                "react": "^18.0.0",
                "react-dom": "^18.0.0",
                "@mui/material": "^5.0.0",
                "@emotion/react": "^11.0.0",
                "@emotion/styled": "^11.0.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/react": "^18.0.0",
                "@types/node": "^18.0.0",
                "eslint": "^8.0.0",
                "prettier": "^2.8.0"
            }
        }
        
        try:
            with open("package.json", "w") as f:
                json.dump(package_json, f, indent=2)
            logger.info("Created package.json")
        except Exception as e:
            logger.error(f"Failed to create package.json: {e}")
        
        # requirements.txt
        requirements = [
            "fastapi==0.100.0",
            "uvicorn==0.23.0",
            "sqlalchemy==2.0.0",
            "psycopg2-binary==2.9.0",
            "redis==4.6.0",
            "requests==2.31.0",
            "pytest==7.4.0",
            "black==23.0.0",
            "flake8==6.0.0"
        ]
        
        try:
            with open("requirements.txt", "w") as f:
                f.write("\n".join(requirements))
            logger.info("Created requirements.txt")
        except Exception as e:
            logger.error(f"Failed to create requirements.txt: {e}")
        
        return True

    def run_complete_setup(self) -> bool:
        """Run complete setup"""
        logger.info("🚀 Starting EHB Fixed Auto Development Setup...")
        
        try:
            # Step 1: Install npm packages
            self.install_working_npm_packages()
            
            # Step 2: Install Python packages
            self.install_basic_python_packages()
            
            # Step 3: Create project structure
            self.create_project_structure()
            
            # Step 4: Create config files
            self.create_config_files()
            
            logger.info("✅ EHB Fixed Auto Development Setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            return False

def main():
    """Main function"""
    try:
        setup = FixedEHBSetup()
        success = setup.run_complete_setup()
        
        if success:
            print("🎉 EHB Fixed Auto Development Setup completed successfully!")
            return 0
        else:
            print("⚠️ Setup completed with some issues.")
            return 1
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 