import '../globals.css'

export default function AI_Projects() {
  return (
    <div className="page-container">
      <div className="content-wrapper">
        <h1 className="page-title">
          📁 AI Projects Management
        </h1>

        <div className="section-container">
          <div className="grid-container">
            <div className="project-card">
              <h3 className="project-title">Web Application</h3>
              <div className="project-info">Type: React/Next.js</div>
              <div className="project-info">Status: In Development</div>
              <div className="project-info">Progress: 75%</div>
              <div className="status-badge running">Active</div>
            </div>

            <div className="project-card">
              <h3 className="project-title">Mobile App</h3>
              <div className="project-info">Type: React Native</div>
              <div className="project-info">Status: Testing</div>
              <div className="project-info">Progress: 90%</div>
              <div className="status-badge testing">Testing</div>
            </div>

            <div className="project-card">
              <h3 className="project-title">API Service</h3>
              <div className="project-info">Type: Node.js/Express</div>
              <div className="project-info">Status: Deployed</div>
              <div className="project-info">Progress: 100%</div>
              <div className="status-badge deploying">Live</div>
            </div>

            <div className="project-card">
              <h3 className="project-title">ML Model</h3>
              <div className="project-info">Type: Python/TensorFlow</div>
              <div className="project-info">Status: Training</div>
              <div className="project-info">Progress: 45%</div>
              <div className="status-badge securing">Training</div>
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
