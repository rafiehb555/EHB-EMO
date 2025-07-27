"""
Analytics Routes Module
Handles all analytics and reporting API endpoints
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# Analytics models
class AnalyticsOverview(BaseModel):
    total_patients: int
    active_patients: int
    total_appointments: int
    completed_appointments: int
    total_revenue: float
    patient_satisfaction: float
    system_uptime: float

class PerformanceMetrics(BaseModel):
    appointment_completion_rate: float
    average_wait_time: float
    patient_retention_rate: float
    doctor_utilization_rate: float

# Sample data for analytics
patients_data = [
    {"id": "P001", "name": "John Doe", "status": "active", "created_at": "2024-01-01"},
    {"id": "P002", "name": "Jane Smith", "status": "active", "created_at": "2024-01-02"},
    {"id": "P003", "name": "Mike Johnson", "status": "active", "created_at": "2024-01-03"}
]

appointments_data = [
    {"id": "A001", "status": "completed", "date": "2024-01-15", "revenue": 150.0},
    {"id": "A002", "status": "scheduled", "date": "2024-01-16", "revenue": 0.0},
    {"id": "A003", "status": "completed", "date": "2024-01-14", "revenue": 200.0}
]

doctors_data = [
    {"id": "D001", "name": "Dr. Sarah Wilson", "specialization": "Cardiology", "rating": 4.8},
    {"id": "D002", "name": "Dr. Michael Brown", "specialization": "Neurology", "rating": 4.9},
    {"id": "D003", "name": "Dr. Emily Davis", "specialization": "Pediatrics", "rating": 4.7}
]

@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview():
    """Get overall analytics overview"""
    total_patients = len(patients_data)
    active_patients = len([p for p in patients_data if p["status"] == "active"])
    total_appointments = len(appointments_data)
    completed_appointments = len([a for a in appointments_data if a["status"] == "completed"])
    total_revenue = sum(a["revenue"] for a in appointments_data if a["status"] == "completed")
    
    return AnalyticsOverview(
        total_patients=total_patients,
        active_patients=active_patients,
        total_appointments=total_appointments,
        completed_appointments=completed_appointments,
        total_revenue=total_revenue,
        patient_satisfaction=94.5,
        system_uptime=99.9
    )

@router.get("/performance", response_model=PerformanceMetrics)
async def get_performance_metrics():
    """Get performance metrics"""
    total_appointments = len(appointments_data)
    completed_appointments = len([a for a in appointments_data if a["status"] == "completed"])
    
    completion_rate = (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0
    
    return PerformanceMetrics(
        appointment_completion_rate=completion_rate,
        average_wait_time=15.5,  # minutes
        patient_retention_rate=87.3,
        doctor_utilization_rate=92.1
    )

@router.get("/revenue")
async def get_revenue_analytics():
    """Get revenue analytics"""
    total_revenue = sum(a["revenue"] for a in appointments_data if a["status"] == "completed")
    monthly_revenue = total_revenue  # Simplified for demo
    
    return {
        "total_revenue": total_revenue,
        "monthly_revenue": monthly_revenue,
        "revenue_trend": "+12.5%",
        "top_services": [
            {"service": "Cardiology Consultation", "revenue": 5000.0},
            {"service": "Neurology Consultation", "revenue": 4500.0},
            {"service": "Pediatrics Consultation", "revenue": 3000.0}
        ],
        "revenue_by_month": [
            {"month": "January", "revenue": 125000.0},
            {"month": "December", "revenue": 110000.0},
            {"month": "November", "revenue": 105000.0}
        ]
    }

@router.get("/patients")
async def get_patient_analytics():
    """Get patient analytics"""
    total_patients = len(patients_data)
    active_patients = len([p for p in patients_data if p["status"] == "active"])
    
    # Age distribution (simulated)
    age_distribution = {
        "18-30": 25,
        "31-45": 35,
        "46-60": 30,
        "60+": 10
    }
    
    # Gender distribution (simulated)
    gender_distribution = {
        "male": 45,
        "female": 55
    }
    
    return {
        "total_patients": total_patients,
        "active_patients": active_patients,
        "new_patients_this_month": 15,
        "patient_growth_rate": "+8.5%",
        "age_distribution": age_distribution,
        "gender_distribution": gender_distribution,
        "top_conditions": [
            {"condition": "Hypertension", "count": 45},
            {"condition": "Diabetes", "count": 32},
            {"condition": "Asthma", "count": 28}
        ]
    }

@router.get("/appointments")
async def get_appointment_analytics():
    """Get appointment analytics"""
    total_appointments = len(appointments_data)
    completed_appointments = len([a for a in appointments_data if a["status"] == "completed"])
    scheduled_appointments = len([a for a in appointments_data if a["status"] == "scheduled"])
    
    return {
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "scheduled_appointments": scheduled_appointments,
        "completion_rate": (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0,
        "average_appointments_per_day": 8.5,
        "appointment_types": {
            "in_person": 65,
            "video": 35
        },
        "peak_hours": [
            {"hour": "9:00 AM", "appointments": 12},
            {"hour": "10:00 AM", "appointments": 15},
            {"hour": "2:00 PM", "appointments": 18}
        ]
    }

@router.get("/doctors")
async def get_doctor_analytics():
    """Get doctor analytics"""
    total_doctors = len(doctors_data)
    average_rating = sum(d["rating"] for d in doctors_data) / len(doctors_data) if doctors_data else 0
    
    return {
        "total_doctors": total_doctors,
        "average_rating": average_rating,
        "top_doctors": [
            {"name": "Dr. Michael Brown", "rating": 4.9, "appointments": 156},
            {"name": "Dr. Sarah Wilson", "rating": 4.8, "appointments": 142},
            {"name": "Dr. Emily Davis", "rating": 4.7, "appointments": 128}
        ],
        "specialization_distribution": {
            "Cardiology": 25,
            "Neurology": 20,
            "Pediatrics": 30,
            "Orthopedics": 15,
            "Dermatology": 10
        },
        "utilization_rates": [
            {"doctor": "Dr. Sarah Wilson", "utilization": 95},
            {"doctor": "Dr. Michael Brown", "utilization": 88},
            {"doctor": "Dr. Emily Davis", "utilization": 92}
        ]
    }

@router.get("/system")
async def get_system_analytics():
    """Get system performance analytics"""
    return {
        "system_uptime": 99.9,
        "average_response_time": 150,  # milliseconds
        "active_sessions": 45,
        "database_performance": {
            "read_latency": 5.2,
            "write_latency": 8.1,
            "connection_pool": 85
        },
        "security_metrics": {
            "failed_login_attempts": 3,
            "security_incidents": 0,
            "data_breaches": 0
        },
        "api_performance": {
            "requests_per_minute": 120,
            "average_response_time": 150,
            "error_rate": 0.1
        }
    }

@router.get("/trends")
async def get_trend_analytics():
    """Get trend analytics"""
    return {
        "patient_growth": [
            {"month": "Jan", "patients": 1200},
            {"month": "Feb", "patients": 1250},
            {"month": "Mar", "patients": 1300}
        ],
        "revenue_trend": [
            {"month": "Jan", "revenue": 110000},
            {"month": "Feb", "revenue": 115000},
            {"month": "Mar", "revenue": 125000}
        ],
        "appointment_trend": [
            {"month": "Jan", "appointments": 850},
            {"month": "Feb", "appointments": 920},
            {"month": "Mar", "appointments": 980}
        ],
        "satisfaction_trend": [
            {"month": "Jan", "satisfaction": 92.5},
            {"month": "Feb", "satisfaction": 93.1},
            {"month": "Mar", "satisfaction": 94.5}
        ]
    }

@router.get("/reports/{report_type}")
async def get_analytics_report(report_type: str):
    """Get specific analytics reports"""
    if report_type == "monthly":
        return {
            "report_type": "Monthly Report",
            "period": "January 2024",
            "summary": {
                "total_patients": 1247,
                "new_patients": 45,
                "total_appointments": 156,
                "total_revenue": 125000,
                "patient_satisfaction": 94.5
            },
            "highlights": [
                "15% increase in new patient registrations",
                "8% improvement in appointment completion rate",
                "12% increase in monthly revenue"
            ]
        }
    elif report_type == "quarterly":
        return {
            "report_type": "Quarterly Report",
            "period": "Q4 2023",
            "summary": {
                "total_patients": 3800,
                "new_patients": 180,
                "total_appointments": 450,
                "total_revenue": 350000,
                "patient_satisfaction": 93.8
            },
            "highlights": [
                "20% increase in quarterly revenue",
                "Improved patient satisfaction scores",
                "Expanded telemedicine services"
            ]
        }
    else:
        raise HTTPException(status_code=404, detail="Report type not found") 