#!/usr/bin/env python3
"""
EHB Healthcare System - API Routes
"""

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
    """Get all patients"""
    patients = db.query(Patient).filter(Patient.is_active == True).all()
    return patients

@router.get("/patients/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get specific patient"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/patients")
async def create_patient(patient_data: dict, db: Session = Depends(get_db)):
    """Create new patient"""
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
    """Get all doctors"""
    doctors = db.query(Doctor).filter(Doctor.is_active == True).all()
    return doctors

@router.get("/appointments")
async def get_appointments(db: Session = Depends(get_db)):
    """Get all appointments"""
    appointments = db.query(Appointment).all()
    return appointments