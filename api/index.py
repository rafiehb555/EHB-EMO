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
        # Get request path
        path = request.get('path', '/')

        # Handle different endpoints
        if path == '/' or path == '':
            response_data = {
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
        elif path == '/api/health':
            response_data = {
                'status': 'healthy',
                'timestamp': datetime.datetime.now().isoformat(),
                'version': '2.0.0',
                'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
                'authentication': 'disabled'
            }
        elif path == '/api/system/status':
            response_data = {
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
        elif path == '/api/public':
            response_data = {
                'message': 'PUBLIC ACCESS CONFIRMED',
                'status': 'public',
                'timestamp': datetime.datetime.now().isoformat(),
                'authentication': 'disabled',
                'access': 'public'
            }
        else:
            response_data = {
                'error': 'Endpoint not found',
                'path': path,
                'available_endpoints': [
                    '/',
                    '/api/health',
                    '/api/system/status',
                    '/api/public'
                ]
            }
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': json.dumps(response_data, default=str)
            }

        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps(response_data, default=str)
        }

    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e),
                'timestamp': datetime.datetime.now().isoformat()
            })
        }


# For local testing
if __name__ == "__main__":
    print("EHB-5 PUBLIC API Handler ready for Vercel deployment")
    print("Test endpoints:")
    print("- GET /")
    print("- GET /api/health")
    print("- GET /api/system/status")
    print("- GET /api/public")
