#!/usr/bin/env python3
"""
EHB-5 Database Module
Handles all database operations including CRUD operations
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class DatabaseManager:
    """Database manager for EHB-5 project"""

    def __init__(self, db_path: str = "ehb5.db") -> None:
        self.db_path = db_path
        self.init_database()

    def init_database(self) -> None:
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Create projects table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        status TEXT DEFAULT 'active',
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                ''')

                # Create data_files table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS data_files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        file_type TEXT NOT NULL,
                        file_size INTEGER,
                        content TEXT,
                        project_id INTEGER,
                        uploaded_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (project_id) REFERENCES projects (id),
                        FOREIGN KEY (uploaded_by) REFERENCES users (id)
                    )
                ''')

                # Create system_logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level TEXT NOT NULL,
                        message TEXT NOT NULL,
                        user_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')

                conn.commit()
                print("✅ Database initialized successfully")

        except Exception as e:
            print("❌ Database initialization error: {e}")

    def create_user(
            self,
            username: str,
            email: str,
            password_hash: str,
            role: str = "user") -> bool:
        """Create a new user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                ''', (username, email, password_hash, role))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            print("❌ User already exists")
            return False
        except Exception as e:
            print("❌ Error creating user: {e}")
            return False

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM users WHERE username = ?', (username,))
                user = cursor.fetchone()
                if user:
                    return {
                        'id': user[0],
                        'username': user[1],
                        'email': user[2],
                        'password_hash': user[3],
                        'role': user[4],
                        'created_at': user[5],
                        'updated_at': user[6]
                    }
                return None
        except Exception as e:
            print("❌ Error getting user: {e}")
            return None

    def create_project(
            self,
            name: str,
            description: str,
            created_by: int) -> bool:
        """Create a new project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO projects (name, description, created_by)
                    VALUES (?, ?, ?)
                ''', (name, description, created_by))
                conn.commit()
                return True
        except Exception as e:
            print("❌ Error creating project: {e}")
            return False

    def get_all_projects(self) -> List[Dict]:
        """Get all projects"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT p.*, u.username as creator_name
                    FROM projects p
                    LEFT JOIN users u ON p.created_by = u.id
                ''')
                projects = cursor.fetchall()
                return [
                    {
                        'id': p[0],
                        'name': p[1],
                        'description': p[2],
                        'status': p[3],
                        'created_by': p[4],
                        'created_at': p[5],
                        'updated_at': p[6],
                        'creator_name': p[7]
                    }
                    for p in projects
                ]
        except Exception as e:
            print("❌ Error getting projects: {e}")
            return []

    def save_data_file(self, filename: str, file_type: str, content: str,
                       project_id: int, uploaded_by: int) -> bool:
        """Save a data file to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO data_files (filename, file_type, content, project_id, uploaded_by)
                    VALUES (?, ?, ?, ?, ?)
                ''', (filename, file_type, content, project_id, uploaded_by))
                conn.commit()
                return True
        except Exception as e:
            print("❌ Error saving data file: {e}")
            return False

    def get_data_files(self, project_id: Optional[int] = None) -> List[Dict]:
        """Get data files, optionally filtered by project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if project_id:
                    cursor.execute('''
                        SELECT df.*, u.username as uploader_name
                        FROM data_files df
                        LEFT JOIN users u ON df.uploaded_by = u.id
                        WHERE df.project_id = ?
                    ''', (project_id,))
                else:
                    cursor.execute('''
                        SELECT df.*, u.username as uploader_name
                        FROM data_files df
                        LEFT JOIN users u ON df.uploaded_by = u.id
                    ''')

                files = cursor.fetchall()
                return [
                    {
                        'id': f[0],
                        'filename': f[1],
                        'file_type': f[2],
                        'file_size': f[3],
                        'content': f[4],
                        'project_id': f[5],
                        'uploaded_by': f[6],
                        'created_at': f[7],
                        'uploader_name': f[8]
                    }
                    for f in files
                ]
        except Exception as e:
            print("❌ Error getting data files: {e}")
            return []

    def log_system_event(self, level: str, message: str,
                         user_id: Optional[int] = None) -> None:
        """Log system events"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_logs (level, message, user_id)
                    VALUES (?, ?, ?)
                ''', (level, message, user_id))
                conn.commit()
        except Exception as e:
            print("❌ Error logging system event: {e}")


# Global database instance
db = DatabaseManager()
