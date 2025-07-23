#!/usr/bin/env python3
"""
EHB-5 PUBLIC API Handler - NO AUTHENTICATION REQUIRED
Simplified API for public access
"""

import json
import datetime
import os


def handler(request, context):
    """Vercel serverless function handler - PUBLIC ACCESS"""
    try:
        # Parse the request
        method = request.method
        path = request.path

        # Handle CORS preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': ''
            }

        # Route the request - NO AUTHENTICATION REQUIRED
        if method == 'GET':
            return handle_get_request(path)
        else:
            return create_response({'error': 'Method not allowed'}, 405)

    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        return create_response(
            {'error': 'Internal server error', 'details': str(e)}, 500)


def handle_get_request(path):
    """Handle GET requests - PUBLIC ACCESS"""
    try:
        if path == '/' or path == '':
            return send_root_response()
        elif path == '/api/health':
            return send_health_response()
        elif path == '/api/system/status':
            return send_system_status()
        elif path == '/api/public':
            return send_public_response()
        else:
            return create_response(
                {'error': 'Endpoint not found', 'path': path}, 404)
    except Exception as e:
        print(f"ERROR in handle_get_request: {str(e)}")
        return create_response({'error': 'Request processing error'}, 500)


def create_response(data, status_code=200):
    """Create a Vercel-compatible response"""
    try:
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps(data, default=str)
        }
    except Exception as e:
        print(f"ERROR in create_response: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Response creation failed'})
        }


def send_root_response():
    """Send root response - PUBLIC ACCESS"""
    try:
        data = {
            'message': 'EHB-5 API is running! PUBLIC ACCESS ENABLED',
            'status': 'operational',
            'version': '2.0.0',
            'timestamp': datetime.datetime.now().isoformat(),
            'authentication': 'disabled',
            'endpoints': [
                '/api/health',
                '/api/system/status',
                '/api/public'
            ]
        }
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_root_response: {str(e)}")
        return create_response({'error': 'Root response failed'}, 500)


def send_health_response():
    """Send health check response - PUBLIC ACCESS"""
    try:
        data = {
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '2.0.0',
            'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
            'authentication': 'disabled'
        }
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_health_response: {str(e)}")
        return create_response({'error': 'Health check failed'}, 500)


def send_system_status():
    """Send system status response - PUBLIC ACCESS"""
    try:
        data = {
            'status': 'operational',
            'uptime': '100%',
            'version': '2.0.0',
            'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
            'timestamp': datetime.datetime.now().isoformat(),
            'authentication': 'disabled',
            'features': {
                'database': 'connected',
                'api': 'active',
                'authentication': 'disabled',
                'ai_agents': 'operational',
                'monitoring': 'active'
            }
        }
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_system_status: {str(e)}")
        return create_response({'error': 'System status failed'}, 500)


def send_public_response():
    """Send public access confirmation"""
    try:
        data = {
            'message': 'PUBLIC ACCESS CONFIRMED',
            'status': 'public',
            'timestamp': datetime.datetime.now().isoformat(),
            'authentication': 'disabled',
            'access': 'public'
        }
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_public_response: {str(e)}")
        return create_response({'error': 'Public response failed'}, 500)


# For local testing
if __name__ == "__main__":
    print("EHB-5 PUBLIC API Handler ready for Vercel deployment")
    print("Test endpoints:")
    print("- GET /")
    print("- GET /api/health")
    print("- GET /api/system/status")
    print("- GET /api/public")
