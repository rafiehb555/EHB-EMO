#!/usr/bin/env python3
"""
EHB-5 Enterprise Security System
Advanced enterprise-grade security features
"""

import hashlib
import secrets
import re
import time
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database import db


class EnterpriseSecurityManager:
    """Enterprise-grade security manager with advanced features"""

    def __init__(self) -> None:
        self.security_config = {
            "password_policy": {
                "min_length": 12,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": True,
                "max_age_days": 90,
                "history_count": 5
            },
            "session_policy": {
                "timeout_minutes": 30,
                "max_sessions_per_user": 5,
                "inactivity_timeout": 15
            },
            "rate_limiting": {
                "requests_per_minute": 100,
                "burst_limit": 20,
                "block_duration_minutes": 15
            },
            "encryption": {
                "algorithm": "AES-256",
                "key_rotation_days": 30,
                "salt_rounds": 12
            }
        }
        self.active_sessions = {}
        self.failed_attempts = {}
        self.blocked_ips = {}
        self.security_events = []
        self.encryption_keys = {}

    def validate_enterprise_password(self, password: str) -> Dict[str, Any]:
        """Validate password against enterprise security policy"""
        errors = []
        warnings = []
        score = 0

        # Length check
        if len(
password) < self.security_config["password_policy"]["min_length"]:
            errors.append(
                f"Password must be at least
{self.security_config['password_policy']['min_length']} characters")
        else:
            score += 20

        # Character variety checks
        if self.security_config["password_policy"]["require_uppercase"]:
            if not re.search(r'[A-Z]', password):
                errors.append(
                    "Password must contain at least one uppercase letter")
            else:
                score += 10

        if self.security_config["password_policy"]["require_lowercase"]:
            if not re.search(r'[a-z]', password):
                errors.append(
                    "Password must contain at least one lowercase letter")
            else:
                score += 10

        if self.security_config["password_policy"]["require_numbers"]:
            if not re.search(r'\d', password):
                errors.append("Password must contain at least one number")
            else:
                score += 10

        if self.security_config["password_policy"]["require_special"]:
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errors.append(
                    "Password must contain at least one special character")
            else:
                score += 15

        # Complexity checks
        unique_chars = len(set(password))
        if unique_chars < len(password) * 0.6:
            warnings.append("Password has low character variety")
        else:
            score += 10

        # Common pattern checks
        common_patterns = [
            'password', '123456', 'qwerty', 'admin', 'user',
            'welcome', 'login', 'secret', 'test', 'demo'
        ]
        if password.lower() in common_patterns:
            errors.append("Password cannot be a common pattern")
            score -= 20

        # Sequential character checks
        if re.search(r'(.)\1{2,}', password):
            warnings.append("Password contains repeated characters")
            score -= 5

        # Keyboard pattern checks
        keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn', '123456', '654321'
        ]
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                warnings.append("Password contains keyboard patterns")
                score -= 10
                break

        return {
            "valid": len(errors) == 0,
            "score": max(0, min(100, score)),
            "errors": errors,
            "warnings": warnings,
            "strength": self._get_strength_level(score)
        }

    def _get_strength_level(self, score: int) -> str:
        """Get password strength level"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        else:
            return "weak"

    def hash_password_enterprise(self, password: str) -> str:
        """Hash password using enterprise-grade bcrypt"""
        salt = bcrypt.gensalt(
            rounds=self.security_config["encryption"]["salt_rounds"])
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password_enterprise(self, password: str, hashed: str) -> bool:
        """Verify password against enterprise hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_enterprise_session(
self, user_id: int, username: str, ip_address: str) -> Dict[str, Any]:
        """Create enterprise-grade session with advanced features"""
        session_id = secrets.token_urlsafe(32)
        now = datetime.now()

        session_data = {
            "user_id": user_id,
            "username": username,
            "ip_address": ip_address,
            "created_at": now,
            "last_activity": now,
            "expires_at": now +
timedelta(minutes=self.security_config["session_policy"]["timeout_minutes"]),
            "user_agent": None,  # Will be set by request
            "session_type": "web",
            "security_level": "high"
        }

        # Check session limits
        user_sessions = [
s for s in self.active_sessions.values() if s["user_id"] == user_id]
        if len(
            user_sessions) >=
    self.security_config["session_policy"]["max_sessions_per_user"]:
        # Remove oldest session
        oldest_session = min(user_sessions, key=lambda x: x["created_at"])
        self.revoke_session(list(self.active_sessions.keys())[list(
            self.active_sessions.values()).index(oldest_session)])

        self.active_sessions[session_id] = session_data

        # Log security event
        self.log_security_event(
            "SESSION_CREATED",
            f"User {username} created session from {ip_address}")

        return {
            "session_id": session_id,
            "expires_at": session_data["expires_at"].isoformat(),
            "security_level": session_data["security_level"]
        }

    def validate_enterprise_session(
self, session_id: str, ip_address: str = None) -> Optional[Dict[str, Any]]:
        """Validate enterprise session with advanced checks"""
        if session_id not in self.active_sessions:
            return None

        session = self.active_sessions[session_id]
        now = datetime.now()

        # Check expiration
        if now > session["expires_at"]:
            self.revoke_session(session_id)
            self.log_security_event(
                "SESSION_EXPIRED",
                f"Session expired for user {session['username']}")
            return None

        # Check inactivity timeout
        inactivity_limit = timedelta(
minutes=self.security_config["session_policy"]["inactivity_timeout"])
        if now - session["last_activity"] > inactivity_limit:
            self.revoke_session(session_id)
            self.log_security_event(
                "SESSION_INACTIVE",
                f"Session inactive for user {session['username']}")
            return None


        # IP address validation
if ip_address and session["ip_address"] and session["ip_address"] !=
ip_address:
    self.log_security_event(
        "SESSION_IP_MISMATCH",
        f"IP mismatch for user {session['username']}")
    # Don't revoke immediately, but log the suspicious activity
    session["security_level"] = "medium"

    # Update last activity
    session["last_activity"] = now

    return {
        "user_id": session["user_id"],
        "username": session["username"],
        "security_level": session["security_level"]
    }

    def revoke_session(self, session_id: str) -> None:
        """Revoke enterprise session"""
        if session_id in self.active_sessions:
            username = self.active_sessions[session_id]["username"]
            del self.active_sessions[session_id]
            self.log_security_event(
                "SESSION_REVOKED",
                f"Session revoked for user {username}")

    def log_security_event(
            self,
            event_type: str,
            message: str,
            severity: str = "INFO",
            details: Dict = None):
        """Log enterprise security event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
            "severity": severity,
            "details": details or {},
            "source": "enterprise_security"
        }

        self.security_events.append(event)

        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]

        # Log to database
        try:
            db.log_system_event(severity, f"SECURITY: {message}")
        except Exception as e:
            print(f"❌ Security log error: {e}")

    def get_security_analytics(self) -> Dict[str, Any]:
        """Get enterprise security analytics"""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)

        recent_events = [
            event for event in self.security_events
            if datetime.fromisoformat(event["timestamp"]) > last_24h
        ]

        # Event type analysis
        event_counts = {}
        severity_counts = {}
        for event in recent_events:
            event_type = event["event_type"]
            severity = event["severity"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "total_events_24h": len(recent_events),
            "active_sessions": len(self.active_sessions),
            "blocked_ips": len(self.blocked_ips),
            "event_breakdown": event_counts,
            "severity_breakdown": severity_counts,
            "security_score": self._calculate_security_score()
        }

    def _calculate_security_score(self) -> int:
        """Calculate overall security score (0-100)"""
        score = 100

        # Deduct for security issues
        if len(self.blocked_ips) > 10:
            score -= 10

        recent_events = [
            e for e in self.security_events if datetime.fromisoformat(
                e["timestamp"]) > datetime.now() -
            timedelta(
                hours=1)]
        critical_events = [
            e for e in recent_events if e["severity"] == "CRITICAL"]
        if len(critical_events) > 0:
            score -= 20

        return max(0, score)


class EnterpriseRateLimiter:
    """Enterprise-grade rate limiting with advanced features"""

    def __init__(self) -> None:
        self.requests = {}
        self.blocked_ips = {}
        self.whitelist = set()
        self.blacklist = set()
        self.config = {
            "requests_per_minute": 100,
            "burst_limit": 20,
            "block_duration_minutes": 15,
            "whitelist_enabled": True,
            "blacklist_enabled": True
        }

    def is_allowed(self, ip_address: str,
                   endpoint: str = None) -> Dict[str, Any]:
        """Check if request is allowed with detailed response"""
        now = time.time()
        window_start = now - 60  # 1 minute window

        # Check whitelist
        if ip_address in self.whitelist:
            return {"allowed": True, "reason": "whitelisted", "remaining": -1}

        # Check blacklist
        if ip_address in self.blacklist:
            return {"allowed": False, "reason": "blacklisted", "remaining": 0}

        # Check if IP is blocked
        if ip_address in self.blocked_ips:
            block_until = self.blocked_ips[ip_address]
            if now < block_until:
                return {"allowed": False, "reason": "blocked", "remaining": 0}
            else:
                del self.blocked_ips[ip_address]

        # Initialize request tracking
        if ip_address not in self.requests:
            self.requests[ip_address] = []

        # Remove old requests
        self.requests[ip_address] = [
            req_time for req_time in self.requests[ip_address]
            if req_time > window_start
        ]

        # Check rate limit
        current_requests = len(self.requests[ip_address])
        if current_requests >= self.config["requests_per_minute"]:
            # Block IP
            self.blocked_ips[ip_address] = now + \
                (self.config["block_duration_minutes"] * 60)
            return {
                "allowed": False,
                "reason": "rate_limit_exceeded",
                "remaining": 0}

        # Add current request
        self.requests[ip_address].append(now)

        remaining = self.config["requests_per_minute"] - current_requests - 1

        return {
            "allowed": True,
            "reason": "allowed",
            "remaining": remaining,
            "reset_time": window_start + 60
        }

    def add_to_whitelist(self, ip_address: str) -> None:
        """Add IP to whitelist"""
        self.whitelist.add(ip_address)

    def add_to_blacklist(self, ip_address: str) -> None:
        """Add IP to blacklist"""
        self.blacklist.add(ip_address)
        if ip_address in self.requests:
            del self.requests[ip_address]

    def get_rate_limit_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics"""
        return {
            "total_ips": len(self.requests),
            "blocked_ips": len(self.blocked_ips),
            "whitelisted_ips": len(self.whitelist),
            "blacklisted_ips": len(self.blacklist),
            "config": self.config
        }


class EnterpriseEncryption:
    """Enterprise-grade encryption utilities"""

    def __init__(self) -> None:
        self.encryption_key = secrets.token_hex(32)
        self.algorithm = "AES-256"

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        # This is a simplified encryption for demonstration
        # In production, use proper encryption libraries
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256()
        hash_obj.update((data + salt + self.encryption_key).encode())
        return f"{salt}:{hash_obj.hexdigest()}"

    def mask_sensitive_data(self, data: str, mask_char: str = "*") -> str:
        """Mask sensitive data for display"""
        if len(data) <= 4:
            return mask_char * len(data)

        return data[:2] + mask_char * (len(data) - 4) + data[-2:]

    def validate_input_security(
            self, data: str, max_length: int = 1000) -> Dict[str, Any]:
        """Validate input for security threats"""
        errors = []
        warnings = []

        # Length check
        if len(data) > max_length:
            errors.append(f"Input too long (max {max_length} characters)")

        # SQL Injection patterns
        sql_patterns = [
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
            r'(\b(or|and)\b\s+\d+\s*=\s*\d+)',
r'(\b(union|select|insert|update|delete|drop|create|alter)\b\s+.*\bfrom\b)']

        for pattern in sql_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                errors.append("Potential SQL injection detected")
                break

        # XSS patterns
        xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]

        for pattern in xss_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                errors.append("Potential XSS attack detected")
                break

        # Command injection patterns
        cmd_patterns = [
            r'(\b(cat|ls|pwd|whoami|id|uname)\b)',
            r'(\b(rm|del|format|fdisk)\b)',
            r'(\b(netcat|nc|telnet|ssh)\b)'
        ]

        for pattern in cmd_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                warnings.append("Potential command injection pattern detected")
                break

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "sanitized": data.strip() if len(errors) == 0 else ""
        }


# Global enterprise security instances
enterprise_security = EnterpriseSecurityManager()
enterprise_rate_limiter = EnterpriseRateLimiter()
enterprise_encryption = EnterpriseEncryption()
