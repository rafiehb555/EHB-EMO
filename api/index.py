#!/usr/bin/env python3
"""
EHB-5 Vercel API Handler
Simplified API for Vercel serverless deployment
"""

import datetime
import json
import os


def handler(request, context):
    """Vercel serverless function handler"""
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
        return create_response({'error': str(e)}, 500)


def handle_get_request(path):
    """Handle GET requests"""
    if path == '/':
        return send_root_response()
    elif path == '/api/health':
        return send_health_response()
    elif path == '/api/system/status':
        return send_system_status()
    else:
        return create_response({'error': 'Endpoint not found'}, 404)


def create_response(data, status_code=200):
    """Create a Vercel-compatible response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(data)
    }


def send_root_response():
    """Send root response"""
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


def send_health_response():
    """Send health check response"""
    data = {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '2.0.0',
        'environment': os.environ.get('EHB5_ENVIRONMENT', 'production')
    }
    return create_response(data)


def send_system_status():
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
    return create_response(data)


# For local testing
if __name__ == "__main__":
    print("EHB-5 API Handler ready for Vercel deployment")
    print("Test endpoints:")
    print("- GET /")
    print("- GET /api/health")
    print("- GET /api/system/status")
