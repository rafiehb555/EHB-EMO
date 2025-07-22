#!/usr/bin/env python3
"""
EHB-5 Production Configuration
Production settings and environment configuration
"""

import os
import json
from pathlib import Path

class ProductionConfig:
    """Production configuration manager"""
    
    def __init__(self):
        self.config_file = "production_config.json"
        self.load_config()
    
    def load_config(self):
        """Load production configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default production configuration"""
        self.config = {
            "environment": "production",
            "debug": False,
            "host": "0.0.0.0",
            "port": 5000,
            "dashboard_port": 8000,
            "database": {
                "type": "sqlite",
                "path": "ehb5.db",
                "backup_enabled": True,
                "backup_interval": 24  # hours
            },
            "security": {
                "jwt_secret": os.environ.get('JWT_SECRET', 'ehb5-production-secret-2024'),
                "session_timeout": 24,  # hours
                "password_min_length": 8,
                "max_login_attempts": 5
            },
            "api": {
                "rate_limit": 100,  # requests per minute
                "cors_enabled": True,
                "cors_origins": ["*"],
                "timeout": 30  # seconds
            },
            "logging": {
                "level": "INFO",
                "file": "ehb5.log",
                "max_size": 10,  # MB
                "backup_count": 5
            },
            "monitoring": {
                "health_check_interval": 60,  # seconds
                "performance_monitoring": True,
                "error_tracking": True
            },
            "backup": {
                "enabled": True,
                "schedule": "daily",
                "retention_days": 30,
                "compression": True
            },
            "ai_agents": {
                "enabled": True,
                "auto_start": True,
                "max_concurrent_tasks": 5,
                "task_timeout": 300  # seconds
            }
        }
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_setting(self, key, default=None):
        """Get a configuration setting"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_setting(self, key, value):
        """Set a configuration setting"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def validate_config(self):
        """Validate production configuration"""
        errors = []
        warnings = []
        
        # Check required settings
        required_settings = [
            "environment", "host", "port", "database.type", 
            "security.jwt_secret", "api.rate_limit"
        ]
        
        for setting in required_settings:
            if not self.get_setting(setting):
                errors.append(f"Missing required setting: {setting}")
        
        # Check security settings
        if self.get_setting("security.password_min_length", 0) < 8:
            warnings.append("Password minimum length should be at least 8")
        
        if self.get_setting("security.session_timeout", 0) > 48:
            warnings.append("Session timeout should not exceed 48 hours")
        
        # Check API settings
        if self.get_setting("api.rate_limit", 0) > 1000:
            warnings.append("Rate limit should not exceed 1000 requests per minute")
        
        # Check database settings
        if not self.get_setting("database.backup_enabled", True):
            warnings.append("Database backup is disabled")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_environment_vars(self):
        """Get environment variables for production"""
        return {
            "EHB5_ENVIRONMENT": self.get_setting("environment", "production"),
            "EHB5_HOST": self.get_setting("host", "0.0.0.0"),
            "EHB5_PORT": str(self.get_setting("port", 5000)),
            "EHB5_DASHBOARD_PORT": str(self.get_setting("dashboard_port", 8000)),
            "JWT_SECRET": self.get_setting("security.jwt_secret"),
            "DATABASE_PATH": self.get_setting("database.path", "ehb5.db"),
            "LOG_LEVEL": self.get_setting("logging.level", "INFO"),
            "DEBUG": str(self.get_setting("debug", False)).lower()
        }
    
    def generate_docker_config(self):
        """Generate Docker configuration"""
        dockerfile = """FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create non-root user
RUN useradd -m -u 1000 ehb5 && chown -R ehb5:ehb5 /app
USER ehb5

# Expose ports
EXPOSE 5000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:5000/api/health || exit 1

# Start application
CMD ["python", "main.py"]
"""
        
        docker_compose = """version: '3.8'

services:
  ehb5-app:
    build: .
    ports:
      - "5000:5000"
      - "8000:8000"
    environment:
      - EHB5_ENVIRONMENT=production
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  ehb5-db:
    image: postgres:13
    environment:
      - POSTGRES_DB=ehb5
      - POSTGRES_USER=ehb5
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
"""
        
        # Save Docker files
        with open("Dockerfile", "w") as f:
            f.write(dockerfile)
        
        with open("docker-compose.yml", "w") as f:
            f.write(docker_compose)
        
        print("✅ Docker configuration generated")
        return True
    
    def generate_nginx_config(self):
        """Generate Nginx configuration"""
        nginx_config = """server {
    listen 80;
    server_name localhost;

    # API server
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Dashboard
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
"""
        
        with open("nginx.conf", "w") as f:
            f.write(nginx_config)
        
        print("✅ Nginx configuration generated")
        return True

# Global production config instance
prod_config = ProductionConfig() 