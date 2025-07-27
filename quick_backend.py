
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from pathlib import Path

app = FastAPI(title="EHB Healthcare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
patients = [
    {"id": 1, "name": "Ahmed Khan", "age": 45, "gender": "Male"},
    {"id": 2, "name": "Fatima Ali", "age": 32, "gender": "Female"}
]

doctors = [
    {"id": 1, "name": "Dr. Sarah Ahmed", "specialization": "Cardiology"},
    {"id": 2, "name": "Dr. Muhammad Hassan", "specialization": "Neurology"}
]

@app.get("/")
async def root():
    return {"message": "EHB Healthcare API is running!"}

@app.get("/api/patients")
async def get_patients():
    return patients

@app.get("/api/doctors")
async def get_doctors():
    return doctors

@app.get("/api/dashboard")
async def get_dashboard():
    return {
        "total_patients": len(patients),
        "total_doctors": len(doctors),
        "status": "online"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
