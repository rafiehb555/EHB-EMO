#!/usr/bin/env python3
"""
EHB-5 API Documentation Generator
Comprehensive API documentation and testing interface
"""

import json
import inspect
from datetime import datetime
from typing import Dict, List, Any
from api_server import app


class APIDocumentation:
    """API documentation generator"""

    def __init__(self) -> None:
        self.endpoints = []
        self.examples = {}
        self.schemas = {}
        self.generate_documentation()

    def generate_documentation(self) -> None:
        """Generate comprehensive API documentation"""
        self._collect_endpoints()
        self._generate_examples()
        self._generate_schemas()

    def _collect_endpoints(self) -> None:
        """Collect all API endpoints"""
        self.endpoints = [
            {
                "path": "/api/health",
                "method": "GET",
                "description": "System health check",
                "response": {
                    "status": "healthy",
                    "timestamp": "2024-01-01T00:00:00",
                    "version": "2.0.0"
                }
            },
            {
                "path": "/api/auth/register",
                "method": "POST",
                "description": "User registration",
                "request": {
                    "username": "string",
                    "password": "string",
                    "email": "string"
                },
                "response": {
                    "status": "success",
                    "message": "User registered successfully",
                    "user_id": 1
                }
            },
            {
                "path": "/api/auth/login",
                "method": "POST",
                "description": "User authentication",
                "request": {
                    "username": "string",
                    "password": "string"
                },
                "response": {
                    "status": "success",
                    "token": "jwt_token_here",
                    "user": {
                        "id": 1,
                        "username": "admin"
                    }
                }
            },
            {
                "path": "/api/projects",
                "method": "GET",
                "description": "Get all projects",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "projects": [
                        {
                            "id": 1,
                            "name": "Project Name",
                            "description": "Project description",
                            "created_at": "2024-01-01T00:00:00"
                        }
                    ]
                }
            },
            {
                "path": "/api/projects",
                "method": "POST",
                "description": "Create new project",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "request": {
                    "name": "string",
                    "description": "string"
                },
                "response": {
                    "status": "success",
                    "project_id": 1
                }
            },
            {
                "path": "/api/data/files",
                "method": "GET",
                "description": "Get all data files",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "files": [
                        {
                            "id": 1,
                            "filename": "data.txt",
                            "size": 1024,
                            "uploaded_at": "2024-01-01T00:00:00"
                        }
                    ]
                }
            },
            {
                "path": "/api/data/process",
                "method": "POST",
                "description": "Process data with specified operation",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "request": {
                    "data": "string",
                    "operation": "analyze|validate|transform|summarize|extract"
                },
                "response": {
                    "status": "success",
                    "result": "processed_data",
                    "operation": "analyze"
                }
            },
            {
                "path": "/api/system/status",
                "method": "GET",
                "description": "Get system status",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "response": {
                    "status": "operational",
                    "uptime": "2 hours",
                    "version": "2.0.0",
                    "components": {
                        "database": "healthy",
                        "api": "healthy",
                        "ai_agents": "active"
                    }
                }
            },
            {
                "path": "/api/system/logs",
                "method": "GET",
                "description": "Get system logs",
                "headers": {
                    "Authorization": "Bearer <token>"
                },
                "query_params": {
                    "level": "INFO|WARNING|ERROR",
                    "limit": "number"
                },
                "response": {
                    "logs": [
                        {
                            "timestamp": "2024-01-01T00:00:00",
                            "level": "INFO",
                            "message": "System event"
                        }
                    ]
                }
            }
        ]

    def _generate_examples(self) -> None:
        """Generate API usage examples"""
        self.examples = {
            "authentication": {
                "register": {
"curl": 'curl - X POST http: // localhost: 5000 / api / auth / register \\\n -
    H
"Content-Type: application/json" \\\n - d \'{"username": "newuser", "password":
"SecurePass123!", "email": "user@example.com"}\'',
                    "python": '''import requests

url = "http://localhost:5000/api/auth/register"
data = {
    "username": "newuser",
    "password": "SecurePass123!",
    "email": "user@example.com"
}
response = requests.post(url, json=data)
print(response.json())'''
                },
                "login": {
"curl": 'curl - X POST http: // localhost: 5000 / api / auth / login \\\n - H
"Content-Type: application/json" \\\n - d \'{"username": "admin", "password":
"admin123"}\'',
                    "python": '''import requests

url = "http://localhost:5000/api/auth/login"
data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(url, json=data)
token = response.json()["token"]
print(f"Token: {token}")'''
                }
            },
            "data_processing": {
                "analyze": {
"curl": 'curl - X POST http: // localhost: 5000 / api / data / process \\\n - H
"Content-Type: application/json" \\\n - H "Authorization: Bearer <token>" \\\n
- d \'{"data": "Sample data for analysis", "operation": "analyze"}\'',
                    "python": '''import requests

url = "http://localhost:5000/api/data/process"
headers = {"Authorization": "Bearer <token>"}
data = {
    "data": "Sample data for analysis",
    "operation": "analyze"
}
response = requests.post(url, json=data, headers=headers)
print(response.json())'''
                }
            },
            "system_monitoring": {
                "health_check": {
                    "curl": "curl http://localhost:5000/api/health",
                    "python": '''import requests

response = requests.get("http://localhost:5000/api/health")
print(response.json())'''
                },
                "system_status": {
                    "curl": 'curl - H "Authorization: Bearer <token>" \\\n
                    http: // localhost: 5000 / api / system / status',
                    "python": '''import requests

headers = {"Authorization": "Bearer <token>"}
response = requests.get("http://localhost:5000/api/system/status",
    headers=headers)
print(response.json())'''
                }
            }
        }

    def _generate_schemas(self) -> None:
        """Generate data schemas"""
        self.schemas = {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            },
            "Project": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "user_id": {"type": "integer"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            },
            "DataFile": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "filename": {"type": "string"},
                    "size": {"type": "integer"},
                    "content_type": {"type": "string"},
                    "uploaded_at": {"type": "string", "format": "date-time"}
                }
            },
            "SystemLog": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "timestamp": {"type": "string", "format": "date-time"},
"level": {"type": "string", "enum": ["INFO", "WARNING", "ERROR"]},
                    "message": {"type": "string"}
                }
            }
        }

    def generate_markdown_docs(self) -> str:
        """Generate markdown documentation"""
        md = f"""# EHB-5 API Documentation

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

The EHB-5 API provides comprehensive data processing, user management, and
    system monitoring capabilities.

### Base URL
```
http://localhost:5000
```

### Authentication
Most endpoints require authentication using JWT tokens. Include the token in
    the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

"""

        for endpoint in self.endpoints:
            md += f"### {endpoint['method']} {endpoint['path']}\n\n"
            md += f"{endpoint['description']}\n\n"

            if 'headers' in endpoint:
                md += "**Headers:**\n"
                for key, value in endpoint['headers'].items():
                    md += f"- `{key}`: {value}\n"
                md += "\n"

            if 'query_params' in endpoint:
                md += "**Query Parameters:**\n"
                for key, value in endpoint['query_params'].items():
                    md += f"- `{key}`: {value}\n"
                md += "\n"

            if 'request' in endpoint:
                md += "**Request Body:**\n"


md += f"```json\n{json.dumps(endpoint['request'], indent=2)}\n```\n\n"

md += "**Response:**\n"
md += f"```json\n{json.dumps(endpoint['response'], indent=2)}\n```\n\n"
md += "---\n\n"

return md


def generate_html_docs(self) -> str:
    """Generate HTML documentation"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EHB-5 API Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
.endpoint {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd;
    border-radius: 5px; }}
        .method {{ font-weight: bold; color: #007bff; }}
        .path {{ font-family: monospace; background: #f8f9fa; padding: 5px; }}
        .description {{ color: #666; margin: 10px 0; }}
.code {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x:
    auto; }}
        .example {{ margin: 10px 0; }}
        .example h4 {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h1>EHB-5 API Documentation</h1>
    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h2>Base URL</h2>
    <p><code>http://localhost:5000</code></p>

    <h2>Authentication</h2>
<p>Most endpoints require authentication using JWT tokens. Include the token in
    the Authorization header:</p>
    <div class="code">
        Authorization: Bearer &lt;your_token&gt;
    </div>

    <h2>Endpoints</h2>
"""

    for endpoint in self.endpoints:
        html += f"""
    <div class="endpoint">
<h3><span class="method">{endpoint['method']}</span> <span
    class="path">{endpoint['path']}</span></h3>
        <p class="description">{endpoint['description']}</p>
"""

        if 'headers' in endpoint:
            html += "        <h4>Headers:</h4><ul>"
            for key, value in endpoint['headers'].items():
                html += f"<li><code>{key}</code>: {value}</li>"
                html += "</ul>"

            if 'query_params' in endpoint:
                html += "        <h4>Query Parameters:</h4><ul>"
                for key, value in endpoint['query_params'].items():
                    html += f"<li><code>{key}</code>: {value}</li>"
                html += "</ul>"

            if 'request' in endpoint:
                html += f"""
        <h4>Request Body:</h4>
        <div class="code">
            <pre>{json.dumps(endpoint['request'], indent=2)}</pre>
        </div>
"""

            html += f"""
        <h4>Response:</h4>
        <div class="code">
            <pre>{json.dumps(endpoint['response'], indent=2)}</pre>
        </div>
    </div>
"""

        html += """
    <h2>Examples</h2>
"""

        for category, examples in self.examples.items():
            html += f"    <h3>{category.title()}</h3>"
            for name, example in examples.items():
                html += f"""
    <div class="example">
        <h4>{name.title()}</h4>
"""
                for lang, code in example.items():
                    html += f"""
        <h5>{lang.upper()}</h5>
        <div class="code">
            <pre>{code}</pre>
        </div>
"""
                html += "    </div>"

        html += """
</body>
</html>
"""

        return html

    def generate_postman_collection(self) -> Dict:
        """Generate Postman collection"""
        collection = {
            "info": {
                "name": "EHB-5 API",
                "description": "EHB-5 Data Processing and Management API",
                "version": "2.0.0"
            },
            "variable": [
                {
                    "key": "base_url",
                    "value": "http://localhost:5000"
                },
                {
                    "key": "token",
                    "value": "your_jwt_token_here"
                }
            ],
            "item": []
        }

        for endpoint in self.endpoints:
            item = {
                "name": f"{endpoint['method']} {endpoint['path']}",
                "request": {
                    "method": endpoint['method'],
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}{{path}}",
                        "host": ["{{base_url}}"],
                        "path": endpoint['path'].split('/')[1:]
                    }
                }
            }

            # Add headers
            if 'headers' in endpoint:
                for key, value in endpoint['headers'].items():
                    if key == 'Authorization':
                        item['request']['header'].append({
                            "key": key,
                            "value": "Bearer {{token}}"
                        })
                    else:
                        item['request']['header'].append({
                            "key": key,
                            "value": value
                        })

            # Add request body
            if 'request' in endpoint:
                item['request']['body'] = {
                    "mode": "raw",
                    "raw": json.dumps(endpoint['request'], indent=2),
                    "options": {
                        "raw": {
                            "language": "json"
                        }
                    }
                }

            collection['item'].append(item)

        return collection


# Global API documentation instance
api_docs = APIDocumentation()
