#!/usr/bin/env python3
"""
EHB Healthcare System - Simple Test Server
Quick HTTP server for testing
"""

import http.server
import socketserver
import json
import os
from pathlib import Path

PORT = 8000

class EHBHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API is running!",
                "status": "operational",
                "service": "EHB Healthcare System",
                "version": "2.0.0"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "EHB Healthcare API",
                "timestamp": "2024-01-21T01:30:00Z"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/api/patients':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            patients = [
                {"id": "P001", "name": "Ahmed Khan", "status": "active", "condition": "Hypertension"},
                {"id": "P002", "name": "Fatima Ali", "status": "active", "condition": "Diabetes Type 2"},
                {"id": "P003", "name": "Muhammad Hassan", "status": "critical", "condition": "Heart Disease"},
                {"id": "P004", "name": "Ayesha Malik", "status": "active", "condition": "Asthma"},
                {"id": "P005", "name": "Omar Farooq", "status": "active", "condition": "Back Pain"}
            ]
            self.wfile.write(json.dumps(patients, indent=2).encode())
            
        elif self.path == '/api/doctors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            doctors = [
                {"id": "D001", "name": "Dr. Sarah Ahmed", "specialization": "Cardiology", "status": "active"},
                {"id": "D002", "name": "Dr. Ali Hassan", "specialization": "Endocrinology", "status": "active"},
                {"id": "D003", "name": "Dr. Fatima Khan", "specialization": "Pediatrics", "status": "active"},
                {"id": "D004", "name": "Dr. Omar Malik", "specialization": "Orthopedics", "status": "active"},
                {"id": "D005", "name": "Dr. Ayesha Ali", "specialization": "Neurology", "status": "active"}
            ]
            self.wfile.write(json.dumps(doctors, indent=2).encode())
            
        elif self.path == '/api/appointments':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            appointments = [
                {"id": "A001", "patient_id": "P001", "doctor_id": "D001", "status": "scheduled", "date": "2024-02-01"},
                {"id": "A002", "patient_id": "P002", "doctor_id": "D002", "status": "scheduled", "date": "2024-02-01"},
                {"id": "A003", "patient_id": "P003", "doctor_id": "D001", "status": "scheduled", "date": "2024-02-02"},
                {"id": "A004", "patient_id": "P004", "doctor_id": "D003", "status": "scheduled", "date": "2024-02-02"},
                {"id": "A005", "patient_id": "P005", "doctor_id": "D004", "status": "scheduled", "date": "2024-02-03"}
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
                }
            }
            self.wfile.write(json.dumps(analytics, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": self.path}
            self.wfile.write(json.dumps(response, indent=2).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare HTTP Server on port {PORT}...")
    print(f"✅ Server will be available at http://localhost:{PORT}")
    print("📋 Available endpoints:")
    print("   - GET / - System status")
    print("   - GET /health - Health check")
    print("   - GET /api/patients - Patient list")
    print("   - GET /api/doctors - Doctor list")
    print("   - GET /api/appointments - Appointment list")
    print("   - GET /api/analytics - Analytics data")
    print("🛑 Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), EHBHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        httpd.serve_forever() 