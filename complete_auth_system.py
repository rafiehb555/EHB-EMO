#!/usr/bin/env python3
"""
EHB AI Dev Agent - Complete Authentication System
JWT-based authentication with user management and security features
"""

import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Optional, Union

import bcrypt
import jwt


@dataclass
class User:
    id: str
    username: str
    email: str
    role: str
    sql_level: str
    is_active: bool
    created_at: str

class AuthenticationSystem:
    def __init__(self, db_path: str = "ehb_ai_dev_agent.db"):
        self.db_path = db_path
        self.jwt_secret = os.getenv("JWT_SECRET", "ehb-ai-dev-secret-key-2025")
        self.jwt_algorithm = "HS256"
        self.jwt_expiry_hours = 24

    def get_db_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def generate_token(self, user_data: Dict) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_data['id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'role': user_data['role'],
            'sql_level': user_data['sql_level'],
            'exp': datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def register_user(self, username: str, email: str, password: str, role: str = "user") -> Dict:
        """Register new user"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
            if cursor.fetchone():
                return {"success": False, "error": "User already exists"}

            # Hash password
            password_hash = self.hash_password(password)

            # Create user
            user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, role, sql_level, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, username, email, password_hash, role, "Free", True))

            conn.commit()

            # Get created user
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()

            # Generate token
            token = self.generate_token({
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'role': user_data[4],
                'sql_level': user_data[5]
            })

            return {
                "success": True,
                "message": "User registered successfully",
                "token": token,
                "user": {
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "role": user_data[4],
                    "sql_level": user_data[5]
                }
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def login_user(self, email: str, password: str) -> Dict:
        """Login user"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Find user
            cursor.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
            user_data = cursor.fetchone()

            if not user_data:
                return {"success": False, "error": "Invalid credentials"}

            # Verify password
            if not self.verify_password(password, user_data[3]):
                return {"success": False, "error": "Invalid credentials"}

            # Update last login
            cursor.execute("""
                UPDATE users SET last_login = ?, login_count = login_count + 1
                WHERE id = ?
            """, (datetime.now().isoformat(), user_data[0]))
            conn.commit()

            # Generate token
            token = self.generate_token({
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'role': user_data[4],
                'sql_level': user_data[5]
            })

            return {
                "success": True,
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "role": user_data[4],
                    "sql_level": user_data[5]
                }
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
            user_data = cursor.fetchone()

            if user_data:
                return {
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "role": user_data[4],
                    "sql_level": user_data[5],
                    "is_active": bool(user_data[7]),
                    "last_login": user_data[8],
                    "login_count": user_data[9],
                    "created_at": user_data[10]
                }
            return None

        except Exception as e:
            return None
        finally:
            conn.close()

    def update_user_profile(self, user_id: str, updates: Dict) -> Dict:
        """Update user profile"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Build update query
            allowed_fields = ['username', 'email', 'sql_level']
            update_fields = []
            update_values = []

            for field, value in updates.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    update_values.append(value)

            if not update_fields:
                return {"success": False, "error": "No valid fields to update"}

            update_values.append(datetime.now().isoformat())
            update_values.append(user_id)

            query = f"UPDATE users SET {', '.join(update_fields)}, updated_at = ? WHERE id = ?"
            cursor.execute(query, update_values)
            conn.commit()

            return {"success": True, "message": "Profile updated successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def change_password(self, user_id: str, current_password: str, new_password: str) -> Dict:
        """Change user password"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Get current password hash
            cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()

            if not result:
                return {"success": False, "error": "User not found"}

            # Verify current password
            if not self.verify_password(current_password, result[0]):
                return {"success": False, "error": "Current password is incorrect"}

            # Hash new password
            new_password_hash = self.hash_password(new_password)

            # Update password
            cursor.execute("""
                UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?
            """, (new_password_hash, datetime.now().isoformat(), user_id))
            conn.commit()

            return {"success": True, "message": "Password changed successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def deactivate_user(self, user_id: str) -> Dict:
        """Deactivate user account"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE users SET is_active = 0, updated_at = ? WHERE id = ?
            """, (datetime.now().isoformat(), user_id))
            conn.commit()

            return {"success": True, "message": "User deactivated successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def get_all_users(self, admin_user_id: str) -> Dict:
        """Get all users (admin only)"""
        try:
            # Verify admin user
            admin_user = self.get_user_by_id(admin_user_id)
            if not admin_user or admin_user['role'] != 'admin':
                return {"success": False, "error": "Admin access required"}

            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, username, email, role, sql_level, is_active,
                       last_login, login_count, created_at
                FROM users ORDER BY created_at DESC
            """)
            users_data = cursor.fetchall()

            users = []
            for user_data in users_data:
                users.append({
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "role": user_data[3],
                    "sql_level": user_data[4],
                    "is_active": bool(user_data[5]),
                    "last_login": user_data[6],
                    "login_count": user_data[7],
                    "created_at": user_data[8]
                })

            return {"success": True, "users": users}

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

# Authentication decorator for API endpoints
def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = kwargs.get('auth_header')
        if not auth_header:
            return {"success": False, "error": "No authorization header"}

        try:
            token = auth_header.split(" ")[1]
            auth_system = AuthenticationSystem()
            user_data = auth_system.verify_token(token)

            if not user_data:
                return {"success": False, "error": "Invalid or expired token"}

            # Add user data to kwargs
            kwargs['user_data'] = user_data
            return f(*args, **kwargs)

        except Exception as e:
            return {"success": False, "error": "Authentication failed"}

    return decorated_function

# Role-based access decorator
def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_data = kwargs.get('user_data')
            if not user_data:
                return {"success": False, "error": "Authentication required"}

            if user_data['role'] != required_role and user_data['role'] != 'admin':
                return {"success": False, "error": f"{required_role} role required"}

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def main():
    """Test authentication system"""
    print("🔐 Testing Authentication System...")

    auth = AuthenticationSystem()

    # Test registration
    print("\n1. Testing user registration...")
    result = auth.register_user("testuser", "test@ehb.com", "test123", "user")
    print(f"Registration result: {result}")

    # Test login
    print("\n2. Testing user login...")
    result = auth.login_user("test@ehb.com", "test123")
    print(f"Login result: {result}")

    if result['success']:
        token = result['token']

        # Test token verification
        print("\n3. Testing token verification...")
        user_data = auth.verify_token(token)
        print(f"Token verification: {user_data}")

        # Test get user
        print("\n4. Testing get user...")
        user = auth.get_user_by_id(result['user']['id'])
        print(f"User data: {user}")

if __name__ == "__main__":
    main()
