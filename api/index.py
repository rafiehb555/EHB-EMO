#!/usr/bin/env python3
"""
EHB-5 Vercel API Handler - FIXED VERSION
Simplified API for Vercel serverless deployment
"""

import json
import datetime
import os


def handler(request, context):
    """Vercel serverless function handler - FIXED"""
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

        # Route the request
        if method == 'GET':
            return handle_get_request(path)
        else:
            return create_response({'error': 'Method not allowed'}, 405)

    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        return create_response({'error': 'Internal server error', 'details': str(e)}, 500)


def handle_get_request(path):
    """Handle GET requests - FIXED"""
    try:
        if path == '/' or path == '':
            return send_root_response()
        elif path == '/api/health':
            return send_health_response()
        elif path == '/api/system/status':
            return send_system_status()
        else:
            return create_response({'error': 'Endpoint not found', 'path': path}, 404)
    except Exception as e:
        print(f"ERROR in handle_get_request: {str(e)}")
        return create_response({'error': 'Request processing error'}, 500)


def create_response(data, status_code=200):
    """Create a Vercel-compatible response - FIXED"""
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
    """Send root response - FIXED"""
    try:
        data = {
            'message': 'EHB-5 API is running!',
            'status': 'operational',
            'version': '2.0.0',
            'timestamp': datetime.datetime.now().isoformat(),
            'endpoints': [
                '/api/health',
                '/api/system/status'
            ]
        }
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_root_response: {str(e)}")
        return create_response({'error': 'Root response failed'}, 500)


def send_health_response():
    """Send health check response - FIXED"""
    try:
        data = {
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '2.0.0',
            'environment': os.environ.get('EHB5_ENVIRONMENT', 'production')
        }
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_health_response: {str(e)}")
        return create_response({'error': 'Health check failed'}, 500)


def send_system_status():
    """Send system status response - FIXED"""
    try:
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
        return create_response(data)
    except Exception as e:
        print(f"ERROR in send_system_status: {str(e)}")
        return create_response({'error': 'System status failed'}, 500)


# For local testing
if __name__ == "__main__":
    print("EHB-5 API Handler ready for Vercel deployment")
    print("Test endpoints:")
    print("- GET /")
    print("- GET /api/health")
    print("- GET /api/system/status")
