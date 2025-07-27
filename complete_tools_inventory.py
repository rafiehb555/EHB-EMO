#!/usr/bin/env python3
"""
Complete Tools Inventory
Comprehensive list of all installed tools, SDKs, and missing packages
"""

import json
import subprocess
import sys
from datetime import datetime


class ToolsInventory:
    def __init__(self):
        self.installed_tools = {}
        self.missing_tools = {}
        self.sdks = {}
        self.running_services = {}
        
    def check_python_packages(self):
        """Check all Python packages"""
        print("🐍 Checking Python Packages...")
        
        python_packages = {
            "ai_ml": [
                "torch", "tensorflow", "scikit-learn", "pandas", "numpy", 
                "scipy", "xgboost", "catboost", "lightgbm", "transformers",
                "openai", "anthropic", "huggingface_hub"
            ],
            "nlp_voice": [
                "SpeechRecognition", "pyttsx3", "librosa", "nltk", "spacy",
                "textblob", "rasa", "whisper", "pyttsx3"
            ],
            "web_frameworks": [
                "fastapi", "uvicorn", "flask", "django", "streamlit",
                "gradio", "dash", "plotly", "bokeh"
            ],
            "databases": [
                "sqlalchemy", "psycopg2-binary", "redis", "celery",
                "pymongo", "sqlite3", "mysql-connector"
            ],
            "cloud_aws": [
                "boto3", "awscli", "botocore", "s3fs"
            ],
            "cloud_google": [
                "google-cloud-storage", "google-cloud-compute",
                "google-cloud-aiplatform"
            ],
            "cloud_azure": [
                "azure-storage-blob", "azure-identity", "azure-mgmt-compute"
            ],
            "devops": [
                "docker", "kubernetes", "helm", "terraform", "ansible",
                "jenkins", "gitlab-ci", "github-actions"
            ],
            "monitoring": [
                "prometheus", "grafana", "elasticsearch", "kibana",
                "logstash", "sentry"
            ],
            "security": [
                "cryptography", "bcrypt", "passlib", "python-jose",
                "python-multipart", "certifi"
            ]
        }
        
        for category, packages in python_packages.items():
            self.installed_tools[category] = {"installed": [], "missing": []}
            
            for package in packages:
                try:
                    if package == "SpeechRecognition":
                        import speech_recognition
                    elif package == "psycopg2-binary":
                        import psycopg2
                    elif package == "sqlite3":
                        import sqlite3
                    else:
                        __import__(package.replace('-', '_'))
                    
                    self.installed_tools[category]["installed"].append(package)
                except ImportError:
                    self.installed_tools[category]["missing"].append(package)
    
    def check_node_packages(self):
        """Check Node.js packages"""
        print("📦 Checking Node.js Packages...")
        
        npm_packages = {
            "ui_frameworks": [
                "@mui/material", "@emotion/react", "@emotion/styled",
                "@mui/icons-material", "@mui/lab", "react", "react-dom"
            ],
            "drag_drop": [
                "react-beautiful-dnd", "@dnd-kit/core", "@dnd-kit/sortable"
            ],
            "forms": [
                "react-hook-form", "@hookform/resolvers", "yup"
            ],
            "routing": [
                "react-router-dom", "next", "gatsby"
            ],
            "state_management": [
                "redux", "@reduxjs/toolkit", "zustand", "recoil"
            ],
            "testing": [
                "jest", "@testing-library/react", "cypress"
            ],
            "build_tools": [
                "webpack", "vite", "parcel", "esbuild"
            ]
        }
        
        for category, packages in npm_packages.items():
            self.installed_tools[f"npm_{category}"] = {"installed": [], "missing": []}
            
            for package in packages:
                try:
                    result = subprocess.run(["npm", "list", package], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.installed_tools[f"npm_{category}"]["installed"].append(package)
                    else:
                        self.installed_tools[f"npm_{category}"]["missing"].append(package)
                except:
                    self.installed_tools[f"npm_{category}"]["missing"].append(package)
    
    def check_system_tools(self):
        """Check system tools and SDKs"""
        print("🛠️ Checking System Tools...")
        
        system_tools = {
            "version_control": ["git", "svn"],
            "containers": ["docker", "kubernetes", "helm"],
            "cloud_cli": ["aws", "gcloud", "az"],
            "databases": ["postgresql", "mysql", "mongodb", "redis"],
            "monitoring": ["prometheus", "grafana", "elasticsearch"],
            "build_tools": ["maven", "gradle", "ant"],
            "languages": ["python", "node", "java", "go", "rust"]
        }
        
        for category, tools in system_tools.items():
            self.sdks[category] = {"installed": [], "missing": []}
            
            for tool in tools:
                try:
                    result = subprocess.run([tool, "--version"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.sdks[category]["installed"].append(tool)
                    else:
                        self.sdks[category]["missing"].append(tool)
                except FileNotFoundError:
                    self.sdks[category]["missing"].append(tool)
    
    def check_running_services(self):
        """Check running services"""
        print("🔄 Checking Running Services...")
        
        services = [
            "redis-server", "postgres", "mysql", "mongod",
            "docker", "kubernetes", "elasticsearch"
        ]
        
        for service in services:
            try:
                result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {service}.exe"], 
                                      capture_output=True, text=True)
                if service in result.stdout:
                    self.running_services[service] = "✅ Running"
                else:
                    self.running_services[service] = "❌ Not Running"
            except:
                self.running_services[service] = "❓ Unknown"
    
    def generate_comprehensive_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE TOOLS INVENTORY REPORT")
        print("=" * 80)
        
        # Python Packages Summary
        print("\n🐍 PYTHON PACKAGES:")
        total_python_installed = 0
        total_python_missing = 0
        
        for category, status in self.installed_tools.items():
            if not category.startswith("npm_"):
                installed_count = len(status["installed"])
                missing_count = len(status["missing"])
                total_python_installed += installed_count
                total_python_missing += missing_count
                
                print(f"\n🔹 {category.upper().replace('_', ' ')}:")
                print(f"  ✅ Installed ({installed_count}): {', '.join(status['installed'])}")
                if status["missing"]:
                    print(f"  ❌ Missing ({missing_count}): {', '.join(status['missing'])}")
        
        # NPM Packages Summary
        print("\n📦 NPM PACKAGES:")
        total_npm_installed = 0
        total_npm_missing = 0
        
        for category, status in self.installed_tools.items():
            if category.startswith("npm_"):
                installed_count = len(status["installed"])
                missing_count = len(status["missing"])
                total_npm_installed += installed_count
                total_npm_missing += missing_count
                
                print(f"\n🔹 {category.upper().replace('_', ' ')}:")
                print(f"  ✅ Installed ({installed_count}): {', '.join(status['installed'])}")
                if status["missing"]:
                    print(f"  ❌ Missing ({missing_count}): {', '.join(status['missing'])}")
        
        # System Tools Summary
        print("\n🛠️ SYSTEM TOOLS & SDKs:")
        total_sdk_installed = 0
        total_sdk_missing = 0
        
        for category, status in self.sdks.items():
            installed_count = len(status["installed"])
            missing_count = len(status["missing"])
            total_sdk_installed += installed_count
            total_sdk_missing += missing_count
            
            print(f"\n🔹 {category.upper().replace('_', ' ')}:")
            print(f"  ✅ Installed ({installed_count}): {', '.join(status['installed'])}")
            if status["missing"]:
                print(f"  ❌ Missing ({missing_count}): {', '.join(status['missing'])}")
        
        # Running Services
        print("\n🔄 RUNNING SERVICES:")
        for service, status in self.running_services.items():
            print(f"  {status} {service}")
        
        # Final Summary
        print("\n" + "=" * 80)
        print("📊 FINAL SUMMARY:")
        print(f"🐍 Python Packages: {total_python_installed} installed, {total_python_missing} missing")
        print(f"📦 NPM Packages: {total_npm_installed} installed, {total_npm_missing} missing")
        print(f"🛠️ System Tools: {total_sdk_installed} installed, {total_sdk_missing} missing")
        print(f"🔄 Running Services: {len([s for s in self.running_services.values() if 'Running' in s])} active")
        
        total_installed = total_python_installed + total_npm_installed + total_sdk_installed
        total_missing = total_python_missing + total_npm_missing + total_sdk_missing
        progress = round((total_installed / (total_installed + total_missing)) * 100, 1)
        
        print(f"\n🎯 OVERALL PROGRESS: {progress}% ({total_installed} installed, {total_missing} missing)")
        print("=" * 80)
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "python_packages": self.installed_tools,
            "system_tools": self.sdks,
            "running_services": self.running_services,
            "summary": {
                "python_installed": total_python_installed,
                "python_missing": total_python_missing,
                "npm_installed": total_npm_installed,
                "npm_missing": total_npm_missing,
                "sdk_installed": total_sdk_installed,
                "sdk_missing": total_sdk_missing,
                "total_installed": total_installed,
                "total_missing": total_missing,
                "progress_percentage": progress
            }
        }
        
        with open("complete_tools_inventory.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: complete_tools_inventory.json")
    
    def run_complete_inventory(self):
        """Run complete inventory check"""
        print("🔍 Starting Complete Tools Inventory...")
        
        self.check_python_packages()
        self.check_node_packages()
        self.check_system_tools()
        self.check_running_services()
        
        self.generate_comprehensive_report()

if __name__ == "__main__":
    inventory = ToolsInventory()
    inventory.run_complete_inventory() 