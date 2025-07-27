"""
Telemedicine Routes Module
Handles all telemedicine and video consultation API endpoints
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import (APIRouter, HTTPException, WebSocket, WebSocketDisconnect,
                     status)
from pydantic import BaseModel

router = APIRouter(prefix="/api/telemedicine", tags=["telemedicine"])

# Telemedicine models
class ConsultationCreate(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    time: str
    type: str = "video"  # video, audio
    notes: Optional[str] = None

class ConsultationUpdate(BaseModel):
    status: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None

# Sample consultation data
consultations_db = [
    {
        "id": "C001",
        "patient_id": "P001",
        "doctor_id": "D001",
        "patient_name": "John Doe",
        "doctor_name": "Dr. Sarah Wilson",
        "date": "2024-01-16",
        "time": "10:00 AM",
        "type": "video",
        "status": "scheduled",
        "duration": None,
        "notes": "Follow-up consultation",
        "created_at": "2024-01-10T09:00:00"
    },
    {
        "id": "C002",
        "patient_id": "P002",
        "doctor_id": "D002",
        "patient_name": "Jane Smith",
        "doctor_name": "Dr. Michael Brown",
        "date": "2024-01-16",
        "time": "2:00 PM",
        "type": "video",
        "status": "in-progress",
        "duration": 25,
        "notes": "Initial consultation",
        "created_at": "2024-01-11T10:00:00"
    },
    {
        "id": "C003",
        "patient_id": "P003",
        "doctor_id": "D003",
        "patient_name": "Mike Johnson",
        "doctor_name": "Dr. Emily Davis",
        "date": "2024-01-15",
        "time": "11:30 AM",
        "type": "audio",
        "status": "completed",
        "duration": 30,
        "notes": "Routine checkup",
        "created_at": "2024-01-09T08:00:00"
    }
]

# Active connections for WebSocket
active_connections: Dict[str, WebSocket] = {}

@router.get("/consultations", response_model=List[Dict[str, Any]])
async def get_all_consultations():
    """Get all telemedicine consultations"""
    return consultations_db

@router.get("/consultations/{consultation_id}", response_model=Dict[str, Any])
async def get_consultation(consultation_id: str):
    """Get consultation by ID"""
    for consultation in consultations_db:
        if consultation["id"] == consultation_id:
            return consultation
    raise HTTPException(status_code=404, detail="Consultation not found")

@router.post("/consultations", response_model=Dict[str, Any])
async def create_consultation(consultation: ConsultationCreate):
    """Create new telemedicine consultation"""
    import uuid
    
    new_consultation = {
        "id": f"C{str(uuid.uuid4())[:8].upper()}",
        "patient_id": consultation.patient_id,
        "doctor_id": consultation.doctor_id,
        "patient_name": "Patient Name",  # Get from patient DB
        "doctor_name": "Doctor Name",    # Get from doctor DB
        "date": consultation.date,
        "time": consultation.time,
        "type": consultation.type,
        "status": "scheduled",
        "duration": None,
        "notes": consultation.notes,
        "created_at": datetime.now().isoformat()
    }
    
    consultations_db.append(new_consultation)
    return new_consultation

@router.put("/consultations/{consultation_id}", response_model=Dict[str, Any])
async def update_consultation(consultation_id: str, consultation_update: ConsultationUpdate):
    """Update consultation"""
    for i, consultation in enumerate(consultations_db):
        if consultation["id"] == consultation_id:
            update_data = consultation_update.dict(exclude_unset=True)
            consultations_db[i].update(update_data)
            consultations_db[i]["updated_at"] = datetime.now().isoformat()
            return consultations_db[i]
    
    raise HTTPException(status_code=404, detail="Consultation not found")

@router.delete("/consultations/{consultation_id}")
async def cancel_consultation(consultation_id: str):
    """Cancel consultation"""
    for i, consultation in enumerate(consultations_db):
        if consultation["id"] == consultation_id:
            consultations_db[i]["status"] = "cancelled"
            consultations_db[i]["cancelled_at"] = datetime.now().isoformat()
            return {"message": "Consultation cancelled successfully"}
    
    raise HTTPException(status_code=404, detail="Consultation not found")

@router.get("/consultations/today/scheduled")
async def get_today_consultations():
    """Get today's scheduled consultations"""
    today = datetime.now().strftime("%Y-%m-%d")
    today_consultations = [c for c in consultations_db if c["date"] == today]
    
    return {
        "date": today,
        "consultations": today_consultations,
        "total": len(today_consultations)
    }

@router.get("/consultations/active")
async def get_active_consultations():
    """Get currently active consultations"""
    active_consultations = [c for c in consultations_db if c["status"] == "in-progress"]
    
    return {
        "active_consultations": active_consultations,
        "total": len(active_consultations)
    }

@router.get("/stats/overview")
async def get_telemedicine_stats():
    """Get telemedicine statistics"""
    total_consultations = len(consultations_db)
    scheduled = len([c for c in consultations_db if c["status"] == "scheduled"])
    in_progress = len([c for c in consultations_db if c["status"] == "in-progress"])
    completed = len([c for c in consultations_db if c["status"] == "completed"])
    cancelled = len([c for c in consultations_db if c["status"] == "cancelled"])
    
    # Calculate average duration
    completed_consultations = [c for c in consultations_db if c["status"] == "completed" and c["duration"]]
    avg_duration = sum(c["duration"] for c in completed_consultations) / len(completed_consultations) if completed_consultations else 0
    
    return {
        "total_consultations": total_consultations,
        "scheduled": scheduled,
        "in_progress": in_progress,
        "completed": completed,
        "cancelled": cancelled,
        "average_duration": avg_duration,
        "completion_rate": (completed / total_consultations * 100) if total_consultations > 0 else 0,
        "type_distribution": {
            "video": len([c for c in consultations_db if c["type"] == "video"]),
            "audio": len([c for c in consultations_db if c["type"] == "audio"])
        }
    }

@router.get("/availability/{doctor_id}/{date}")
async def get_doctor_availability(doctor_id: str, date: str):
    """Get doctor's availability for telemedicine"""
    # Check if doctor exists
    doctor = {"id": doctor_id, "name": "Dr. Example", "specialization": "General"}
    
    # Get existing consultations for this doctor on this date
    existing_consultations = [c for c in consultations_db if c["doctor_id"] == doctor_id and c["date"] == date]
    
    # Generate available time slots (9 AM to 5 PM, 30-minute intervals)
    all_slots = []
    for hour in range(9, 17):
        for minute in [0, 30]:
            time_slot = f"{hour:02d}:{minute:02d}"
            all_slots.append(time_slot)
    
    # Remove booked slots
    booked_times = [c["time"] for c in existing_consultations if c["status"] != "cancelled"]
    available_slots = [slot for slot in all_slots if slot not in booked_times]
    
    return {
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "date": date,
        "available_slots": available_slots,
        "booked_slots": booked_times,
        "total_available": len(available_slots)
    }

@router.websocket("/ws/{consultation_id}")
async def websocket_endpoint(websocket: WebSocket, consultation_id: str):
    """WebSocket endpoint for real-time video consultation"""
    await websocket.accept()
    
    # Store connection
    connection_id = f"{consultation_id}_{datetime.now().timestamp()}"
    active_connections[connection_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "join":
                # User joining consultation
                await websocket.send_text(json.dumps({
                    "type": "joined",
                    "consultation_id": consultation_id,
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "offer":
                # WebRTC offer
                await websocket.send_text(json.dumps({
                    "type": "offer",
                    "sdp": message["sdp"],
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "answer":
                # WebRTC answer
                await websocket.send_text(json.dumps({
                    "type": "answer",
                    "sdp": message["sdp"],
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "ice_candidate":
                # ICE candidate
                await websocket.send_text(json.dumps({
                    "type": "ice_candidate",
                    "candidate": message["candidate"],
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "chat":
                # Chat message
                await websocket.send_text(json.dumps({
                    "type": "chat",
                    "message": message["message"],
                    "sender": message["sender"],
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "start_recording":
                # Start recording
                await websocket.send_text(json.dumps({
                    "type": "recording_started",
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "stop_recording":
                # Stop recording
                await websocket.send_text(json.dumps({
                    "type": "recording_stopped",
                    "timestamp": datetime.now().isoformat()
                }))
    
    except WebSocketDisconnect:
        # Remove connection when disconnected
        if connection_id in active_connections:
            del active_connections[connection_id]

@router.get("/consultations/{consultation_id}/chat")
async def get_consultation_chat(consultation_id: str):
    """Get chat history for a consultation"""
    # In real app, fetch from database
    chat_history = [
        {
            "id": "1",
            "sender": "doctor",
            "message": "Hello, how are you feeling today?",
            "timestamp": "2024-01-16T10:00:00"
        },
        {
            "id": "2",
            "sender": "patient",
            "message": "I'm feeling better, thank you doctor.",
            "timestamp": "2024-01-16T10:01:00"
        }
    ]
    
    return {
        "consultation_id": consultation_id,
        "chat_history": chat_history
    }

@router.post("/consultations/{consultation_id}/chat")
async def send_chat_message(consultation_id: str, message: Dict[str, str]):
    """Send a chat message during consultation"""
    # In real app, save to database
    return {
        "consultation_id": consultation_id,
        "message": message["message"],
        "sender": message["sender"],
        "timestamp": datetime.now().isoformat()
    } 