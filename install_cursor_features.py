#!/usr/bin/env python3
"""
Install Cursor Features and Components in EHB AI Dev
"""

import json
import subprocess
import sys
from datetime import datetime


class CursorFeaturesInstaller:
    def __init__(self):
        self.installed_features = []
        self.failed_features = []
        
    def install_cursor_extensions(self):
        """Install Cursor IDE extensions"""
        print("🔧 Installing Cursor IDE Extensions...")
        print("=" * 50)
        
        cursor_extensions = [
            # AI/ML Extensions
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-python.isort",
            "ms-python.flake8",
            "ms-python.mypy-type-checker",
            "ms-python.pylint",
            "ms-python.pytest-adapter",
            "ms-python.coverage-gutters",
            
            # JavaScript/TypeScript Extensions
            "ms-vscode.vscode-typescript-next",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "dbaeumer.vscode-eslint",
            "ms-vscode.vscode-json",
            
            # React/Node.js Extensions
            "ms-vscode.vscode-react-native",
            "ms-vscode.vscode-node-debug2",
            "ms-vscode.vscode-js-debug",
            "ms-vscode.vscode-js-debug-companion",
            
            # Git Extensions
            "eamodio.gitlens",
            "mhutchie.git-graph",
            "donjayamanne.githistory",
            
            # Database Extensions
            "ms-mssql.mssql",
            "cweijan.vscode-mysql-client2",
            "ms-vscode.vscode-cosmosdb",
            
            # Docker Extensions
            "ms-azuretools.vscode-docker",
            "ms-kubernetes-tools.vscode-kubernetes-tools",
            
            # Cloud Extensions
            "ms-vscode.vscode-azure-account",
            "ms-vscode.vscode-azurecli",
            "ms-vscode.vscode-azureappservice",
            "ms-vscode.vscode-azurefunctions",
            "ms-vscode.vscode-azurestorage",
            
            # AI/ML Specific Extensions
            "ms-toolsai.jupyter",
            "ms-toolsai.jupyter-keymap",
            "ms-toolsai.jupyter-renderers",
            "ms-toolsai.vscode-jupyter-cell-tags",
            "ms-toolsai.vscode-jupyter-slideshow",
            
            # Healthcare Extensions
            "ms-vscode.vscode-json",
            "redhat.vscode-yaml",
            "ms-vscode.vscode-xml",
            
            # Security Extensions
            "ms-vscode.vscode-json",
            "ms-vscode.vscode-markdownlint",
            "ms-vscode.vscode-sonarqube",
            
            # Testing Extensions
            "ms-vscode.vscode-jest",
            "ms-vscode.vscode-cypress",
            "ms-vscode.vscode-playwright",
            
            # Documentation Extensions
            "ms-vscode.vscode-markdown",
            "ms-vscode.vscode-markdown-math",
            "ms-vscode.vscode-markdown-preview-enhanced",
            
            # Productivity Extensions
            "ms-vscode.vscode-thunder-client",
            "ms-vscode.vscode-rest-client",
            "ms-vscode.vscode-postman",
            
            # Code Quality Extensions
            "ms-vscode.vscode-sonarqube",
            "ms-vscode.vscode-codeclimate",
            "ms-vscode.vscode-codacy",
            
            # Monitoring Extensions
            "ms-vscode.vscode-azuremonitor",
            "ms-vscode.vscode-application-insights",
            "ms-vscode.vscode-log-analytics"
        ]
        
        for extension in cursor_extensions:
            try:
                print(f"Installing {extension}...")
                result = subprocess.run(["code", "--install-extension", extension], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    self.installed_features.append(f"Extension: {extension}")
                    print(f"✅ {extension} installed successfully")
                else:
                    self.failed_features.append(f"Extension: {extension} - {result.stderr}")
                    print(f"❌ {extension} failed: {result.stderr}")
            except Exception as e:
                self.failed_features.append(f"Extension: {extension} - {str(e)}")
                print(f"❌ {extension} error: {str(e)}")
    
    def install_cursor_ai_features(self):
        """Install Cursor AI features"""
        print("\n🤖 Installing Cursor AI Features...")
        print("=" * 50)
        
        ai_features = [
            # AI Code Completion
            "github.copilot",
            "github.copilot-chat",
            "github.copilot-labs",
            
            # AI Code Review
            "ms-vscode.vscode-pull-request-github",
            "ms-vscode.vscode-github",
            
            # AI Documentation
            "ms-vscode.vscode-markdown-all-in-one",
            "ms-vscode.vscode-markdown-preview-enhanced",
            
            # AI Testing
            "ms-vscode.vscode-jest",
            "ms-vscode.vscode-cypress",
            "ms-vscode.vscode-playwright",
            
            # AI Debugging
            "ms-vscode.vscode-js-debug",
            "ms-vscode.vscode-node-debug2",
            "ms-vscode.vscode-chrome-debug",
            
            # AI Refactoring
            "ms-vscode.vscode-refactor",
            "ms-vscode.vscode-extract-method",
            "ms-vscode.vscode-extract-variable",
            
            # AI Code Analysis
            "ms-vscode.vscode-sonarqube",
            "ms-vscode.vscode-codeclimate",
            "ms-vscode.vscode-codacy"
        ]
        
        for feature in ai_features:
            try:
                print(f"Installing {feature}...")
                result = subprocess.run(["code", "--install-extension", feature], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    self.installed_features.append(f"AI Feature: {feature}")
                    print(f"✅ {feature} installed successfully")
                else:
                    self.failed_features.append(f"AI Feature: {feature} - {result.stderr}")
                    print(f"❌ {feature} failed: {result.stderr}")
            except Exception as e:
                self.failed_features.append(f"AI Feature: {feature} - {str(e)}")
                print(f"❌ {feature} error: {str(e)}")
    
    def install_cursor_healthcare_features(self):
        """Install Cursor healthcare-specific features"""
        print("\n🏥 Installing Cursor Healthcare Features...")
        print("=" * 50)
        
        healthcare_features = [
            # FHIR Support
            "hl7.fhir",
            "hl7.fhir-validator",
            "hl7.fhir-tools",
            
            # HL7 Support
            "hl7.hl7-tools",
            "hl7.hl7-validator",
            
            # DICOM Support
            "dicom.dicom-viewer",
            "dicom.dicom-tools",
            
            # Healthcare Standards
            "healthcare.hipaa-compliance",
            "healthcare.hl7-fhir",
            "healthcare.dicom-support",
            
            # Medical Data Validation
            "healthcare.data-validation",
            "healthcare.patient-data",
            "healthcare.clinical-workflow",
            
            # Security & Compliance
            "healthcare.security-audit",
            "healthcare.compliance-checker",
            "healthcare.privacy-protection"
        ]
        
        for feature in healthcare_features:
            try:
                print(f"Installing {feature}...")
                result = subprocess.run(["code", "--install-extension", feature], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    self.installed_features.append(f"Healthcare: {feature}")
                    print(f"✅ {feature} installed successfully")
                else:
                    self.failed_features.append(f"Healthcare: {feature} - {result.stderr}")
                    print(f"❌ {feature} failed: {result.stderr}")
            except Exception as e:
                self.failed_features.append(f"Healthcare: {feature} - {str(e)}")
                print(f"❌ {feature} error: {str(e)}")
    
    def install_cursor_devops_features(self):
        """Install Cursor DevOps features"""
        print("\n🛠️ Installing Cursor DevOps Features...")
        print("=" * 50)
        
        devops_features = [
            # Kubernetes
            "ms-kubernetes-tools.vscode-kubernetes-tools",
            "ms-kubernetes-tools.vscode-kustomize",
            "ms-kubernetes-tools.vscode-helm",
            
            # Docker
            "ms-azuretools.vscode-docker",
            "ms-azuretools.vscode-docker-explorer",
            
            # Terraform
            "hashicorp.terraform",
            "hashicorp.hcl",
            
            # Ansible
            "redhat.ansible",
            "redhat.vscode-yaml",
            
            # CI/CD
            "ms-vscode.vscode-github-actions",
            "ms-vscode.vscode-azure-pipelines",
            "ms-vscode.vscode-jenkins",
            
            # Monitoring
            "ms-vscode.vscode-azuremonitor",
            "ms-vscode.vscode-application-insights",
            "ms-vscode.vscode-log-analytics",
            
            # Security
            "ms-vscode.vscode-sonarqube",
            "ms-vscode.vscode-codeclimate",
            "ms-vscode.vscode-codacy"
        ]
        
        for feature in devops_features:
            try:
                print(f"Installing {feature}...")
                result = subprocess.run(["code", "--install-extension", feature], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    self.installed_features.append(f"DevOps: {feature}")
                    print(f"✅ {feature} installed successfully")
                else:
                    self.failed_features.append(f"DevOps: {feature} - {result.stderr}")
                    print(f"❌ {feature} failed: {result.stderr}")
            except Exception as e:
                self.failed_features.append(f"DevOps: {feature} - {str(e)}")
                print(f"❌ {feature} error: {str(e)}")
    
    def create_cursor_config(self):
        """Create Cursor configuration files"""
        print("\n⚙️ Creating Cursor Configuration...")
        print("=" * 50)
        
        # Create .vscode/settings.json
        cursor_settings = {
            "python.defaultInterpreterPath": "./venv/bin/python",
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.linting.flake8Enabled": True,
            "python.formatting.provider": "black",
            "python.formatting.blackArgs": ["--line-length", "88"],
            "python.sortImports.args": ["--profile", "black"],
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            },
            "typescript.preferences.importModuleSpecifier": "relative",
            "javascript.preferences.importModuleSpecifier": "relative",
            "files.associations": {
                "*.fhir": "json",
                "*.hl7": "plaintext",
                "*.dcm": "binary"
            },
            "emmet.includeLanguages": {
                "javascript": "javascriptreact",
                "typescript": "typescriptreact"
            },
            "git.enableSmartCommit": True,
            "git.confirmSync": False,
            "git.autofetch": True,
            "terminal.integrated.defaultProfile.windows": "PowerShell",
            "workbench.colorTheme": "Default Dark+",
            "workbench.iconTheme": "vs-seti",
            "editor.fontSize": 14,
            "editor.fontFamily": "'Cascadia Code', 'Consolas', 'Courier New', monospace",
            "editor.fontLigatures": True,
            "editor.minimap.enabled": True,
            "editor.wordWrap": "on",
            "editor.rulers": [88, 120],
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            "files.trimTrailingWhitespace": True,
            "files.insertFinalNewline": True,
            "files.trimFinalNewlines": True,
            "search.exclude": {
                "**/node_modules": True,
                "**/bower_components": True,
                "**/*.code-search": True,
                "**/venv": True,
                "**/.venv": True,
                "**/__pycache__": True,
                "**/*.pyc": True
            },
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                "**/node_modules": True,
                "**/.git": True,
                "**/.DS_Store": True,
                "**/Thumbs.db": True
            }
        }
        
        try:
            import os
            os.makedirs(".vscode", exist_ok=True)
            
            with open(".vscode/settings.json", "w") as f:
                json.dump(cursor_settings, f, indent=2)
            
            print("✅ Cursor settings.json created successfully")
            self.installed_features.append("Cursor Settings")
            
        except Exception as e:
            print(f"❌ Failed to create Cursor settings: {str(e)}")
            self.failed_features.append(f"Cursor Settings - {str(e)}")
        
        # Create .vscode/extensions.json
        recommended_extensions = [
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-python.isort",
            "ms-python.flake8",
            "ms-python.mypy-type-checker",
            "ms-vscode.vscode-typescript-next",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "dbaeumer.vscode-eslint",
            "eamodio.gitlens",
            "ms-azuretools.vscode-docker",
            "ms-kubernetes-tools.vscode-kubernetes-tools",
            "ms-toolsai.jupyter",
            "github.copilot",
            "github.copilot-chat"
        ]
        
        extensions_config = {
            "recommendations": recommended_extensions
        }
        
        try:
            with open(".vscode/extensions.json", "w") as f:
                json.dump(extensions_config, f, indent=2)
            
            print("✅ Cursor extensions.json created successfully")
            self.installed_features.append("Cursor Extensions Config")
            
        except Exception as e:
            print(f"❌ Failed to create extensions config: {str(e)}")
            self.failed_features.append(f"Cursor Extensions Config - {str(e)}")
    
    def create_cursor_tasks(self):
        """Create Cursor tasks configuration"""
        print("\n📋 Creating Cursor Tasks...")
        print("=" * 50)
        
        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Run Python Tests",
                    "type": "shell",
                    "command": "python",
                    "args": ["-m", "pytest"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Run JavaScript Tests",
                    "type": "shell",
                    "command": "npm",
                    "args": ["test"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Format Python Code",
                    "type": "shell",
                    "command": "python",
                    "args": ["-m", "black", "."],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Format JavaScript Code",
                    "type": "shell",
                    "command": "npx",
                    "args": ["prettier", "--write", "."],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Lint Python Code",
                    "type": "shell",
                    "command": "python",
                    "args": ["-m", "flake8"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Lint JavaScript Code",
                    "type": "shell",
                    "command": "npx",
                    "args": ["eslint", "."],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Start Development Server",
                    "type": "shell",
                    "command": "python",
                    "args": ["app.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Start Frontend Server",
                    "type": "shell",
                    "command": "npm",
                    "args": ["start"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                }
            ]
        }
        
        try:
            with open(".vscode/tasks.json", "w") as f:
                json.dump(tasks_config, f, indent=2)
            
            print("✅ Cursor tasks.json created successfully")
            self.installed_features.append("Cursor Tasks")
            
        except Exception as e:
            print(f"❌ Failed to create tasks config: {str(e)}")
            self.failed_features.append(f"Cursor Tasks - {str(e)}")
    
    def create_cursor_launch_config(self):
        """Create Cursor launch configuration"""
        print("\n🚀 Creating Cursor Launch Configuration...")
        print("=" * 50)
        
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Current File",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "justMyCode": True
                },
                {
                    "name": "Python: FastAPI",
                    "type": "python",
                    "request": "launch",
                    "module": "uvicorn",
                    "args": ["main:app", "--reload", "--port", "8000"],
                    "console": "integratedTerminal",
                    "justMyCode": True
                },
                {
                    "name": "Python: Streamlit",
                    "type": "python",
                    "request": "launch",
                    "module": "streamlit",
                    "args": ["run", "app.py"],
                    "console": "integratedTerminal",
                    "justMyCode": True
                },
                {
                    "name": "Node.js: Current File",
                    "type": "node",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal"
                },
                {
                    "name": "Node.js: React App",
                    "type": "node",
                    "request": "launch",
                    "program": "${workspaceFolder}/node_modules/.bin/react-scripts",
                    "args": ["start"],
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}"
                }
            ]
        }
        
        try:
            with open(".vscode/launch.json", "w") as f:
                json.dump(launch_config, f, indent=2)
            
            print("✅ Cursor launch.json created successfully")
            self.installed_features.append("Cursor Launch Config")
            
        except Exception as e:
            print(f"❌ Failed to create launch config: {str(e)}")
            self.failed_features.append(f"Cursor Launch Config - {str(e)}")
    
    def generate_cursor_report(self):
        """Generate Cursor installation report"""
        print("\n" + "=" * 80)
        print("🔧 CURSOR FEATURES INSTALLATION REPORT")
        print("=" * 80)
        
        total_installed = len(self.installed_features)
        total_failed = len(self.failed_features)
        total_attempted = total_installed + total_failed
        success_rate = round((total_installed / total_attempted) * 100, 1) if total_attempted > 0 else 0
        
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ Successfully Installed: {total_installed}")
        print(f"❌ Failed Installations: {total_failed}")
        print(f"📊 Success Rate: {success_rate}%")
        
        if self.installed_features:
            print("\n✅ SUCCESSFULLY INSTALLED:")
            for feature in self.installed_features:
                print(f"  ✅ {feature}")
        
        if self.failed_features:
            print("\n❌ FAILED INSTALLATIONS:")
            for feature in self.failed_features:
                print(f"  ❌ {feature}")
        
        print("\n" + "=" * 80)
        print("🎯 CURSOR INTEGRATION SUMMARY:")
        print(f"✅ Installed Features: {total_installed}")
        print(f"❌ Failed Features: {total_failed}")
        print(f"📈 Success Rate: {success_rate}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Most Cursor features are installed!")
        elif success_rate >= 70:
            print("👍 GOOD! Most essential Cursor features are installed!")
        else:
            print("⚠️  NEEDS ATTENTION! Many Cursor features failed to install!")
        
        print("\n🎉 CURSOR AI INTEGRATION COMPLETE!")
        print("🚀 EHB AI Development System with Cursor is ready!")
        print("=" * 80)
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_name": "EHB AI Development System - Cursor Integration",
            "status": "COMPLETED",
            "success_rate": f"{success_rate}%",
            "installed_features": self.installed_features,
            "failed_features": self.failed_features,
            "summary": {
                "total_installed": total_installed,
                "total_failed": total_failed,
                "success_rate": success_rate
            }
        }
        
        with open("cursor_integration_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: cursor_integration_report.json")
    
    def run_complete_installation(self):
        """Run complete Cursor features installation"""
        print("🔧 Starting Cursor Features Installation...")
        print("=" * 60)
        
        # Install Cursor extensions
        self.install_cursor_extensions()
        
        # Install Cursor AI features
        self.install_cursor_ai_features()
        
        # Install Cursor healthcare features
        self.install_cursor_healthcare_features()
        
        # Install Cursor DevOps features
        self.install_cursor_devops_features()
        
        # Create Cursor configuration
        self.create_cursor_config()
        
        # Create Cursor tasks
        self.create_cursor_tasks()
        
        # Create Cursor launch configuration
        self.create_cursor_launch_config()
        
        # Generate report
        self.generate_cursor_report()
        
        print("\n🎉 Cursor Features Installation Complete!")
        print("🚀 EHB AI Development System with Cursor is ready!")

if __name__ == "__main__":
    installer = CursorFeaturesInstaller()
    installer.run_complete_installation() 