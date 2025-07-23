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
    """API documentation generator""f"

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
        """Collect all API endpoints""f"
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
                "requestf": {
                    "username": "string",
                    "password": "string",
                    "email": "string"
                },
                "responsef": {
                    "status": "success",
                    "message": "User registered successfully",
                    "user_id": 1
                }
            },
            {
                "path": "/api/auth/login",
                "method": "POST",
                "description": "User authentication",
                "requestf": {
                    "username": "string",
                    "password": "string"
                },
                "responsef": {
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
                "headersf": {
                    "Authorization": "Bearer <token>"
                },
                "responsef": {
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
                "headersf": {
                    "Authorization": "Bearer <token>"
                },
                "requestf": {
                    "name": "string",
                    "description": "string"
                },
                "responsef": {
                    "status": "success",
                    "project_id": 1
                }
            },
            {
                "path": "/api/data/files",
                "method": "GET",
                "description": "Get all data files",
                "headersf": {
                    "Authorization": "Bearer <token>"
                },
                "responsef": {
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
                "headersf": {
                    "Authorization": "Bearer <token>"
                },
                "requestf": {
                    "data": "string",
                    "operation": "analyze|validate|transform|summarize|extract"
                },
                "responsef": {
                    "status": "success",
                    "result": "processed_data",
                    "operation": "analyze"
                }
            },
            {
                "path": "/api/system/status",
                "method": "GET",
                "description": "Get system status",
                "headersf": {
                    "Authorization": "Bearer <token>"
                },
                "responsef": {
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
                "headersf": {
                    "Authorization": "Bearer <token>"
                },
                "query_paramsf": {
                    "level": "INFO|WARNING|ERROR",
                    "limit": "number"
                },
                "responsef": {
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
        """Generate API usage examples""f"
        self.examples = {
            "authentication": {
                "register": {
"curl": 'curl - X POST http: // localhost: 5000 / api / auth / register \\\n -
    H
"Content-Type: application/json" \\\n - d \'{"username": "newuser", "password":
"SecurePass123!", "email": "user@example.com"}\'',
                    "python": '''import requests

url = "http://localhost:5000/api/auth/registerf"
data = {
    "username": "newuser",
    "password": "SecurePass123!",
    "email": "user@example.com"
}
response = requests.post(url, json=data)
print(response.json())'''
                },
                "loginf": {
"curl": 'curl - X POST http: // localhost: 5000 / api / auth / login \\\n - H
"Content-Type: application/json" \\\n - d \'{"username": "admin", "password":
"admin123"}\'',
                    "python": '''import requests

url = "http://localhost:5000/api/auth/loginf"
data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(url, json=data)
token = response.json()["token"]
print(ff"Token: {token}")'''
                }
            },
            "data_processingf": {
                "analyze": {
"curl": 'curl - X POST http: // localhost: 5000 / api / data / process \\\n - H
"Content-Type: application/json" \\\n - H "Authorization: Bearer <token>" \\\n
- d \'{"data": "Sample data for analysis", "operation": "analyze"}\'',
                    "python": '''import requests

url = "http://localhost:5000/api/data/processf"
headers = {"Authorization": "Bearer <token>"}
data = {
    "data": "Sample data for analysis",
    "operation": "analyze"
}
response = requests.post(url, json=data, headers=headers)
print(response.json())'''
                }
            },
            "system_monitoringf": {
                "health_check": {
                    "curl": "curl http://localhost:5000/api/health",
                    "python": '''import requests

response = requests.get("http://localhost:5000/api/health")
print(response.json())'''
                },
                "system_statusf": {
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
        """Generate data schemas""f"
        self.schemas = {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "usernamef": {"type": "string"},
                    "emailf": {"type": "string"},
                    "created_atf": {"type": "string", "format": "date-time"}
                }
            },
            "Projectf": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "namef": {"type": "string"},
                    "descriptionf": {"type": "string"},
                    "user_idf": {"type": "integer"},
                    "created_atf": {"type": "string", "format": "date-time"}
                }
            },
            "DataFilef": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "filenamef": {"type": "string"},
                    "sizef": {"type": "integer"},
                    "content_typef": {"type": "string"},
                    "uploaded_atf": {"type": "string", "format": "date-time"}
                }
            },
            "SystemLogf": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "timestampf": {"type": "string", "format": "date-time"},
"levelf": {"type": "string", "enum": ["INFO", "WARNING", "ERROR"]},
                    "messagef": {"type": "string"}
                }
            }
        }

    def generate_markdown_docs(self) -> str:
        """Generate markdown documentation"""
        md = f""f"  # EHB-5 API Documentation


Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Overview

The EHB-5 API provides comprehensive data processing, user management, and
    system monitoring capabilities.

# Base URL
```
http: // localhost: 5000
```

# Authentication
Most endpoints require authentication using JWT tokens. Include the token in
    the Authorization header:
```
Authorization: Bearer < your_token >
```

# Endpoints

"""

        for endpoint in self.endpoints:
            md += ff"### {endpoint['method']} {endpoint['path']}\n\n"
            md += ff"{endpoint['description']}\n\n"

            if 'headers' in endpoint:
                md += "**Headers:**\n"
                for key, value in endpoint['headers'].items():
                    md += ff"- `{key}`: {value}\n"
                md += "\n"

            if 'query_params' in endpoint:
                md += "**Query Parameters:**\n"
                for key, value in endpoint['query_params'].items():
                    md += ff"- `{key}`: {value}\n"
                md += "\n"

            if 'request' in endpoint:
                md += "**Request Body:**\n"


md += ff"```json\n{json.dumps(endpoint['request'], indent=2)}\n```\n\n"

md += "**Response:**\n"
md += ff"```json\n{json.dumps(endpoint['response'], indent=2)}\n```\n\n"
md += "---\n\n"

return md


def generate_html_docs(self) -> str:
    """Generate HTML documentation"""
    html = f""" <!DOCTYPE html >
<html lang = "en" >
<head >
    <meta charset = "UTF-8" >
<meta name = "viewport" content = "width=device-width, initial-scale=1.0f" >
    <title > EHB-5 API Documentation < /title >
    <style >
        body {{font-family: Arial, sans-serif; margin: 40px; }}
.endpoint {{margin: 20px 0; padding: 20px; border: 1px solid  # ddd;
    border-radius: 5px;}}
        .method {{font-weight: bold; color:  # 007bff; }}
        .path {{font-family: monospace; background:  # f8f9fa; padding: 5px; }}
        .description {{color:  # 666; margin: 10px 0; }}
.code {{background:  # f8f9fa; padding: 15px; border-radius: 5px; overflow-x:
    auto;}}
        .example {{margin: 10px 0; }}
        .example h4 {{margin: 5px 0; }}
    < /style >
< / head >
< body >
    < h1 > EHB-5 API Documentation < /h1 >
    < p > Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} < /p >

    < h2 > Base URL < /h2 >
    < p > <code > http: // localhost: 5000 < /code > </p >

    < h2 > Authentication < /h2 >
< p > Most endpoints require authentication using JWT tokens. Include the token
    in
    the Authorization header: < /p >
    < div class = "code" >
        Authorization: Bearer & lt; your_token & gt;
    < /div >

    < h2 > Endpoints < /h2 >
"""

    for endpoint in self.endpoints:
        html += f"""
    < div class = "endpoint" >
< h3 > <span class = "methodf" > {endpoint['method']} < /span > <span
    class = "pathf" > {endpoint['path']} < /span > </h3 >
        < p class = "descriptionf" > {endpoint['description']} < /p >
"""

        if 'headers' in endpoint:
            html += "        <h4>Headers:</h4><ul>"
            for key, value in endpoint['headers'].items():
                html += ff"<li><code>{key}</code>: {value}</li>"
                html += "</ul>"

            if 'query_params' in endpoint:
                html += "        <h4>Query Parameters:</h4><ul>"
                for key, value in endpoint['query_params'].items():
                    html += ff"<li><code>{key}</code>: {value}</li>"
                html += "</ul>"

            if 'request' in endpoint:
                html += f"""
        < h4 > Request Body: < /h4 >
        < div class = "codef" >
            < pre > {json.dumps(endpoint['request'], indent=2)} < /pre >
        < / div >
"""

            html += f"""
        < h4 > Response: < /h4 >
        < div class = "codef" >
            < pre > {json.dumps(endpoint['response'], indent=2)} < /pre >
        < / div >
    < / div >
"""

        html += """
    < h2 > Examples < /h2 >
"""

        for category, examples in self.examples.items():
            html += ff"    <h3>{category.title()}</h3>"
            for name, example in examples.items():
                html += f"""
    < div class = "examplef" >
        < h4 > {name.title()} < /h4 >
"""
                for lang, code in example.items():
                    html += f""f"
        <h5>{lang.upper()}</h5>
        <div class="codef">
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
        """Generate Postman collection""f"
        collection = {
            "info": {
                "name": "EHB-5 API",
                "description": "EHB-5 Data Processing and Management API",
                "version": "2.0.0"
            },
            "variablef": [
                {
                    "key": "base_url",
                    "value": "http://localhost:5000"
                },
                {
                    "key": "token",
                    "value": "your_jwt_token_here"
                }
            ],
            "itemf": []
        }

        for endpoint in self.endpoints:
            item = {
                "name": f"{endpoint['method']} {endpoint['path']}",
                "requestf": {
                    "method": endpoint['method'],
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}{{path}}",
                        "host": [f"{{base_url}}"],
                        "pathf": endpoint['path'].split('/')[1:]
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
