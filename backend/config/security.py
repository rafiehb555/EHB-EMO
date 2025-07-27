"""
Security Configuration Module
Handles security, authentication, and HIPAA compliance for healthcare system
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import bcrypt
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    role: str
    is_active: bool = True

# Security utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Hash password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Authentication dependency
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = security):
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    username = payload.get("sub")
    
    # In real app, fetch user from database
    # For demo, return mock user
    return User(
        username=username,
        email=f"{username}@ehb.com",
        role="doctor" if "doctor" in username else "patient"
    )

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# HIPAA Compliance utilities
class HIPAACompliance:
    """HIPAA compliance utilities"""
    
    @staticmethod
    def audit_log(user_id: str, action: str, resource_type: str, resource_id: str = None, details: str = None):
        """Log audit trail for HIPAA compliance"""
        log_entry = {
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
            "ip_address": "127.0.0.1"  # Get from request in real app
        }
        
        # In real app, save to audit log database
        print(f"🔒 AUDIT LOG: {log_entry}")
        return log_entry
    
    @staticmethod
    def encrypt_sensitive_data(data: str) -> str:
        """Encrypt sensitive healthcare data"""
        # In real app, use proper encryption
        return f"ENCRYPTED_{data}"
    
    @staticmethod
    def decrypt_sensitive_data(encrypted_data: str) -> str:
        """Decrypt sensitive healthcare data"""
        # In real app, use proper decryption
        return encrypted_data.replace("ENCRYPTED_", "")
    
    @staticmethod
    def mask_phi(data: str) -> str:
        """Mask Protected Health Information"""
        if len(data) > 4:
            return data[:2] + "*" * (len(data) - 4) + data[-2:]
        return "*" * len(data)
    
    @staticmethod
    def validate_phi_access(user_role: str, resource_type: str) -> bool:
        """Validate PHI access based on user role"""
        access_rules = {
            "admin": ["patients", "doctors", "appointments", "medical_records"],
            "doctor": ["patients", "appointments", "medical_records"],
            "patient": ["own_records", "own_appointments"],
            "nurse": ["patients", "appointments"]
        }
        
        allowed_resources = access_rules.get(user_role, [])
        return resource_type in allowed_resources

# Security middleware
class SecurityMiddleware:
    """Security middleware for request/response processing"""
    
    @staticmethod
    def add_security_headers(response):
        """Add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
    
    @staticmethod
    def validate_request_origin(origin: str) -> bool:
        """Validate request origin"""
        allowed_origins = [
            "http://localhost:3001",
            "http://localhost:3000",
            "https://ehb-healthcare.com"
        ]
        return origin in allowed_origins

# Rate limiting
class RateLimiter:
    """Rate limiting for API endpoints"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, client_id: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if request is allowed based on rate limit"""
        now = datetime.utcnow()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests outside window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if (now - req_time).seconds < window
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= limit:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True

# Security decorators
def require_authentication(func):
    """Decorator to require authentication"""
    async def wrapper(*args, **kwargs):
        # Authentication logic here
        return await func(*args, **kwargs)
    return wrapper

def require_role(role: str):
    """Decorator to require specific role"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Role validation logic here
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def audit_action(action: str, resource_type: str):
    """Decorator to audit actions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Audit logging logic here
            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Security configuration
SECURITY_CONFIG = {
    "password_min_length": 8,
    "password_require_uppercase": True,
    "password_require_lowercase": True,
    "password_require_numbers": True,
    "password_require_special": True,
    "session_timeout_minutes": 30,
    "max_login_attempts": 5,
    "lockout_duration_minutes": 15,
    "require_mfa": True,
    "encryption_algorithm": "AES-256",
    "audit_log_retention_days": 2555,  # 7 years for HIPAA
    "backup_frequency_hours": 24,
    "data_retention_years": 7
}

# Security validation
def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    errors = []
    
    if len(password) < SECURITY_CONFIG["password_min_length"]:
        errors.append(f"Password must be at least {SECURITY_CONFIG['password_min_length']} characters")
    
    if SECURITY_CONFIG["password_require_uppercase"] and not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if SECURITY_CONFIG["password_require_lowercase"] and not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if SECURITY_CONFIG["password_require_numbers"] and not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    
    if SECURITY_CONFIG["password_require_special"] and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        errors.append("Password must contain at least one special character")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

# Initialize security components
rate_limiter = RateLimiter()
hipaa_compliance = HIPAACompliance() 