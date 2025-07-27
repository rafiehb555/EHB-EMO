#!/usr/bin/env python3
"""
EHB Healthcare System - API Server
Serves healthcare endpoints with proper JSON responses
"""

import http.server
import socketserver
import json
import time
from datetime import datetime

PORT = 8000

class EHBAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API Server",
                "status": "operational",
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat(),
                "endpoints": {
                    "/api/patients": "Get all patients",
                    "/api/doctors": "Get all doctors", 
                    "/api/appointments": "Get all appointments",
                    "/api/analytics": "Get healthcare analytics",
                    "/health": "Health check"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "EHB Healthcare API",
                "timestamp": datetime.now().isoformat(),
                "uptime": "99.9%"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/api/patients':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            patients = [
                {
                    "id": "P001",
                    "name": "Ahmed Khan",
                    "date_of_birth": "1985-03-15",
                    "contact": "+92-300-1234567",
                    "status": "active",
                    "condition": "Hypertension",
                    "last_visit": "2024-01-15"
                },
                {
                    "id": "P002", 
                    "name": "Fatima Ali",
                    "date_of_birth": "1990-07-22",
                    "contact": "+92-301-2345678",
                    "status": "active",
                    "condition": "Diabetes Type 2",
                    "last_visit": "2024-01-20"
                },
                {
                    "id": "P003",
                    "name": "Muhammad Hassan", 
                    "date_of_birth": "1978-11-08",
                    "contact": "+92-302-3456789",
                    "status": "critical",
                    "condition": "Heart Disease",
                    "last_visit": "2024-01-25"
                },
                {
                    "id": "P004",
                    "name": "Ayesha Malik",
                    "date_of_birth": "1995-04-12", 
                    "contact": "+92-303-4567890",
                    "status": "active",
                    "condition": "Asthma",
                    "last_visit": "2024-01-18"
                },
                {
                    "id": "P005",
                    "name": "Omar Farooq",
                    "date_of_birth": "1982-09-30",
                    "contact": "+92-304-5678901", 
                    "status": "active",
                    "condition": "Back Pain",
                    "last_visit": "2024-01-22"
                }
            ]
            self.wfile.write(json.dumps(patients, indent=2).encode())
            
        elif self.path == '/api/doctors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            doctors = [
                {
                    "id": "D001",
                    "name": "Dr. Sarah Ahmed",
                    "specialization": "Cardiology",
                    "contact": "+92-300-1111111",
                    "status": "active",
                    "experience": "15 years"
                },
                {
                    "id": "D002",
                    "name": "Dr. Ali Hassan",
                    "specialization": "Endocrinology", 
                    "contact": "+92-300-2222222",
                    "status": "active",
                    "experience": "12 years"
                },
                {
                    "id": "D003",
                    "name": "Dr. Fatima Khan",
                    "specialization": "Pediatrics",
                    "contact": "+92-300-3333333", 
                    "status": "active",
                    "experience": "18 years"
                },
                {
                    "id": "D004",
                    "name": "Dr. Omar Malik",
                    "specialization": "Orthopedics",
                    "contact": "+92-300-4444444",
                    "status": "active", 
                    "experience": "10 years"
                },
                {
                    "id": "D005",
                    "name": "Dr. Ayesha Ali",
                    "specialization": "Neurology",
                    "contact": "+92-300-5555555",
                    "status": "active",
                    "experience": "20 years"
                }
            ]
            self.wfile.write(json.dumps(doctors, indent=2).encode())
            
        elif self.path == '/api/appointments':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            appointments = [
                {
                    "id": "A001",
                    "patient_id": "P001",
                    "doctor_id": "D001", 
                    "date": "2024-02-01",
                    "time": "10:00",
                    "type": "consultation",
                    "status": "scheduled"
                },
                {
                    "id": "A002",
                    "patient_id": "P002",
                    "doctor_id": "D002",
                    "date": "2024-02-01", 
                    "time": "11:30",
                    "type": "follow-up",
                    "status": "scheduled"
                },
                {
                    "id": "A003",
                    "patient_id": "P003",
                    "doctor_id": "D001",
                    "date": "2024-02-02",
                    "time": "09:00", 
                    "type": "emergency",
                    "status": "scheduled"
                },
                {
                    "id": "A004",
                    "patient_id": "P004",
                    "doctor_id": "D003",
                    "date": "2024-02-02",
                    "time": "14:00",
                    "type": "consultation", 
                    "status": "scheduled"
                },
                {
                    "id": "A005",
                    "patient_id": "P005",
                    "doctor_id": "D004",
                    "date": "2024-02-03",
                    "time": "15:30",
                    "type": "follow-up",
                    "status": "scheduled"
                }
            ]
            self.wfile.write(json.dumps(appointments, indent=2).encode())
            
        elif self.path == '/api/analytics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            analytics = {
                "patient_stats": {
                    "total_patients": 1250,
                    "active_patients": 1180,
                    "critical_patients": 45,
                    "new_patients_this_month": 85
                },
                "appointment_stats": {
                    "total_appointments": 2850,
                    "scheduled_appointments": 2450,
                    "completed_appointments": 2350,
                    "cancelled_appointments": 50
                },
                "revenue_stats": {
                    "total_revenue": 2500000,
                    "monthly_revenue": 185000,
                    "average_appointment_cost": 850
                },
                "doctor_stats": {
                    "total_doctors": 25,
                    "active_doctors": 23,
                    "average_patients_per_doctor": 50
                },
                "system_stats": {
                    "uptime": "99.9%",
                    "api_response_time": "< 200ms",
                    "last_updated": datetime.now().isoformat()
                }
            }
            self.wfile.write(json.dumps(analytics, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "error": "Endpoint not found",
                "path": self.path,
                "available_endpoints": [
                    "/",
                    "/health", 
                    "/api/patients",
                    "/api/doctors",
                    "/api/appointments",
                    "/api/analytics"
                ]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare API Server on port {PORT}...")
    print(f"✅ Server will be available at http://localhost:{PORT}")
    print("📋 Available endpoints:")
    print("   - GET / - API information")
    print("   - GET /health - Health check")
    print("   - GET /api/patients - Patient list")
    print("   - GET /api/doctors - Doctor list")
    print("   - GET /api/appointments - Appointment list")
    print("   - GET /api/analytics - Analytics data")
    print("🛑 Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), EHBAPIHandler) as httpd:
        print(f"✅ API server running at http://localhost:{PORT}")
        httpd.serve_forever() 