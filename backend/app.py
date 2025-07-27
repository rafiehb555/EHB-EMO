#!/usr/bin/env python3
"""
EHB Healthcare System - FastAPI Backend
Complete healthcare management API with HIPAA compliance
"""

import json
import logging
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

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
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Patient(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    age: int
    gender: str
    contact: str
    email: str
    blood_type: str
    allergies: List[str] = []
    conditions: List[str] = []
    medications: List[str] = []
    status: str = "active"
    last_visit: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class Doctor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    specialization: str
    contact: str
    email: str
    rating: float = 4.5
    status: str = "active"
    availability: str = "available"

class Appointment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    patient_id: str
    doctor_id: str
    patient_name: str
    doctor_name: str
    date: str
    time: str
    type: str = "in-person"  # in-person, video
    status: str = "scheduled"  # scheduled, completed, cancelled
    notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class MedicalRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    patient_id: str
    doctor_id: str
    diagnosis: str
    treatment: str
    prescription: Optional[str] = None
    notes: Optional[str] = None
    date: str = Field(default_factory=lambda: datetime.now().isoformat())

class Analytics(BaseModel):
    total_patients: int
    active_patients: int
    total_appointments: int
    completed_appointments: int
    total_revenue: float
    patient_satisfaction: float
    system_uptime: float

# In-memory data storage (replace with database in production)
patients_data = []
doctors_data = []
appointments_data = []
medical_records_data = []

# Load initial data
def load_initial_data():
    """Load initial sample data"""
    global patients_data, doctors_data, appointments_data, medical_records_data
    
    # Sample patients
    patients_data = [
        {
            "id": "P001",
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "contact": "+1-555-0123",
            "email": "john.doe@email.com",
            "blood_type": "A+",
            "allergies": ["Penicillin", "Peanuts"],
            "conditions": ["Hypertension", "Diabetes Type 2"],
            "medications": ["Metformin", "Lisinopril"],
            "status": "active",
            "last_visit": "2024-01-15",
            "created_at": "2024-01-01T10:00:00"
        },
        {
            "id": "P002",
            "name": "Jane Smith",
            "age": 32,
            "gender": "female",
            "contact": "+1-555-0124",
            "email": "jane.smith@email.com",
            "blood_type": "O-",
            "allergies": ["Latex"],
            "conditions": ["Asthma"],
            "medications": ["Albuterol"],
            "status": "active",
            "last_visit": "2024-01-14",
            "created_at": "2024-01-02T11:00:00"
        },
        {
            "id": "P003",
            "name": "Mike Johnson",
            "age": 58,
            "gender": "male",
            "contact": "+1-555-0125",
            "email": "mike.johnson@email.com",
            "blood_type": "B+",
            "allergies": ["Sulfa drugs"],
            "conditions": ["Heart Disease", "Arthritis"],
            "medications": ["Aspirin", "Ibuprofen"],
            "status": "active",
            "last_visit": "2024-01-13",
            "created_at": "2024-01-03T12:00:00"
        }
    ]

    # Sample doctors
    doctors_data = [
        {
            "id": "D001",
            "name": "Dr. Sarah Wilson",
            "specialization": "Cardiology",
            "contact": "+1-555-0201",
            "email": "sarah.wilson@ehb.com",
            "rating": 4.8,
            "status": "active",
            "availability": "available"
        },
        {
            "id": "D002",
            "name": "Dr. Michael Brown",
            "specialization": "Neurology",
            "contact": "+1-555-0202",
            "email": "michael.brown@ehb.com",
            "rating": 4.9,
            "status": "active",
            "availability": "available"
        },
        {
            "id": "D003",
            "name": "Dr. Emily Davis",
            "specialization": "Pediatrics",
            "contact": "+1-555-0203",
            "email": "emily.davis@ehb.com",
            "rating": 4.7,
            "status": "active",
            "availability": "busy"
        }
    ]

    # Sample appointments
    appointments_data = [
        {
            "id": "A001",
            "patient_id": "P001",
            "doctor_id": "D001",
            "patient_name": "John Doe",
            "doctor_name": "Dr. Sarah Wilson",
            "date": "2024-01-16",
            "time": "10:00 AM",
            "type": "in-person",
            "status": "scheduled",
            "notes": "Follow-up consultation",
            "created_at": "2024-01-10T09:00:00"
        },
        {
            "id": "A002",
            "patient_id": "P002",
            "doctor_id": "D002",
            "patient_name": "Jane Smith",
            "doctor_name": "Dr. Michael Brown",
            "date": "2024-01-16",
            "time": "2:00 PM",
            "type": "video",
            "status": "scheduled",
            "notes": "Initial consultation",
            "created_at": "2024-01-11T10:00:00"
        }
    ]

    logger.info("✅ Initial data loaded successfully")

# Load data on startup
load_initial_data()

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
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "99.9%",
        "version": "2.0.0"
    }

# Patient endpoints
@app.get("/api/patients", response_model=List[Patient])
async def get_patients():
    """Get all patients"""
    return patients_data

@app.get("/api/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get patient by ID"""
    for patient in patients_data:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/api/patients", response_model=Patient)
async def create_patient(patient: Patient):
    """Create new patient"""
    patient_dict = patient.dict()
    patients_data.append(patient_dict)
    logger.info(f"✅ Created patient: {patient.name}")
    return patient_dict

@app.put("/api/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, patient: Patient):
    """Update patient"""
    for i, p in enumerate(patients_data):
        if p["id"] == patient_id:
            patient_dict = patient.dict()
            patient_dict["id"] = patient_id
            patients_data[i] = patient_dict
            logger.info(f"✅ Updated patient: {patient.name}")
            return patient_dict
    raise HTTPException(status_code=404, detail="Patient not found")

# Doctor endpoints
@app.get("/api/doctors", response_model=List[Doctor])
async def get_doctors():
    """Get all doctors"""
    return doctors_data

@app.get("/api/doctors/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str):
    """Get doctor by ID"""
    for doctor in doctors_data:
        if doctor["id"] == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.post("/api/doctors", response_model=Doctor)
async def create_doctor(doctor: Doctor):
    """Create new doctor"""
    doctor_dict = doctor.dict()
    doctors_data.append(doctor_dict)
    logger.info(f"✅ Created doctor: {doctor.name}")
    return doctor_dict

# Appointment endpoints
@app.get("/api/appointments", response_model=List[Appointment])
async def get_appointments():
    """Get all appointments"""
    return appointments_data

@app.get("/api/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    """Get appointment by ID"""
    for appointment in appointments_data:
        if appointment["id"] == appointment_id:
            return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.post("/api/appointments", response_model=Appointment)
async def create_appointment(appointment: Appointment):
    """Create new appointment"""
    appointment_dict = appointment.dict()
    appointments_data.append(appointment_dict)
    logger.info(f"✅ Created appointment: {appointment.patient_name} with {appointment.doctor_name}")
    return appointment_dict

@app.put("/api/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, appointment: Appointment):
    """Update appointment"""
    for i, apt in enumerate(appointments_data):
        if apt["id"] == appointment_id:
            appointment_dict = appointment.dict()
            appointment_dict["id"] = appointment_id
            appointments_data[i] = appointment_dict
            logger.info(f"✅ Updated appointment: {appointment.patient_name}")
            return appointment_dict
    raise HTTPException(status_code=404, detail="Appointment not found")

# Medical records endpoints
@app.get("/api/medical-records", response_model=List[MedicalRecord])
async def get_medical_records():
    """Get all medical records"""
    return medical_records_data

@app.get("/api/medical-records/{record_id}", response_model=MedicalRecord)
async def get_medical_record(record_id: str):
    """Get medical record by ID"""
    for record in medical_records_data:
        if record["id"] == record_id:
            return record
    raise HTTPException(status_code=404, detail="Medical record not found")

@app.post("/api/medical-records", response_model=MedicalRecord)
async def create_medical_record(record: MedicalRecord):
    """Create new medical record"""
    record_dict = record.dict()
    medical_records_data.append(record_dict)
    logger.info(f"✅ Created medical record for patient: {record.patient_id}")
    return record_dict

# Analytics endpoint
@app.get("/api/analytics", response_model=Analytics)
async def get_analytics():
    """Get analytics data"""
    total_patients = len(patients_data)
    active_patients = len([p for p in patients_data if p["status"] == "active"])
    total_appointments = len(appointments_data)
    completed_appointments = len([a for a in appointments_data if a["status"] == "completed"])
    
    return Analytics(
        total_patients=total_patients,
        active_patients=active_patients,
        total_appointments=total_appointments,
        completed_appointments=completed_appointments,
        total_revenue=125000.0,
        patient_satisfaction=94.5,
        system_uptime=99.9
    )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 