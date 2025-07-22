#!/usr/bin/env python3
"""
EHB-5 Vercel API Handler
Serverless function for Vercel deployment
"""

import os
import sys
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database import db
    from auth_manager import auth
    from data_processor import DataProcessor
    from ai_agents import agent_manager
    from monitoring import system_monitor
    from security_manager import security_manager
except ImportError as e:
    print(f"Import error: {e}")

class VercelHandler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            # Set CORS headers
            self.send_cors_headers()
            
            if path == "/api/health":
                self.handle_health_check()
            elif path == "/api/system/status":
                self.handle_system_status()
            elif path == "/api/system/logs":
                self.handle_system_logs(query_params)
            elif path == "/api/projects":
                self.handle_get_projects()
            elif path == "/api/data/files":
                self.handle_get_files()
            elif path == "/api/ai/agents":
                self.handle_ai_agents()
            elif path == "/api/monitoring/metrics":
                self.handle_monitoring_metrics()
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            # Set CORS headers
            self.send_cors_headers()
            
            # Get request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            if path == "/api/auth/login":
                self.handle_login(data)
            elif path == "/api/auth/register":
                self.handle_register(data)
            elif path == "/api/projects":
                self.handle_create_project(data)
            elif path == "/api/data/process":
                self.handle_data_process(data)
            elif path == "/api/ai/agents/execute":
                self.handle_ai_execute(data)
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Type', 'application/json')
    
    def handle_health_check(self):
        """Handle health check endpoint"""
        response = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "environment": os.getenv("EHB5_ENVIRONMENT", "production"),
            "deployment": "vercel"
        }
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_system_status(self):
        """Handle system status endpoint"""
        try:
            # Get system metrics
            metrics = system_monitor.get_metrics()
            health_status = system_monitor.get_health_status()
            
            response = {
                "status": "operational",
                "uptime": "2 hours",
                "version": "2.0.0",
                "deployment": "vercel",
                "components": {
                    "database": "healthy",
                    "api": "healthy",
                    "ai_agents": "active",
                    "monitoring": "active"
                },
                "metrics": metrics,
                "health": health_status
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"System status error: {str(e)}")
    
    def handle_system_logs(self, query_params):
        """Handle system logs endpoint"""
        try:
            level = query_params.get('level', ['INFO'])[0]
            limit = int(query_params.get('limit', ['50'])[0])
            
            # Get logs from database
            logs = db.get_system_logs(level=level, limit=limit)
            
            response = {
                "logs": logs,
                "count": len(logs),
                "level": level
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Logs error: {str(e)}")
    
    def handle_get_projects(self):
        """Handle get projects endpoint"""
        try:
            projects = db.get_all_projects()
            
            response = {
                "projects": projects,
                "count": len(projects)
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Projects error: {str(e)}")
    
    def handle_get_files(self):
        """Handle get files endpoint"""
        try:
            files = db.get_data_files()
            
            response = {
                "files": files,
                "count": len(files)
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Files error: {str(e)}")
    
    def handle_ai_agents(self):
        """Handle AI agents status endpoint"""
        try:
            agents_status = agent_manager.get_all_agents_status()
            
            response = {
                "agents": agents_status,
                "total_agents": len(agents_status),
                "active_agents": len([a for a in agents_status if a.get('status') == 'active'])
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"AI agents error: {str(e)}")
    
    def handle_monitoring_metrics(self):
        """Handle monitoring metrics endpoint"""
        try:
            metrics = system_monitor.get_metrics()
            alerts = system_monitor.get_alerts()
            
            response = {
                "metrics": metrics,
                "alerts": alerts,
                "alerts_count": len(alerts)
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Monitoring error: {str(e)}")
    
    def handle_login(self, data):
        """Handle login endpoint"""
        try:
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                self.send_error(400, "Username and password required")
                return
            
            # Authenticate user
            user = auth.authenticate_user(username, password)
            if user:
                token = auth.generate_token(user['id'])
                
                response = {
                    "status": "success",
                    "message": "Login successful",
                    "token": token,
                    "user": {
                        "id": user['id'],
                        "username": user['username']
                    }
                }
                
                self.send_response(200)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(401, "Invalid credentials")
                
        except Exception as e:
            self.send_error(500, f"Login error: {str(e)}")
    
    def handle_register(self, data):
        """Handle register endpoint"""
        try:
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            
            if not username or not password:
                self.send_error(400, "Username and password required")
                return
            
            # Create user
            user_id = db.create_user(username, password, email)
            
            response = {
                "status": "success",
                "message": "User registered successfully",
                "user_id": user_id
            }
            
            self.send_response(201)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Registration error: {str(e)}")
    
    def handle_create_project(self, data):
        """Handle create project endpoint"""
        try:
            name = data.get('name')
            description = data.get('description', '')
            
            if not name:
                self.send_error(400, "Project name required")
                return
            
            # Create project
            project_id = db.create_project(name, description, user_id=1)
            
            response = {
                "status": "success",
                "message": "Project created successfully",
                "project_id": project_id
            }
            
            self.send_response(201)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Project creation error: {str(e)}")
    
    def handle_data_process(self, data):
        """Handle data processing endpoint"""
        try:
            input_data = data.get('data')
            operation = data.get('operation', 'analyze')
            
            if not input_data:
                self.send_error(400, "Data required")
                return
            
            # Process data
            processor = DataProcessor()
            result = processor.process_data(input_data, operation)
            
            response = {
                "status": "success",
                "result": result,
                "operation": operation
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Data processing error: {str(e)}")
    
    def handle_ai_execute(self, data):
        """Handle AI agent execution endpoint"""
        try:
            agent_name = data.get('agent')
            task_data = data.get('data', {})
            
            if not agent_name:
                self.send_error(400, "Agent name required")
                return
            
            # Execute AI agent
            result = agent_manager.execute_agent(agent_name, task_data)
            
            response = {
                "status": "success",
                "agent": agent_name,
                "result": result
            }
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"AI execution error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

# Vercel serverless function handler
def handler(request, context):
    """Vercel serverless function entry point"""
    return VercelHandler().handle_request(request) 