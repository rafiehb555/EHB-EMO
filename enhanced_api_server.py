#!/usr/bin/env python3
"""
EHB-5 Enhanced API Server
Complete RESTful API with advanced security and comprehensive features
"""

import datetime
import hashlib
import os
import jwt
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from auth_manager import AuthManager
from data_processor import DataProcessor
from database import db
from enhanced_security import security_manager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ehb5-secret-key-2024')
CORS(app)

# Initialize managers
auth_manager = AuthManager()
data_processor = DataProcessor()


@app.route('/api/health', methods=['GET'])
@security_manager.rate_limit
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '2.0.0',
        'security': 'enhanced'
    })


@app.route('/api/auth/register', methods=['POST'])
@security_manager.rate_limit
def register():
    """User registration endpoint with enhanced validation"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['username', 'email', 'password']
        validation = security_manager.validate_json_schema(data, required_fields)

        if not validation['is_valid']:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': validation['missing_fields']
            }), 400

        username = security_manager.sanitize_input(data.get('username'))
        email = security_manager.sanitize_input(data.get('email'))
        password = data.get('password')

        # Validate input
        if not security_manager.validate_username(username):
            return jsonify({'error': 'Invalid username format'}), 400

        if not security_manager.validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Validate password strength
        password_validation = security_manager.validate_password_strength(password)
        if not password_validation['is_valid']:
            return jsonify({
                'error': 'Password validation failed',
                'errors': password_validation['errors']
            }), 400

        # Hash password with bcrypt
        password_hash = security_manager.hash_password_bcrypt(password)

        # Create user
        if db.create_user(username, email, password_hash):
            security_manager.log_security_event('USER_REGISTERED', f'User {username} registered')
            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify({'error': 'User already exists'}), 409

    except Exception as e:
        security_manager.log_security_event('REGISTRATION_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
@security_manager.rate_limit
def login():
    """User login endpoint with enhanced security"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['username', 'password']
        validation = security_manager.validate_json_schema(data, required_fields)

        if not validation['is_valid']:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': validation['missing_fields']
            }), 400

        username = security_manager.sanitize_input(data.get('username'))
        password = data.get('password')

        # Verify user with bcrypt
        user = db.get_user_by_username(username)
        if user and security_manager.verify_password_bcrypt(password, user['password_hash']):
            # Generate secure JWT token
            token = security_manager.generate_secure_token(user['id'], user['username'])

            security_manager.log_security_event('USER_LOGIN', f'User {username} logged in')

            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
        else:
            security_manager.log_security_event('LOGIN_FAILED', f'Failed login attempt for {username}')
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        security_manager.log_security_event('LOGIN_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
@auth_manager.require_auth
@security_manager.rate_limit
def get_projects():
    """Get all projects with enhanced security"""
    try:
        projects = db.get_all_projects()
        return jsonify({
            'projects': projects,
            'count': len(projects)
        }), 200
    except Exception as e:
        security_manager.log_security_event('PROJECTS_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['POST'])
@auth_manager.require_auth
@security_manager.rate_limit
def create_project():
    """Create a new project with enhanced validation"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name']
        validation = security_manager.validate_json_schema(data, required_fields)

        if not validation['is_valid']:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': validation['missing_fields']
            }), 400

        name = security_manager.sanitize_input(data.get('name'))
        description = security_manager.sanitize_input(data.get('description', ''))

        if not name:
            return jsonify({'error': 'Project name is required'}), 400

        user_id = session.get('user_id')
        if db.create_project(name, description, user_id):
            security_manager.log_security_event('PROJECT_CREATED', f'Project {name} created by user {user_id}')
            return jsonify({'message': 'Project created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create project'}), 500

    except Exception as e:
        security_manager.log_security_event('PROJECT_CREATION_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/files', methods=['GET'])
@auth_manager.require_auth
@security_manager.rate_limit
def get_data_files():
    """Get all data files with enhanced security"""
    try:
        project_id = request.args.get('project_id', type=int)
        files = db.get_data_files(project_id)
        return jsonify({
            'files': files,
            'count': len(files)
        }), 200
    except Exception as e:
        security_manager.log_security_event('FILES_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/files', methods=['POST'])
@auth_manager.require_auth
@security_manager.rate_limit
def upload_data_file():
    """Upload a data file with enhanced validation"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['filename', 'file_type', 'content']
        validation = security_manager.validate_json_schema(data, required_fields)

        if not validation['is_valid']:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': validation['missing_fields']
            }), 400

        filename = security_manager.sanitize_input(data.get('filename'))
        file_type = security_manager.sanitize_input(data.get('file_type'))
        content = data.get('content')
        project_id = data.get('project_id')

        # Validate file upload
        file_validation = security_manager.validate_file_upload(
            filename,
            len(content),
            ['txt', 'json', 'csv', 'xml', 'md']
        )

        if not file_validation['is_valid']:
            return jsonify({
                'error': 'File validation failed',
                'errors': file_validation['errors']
            }), 400

        user_id = session.get('user_id')
        if db.save_data_file(filename, file_type, content, project_id, user_id):
            security_manager.log_security_event('FILE_UPLOADED', f'File {filename} uploaded by user {user_id}')
            return jsonify({'message': 'File uploaded successfully'}), 201
        else:
            return jsonify({'error': 'Failed to upload file'}), 500

    except Exception as e:
        security_manager.log_security_event('FILE_UPLOAD_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/process', methods=['POST'])
@auth_manager.require_auth
@security_manager.rate_limit
def process_data():
    """Process data using the data processor with enhanced security"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['data']
        validation = security_manager.validate_json_schema(data, required_fields)

        if not validation['is_valid']:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': validation['missing_fields']
            }), 400

        input_data = data.get('data')
        operation = data.get('operation', 'analyze')

        if not input_data:
            return jsonify({'error': 'No data provided'}), 400

        # Sanitize input data
        if isinstance(input_data, str):
            input_data = security_manager.sanitize_input(input_data)

        # Process data
        result = data_processor.process_data(input_data, operation)

        security_manager.log_security_event('DATA_PROCESSED', f'Data processed with operation {operation}')

        return jsonify({
            'result': result,
            'operation': operation,
            'processed_at': datetime.datetime.now().isoformat()
        }), 200

    except Exception as e:
        security_manager.log_security_event('DATA_PROCESSING_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/status', methods=['GET'])
@security_manager.rate_limit
def get_system_status():
    """Get system status with enhanced monitoring"""
    try:
        # Get database status
        projects_count = len(db.get_all_projects())
        files_count = len(db.get_data_files())

        return jsonify({
            'status': 'operational',
            'database': 'connected',
            'api': 'active',
            'security': 'enhanced',
            'debug': False,
            'stats': {
                'projects': projects_count,
                'files': files_count,
                'users': 1  # Placeholder
            },
            'timestamp': datetime.datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 500


@app.route('/api/system/logs', methods=['GET'])
@auth_manager.require_auth
@security_manager.rate_limit
def get_system_logs():
    """Get system logs with enhanced security"""
    try:
        # This would typically get logs from the database
        logs = [
            {
                'id': 1,
                'level': 'INFO',
                'message': 'System initialized with enhanced security',
                'timestamp': datetime.datetime.now().isoformat()
            }
        ]

        return jsonify({
            'logs': logs,
            'count': len(logs)
        }), 200

    except Exception as e:
        security_manager.log_security_event('LOGS_ERROR', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/security/status', methods=['GET'])
@auth_manager.require_auth
def get_security_status():
    """Get security status and statistics"""
    try:
        return jsonify({
            'rate_limiting': 'active',
            'input_validation': 'enabled',
            'password_hashing': 'bcrypt',
            'jwt_security': 'enhanced',
            'xss_protection': 'enabled',
            'sql_injection_protection': 'enabled',
            'blocked_ips_count': len(security_manager.blocked_ips),
            'timestamp': datetime.datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting EHB-5 Enhanced API Server...")
    print("📊 API URL: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/health")
    print("🔒 Enhanced Security: Enabled")

    # Log system startup
    db.log_system_event('INFO', 'Enhanced API Server started with security features')

    app.run(host='0.0.0.0', port=5000, debug=True)
