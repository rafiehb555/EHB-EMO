#!/usr/bin/env python3
"""
EHB Python Project Checker - Comprehensive Python project analysis and fixing
"""

import ast
import importlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class EHBPythonProjectChecker:
    def __init__(self):
        self.project_root = Path.cwd()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "missing_dependencies": [],
            "python_errors": [],
            "missing_files": [],
            "missing_data": [],
            "tools_to_install": [],
            "fixed_issues": [],
            "test_results": [],
            "summary": {}
        }
    
    def check_python_installation(self):
        """Check Python installation and version"""
        print("🐍 Checking Python Installation...")
        
        try:
            version = sys.version_info
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} installed")
            
            if version.major < 3 or (version.major == 3 and version.minor < 8):
                print("⚠️ Python version should be 3.8 or higher")
                self.results["tools_to_install"].append("Python 3.8+")
            else:
                print("✅ Python version is compatible")
                
        except Exception as e:
            print(f"❌ Python check failed: {e}")
            self.results["python_errors"].append(f"Python installation error: {e}")
    
    def check_missing_dependencies(self):
        """Check for missing Python dependencies"""
        print("📦 Checking Missing Dependencies...")
        
        required_packages = [
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
            "pre-commit",
            "psutil",
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "jupyter",
            "ipython"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                importlib.import_module(package)
                print(f"✅ {package}: Installed")
            except ImportError:
                print(f"❌ {package}: Missing")
                missing_packages.append(package)
                self.results["missing_dependencies"].append(package)
        
        # Install missing packages
        if missing_packages:
            print(f"\n📦 Installing {len(missing_packages)} missing packages...")
            for package in missing_packages:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                 check=True, capture_output=True)
                    print(f"✅ {package}: Installed successfully")
                    self.results["fixed_issues"].append(f"Installed missing package: {package}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ {package}: Failed to install")
                    self.results["python_errors"].append(f"Failed to install {package}: {e}")
        
        return len(missing_packages) == 0
    
    def check_missing_files(self):
        """Check for missing essential files"""
        print("📁 Checking Missing Files...")
        
        essential_files = [
            "requirements.txt",
            "README.md",
            "main.py",
            "config.py",
            "utils.py",
            "models.py",
            "api.py",
            "database.py",
            "test_main.py"
        ]
        
        for file_name in essential_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                print(f"❌ {file_name}: Missing")
                self.results["missing_files"].append(file_name)
                self.create_missing_file(file_name)
            else:
                print(f"✅ {file_name}: Exists")
    
    def create_missing_file(self, file_name):
        """Create missing file with appropriate content"""
        print(f"📝 Creating {file_name}...")
        
        if file_name == "requirements.txt":
            content = """fastapi==0.100.0
uvicorn==0.23.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
redis==4.6.0
requests==2.31.0
pytest==7.4.0
black==23.0.0
flake8==6.0.0
mypy==1.5.0
pre-commit==3.3.0
psutil==5.9.0
numpy==1.24.0
pandas==2.0.0
matplotlib==3.7.0
seaborn==0.12.0
scikit-learn==1.3.0
jupyter==1.0.0
ipython==8.14.0"""
        
        elif file_name == "README.md":
            content = """# EHB Healthcare System

## Overview
EHB Healthcare Management System with Python backend and modern web interface.

## Features
- Patient Management
- Doctor Management  
- Appointment Scheduling
- Analytics Dashboard
- API Endpoints

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Testing
```bash
pytest
```"""
        
        elif file_name == "main.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - Main Application
\"\"\"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import router
from database import init_db

app = FastAPI(title="EHB Healthcare System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "🏥 EHB Healthcare System is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EHB Healthcare System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)"""
        
        elif file_name == "config.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - Configuration
\"\"\"

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ehb.db")

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "ehb.log"

# Healthcare specific
HIPAA_COMPLIANT = True
DATA_ENCRYPTION = True
AUDIT_LOGGING = True"""
        
        elif file_name == "utils.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - Utilities
\"\"\"

import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional

def generate_secure_id(length: int = 8) -> str:
    \"\"\"Generate secure random ID\"\"\"
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password: str) -> str:
    \"\"\"Hash password securely\"\"\"
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    \"\"\"Validate email format\"\"\"
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_datetime(dt: datetime) -> str:
    \"\"\"Format datetime for display\"\"\"
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_age(birth_date: datetime) -> int:
    \"\"\"Calculate age from birth date\"\"\"
    today = datetime.now()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age"""
        
        elif file_name == "models.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - Data Models
\"\"\"

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(DateTime)
    address = Column(Text)
    emergency_contact = Column(String)
    medical_history = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    specialization = Column(String)
    license_number = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(String, unique=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("Patient")
    doctor = relationship("Doctor")"""
        
        elif file_name == "api.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - API Routes
\"\"\"

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Patient, Doctor, Appointment
from utils import generate_secure_id, format_datetime
from datetime import datetime

router = APIRouter()

@router.get("/patients")
async def get_patients(db: Session = Depends(get_db)):
    \"\"\"Get all patients\"\"\"
    patients = db.query(Patient).filter(Patient.is_active == True).all()
    return patients

@router.get("/patients/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    \"\"\"Get specific patient\"\"\"
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/patients")
async def create_patient(patient_data: dict, db: Session = Depends(get_db)):
    \"\"\"Create new patient\"\"\"
    patient = Patient(
        patient_id=generate_secure_id(),
        **patient_data
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/doctors")
async def get_doctors(db: Session = Depends(get_db)):
    \"\"\"Get all doctors\"\"\"
    doctors = db.query(Doctor).filter(Doctor.is_active == True).all()
    return doctors

@router.get("/appointments")
async def get_appointments(db: Session = Depends(get_db)):
    \"\"\"Get all appointments\"\"\"
    appointments = db.query(Appointment).all()
    return appointments"""
        
        elif file_name == "database.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - Database Configuration
\"\"\"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from models import Base
import config

# Create database engine
engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()"""
        
        elif file_name == "test_main.py":
            content = """#!/usr/bin/env python3
\"\"\"
EHB Healthcare System - Tests
\"\"\"

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    \"\"\"Test root endpoint\"\"\"
    response = client.get("/")
    assert response.status_code == 200
    assert "EHB Healthcare System" in response.json()["message"]

def test_health():
    \"\"\"Test health endpoint\"\"\"
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_patients_endpoint():
    \"\"\"Test patients endpoint\"\"\"
    response = client.get("/api/patients")
    assert response.status_code == 200

def test_doctors_endpoint():
    \"\"\"Test doctors endpoint\"\"\"
    response = client.get("/api/doctors")
    assert response.status_code == 200

def test_appointments_endpoint():
    \"\"\"Test appointments endpoint\"\"\"
    response = client.get("/api/appointments")
    assert response.status_code == 200"""
        
        else:
            content = f"# {file_name}\n# Auto-generated file for EHB Healthcare System"
        
        with open(file_name, "w") as f:
            f.write(content)
        
        print(f"✅ {file_name}: Created")
        self.results["fixed_issues"].append(f"Created missing file: {file_name}")
    
    def check_python_syntax_errors(self):
        """Check Python files for syntax errors"""
        print("🔍 Checking Python Syntax Errors...")
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                # Parse Python code
                ast.parse(source)
                print(f"✅ {py_file.name}: No syntax errors")
                
            except SyntaxError as e:
                print(f"❌ {py_file.name}: Syntax error - {e}")
                self.results["python_errors"].append(f"Syntax error in {py_file.name}: {e}")
            except Exception as e:
                print(f"❌ {py_file.name}: Error reading file - {e}")
                self.results["python_errors"].append(f"File error in {py_file.name}: {e}")
    
    def create_missing_data(self):
        """Create missing data files"""
        print("📊 Creating Missing Data...")
        
        # Create sample data
        sample_data = {
            "patients": [
                {"id": "P001", "name": "Ahmed Khan", "email": "ahmed@example.com", "phone": "+92-300-1234567"},
                {"id": "P002", "name": "Fatima Ali", "email": "fatima@example.com", "phone": "+92-301-2345678"},
                {"id": "P003", "name": "Muhammad Hassan", "email": "hassan@example.com", "phone": "+92-302-3456789"}
            ],
            "doctors": [
                {"id": "D001", "name": "Dr. Sarah Ahmed", "specialization": "Cardiology", "email": "sarah@ehb.com"},
                {"id": "D002", "name": "Dr. Ali Hassan", "specialization": "Endocrinology", "email": "ali@ehb.com"},
                {"id": "D003", "name": "Dr. Fatima Khan", "specialization": "Pediatrics", "email": "fatima@ehb.com"}
            ],
            "appointments": [
                {"id": "A001", "patient_id": "P001", "doctor_id": "D001", "date": "2025-07-25T10:00:00"},
                {"id": "A002", "patient_id": "P002", "doctor_id": "D002", "date": "2025-07-26T14:00:00"},
                {"id": "A003", "patient_id": "P003", "doctor_id": "D003", "date": "2025-07-27T09:00:00"}
            ]
        }
        
        # Create data directory
        data_dir = self.project_root / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Save sample data
        for data_type, data in sample_data.items():
            file_path = data_dir / f"{data_type}.json"
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Created {data_type}.json with sample data")
            self.results["fixed_issues"].append(f"Created sample data: {data_type}.json")
    
    def install_missing_tools(self):
        """Install missing development tools"""
        print("🛠️ Installing Missing Tools...")
        
        tools_to_install = [
            "pip",
            "setuptools",
            "wheel",
            "virtualenv",
            "pipenv",
            "poetry"
        ]
        
        for tool in tools_to_install:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", tool], 
                             check=True, capture_output=True)
                print(f"✅ {tool}: Installed/Updated")
                self.results["fixed_issues"].append(f"Installed tool: {tool}")
            except subprocess.CalledProcessError as e:
                print(f"❌ {tool}: Failed to install")
                self.results["python_errors"].append(f"Failed to install {tool}: {e}")
    
    def run_tests(self):
        """Run Python tests"""
        print("🧪 Running Tests...")
        
        try:
            # Run pytest
            result = subprocess.run([sys.executable, "-m", "pytest", "-v"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ All tests passed")
                self.results["test_results"].append("All tests passed")
            else:
                print("❌ Some tests failed")
                self.results["test_results"].append("Some tests failed")
                print(result.stdout)
                
        except subprocess.TimeoutExpired:
            print("⏰ Tests timed out")
            self.results["test_results"].append("Tests timed out")
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            self.results["python_errors"].append(f"Test execution failed: {e}")
    
    def run_comprehensive_check(self):
        """Run comprehensive Python project check"""
        print("🔍 EHB Python Project Checker")
        print("=" * 50)
        print("Checking Python project comprehensively...")
        print("=" * 50)
        
        try:
            # Step 1: Check Python installation
            self.check_python_installation()
            
            # Step 2: Check missing dependencies
            self.check_missing_dependencies()
            
            # Step 3: Check missing files
            self.check_missing_files()
            
            # Step 4: Check Python syntax errors
            self.check_python_syntax_errors()
            
            # Step 5: Create missing data
            self.create_missing_data()
            
            # Step 6: Install missing tools
            self.install_missing_tools()
            
            # Step 7: Run tests
            self.run_tests()
            
            # Step 8: Generate summary
            self.generate_summary()
            
            print("✅ Comprehensive Python project check completed")
            
        except Exception as e:
            print(f"❌ Comprehensive check failed: {e}")
            self.results["summary"]["status"] = "failed"
            self.results["summary"]["error"] = str(e)
        
        return self.results
    
    def generate_summary(self):
        """Generate comprehensive summary"""
        print("\n" + "=" * 50)
        print("📊 PYTHON PROJECT CHECK SUMMARY")
        print("=" * 50)
        
        # Issues found and fixed
        if self.results["fixed_issues"]:
            print(f"🔧 Issues Fixed: {len(self.results['fixed_issues'])}")
            for issue in self.results["fixed_issues"][:10]:  # Show first 10
                print(f"  ✅ {issue}")
        
        # Missing dependencies
        if self.results["missing_dependencies"]:
            print(f"\n📦 Missing Dependencies: {len(self.results['missing_dependencies'])}")
            for dep in self.results["missing_dependencies"]:
                print(f"  ❌ {dep}")
        
        # Python errors
        if self.results["python_errors"]:
            print(f"\n🐍 Python Errors: {len(self.results['python_errors'])}")
            for error in self.results["python_errors"][:5]:  # Show first 5
                print(f"  ❌ {error}")
        
        # Missing files
        if self.results["missing_files"]:
            print(f"\n📁 Missing Files: {len(self.results['missing_files'])}")
            for file in self.results["missing_files"]:
                print(f"  ❌ {file}")
        
        # Test results
        if self.results["test_results"]:
            print(f"\n🧪 Test Results:")
            for result in self.results["test_results"]:
                print(f"  📊 {result}")
        
        # Calculate success rate
        total_issues = len(self.results["python_errors"]) + len(self.results["missing_dependencies"])
        fixed_issues = len(self.results["fixed_issues"])
        
        if total_issues > 0:
            success_rate = (fixed_issues / (total_issues + fixed_issues)) * 100
            print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        # Save results
        report_file = f"reports/python_project_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("=" * 50)
        
        self.results["summary"] = {
            "fixed_issues": len(self.results["fixed_issues"]),
            "python_errors": len(self.results["python_errors"]),
            "missing_dependencies": len(self.results["missing_dependencies"]),
            "missing_files": len(self.results["missing_files"]),
            "test_results": len(self.results["test_results"]),
            "success_rate": success_rate if total_issues > 0 else 100,
            "report_file": report_file
        }

def main():
    """Main function"""
    try:
        checker = EHBPythonProjectChecker()
        results = checker.run_comprehensive_check()
        
        if results["summary"]["success_rate"] >= 80:
            print("\n🎉 Python project check completed successfully!")
            return 0
        else:
            print(f"\n⚠️ Some issues remain. Success rate: {results['summary']['success_rate']:.1f}%")
            return 1
            
    except Exception as e:
        print(f"❌ Python project check failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 