#!/usr/bin/env python3
"""
EHB-5 Vercel API Handler
Simplified API for Vercel serverless deployment
"""

import datetime
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class EHB5APIHandler(BaseHTTPRequestHandler):
    """API handler for EHB-5 on Vercel"""

    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path

            if path == '/api/health':
                self.send_health_response()
            elif path == '/api/system/status':
                self.send_system_status()
            elif path == '/api/projects':
                self.send_projects_response()
            elif path == '/api/data/files':
                self.send_data_files_response()
            elif path == '/api/ai/agents':
                self.send_ai_agents_response()
            else:
                self.send_not_found()

        except Exception as e:
            self.send_error_response(str(e))

    def do_POST(self):
        """Handle POST requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path

            if path == '/api/auth/login':
                self.handle_login()
            elif path == '/api/auth/register':
                self.handle_register()
            elif path == '/api/projects':
                self.handle_create_project()
            elif path == '/api/data/process':
                self.handle_data_process()
            else:
                self.send_not_found()

        except Exception as e:
            self.send_error_response(str(e))

    def send_response_json(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_health_response(self):
        """Send health check response"""
        data = {
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '2.0.0',
            'environment': os.environ.get('EHB5_ENVIRONMENT', 'production')
        }
        self.send_response_json(data)

    def send_system_status(self):
        """Send system status response"""
        data = {
            'status': 'operational',
            'uptime': '100%',
            'version': '2.0.0',
            'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
            'timestamp': datetime.datetime.now().isoformat(),
            'features': {
                'database': 'connected',
                'api': 'active',
                'authentication': 'enabled',
                'ai_agents': 'operational',
                'monitoring': 'active'
            }
        }
        self.send_response_json(data)

    def send_projects_response(self):
        """Send projects response"""
        data = {
            'projects': [
                {
                    'id': 1,
                    'name': 'EHB-5 Main Project',
                    'description': 'Enterprise Data Processing System',
                    'status': 'active',
                    'created_at': datetime.datetime.now().isoformat()
                }
            ],
            'total': 1
        }
        self.send_response_json(data)

    def send_data_files_response(self):
        """Send data files response"""
        data = {
            'files': [
                {
                    'id': 1,
                    'name': 'config.json',
                    'type': 'json',
                    'size': '2.1 KB',
                    'uploaded_at': datetime.datetime.now().isoformat()
                }
            ],
            'total': 1
        }
        self.send_response_json(data)

    def send_ai_agents_response(self):
        """Send AI agents response"""
        data = {
            'agents': [
                {
                    'id': 1,
                    'name': 'Data Processor Agent',
                    'status': 'active',
                    'type': 'data_processing'
                },
                {
                    'id': 2,
                    'name': 'Config Manager Agent',
                    'status': 'active',
                    'type': 'configuration'
                },
                {
                    'id': 3,
                    'name': 'File Organizer Agent',
                    'status': 'active',
                    'type': 'file_management'
                },
                {
                    'id': 4,
                    'name': 'Code Analyzer Agent',
                    'status': 'active',
                    'type': 'code_analysis'
                },
                {
                    'id': 5,
                    'name': 'Deployment Manager Agent',
                    'status': 'active',
                    'type': 'deployment'
                }
            ],
            'total': 5,
            'status': 'all_operational'
        }
        self.send_response_json(data)

    def handle_login(self):
        """Handle login request"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        username = data.get('username')
        password = data.get('password')

        # Simple authentication for demo
        if username == 'admin' and password == 'admin123':
            token = hashlib.sha256(f"{username}{datetime.datetime.now()}".encode()).hexdigest()
            response_data = {
                'status': 'success',
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': 1,
                    'username': username,
                    'email': 'admin@ehb5.com',
                    'role': 'admin'
                }
            }
            self.send_response_json(response_data)
        else:
            self.send_response_json({'error': 'Invalid credentials'}, 401)

    def handle_register(self):
        """Handle registration request"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        response_data = {
            'status': 'success',
            'message': 'User registered successfully'
        }
        self.send_response_json(response_data, 201)

    def handle_create_project(self):
        """Handle project creation"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        response_data = {
            'status': 'success',
            'message': 'Project created successfully',
            'project_id': 1
        }
        self.send_response_json(response_data, 201)

    def handle_data_process(self):
        """Handle data processing"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        response_data = {
            'status': 'success',
            'message': 'Data processed successfully',
            'result': {
                'processed_items': 1,
                'analysis_complete': True
            }
        }
        self.send_response_json(response_data)

    def send_not_found(self):
        """Send 404 response"""
        self.send_response_json({'error': 'Endpoint not found'}, 404)

    def send_error_response(self, error_message):
        """Send error response"""
        self.send_response_json({'error': error_message}, 500)

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def handler(request, context):
    """Vercel serverless function handler"""
    return EHB5APIHandler().handle_request(request, context)

# For local testing
if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), EHB5APIHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
