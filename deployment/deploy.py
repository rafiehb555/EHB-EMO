#!/usr/bin/env python3
import subprocess
import sys
import os

def deploy():
    print("EHB AI Dev Agent - Deploying...")
    
    # Install dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run security scan
    subprocess.run([sys.executable, "auto_bug_fixer_complete.py"])
    
    # Start server
    subprocess.run([sys.executable, "api_server.py", "--port", "8000"])
    
    print("Deployment complete!")

if __name__ == "__main__":
    deploy()
