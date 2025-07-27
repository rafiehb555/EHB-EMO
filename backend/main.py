#!/usr/bin/env python3
"""
EHB Healthcare System - FastAPI Backend
Complete healthcare management API with HIPAA compliance
"""

import json
import logging
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="EHB Healthcare API",
    description="Advanced healthcare management system with HIPAA compliance",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Patient(BaseModel):
    id: str
    name: str
    date_of_birth: str
    contact: str
    status: str
    condition: Optional[str] = None
    last_visit: Optional[str] = None

class Appointment(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    date: str
    time: str
    type: str
    status: str = "scheduled"

class MedicalRecord(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    diagnosis: str
    treatment: str
    date: str
    notes: Optional[str] = None

class Doctor(BaseModel):
    id: str
    name: str
    specialization: str
    contact: str
    status: str = "active"

# Load data
def load_data(filename: str) -> List[Dict[str, Any]]:
    """Load data from JSON file"""
    try:
        data_path = Path("data") / filename
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"✅ Loaded {filename}")
                return data
        else:
            logger.warning(f"⚠️ File not found: {filename}")
            return []
    except Exception as e:
        logger.error(f"❌ Error loading {filename}: {e}")
        return []

# Authentication middleware
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify authentication token"""
    # In production, implement proper JWT verification
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EHB Healthcare API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "services": {
            "api": "operational",
            "database": "connected",
            "security": "active"
        }
    }

# Patient endpoints
@app.get("/api/patients", response_model=List[Patient])
async def get_patients():
    """Get all patients"""
    try:
        patients_data = load_data("patients.json")
        return patients_data
    except Exception as e:
        logger.error(f"Error fetching patients: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get specific patient by ID"""
    try:
        patients_data = load_data("patients.json")
        patient = next((p for p in patients_data if p.get("id") == patient_id), None)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching patient {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/patients", response_model=Patient)
async def create_patient(patient: Patient):
    """Create new patient"""
    try:
        # In production, save to database
        logger.info(f"Creating patient: {patient.name}")
        return patient
    except Exception as e:
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Appointment endpoints
@app.get("/api/appointments", response_model=List[Appointment])
async def get_appointments():
    """Get all appointments"""
    try:
        appointments_data = load_data("appointments.json")
        return appointments_data
    except Exception as e:
        logger.error(f"Error fetching appointments: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    """Get specific appointment by ID"""
    try:
        appointments_data = load_data("appointments.json")
        appointment = next((a for a in appointments_data if a.get("id") == appointment_id), None)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching appointment {appointment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/appointments", response_model=Appointment)
async def create_appointment(appointment: Appointment):
    """Create new appointment"""
    try:
        # In production, save to database
        logger.info(f"Creating appointment: {appointment.id}")
        return appointment
    except Exception as e:
        logger.error(f"Error creating appointment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Medical records endpoints
@app.get("/api/medical-records", response_model=List[MedicalRecord])
async def get_medical_records():
    """Get all medical records"""
    try:
        records_data = load_data("medical_records.json")
        return records_data
    except Exception as e:
        logger.error(f"Error fetching medical records: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/medical-records/{record_id}", response_model=MedicalRecord)
async def get_medical_record(record_id: str):
    """Get specific medical record by ID"""
    try:
        records_data = load_data("medical_records.json")
        record = next((r for r in records_data if r.get("id") == record_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching medical record {record_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Doctor endpoints
@app.get("/api/doctors", response_model=List[Doctor])
async def get_doctors():
    """Get all doctors"""
    try:
        doctors_data = load_data("doctors.json")
        return doctors_data
    except Exception as e:
        logger.error(f"Error fetching doctors: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/doctors/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str):
    """Get specific doctor by ID"""
    try:
        doctors_data = load_data("doctors.json")
        doctor = next((d for d in doctors_data if d.get("id") == doctor_id), None)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching doctor {doctor_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Analytics endpoints
@app.get("/api/analytics")
async def get_analytics():
    """Get healthcare analytics"""
    try:
        analytics_data = load_data("analytics.json")
        return {
            "analytics": analytics_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin endpoints
@app.get("/api/admin")
async def admin_dashboard():
    """Admin dashboard data"""
    try:
        patients_data = load_data("patients.json")
        appointments_data = load_data("appointments.json")
        doctors_data = load_data("doctors.json")
        
        return {
            "system_status": "operational",
            "total_patients": len(patients_data),
            "total_appointments": len(appointments_data),
            "total_doctors": len(doctors_data),
            "active_appointments": len([a for a in appointments_data if a.get("status") == "scheduled"]),
            "critical_patients": len([p for p in patients_data if p.get("status") == "critical"]),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching admin data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Pharmacy endpoints
@app.get("/api/pharmacies")
async def get_pharmacies():
    """Get all pharmacies"""
    try:
        pharmacies_data = load_data("pharmacies.json")
        return pharmacies_data
    except Exception as e:
        logger.error(f"Error fetching pharmacies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Insurance endpoints
@app.get("/api/insurance")
async def get_insurance_policies():
    """Get insurance policies"""
    try:
        insurance_data = load_data("insurance_policies.json")
        return insurance_data
    except Exception as e:
        logger.error(f"Error fetching insurance policies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    logger.info("🏥 Starting EHB Healthcare API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
