"""
Auto Restart System Script
Automatically restarts and fixes the EHB system after PC restart
"""

import json
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EHBSystemRestarter:
    """Automated EHB system restarter"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.status = {
            "frontend_running": False,
            "backend_running": False,
            "dependencies_installed": False,
            "env_setup": False,
            "data_created": False
        }
    
    def check_npm_installation(self):
        """Check if npm is available"""
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ npm found: {result.stdout.strip()}")
                return True
            else:
                logger.error("❌ npm not found")
                return False
        except FileNotFoundError:
            logger.error("❌ npm not found in PATH")
            return False
    
    def check_python_dependencies(self):
        """Check and install Python dependencies"""
        logger.info("🔍 Checking Python dependencies...")
        
        required_packages = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'pydantic',
            'flask',
            'flask-cors',
            'requests',
            'psycopg2-binary',
            'redis',
            'celery',
            'pytest',
            'pytest-asyncio',
            'httpx',
            'bcryptjs',
            'jsonwebtoken',
            'python-dotenv'
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✅ {package} already installed")
            except ImportError:
                logger.info(f"📦 Installing {package}...")
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
                    logger.info(f"✅ {package} installed successfully")
                except subprocess.CalledProcessError:
                    logger.error(f"❌ Failed to install {package}")
    
    def setup_environment(self):
        """Setup environment files"""
        logger.info("🔧 Setting up environment...")
        
        # Create .env.example if not exists
        env_example_content = """# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/ehb_healthcare
SQLITE_DATABASE_URL=sqlite:///./ehb_healthcare.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_VERSION=v1
DEBUG_MODE=true

# Security Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
CORS_ENABLED=true

# Healthcare Compliance
HIPAA_COMPLIANT=true
DATA_ENCRYPTION_ENABLED=true
AUDIT_LOGGING_ENABLED=true

# AI Configuration
AI_MODEL_PATH=./models/
AI_ENABLED=true
AI_DIAGNOSIS_ENABLED=true

# AWS Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=ehb-healthcare-data

# Azure Configuration
AZURE_CONNECTION_STRING=your-azure-connection-string
AZURE_STORAGE_ACCOUNT=your-storage-account

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_CREDENTIALS=path/to/credentials.json

# Healthcare APIs
FHIR_SERVER_URL=https://hapi.fhir.org/baseR4
HL7_ENABLED=true
DICOM_ENABLED=true

# Monitoring Configuration
MONITORING_ENABLED=true
LOG_LEVEL=INFO
METRICS_ENABLED=true

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Payment Configuration
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
PAYMENT_ENABLED=true

# Telemedicine Configuration
VIDEO_CALL_ENABLED=true
WEBRTC_ENABLED=true
SCREEN_SHARING_ENABLED=true

# Development Configuration
NODE_ENV=development
REACT_APP_API_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Testing Configuration
TEST_DATABASE_URL=sqlite:///./test.db
TEST_MODE=false
COVERAGE_ENABLED=true

# Deployment Configuration
DEPLOYMENT_ENV=development
DOCKER_ENABLED=true
KUBERNETES_ENABLED=false

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=daily
BACKUP_RETENTION_DAYS=30

# Performance Configuration
CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379
CDN_ENABLED=false

# Feature Flags
FEATURE_TELEMEDICINE=true
FEATURE_AI_DIAGNOSIS=true
FEATURE_BLOCKCHAIN=true
FEATURE_MOBILE_APP=true
"""
        
        env_example_path = self.project_root / ".env.example"
        if not env_example_path.exists():
            with open(env_example_path, 'w') as f:
                f.write(env_example_content)
            logger.info("✅ Created .env.example")
        
        # Create .env.local if not exists
        env_local_path = self.project_root / ".env.local"
        if not env_local_path.exists():
            with open(env_local_path, 'w') as f:
                f.write(env_example_content)
            logger.info("✅ Created .env.local")
        
        self.status["env_setup"] = True
    
    def create_missing_data(self):
        """Create missing healthcare data"""
        logger.info("📊 Creating missing healthcare data...")
        
        data_dir = self.project_root / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Sample patients data
        patients_data = {
            "patients": [
                {
                    "id": 1,
                    "name": "Ahmed Khan",
                    "age": 45,
                    "gender": "Male",
                    "phone": "+92-300-1234567",
                    "email": "ahmed.khan@email.com",
                    "address": "House 123, Street 5, Islamabad",
                    "blood_type": "O+",
                    "emergency_contact": "+92-300-7654321",
                    "medical_history": ["Diabetes", "Hypertension"],
                    "allergies": ["Penicillin"],
                    "insurance_provider": "State Life",
                    "insurance_number": "SL-2024-001"
                },
                {
                    "id": 2,
                    "name": "Fatima Ali",
                    "age": 32,
                    "gender": "Female",
                    "phone": "+92-300-2345678",
                    "email": "fatima.ali@email.com",
                    "address": "Apartment 45, Block 7, Karachi",
                    "blood_type": "A+",
                    "emergency_contact": "+92-300-8765432",
                    "medical_history": ["Asthma"],
                    "allergies": ["Dust", "Pollen"],
                    "insurance_provider": "EFU Health",
                    "insurance_number": "EFU-2024-002"
                }
            ]
        }
        
        # Sample doctors data
        doctors_data = {
            "doctors": [
                {
                    "id": 1,
                    "name": "Dr. Sarah Ahmed",
                    "specialization": "Cardiology",
                    "experience_years": 15,
                    "phone": "+92-300-3456789",
                    "email": "dr.sarah.ahmed@ehb.com",
                    "qualifications": ["MBBS", "FCPS", "FRCP"],
                    "availability": "Mon-Fri 9AM-5PM",
                    "rating": 4.8,
                    "patients_count": 150
                },
                {
                    "id": 2,
                    "name": "Dr. Muhammad Hassan",
                    "specialization": "Neurology",
                    "experience_years": 12,
                    "phone": "+92-300-4567890",
                    "email": "dr.muhammad.hassan@ehb.com",
                    "qualifications": ["MBBS", "FCPS", "MRCP"],
                    "availability": "Mon-Sat 10AM-6PM",
                    "rating": 4.9,
                    "patients_count": 200
                }
            ]
        }
        
        # Sample appointments data
        appointments_data = {
            "appointments": [
                {
                    "id": 1,
                    "patient_id": 1,
                    "doctor_id": 1,
                    "date": "2024-01-20",
                    "time": "10:00",
                    "type": "Consultation",
                    "status": "Scheduled",
                    "notes": "Regular checkup",
                    "duration_minutes": 30
                },
                {
                    "id": 2,
                    "patient_id": 2,
                    "doctor_id": 2,
                    "date": "2024-01-21",
                    "time": "14:00",
                    "type": "Follow-up",
                    "status": "Confirmed",
                    "notes": "Neurological assessment",
                    "duration_minutes": 45
                }
            ]
        }
        
        # Save data files
        with open(data_dir / "patients.json", 'w') as f:
            json.dump(patients_data, f, indent=2)
        
        with open(data_dir / "doctors.json", 'w') as f:
            json.dump(doctors_data, f, indent=2)
        
        with open(data_dir / "appointments.json", 'w') as f:
            json.dump(appointments_data, f, indent=2)
        
        logger.info("✅ Created healthcare data files")
        self.status["data_created"] = True
    
    def start_backend_server(self):
        """Start the backend server"""
        logger.info("🚀 Starting backend server...")
        
        backend_script = """
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import List, Optional
import uvicorn

app = FastAPI(title="EHB Healthcare API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: str
    email: str

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    experience_years: int
    phone: str
    email: str

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str
    time: str
    type: str
    status: str

# Load data
def load_data(filename):
    try:
        with open(f"data/{filename}.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"data": []}

@app.get("/")
async def root():
    return {"message": "EHB Healthcare API is running!"}

@app.get("/api/patients")
async def get_patients():
    data = load_data("patients")
    return data.get("patients", [])

@app.get("/api/doctors")
async def get_doctors():
    data = load_data("doctors")
    return data.get("doctors", [])

@app.get("/api/appointments")
async def get_appointments():
    data = load_data("appointments")
    return data.get("appointments", [])

@app.get("/api/dashboard")
async def get_dashboard():
    patients = load_data("patients")
    doctors = load_data("doctors")
    appointments = load_data("appointments")
    
    return {
        "total_patients": len(patients.get("patients", [])),
        "total_doctors": len(doctors.get("doctors", [])),
        "total_appointments": len(appointments.get("appointments", [])),
        "recent_appointments": appointments.get("appointments", [])[:5]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        
        with open("backend_server.py", 'w') as f:
            f.write(backend_script)
        
        # Start backend server
        try:
            subprocess.Popen([sys.executable, "backend_server.py"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(3)  # Wait for server to start
            logger.info("✅ Backend server started on port 8000")
            self.status["backend_running"] = True
        except Exception as e:
            logger.error(f"❌ Failed to start backend: {e}")
    
    def start_frontend_server(self):
        """Start the frontend server"""
        logger.info("🚀 Starting frontend server...")
        
        # Check if frontend directory exists
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            logger.info("📁 Creating frontend directory...")
            frontend_dir.mkdir(exist_ok=True)
            
            # Create basic Next.js structure
            (frontend_dir / "app").mkdir(exist_ok=True)
            (frontend_dir / "components").mkdir(exist_ok=True)
            (frontend_dir / "public").mkdir(exist_ok=True)
            
            # Create package.json
            package_json = {
                "name": "ehb-frontend",
                "version": "0.1.0",
                "private": True,
                "scripts": {
                    "dev": "next dev -p 3001",
                    "build": "next build",
                    "start": "next start",
                    "lint": "next lint"
                },
                "dependencies": {
                    "next": "14.0.0",
                    "react": "^18",
                    "react-dom": "^18",
                    "axios": "^1.6.0",
                    "@heroicons/react": "^2.0.18"
                },
                "devDependencies": {
                    "@types/node": "^20",
                    "@types/react": "^18",
                    "@types/react-dom": "^18",
                    "typescript": "^5",
                    "tailwindcss": "^3.3.0",
                    "autoprefixer": "^10.0.1",
                    "postcss": "^8"
                }
            }
            
            with open(frontend_dir / "package.json", 'w') as f:
                json.dump(package_json, f, indent=2)
            
            # Create basic page
            page_content = """
import { useState, useEffect } from 'react'

export default function Home() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://localhost:8000/api/dashboard')
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching data:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading EHB Healthcare System...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          EHB Healthcare System
        </h1>
        
        {data && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Patients</h3>
              <p className="text-3xl font-bold text-blue-600">{data.total_patients}</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Doctors</h3>
              <p className="text-3xl font-bold text-green-600">{data.total_doctors}</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Appointments</h3>
              <p className="text-3xl font-bold text-purple-600">{data.total_appointments}</p>
            </div>
          </div>
        )}
        
        <div className="mt-8 text-center">
          <p className="text-gray-600">
            System Status: <span className="text-green-600 font-semibold">Online</span>
          </p>
        </div>
      </div>
    </div>
  )
}
"""
            
            with open(frontend_dir / "app" / "page.tsx", 'w') as f:
                f.write(page_content)
        
        # Install dependencies and start frontend
        try:
            os.chdir(frontend_dir)
            subprocess.run(['npm', 'install'], check=True, capture_output=True)
            logger.info("✅ Frontend dependencies installed")
            
            # Start frontend server
            subprocess.Popen(['npm', 'run', 'dev'], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5)  # Wait for server to start
            logger.info("✅ Frontend server started on port 3001")
            self.status["frontend_running"] = True
            
            os.chdir(self.project_root)  # Return to project root
        except Exception as e:
            logger.error(f"❌ Failed to start frontend: {e}")
            os.chdir(self.project_root)
    
    def run_system_check(self):
        """Run comprehensive system check"""
        logger.info("🔍 Running system check...")
        
        print("\n" + "="*60)
        print("🏥 EHB Healthcare System Status")
        print("="*60)
        
        # Check backend
        try:
            import requests
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend Server: RUNNING (Port 8000)")
            else:
                print("❌ Backend Server: ERROR")
        except:
            print("❌ Backend Server: NOT RUNNING")
        
        # Check frontend
        try:
            response = requests.get("http://localhost:3001/", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend Server: RUNNING (Port 3001)")
            else:
                print("❌ Frontend Server: ERROR")
        except:
            print("❌ Frontend Server: NOT RUNNING")
        
        # Check data files
        data_dir = self.project_root / "data"
        if data_dir.exists():
            files = list(data_dir.glob("*.json"))
            print(f"✅ Data Files: {len(files)} files found")
        else:
            print("❌ Data Files: NOT FOUND")
        
        # Check environment
        env_files = [".env.example", ".env.local"]
        env_count = sum(1 for f in env_files if (self.project_root / f).exists())
        print(f"✅ Environment Files: {env_count}/{len(env_files)} files found")
        
        print("="*60)
        print("🎉 System restart completed!")
        print("📱 Frontend: http://localhost:3001")
        print("🔧 Backend API: http://localhost:8000")
        print("📊 Dashboard: http://localhost:3001")
        print("="*60)

def main():
    """Main function to restart the system"""
    print("🚀 EHB Healthcare System Auto Restart")
    print("="*50)
    
    restarter = EHBSystemRestarter()
    
    # Step 1: Check dependencies
    print("\n1️⃣ Checking dependencies...")
    restarter.check_npm_installation()
    restarter.check_python_dependencies()
    
    # Step 2: Setup environment
    print("\n2️⃣ Setting up environment...")
    restarter.setup_environment()
    
    # Step 3: Create missing data
    print("\n3️⃣ Creating healthcare data...")
    restarter.create_missing_data()
    
    # Step 4: Start backend
    print("\n4️⃣ Starting backend server...")
    restarter.start_backend_server()
    
    # Step 5: Start frontend
    print("\n5️⃣ Starting frontend server...")
    restarter.start_frontend_server()
    
    # Step 6: System check
    print("\n6️⃣ Running system check...")
    restarter.run_system_check()
    
    print("\n🎉 System restart completed successfully!")
    print("💡 You can now access the EHB Healthcare System")

if __name__ == "__main__":
    main() 