"""
Appointment Routes Module
Handles all appointment-related API endpoints
"""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

# Appointment models
class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    time: str
    type: str = "in-person"  # in-person, video
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

# Sample appointment data (replace with database)
appointments_db = [
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
    },
    {
        "id": "A003",
        "patient_id": "P003",
        "doctor_id": "D003",
        "patient_name": "Mike Johnson",
        "doctor_name": "Dr. Emily Davis",
        "date": "2024-01-15",
        "time": "11:30 AM",
        "type": "in-person",
        "status": "completed",
        "notes": "Routine checkup",
        "created_at": "2024-01-09T08:00:00"
    }
]

# Sample patient and doctor data for reference
patients_db = [
    {"id": "P001", "name": "John Doe"},
    {"id": "P002", "name": "Jane Smith"},
    {"id": "P003", "name": "Mike Johnson"}
]

doctors_db = [
    {"id": "D001", "name": "Dr. Sarah Wilson", "specialization": "Cardiology"},
    {"id": "D002", "name": "Dr. Michael Brown", "specialization": "Neurology"},
    {"id": "D003", "name": "Dr. Emily Davis", "specialization": "Pediatrics"}
]

@router.get("/", response_model=List[dict])
async def get_all_appointments():
    """Get all appointments"""
    return appointments_db

@router.get("/{appointment_id}", response_model=dict)
async def get_appointment(appointment_id: str):
    """Get appointment by ID"""
    for appointment in appointments_db:
        if appointment["id"] == appointment_id:
            return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")

@router.post("/", response_model=dict)
async def create_appointment(appointment: AppointmentCreate):
    """Create new appointment"""
    import uuid

    # Get patient and doctor names
    patient_name = next((p["name"] for p in patients_db if p["id"] == appointment.patient_id), "Unknown Patient")
    doctor_name = next((d["name"] for d in doctors_db if d["id"] == appointment.doctor_id), "Unknown Doctor")
    
    new_appointment = {
        "id": f"A{str(uuid.uuid4())[:8].upper()}",
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "patient_name": patient_name,
        "doctor_name": doctor_name,
        "date": appointment.date,
        "time": appointment.time,
        "type": appointment.type,
        "status": "scheduled",
        "notes": appointment.notes,
        "created_at": datetime.now().isoformat()
    }
    
    appointments_db.append(new_appointment)
    return new_appointment

@router.put("/{appointment_id}", response_model=dict)
async def update_appointment(appointment_id: str, appointment_update: AppointmentUpdate):
    """Update appointment"""
    for i, appointment in enumerate(appointments_db):
        if appointment["id"] == appointment_id:
            update_data = appointment_update.dict(exclude_unset=True)
            appointments_db[i].update(update_data)
            appointments_db[i]["updated_at"] = datetime.now().isoformat()
            return appointments_db[i]
    
    raise HTTPException(status_code=404, detail="Appointment not found")

@router.delete("/{appointment_id}")
async def cancel_appointment(appointment_id: str):
    """Cancel appointment"""
    for i, appointment in enumerate(appointments_db):
        if appointment["id"] == appointment_id:
            appointments_db[i]["status"] = "cancelled"
            appointments_db[i]["cancelled_at"] = datetime.now().isoformat()
            return {"message": "Appointment cancelled successfully"}
    
    raise HTTPException(status_code=404, detail="Appointment not found")

@router.get("/today/scheduled")
async def get_today_appointments():
    """Get today's scheduled appointments"""
    today = datetime.now().strftime("%Y-%m-%d")
    today_appointments = [apt for apt in appointments_db if apt["date"] == today]
    
    return {
        "date": today,
        "appointments": today_appointments,
        "total": len(today_appointments)
    }

@router.get("/upcoming")
async def get_upcoming_appointments():
    """Get upcoming appointments"""
    today = datetime.now().date()
    upcoming = [apt for apt in appointments_db if datetime.strptime(apt["date"], "%Y-%m-%d").date() > today]
    
    return {
        "upcoming_appointments": upcoming,
        "total": len(upcoming)
    }

@router.get("/doctor/{doctor_id}")
async def get_doctor_appointments(doctor_id: str):
    """Get appointments for a specific doctor"""
    doctor_appointments = [apt for apt in appointments_db if apt["doctor_id"] == doctor_id]
    
    if not doctor_appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this doctor")
    
    return {
        "doctor_id": doctor_id,
        "appointments": doctor_appointments,
        "total": len(doctor_appointments)
    }

@router.get("/patient/{patient_id}")
async def get_patient_appointments(patient_id: str):
    """Get appointments for a specific patient"""
    patient_appointments = [apt for apt in appointments_db if apt["patient_id"] == patient_id]
    
    if not patient_appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this patient")
    
    return {
        "patient_id": patient_id,
        "appointments": patient_appointments,
        "total": len(patient_appointments)
    }

@router.get("/stats/overview")
async def get_appointment_stats():
    """Get appointment statistics"""
    total_appointments = len(appointments_db)
    scheduled = len([apt for apt in appointments_db if apt["status"] == "scheduled"])
    completed = len([apt for apt in appointments_db if apt["status"] == "completed"])
    cancelled = len([apt for apt in appointments_db if apt["status"] == "cancelled"])
    
    # Today's stats
    today = datetime.now().strftime("%Y-%m-%d")
    today_appointments = [apt for apt in appointments_db if apt["date"] == today]
    
    return {
        "total_appointments": total_appointments,
        "scheduled": scheduled,
        "completed": completed,
        "cancelled": cancelled,
        "today_appointments": len(today_appointments),
        "completion_rate": (completed / total_appointments * 100) if total_appointments > 0 else 0,
        "type_distribution": {
            "in_person": len([apt for apt in appointments_db if apt["type"] == "in-person"]),
            "video": len([apt for apt in appointments_db if apt["type"] == "video"])
        }
    }

@router.get("/available-slots/{doctor_id}/{date}")
async def get_available_slots(doctor_id: str, date: str):
    """Get available appointment slots for a doctor on a specific date"""
    # Check if doctor exists
    doctor = next((d for d in doctors_db if d["id"] == doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Get existing appointments for this doctor on this date
    existing_appointments = [apt for apt in appointments_db if apt["doctor_id"] == doctor_id and apt["date"] == date]
    
    # Generate available time slots (9 AM to 5 PM, 30-minute intervals)
    all_slots = []
    for hour in range(9, 17):
        for minute in [0, 30]:
            time_slot = f"{hour:02d}:{minute:02d}"
            all_slots.append(time_slot)
    
    # Remove booked slots
    booked_times = [apt["time"] for apt in existing_appointments if apt["status"] != "cancelled"]
    available_slots = [slot for slot in all_slots if slot not in booked_times]
    
    return {
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "date": date,
        "available_slots": available_slots,
        "booked_slots": booked_times,
        "total_available": len(available_slots)
    } 