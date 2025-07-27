#!/usr/bin/env python3
"""
EHB AI Dev Agent - Complete Database Setup
Creates all missing database tables and sample data
"""

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List

import bcrypt


class CompleteDatabaseSetup:
    def __init__(self):
        self.db_path = "ehb_ai_dev_agent.db"
        self.conn = None
        self.cursor = None

    def setup_database(self):
        """Setup complete database with all tables"""
        print("Setting up complete database...")

        try:
            # Connect to database
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            # Create all tables
            self.create_users_table()
            self.create_ai_agents_table()
            self.create_projects_table()
            self.create_agent_memory_table()
            self.create_agent_tasks_table()
            self.create_agent_communications_table()
            self.create_analytics_table()
            self.create_errors_table()
            self.create_notifications_table()
            self.create_settings_table()

            # Insert sample data
            self.insert_sample_data()

            # Commit changes
            self.conn.commit()
            print("Database setup completed successfully!")

        except Exception as e:
            print(f"Database setup failed: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()

    def create_users_table(self):
        """Create users table with authentication"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                sql_level TEXT DEFAULT 'Free',
                sql_expiry_date TEXT,
                is_active BOOLEAN DEFAULT 1,
                last_login TEXT,
                login_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Users table created")

    def create_ai_agents_table(self):
        """Create AI agents table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                status TEXT DEFAULT 'offline',
                performance_score REAL DEFAULT 0.0,
                current_task TEXT,
                last_activity TEXT,
                configuration TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("AI Agents table created")

    def create_projects_table(self):
        """Create projects table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                owner_id TEXT,
                assigned_agents TEXT,
                progress REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')
        print("Projects table created")

    def create_agent_memory_table(self):
        """Create agent memory table"""
        self.cursor.execute('''
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
        print("Agent Memory table created")

    def create_agent_tasks_table(self):
        """Create agent tasks table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_tasks (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                task_type TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                progress REAL DEFAULT 0.0,
                result TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES ai_agents (id)
            )
        ''')
        print("Agent Tasks table created")

    def create_agent_communications_table(self):
        """Create agent communications table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_communications (
                id TEXT PRIMARY KEY,
                sender_id TEXT NOT NULL,
                receiver_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'sent',
                FOREIGN KEY (sender_id) REFERENCES ai_agents (id),
                FOREIGN KEY (receiver_id) REFERENCES ai_agents (id)
            )
        ''')
        print("Agent Communications table created")

    def create_analytics_table(self):
        """Create analytics table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id TEXT PRIMARY KEY,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_data TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                category TEXT,
                tags TEXT
            )
        ''')
        print("Analytics table created")

    def create_errors_table(self):
        """Create errors table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id TEXT PRIMARY KEY,
                error_type TEXT NOT NULL,
                error_message TEXT,
                stack_trace TEXT,
                severity TEXT DEFAULT 'medium',
                resolved BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT
            )
        ''')
        print("Errors table created")

    def create_notifications_table(self):
        """Create notifications table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT,
                type TEXT DEFAULT 'info',
                read BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("Notifications table created")

    def create_settings_table(self):
        """Create settings table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id TEXT PRIMARY KEY,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                setting_type TEXT DEFAULT 'string',
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Settings table created")

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def insert_sample_data(self):
        """Insert sample data into all tables"""
        print("Inserting sample data...")

        # Insert sample users
        self.insert_sample_users()

        # Insert sample AI agents
        self.insert_sample_agents()

        # Insert sample projects
        self.insert_sample_projects()

        # Insert sample analytics
        self.insert_sample_analytics()

        # Insert sample settings
        self.insert_sample_settings()

        print("Sample data inserted successfully!")

    def insert_sample_users(self):
        """Insert sample users"""
        users = [
            {
                'id': 'user_001',
                'username': 'admin',
                'email': 'admin@ehb.com',
                'password_hash': self.hash_password('admin123'),
                'role': 'admin',
                'sql_level': 'Enterprise',
                'is_active': True
            },
            {
                'id': 'user_002',
                'username': 'developer',
                'email': 'dev@ehb.com',
                'password_hash': self.hash_password('dev123'),
                'role': 'developer',
                'sql_level': 'Premium',
                'is_active': True
            },
            {
                'id': 'user_003',
                'username': 'user',
                'email': 'user@ehb.com',
                'password_hash': self.hash_password('user123'),
                'role': 'user',
                'sql_level': 'Basic',
                'is_active': True
            }
        ]

        for user in users:
            self.cursor.execute('''
                INSERT OR REPLACE INTO users
                (id, username, email, password_hash, role, sql_level, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user['id'], user['username'], user['email'],
                user['password_hash'], user['role'], user['sql_level'], user['is_active']
            ))

        print("Sample users inserted")

    def insert_sample_agents(self):
        """Insert sample AI agents"""
        agents = [
            {
                'id': 'agent_001',
                'name': 'Development Agent',
                'agent_type': 'development',
                'status': 'active',
                'performance_score': 98.5,
                'current_task': 'Writing Code',
                'configuration': json.dumps({
                    'model': 'gpt-4',
                    'temperature': 0.7,
                    'max_tokens': 2000
                })
            },
            {
                'id': 'agent_002',
                'name': 'Testing Agent',
                'agent_type': 'testing',
                'status': 'active',
                'performance_score': 95.2,
                'current_task': 'Running Tests',
                'configuration': json.dumps({
                    'model': 'gpt-4',
                    'temperature': 0.3,
                    'max_tokens': 1500
                })
            },
            {
                'id': 'agent_003',
                'name': 'Deployment Agent',
                'agent_type': 'deployment',
                'status': 'active',
                'performance_score': 97.8,
                'current_task': 'Deploying Apps',
                'configuration': json.dumps({
                    'model': 'gpt-4',
                    'temperature': 0.5,
                    'max_tokens': 1800
                })
            },
            {
                'id': 'agent_004',
                'name': 'Security Agent',
                'agent_type': 'security',
                'status': 'active',
                'performance_score': 99.1,
                'current_task': 'Monitoring Security',
                'configuration': json.dumps({
                    'model': 'gpt-4',
                    'temperature': 0.2,
                    'max_tokens': 1200
                })
            }
        ]

        for agent in agents:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ai_agents
                (id, name, agent_type, status, performance_score, current_task, configuration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent['id'], agent['name'], agent['agent_type'], agent['status'],
                agent['performance_score'], agent['current_task'], agent['configuration']
            ))

        print("Sample AI agents inserted")

    def insert_sample_projects(self):
        """Insert sample projects"""
        projects = [
            {
                'id': 'project_001',
                'name': 'EHB AI Dev Agent',
                'description': 'Advanced AI Development Platform',
                'status': 'active',
                'owner_id': 'user_001',
                'assigned_agents': json.dumps(['agent_001', 'agent_002', 'agent_003', 'agent_004']),
                'progress': 85.5
            },
            {
                'id': 'project_002',
                'name': 'Healthcare Management System',
                'description': 'Complete healthcare platform',
                'status': 'active',
                'owner_id': 'user_002',
                'assigned_agents': json.dumps(['agent_001', 'agent_002']),
                'progress': 92.3
            },
            {
                'id': 'project_003',
                'name': 'Mobile App Development',
                'description': 'Cross-platform mobile application',
                'status': 'pending',
                'owner_id': 'user_003',
                'assigned_agents': json.dumps(['agent_001', 'agent_003']),
                'progress': 45.7
            }
        ]

        for project in projects:
            self.cursor.execute('''
                INSERT OR REPLACE INTO projects
                (id, name, description, status, owner_id, assigned_agents, progress)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                project['id'], project['name'], project['description'], project['status'],
                project['owner_id'], project['assigned_agents'], project['progress']
            ))

        print("Sample projects inserted")

    def insert_sample_analytics(self):
        """Insert sample analytics data"""
        analytics = [
            {
                'id': 'analytics_001',
                'metric_name': 'system_uptime',
                'metric_value': 99.9,
                'metric_data': json.dumps({'daily': 99.9, 'weekly': 99.8, 'monthly': 99.7}),
                'category': 'performance',
                'tags': json.dumps(['system', 'uptime', 'reliability'])
            },
            {
                'id': 'analytics_002',
                'metric_name': 'active_users',
                'metric_value': 1250,
                'metric_data': json.dumps({'current': 1250, 'peak': 1500, 'average': 1100}),
                'category': 'usage',
                'tags': json.dumps(['users', 'engagement', 'growth'])
            },
            {
                'id': 'analytics_003',
                'metric_name': 'ai_agent_performance',
                'metric_value': 97.6,
                'metric_data': json.dumps({
                    'development_agent': 98.5,
                    'testing_agent': 95.2,
                    'deployment_agent': 97.8,
                    'security_agent': 99.1
                }),
                'category': 'ai',
                'tags': json.dumps(['ai', 'agents', 'performance'])
            }
        ]

        for analytic in analytics:
            self.cursor.execute('''
                INSERT OR REPLACE INTO analytics
                (id, metric_name, metric_value, metric_data, category, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                analytic['id'], analytic['metric_name'], analytic['metric_value'],
                analytic['metric_data'], analytic['category'], analytic['tags']
            ))

        print("Sample analytics inserted")

    def insert_sample_settings(self):
        """Insert sample settings"""
        settings = [
            {
                'id': 'setting_001',
                'setting_key': 'system_name',
                'setting_value': 'EHB AI Dev Agent',
                'setting_type': 'string',
                'description': 'System display name'
            },
            {
                'id': 'setting_002',
                'setting_key': 'max_agents',
                'setting_value': '10',
                'setting_type': 'integer',
                'description': 'Maximum number of AI agents'
            },
            {
                'id': 'setting_003',
                'setting_key': 'auto_deploy',
                'setting_value': 'true',
                'setting_type': 'boolean',
                'description': 'Enable automatic deployment'
            },
            {
                'id': 'setting_004',
                'setting_key': 'notification_email',
                'setting_value': 'notifications@ehb.com',
                'setting_type': 'string',
                'description': 'Notification email address'
            }
        ]

        for setting in settings:
            self.cursor.execute('''
                INSERT OR REPLACE INTO settings
                (id, setting_key, setting_value, setting_type, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                setting['id'], setting['setting_key'], setting['setting_value'],
                setting['setting_type'], setting['description']
            ))

        print("Sample settings inserted")

def main():
    """Main function"""
    print("Starting complete database setup...")

    setup = CompleteDatabaseSetup()
    setup.setup_database()

    print("\nDatabase setup completed!")
    print("Database file: ehb_ai_dev_agent.db")
    print("Default users:")
    print("   - Admin: admin@ehb.com / admin123")
    print("   - Developer: dev@ehb.com / dev123")
    print("   - User: user@ehb.com / user123")

if __name__ == "__main__":
    main()
