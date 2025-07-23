# EHB-5 Intelligent System Documentation

## 🚀 Overview

The EHB-5 Intelligent System is a comprehensive, AI-powered development environment management platform that provides real-time monitoring, automated error resolution, and intelligent agent management. This system integrates seamlessly with Cursor IDE and provides a centralized configuration for all development tools and environments.

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Components](#components)
3. [Installation & Setup](#installation--setup)
4. [API Reference](#api-reference)
5. [Dashboard Usage](#dashboard-usage)
6. [CLI Commands](#cli-commands)
7. [AI Agents](#ai-agents)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Development](#development)

## 🏗️ System Architecture

### Core Components

```
EHB-5 Intelligent System
├── Intelligent API Server (Node.js/Express)
├── Real-time Dashboard (HTML/CSS/JavaScript)
├── WebSocket Communication Layer
├── AI Agents Management System
├── Auto-Recovery Engine
├── Configuration Management
└── CLI Interface
```

### Data Flow

```
User Input → CLI/Dashboard → API Server → AI Agents → System Actions → Real-time Updates
```

### Technology Stack

- **Backend**: Node.js, Express.js, WebSocket
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: In-memory with file persistence
- **Security**: Helmet, CORS, Rate Limiting
- **Monitoring**: Real-time metrics, error tracking
- **Testing**: Jest, Supertest

## 🧩 Components

### 1. Intelligent API Server (`intelligent-api-server.js`)

The core server that handles all API requests, WebSocket connections, and system management.

**Key Features:**
- RESTful API endpoints
- Real-time WebSocket communication
- AI agents management
- Auto-recovery system
- System metrics monitoring
- Error handling and logging

**Ports:**
- HTTP API: 3001
- WebSocket: 3001 (same port)
- Dashboard: 3001

### 2. Real-time Dashboard (`intelligent-dashboard.html`)

A modern, responsive web interface for monitoring and controlling the system.

**Features:**
- Real-time system metrics
- AI agents management
- Error monitoring and resolution
- Performance analytics
- Configuration management
- File operations

### 3. CLI Interface (`cli.js`)

Command-line interface for server management and automation.

**Commands:**
- `start` - Start the server
- `stop` - Stop the server
- `status` - Check server status
- `monitor` - Real-time monitoring
- `config` - Configuration management
- `agents` - AI agents management
- `logs` - View server logs
- `backup` - Backup system data
- `health` - System health check

### 4. AI Agents System

Intelligent agents that handle different aspects of the system:

- **Main Agent**: Overall system coordination
- **Data Processing Agent**: File and data operations
- **Analytics Agent**: Performance analysis
- **Security Agent**: Security monitoring
- **Recovery Agent**: Auto-recovery operations

## 🛠️ Installation & Setup

### Prerequisites

- Node.js 16.0.0 or higher
- npm 8.0.0 or higher
- Windows 10/11 (for Windows-specific features)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ehb-5/intelligent-system.git
   cd intelligent-system
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run setup:**
   ```bash
   npm run setup
   ```

4. **Start the server:**
   ```bash
   npm start
   ```

5. **Open dashboard:**
   ```
   http://localhost:3001
   ```

### Advanced Setup

#### Using CLI
```bash
# Setup the system
ehb-api setup

# Start the server
ehb-api start

# Check status
ehb-api status

# Monitor in real-time
ehb-api monitor
```

#### Using PowerShell Scripts
```powershell
# Run setup script
.\setup-cursor-global.ps1

# Verify setup
.\verify-setup.ps1

# Launch project
.\launch-project.ps1 my-project
```

## 📚 API Reference

### Base URL
```
http://localhost:3001/api/v1
```

### Authentication
Currently, the API uses basic authentication. Add headers for future implementations:
```javascript
headers: {
  'Authorization': 'Bearer YOUR_TOKEN',
  'Content-Type': 'application/json'
}
```

### Endpoints

#### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 3600,
  "version": "2.0.0"
}
```

#### Dashboard Data
```http
GET /api/v1/dashboard
```
**Response:**
```json
{
  "metrics": {
    "cpu": 45,
    "memory": 65,
    "network": 12.5,
    "storage": 75,
    "uptime": 3600
  },
  "agents": [...],
  "recentErrors": [...],
  "recentRecoveryActions": [...],
  "systemStatus": {...},
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

#### System Metrics
```http
GET /api/v1/metrics
```
**Response:**
```json
{
  "cpu": 45,
  "memory": 65,
  "network": 12.5,
  "storage": 75,
  "uptime": 3600
}
```

#### AI Agents

**List Agents:**
```http
GET /api/v1/agents
```

**Create Agent:**
```http
POST /api/v1/agents
Content-Type: application/json

{
  "name": "Test Agent",
  "type": "test",
  "config": {
    "status": "active"
  }
}
```

**Update Agent:**
```http
PUT /api/v1/agents/{id}
Content-Type: application/json

{
  "status": "active",
  "config": {
    "newSetting": "value"
  }
}
```

**Delete Agent:**
```http
DELETE /api/v1/agents/{id}
```

#### Error Management

**List Errors:**
```http
GET /api/v1/errors?limit=50&type=API_ERROR
```

**Resolve Error:**
```http
POST /api/v1/errors/resolve
Content-Type: application/json

{
  "errorId": "error-uuid"
}
```

#### Recovery Actions

**List Recovery Actions:**
```http
GET /api/v1/recovery
```

**Execute Recovery Action:**
```http
POST /api/v1/recovery/execute
Content-Type: application/json

{
  "actionId": "action-uuid"
}
```

#### File Operations

**Scan Files:**
```http
GET /api/v1/files?path=./src
```

**Process File:**
```http
POST /api/v1/files/process
Content-Type: application/json

{
  "filePath": "./test.txt",
  "action": "read"
}
```

#### Configuration

**Get Configuration:**
```http
GET /api/v1/config
```

**Update Configuration:**
```http
PUT /api/v1/config
Content-Type: application/json

{
  "config": {
    "newSetting": "value"
  }
}
```

#### System Commands

**Execute System Command:**
```http
POST /api/v1/system/command
Content-Type: application/json

{
  "command": "dir",
  "args": ["/s"]
}
```

#### Auto-Recovery

**Trigger Auto-Recovery:**
```http
POST /api/v1/recovery/auto
```

### WebSocket Events

Connect to WebSocket:
```javascript
const ws = new WebSocket('ws://localhost:3001');
```

#### Event Types

**Connection:**
```json
{
  "type": "connection",
  "clientId": "uuid",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

**Metrics Update:**
```json
{
  "type": "metrics_update",
  "data": {
    "cpu": 45,
    "memory": 65,
    "network": 12.5,
    "storage": 75,
    "uptime": 3600
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

**Agent Updates:**
```json
{
  "type": "agents_update",
  "data": [...],
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

**Error Events:**
```json
{
  "type": "error_logged",
  "data": {
    "id": "error-uuid",
    "type": "API_ERROR",
    "message": "Error message",
    "severity": "medium",
    "timestamp": "2024-01-01T00:00:00.000Z"
  }
}
```

**Recovery Events:**
```json
{
  "type": "recovery_action_completed",
  "data": {
    "id": "action-uuid",
    "status": "completed",
    "result": {...}
  }
}
```

## 🎛️ Dashboard Usage

### Main Dashboard

The dashboard provides real-time monitoring of all system components:

1. **System Metrics**: CPU, memory, network, and storage usage
2. **AI Agents**: Status and management of all agents
3. **Recent Activity**: Latest system events and actions
4. **Quick Actions**: Common operations and shortcuts
5. **Performance Analytics**: Charts and graphs of system performance
6. **Error Monitoring**: Real-time error tracking and resolution

### Navigation

- **Home**: Overview and quick stats
- **Dashboard**: Detailed system monitoring
- **Agents**: AI agents management
- **Tools**: Development tools and utilities
- **Projects**: Project management
- **Analytics**: Performance analytics
- **Settings**: System configuration

### Features

#### Real-time Updates
All dashboard components update automatically via WebSocket connections.

#### Interactive Controls
- Click on agents to manage their status
- Use quick action buttons for common tasks
- Monitor system metrics in real-time
- View and resolve errors directly

#### Responsive Design
The dashboard adapts to different screen sizes and devices.

## 🖥️ CLI Commands

### Basic Commands

#### Start Server
```bash
ehb-api start [options]
```
**Options:**
- `-p, --port <port>`: Port number (default: 3001)
- `-e, --env <environment>`: Environment (development/production)
- `--daemon`: Run as daemon process

**Example:**
```bash
ehb-api start -p 3002 -e production
```

#### Stop Server
```bash
ehb-api stop
```

#### Check Status
```bash
ehb-api status
```

#### Monitor Server
```bash
ehb-api monitor [options]
```
**Options:**
- `-i, --interval <seconds>`: Update interval (default: 5)

**Example:**
```bash
ehb-api monitor -i 10
```

### Configuration Commands

#### Setup Server
```bash
ehb-api setup [options]
```
**Options:**
- `--force`: Force setup even if already configured

#### Manage Configuration
```bash
ehb-api config [options]
```
**Options:**
- `--show`: Show current configuration
- `--edit`: Edit configuration interactively
- `--reset`: Reset to default configuration

**Examples:**
```bash
ehb-api config --show
ehb-api config --edit
ehb-api config --reset
```

### Agent Management

#### List Agents
```bash
ehb-api agents --list
```

#### Start Agent
```bash
ehb-api agents --start <agent-id>
```

#### Stop Agent
```bash
ehb-api agents --stop <agent-id>
```

#### Restart Agent
```bash
ehb-api agents --restart <agent-id>
```

#### Check Agent Status
```bash
ehb-api agents --status <agent-id>
```

### Logging and Monitoring

#### View Logs
```bash
ehb-api logs [options]
```
**Options:**
- `-f, --follow`: Follow log output
- `-n, --lines <number>`: Number of lines to show
- `--level <level>`: Log level (error/warn/info/debug)

**Examples:**
```bash
ehb-api logs -f
ehb-api logs -n 100 --level error
```

### Backup and Recovery

#### Backup Server
```bash
ehb-api backup [options]
```
**Options:**
- `-d, --destination <path>`: Backup destination path
- `--include-logs`: Include log files
- `--include-config`: Include configuration files

**Example:**
```bash
ehb-api backup -d ./backups/ --include-logs
```

#### Restore Server
```bash
ehb-api restore [options]
```
**Options:**
- `-s, --source <path>`: Backup source path
- `--force`: Force restore without confirmation

**Example:**
```bash
ehb-api restore -s ./backups/backup-2024-01-01.zip
```

### System Management

#### Health Check
```bash
ehb-api health [options]
```
**Options:**
- `--detailed`: Show detailed health information
- `--fix`: Attempt to fix health issues

**Example:**
```bash
ehb-api health --detailed --fix
```

#### Update Server
```bash
ehb-api update [options]
```
**Options:**
- `--check`: Check for updates only
- `--force`: Force update without confirmation

#### Deploy Server
```bash
ehb-api deploy [options]
```
**Options:**
- `--environment <env>`: Target environment
- `--config <path>`: Deployment configuration file
- `--dry-run`: Simulate deployment

### Utility Commands

#### Open Dashboard
```bash
ehb-api dashboard [options]
```
**Options:**
- `--port <port>`: Dashboard port (default: 3001)

#### Run Tests
```bash
ehb-api test [options]
```
**Options:**
- `--unit`: Run unit tests only
- `--integration`: Run integration tests only
- `--coverage`: Generate coverage report

## 🤖 AI Agents

### Agent Types

#### Main Agent
- **Purpose**: Overall system coordination
- **Responsibilities**:
  - System monitoring
  - Resource allocation
  - Task scheduling
  - Inter-agent communication

#### Data Processing Agent
- **Purpose**: Handle file and data operations
- **Responsibilities**:
  - File scanning and processing
  - Data validation
  - Backup operations
  - Data transformation

#### Analytics Agent
- **Purpose**: Performance analysis and reporting
- **Responsibilities**:
  - Metrics collection
  - Performance analysis
  - Trend identification
  - Report generation

#### Security Agent
- **Purpose**: Security monitoring and threat detection
- **Responsibilities**:
  - Security scanning
  - Threat detection
  - Access control
  - Audit logging

#### Recovery Agent
- **Purpose**: Automated error recovery
- **Responsibilities**:
  - Error detection
  - Recovery action execution
  - System restoration
  - Health monitoring

### Agent Lifecycle

1. **Initialization**: Agent is created and configured
2. **Activation**: Agent starts monitoring and processing
3. **Operation**: Agent performs assigned tasks
4. **Monitoring**: Agent reports status and metrics
5. **Recovery**: Agent handles errors and self-heals
6. **Termination**: Agent is stopped and cleaned up

### Agent Communication

Agents communicate through the central API server using:
- **REST API**: For command and control
- **WebSocket**: For real-time updates
- **Event System**: For inter-agent communication

### Agent Configuration

Each agent can be configured with:
- **Status**: active, inactive, restarting
- **Parameters**: Custom configuration options
- **Schedules**: When to perform tasks
- **Dependencies**: Other agents or resources required

## ⚙️ Configuration

### Server Configuration

The server configuration is stored in `config/server.json`:

```json
{
  "server": {
    "port": 3001,
    "host": "localhost",
    "environment": "development"
  },
  "security": {
    "rateLimit": true,
    "cors": true,
    "helmet": true
  },
  "monitoring": {
    "enabled": true,
    "interval": 5000,
    "metrics": true
  },
  "agents": {
    "autoStart": true,
    "maxAgents": 10,
    "healthCheck": true
  },
  "logging": {
    "level": "info",
    "file": "logs/server.log",
    "maxSize": "10m",
    "maxFiles": 5
  }
}
```

### Environment Variables

```bash
# Server Configuration
PORT=3001
NODE_ENV=development
CURSOR_GLOBAL_CONFIG=C:/CursorWorkspace/config
GLOBAL_PACKAGES_PATH=C:/CursorWorkspace/packages
SHARED_EXTENSIONS_PATH=C:/CursorWorkspace/extensions

# Security
JWT_SECRET=your-jwt-secret
API_KEY=your-api-key

# Database (for future use)
DATABASE_URL=your-database-url

# External Services
OPENAI_API_KEY=your-openai-key
REPLIT_API_KEY=your-replit-key
```

### Dashboard Configuration

The dashboard can be customized through the settings panel:

- **Theme**: Light/Dark mode
- **Refresh Rate**: Update intervals
- **Notifications**: Alert preferences
- **Layout**: Component arrangement
- **Permissions**: Access control

## 🔧 Troubleshooting

### Common Issues

#### Server Won't Start

**Symptoms:**
- Port already in use
- Missing dependencies
- Configuration errors

**Solutions:**
```bash
# Check if port is in use
netstat -ano | findstr :3001

# Kill process using port
taskkill /PID <PID> /F

# Reinstall dependencies
npm install

# Check configuration
ehb-api config --show
```

#### WebSocket Connection Issues

**Symptoms:**
- Dashboard not updating
- Real-time features not working

**Solutions:**
```bash
# Check WebSocket server
ehb-api status

# Restart server
ehb-api stop
ehb-api start

# Check firewall settings
```

#### Agent Not Responding

**Symptoms:**
- Agent status shows "inactive"
- No agent metrics

**Solutions:**
```bash
# Check agent status
ehb-api agents --list

# Restart specific agent
ehb-api agents --restart <agent-id>

# Check agent logs
ehb-api logs --level error
```

#### Performance Issues

**Symptoms:**
- Slow response times
- High CPU/memory usage

**Solutions:**
```bash
# Check system health
ehb-api health --detailed

# Monitor performance
ehb-api monitor

# Optimize configuration
ehb-api config --edit
```

### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| EADDRINUSE | Port already in use | Change port or kill process |
| EACCES | Permission denied | Run as administrator |
| ENOENT | File not found | Check file paths |
| ECONNREFUSED | Connection refused | Check server status |
| ETIMEDOUT | Connection timeout | Check network |

### Log Analysis

#### Error Logs
```bash
# View error logs
ehb-api logs --level error

# Follow error logs
ehb-api logs -f --level error
```

#### Debug Mode
```bash
# Enable debug logging
NODE_ENV=development ehb-api start

# View debug logs
ehb-api logs --level debug
```

### Recovery Procedures

#### Automatic Recovery
The system includes automatic recovery for common issues:
- Service restart on failure
- Configuration validation
- Resource cleanup
- Error resolution

#### Manual Recovery
```bash
# Full system restart
ehb-api stop
ehb-api start

# Reset configuration
ehb-api config --reset

# Restore from backup
ehb-api restore -s ./backups/latest.zip
```

## 🚀 Development

### Project Structure

```
intelligent-system/
├── intelligent-api-server.js    # Main server
├── intelligent-dashboard.html   # Dashboard UI
├── intelligent-dashboard.js     # Dashboard logic
├── cli.js                      # CLI interface
├── package.json                 # Dependencies
├── config/                      # Configuration files
├── logs/                        # Log files
├── test/                        # Test files
├── docs/                        # Documentation
└── backups/                     # Backup files
```

### Development Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/ehb-5/intelligent-system.git
   cd intelligent-system
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run in development mode:**
   ```bash
   npm run dev
   ```

4. **Run tests:**
   ```bash
   npm test
   ```

5. **Lint code:**
   ```bash
   npm run lint
   ```

### Testing

#### Unit Tests
```bash
npm run test:unit
```

#### Integration Tests
```bash
npm run test:integration
```

#### Coverage Report
```bash
npm run test:coverage
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

### Code Style

- Use ES6+ features
- Follow ESLint configuration
- Write comprehensive tests
- Document new features
- Use meaningful commit messages

### Deployment

#### Development
```bash
npm run dev
```

#### Production
```bash
npm start
```

#### Docker (Future)
```bash
docker build -t intelligent-system .
docker run -p 3001:3001 intelligent-system
```

## 📈 Performance Optimization

### Server Optimization

- **Caching**: Implement Redis for caching
- **Compression**: Enable gzip compression
- **Rate Limiting**: Prevent abuse
- **Connection Pooling**: Optimize database connections

### Dashboard Optimization

- **Lazy Loading**: Load components on demand
- **Virtual Scrolling**: Handle large datasets
- **Caching**: Cache API responses
- **Minification**: Compress assets

### Monitoring

- **Metrics Collection**: System performance metrics
- **Alerting**: Proactive issue detection
- **Logging**: Comprehensive logging
- **Tracing**: Request tracing

## 🔒 Security

### Authentication & Authorization

- **JWT Tokens**: Secure API access
- **Role-based Access**: User permissions
- **API Keys**: Service authentication
- **Session Management**: Secure sessions

### Data Protection

- **Encryption**: Data at rest and in transit
- **Input Validation**: Prevent injection attacks
- **Output Sanitization**: Prevent XSS
- **Audit Logging**: Track all actions

### Network Security

- **HTTPS**: Secure communication
- **CORS**: Cross-origin resource sharing
- **Rate Limiting**: Prevent abuse
- **Firewall Rules**: Network protection

## 📊 Monitoring & Analytics

### System Metrics

- **CPU Usage**: Processor utilization
- **Memory Usage**: RAM consumption
- **Network I/O**: Network activity
- **Disk I/O**: Storage activity
- **Response Times**: API performance

### Business Metrics

- **User Activity**: Dashboard usage
- **Agent Performance**: AI agent metrics
- **Error Rates**: System reliability
- **Recovery Success**: Auto-recovery effectiveness

### Alerting

- **Threshold Alerts**: Performance thresholds
- **Anomaly Detection**: Unusual patterns
- **Escalation**: Alert escalation procedures
- **Integration**: External alerting systems

## 🔮 Future Enhancements

### Planned Features

- **Machine Learning**: Predictive analytics
- **Advanced AI**: More sophisticated agents
- **Mobile App**: Mobile dashboard
- **API Gateway**: Enhanced API management
- **Microservices**: Service decomposition

### Integration Opportunities

- **CI/CD**: Continuous integration
- **Cloud Platforms**: AWS, Azure, GCP
- **Monitoring Tools**: Prometheus, Grafana
- **Logging**: ELK Stack
- **Security**: SIEM integration

---

## 📞 Support

For support and questions:

- **Documentation**: This file and inline code comments
- **Issues**: GitHub issue tracker
- **Discussions**: GitHub discussions
- **Email**: support@ehb-5.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Version**: 2.0.0
**Last Updated**: January 2024
**Maintainer**: EHB-5 Team
