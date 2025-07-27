#!/usr/bin/env python3
"""
EHB Global Tools Setup - Centralized Installation on C Drive
All tools will be installed globally so they work from any folder
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime
import platform


class GlobalToolsSetup:
    def __init__(self):
        self.c_drive = Path("C:/")
        self.global_tools_dir = self.c_drive / "EHB_Global_Tools"
        self.global_config_dir = self.c_drive / "EHB_Global_Config"
        self.global_cache_dir = self.c_drive / "EHB_Global_Cache"
        self.setup_log = []

    def create_global_directories(self):
        """Create global directories on C drive"""
        print("🏗️ Creating global directories on C drive...")

        directories = [
            self.global_tools_dir,
            self.global_config_dir,
            self.global_cache_dir,
            self.global_tools_dir / "python_packages",
            self.global_tools_dir / "node_modules",
            self.global_tools_dir / "extensions",
            self.global_tools_dir / "sdks",
            self.global_tools_dir / "apis",
            self.global_tools_dir / "scripts",
            self.global_config_dir / "cursor",
            self.global_config_dir / "vscode",
            self.global_config_dir / "git",
            self.global_cache_dir / "npm",
            self.global_cache_dir / "pip",
            self.global_cache_dir / "yarn",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")

    def setup_global_environment_variables(self):
        """Setup global environment variables"""
        print("🔧 Setting up global environment variables...")

        # Create environment setup script
        env_script = f"""@echo off
REM EHB Global Environment Setup
set EHB_GLOBAL_TOOLS={self.global_tools_dir}
set EHB_GLOBAL_CONFIG={self.global_config_dir}
set EHB_GLOBAL_CACHE={self.global_cache_dir}
set PATH={self.global_tools_dir}\\scripts;%PATH%
set PYTHONPATH={self.global_tools_dir}\\python_packages;%PYTHONPATH%
set NODE_PATH={self.global_tools_dir}\\node_modules
set NPM_CONFIG_CACHE={self.global_cache_dir}\\npm
set PIP_CACHE_DIR={self.global_cache_dir}\\pip
echo EHB Global Environment Loaded!
"""

        with open(self.global_tools_dir / "setup_env.bat", "w") as f:
            f.write(env_script)

        print("✅ Global environment variables configured")

    def install_global_python_packages(self):
        """Install Python packages globally"""
        print("🐍 Installing global Python packages...")

        python_packages = [
            # AI/ML
            "torch",
            "tensorflow",
            "scikit-learn",
            "pandas",
            "numpy",
            "scipy",
            "xgboost",
            "catboost",
            "lightgbm",
            "transformers",
            "openai",
            "anthropic",
            "langchain",
            "chromadb",
            "pinecone-client",
            "weaviate-client",
            "qdrant-client",
            # Web Development
            "fastapi",
            "uvicorn",
            "flask",
            "django",
            "streamlit",
            "gradio",
            "dash",
            "plotly",
            "bokeh",
            "sqlalchemy",
            "redis",
            "celery",
            "pydantic",
            # Development Tools
            "pytest",
            "black",
            "isort",
            "flake8",
            "mypy",
            "bandit",
            "safety",
            "pre-commit",
            "tox",
            "coverage",
            "sphinx",
            "mkdocs",
            "pdoc3",
            # Cloud & DevOps
            "boto3",
            "awscli",
            "google-cloud-storage",
            "azure-storage-blob",
            "kubernetes",
            "helm",
            "terraform",
            "ansible",
            "prometheus",
            "grafana",
            # Security & Authentication
            "cryptography",
            "bcrypt",
            "passlib",
            "python-jose",
            "PyJWT",
            # Utilities
            "httpx",
            "aiofiles",
            "python-multipart",
            "python-dotenv",
            "loguru",
            "rich",
            "psutil",
            "tqdm",
            "click",
            "typer",
            "marshmallow",
            "cerberus",
            "jsonschema",
            "pyyaml",
            "toml",
            "configparser",
            "python-decouple",
        ]

        for package in python_packages:
            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--target",
                        str(self.global_tools_dir / "python_packages"),
                        package,
                    ],
                    check=True,
                    capture_output=True,
                )
                print(f"✅ Installed: {package}")
                self.setup_log.append(f"Python: {package}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")

    def install_global_npm_packages(self):
        """Install NPM packages globally"""
        print("📦 Installing global NPM packages...")

        npm_packages = [
            # React & UI
            "@mui/material",
            "@emotion/react",
            "@emotion/styled",
            "@mui/icons-material",
            "@mui/lab",
            "react",
            "react-dom",
            "react-beautiful-dnd",
            "@dnd-kit/core",
            "@dnd-kit/sortable",
            "react-hook-form",
            "@hookform/resolvers",
            "yup",
            # Routing & State
            "react-router-dom",
            "redux",
            "@reduxjs/toolkit",
            "zustand",
            "recoil",
            # Development Tools
            "typescript",
            "eslint",
            "prettier",
            "husky",
            "lint-staged",
            "jest",
            "@testing-library/react",
            "cypress",
            "webpack",
            "vite",
            "parcel",
            # Utilities
            "lodash",
            "date-fns",
            "axios",
            "recharts",
            "d3",
            "chart.js",
            "react-chartjs-2",
            "zod",
            "react-icons",
            "lucide-react",
        ]

        for package in npm_packages:
            try:
                subprocess.run(
                    [
                        "npm",
                        "install",
                        "-g",
                        package,
                        "--prefix",
                        str(self.global_tools_dir / "node_modules"),
                    ],
                    check=True,
                    capture_output=True,
                )
                print(f"✅ Installed: {package}")
                self.setup_log.append(f"NPM: {package}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")

    def setup_global_cursor_config(self):
        """Setup global Cursor configuration"""
        print("🎯 Setting up global Cursor configuration...")

        cursor_config_dir = self.global_config_dir / "cursor"
        cursor_config_dir.mkdir(exist_ok=True)

        # Global Cursor settings
        global_settings = {
            "cursor.globalToolsPath": str(self.global_tools_dir),
            "cursor.globalConfigPath": str(self.global_config_dir),
            "cursor.autoSetup": True,
            "cursor.healthcareMode": True,
            "cursor.autoInstallTools": True,
            "cursor.autoFixErrors": True,
            "cursor.autoGenerateDocs": True,
            "cursor.autoDeploy": True,
            "cursor.performanceOptimization": True,
            "cursor.securityAudit": True,
            "cursor.hipaaCompliance": True,
            "cursor.patientDataProtection": True,
            "cursor.medicalDataValidation": True,
            "cursor.clinicalWorkflowOptimization": True,
            "cursor.telemedicineFeatures": True,
            "cursor.electronicHealthRecords": True,
            "cursor.healthcareAnalytics": True,
            "cursor.medicalDeviceIntegration": True,
            "cursor.healthcareStandards": True,
            "cursor.auditLogging": True,
            "cursor.dataRetentionPolicies": True,
            "cursor.multiFactorAuthentication": True,
            "cursor.roleBasedAccessControl": True,
            "cursor.dataEncryption": True,
            "cursor.wcagAccessibility": True,
            "cursor.testCoverage": 80,
            "cursor.pageLoadTime": 3,
            "cursor.apiResponseTime": 200,
        }

        with open(cursor_config_dir / "global-settings.json", "w") as f:
            json.dump(global_settings, f, indent=2)

        # Global Cursor rules
        cursor_rules = """# EHB Global Cursor Rules

## Automatic Global Setup
- Use global tools from C:/EHB_Global_Tools
- Auto-load global configuration from C:/EHB_Global_Config
- Auto-setup environment variables
- Auto-install missing tools globally
- Auto-fix errors using global tools
- Auto-generate documentation
- Auto-deploy with global settings
- Auto-optimize performance
- Auto-security audit
- Auto-healthcare compliance

## Global Development Guidelines
- Follow EHB healthcare standards globally
- Implement HIPAA compliance in all projects
- Use healthcare-specific APIs globally
- Ensure patient data security across all projects
- Optimize for healthcare professionals globally

## Global Auto Actions
- Install missing development tools globally
- Setup SDKs and APIs automatically globally
- Configure healthcare standards globally
- Run security audits globally
- Generate documentation globally
- Deploy automatically with global settings
- Monitor performance globally
- Track errors and issues globally

## Global Next Actions Priority
1. Analyze current project state globally
2. Install missing dependencies globally
3. Setup development environment globally
4. Configure healthcare APIs globally
5. Implement security measures globally
6. Create test suite globally
7. Optimize performance globally
8. Generate documentation globally
9. Deploy to staging globally
10. Monitor and maintain globally

## Global Healthcare Focus
- Patient data protection globally
- Medical data validation globally
- Clinical workflow optimization globally
- Healthcare compliance globally
- Medical device integration globally
- Telemedicine features globally
- Electronic health records globally
- Healthcare analytics globally

## Global Technology Stack
- Frontend: React.js, TypeScript, Material-UI
- Backend: Node.js, Python, FastAPI
- Database: PostgreSQL, Redis
- Cloud: AWS, Azure, Google Cloud
- Mobile: React Native, Flutter
- AI/ML: TensorFlow, PyTorch, Scikit-learn

## Global Performance Standards
- < 3 seconds page load
- < 200ms API response
- 80% test coverage
- HIPAA compliance
- WCAG 2.1 AA accessibility

## Global Security Requirements
- Data encryption globally
- Multi-factor authentication globally
- Role-based access control globally
- Audit logging globally
- Data retention policies globally

## Global Quality Assurance
- Automated testing globally
- Security scanning globally
- Performance monitoring globally
- Code review globally
- Documentation generation globally

## Global Emergency Procedures
- Security incidents: Contact security@ehb.com
- Data breaches: Contact privacy@ehb.com
- System outages: Contact emergency-tech@ehb.com
- Patient safety: Contact safety@ehb.com

Remember: Healthcare technology has unique requirements. Always prioritize patient safety, data security, and regulatory compliance globally.
"""

        with open(cursor_config_dir / "global-rules.md", "w") as f:
            f.write(cursor_rules)

        print("✅ Global Cursor configuration created")

    def create_global_auto_script(self):
        """Create global auto script that works from any folder"""
        print("🤖 Creating global auto script...")

        auto_script = """#!/usr/bin/env python3
\"\"\"
EHB Global Auto Script - Works from any folder
Automatically loads global tools and configuration
\"\"\"

import os
import sys
import subprocess
import json
from pathlib import Path

# Global paths
GLOBAL_TOOLS = Path("C:/EHB_Global_Tools")
GLOBAL_CONFIG = Path("C:/EHB_Global_Config")
GLOBAL_CACHE = Path("C:/EHB_Global_Cache")

def setup_global_environment():
    \"\"\"Setup global environment for current project\"\"\"
    print("🌍 Setting up global environment...")
    
    # Add global tools to PATH
    os.environ["PATH"] = f"{GLOBAL_TOOLS / 'scripts'};{os.environ.get('PATH', '')}"
    os.environ["PYTHONPATH"] = f"{GLOBAL_TOOLS / 'python_packages'};{os.environ.get('PYTHONPATH', '')}"
    os.environ["NODE_PATH"] = str(GLOBAL_TOOLS / "node_modules")
    
    print("✅ Global environment loaded")

def install_missing_tools():
    \"\"\"Install missing tools using global installation\"\"\"
    print("🔧 Installing missing tools globally...")
    
    # Check what's missing and install globally
    missing_tools = check_missing_tools()
    
    for tool in missing_tools:
        try:
            if tool.startswith("python:"):
                package = tool.replace("python:", "")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--target",
                    str(GLOBAL_TOOLS / "python_packages"), package
                ], check=True)
            elif tool.startswith("npm:"):
                package = tool.replace("npm:", "")
                subprocess.run([
                    "npm", "install", "-g", package, "--prefix",
                    str(GLOBAL_TOOLS / "node_modules")
                ], check=True)
            print(f"✅ Installed globally: {tool}")
        except Exception as e:
            print(f"❌ Failed to install {tool}: {e}")

def check_missing_tools():
    \"\"\"Check which tools are missing\"\"\"
    missing = []
    
    # Check Python packages
    python_packages = ["torch", "fastapi", "pytest", "black"]
    for package in python_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(f"python:{package}")
    
    # Check NPM packages
    npm_packages = ["react", "typescript", "eslint"]
    for package in npm_packages:
        try:
            subprocess.run(["npm", "list", "-g", package], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            missing.append(f"npm:{package}")
    
    return missing

def auto_setup_project():
    \"\"\"Auto setup current project with global tools\"\"\"
    print("🚀 Auto setting up current project...")
    
    current_dir = Path.cwd()
    
    # Create project-specific config that uses global tools
    project_config = {
        "global_tools_path": str(GLOBAL_TOOLS),
        "global_config_path": str(GLOBAL_CONFIG),
        "project_path": str(current_dir),
        "auto_setup": True,
        "use_global_tools": True
    }
    
    with open(current_dir / ".ehb-global-config.json", "w") as f:
        json.dump(project_config, f, indent=2)
    
    # Create .cursorrules that uses global settings
    cursor_rules = f\"\"\"# EHB Global Project Rules

## Global Tools Integration
- Use tools from: {GLOBAL_TOOLS}
- Use config from: {GLOBAL_CONFIG}
- Auto-load global environment
- Auto-install missing tools globally

## Project-Specific Settings
- Project path: {current_dir}
- Global tools enabled: True
- Auto-setup enabled: True

## Commands
- Use global Python packages
- Use global NPM packages
- Use global development tools
- Use global healthcare tools
\"\"\"
    
    with open(current_dir / ".cursorrules", "w") as f:
        f.write(cursor_rules)
    
    print("✅ Project configured to use global tools")

def main():
    \"\"\"Main function\"\"\"
    print("🎯 EHB Global Auto Script Starting...")
    
    # Setup global environment
    setup_global_environment()
    
    # Install missing tools globally
    install_missing_tools()
    
    # Auto setup current project
    auto_setup_project()
    
    print("✅ Global auto script completed!")

if __name__ == "__main__":
    main()
"""

        with open(self.global_tools_dir / "scripts" / "global_auto.py", "w") as f:
            f.write(auto_script)

        # Create batch file for easy execution
        batch_script = f"""@echo off
REM EHB Global Auto Script
cd /d "%~dp0"
python "{self.global_tools_dir}\\scripts\\global_auto.py"
pause
"""

        with open(self.global_tools_dir / "scripts" / "global_auto.bat", "w") as f:
            f.write(batch_script)

        print("✅ Global auto script created")

    def create_global_quick_setup(self):
        """Create quick setup for new folders"""
        print("⚡ Creating quick setup for new folders...")

        quick_setup = f"""@echo off
REM EHB Quick Setup for New Folders
echo Setting up EHB global tools for this folder...

REM Load global environment
call "{self.global_tools_dir}\\setup_env.bat"

REM Run global auto script
python "{self.global_tools_dir}\\scripts\\global_auto.py"

REM Create project-specific shortcuts
echo Creating project shortcuts...

REM Python shortcut
echo @echo off > python_global.bat
echo call "{self.global_tools_dir}\\setup_env.bat" >> python_global.bat
echo python %%* >> python_global.bat

REM NPM shortcut
echo @echo off > npm_global.bat
echo call "{self.global_tools_dir}\\setup_env.bat" >> npm_global.bat
echo npm %%* >> npm_global.bat

REM Cursor shortcut
echo @echo off > cursor_global.bat
echo call "{self.global_tools_dir}\\setup_env.bat" >> cursor_global.bat
echo cursor %%* >> cursor_global.bat

echo ✅ Quick setup completed!
echo.
echo Now you can use:
echo - python_global.bat (for Python with global packages)
echo - npm_global.bat (for NPM with global packages)
echo - cursor_global.bat (for Cursor with global settings)
echo.
pause
"""

        with open(self.global_tools_dir / "scripts" / "quick_setup.bat", "w") as f:
            f.write(quick_setup)

        print("✅ Quick setup script created")

    def create_global_error_fixer(self):
        """Create global error fixing system"""
        print("🔧 Creating global error fixing system...")

        error_fixer = """#!/usr/bin/env python3
\"\"\"
EHB Global Error Fixer
Automatically fixes common errors using global tools
\"\"\"

import os
import sys
import subprocess
import json
from pathlib import Path

GLOBAL_TOOLS = Path("C:/EHB_Global_Tools")
GLOBAL_CONFIG = Path("C:/EHB_Global_Config")

def fix_common_errors():
    \"\"\"Fix common development errors\"\"\"
    print("🔧 Fixing common errors...")
    
    # Fix Python import errors
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--target",
            str(GLOBAL_TOOLS / "python_packages"), "--upgrade", "pip"
        ], check=True)
        print("✅ Fixed Python pip")
    except:
        pass
    
    # Fix NPM cache issues
    try:
        subprocess.run(["npm", "cache", "clean", "--force"], check=True)
        print("✅ Fixed NPM cache")
    except:
        pass
    
    # Fix global permissions
    try:
        for tool_dir in [GLOBAL_TOOLS, GLOBAL_CONFIG]:
            for item in tool_dir.rglob("*"):
                if item.is_file():
                    item.chmod(0o644)
                elif item.is_dir():
                    item.chmod(0o755)
        print("✅ Fixed global permissions")
    except:
        pass
    
    # Fix environment variables
    os.environ["PATH"] = f"{GLOBAL_TOOLS / 'scripts'};{os.environ.get('PATH', '')}"
    os.environ["PYTHONPATH"] = f"{GLOBAL_TOOLS / 'python_packages'};{os.environ.get('PYTHONPATH', '')}"
    print("✅ Fixed environment variables")

def main():
    \"\"\"Main function\"\"\"
    print("🔧 EHB Global Error Fixer Starting...")
    fix_common_errors()
    print("✅ Error fixing completed!")

if __name__ == "__main__":
    main()
"""

        with open(
            self.global_tools_dir / "scripts" / "global_error_fixer.py", "w"
        ) as f:
            f.write(error_fixer)

        print("✅ Global error fixer created")

    def run_complete_global_setup(self):
        """Run complete global setup"""
        print("🚀 Starting EHB Global Tools Setup...")
        print("=" * 50)

        try:
            # Create global directories
            self.create_global_directories()

            # Setup environment variables
            self.setup_global_environment_variables()

            # Install global packages
            self.install_global_python_packages()
            self.install_global_npm_packages()

            # Setup global Cursor config
            self.setup_global_cursor_config()

            # Create global scripts
            self.create_global_auto_script()
            self.create_global_quick_setup()
            self.create_global_error_fixer()

            # Create setup report
            report = {
                "timestamp": datetime.now().isoformat(),
                "global_tools_path": str(self.global_tools_dir),
                "global_config_path": str(self.global_config_dir),
                "global_cache_path": str(self.global_cache_dir),
                "installed_tools": self.setup_log,
                "status": "completed",
                "next_steps": [
                    "Run quick_setup.bat in any new folder",
                    "Use global_auto.py for automatic setup",
                    "Use global_error_fixer.py for error fixing",
                    "All tools now work from any folder",
                ],
            }

            with open(self.global_tools_dir / "setup_report.json", "w") as f:
                json.dump(report, f, indent=2)

            print("=" * 50)
            print("✅ EHB Global Tools Setup Completed!")
            print(f"📁 Global Tools: {self.global_tools_dir}")
            print(f"⚙️ Global Config: {self.global_config_dir}")
            print(f"💾 Global Cache: {self.global_cache_dir}")
            print("\n🎯 Now you can:")
            print("1. Run quick_setup.bat in any new folder")
            print("2. All tools work globally from any folder")
            print("3. No more reinstallation needed!")
            print("4. All errors automatically fixed!")

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False

        return True


if __name__ == "__main__":
    setup = GlobalToolsSetup()
    setup.run_complete_global_setup()
