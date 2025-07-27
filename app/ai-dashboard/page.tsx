import '../globals.css'

export default function AI_Dashboard() {
  return (
    <div className="page-container">
      <div className="content-wrapper" style={{ maxWidth: '1400px' }}>
        <h1 className="page-title">
          🎛️ AI Development Dashboard
        </h1>

        <div className="dashboard-grid" style={{ marginBottom: '3rem' }}>
          <div className="metric-card">
            <h3 className="metric-title">AI Models</h3>
            <div className="metric-value" style={{ color: '#a855f7' }}>12</div>
            <div className="metric-title">Active Models</div>
            <div className="metric-description">
              GPT-4, Claude, Llama, Custom Models
            </div>
          </div>

          <div className="metric-card">
            <h3 className="metric-title">AI Agents</h3>
            <div className="metric-value metric-green">8</div>
            <div className="metric-title">Running Agents</div>
            <div className="metric-description">
              Development, Testing, Deployment, Security
            </div>
          </div>

          <div className="metric-card">
            <h3 className="metric-title">Projects</h3>
            <div className="metric-value" style={{ color: '#f59e0b' }}>25</div>
            <div className="metric-title">Active Projects</div>
            <div className="metric-description">
              Web Apps, Mobile Apps, APIs, ML Models
            </div>
          </div>

          <div className="metric-card">
            <h3 className="metric-title">Performance</h3>
            <div className="metric-value metric-red">99.9%</div>
            <div className="metric-title">System Uptime</div>
            <div className="metric-description">
              High Availability, Low Latency
            </div>
          </div>
        </div>

        <div className="section-container" style={{ marginBottom: '2rem' }}>
          <h2 className="section-title">AI Agent Status</h2>
          <div className="agent-status-grid">
            <div className="agent-status-card">
              <div className="agent-status-name">Development Agent</div>
              <div className="agent-status-info">ACTIVE - Writing Code</div>
            </div>
            <div className="agent-status-card">
              <div className="agent-status-name">Testing Agent</div>
              <div className="agent-status-info">ACTIVE - Running Tests</div>
            </div>
            <div className="agent-status-card">
              <div className="agent-status-name">Deployment Agent</div>
              <div className="agent-status-info">ACTIVE - Deploying</div>
            </div>
            <div className="agent-status-card">
              <div className="agent-status-name">Security Agent</div>
              <div className="agent-status-info">ACTIVE - Monitoring</div>
            </div>
          </div>
        </div>

        <div className="nav-container">
          <a href="/" className="back-button">
            ← Back to AI Dev Agent
          </a>
        </div>
      </div>
    </div>
  )
}
