"""
Patient Routes Module
Handles all patient-related API endpoints
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/patients", tags=["patients"])

# Patient models
class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    contact: str
    email: str
    blood_type: str
    allergies: List[str] = []
    conditions: List[str] = []
    medications: List[str] = []

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[List[str]] = None
    conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    status: Optional[str] = None

# Sample patient data (replace with database)
patients_db = [
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

@router.get("/", response_model=List[dict])
async def get_all_patients():
    """Get all patients"""
    return patients_db

@router.get("/{patient_id}", response_model=dict)
async def get_patient(patient_id: str):
    """Get patient by ID"""
    for patient in patients_db:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@router.post("/", response_model=dict)
async def create_patient(patient: PatientCreate):
    """Create new patient"""
    import uuid
    
    new_patient = {
        "id": f"P{str(uuid.uuid4())[:8].upper()}",
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "contact": patient.contact,
        "email": patient.email,
        "blood_type": patient.blood_type,
        "allergies": patient.allergies,
        "conditions": patient.conditions,
        "medications": patient.medications,
        "status": "active",
        "last_visit": None,
        "created_at": datetime.now().isoformat()
    }
    
    patients_db.append(new_patient)
    return new_patient

@router.put("/{patient_id}", response_model=dict)
async def update_patient(patient_id: str, patient_update: PatientUpdate):
    """Update patient"""
    for i, patient in enumerate(patients_db):
        if patient["id"] == patient_id:
            update_data = patient_update.dict(exclude_unset=True)
            patients_db[i].update(update_data)
            patients_db[i]["updated_at"] = datetime.now().isoformat()
            return patients_db[i]
    
    raise HTTPException(status_code=404, detail="Patient not found")

@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    """Delete patient (soft delete)"""
    for i, patient in enumerate(patients_db):
        if patient["id"] == patient_id:
            patients_db[i]["status"] = "deleted"
            patients_db[i]["deleted_at"] = datetime.now().isoformat()
            return {"message": "Patient deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Patient not found")

@router.get("/{patient_id}/medical-history")
async def get_patient_medical_history(patient_id: str):
    """Get patient medical history"""
    # Find patient
    patient = None
    for p in patients_db:
        if p["id"] == patient_id:
            patient = p
            break
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Return medical history (in real app, fetch from medical records)
    return {
        "patient": patient,
        "medical_history": [
            {
                "date": "2024-01-15",
                "type": "consultation",
                "doctor": "Dr. Sarah Wilson",
                "diagnosis": "Hypertension under control",
                "treatment": "Continue current medication"
            },
            {
                "date": "2024-01-10",
                "type": "lab_result",
                "doctor": "Dr. Michael Brown",
                "diagnosis": "Blood work normal",
                "treatment": "No changes needed"
            }
        ]
    }

@router.get("/{patient_id}/appointments")
async def get_patient_appointments(patient_id: str):
    """Get patient appointments"""
    # Find patient
    patient = None
    for p in patients_db:
        if p["id"] == patient_id:
            patient = p
            break
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Return appointments (in real app, fetch from appointments table)
    return {
        "patient": patient,
        "appointments": [
            {
                "id": "A001",
                "date": "2024-01-16",
                "time": "10:00 AM",
                "doctor": "Dr. Sarah Wilson",
                "type": "in-person",
                "status": "scheduled"
            },
            {
                "id": "A002",
                "date": "2024-01-20",
                "time": "2:00 PM",
                "doctor": "Dr. Michael Brown",
                "type": "video",
                "status": "scheduled"
            }
        ]
    }

@router.get("/stats/overview")
async def get_patient_stats():
    """Get patient statistics"""
    total_patients = len(patients_db)
    active_patients = len([p for p in patients_db if p["status"] == "active"])
    new_patients_this_month = len([p for p in patients_db if p["created_at"].startswith("2024-01")])
    
    return {
        "total_patients": total_patients,
        "active_patients": active_patients,
        "new_patients_this_month": new_patients_this_month,
        "average_age": sum(p["age"] for p in patients_db) / len(patients_db) if patients_db else 0,
        "gender_distribution": {
            "male": len([p for p in patients_db if p["gender"] == "male"]),
            "female": len([p for p in patients_db if p["gender"] == "female"])
        }
    } 