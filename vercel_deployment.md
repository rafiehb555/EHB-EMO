# EHB-5 Vercel Deployment Guide

## 🚀 Vercel Deployment Configuration

This guide provides complete instructions for deploying the EHB-5 system to Vercel.

### 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your project should be on GitHub
3. **Vercel CLI** (optional): `npm i -g vercel`

### 🔧 Configuration Files

#### 1. `vercel.json`
Main configuration file for Vercel deployment:

```json
{
  "version": 2,
  "name": "ehb-5",
  "description": "EHB-5 Data Processing and Configuration Management System",
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    },
    {
      "src": "api_server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api_server.py"
    },
    {
      "src": "/(.*)",
      "dest": "/main.py"
    }
  ],
  "env": {
    "EHB5_ENVIRONMENT": "production",
    "EHB5_HOST": "0.0.0.0",
    "EHB5_PORT": "5000",
    "EHB5_DASHBOARD_PORT": "8000",
    "JWT_SECRET": "@jwt_secret",
    "DATABASE_PATH": "ehb5.db",
    "LOG_LEVEL": "INFO",
    "DEBUG": "false"
  },
  "functions": {
    "main.py": {
      "runtime": "python3.9",
      "maxDuration": 30
    },
    "api_server.py": {
      "runtime": "python3.9",
      "maxDuration": 30
    }
  },
  "regions": ["iad1"],
  "public": true
}
```

#### 2. `api/index.py`
Serverless function for API endpoints:

```python
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
```

### 🚀 Deployment Steps

#### Method 1: Vercel Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository: `rafiehb555/ehb-5`

2. **Configure Project**:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `./`
   - Install Command: `pip install -r requirements.txt`

3. **Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add the following variables:
     ```
     EHB5_ENVIRONMENT=production
     EHB5_HOST=0.0.0.0
     EHB5_PORT=5000
     EHB5_DASHBOARD_PORT=8000
     JWT_SECRET=your-secure-jwt-secret-here
     DATABASE_PATH=ehb5.db
     LOG_LEVEL=INFO
     DEBUG=false
     ```

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be available at: `https://your-project-name.vercel.app`

#### Method 2: Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project: `No`
   - Project name: `ehb-5`
   - Directory: `./`
   - Override settings: `No`

### 🔧 Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `EHB5_ENVIRONMENT` | `production` | Environment mode |
| `EHB5_HOST` | `0.0.0.0` | Host binding |
| `EHB5_PORT` | `5000` | API port |
| `EHB5_DASHBOARD_PORT` | `8000` | Dashboard port |
| `JWT_SECRET` | `your-secure-secret` | JWT signing secret |
| `DATABASE_PATH` | `ehb5.db` | Database file path |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DEBUG` | `false` | Debug mode |

### 📊 API Endpoints

Your deployed API will be available at:
- **Base URL**: `https://your-project-name.vercel.app`
- **Health Check**: `GET /api/health`
- **System Status**: `GET /api/system/status`
- **Authentication**: `POST /api/auth/login`
- **Projects**: `GET /api/projects`
- **Data Processing**: `POST /api/data/process`
- **AI Agents**: `GET /api/ai/agents`

### 🧪 Testing Deployment

1. **Health Check**:
   ```bash
   curl https://your-project-name.vercel.app/api/health
   ```

2. **System Status**:
   ```bash
   curl https://your-project-name.vercel.app/api/system/status
   ```

3. **Login Test**:
   ```bash
   curl -X POST https://your-project-name.vercel.app/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
   ```

### 🔍 Monitoring

- **Vercel Analytics**: Available in Vercel Dashboard
- **Function Logs**: View in Vercel Dashboard → Functions
- **Performance**: Monitor in Vercel Dashboard → Analytics

### 🚨 Troubleshooting

1. **Build Errors**:
   - Check `requirements.txt` for missing dependencies
   - Verify Python version compatibility
   - Check for syntax errors in Python files

2. **Runtime Errors**:
   - Check function logs in Vercel Dashboard
   - Verify environment variables are set
   - Test locally before deploying

3. **CORS Issues**:
   - Verify CORS headers in `api/index.py`
   - Check browser console for errors

4. **Database Issues**:
   - SQLite files are read-only on Vercel
   - Consider using external database (PostgreSQL, MongoDB)
   - Use Vercel KV for session storage

### 📈 Performance Optimization

1. **Function Optimization**:
   - Keep functions lightweight
   - Use caching for expensive operations
   - Minimize dependencies

2. **Database Optimization**:
   - Use connection pooling
   - Implement query caching
   - Consider serverless database

3. **Monitoring**:
   - Set up Vercel Analytics
   - Monitor function execution times
   - Track error rates

### 🎉 Success!

Your EHB-5 system is now deployed on Vercel and ready for production use!

**Live URL**: `https://your-project-name.vercel.app`
**API Documentation**: Available at `/api/health`
**Dashboard**: Available at the root URL

### 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Python Runtime**: [vercel.com/docs/runtimes/python](https://vercel.com/docs/runtimes/python)
- **Serverless Functions**: [vercel.com/docs/functions](https://vercel.com/docs/functions) 