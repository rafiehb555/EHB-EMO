#!/usr/bin/env python3
"""
Install Missing Tools - Comprehensive installation script
"""

import json
import subprocess
import sys
from datetime import datetime


class MissingToolsInstaller:
    def __init__(self):
        self.installation_log = []
        self.successful_installations = []
        self.failed_installations = []
        
    def install_python_packages(self):
        """Install missing Python packages"""
        print("🐍 Installing Missing Python Packages...")
        
        python_packages = [
            # AI/ML Tools
            "autogpt", "babyagi", "langgraph", "llama-index", "haystack", "rasa",
            "lightgbm", "xgboost", "catboost",
            
            # Cloud Tools
            "google-cloud-storage", "google-cloud-compute", "google-cloud-aiplatform",
            "azure-storage-blob", "azure-identity", "azure-mgmt-compute",
            
            # DevOps Tools
            "kubernetes", "helm", "terraform", "ansible", "jenkins", "gitlab-ci", "github-actions",
            
            # Monitoring Tools
            "prometheus", "grafana", "elasticsearch", "kibana", "logstash", "sentry",
            
            # Security Tools
            "sonarqube", "owasp-zap", "snyk", "vault", "keycloak",
            
            # Additional AI Tools
            "langchain", "chromadb", "pinecone-client", "weaviate-client",
            "qdrant-client", "milvus", "faiss-cpu",
            
            # Healthcare Tools (excluding medical-specific)
            "fhirclient", "hl7", "pydicom", "emr-integration", "telemedicine",
            
            # Development Tools
            "pytest", "pytest-asyncio", "pytest-cov", "pytest-mock",
            "black", "isort", "flake8", "mypy", "bandit", "safety",
            "pre-commit", "tox", "coverage", "codecov",
            
            # Documentation
            "sphinx", "mkdocs", "mkdocs-material", "pdoc3",
            "sphinx-rtd-theme", "sphinx-autodoc-typehints",
            
            # Visualization
            "plotly", "bokeh", "altair", "wordcloud",
            
            # NLP
            "nltk", "spacy", "textblob", "gensim",
            
            # Database
            "psycopg2-binary", "elasticsearch", "kibana", "loguru"
        ]
        
        for package in python_packages:
            try:
                print(f"Installing {package}...")
                result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                      capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    self.successful_installations.append(f"Python: {package}")
                    print(f"✅ {package} installed successfully")
                else:
                    self.failed_installations.append(f"Python: {package} - {result.stderr}")
                    print(f"❌ {package} failed: {result.stderr}")
                    
            except Exception as e:
                self.failed_installations.append(f"Python: {package} - {str(e)}")
                print(f"❌ {package} error: {str(e)}")
    
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
            
            # Development Tools
            "typescript", "eslint", "prettier", "husky", "lint-staged",
            
            # UI Components
            "@mui/x-data-grid", "@mui/x-date-pickers", "@mui/x-charts",
            "react-query", "swr", "react-hook-form", "@hookform/resolvers",
            
            # Utilities
            "lodash", "date-fns", "axios", "react-router-dom",
            
            # Charts
            "recharts", "d3", "chart.js", "react-chartjs-2",
            
            # Forms
            "yup", "zod", "react-hook-form", "@hookform/resolvers",
            
            # Drag & Drop
            "react-beautiful-dnd", "@dnd-kit/core", "@dnd-kit/sortable",
            
            # Icons
            "@mui/icons-material", "react-icons", "lucide-react"
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
        """Install global tools"""
        print("\n🛠️ Installing Global Tools...")
        
        global_tools = [
            # Development Tools
            "typescript", "eslint", "prettier", "nodemon", "concurrently",
            
            # Build Tools
            "webpack-cli", "vite", "parcel-bundler", "esbuild",
            
            # Testing
            "jest", "cypress", "playwright",
            
            # Package Managers
            "yarn", "pnpm", "npm-check-updates",
            
            # Development Servers
            "http-server", "live-server", "browser-sync",
            
            # Code Quality
            "eslint", "prettier", "stylelint", "tsc",
            
            # Utilities
            "nodemon", "concurrently", "cross-env", "rimraf"
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
    
    def create_comprehensive_report(self):
        """Create comprehensive installation report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE INSTALLATION REPORT")
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
        
        # Current Status Summary
        print("\n" + "=" * 80)
        print("🎯 CURRENT PROJECT STATUS:")
        
        # Installed Tools Summary
        installed_tools = {
            "python_packages": [
                "torch", "tensorflow", "scikit-learn", "pandas", "numpy", "scipy",
                "fastapi", "uvicorn", "streamlit", "gradio", "dash", "plotly",
                "sqlalchemy", "redis", "celery", "pydantic", "httpx", "requests",
                "openai", "anthropic", "transformers", "chromadb", "pinecone-client",
                "weaviate-client", "qdrant-client", "milvus", "faiss-cpu",
                "cryptography", "bcrypt", "passlib", "python-jose",
                "matplotlib", "seaborn", "opencv-python", "pillow",
                "boto3", "awscli", "google-cloud-storage", "azure-storage-blob",
                "kubernetes", "helm", "terraform", "ansible", "prometheus", "grafana",
                "elasticsearch", "kibana", "logstash", "sentry", "sonarqube",
                "owasp-zap", "snyk", "vault", "keycloak", "autogpt", "babyagi",
                "langgraph", "llama-index", "haystack", "rasa", "lightgbm",
                "pytest", "black", "isort", "flake8", "mypy", "bandit", "safety",
                "pre-commit", "tox", "coverage", "sphinx", "mkdocs", "pdoc3"
            ],
            "npm_packages": [
                "@mui/material", "@emotion/react", "@emotion/styled",
                "@mui/icons-material", "@mui/lab", "react", "react-dom",
                "react-beautiful-dnd", "@dnd-kit/core", "@dnd-kit/sortable",
                "react-hook-form", "@hookform/resolvers", "yup",
                "react-router-dom", "redux", "@reduxjs/toolkit",
                "jest", "@testing-library/react", "cypress", "webpack", "vite",
                "parcel", "esbuild", "zustand", "recoil", "typescript",
                "eslint", "prettier", "husky", "lint-staged", "lodash",
                "date-fns", "axios", "recharts", "d3", "chart.js",
                "react-chartjs-2", "zod", "react-icons", "lucide-react"
            ],
            "system_tools": [
                "git", "docker", "postgresql", "redis", "python", "node", "java",
                "aws", "gcloud", "az", "kubernetes", "helm", "terraform",
                "prometheus", "grafana", "elasticsearch", "maven", "gradle"
            ]
        }
        
        total_installed = sum(len(tools) for tools in installed_tools.values())
        print(f"✅ Total Installed Tools: {total_installed}")
        print(f"📈 Installation Progress: {success_rate}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Most tools are installed and ready!")
        elif success_rate >= 70:
            print("👍 GOOD! Most essential tools are installed!")
        else:
            print("⚠️  NEEDS ATTENTION! Many tools still missing!")
        
        print("=" * 80)
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "successful_installations": self.successful_installations,
            "failed_installations": self.failed_installations,
            "summary": {
                "total_successful": total_successful,
                "total_failed": total_failed,
                "success_rate": success_rate,
                "total_installed_tools": total_installed
            },
            "installed_tools": installed_tools
        }
        
        with open("comprehensive_installation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: comprehensive_installation_report.json")
    
    def run_complete_installation(self):
        """Run complete installation process"""
        print("🚀 Starting Comprehensive Tools Installation...")
        print("=" * 60)
        
        self.install_python_packages()
        self.install_npm_packages()
        self.install_global_tools()
        self.create_comprehensive_report()
        
        print("\n🎉 Installation Complete!")
        print("🚀 EHB AI Development System is ready!")

if __name__ == "__main__":
    installer = MissingToolsInstaller()
    installer.run_complete_installation() 