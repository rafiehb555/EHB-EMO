import '../globals.css'

export default function AI_Agents() {
  return (
    <div className="page-container">
      <div className="content-wrapper">
        <h1 className="page-title">
          🤖 AI Agents Management
        </h1>

        <div className="section-container">
          <div className="grid-container">
            <div className="agent-card development">
              <h3 className="agent-title">Development Agent</h3>
              <div className="agent-info">Status: ACTIVE</div>
              <div className="agent-info">Task: Writing Code</div>
              <div className="agent-info">Performance: 98%</div>
              <div className="status-badge running">Running</div>
            </div>

            <div className="agent-card testing">
              <h3 className="agent-title">Testing Agent</h3>
              <div className="agent-info">Status: ACTIVE</div>
              <div className="agent-info">Task: Running Tests</div>
              <div className="agent-info">Performance: 95%</div>
              <div className="status-badge testing">Testing</div>
            </div>

            <div className="agent-card deployment">
              <h3 className="agent-title">Deployment Agent</h3>
              <div className="agent-info">Status: ACTIVE</div>
              <div className="agent-info">Task: Deploying Apps</div>
              <div className="agent-info">Performance: 97%</div>
              <div className="status-badge deploying">Deploying</div>
            </div>

            <div className="agent-card security">
              <h3 className="agent-title">Security Agent</h3>
              <div className="agent-info">Status: ACTIVE</div>
              <div className="agent-info">Task: Monitoring Security</div>
              <div className="agent-info">Performance: 99%</div>
              <div className="status-badge securing">Securing</div>
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
