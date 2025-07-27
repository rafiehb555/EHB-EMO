
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
