import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EHB Healthcare API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "🏥 EHB Healthcare API is running!", "status": "operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EHB Healthcare API"}

@app.get("/api/patients")
async def get_patients():
    return [
        {"id": "P001", "name": "Ahmed Khan", "status": "active"},
        {"id": "P002", "name": "Fatima Ali", "status": "active"},
        {"id": "P003", "name": "Muhammad Hassan", "status": "critical"}
    ]

@app.get("/api/doctors")
async def get_doctors():
    return [
        {"id": "D001", "name": "Dr. Sarah Ahmed", "specialization": "Cardiology"},
        {"id": "D002", "name": "Dr. Ali Hassan", "specialization": "Endocrinology"},
        {"id": "D003", "name": "Dr. Fatima Khan", "specialization": "Pediatrics"}
    ]

@app.get("/api/appointments")
async def get_appointments():
    return [
        {"id": "A001", "patient_id": "P001", "doctor_id": "D001", "status": "scheduled"},
        {"id": "A002", "patient_id": "P002", "doctor_id": "D002", "status": "scheduled"},
        {"id": "A003", "patient_id": "P003", "doctor_id": "D001", "status": "scheduled"}
    ]

if __name__ == "__main__":
    print("🏥 Starting EHB Healthcare API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 