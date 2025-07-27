"""
Database Configuration Module
Handles database connections and configurations for healthcare system
"""

import os
from datetime import datetime
from typing import Optional

from sqlalchemy import (Boolean, Column, DateTime, Integer, String, Text,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ehb_healthcare.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_recycle=300
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Database models
class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    allergies = Column(Text)  # JSON string
    conditions = Column(Text)  # JSON string
    medications = Column(Text)  # JSON string
    status = Column(String, default="active")
    last_visit = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, nullable=False)
    rating = Column(Integer, default=5)
    status = Column(String, default="active")
    availability = Column(String, default="available")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, nullable=False)
    doctor_id = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    doctor_name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    type = Column(String, default="in-person")
    status = Column(String, default="scheduled")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, nullable=False)
    doctor_id = Column(String, nullable=False)
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    prescription = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, nullable=False)
    doctor_id = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    doctor_name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    type = Column(String, default="video")
    status = Column(String, default="scheduled")
    duration = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # admin, doctor, patient
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

# Database utilities
def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all tables"""
    Base.metadata.drop_all(bind=engine)

def reset_database():
    """Reset database (drop and recreate all tables)"""
    drop_tables()
    create_tables()

# Health check
def check_database_health():
    """Check database connectivity"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

# Sample data insertion
def insert_sample_data():
    """Insert sample data for development"""
    db = SessionLocal()
    
    try:
        # Sample patients
        patients = [
            Patient(
                id="P001",
                name="John Doe",
                age=45,
                gender="male",
                contact="+1-555-0123",
                email="john.doe@email.com",
                blood_type="A+",
                allergies='["Penicillin", "Peanuts"]',
                conditions='["Hypertension", "Diabetes Type 2"]',
                medications='["Metformin", "Lisinopril"]',
                status="active"
            ),
            Patient(
                id="P002",
                name="Jane Smith",
                age=32,
                gender="female",
                contact="+1-555-0124",
                email="jane.smith@email.com",
                blood_type="O-",
                allergies='["Latex"]',
                conditions='["Asthma"]',
                medications='["Albuterol"]',
                status="active"
            )
        ]
        
        # Sample doctors
        doctors = [
            Doctor(
                id="D001",
                name="Dr. Sarah Wilson",
                specialization="Cardiology",
                contact="+1-555-0201",
                email="sarah.wilson@ehb.com",
                rating=4.8,
                status="active"
            ),
            Doctor(
                id="D002",
                name="Dr. Michael Brown",
                specialization="Neurology",
                contact="+1-555-0202",
                email="michael.brown@ehb.com",
                rating=4.9,
                status="active"
            )
        ]
        
        # Add to database
        for patient in patients:
            db.add(patient)
        
        for doctor in doctors:
            db.add(doctor)
        
        db.commit()
        print("✅ Sample data inserted successfully")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize database
    init_db()
    print("✅ Database initialized successfully")
    
    # Insert sample data
    insert_sample_data() 