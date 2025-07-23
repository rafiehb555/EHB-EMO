# 🚀 EHB-5 Intelligent System

A comprehensive, AI-powered development environment management platform that provides real-time monitoring, automated error resolution, and intelligent agent management. This system integrates seamlessly with Cursor IDE and provides a centralized configuration for all development tools and environments.

## 🌟 Features

### 🎯 Core Features
- **Real-time Dashboard**: Modern, responsive web interface for system monitoring
- **AI Agents Management**: Intelligent agents for different system aspects
- **Auto-Recovery System**: Automated error detection and resolution
- **WebSocket Communication**: Real-time updates and notifications
- **CLI Interface**: Comprehensive command-line management
- **Security**: Built-in security features and rate limiting
- **Performance Monitoring**: Real-time system metrics and analytics

### 🤖 AI Agents
- **Main Agent**: Overall system coordination and management
- **Data Processing Agent**: File operations and data handling
- **Analytics Agent**: Performance analysis and reporting
- **Security Agent**: Security monitoring and threat detection
- **Recovery Agent**: Automated error recovery and system restoration

### 📊 Dashboard Features
- Real-time system metrics (CPU, Memory, Network, Storage)
- AI agents status and management
- Error monitoring and resolution
- Performance analytics with charts
- Configuration management
- File operations and backup
- User activity tracking

### 🔧 CLI Commands
- Server management (start, stop, status, monitor)
- Configuration management
- AI agents control
- Log viewing and analysis
- Backup and restore operations
- System health checks
- Deployment tools

## 🚀 Quick Start

### Prerequisites
- Node.js 16.0.0 or higher
- npm 8.0.0 or higher
- Windows 10/11 (for Windows-specific features)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ehb-5/intelligent-system.git
   cd intelligent-system
   ```

2. **Run the startup script:**
   ```bash
   start-intelligent-system.bat
   ```

3. **Or install manually:**
   ```bash
   npm install
   npm start
   ```

4. **Open the dashboard:**
   ```
   http://localhost:3001
   ```

### Using CLI
```bash
# Setup the system
node cli.js setup

# Start the server
node cli.js start

# Check status
node cli.js status

# Monitor in real-time
node cli.js monitor

# Manage AI agents
node cli.js agents --list

# View logs
node cli.js logs

# System health check
node cli.js health
```

## 📁 Project Structure

```
ehb-5-intelligent-system/
├── intelligent-api-server.js      # Main API server
├── intelligent-dashboard.html     # Dashboard UI
├── intelligent-dashboard.js       # Dashboard logic
├── cli.js                        # CLI interface
├── package.json                   # Dependencies
├── start-intelligent-system.bat   # Windows startup script
├── INTELLIGENT-SYSTEM-DOCS.md    # Comprehensive documentation
├── test/                         # Test files
│   └── intelligent-api.test.js   # API tests
├── config/                       # Configuration files
├── logs/                         # Log files
├── backups/                      # Backup files
├── data/                         # Data files
└── public/                       # Static files
```

## 🔌 API Endpoints

### Base URL
```
http://localhost:3001/api/v1
```

### Key Endpoints
- `GET /health` - Health check
- `GET /dashboard` - Dashboard data
- `GET /metrics` - System metrics
- `GET /agents` - List AI agents
- `POST /agents` - Create agent
- `PUT /agents/:id` - Update agent
- `DELETE /agents/:id` - Delete agent
- `GET /errors` - List errors
- `POST /errors/resolve` - Resolve error
- `GET /recovery` - List recovery actions
- `POST /recovery/execute` - Execute recovery action
- `GET /files` - Scan files
- `POST /files/process` - Process file
- `GET /config` - Get configuration
- `PUT /config` - Update configuration
- `POST /system/command` - Execute system command
- `POST /recovery/auto` - Trigger auto-recovery

## �� WebSocket Events

Connect to WebSocket:
```javascript
const ws = new WebSocket('ws://localhost:3001');
```

### Event Types
- `connection` - Connection established
- `metrics_update` - System metrics update
- `agents_update` - AI agents status update
- `error_logged` - New error logged
- `error_resolved` - Error resolved
- `recovery_action_completed` - Recovery action completed
- `recovery_action_failed` - Recovery action failed

## 🛠️ Configuration

### Server Configuration (`config/server.json`)
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
PORT=3001
NODE_ENV=development
CURSOR_GLOBAL_CONFIG=C:/CursorWorkspace/config
GLOBAL_PACKAGES_PATH=C:/CursorWorkspace/packages
SHARED_EXTENSIONS_PATH=C:/CursorWorkspace/extensions
```

## 🧪 Testing

### Run Tests
```bash
# All tests
npm test

# Unit tests only
npm run test:unit

# Integration tests only
npm run test:integration

# With coverage
npm run test:coverage
```

### Test Coverage
- API endpoints testing
- WebSocket communication testing
- AI agents functionality testing
- Error handling testing
- Auto-recovery testing
- Security testing

## 🔒 Security Features

- **Rate Limiting**: Prevents API abuse
- **CORS Protection**: Cross-origin resource sharing
- **Helmet Security**: Security headers
- **Input Validation**: Request validation
- **Error Logging**: Comprehensive error tracking
- **Access Control**: Role-based permissions (future)

## 📈 Performance Features

- **Real-time Monitoring**: Live system metrics
- **Auto-scaling**: Dynamic resource allocation
- **Memory Optimization**: Efficient memory usage
- **WebSocket Efficiency**: Optimized real-time communication
- **Caching**: Response caching
- **Compression**: Gzip compression

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production
```bash
npm start
```

### Docker (Future)
```bash
docker build -t intelligent-system .
docker run -p 3001:3001 intelligent-system
```

## 📚 Documentation

- **[Comprehensive Documentation](INTELLIGENT-SYSTEM-DOCS.md)** - Complete system documentation
- **[API Reference](INTELLIGENT-SYSTEM-DOCS.md#api-reference)** - Detailed API documentation
- **[CLI Commands](INTELLIGENT-SYSTEM-DOCS.md#cli-commands)** - CLI usage guide
- **[Troubleshooting](INTELLIGENT-SYSTEM-DOCS.md#troubleshooting)** - Common issues and solutions

## 🔧 Development

### Prerequisites
- Node.js 16.0.0+
- npm 8.0.0+
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/ehb-5/intelligent-system.git
cd intelligent-system

# Install dependencies
npm install

# Run in development mode
npm run dev

# Run tests
npm test

# Lint code
npm run lint
```

### Code Style
- ES6+ features
- ESLint configuration
- Comprehensive testing
- Meaningful commit messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## 📞 Support

- **Documentation**: [INTELLIGENT-SYSTEM-DOCS.md](INTELLIGENT-SYSTEM-DOCS.md)
- **Issues**: GitHub issue tracker
- **Discussions**: GitHub discussions
- **Email**: support@ehb-5.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Roadmap

### Version 2.1 (Planned)
- Machine learning integration
- Advanced AI agents
- Mobile dashboard
- Enhanced security features
- Performance optimizations

### Version 2.2 (Planned)
- Cloud deployment support
- Multi-tenant architecture
- Advanced analytics
- Plugin system
- API gateway

### Version 2.3 (Planned)
- Microservices architecture
- Kubernetes deployment
- Advanced monitoring
- Machine learning models
- AI-powered recommendations

## 🙏 Acknowledgments

- **Cursor IDE** - For the development environment integration
- **Node.js Community** - For the excellent ecosystem
- **Express.js Team** - For the robust web framework
- **WebSocket Community** - For real-time communication
- **AI/ML Community** - For intelligent system concepts

---

**Version**: 2.0.0
**Last Updated**: January 2024
**Maintainer**: EHB-5 Team

---

<div align="center">

**🎉 Welcome to the EHB-5 Intelligent System!**

*Empowering developers with intelligent automation and real-time monitoring.*

[🚀 Quick Start](#quick-start) • [📚 Documentation](INTELLIGENT-SYSTEM-DOCS.md) • [🐛 Report Issues](https://github.com/ehb-5/intelligent-system/issues)

</div>
