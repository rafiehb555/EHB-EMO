#!/usr/bin/env python3
"""
Python Error Handler
Handles common Python execution errors
"""

import sys
import traceback
import logging
from functools import wraps

def handle_errors(func):
    """Decorator to handle errors gracefully"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            logging.error(traceback.format_exc())
            return None
    return wrapper

def safe_import(module_name):
    """Safely import a module"""
    try:
        return __import__(module_name)
    except ImportError as e:
        logging.warning(f"Could not import {module_name}: {e}")
        return None

def safe_execute_command(command, timeout=30):
    """Safely execute a command"""
    import subprocess
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='ignore'
        )
        return result
    except Exception as e:
        logging.error(f"Command execution failed: {e}")
        return None

class PythonAgentErrorHandler:
    def __init__(self):
        self.errors = []
        self.fixes = []
    
    def log_error(self, error, context=""):
        """Log an error with context"""
        error_info = {
            "error": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self.errors.append(error_info)
        logging.error(f"Error in {context}: {error}")
    
    def apply_fix(self, fix_description):
        """Apply a fix"""
        self.fixes.append(fix_description)
        logging.info(f"Applied fix: {fix_description}")
    
    def get_summary(self):
        """Get error summary"""
        return {
            "total_errors": len(self.errors),
            "total_fixes": len(self.fixes),
            "errors": self.errors,
            "fixes": self.fixes
        }
