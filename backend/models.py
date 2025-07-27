"""
AI Agent Models for Healthcare System
Comprehensive data models for AI agent development
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Enums
class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROCESSING = "processing"
    ERROR = "error"
    TRAINING = "training"

class AgentType(str, Enum):
    ERROR_FIX = "error_fix"
    HEALTH_MONITOR = "health_monitor"
    DEVELOPMENT = "development"
    SECURITY = "security"
    ANALYTICS = "analytics"
    TELEMEDICINE = "telemedicine"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base Models
class BaseAgentModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    version: str = "1.0.0"
    status: AgentStatus = AgentStatus.INACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# AI Agent Models
class AIAgent(BaseAgentModel):
    """AI Agent Model"""
    agent_type: AgentType
    capabilities: List[str] = []
    performance_metrics: Dict[str, float] = {}
    health_score: float = 0.0
    last_activity: Optional[datetime] = None
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    active_tasks: int = 0
    total_tasks_completed: int = 0
    error_count: int = 0
    success_rate: float = 0.0

class AgentTask(BaseModel):
    """Agent Task Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    task_type: str
    description: str
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = {}
    output_data: Dict[str, Any] = {}
    error_message: Optional[str] = None
    progress: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: Optional[int] = None  # in seconds

class AgentMemory(BaseModel):
    """Agent Memory Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    memory_type: str  # short_term, long_term, episodic
    content: Dict[str, Any] = {}
    importance_score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    accessed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class AgentCommunication(BaseModel):
    """Agent Communication Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    receiver_id: str
    message_type: str  # request, response, notification, error
    content: Dict[str, Any] = {}
    priority: Priority = Priority.MEDIUM
    status: str = "sent"  # sent, delivered, read, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None

# Healthcare Models
class Patient(BaseModel):
    """Patient Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    age: int
    gender: str
    contact: str
    email: str
    blood_type: str
    allergies: List[str] = []
    conditions: List[str] = []
    medications: List[str] = []
    status: str = "active"
    last_visit: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Doctor(BaseModel):
    """Doctor Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    specialization: str
    contact: str
    email: str
    rating: float = 4.5
    status: str = "active"
    availability: str = "available"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Appointment(BaseModel):
    """Appointment Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str
    doctor_id: str
    patient_name: str
    doctor_name: str
    date: str
    time: str
    type: str = "in-person"  # in-person, video
    status: str = "scheduled"  # scheduled, completed, cancelled
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MedicalRecord(BaseModel):
    """Medical Record Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str
    doctor_id: str
    diagnosis: str
    treatment: str
    prescription: Optional[str] = None
    notes: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# AI Development Models
class CodeBlock(BaseModel):
    """Code Block Model for AI Development"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_path: str
    language: str
    content: str
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    line_start: int
    line_end: int
    complexity: float = 0.0
    quality_score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ErrorLog(BaseModel):
    """Error Log Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    severity: str = "medium"  # low, medium, high, critical
    status: str = "open"  # open, in_progress, resolved, closed
    assigned_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

class FixSuggestion(BaseModel):
    """Fix Suggestion Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    error_id: str
    agent_id: str
    suggestion_type: str  # code_fix, configuration, dependency
    description: str
    code_changes: Dict[str, str] = {}
    confidence_score: float = 0.0
    estimated_impact: str = "low"  # low, medium, high
    status: str = "pending"  # pending, applied, rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
    applied_at: Optional[datetime] = None

# Analytics Models
class AnalyticsData(BaseModel):
    """Analytics Data Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metric_name: str
    metric_value: float
    metric_unit: str
    category: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class PerformanceMetrics(BaseModel):
    """Performance Metrics Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    cpu_usage: float
    memory_usage: float
    response_time: float
    throughput: float
    error_rate: float
    success_rate: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Configuration Models
class AgentConfig(BaseModel):
    """Agent Configuration Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    config_type: str  # general, performance, security, healthcare
    config_data: Dict[str, Any] = {}
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SystemConfig(BaseModel):
    """System Configuration Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    config_key: str
    config_value: Any
    description: str
    category: str
    is_encrypted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Training Models
class TrainingData(BaseModel):
    """Training Data Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    data_type: str  # code_samples, error_patterns, healthcare_data
    content: Dict[str, Any] = {}
    quality_score: float = 0.0
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TrainingSession(BaseModel):
    """Training Session Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    session_type: str  # supervised, unsupervised, reinforcement
    training_data_ids: List[str] = []
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    progress: float = 0.0
    accuracy: float = 0.0
    loss: float = 0.0
    status: str = "running"  # running, completed, failed, paused

# Communication Models
class Message(BaseModel):
    """Message Model for Agent Communication"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    receiver_id: str
    message_type: str  # request, response, notification, error
    content: Dict[str, Any] = {}
    priority: Priority = Priority.MEDIUM
    status: str = "sent"  # sent, delivered, read, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None

# Health Monitoring Models
class HealthCheck(BaseModel):
    """Health Check Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    component_id: str
    component_type: str  # agent, service, database, api
    status: str  # healthy, warning, critical, offline
    metrics: Dict[str, float] = {}
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Alert(BaseModel):
    """Alert Model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    alert_type: str  # error, warning, info, critical
    title: str
    message: str
    component_id: Optional[str] = None
    severity: str = "medium"  # low, medium, high, critical
    status: str = "active"  # active, acknowledged, resolved
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

# Export all models
__all__ = [
    "AIAgent", "AgentTask", "AgentMemory", "AgentCommunication",
    "Patient", "Doctor", "Appointment", "MedicalRecord",
    "CodeBlock", "ErrorLog", "FixSuggestion",
    "AnalyticsData", "PerformanceMetrics",
    "AgentConfig", "SystemConfig",
    "TrainingData", "TrainingSession",
    "Message", "HealthCheck", "Alert",
    "AgentStatus", "AgentType", "TaskStatus", "Priority"
] 