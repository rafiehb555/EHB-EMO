#!/usr/bin/env python3
"""
EHB Missing Data Creator
Creates missing data, components, and configurations for the healthcare system
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path


class EHBDataCreator:
    def __init__(self):
        self.project_root = Path.cwd()
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)

    def create_patient_data(self):
        """Create sample patient data"""
        print("👥 Creating patient data...")
        
        patients = []
        names = [
            "Ahmed Khan", "Fatima Ali", "Muhammad Hassan", "Aisha Rahman",
            "Omar Malik", "Zara Ahmed", "Yusuf Khan", "Layla Hassan",
            "Ibrahim Ali", "Noor Fatima", "Khalid Rahman", "Amina Malik",
            "Hassan Ahmed", "Mariam Khan", "Ali Hassan", "Sara Rahman"
        ]
        
        conditions = [
            "Hypertension", "Diabetes Type 2", "Asthma", "Heart Disease",
            "Arthritis", "Depression", "Anxiety", "Obesity",
            "High Cholesterol", "Migraine", "Insomnia", "Back Pain"
        ]
        
        for i in range(50):
            patient = {
                "id": f"P{i+1:04d}",
                "name": random.choice(names),
                "age": random.randint(18, 85),
                "gender": random.choice(["Male", "Female"]),
                "phone": f"+92-{random.randint(300, 399)}-{random.randint(1000000, 9999999)}",
                "email": f"patient{i+1}@example.com",
                "address": f"House {random.randint(1, 100)}, Street {random.randint(1, 50)}, Karachi",
                "blood_type": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                "emergency_contact": f"+92-{random.randint(300, 399)}-{random.randint(1000000, 9999999)}",
                "medical_history": random.sample(conditions, random.randint(1, 3)),
                "allergies": random.choice([["Penicillin"], ["Latex"], ["Peanuts"], [], ["Dairy"]]),
                "insurance_provider": random.choice(["State Life", "EFU", "Adamjee", "Jubilee", "Takaful"]),
                "insurance_number": f"INS-{random.randint(100000, 999999)}",
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "last_visit": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                "status": random.choice(["Active", "Inactive", "Emergency"])
            }
            patients.append(patient)
        
        with open(self.data_dir / "patients.json", "w", encoding="utf-8") as f:
            json.dump(patients, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(patients)} patient records")

    def create_doctor_data(self):
        """Create sample doctor data"""
        print("👨‍⚕️ Creating doctor data...")
        
        doctors = []
        names = [
            "Dr. Sarah Johnson", "Dr. Ahmed Malik", "Dr. Fatima Hassan",
            "Dr. Michael Chen", "Dr. Aisha Rahman", "Dr. David Wilson",
            "Dr. Mariam Khan", "Dr. James Brown", "Dr. Zara Ahmed",
            "Dr. Robert Davis", "Dr. Layla Hassan", "Dr. Emily White"
        ]
        
        specializations = [
            "Cardiology", "Neurology", "Orthopedics", "Pediatrics",
            "Dermatology", "Psychiatry", "Oncology", "Endocrinology",
            "Gastroenterology", "Pulmonology", "Rheumatology", "Urology"
        ]
        
        for i in range(20):
            doctor = {
                "id": f"D{i+1:03d}",
                "name": random.choice(names),
                "specialization": random.choice(specializations),
                "qualification": random.choice(["MBBS", "MD", "PhD", "FCPS"]),
                "experience_years": random.randint(5, 25),
                "phone": f"+92-{random.randint(300, 399)}-{random.randint(1000000, 9999999)}",
                "email": f"doctor{i+1}@ehb.com",
                "license_number": f"MED-{random.randint(10000, 99999)}",
                "availability": random.choice(["Full-time", "Part-time", "Consultant"]),
                "rating": round(random.uniform(4.0, 5.0), 1),
                "patients_count": random.randint(50, 500),
                "consultation_fee": random.randint(1000, 5000),
                "languages": random.sample(["English", "Urdu", "Arabic", "Punjabi"], random.randint(1, 3)),
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "status": random.choice(["Active", "On Leave", "Retired"])
            }
            doctors.append(doctor)
        
        with open(self.data_dir / "doctors.json", "w", encoding="utf-8") as f:
            json.dump(doctors, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(doctors)} doctor records")

    def create_appointment_data(self):
        """Create sample appointment data"""
        print("📅 Creating appointment data...")
        
        appointments = []
        statuses = ["Scheduled", "Completed", "Cancelled", "No-show", "Rescheduled"]
        
        for i in range(100):
            appointment_date = datetime.now() + timedelta(days=random.randint(-30, 60))
            appointment = {
                "id": f"APT{i+1:04d}",
                "patient_id": f"P{random.randint(1, 50):04d}",
                "doctor_id": f"D{random.randint(1, 20):03d}",
                "appointment_date": appointment_date.isoformat(),
                "appointment_time": f"{random.randint(9, 17):02d}:{random.randint(0, 5):01d}0",
                "duration_minutes": random.choice([15, 30, 45, 60]),
                "type": random.choice(["Consultation", "Follow-up", "Emergency", "Routine Checkup"]),
                "status": random.choice(statuses),
                "notes": random.choice([
                    "Regular checkup", "Follow-up for previous condition",
                    "New symptoms reported", "Emergency consultation",
                    "Routine blood work", "Prescription renewal"
                ]),
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "fee": random.randint(500, 3000),
                "payment_status": random.choice(["Paid", "Pending", "Insurance"])
            }
            appointments.append(appointment)
        
        with open(self.data_dir / "appointments.json", "w", encoding="utf-8") as f:
            json.dump(appointments, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(appointments)} appointment records")

    def create_medical_records(self):
        """Create sample medical records"""
        print("📋 Creating medical records...")
        
        records = []
        diagnoses = [
            "Hypertension", "Type 2 Diabetes", "Asthma", "Coronary Artery Disease",
            "Depression", "Anxiety Disorder", "Osteoarthritis", "Migraine",
            "Insomnia", "Gastroesophageal Reflux Disease", "Chronic Back Pain",
            "Allergic Rhinitis", "Urinary Tract Infection", "Pneumonia"
        ]
        
        treatments = [
            "Medication prescribed", "Lifestyle modification", "Physical therapy",
            "Surgery recommended", "Counseling", "Dietary changes",
            "Exercise program", "Regular monitoring", "Referral to specialist"
        ]
        
        for i in range(200):
            record = {
                "id": f"MR{i+1:05d}",
                "patient_id": f"P{random.randint(1, 50):04d}",
                "doctor_id": f"D{random.randint(1, 20):03d}",
                "visit_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "chief_complaint": random.choice([
                    "Headache", "Chest pain", "Shortness of breath", "Fever",
                    "Cough", "Back pain", "Joint pain", "Fatigue",
                    "Dizziness", "Nausea", "Abdominal pain", "Insomnia"
                ]),
                "diagnosis": random.choice(diagnoses),
                "treatment": random.choice(treatments),
                "medications": random.sample([
                    "Paracetamol", "Ibuprofen", "Omeprazole", "Metformin",
                    "Amlodipine", "Atorvastatin", "Sertraline", "Albuterol"
                ], random.randint(1, 3)),
                "vital_signs": {
                    "blood_pressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
                    "heart_rate": random.randint(60, 100),
                    "temperature": round(random.uniform(36.5, 37.5), 1),
                    "weight_kg": round(random.uniform(50, 100), 1),
                    "height_cm": random.randint(150, 190)
                },
                "lab_results": random.choice([
                    {"blood_sugar": random.randint(80, 200), "cholesterol": random.randint(150, 300)},
                    {"hemoglobin": round(random.uniform(12, 16), 1), "platelets": random.randint(150000, 450000)},
                    {"creatinine": round(random.uniform(0.6, 1.2), 2), "urea": random.randint(7, 20)}
                ]),
                "next_follow_up": (datetime.now() + timedelta(days=random.randint(7, 90))).isoformat(),
                "notes": random.choice([
                    "Patient responding well to treatment",
                    "Continue current medication",
                    "Monitor symptoms closely",
                    "Schedule follow-up in 2 weeks",
                    "Consider alternative treatment"
                ])
            }
            records.append(record)
        
        with open(self.data_dir / "medical_records.json", "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(records)} medical records")

    def create_pharmacy_data(self):
        """Create sample pharmacy data"""
        print("💊 Creating pharmacy data...")
        
        pharmacies = []
        names = [
            "MedPlus Pharmacy", "HealthCare Pharmacy", "LifeCare Pharmacy",
            "Wellness Pharmacy", "CareFirst Pharmacy", "MediCare Pharmacy",
            "HealthFirst Pharmacy", "CarePlus Pharmacy", "WellCare Pharmacy",
            "MediPlus Pharmacy"
        ]
        
        for i in range(10):
            pharmacy = {
                "id": f"PH{i+1:02d}",
                "name": names[i],
                "address": f"Shop {random.randint(1, 50)}, Block {random.randint(1, 20)}, Karachi",
                "phone": f"+92-{random.randint(300, 399)}-{random.randint(1000000, 9999999)}",
                "email": f"pharmacy{i+1}@example.com",
                "license_number": f"PHARM-{random.randint(10000, 99999)}",
                "operating_hours": "09:00-22:00",
                "services": random.sample([
                    "Prescription dispensing", "Over-the-counter medicines",
                    "Health consultations", "Vaccination", "Medical supplies",
                    "Home delivery", "Emergency services"
                ], random.randint(4, 7)),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "delivery_available": random.choice([True, False]),
                "emergency_services": random.choice([True, False]),
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "status": "Active"
            }
            pharmacies.append(pharmacy)
        
        with open(self.data_dir / "pharmacies.json", "w", encoding="utf-8") as f:
            json.dump(pharmacies, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(pharmacies)} pharmacy records")

    def create_insurance_data(self):
        """Create sample insurance data"""
        print("🛡️ Creating insurance data...")
        
        insurance_policies = []
        providers = [
            "State Life Insurance", "EFU Life Insurance", "Adamjee Insurance",
            "Jubilee Life Insurance", "Takaful Pakistan", "Pak-Qatar Insurance"
        ]
        
        plan_types = [
            "Basic Health", "Premium Health", "Family Health", "Senior Health",
            "Critical Illness", "Maternity", "Dental", "Vision"
        ]
        
        for i in range(100):
            policy = {
                "id": f"POL{i+1:05d}",
                "patient_id": f"P{random.randint(1, 50):04d}",
                "provider": random.choice(providers),
                "plan_type": random.choice(plan_types),
                "policy_number": f"POL-{random.randint(100000, 999999)}",
                "start_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
                "end_date": (datetime.now() + timedelta(days=random.randint(30, 365))).isoformat(),
                "premium_amount": random.randint(5000, 50000),
                "coverage_amount": random.randint(100000, 1000000),
                "deductible": random.randint(5000, 50000),
                "coverage_details": random.choice([
                    "Inpatient and outpatient care",
                    "Prescription drugs coverage",
                    "Dental and vision care",
                    "Mental health services",
                    "Emergency services",
                    "Preventive care"
                ]),
                "status": random.choice(["Active", "Expired", "Suspended", "Pending"]),
                "renewal_date": (datetime.now() + timedelta(days=random.randint(1, 365))).isoformat(),
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
            }
            insurance_policies.append(policy)
        
        with open(self.data_dir / "insurance_policies.json", "w", encoding="utf-8") as f:
            json.dump(insurance_policies, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(insurance_policies)} insurance policy records")

    def create_analytics_data(self):
        """Create sample analytics data"""
        print("📊 Creating analytics data...")
        
        analytics = {
            "system_metrics": {
                "total_patients": 50,
                "total_doctors": 20,
                "total_appointments": 100,
                "total_medical_records": 200,
                "total_pharmacies": 10,
                "total_insurance_policies": 100,
                "system_uptime": "99.9%",
                "average_response_time": "150ms",
                "active_users": random.randint(50, 200),
                "daily_appointments": random.randint(20, 50)
            },
            "healthcare_metrics": {
                "patient_satisfaction": round(random.uniform(4.0, 5.0), 1),
                "treatment_success_rate": round(random.uniform(85, 95), 1),
                "average_wait_time": f"{random.randint(10, 30)} minutes",
                "emergency_response_time": f"{random.randint(5, 15)} minutes",
                "readmission_rate": round(random.uniform(5, 15), 1),
                "medication_adherence": round(random.uniform(70, 90), 1)
            },
            "financial_metrics": {
                "total_revenue": random.randint(5000000, 20000000),
                "average_consultation_fee": random.randint(1000, 3000),
                "insurance_claims_processed": random.randint(1000, 5000),
                "payment_collection_rate": round(random.uniform(85, 98), 1),
                "operational_costs": random.randint(2000000, 8000000),
                "profit_margin": round(random.uniform(15, 35), 1)
            },
            "compliance_metrics": {
                "hipaa_compliance": "100%",
                "data_encryption": "AES-256",
                "audit_logs": "Complete",
                "access_controls": "Active",
                "backup_frequency": "Daily",
                "security_incidents": 0
            }
        }
        
        with open(self.data_dir / "analytics.json", "w", encoding="utf-8") as f:
            json.dump(analytics, f, indent=2, ensure_ascii=False)
        
        print("✅ Created analytics data")

    def create_config_files(self):
        """Create configuration files"""
        print("⚙️ Creating configuration files...")
        
        # Database configuration
        db_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "ehb_healthcare",
                "user": "ehb_user",
                "password": "secure_password_123",
                "pool_size": 10,
                "max_overflow": 20
            },
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0,
                "password": None
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": True,
                "cors_origins": ["http://localhost:3000", "http://127.0.0.1:3000"]
            },
            "security": {
                "jwt_secret": "ehb_healthcare_secret_key_2025",
                "jwt_expiry": 3600,
                "password_salt_rounds": 12,
                "session_timeout": 1800
            },
            "email": {
                "smtp_host": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "noreply@ehb.com",
                "password": "app_password_here"
            },
            "sms": {
                "provider": "twilio",
                "account_sid": "your_account_sid",
                "auth_token": "your_auth_token",
                "from_number": "+1234567890"
            }
        }
        
        with open(self.data_dir / "config.json", "w", encoding="utf-8") as f:
            json.dump(db_config, f, indent=2, ensure_ascii=False)
        
        # API endpoints configuration
        api_endpoints = {
            "endpoints": {
                "auth": {
                    "login": "/api/auth/login",
                    "register": "/api/auth/register",
                    "logout": "/api/auth/logout",
                    "refresh": "/api/auth/refresh"
                },
                "patients": {
                    "list": "/api/patients",
                    "create": "/api/patients",
                    "get": "/api/patients/{id}",
                    "update": "/api/patients/{id}",
                    "delete": "/api/patients/{id}"
                },
                "doctors": {
                    "list": "/api/doctors",
                    "create": "/api/doctors",
                    "get": "/api/doctors/{id}",
                    "update": "/api/doctors/{id}",
                    "delete": "/api/doctors/{id}"
                },
                "appointments": {
                    "list": "/api/appointments",
                    "create": "/api/appointments",
                    "get": "/api/appointments/{id}",
                    "update": "/api/appointments/{id}",
                    "delete": "/api/appointments/{id}"
                },
                "medical_records": {
                    "list": "/api/medical-records",
                    "create": "/api/medical-records",
                    "get": "/api/medical-records/{id}",
                    "update": "/api/medical-records/{id}",
                    "delete": "/api/medical-records/{id}"
                },
                "analytics": {
                    "dashboard": "/api/analytics/dashboard",
                    "metrics": "/api/analytics/metrics",
                    "reports": "/api/analytics/reports"
                }
            }
        }
        
        with open(self.data_dir / "api_endpoints.json", "w", encoding="utf-8") as f:
            json.dump(api_endpoints, f, indent=2, ensure_ascii=False)
        
        print("✅ Created configuration files")

    def create_all_data(self):
        """Create all missing data"""
        print("=" * 60)
        print("🏥 EHB Healthcare System - Data Creation")
        print("=" * 60)
        
        self.create_patient_data()
        self.create_doctor_data()
        self.create_appointment_data()
        self.create_medical_records()
        self.create_pharmacy_data()
        self.create_insurance_data()
        self.create_analytics_data()
        self.create_config_files()
        
        print("=" * 60)
        print("✅ All missing data created successfully!")
        print(f"📁 Data saved in: {self.data_dir}")
        print("=" * 60)

def main():
    """Main function"""
    creator = EHBDataCreator()
    creator.create_all_data()

if __name__ == "__main__":
    main() 