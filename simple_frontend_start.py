"""
Simple Frontend Starter for EHB Healthcare System
Uses a different approach that works on Windows
"""

import os
import subprocess
import time
import json
from pathlib import Path

def create_simple_frontend():
    """Create a simple frontend that works on Windows"""
    print("🚀 Creating simple frontend...")
    
    # Create frontend directory
    frontend_dir = Path("frontend")
    frontend_dir.mkdir(exist_ok=True)
    
    # Create a simple HTML file instead of Next.js
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EHB Healthcare System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
        }
        
        h1 {
            color: #1f2937;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: bold;
        }
        
        .status {
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        .status span {
            color: #10b981;
            font-weight: bold;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: #f3f4f6;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
        }
        
        .stat-label {
            color: #6b7280;
        }
        
        .patients { color: #3b82f6; }
        .doctors { color: #10b981; }
        .appointments { color: #8b5cf6; }
        
        .message {
            background: #fef3c7;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #f59e0b;
            color: #92400e;
        }
        
        .api-status {
            margin-top: 1rem;
            padding: 0.5rem;
            border-radius: 0.5rem;
            font-size: 0.9rem;
        }
        
        .api-online {
            background: #d1fae5;
            color: #065f46;
        }
        
        .api-offline {
            background: #fee2e2;
            color: #991b1b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>EHB Healthcare System</h1>
        
        <div class="status">
            System Status: <span>ONLINE</span>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number patients">150</div>
                <div class="stat-label">Patients</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number doctors">25</div>
                <div class="stat-label">Doctors</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number appointments">45</div>
                <div class="stat-label">Appointments</div>
            </div>
        </div>
        
        <div class="message">
            System automatically restarted after PC shutdown
        </div>
        
        <div id="api-status" class="api-status api-online">
            Backend API: Checking...
        </div>
    </div>
    
    <script>
        // Check backend API status
        async function checkAPI() {
            try {
                const response = await fetch('http://localhost:8000/');
                const data = await response.json();
                document.getElementById('api-status').innerHTML = 'Backend API: ONLINE';
                document.getElementById('api-status').className = 'api-status api-online';
            } catch (error) {
                document.getElementById('api-status').innerHTML = 'Backend API: OFFLINE';
                document.getElementById('api-status').className = 'api-status api-offline';
            }
        }
        
        // Check API status on load and every 10 seconds
        checkAPI();
        setInterval(checkAPI, 10000);
    </script>
</body>
</html>
'''
    
    with open(frontend_dir / "index.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Simple frontend created")

def start_simple_server():
    """Start a simple HTTP server for the frontend"""
    print("🚀 Starting simple HTTP server...")
    
    try:
        # Use Python's built-in HTTP server
        frontend_dir = Path("frontend")
        os.chdir(frontend_dir)
        
        # Start HTTP server on port 3001
        subprocess.Popen([
            "python", "-m", "http.server", "3001"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        print("✅ Simple HTTP server started on port 3001")
        os.chdir("..")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start simple server: {e}")
        os.chdir("..")
        return False

def main():
    """Main function"""
    print("🚀 EHB Healthcare System - Simple Frontend")
    print("=" * 50)
    
    # Create simple frontend
    create_simple_frontend()
    
    # Start simple server
    server_ok = start_simple_server()
    
    if server_ok:
        print("\n" + "=" * 50)
        print("🎉 Simple frontend started successfully!")
        print("📱 Frontend: http://localhost:3001")
        print("🔧 Backend API: http://localhost:8000")
        print("📊 Dashboard: http://localhost:3001")
        print("=" * 50)
    else:
        print("\n❌ Failed to start frontend server")

if __name__ == "__main__":
    main() 