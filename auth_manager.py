#!/usr/bin/env python3
"""
EHB-5 Authentication Manager
Handles user authentication and JWT token management
"""

import datetime
import functools
import hashlib

import jwt  # type: ignore  # type: ignore
from flask import jsonify, request, session

from database import db


class AuthManager:
    """Authentication manager for EHB-5 project"""

    def __init__(self, secret_key: str = 'ehb5-secret-key-2024') -> None:
        self.secret_key = secret_key

    def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user with username and password"""
        try:
            # Get user from database
            user = db.get_user_by_username(username)
            if not user:
                return None

            # Verify password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user['password_hash'] == password_hash:
                return user

            return None

        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return None

    def generate_token(self, user_id: int, username: str) -> str:
        """Generate JWT token for user"""
        try:
            payload = {
                'user_id': user_id,
                'username': username,
'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                'iat': datetime.datetime.utcnow()
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        except Exception as e:
            print(f"❌ Token generation error: {e}")
            return None

    def verify_token(self, token: str) -> dict:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("❌ Token expired")
            return None
        except jwt.InvalidTokenError:
            print("❌ Invalid token")
            return None
        except Exception as e:
            print(f"❌ Token verification error: {e}")
            return None

    def require_auth(self, f) -> None:
        """Decorator to require authentication for API endpoints"""
        @functools.wraps(f)
        def decorated_function(*args, **kwargs) -> None:
            # Get token from header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'error': 'No authorization header'}), 401

            # Extract token
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401

            # Verify token
            payload = self.verify_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401

            # Set user info in session
            session['user_id'] = payload['user_id']
            session['username'] = payload['username']

            return f(*args, **kwargs)

        return decorated_function

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        return True
