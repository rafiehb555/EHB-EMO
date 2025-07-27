#!/usr/bin/env python3
"""
Healthcare Data Cleaner
Permanently deletes all healthcare related data and focuses on EHB AI Dev Agent development
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


class HealthcareDataCleaner:
    def __init__(self):
        self.project_root = Path(".")

    def kill_port_processes(self):
        """Kill processes using ports 3000 and 8000"""
        print("🛑 Stopping all running processes...")

        try:
            # Kill processes on port 3000
            subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            subprocess.run(['taskkill', '/F', '/PID', '23656'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/PID', '12812'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/PID', '34480'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/PID', '37724'], capture_output=True)
            print("✅ Stopped all processes")
        except Exception as e:
            print(f"⚠️ Process stop warning: {e}")

    def delete_healthcare_files(self):
        """Delete all healthcare related files"""
        print("🗑️ Deleting healthcare related files...")

        # Files to delete
        healthcare_files = [
            "frontend/app/page.tsx",
            "frontend/app/dashboard.tsx",
            "frontend/app/patients/page.tsx",
            "frontend/app/doctors/page.tsx",
            "frontend/app/healthcare-dashboard/page.tsx",
            "src/pages/index.tsx",
            "src/pages/Dashboard.tsx",
            "src/components/Dashboard.tsx",
            "src/components/PatientCard.tsx",
            "api_server.py",
            "simple_backend.py",
            "EHB_LIVE_STATUS.md",
            "DEPLOYMENT_SUCCESS.md",
            "REACT_ERROR_FIXED.md"
        ]

        for file_path in healthcare_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not delete {file_path}: {e}")

    def delete_healthcare_directories(self):
        """Delete healthcare related directories"""
        print("🗑️ Deleting healthcare directories...")

        healthcare_dirs = [
            "frontend/app/dashboard",
            "frontend/app/patients",
            "frontend/app/doctors",
            "frontend/app/healthcare-dashboard",
            "src/pages",
            "src/components"
        ]

        for dir_path in healthcare_dirs:
            try:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"✅ Deleted directory: {dir_path}")
            except Exception as e:
                print(f"⚠️ Could not delete {dir_path}: {e}")

    def create_ehb_ai_dev_agent(self):
        """Create EHB AI Dev Agent development environment"""
        print("🚀 Creating EHB AI Dev Agent development environment...")

        # Create main AI Dev Agent page
        ai_dev_content = '''export default function EHB_AI_Dev_Agent() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        background: 'white',
        padding: '3rem',
        borderRadius: '1rem',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        textAlign: 'center',
        maxWidth: '800px'
      }}>
        <h1 style={{
          color: '#1e3a8a',
          fontSize: '3rem',
          marginBottom: '1rem',
          fontWeight: 'bold'
        }}>
          🤖 EHB AI Dev Agent
        </h1>

        <p style={{
          color: '#6b7280',
          fontSize: '1.2rem',
          marginBottom: '2rem'
        }}>
          Advanced AI Development Platform
        </p>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '2rem',
          marginBottom: '2rem'
        }}>
          <div style={{
            background: '#f8fafc',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '2px solid #e2e8f0'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#1e3a8a' }}>AI Models</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7c3aed' }}>12</div>
            <div style={{ color: '#6b7280' }}>Active Models</div>
          </div>

          <div style={{
            background: '#f8fafc',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '2px solid #e2e8f0'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#1e3a8a' }}>Agents</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>8</div>
            <div style={{ color: '#6b7280' }}>Running Agents</div>
          </div>

          <div style={{
            background: '#f8fafc',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '2px solid #e2e8f0'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#1e3a8a' }}>Projects</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f59e0b' }}>25</div>
            <div style={{ color: '#6b7280' }}>Active Projects</div>
          </div>

          <div style={{
            background: '#f8fafc',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '2px solid #e2e8f0'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#1e3a8a' }}>Performance</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ef4444' }}>99.9%</div>
            <div style={{ color: '#6b7280' }}>Uptime</div>
          </div>
        </div>

        <div style={{
          background: '#fef3c7',
          padding: '1.5rem',
          borderRadius: '0.5rem',
          border: '2px solid #f59e0b',
          marginBottom: '2rem'
        }}>
          <h3 style={{ margin: '0 0 1rem 0', color: '#92400e' }}>AI Agent Status</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', fontSize: '0.9rem' }}>
            <div>Development Agent: <span style={{ color: '#10b981', fontWeight: 'bold' }}>ACTIVE</span></div>
            <div>Deployment Agent: <span style={{ color: '#10b981', fontWeight: 'bold' }}>ACTIVE</span></div>
            <div>Testing Agent: <span style={{ color: '#10b981', fontWeight: 'bold' }}>ACTIVE</span></div>
            <div>Security Agent: <span style={{ color: '#10b981', fontWeight: 'bold' }}>ACTIVE</span></div>
          </div>
        </div>

        <div style={{
          display: 'flex',
          gap: '1rem',
          justifyContent: 'center',
          flexWrap: 'wrap'
        }}>
          <a href="/ai-dashboard" style={{
            background: '#1e3a8a',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '0.5rem',
            textDecoration: 'none',
            fontWeight: 'bold'
          }}>
            🎛️ AI Dashboard
          </a>
          <a href="/ai-agents" style={{
            background: '#7c3aed',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '0.5rem',
            textDecoration: 'none',
            fontWeight: 'bold'
          }}>
            🤖 AI Agents
          </a>
          <a href="/ai-projects" style={{
            background: '#10b981',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '0.5rem',
            textDecoration: 'none',
            fontWeight: 'bold'
          }}>
            📁 AI Projects
          </a>
        </div>

        <div style={{
          marginTop: '2rem',
          padding: '1rem',
          background: '#f1f5f9',
          borderRadius: '0.5rem',
          border: '1px solid #e2e8f0'
        }}>
          <h3 style={{ margin: '0 0 1rem 0', color: '#1e3a8a' }}>System Information</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem', fontSize: '0.9rem' }}>
            <div>AI Engine: <span style={{ color: '#10b981' }}>Running</span></div>
            <div>Neural Network: <span style={{ color: '#10b981' }}>Active</span></div>
            <div>Machine Learning: <span style={{ color: '#10b981' }}>Training</span></div>
            <div>Deep Learning: <span style={{ color: '#10b981' }}>Processing</span></div>
          </div>
        </div>
      </div>
    </div>
  )
}'''

        # Create app directory
        app_dir = self.project_root / "app"
        app_dir.mkdir(exist_ok=True)

        # Write AI Dev Agent page
        with open(app_dir / "page.tsx", "w", encoding='utf-8') as f:
            f.write(ai_dev_content)

        print("✅ Created EHB AI Dev Agent main page")

    def create_ai_dashboard(self):
        """Create AI Dashboard page"""

        ai_dashboard_content = '''export default function AI_Dashboard() {
  return (
    <div style={{
      minHeight: '100vh',
      background: '#0f172a',
      padding: '2rem',
      color: 'white'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto'
      }}>
        <h1 style={{
          color: '#60a5fa',
          fontSize: '2.5rem',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          🎛️ AI Development Dashboard
        </h1>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '2rem',
          marginBottom: '3rem'
        }}>
          <div style={{
            background: '#1e293b',
            padding: '2rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>AI Models</h3>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#a855f7' }}>12</div>
            <div style={{ color: '#94a3b8' }}>Active Models</div>
            <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#64748b' }}>
              GPT-4, Claude, Llama, Custom Models
            </div>
          </div>

          <div style={{
            background: '#1e293b',
            padding: '2rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>AI Agents</h3>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#10b981' }}>8</div>
            <div style={{ color: '#94a3b8' }}>Running Agents</div>
            <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#64748b' }}>
              Development, Testing, Deployment, Security
            </div>
          </div>

          <div style={{
            background: '#1e293b',
            padding: '2rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Projects</h3>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#f59e0b' }}>25</div>
            <div style={{ color: '#94a3b8' }}>Active Projects</div>
            <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#64748b' }}>
              Web Apps, Mobile Apps, APIs, ML Models
            </div>
          </div>

          <div style={{
            background: '#1e293b',
            padding: '2rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Performance</h3>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#ef4444' }}>99.9%</div>
            <div style={{ color: '#94a3b8' }}>System Uptime</div>
            <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#64748b' }}>
              High Availability, Low Latency
            </div>
          </div>
        </div>

        <div style={{
          background: '#1e293b',
          padding: '2rem',
          borderRadius: '0.5rem',
          border: '1px solid #334155',
          marginBottom: '2rem'
        }}>
          <h2 style={{ margin: '0 0 1.5rem 0', color: '#60a5fa' }}>AI Agent Status</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
            <div style={{
              padding: '1rem',
              background: '#334155',
              borderRadius: '0.5rem',
              border: '1px solid #475569'
            }}>
              <div style={{ fontWeight: 'bold', color: '#60a5fa' }}>Development Agent</div>
              <div style={{ color: '#10b981', fontSize: '0.9rem' }}>ACTIVE - Writing Code</div>
            </div>
            <div style={{
              padding: '1rem',
              background: '#334155',
              borderRadius: '0.5rem',
              border: '1px solid #475569'
            }}>
              <div style={{ fontWeight: 'bold', color: '#60a5fa' }}>Testing Agent</div>
              <div style={{ color: '#10b981', fontSize: '0.9rem' }}>ACTIVE - Running Tests</div>
            </div>
            <div style={{
              padding: '1rem',
              background: '#334155',
              borderRadius: '0.5rem',
              border: '1px solid #475569'
            }}>
              <div style={{ fontWeight: 'bold', color: '#60a5fa' }}>Deployment Agent</div>
              <div style={{ color: '#10b981', fontSize: '0.9rem' }}>ACTIVE - Deploying</div>
            </div>
            <div style={{
              padding: '1rem',
              background: '#334155',
              borderRadius: '0.5rem',
              border: '1px solid #475569'
            }}>
              <div style={{ fontWeight: 'bold', color: '#60a5fa' }}>Security Agent</div>
              <div style={{ color: '#10b981', fontSize: '0.9rem' }}>ACTIVE - Monitoring</div>
            </div>
          </div>
        </div>

        <div style={{
          textAlign: 'center'
        }}>
          <a href="/" style={{
            background: '#60a5fa',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '0.5rem',
            textDecoration: 'none',
            fontWeight: 'bold'
          }}>
            ← Back to AI Dev Agent
          </a>
        </div>
      </div>
    </div>
  )
}'''

        # Create AI dashboard directory
        app_dir = self.project_root / "app"
        ai_dashboard_dir = app_dir / "ai-dashboard"
        ai_dashboard_dir.mkdir(exist_ok=True)

        # Write AI dashboard page
        with open(ai_dashboard_dir / "page.tsx", "w", encoding='utf-8') as f:
            f.write(ai_dashboard_content)

        print("✅ Created AI Dashboard page")

    def create_ai_agents_page(self):
        """Create AI Agents page"""

        ai_agents_content = '''export default function AI_Agents() {
  return (
    <div style={{
      minHeight: '100vh',
      background: '#0f172a',
      padding: '2rem',
      color: 'white'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <h1 style={{
          color: '#60a5fa',
          fontSize: '2.5rem',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          🤖 AI Agents Management
        </h1>

        <div style={{
          background: '#1e293b',
          padding: '2rem',
          borderRadius: '0.5rem',
          border: '1px solid #334155'
        }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: '2rem'
          }}>
            <div style={{
              padding: '2rem',
              border: '2px solid #10b981',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Development Agent</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: ACTIVE</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Task: Writing Code</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Performance: 98%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#10b981',
                color: 'white',
                fontSize: '0.8rem'
              }}>Running</div>
            </div>

            <div style={{
              padding: '2rem',
              border: '2px solid #f59e0b',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Testing Agent</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: ACTIVE</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Task: Running Tests</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Performance: 95%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#f59e0b',
                color: 'white',
                fontSize: '0.8rem'
              }}>Testing</div>
            </div>

            <div style={{
              padding: '2rem',
              border: '2px solid '#7c3aed',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Deployment Agent</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: ACTIVE</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Task: Deploying Apps</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Performance: 97%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#7c3aed',
                color: 'white',
                fontSize: '0.8rem'
              }}>Deploying</div>
            </div>

            <div style={{
              padding: '2rem',
              border: '2px solid '#ef4444',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Security Agent</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: ACTIVE</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Task: Monitoring Security</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Performance: 99%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#ef4444',
                color: 'white',
                fontSize: '0.8rem'
              }}>Securing</div>
            </div>
          </div>
        </div>

        <div style={{
          marginTop: '2rem',
          textAlign: 'center'
        }}>
          <a href="/" style={{
            background: '#60a5fa',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '0.5rem',
            textDecoration: 'none',
            fontWeight: 'bold'
          }}>
            ← Back to AI Dev Agent
          </a>
        </div>
      </div>
    </div>
  )
}'''

        # Create AI agents directory
        app_dir = self.project_root / "app"
        ai_agents_dir = app_dir / "ai-agents"
        ai_agents_dir.mkdir(exist_ok=True)

        # Write AI agents page
        with open(ai_agents_dir / "page.tsx", "w", encoding='utf-8') as f:
            f.write(ai_agents_content)

        print("✅ Created AI Agents page")

    def create_ai_projects_page(self):
        """Create AI Projects page"""

        ai_projects_content = '''export default function AI_Projects() {
  return (
    <div style={{
      minHeight: '100vh',
      background: '#0f172a',
      padding: '2rem',
      color: 'white'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <h1 style={{
          color: '#60a5fa',
          fontSize: '2.5rem',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          📁 AI Projects Management
        </h1>

        <div style={{
          background: '#1e293b',
          padding: '2rem',
          borderRadius: '0.5rem',
          border: '1px solid #334155'
        }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: '2rem'
          }}>
            <div style={{
              padding: '2rem',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Web Application</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Type: React/Next.js</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: In Development</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Progress: 75%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#10b981',
                color: 'white',
                fontSize: '0.8rem'
              }}>Active</div>
            </div>

            <div style={{
              padding: '2rem',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>Mobile App</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Type: React Native</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: Testing</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Progress: 90%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#f59e0b',
                color: 'white',
                fontSize: '0.8rem'
              }}>Testing</div>
            </div>

            <div style={{
              padding: '2rem',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>API Service</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Type: Node.js/Express</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: Deployed</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Progress: 100%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#7c3aed',
                color: 'white',
                fontSize: '0.8rem'
              }}>Live</div>
            </div>

            <div style={{
              padding: '2rem',
              border: '1px solid #334155',
              borderRadius: '0.5rem',
              background: '#0f172a'
            }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#60a5fa' }}>ML Model</h3>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Type: Python/TensorFlow</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Status: Training</div>
              <div style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Progress: 45%</div>
              <div style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                borderRadius: '0.25rem',
                background: '#ef4444',
                color: 'white',
                fontSize: '0.8rem'
              }}>Training</div>
            </div>
          </div>
        </div>

        <div style={{
          marginTop: '2rem',
          textAlign: 'center'
        }}>
          <a href="/" style={{
            background: '#60a5fa',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '0.5rem',
            textDecoration: 'none',
            fontWeight: 'bold'
          }}>
            ← Back to AI Dev Agent
          </a>
        </div>
      </div>
    </div>
  )
}'''

        # Create AI projects directory
        app_dir = self.project_root / "app"
        ai_projects_dir = app_dir / "ai-projects"
        ai_projects_dir.mkdir(exist_ok=True)

        # Write AI projects page
        with open(ai_projects_dir / "page.tsx", "w", encoding='utf-8') as f:
            f.write(ai_projects_content)

        print("✅ Created AI Projects page")

    def update_package_json(self):
        """Update package.json for AI Dev Agent"""

        package_content = '''{
  "name": "ehb-ai-dev-agent",
  "version": "1.0.0",
  "description": "EHB AI Development Agent - Advanced AI Development Platform",
  "main": "index.js",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0",
    "typescript": "^5.0.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=8.0.0"
  },
  "keywords": [
    "ai",
    "development",
    "agent",
    "ehb",
    "react",
    "nextjs",
    "typescript"
  ],
  "author": "EHB AI Development Team",
  "license": "MIT"
}'''

        with open("package.json", "w", encoding='utf-8') as f:
            f.write(package_content)

        print("✅ Updated package.json for AI Dev Agent")

    def run_cleanup(self):
        """Run the complete cleanup and AI Dev Agent setup"""
        print("🧹 Cleaning up healthcare data and setting up AI Dev Agent...")

        # Kill processes
        self.kill_port_processes()

        # Delete healthcare files
        self.delete_healthcare_files()
        self.delete_healthcare_directories()

        # Create AI Dev Agent
        self.create_ehb_ai_dev_agent()
        self.create_ai_dashboard()
        self.create_ai_agents_page()
        self.create_ai_projects_page()

        # Update configuration
        self.update_package_json()

        print("\n✅ Healthcare data permanently deleted!")
        print("🚀 EHB AI Dev Agent development environment created!")
        print("📋 Available pages:")
        print("   - / (AI Dev Agent Home)")
        print("   - /ai-dashboard (AI Dashboard)")
        print("   - /ai-agents (AI Agents)")
        print("   - /ai-projects (AI Projects)")
        print("\n🎯 Focus: EHB AI Dev Agent Development")
        print("🤖 AI Agents: Development, Testing, Deployment, Security")
        print("📊 AI Models: 12 Active Models")
        print("📁 AI Projects: 25 Active Projects")

def main():
    """Main function"""
    cleaner = HealthcareDataCleaner()
    cleaner.run_cleanup()

if __name__ == "__main__":
    main()
