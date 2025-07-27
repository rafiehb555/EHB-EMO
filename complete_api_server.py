#!/usr/bin/env python3
"""
EHB AI Dev Agent - Complete API Server
Real-time API with WebSocket support and all missing endpoints
"""

import asyncio
import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import uvicorn
import websockets
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# Import authentication system
from complete_auth_system import AuthenticationSystem, require_auth, require_role


# Pydantic models
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class AgentTask(BaseModel):
    agent_id: str
    task_type: str
    description: str
    priority: str = "medium"

class ProjectCreate(BaseModel):
    name: str
    description: str
    assigned_agents: List[str] = []

# Initialize FastAPI app
app = FastAPI(
    title="EHB AI Dev Agent API",
    description="Complete AI Development Platform API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize authentication system
auth_system = AuthenticationSystem()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.agent_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_type: str = "user"):
        await websocket.accept()
        self.active_connections.append(websocket)
        if client_type == "agent":
            # Store agent connection
            pass

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove broken connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Database helper functions
def get_db_connection():
    return sqlite3.connect("ehb_ai_dev_agent.db")

def get_ai_agents() -> List[Dict]:
    """Get all AI agents"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, agent_type, status, performance_score, current_task, configuration
        FROM ai_agents ORDER BY performance_score DESC
    """)

    agents = []
    for row in cursor.fetchall():
        agents.append({
            "id": row[0],
            "name": row[1],
            "agent_type": row[2],
            "status": row[3],
            "performance_score": row[4],
            "current_task": row[5],
            "configuration": json.loads(row[6]) if row[6] else {}
        })

    conn.close()
    return agents

def get_projects() -> List[Dict]:
    """Get all projects"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, description, status, owner_id, assigned_agents, progress
        FROM projects ORDER BY created_at DESC
    """)

    projects = []
    for row in cursor.fetchall():
        projects.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "status": row[3],
            "owner_id": row[4],
            "assigned_agents": json.loads(row[5]) if row[5] else [],
            "progress": row[6]
        })

    conn.close()
    return projects

def get_analytics() -> List[Dict]:
    """Get analytics data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT metric_name, metric_value, metric_data, category, tags
        FROM analytics ORDER BY timestamp DESC
    """)

    analytics = []
    for row in cursor.fetchall():
        analytics.append({
            "metric_name": row[0],
            "metric_value": row[1],
            "metric_data": json.loads(row[2]) if row[2] else {},
            "category": row[3],
            "tags": json.loads(row[4]) if row[4] else []
        })

    conn.close()
    return analytics

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    token = credentials.credentials
    user_data = auth_system.verify_token(token)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_data

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EHB AI Dev Agent API",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EHB AI Dev Agent API",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# Authentication endpoints
@app.post("/api/auth/register")
async def register_user(user_data: UserRegister):
    """Register new user"""
    result = auth_system.register_user(
        user_data.username,
        user_data.email,
        user_data.password,
        user_data.role
    )

    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/api/auth/login")
async def login_user(user_data: UserLogin):
    """Login user"""
    result = auth_system.login_user(user_data.email, user_data.password)

    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=401, detail=result["error"])

@app.get("/api/auth/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    user = auth_system.get_user_by_id(current_user["user_id"])
    if user:
        return {"success": True, "user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# AI Agents endpoints
@app.get("/api/agents")
async def get_agents():
    """Get all AI agents"""
    agents = get_ai_agents()
    return {
        "success": True,
        "agents": agents,
        "total": len(agents)
    }

@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, agent_type, status, performance_score, current_task, configuration
        FROM ai_agents WHERE id = ?
    """, (agent_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "success": True,
            "agent": {
                "id": row[0],
                "name": row[1],
                "agent_type": row[2],
                "status": row[3],
                "performance_score": row[4],
                "current_task": row[5],
                "configuration": json.loads(row[6]) if row[6] else {}
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/api/agents/{agent_id}/tasks")
async def create_agent_task(agent_id: str, task: AgentTask, current_user: Dict = Depends(get_current_user)):
    """Create new task for agent"""
    conn = get_db_connection()
    cursor = conn.cursor()

    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    cursor.execute("""
        INSERT INTO agent_tasks (id, agent_id, task_type, description, status, priority, progress)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_id, agent_id, task.task_type, task.description, "pending", task.priority, 0.0))

    conn.commit()
    conn.close()

    # Broadcast to WebSocket clients
    await manager.broadcast(json.dumps({
        "type": "agent_task_created",
        "task_id": task_id,
        "agent_id": agent_id,
        "task_type": task.task_type,
        "description": task.description
    }))

    return {
        "success": True,
        "message": "Task created successfully",
        "task_id": task_id
    }

# Projects endpoints
@app.get("/api/projects")
async def get_projects():
    """Get all projects"""
    projects = get_projects()
    return {
        "success": True,
        "projects": projects,
        "total": len(projects)
    }

@app.post("/api/projects")
async def create_project(project: ProjectCreate, current_user: Dict = Depends(get_current_user)):
    """Create new project"""
    conn = get_db_connection()
    cursor = conn.cursor()

    project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    cursor.execute("""
        INSERT INTO projects (id, name, description, status, owner_id, assigned_agents, progress)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        project_id, project.name, project.description, "active",
        current_user["user_id"], json.dumps(project.assigned_agents), 0.0
    ))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Project created successfully",
        "project_id": project_id
    }

# Analytics endpoints
@app.get("/api/analytics")
async def get_analytics():
    """Get analytics data"""
    analytics = get_analytics()
    return {
        "success": True,
        "analytics": analytics
    }

@app.get("/api/analytics/{metric_name}")
async def get_metric(metric_name: str):
    """Get specific metric"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT metric_name, metric_value, metric_data, category, tags
        FROM analytics WHERE metric_name = ?
    """, (metric_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "success": True,
            "metric": {
                "metric_name": row[0],
                "metric_value": row[1],
                "metric_data": json.loads(row[2]) if row[2] else {},
                "category": row[3],
                "tags": json.loads(row[4]) if row[4] else []
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Metric not found")

# Dashboard endpoints
@app.get("/api/dashboard")
async def get_dashboard(current_user: Dict = Depends(get_current_user)):
    """Get dashboard data"""
    agents = get_ai_agents()
    projects = get_projects()
    analytics = get_analytics()

    # Calculate dashboard metrics
    active_agents = len([a for a in agents if a["status"] == "active"])
    total_projects = len(projects)
    avg_performance = sum(a["performance_score"] for a in agents) / len(agents) if agents else 0

    return {
        "success": True,
        "dashboard": {
            "metrics": {
                "active_agents": active_agents,
                "total_projects": total_projects,
                "avg_performance": round(avg_performance, 2),
                "system_uptime": 99.9
            },
            "agents": agents[:4],  # Top 4 agents
            "projects": projects[:5],  # Recent 5 projects
            "analytics": analytics[:3]  # Top 3 metrics
        }
    }

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()}))

            elif message.get("type") == "subscribe_agents":
                # Send current agent status
                agents = get_ai_agents()
                await websocket.send_text(json.dumps({
                    "type": "agent_status_update",
                    "agents": agents
                }))

            elif message.get("type") == "subscribe_projects":
                # Send current project status
                projects = get_projects()
                await websocket.send_text(json.dumps({
                    "type": "project_status_update",
                    "projects": projects
                }))

            else:
                # Echo back the message
                await websocket.send_text(json.dumps({
                    "type": "echo",
                    "message": message
                }))

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Admin endpoints
@app.get("/api/admin/users")
@require_role("admin")
async def get_all_users(current_user: Dict = Depends(get_current_user)):
    """Get all users (admin only)"""
    result = auth_system.get_all_users(current_user["user_id"])

    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=403, detail=result["error"])

@app.post("/api/admin/users/{user_id}/deactivate")
@require_role("admin")
async def deactivate_user(user_id: str, current_user: Dict = Depends(get_current_user)):
    """Deactivate user (admin only)"""
    result = auth_system.deactivate_user(user_id)

    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result["error"])

# Error handling
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status_code": 500}

# Background tasks
async def update_agent_status():
    """Background task to update agent status"""
    while True:
        try:
            # Update agent performance scores
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM ai_agents WHERE status = 'active'")
            active_agents = cursor.fetchall()

            for agent in active_agents:
                # Simulate performance updates
                new_score = min(100, max(0, 95 + (datetime.now().second % 10) - 5))

                cursor.execute("""
                    UPDATE ai_agents
                    SET performance_score = ?, last_activity = ?, updated_at = ?
                    WHERE id = ?
                """, (new_score, datetime.now().isoformat(), datetime.now().isoformat(), agent[0]))

            conn.commit()
            conn.close()

            # Broadcast updates to WebSocket clients
            agents = get_ai_agents()
            await manager.broadcast(json.dumps({
                "type": "agent_status_update",
                "agents": agents,
                "timestamp": datetime.now().isoformat()
            }))

        except Exception as e:
            print(f"Error updating agent status: {e}")

        await asyncio.sleep(30)  # Update every 30 seconds

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("🚀 Starting EHB AI Dev Agent API Server...")

    # Start background tasks
    asyncio.create_task(update_agent_status())

    print("✅ API Server started successfully!")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    print("🛑 Shutting down EHB AI Dev Agent API Server...")

def main():
    """Run the API server"""
    print("🚀 Starting EHB AI Dev Agent API Server...")

    uvicorn.run(
        "complete_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
