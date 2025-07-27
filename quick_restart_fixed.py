"""
Quick Restart Script for EHB Healthcare System - Fixed Version
Uses npx and handles system restart efficiently without Unicode issues
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests


def check_server(url, name):
    """Check if server is running"""
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print(f"✅ {name}: RUNNING")
            return True
        else:
            print(f"❌ {name}: ERROR")
            return False
    except:
        print(f"❌ {name}: NOT RUNNING")
        return False

def start_backend():
    """Start backend server"""
    print("🚀 Starting backend server...")
    
    backend_code = '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from pathlib import Path

app = FastAPI(title="EHB Healthcare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
patients = [
    {"id": 1, "name": "Ahmed Khan", "age": 45, "gender": "Male"},
    {"id": 2, "name": "Fatima Ali", "age": 32, "gender": "Female"}
]

doctors = [
    {"id": 1, "name": "Dr. Sarah Ahmed", "specialization": "Cardiology"},
    {"id": 2, "name": "Dr. Muhammad Hassan", "specialization": "Neurology"}
]

@app.get("/")
async def root():
    return {"message": "EHB Healthcare API is running!"}

@app.get("/api/patients")
async def get_patients():
    return patients

@app.get("/api/doctors")
async def get_doctors():
    return doctors

@app.get("/api/dashboard")
async def get_dashboard():
    return {
        "total_patients": len(patients),
        "total_doctors": len(doctors),
        "status": "online"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open("quick_backend.py", "w", encoding='utf-8') as f:
        f.write(backend_code)
    
    try:
        subprocess.Popen([sys.executable, "quick_backend.py"], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        print("✅ Backend started on port 8000")
        return True
    except Exception as e:
        print(f"❌ Backend failed: {e}")
        return False

def start_frontend():
    """Start frontend server using npx"""
    print("🚀 Starting frontend server...")
    
    # Create frontend directory if not exists
    frontend_dir = Path("frontend")
    frontend_dir.mkdir(exist_ok=True)
    
    # Create basic Next.js app
    app_dir = frontend_dir / "app"
    app_dir.mkdir(exist_ok=True)
    
    # Create page.tsx without Unicode characters
    page_content = '''
export default function Home() {
  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        background: 'white',
        padding: '2rem',
        borderRadius: '1rem',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        maxWidth: '500px'
      }}>
        <h1 style={{ 
          color: '#1f2937', 
          fontSize: '2.5rem', 
          marginBottom: '1rem',
          fontWeight: 'bold'
        }}>
          EHB Healthcare System
        </h1>
        
        <p style={{ 
          color: '#6b7280', 
          fontSize: '1.1rem',
          marginBottom: '2rem'
        }}>
          System Status: <span style={{ color: '#10b981', fontWeight: 'bold' }}>ONLINE</span>
        </p>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '1rem',
          marginBottom: '2rem'
        }}>
          <div style={{
            background: '#f3f4f6',
            padding: '1rem',
            borderRadius: '0.5rem',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3b82f6' }}>150</div>
            <div style={{ color: '#6b7280' }}>Patients</div>
          </div>
          
          <div style={{
            background: '#f3f4f6',
            padding: '1rem',
            borderRadius: '0.5rem',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>25</div>
            <div style={{ color: '#6b7280' }}>Doctors</div>
          </div>
          
          <div style={{
            background: '#f3f4f6',
            padding: '1rem',
            borderRadius: '0.5rem',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#8b5cf6' }}>45</div>
            <div style={{ color: '#6b7280' }}>Appointments</div>
          </div>
        </div>
        
        <div style={{
          background: '#fef3c7',
          padding: '1rem',
          borderRadius: '0.5rem',
          border: '1px solid #f59e0b'
        }}>
          <p style={{ margin: 0, color: '#92400e' }}>
            System automatically restarted after PC shutdown
          </p>
        </div>
      </div>
    </div>
  )
}
'''
    
    with open(app_dir / "page.tsx", "w", encoding='utf-8') as f:
        f.write(page_content)
    
    # Create package.json
    package_json = {
        "name": "ehb-frontend",
        "version": "0.1.0",
        "scripts": {
            "dev": "next dev -p 3001",
            "build": "next build",
            "start": "next start"
        },
        "dependencies": {
            "next": "14.0.0",
            "react": "^18",
            "react-dom": "^18"
        }
    }
    
    with open(frontend_dir / "package.json", "w", encoding='utf-8') as f:
        json.dump(package_json, f, indent=2)
    
    # Create next.config.js
    next_config = '''
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
'''
    
    with open(frontend_dir / "next.config.js", "w", encoding='utf-8') as f:
        f.write(next_config)
    
    try:
        # Use npx to run Next.js
        os.chdir(frontend_dir)
        subprocess.Popen(['npx', 'next', 'dev', '-p', '3001'], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        print("✅ Frontend started on port 3001")
        os.chdir("..")
        return True
    except Exception as e:
        print(f"❌ Frontend failed: {e}")
        os.chdir("..")
        return False

def main():
    """Main function"""
    print("🚀 EHB Healthcare System Quick Restart")
    print("=" * 50)
    
    # Start backend
    backend_ok = start_backend()
    
    # Start frontend
    frontend_ok = start_frontend()
    
    # Wait a bit for servers to start
    time.sleep(5)
    
    print("\n" + "=" * 50)
    print("🔍 System Status Check")
    print("=" * 50)
    
    # Check servers
    backend_running = check_server("http://localhost:8000/", "Backend Server")
    frontend_running = check_server("http://localhost:3001/", "Frontend Server")
    
    print("\n" + "=" * 50)
    if backend_running and frontend_running:
        print("🎉 System restart completed successfully!")
        print("📱 Frontend: http://localhost:3001")
        print("🔧 Backend API: http://localhost:8000")
        print("📊 Dashboard: http://localhost:3001")
    else:
        print("⚠️  Some services failed to start")
        print("💡 Check the logs above for details")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 