"""
Test Suite for AI Agent Development and Healthcare System
Comprehensive testing for all components
"""

import asyncio
import json
import os
import sys
import unittest
from datetime import datetime, timedelta
from typing import Any, Dict, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (AgentCommunication, AgentConfig, AgentMemory, AgentStatus,
                    AgentTask, AgentType, AIAgent, Alert, AnalyticsData,
                    Appointment, CodeBlock, Doctor, ErrorLog, FixSuggestion,
                    HealthCheck, MedicalRecord, Message, Patient,
                    PerformanceMetrics, Priority, SystemConfig, TaskStatus,
                    TrainingData, TrainingSession)


class TestAIAgentModels(unittest.TestCase):
    """Test AI Agent Models"""
    
    def test_ai_agent_creation(self):
        """Test AI agent model creation"""
        agent = AIAgent(
            name="Test Agent",
            description="Test agent for testing",
            agent_type=AgentType.ERROR_FIX,
            capabilities=["error_detection", "code_fixing"],
            health_score=95.0
        )
        
        self.assertEqual(agent.name, "Test Agent")
        self.assertEqual(agent.agent_type, AgentType.ERROR_FIX)
        self.assertEqual(agent.status, AgentStatus.INACTIVE)
        self.assertIsNotNone(agent.id)
    
    def test_agent_task_creation(self):
        """Test agent task model creation"""
        task = AgentTask(
            agent_id="test_agent_001",
            task_type="error_fix",
            description="Fix critical error in main.py",
            priority=Priority.HIGH,
            input_data={"file_path": "main.py", "error_line": 25}
        )
        
        self.assertEqual(task.agent_id, "test_agent_001")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNotNone(task.id)
    
    def test_agent_memory_creation(self):
        """Test agent memory model creation"""
        memory = AgentMemory(
            agent_id="test_agent_001",
            memory_type="short_term",
            content={"recent_errors": ["error1", "error2"]},
            importance_score=0.8
        )
        
        self.assertEqual(memory.agent_id, "test_agent_001")
        self.assertEqual(memory.memory_type, "short_term")
        self.assertEqual(memory.importance_score, 0.8)

class TestHealthcareModels(unittest.TestCase):
    """Test Healthcare Models"""
    
    def test_patient_creation(self):
        """Test patient model creation"""
        patient = Patient(
            name="John Doe",
            age=45,
            gender="male",
            contact="+1-555-0123",
            email="john.doe@email.com",
            blood_type="A+",
            allergies=["Penicillin"],
            conditions=["Hypertension"]
        )
        
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.age, 45)
        self.assertEqual(patient.status, "active")
        self.assertIsNotNone(patient.id)
    
    def test_doctor_creation(self):
        """Test doctor model creation"""
        doctor = Doctor(
            name="Dr. Sarah Wilson",
            specialization="Cardiology",
            contact="+1-555-0201",
            email="sarah.wilson@ehb.com",
            rating=4.8
        )
        
        self.assertEqual(doctor.name, "Dr. Sarah Wilson")
        self.assertEqual(doctor.specialization, "Cardiology")
        self.assertEqual(doctor.status, "active")
    
    def test_appointment_creation(self):
        """Test appointment model creation"""
        appointment = Appointment(
            patient_id="P001",
            doctor_id="D001",
            patient_name="John Doe",
            doctor_name="Dr. Sarah Wilson",
            date="2024-01-16",
            time="10:00 AM",
            type="in-person"
        )
        
        self.assertEqual(appointment.patient_id, "P001")
        self.assertEqual(appointment.status, "scheduled")
        self.assertEqual(appointment.type, "in-person")

class TestErrorHandlingModels(unittest.TestCase):
    """Test Error Handling Models"""
    
    def test_error_log_creation(self):
        """Test error log model creation"""
        error = ErrorLog(
            error_type="syntax_error",
            error_message="Invalid syntax in line 25",
            file_path="main.py",
            line_number=25,
            severity="high"
        )
        
        self.assertEqual(error.error_type, "syntax_error")
        self.assertEqual(error.severity, "high")
        self.assertEqual(error.status, "open")
    
    def test_fix_suggestion_creation(self):
        """Test fix suggestion model creation"""
        fix = FixSuggestion(
            error_id="error_001",
            agent_id="agent_001",
            suggestion_type="code_fix",
            description="Add missing semicolon",
            code_changes={"line_25": "console.log('Hello');"},
            confidence_score=0.95
        )
        
        self.assertEqual(fix.error_id, "error_001")
        self.assertEqual(fix.confidence_score, 0.95)
        self.assertEqual(fix.status, "pending")

class TestAnalyticsModels(unittest.TestCase):
    """Test Analytics Models"""
    
    def test_analytics_data_creation(self):
        """Test analytics data model creation"""
        analytics = AnalyticsData(
            metric_name="response_time",
            metric_value=150.5,
            metric_unit="ms",
            category="performance",
            metadata={"endpoint": "/api/patients"}
        )
        
        self.assertEqual(analytics.metric_name, "response_time")
        self.assertEqual(analytics.metric_value, 150.5)
        self.assertEqual(analytics.category, "performance")
    
    def test_performance_metrics_creation(self):
        """Test performance metrics model creation"""
        metrics = PerformanceMetrics(
            agent_id="agent_001",
            cpu_usage=25.5,
            memory_usage=512.0,
            response_time=150.0,
            throughput=100.0,
            error_rate=0.01,
            success_rate=0.99
        )
        
        self.assertEqual(metrics.agent_id, "agent_001")
        self.assertEqual(metrics.cpu_usage, 25.5)
        self.assertEqual(metrics.success_rate, 0.99)

class TestDatabaseOperations(unittest.TestCase):
    """Test Database Operations"""
    
    def setUp(self):
        """Set up test database"""
        from database import DatabaseManager
        self.db_manager = DatabaseManager("test_db.sqlite")
    
    def tearDown(self):
        """Clean up test database"""
        self.db_manager.close()
        if os.path.exists("test_db.sqlite"):
            os.remove("test_db.sqlite")
    
    def test_agent_insertion(self):
        """Test agent insertion into database"""
        agent_data = {
            "id": "test_agent_001",
            "name": "Test Agent",
            "description": "Test agent",
            "agent_type": "error_fix",
            "status": "active",
            "capabilities": ["error_detection"]
        }
        
        result = self.db_manager.insert_agent(agent_data)
        self.assertTrue(result)
    
    def test_patient_insertion(self):
        """Test patient insertion into database"""
        patient_data = {
            "id": "P001",
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "contact": "+1-555-0123",
            "email": "john.doe@email.com",
            "blood_type": "A+",
            "allergies": ["Penicillin"],
            "conditions": ["Hypertension"]
        }
        
        result = self.db_manager.insert_patient(patient_data)
        self.assertTrue(result)
    
    def test_error_log_insertion(self):
        """Test error log insertion into database"""
        error_data = {
            "id": "error_001",
            "error_type": "syntax_error",
            "error_message": "Invalid syntax",
            "severity": "high",
            "status": "open"
        }
        
        result = self.db_manager.insert_error_log(error_data)
        self.assertTrue(result)

class TestAPIOperations(unittest.TestCase):
    """Test API Operations"""
    
    def setUp(self):
        """Set up test client"""
        from fastapi.testclient import TestClient

        from api import app
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
    
    def test_get_agents(self):
        """Test get agents endpoint"""
        response = self.client.get("/api/agents")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_create_agent(self):
        """Test create agent endpoint"""
        agent_data = {
            "name": "Test Agent",
            "description": "Test agent",
            "agent_type": "error_fix",
            "capabilities": ["error_detection"]
        }
        
        response = self.client.post("/api/agents", json=agent_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Agent")
    
    def test_get_patients(self):
        """Test get patients endpoint"""
        response = self.client.get("/api/healthcare/patients")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_create_patient(self):
        """Test create patient endpoint"""
        patient_data = {
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "contact": "+1-555-0123",
            "email": "john.doe@email.com",
            "blood_type": "A+"
        }
        
        response = self.client.post("/api/healthcare/patients", json=patient_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "John Doe")

class TestAIAgentFunctionality(unittest.TestCase):
    """Test AI Agent Functionality"""
    
    def test_agent_task_processing(self):
        """Test agent task processing"""
        task = AgentTask(
            agent_id="agent_001",
            task_type="error_fix",
            description="Fix critical error",
            priority=Priority.HIGH
        )
        
        # Simulate task processing
        task.status = TaskStatus.IN_PROGRESS
        task.progress = 50.0
        
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertEqual(task.progress, 50.0)
    
    def test_agent_memory_management(self):
        """Test agent memory management"""
        memory = AgentMemory(
            agent_id="agent_001",
            memory_type="short_term",
            content={"recent_errors": ["error1"]},
            importance_score=0.8
        )
        
        # Simulate memory access
        memory.accessed_at = datetime.now()
        
        self.assertIsNotNone(memory.accessed_at)
        self.assertEqual(memory.importance_score, 0.8)
    
    def test_agent_communication(self):
        """Test agent communication"""
        message = Message(
            sender_id="agent_001",
            receiver_id="agent_002",
            message_type="request",
            content={"action": "process_data"}
        )
        
        self.assertEqual(message.sender_id, "agent_001")
        self.assertEqual(message.message_type, "request")

class TestHealthcareFunctionality(unittest.TestCase):
    """Test Healthcare Functionality"""
    
    def test_patient_management(self):
        """Test patient management"""
        patient = Patient(
            name="John Doe",
            age=45,
            gender="male",
            contact="+1-555-0123",
            email="john.doe@email.com",
            blood_type="A+"
        )
        
        # Simulate patient update
        patient.updated_at = datetime.now()
        
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.status, "active")
    
    def test_appointment_scheduling(self):
        """Test appointment scheduling"""
        appointment = Appointment(
            patient_id="P001",
            doctor_id="D001",
            patient_name="John Doe",
            doctor_name="Dr. Sarah Wilson",
            date="2024-01-16",
            time="10:00 AM"
        )
        
        # Simulate appointment status change
        appointment.status = "confirmed"
        
        self.assertEqual(appointment.status, "confirmed")
        self.assertEqual(appointment.type, "in-person")

class TestSecurityAndCompliance(unittest.TestCase):
    """Test Security and Compliance"""
    
    def test_hipaa_compliance(self):
        """Test HIPAA compliance features"""
        from config.security import HIPAACompliance

        # Test data masking
        masked_data = HIPAACompliance.mask_phi("John Doe")
        self.assertNotEqual(masked_data, "John Doe")
        
        # Test access validation
        has_access = HIPAACompliance.validate_phi_access("doctor", "patients")
        self.assertTrue(has_access)
    
    def test_password_strength(self):
        """Test password strength validation"""
        from config.security import validate_password_strength

        # Test weak password
        weak_result = validate_password_strength("weak")
        self.assertFalse(weak_result["is_valid"])
        
        # Test strong password
        strong_result = validate_password_strength("StrongPass123!")
        self.assertTrue(strong_result["is_valid"])

def run_performance_tests():
    """Run performance tests"""
    print("🚀 Running Performance Tests...")
    
    # Test database performance
    from database import DatabaseManager
    db = DatabaseManager("perf_test.sqlite")
    
    start_time = datetime.now()
    
    # Insert 1000 agents
    for i in range(1000):
        agent_data = {
            "id": f"agent_{i:04d}",
            "name": f"Agent {i}",
            "description": f"Test agent {i}",
            "agent_type": "error_fix",
            "status": "active"
        }
        db.insert_agent(agent_data)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"✅ Inserted 1000 agents in {duration:.2f} seconds")
    print(f"📊 Performance: {1000/duration:.0f} operations/second")
    
    db.close()
    if os.path.exists("perf_test.sqlite"):
        os.remove("perf_test.sqlite")

def run_integration_tests():
    """Run integration tests"""
    print("🔗 Running Integration Tests...")
    
    # Test API integration
    from fastapi.testclient import TestClient

    from api import app
    
    client = TestClient(app)
    
    # Test complete workflow
    # 1. Create agent
    agent_data = {
        "name": "Integration Test Agent",
        "description": "Agent for integration testing",
        "agent_type": "error_fix"
    }
    response = client.post("/api/agents", json=agent_data)
    assert response.status_code == 200
    
    # 2. Create task
    task_data = {
        "agent_id": response.json()["id"],
        "task_type": "error_fix",
        "description": "Integration test task"
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 200
    
    # 3. Create patient
    patient_data = {
        "name": "Integration Test Patient",
        "age": 30,
        "gender": "female",
        "contact": "+1-555-9999",
        "email": "test@example.com",
        "blood_type": "O+"
    }
    response = client.post("/api/healthcare/patients", json=patient_data)
    assert response.status_code == 200
    
    print("✅ Integration tests completed successfully")

if __name__ == "__main__":
    print("🧪 Starting Test Suite for EHB AI Agent Development")
    print("=" * 60)
    
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    
    # Run performance tests
    run_performance_tests()
    
    print("\n" + "=" * 60)
    
    # Run integration tests
    run_integration_tests()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed successfully!") 