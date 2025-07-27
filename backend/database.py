"""
Database Module for AI Agent Development
Comprehensive database operations for healthcare and AI agent management
"""

import asyncio
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiosqlite

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database Manager for AI Agent Development"""
    
    def __init__(self, db_path: str = "ehb_ai_agents.db"):
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def init_database(self):
        """Initialize database with all tables"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.create_tables()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    def create_tables(self):
        """Create all database tables"""
        cursor = self.connection.cursor()
        
        # AI Agents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                agent_type TEXT NOT NULL,
                status TEXT DEFAULT 'inactive',
                version TEXT DEFAULT '1.0.0',
                capabilities TEXT,
                performance_metrics TEXT,
                health_score REAL DEFAULT 0.0,
                last_activity TEXT,
                memory_usage REAL DEFAULT 0.0,
                cpu_usage REAL DEFAULT 0.0,
                active_tasks INTEGER DEFAULT 0,
                total_tasks_completed INTEGER DEFAULT 0,
                error_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Agent Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_tasks (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                task_type TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                input_data TEXT,
                output_data TEXT,
                error_message TEXT,
                progress REAL DEFAULT 0.0,
                estimated_duration INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                started_at TEXT,
                completed_at TEXT,
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Agent Memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_memory (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                content TEXT,
                importance_score REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                accessed_at TEXT,
                expires_at TEXT,
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT NOT NULL,
                blood_type TEXT NOT NULL,
                allergies TEXT,
                conditions TEXT,
                medications TEXT,
                status TEXT DEFAULT 'active',
                last_visit TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT NOT NULL,
                rating REAL DEFAULT 4.5,
                status TEXT DEFAULT 'active',
                availability TEXT DEFAULT 'available',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                type TEXT DEFAULT 'in-person',
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        # Medical Records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                treatment TEXT NOT NULL,
                prescription TEXT,
                notes TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        # Error Logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_logs (
                id TEXT PRIMARY KEY,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                stack_trace TEXT,
                file_path TEXT,
                line_number INTEGER,
                severity TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'open',
                assigned_agent TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT
            )
        ''')
        
        # Fix Suggestions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fix_suggestions (
                id TEXT PRIMARY KEY,
                error_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                suggestion_type TEXT NOT NULL,
                description TEXT,
                code_changes TEXT,
                confidence_score REAL DEFAULT 0.0,
                estimated_impact TEXT DEFAULT 'low',
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                applied_at TEXT,
                FOREIGN KEY (error_id) REFERENCES error_logs (id),
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Analytics Data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_data (
                id TEXT PRIMARY KEY,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_unit TEXT,
                category TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Performance Metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                response_time REAL,
                throughput REAL,
                error_rate REAL,
                success_rate REAL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Agent Configurations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_configs (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                config_type TEXT NOT NULL,
                config_data TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Training Data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_data (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                data_type TEXT NOT NULL,
                content TEXT,
                quality_score REAL DEFAULT 0.0,
                is_verified BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Training Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_sessions (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                session_type TEXT NOT NULL,
                training_data_ids TEXT,
                start_time TEXT DEFAULT CURRENT_TIMESTAMP,
                end_time TEXT,
                progress REAL DEFAULT 0.0,
                accuracy REAL DEFAULT 0.0,
                loss REAL DEFAULT 0.0,
                status TEXT DEFAULT 'running',
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        
        # Health Checks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_checks (
                id TEXT PRIMARY KEY,
                component_id TEXT NOT NULL,
                component_type TEXT NOT NULL,
                status TEXT NOT NULL,
                metrics TEXT,
                error_message TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                alert_type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                component_id TEXT,
                severity TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT
            )
        ''')
        
        self.connection.commit()
        logger.info("✅ All database tables created successfully")
    
    def insert_agent(self, agent_data: Dict[str, Any]) -> bool:
        """Insert AI agent into database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO ai_agents (
                    id, name, description, agent_type, status, version,
                    capabilities, performance_metrics, health_score,
                    last_activity, memory_usage, cpu_usage,
                    active_tasks, total_tasks_completed, error_count, success_rate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent_data['id'], agent_data['name'], agent_data['description'],
                agent_data['agent_type'], agent_data['status'], agent_data.get('version', '1.0.0'),
                json.dumps(agent_data.get('capabilities', [])),
                json.dumps(agent_data.get('performance_metrics', {})),
                agent_data.get('health_score', 0.0),
                agent_data.get('last_activity'),
                agent_data.get('memory_usage', 0.0),
                agent_data.get('cpu_usage', 0.0),
                agent_data.get('active_tasks', 0),
                agent_data.get('total_tasks_completed', 0),
                agent_data.get('error_count', 0),
                agent_data.get('success_rate', 0.0)
            ))
            self.connection.commit()
            logger.info(f"✅ Agent {agent_data['name']} inserted successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to insert agent: {e}")
            return False
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all AI agents from database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM ai_agents')
            columns = [description[0] for description in cursor.description]
            agents = []
            for row in cursor.fetchall():
                agent = dict(zip(columns, row))
                # Parse JSON fields
                agent['capabilities'] = json.loads(agent['capabilities']) if agent['capabilities'] else []
                agent['performance_metrics'] = json.loads(agent['performance_metrics']) if agent['performance_metrics'] else {}
                agents.append(agent)
            return agents
        except Exception as e:
            logger.error(f"❌ Failed to get agents: {e}")
            return []
    
    def insert_task(self, task_data: Dict[str, Any]) -> bool:
        """Insert agent task into database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO agent_tasks (
                    id, agent_id, task_type, description, priority, status,
                    input_data, output_data, error_message, progress,
                    estimated_duration, started_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_data['id'], task_data['agent_id'], task_data['task_type'],
                task_data['description'], task_data['priority'], task_data['status'],
                json.dumps(task_data.get('input_data', {})),
                json.dumps(task_data.get('output_data', {})),
                task_data.get('error_message'),
                task_data.get('progress', 0.0),
                task_data.get('estimated_duration'),
                task_data.get('started_at'),
                task_data.get('completed_at')
            ))
            self.connection.commit()
            logger.info(f"✅ Task {task_data['id']} inserted successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to insert task: {e}")
            return False
    
    def get_agent_tasks(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get tasks for specific agent"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM agent_tasks WHERE agent_id = ?', (agent_id,))
            columns = [description[0] for description in cursor.description]
            tasks = []
            for row in cursor.fetchall():
                task = dict(zip(columns, row))
                # Parse JSON fields
                task['input_data'] = json.loads(task['input_data']) if task['input_data'] else {}
                task['output_data'] = json.loads(task['output_data']) if task['output_data'] else {}
                tasks.append(task)
            return tasks
        except Exception as e:
            logger.error(f"❌ Failed to get agent tasks: {e}")
            return []
    
    def insert_patient(self, patient_data: Dict[str, Any]) -> bool:
        """Insert patient into database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO patients (
                    id, name, age, gender, contact, email, blood_type,
                    allergies, conditions, medications, status, last_visit
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_data['id'], patient_data['name'], patient_data['age'],
                patient_data['gender'], patient_data['contact'], patient_data['email'],
                patient_data['blood_type'],
                json.dumps(patient_data.get('allergies', [])),
                json.dumps(patient_data.get('conditions', [])),
                json.dumps(patient_data.get('medications', [])),
                patient_data.get('status', 'active'),
                patient_data.get('last_visit')
            ))
            self.connection.commit()
            logger.info(f"✅ Patient {patient_data['name']} inserted successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to insert patient: {e}")
            return False
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Get all patients from database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM patients')
            columns = [description[0] for description in cursor.description]
            patients = []
            for row in cursor.fetchall():
                patient = dict(zip(columns, row))
                # Parse JSON fields
                patient['allergies'] = json.loads(patient['allergies']) if patient['allergies'] else []
                patient['conditions'] = json.loads(patient['conditions']) if patient['conditions'] else []
                patient['medications'] = json.loads(patient['medications']) if patient['medications'] else []
                patients.append(patient)
            return patients
        except Exception as e:
            logger.error(f"❌ Failed to get patients: {e}")
            return []
    
    def insert_error_log(self, error_data: Dict[str, Any]) -> bool:
        """Insert error log into database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO error_logs (
                    id, error_type, error_message, stack_trace, file_path,
                    line_number, severity, status, assigned_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                error_data['id'], error_data['error_type'], error_data['error_message'],
                error_data.get('stack_trace'), error_data.get('file_path'),
                error_data.get('line_number'), error_data.get('severity', 'medium'),
                error_data.get('status', 'open'), error_data.get('assigned_agent')
            ))
            self.connection.commit()
            logger.warning(f"⚠️ Error logged: {error_data['error_message']}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to insert error log: {e}")
            return False
    
    def get_analytics_data(self, metric_name: str = None, category: str = None) -> List[Dict[str, Any]]:
        """Get analytics data from database"""
        try:
            cursor = self.connection.cursor()
            if metric_name and category:
                cursor.execute('SELECT * FROM analytics_data WHERE metric_name = ? AND category = ?', (metric_name, category))
            elif metric_name:
                cursor.execute('SELECT * FROM analytics_data WHERE metric_name = ?', (metric_name,))
            elif category:
                cursor.execute('SELECT * FROM analytics_data WHERE category = ?', (category,))
            else:
                cursor.execute('SELECT * FROM analytics_data ORDER BY timestamp DESC LIMIT 100')
            
            columns = [description[0] for description in cursor.description]
            analytics = []
            for row in cursor.fetchall():
                data = dict(zip(columns, row))
                data['metadata'] = json.loads(data['metadata']) if data['metadata'] else {}
                analytics.append(data)
            return analytics
        except Exception as e:
            logger.error(f"❌ Failed to get analytics data: {e}")
            return []
    
    def insert_analytics_data(self, analytics_data: Dict[str, Any]) -> bool:
        """Insert analytics data into database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO analytics_data (
                    id, metric_name, metric_value, metric_unit, category,
                    timestamp, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                analytics_data['id'], analytics_data['metric_name'],
                analytics_data['metric_value'], analytics_data.get('metric_unit'),
                analytics_data.get('category'), analytics_data.get('timestamp'),
                json.dumps(analytics_data.get('metadata', {}))
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Failed to insert analytics data: {e}")
            return False
    
    def get_performance_metrics(self, agent_id: str = None) -> List[Dict[str, Any]]:
        """Get performance metrics from database"""
        try:
            cursor = self.connection.cursor()
            if agent_id:
                cursor.execute('SELECT * FROM performance_metrics WHERE agent_id = ? ORDER BY timestamp DESC', (agent_id,))
            else:
                cursor.execute('SELECT * FROM performance_metrics ORDER BY timestamp DESC LIMIT 100')
            
            columns = [description[0] for description in cursor.description]
            metrics = []
            for row in cursor.fetchall():
                metrics.append(dict(zip(columns, row)))
            return metrics
        except Exception as e:
            logger.error(f"❌ Failed to get performance metrics: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("✅ Database connection closed")

# Initialize database manager
db_manager = DatabaseManager()

# Sample data insertion
def insert_sample_data():
    """Insert sample data for development"""
    # Sample agents
    agents = [
        {
            "id": "agent_001",
            "name": "EHB Error Fix Agent",
            "description": "AI agent for automatic error detection and fixing",
            "agent_type": "error_fix",
            "status": "active",
            "capabilities": ["error_detection", "code_fixing", "suggestion_generation"],
            "health_score": 95.0
        },
        {
            "id": "agent_002",
            "name": "EHB Health Monitor",
            "description": "AI agent for system health monitoring",
            "agent_type": "health_monitor",
            "status": "active",
            "capabilities": ["health_checking", "performance_monitoring", "alerting"],
            "health_score": 88.0
        }
    ]
    
    # Sample patients
    patients = [
        {
            "id": "P001",
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "contact": "+1-555-0123",
            "email": "john.doe@email.com",
            "blood_type": "A+",
            "allergies": ["Penicillin", "Peanuts"],
            "conditions": ["Hypertension", "Diabetes Type 2"],
            "medications": ["Metformin", "Lisinopril"]
        },
        {
            "id": "P002",
            "name": "Jane Smith",
            "age": 32,
            "gender": "female",
            "contact": "+1-555-0124",
            "email": "jane.smith@email.com",
            "blood_type": "O-",
            "allergies": ["Latex"],
            "conditions": ["Asthma"],
            "medications": ["Albuterol"]
        }
    ]
    
    # Insert sample data
    for agent in agents:
        db_manager.insert_agent(agent)
    
    for patient in patients:
        db_manager.insert_patient(patient)
    
    logger.info("✅ Sample data inserted successfully")

if __name__ == "__main__":
    # Insert sample data
    insert_sample_data() 