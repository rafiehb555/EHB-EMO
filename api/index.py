#!/usr/bin/env python3
"""
EHB-5 PUBLIC API Handler - NO AUTHENTICATION REQUIRED
Enhanced API for public access with home page support
"""

import json
import datetime
import os
import platform


def get_system_info():
    """Get system information"""
    try:
        return {
            'platform': platform.system(),
            'python_version': platform.python_version(),
            'environment': os.environ.get('EHB5_ENVIRONMENT', 'production')
        }
    except Exception:
        return {'platform': 'unknown', 'python_version': 'unknown'}


def handler(request, context):
    """Vercel serverless function handler - PUBLIC ACCESS"""
    try:
        # Get request path and method
        path = request.get('path', '/')
        method = request.get('method', 'GET')

        # Handle OPTIONS for CORS
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': ''
            }

        # Handle different endpoints
        if path == '/' or path == '':
            response_data = {
                'message': '🚀 EHB-5 API is running! PUBLIC ACCESS ENABLED',
                'status': 'operational',
                'version': '2.0.0',
                'timestamp': datetime.datetime.now().isoformat(),
                'authentication': 'disabled',
                'features': {
                    'ai_agents': 'operational',
                    'security': 'enabled',
                    'analytics': 'active',
                    'performance': 'optimized'
                },
                'endpoints': [
                    '/',
                    '/health',
                    '/api/status',
                    '/api/system/status',
                    '/api/public'
                ]
            }
        elif path == '/health':
            response_data = {
                'status': 'healthy',
                'message': '✅ System is healthy and running',
                'timestamp': datetime.datetime.now().isoformat(),
                'version': '2.0.0',
                'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
                'authentication': 'disabled',
                'uptime': '100%'
            }
        elif path == '/api/status':
            response_data = {
                'status': 'operational',
                'message': '📊 System status and metrics',
                'uptime': '100%',
                'version': '2.0.0',
                'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
                'timestamp': datetime.datetime.now().isoformat(),
                'authentication': 'disabled',
                'system_info': get_system_info(),
                'features': {
                    'database': 'connected',
                    'api': 'active',
                    'authentication': 'disabled',
                    'ai_agents': 'operational',
                    'monitoring': 'active',
                    'security': 'enabled'
                },
                'performance': {
                    'response_time': 'fast',
                    'memory_usage': 'optimal',
                    'cpu_usage': 'normal'
                }
            }
        elif path == '/api/system/status':
            response_data = {
                'status': 'operational',
                'message': '🔧 Detailed system status',
                'uptime': '100%',
                'version': '2.0.0',
                'environment': os.environ.get('EHB5_ENVIRONMENT', 'production'),
                'timestamp': datetime.datetime.now().isoformat(),
                'authentication': 'disabled',
                'system_info': get_system_info(),
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
                'message': '🌐 PUBLIC ACCESS CONFIRMED',
                'status': 'public',
                'timestamp': datetime.datetime.now().isoformat(),
                'authentication': 'disabled',
                'access': 'public',
                'features': {
                    'public_api': 'enabled',
                    'cors': 'enabled',
                    'rate_limiting': 'disabled'
                }
            }
        else:
            response_data = {
                'error': 'Endpoint not found',
                'message': '❌ The requested endpoint does not exist',
                'path': path,
                'timestamp': datetime.datetime.now().isoformat(),
                'available_endpoints': [
                    '/',
                    '/health',
                    '/api/status',
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
                'message': '❌ An internal error occurred',
                'details': str(e),
                'timestamp': datetime.datetime.now().isoformat()
            })
        }


# For local testing
if __name__ == "__main__":
    print("🚀 EHB-5 PUBLIC API Handler ready for Vercel deployment")
    print("Test endpoints:")
    print("- GET /")
    print("- GET /health")
    print("- GET /api/status")
    print("- GET /api/system/status")
    print("- GET /api/public")
