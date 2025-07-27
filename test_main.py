#!/usr/bin/env python3
"""
EHB Healthcare System - Tests
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "EHB Healthcare System" in response.json()["message"]

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_patients_endpoint():
    """Test patients endpoint"""
    response = client.get("/api/patients")
    assert response.status_code == 200

def test_doctors_endpoint():
    """Test doctors endpoint"""
    response = client.get("/api/doctors")
    assert response.status_code == 200

def test_appointments_endpoint():
    """Test appointments endpoint"""
    response = client.get("/api/appointments")
    assert response.status_code == 200