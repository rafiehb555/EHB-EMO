"""
EHB Healthcare API Server - Fixed Version
"""

import json
import logging
import os
import time
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Project root
PROJECT_ROOT = Path(".")
DATA_DIR = PROJECT_ROOT / "data"

def load_json_data(filename):
    """Load JSON data from file"""
    try:
        file_path = DATA_DIR / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"File not found: {file_path}")
            return {"error": f"File {filename} not found"}
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return {"error": f"Error loading {filename}"}

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "EHB Healthcare API Server",
        "status": "running",
        "version": "1.0.0",
        "endpoints": [
            "/api/patients",
            "/api/doctors", 
            "/api/appointments",
            "/api/medical-records",
            "/api/pharmacies",
            "/api/insurance",
            "/api/dashboard",
            "/api/status"
        ]
    })

@app.route('/api/patients')
def get_patients():
    """Get all patients"""
    data = load_json_data("patients.json")
    return jsonify(data)

@app.route('/api/doctors')
def get_doctors():
    """Get all doctors"""
    data = load_json_data("doctors.json")
    return jsonify(data)

@app.route('/api/appointments')
def get_appointments():
    """Get all appointments"""
    data = load_json_data("appointments.json")
    return jsonify(data)

@app.route('/api/medical-records')
def get_medical_records():
    """Get all medical records"""
    data = load_json_data("medical_records.json")
    return jsonify(data)

@app.route('/api/pharmacies')
def get_pharmacies():
    """Get all pharmacies"""
    data = load_json_data("pharmacies.json")
    return jsonify(data)

@app.route('/api/insurance')
def get_insurance():
    """Get all insurance providers"""
    data = load_json_data("insurance.json")
    return jsonify(data)

@app.route('/api/dashboard')
def get_dashboard():
    """Get dashboard data"""
    return jsonify({
        "total_patients": 150,
        "total_doctors": 25,
        "total_appointments": 45,
        "system_status": "online",
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        "status": "online",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0.0"
    })

def create_sample_data():
    """Create sample data if it doesn't exist"""
    DATA_DIR.mkdir(exist_ok=True)
    
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
    
    for filename, data in sample_data.items():
        file_path = DATA_DIR / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Created {filename}")

def main():
    """Main function"""
    print("="*60)
    print("🏥 EHB Healthcare API Server - Fixed Version")
    print("="*60)
    
    # Create sample data
    print("📊 Creating sample data...")
    create_sample_data()
    
    # Try different ports
    ports = [8001, 8002, 8003, 8004, 8005]
    
    for port in ports:
        try:
            print(f"🚀 Starting server on port {port}...")
            app.run(host='0.0.0.0', port=port, debug=False)
            break
        except OSError as e:
            print(f"❌ Port {port} is in use, trying next port...")
            continue
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            break
    else:
        print("❌ Could not start server on any port")

if __name__ == "__main__":
    main() 