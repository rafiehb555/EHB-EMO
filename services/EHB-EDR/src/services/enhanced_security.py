#!/usr/bin/env python3
"""
EHB-5 Enhanced Security Module
Advanced security features including bcrypt, rate limiting, and input validation
"""

import bcrypt
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import request, jsonify
from functools import wraps


class SecurityManager:
    """Enhanced security manager for EHB-5 project"""

    def __init__(self) -> None:
        self.rate_limit_requests = {}
        self.blocked_ips = {}
        self.max_requests_per_minute = 60
        self.block_duration = 300  # 5 minutes

    def hash_password_bcrypt(self, password: str) -> str:
        """Hash password using bcrypt (more secure than SHA-256)"""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            print(f"❌ Error hashing password: {e}")
            return ""

    def verify_password_bcrypt(self, password: str, hashed_password: str) -> bool:
        """Verify password using bcrypt"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            print(f"❌ Error verifying password: {e}")
            return False

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        # Username should be 3-20 characters, alphanumeric and underscores only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))

    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }

        if len(password) < 8:
            validation['is_valid'] = False
            validation['errors'].append('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', password):
            validation['warnings'].append('Password should contain uppercase letters')

        if not re.search(r'[a-z]', password):
            validation['warnings'].append('Password should contain lowercase letters')

        if not re.search(r'\d', password):
            validation['warnings'].append('Password should contain numbers')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            validation['warnings'].append('Password should contain special characters')

        return validation

    def sanitize_input(self, data: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks"""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')']
        for char in dangerous_chars:
            data = data.replace(char, '')

        # Remove script tags
        data = re.sub(r'<script.*?</script>', '', data, flags=re.IGNORECASE)

        return data.strip()

    def rate_limit(self, f):
        """Rate limiting decorator"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr

            # Check if IP is blocked
            if client_ip in self.blocked_ips:
                block_time = self.blocked_ips[client_ip]
                if datetime.now() < block_time:
                    return jsonify({
                        'error': 'Too many requests. Please try again later.',
                        'blocked_until': block_time.isoformat()
                    }), 429
                else:
                    del self.blocked_ips[client_ip]

            # Check rate limit
            current_time = datetime.now()
            if client_ip not in self.rate_limit_requests:
                self.rate_limit_requests[client_ip] = []

            # Remove old requests (older than 1 minute)
            self.rate_limit_requests[client_ip] = [
                req_time for req_time in self.rate_limit_requests[client_ip]
                if current_time - req_time < timedelta(minutes=1)
            ]

            # Check if limit exceeded
            if len(self.rate_limit_requests[client_ip]) >= self.max_requests_per_minute:
                # Block IP for 5 minutes
                self.blocked_ips[client_ip] = current_time + timedelta(seconds=self.block_duration)
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.',
                    'blocked_until': self.blocked_ips[client_ip].isoformat()
                }), 429

            # Add current request
            self.rate_limit_requests[client_ip].append(current_time)

            return f(*args, **kwargs)

        return decorated_function

    def validate_json_schema(self, data: Dict, required_fields: List[str]) -> Dict[str, Any]:
        """Validate JSON data against required schema"""
        validation = {
            'is_valid': True,
            'errors': [],
            'missing_fields': []
        }

        for field in required_fields:
            if field not in data:
                validation['is_valid'] = False
                validation['missing_fields'].append(field)

        return validation

    def log_security_event(self, event_type: str, details: str, user_id: Optional[int] = None) -> None:
        """Log security events"""
        try:
            from database import db
            log_message = f"SECURITY: {event_type} - {details}"
            db.log_system_event('SECURITY', log_message, user_id)
        except Exception as e:
            print(f"❌ Error logging security event: {e}")

    def generate_secure_token(self, user_id: int, username: str) -> str:
        """Generate secure JWT token with additional security measures"""
        try:
            import jwt
            payload = {
                'user_id': user_id,
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=1),  # Shorter expiry
                'iat': datetime.utcnow(),
                'jti': f"{user_id}_{int(time.time())}"  # JWT ID for uniqueness
            }
            return jwt.encode(payload, 'ehb5-secure-secret-key-2024', algorithm='HS256')
        except Exception as e:
            print(f"❌ Error generating secure token: {e}")
            return ""

    def validate_file_upload(self, filename: str, file_size: int, allowed_extensions: List[str]) -> Dict[str, Any]:
        """Validate file upload security"""
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }

        # Check file extension
        file_ext = filename.split('.')[-1].lower() if '.' in filename else ''
        if file_ext not in allowed_extensions:
            validation['is_valid'] = False
            validation['errors'].append(f'File type .{file_ext} not allowed')

        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            validation['is_valid'] = False
            validation['errors'].append('File size too large (max 10MB)')

        # Check for dangerous file names
        dangerous_patterns = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for pattern in dangerous_patterns:
            if pattern in filename:
                validation['is_valid'] = False
                validation['errors'].append('Invalid filename')

        return validation


# Global security manager instance
security_manager = SecurityManager()
