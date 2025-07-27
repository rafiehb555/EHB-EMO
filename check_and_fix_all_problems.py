"""
Check and Fix All Current Problems
Comprehensive problem detection and fixing script
"""

import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProblemChecker:
    """Check and fix all current problems"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.problems_found = []
        self.problems_fixed = []
    
    def check_python_environment(self):
        """Check Python environment and dependencies"""
        logger.info("🔍 Checking Python environment...")
        
        try:
            # Check Python version
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            logger.info(f"✅ Python: {result.stdout.strip()}")
        except Exception as e:
            self.problems_found.append(f"Python version check failed: {e}")
        
        # Check pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True)
            logger.info(f"✅ Pip: {result.stdout.strip()}")
        except Exception as e:
            self.problems_found.append(f"Pip check failed: {e}")
        
        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            logger.info("✅ Virtual environment detected")
        else:
            self.problems_found.append("No virtual environment detected")
    
    def check_node_environment(self):
        """Check Node.js environment"""
        logger.info("🔍 Checking Node.js environment...")
        
        try:
            # Check Node.js
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True)
            logger.info(f"✅ Node.js: {result.stdout.strip()}")
        except Exception as e:
            self.problems_found.append(f"Node.js not found: {e}")
        
        try:
            # Check npm
            result = subprocess.run(["npm", "--version"], 
                                  capture_output=True, text=True)
            logger.info(f"✅ NPM: {result.stdout.strip()}")
        except Exception as e:
            self.problems_found.append(f"NPM not found: {e}")
    
    def check_frontend_dependencies(self):
        """Check and fix frontend dependencies"""
        logger.info("🔍 Checking frontend dependencies...")
        
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            self.problems_found.append("Frontend directory not found")
            return
        
        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            self.problems_found.append("package.json not found")
            return
        
        # Check node_modules
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            logger.info("📦 Installing frontend dependencies...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
                self.problems_fixed.append("Frontend dependencies installed")
            except subprocess.CalledProcessError as e:
                self.problems_found.append(f"Failed to install frontend dependencies: {e}")
    
    def check_backend_dependencies(self):
        """Check and fix backend dependencies"""
        logger.info("🔍 Checking backend dependencies...")
        
        backend_dir = self.project_root / "backend"
        if not backend_dir.exists():
            self.problems_found.append("Backend directory not found")
            return
        
        # Check requirements.txt
        requirements_file = backend_dir / "requirements.txt"
        if not requirements_file.exists():
            logger.info("📦 Creating requirements.txt...")
            requirements_content = """
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
bcrypt==4.1.2
pyjwt==2.8.0
flask==3.0.0
flask-cors==4.0.0
aiofiles==23.2.1
httpx==0.25.2
websockets==12.0
markdown==3.5.1
jinja2==3.1.2
"""
            with open(requirements_file, "w") as f:
                f.write(requirements_content)
            self.problems_fixed.append("Created requirements.txt")
        
        # Install Python dependencies
        try:
            logger.info("📦 Installing backend dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True)
            self.problems_fixed.append("Backend dependencies installed")
        except subprocess.CalledProcessError as e:
            self.problems_found.append(f"Failed to install backend dependencies: {e}")
    
    def check_database(self):
        """Check and setup database"""
        logger.info("🔍 Checking database...")
        
        # Create data directory if it doesn't exist
        data_dir = self.project_root / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Check if database files exist
        db_files = ["patients.json", "doctors.json", "appointments.json", 
                   "medical_records.json", "pharmacies.json", "insurance.json"]
        
        for db_file in db_files:
            file_path = data_dir / db_file
            if not file_path.exists():
                logger.info(f"📊 Creating {db_file}...")
                self.create_sample_data(db_file)
                self.problems_fixed.append(f"Created {db_file}")
    
    def create_sample_data(self, filename):
        """Create sample data for the given filename"""
        data_dir = self.project_root / "data"
        
        sample_data = {
            "patients.json": {
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
                        "insurance_number": "SL-2024-001",
                        "last_visit": "2024-01-15",
                        "next_appointment": "2024-01-25"
                    }
                ]
            },
            "doctors.json": {
                "doctors": [
                    {
                        "id": 1,
                        "name": "Dr. Sarah Ahmed",
                        "specialization": "Cardiology",
                        "experience_years": 15,
                        "phone": "+92-300-4567890",
                        "email": "dr.sarah.ahmed@ehb.com",
                        "qualifications": ["MBBS", "FCPS", "FRCP"],
                        "availability": "Mon-Fri 9AM-5PM",
                        "rating": 4.8,
                        "patients_count": 150,
                        "consultation_fee": 5000,
                        "languages": ["English", "Urdu"],
                        "department": "Cardiology"
                    }
                ]
            },
            "appointments.json": {
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
                        "duration_minutes": 30,
                        "room": "Cardiology-101",
                        "priority": "Normal"
                    }
                ]
            },
            "medical_records.json": {
                "medical_records": [
                    {
                        "id": 1,
                        "patient_id": 1,
                        "doctor_id": 1,
                        "date": "2024-01-15",
                        "diagnosis": "Type 2 Diabetes",
                        "treatment": "Metformin 500mg twice daily",
                        "prescription": "Metformin, Glimepiride",
                        "notes": "Patient shows improvement in blood sugar levels",
                        "vital_signs": {
                            "blood_pressure": "140/90",
                            "heart_rate": "72",
                            "temperature": "98.6",
                            "weight": "75kg"
                        }
                    }
                ]
            },
            "pharmacies.json": {
                "pharmacies": [
                    {
                        "id": 1,
                        "name": "MedPlus Pharmacy",
                        "address": "Shop 15, Mall Road, Islamabad",
                        "phone": "+92-51-1234567",
                        "email": "info@medplus.com",
                        "operating_hours": "24/7",
                        "services": ["Prescription", "OTC", "Vaccination"]
                    }
                ]
            },
            "insurance.json": {
                "insurance_providers": [
                    {
                        "id": 1,
                        "name": "State Life Insurance",
                        "coverage_types": ["Health", "Life", "Accident"],
                        "contact": "+92-51-2345678",
                        "website": "www.statelifepakistan.com"
                    }
                ]
            }
        }
        
        if filename in sample_data:
            with open(data_dir / filename, "w", encoding="utf-8") as f:
                json.dump(sample_data[filename], f, indent=2, ensure_ascii=False)
    
    def check_environment_files(self):
        """Check and create environment files"""
        logger.info("🔍 Checking environment files...")
        
        # Create .env.example
        env_example = self.project_root / ".env.example"
        if not env_example.exists():
            logger.info("📝 Creating .env.example...")
            env_content = """
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ehb_healthcare
REDIS_URL=redis://localhost:6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=EHB Healthcare

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/ehb_healthcare.log
"""
            with open(env_example, "w") as f:
                f.write(env_content)
            self.problems_fixed.append("Created .env.example")
        
        # Create .env.local for frontend
        frontend_env = self.project_root / "frontend" / ".env.local"
        if not frontend_env.exists():
            logger.info("📝 Creating frontend .env.local...")
            frontend_env_content = """
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=EHB Healthcare
NEXT_PUBLIC_VERSION=1.0.0
"""
            with open(frontend_env, "w") as f:
                f.write(frontend_env_content)
            self.problems_fixed.append("Created frontend .env.local")
    
    def check_server_status(self):
        """Check if servers are running"""
        logger.info("🔍 Checking server status...")
        
        # Check if backend server is running
        try:
            import requests
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Backend server is running")
            else:
                self.problems_found.append("Backend server not responding properly")
        except:
            self.problems_found.append("Backend server is not running")
        
        # Check if frontend server is running
        try:
            response = requests.get("http://localhost:3001/", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Frontend server is running")
            else:
                self.problems_found.append("Frontend server not responding properly")
        except:
            self.problems_found.append("Frontend server is not running")
    
    def fix_all_problems(self):
        """Fix all detected problems"""
        logger.info("🔧 Fixing all problems...")
        
        # Start backend server if not running
        if "Backend server is not running" in self.problems_found:
            logger.info("🚀 Starting backend server...")
            try:
                backend_script = self.project_root / "api_server.py"
                if backend_script.exists():
                    subprocess.Popen([sys.executable, str(backend_script)], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.problems_fixed.append("Started backend server")
            except Exception as e:
                self.problems_found.append(f"Failed to start backend server: {e}")
        
        # Start frontend server if not running
        if "Frontend server is not running" in self.problems_found:
            logger.info("🚀 Starting frontend server...")
            try:
                frontend_dir = self.project_root / "frontend"
                subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.problems_fixed.append("Started frontend server")
            except Exception as e:
                self.problems_found.append(f"Failed to start frontend server: {e}")
    
    def run_comprehensive_check(self):
        """Run comprehensive problem check and fix"""
        logger.info("🚀 Starting comprehensive problem check...")
        
        print("\n" + "="*60)
        print("🔍 EHB Healthcare System - Problem Check & Fix")
        print("="*60)
        
        # Step 1: Check environments
        print("\n1️⃣ Checking environments...")
        self.check_python_environment()
        self.check_node_environment()
        
        # Step 2: Check dependencies
        print("\n2️⃣ Checking dependencies...")
        self.check_frontend_dependencies()
        self.check_backend_dependencies()
        
        # Step 3: Check database
        print("\n3️⃣ Checking database...")
        self.check_database()
        
        # Step 4: Check environment files
        print("\n4️⃣ Checking environment files...")
        self.check_environment_files()
        
        # Step 5: Check server status
        print("\n5️⃣ Checking server status...")
        self.check_server_status()
        
        # Step 6: Fix problems
        print("\n6️⃣ Fixing problems...")
        self.fix_all_problems()
        
        print("\n" + "="*60)
        print("📊 Problem Check Results:")
        print(f"❌ Problems Found: {len(self.problems_found)}")
        print(f"✅ Problems Fixed: {len(self.problems_fixed)}")
        
        if self.problems_found:
            print("\n❌ Remaining Problems:")
            for problem in self.problems_found:
                print(f"  - {problem}")
        
        if self.problems_fixed:
            print("\n✅ Fixed Problems:")
            for fix in self.problems_fixed:
                print(f"  - {fix}")
        
        print("="*60)

def main():
    """Main function"""
    checker = ProblemChecker()
    checker.run_comprehensive_check()

if __name__ == "__main__":
    main() 