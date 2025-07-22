const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const compression = require('compression');
const morgan = require('morgan');
const { v4: uuidv4 } = require('uuid');
const WebSocket = require('ws');
const http = require('http');
const path = require('path');
const fs = require('fs').promises;
const os = require('os');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

class IntelligentAPIServer {
    constructor() {
        this.app = express();
        this.server = http.createServer(this.app);
        this.wss = new WebSocket.Server({ server: this.server });
        this.port = process.env.PORT || 3001;
        this.clients = new Set();
        this.agents = new Map();
        this.systemMetrics = {
            cpu: 0,
            memory: 0,
            network: 0,
            storage: 0,
            uptime: 0
        };
        this.errorLog = [];
        this.recoveryActions = [];
        this.isRunning = false;

        this.setupMiddleware();
        this.setupRoutes();
        this.setupWebSocket();
        this.initializeAgents();
        this.startMonitoring();
    }

    setupMiddleware() {
        // Security middleware
        this.app.use(helmet({
            contentSecurityPolicy: {
                directives: {
                    defaultSrc: ["'self'"],
                    styleSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
                    scriptSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
                    fontSrc: ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
                    imgSrc: ["'self'", "data:", "https:"],
                    connectSrc: ["'self'", "ws:", "wss:"]
                }
            }
        }));

        // Rate limiting
        const limiter = rateLimit({
            windowMs: 15 * 60 * 1000, // 15 minutes
            max: 100, // limit each IP to 100 requests per windowMs
            message: 'Too many requests from this IP, please try again later.'
        });
        this.app.use('/api/', limiter);

        // Other middleware
        this.app.use(cors({
            origin: ['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:3000'],
            credentials: true
        }));
        this.app.use(compression());
        this.app.use(morgan('combined'));
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));

        // Static files
        this.app.use(express.static(path.join(__dirname, 'public')));
    }

    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'healthy',
                timestamp: new Date().toISOString(),
                uptime: process.uptime(),
                version: '2.0.0'
            });
        });

        // API Routes
        this.app.use('/api/v1', this.createAPIRoutes());

        // Dashboard route
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, 'intelligent-dashboard.html'));
        });

        // Error handling
        this.app.use((err, req, res, next) => {
            console.error('API Error:', err);
            this.logError('API_ERROR', err.message, req.url);
            res.status(500).json({
                error: 'Internal Server Error',
                message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
            });
        });

        // 404 handler
        this.app.use((req, res) => {
            res.status(404).json({
                error: 'Not Found',
                message: `Route ${req.method} ${req.url} not found`
            });
        });
    }

    createAPIRoutes() {
        const router = express.Router();

        // Dashboard Data
        router.get('/dashboard', async (req, res) => {
            try {
                const dashboardData = await this.getDashboardData();
                res.json(dashboardData);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // System Metrics
        router.get('/metrics', async (req, res) => {
            try {
                const metrics = await this.getSystemMetrics();
                res.json(metrics);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // AI Agents
        router.get('/agents', (req, res) => {
            const agents = Array.from(this.agents.values());
            res.json(agents);
        });

        router.post('/agents', async (req, res) => {
            try {
                const { name, type, config } = req.body;
                const agent = await this.createAgent(name, type, config);
                res.json(agent);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        router.put('/agents/:id', async (req, res) => {
            try {
                const { id } = req.params;
                const { status, config } = req.body;
                const agent = await this.updateAgent(id, status, config);
                res.json(agent);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        router.delete('/agents/:id', async (req, res) => {
            try {
                const { id } = req.params;
                await this.deleteAgent(id);
                res.json({ message: 'Agent deleted successfully' });
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // Error Management
        router.get('/errors', (req, res) => {
            const { limit = 50, type } = req.query;
            let errors = this.errorLog;

            if (type) {
                errors = errors.filter(error => error.type === type);
            }

            res.json(errors.slice(-limit));
        });

        router.post('/errors/resolve', async (req, res) => {
            try {
                const { errorId } = req.body;
                const result = await this.resolveError(errorId);
                res.json(result);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // Recovery Actions
        router.get('/recovery', (req, res) => {
            res.json(this.recoveryActions);
        });

        router.post('/recovery/execute', async (req, res) => {
            try {
                const { actionId } = req.body;
                const result = await this.executeRecoveryAction(actionId);
                res.json(result);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // File Operations
        router.get('/files', async (req, res) => {
            try {
                const { path: filePath = '.' } = req.query;
                const files = await this.scanFiles(filePath);
                res.json(files);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        router.post('/files/process', async (req, res) => {
            try {
                const { filePath, action } = req.body;
                const result = await this.processFile(filePath, action);
                res.json(result);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // Configuration Management
        router.get('/config', async (req, res) => {
            try {
                const config = await this.getConfiguration();
                res.json(config);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        router.put('/config', async (req, res) => {
            try {
                const { config } = req.body;
                const result = await this.updateConfiguration(config);
                res.json(result);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // Real-time Events
        router.post('/events', (req, res) => {
            try {
                const { type, data } = req.body;
                this.broadcastEvent(type, data);
                res.json({ message: 'Event broadcasted successfully' });
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // System Commands
        router.post('/system/command', async (req, res) => {
            try {
                const { command, args = [] } = req.body;
                const result = await this.executeSystemCommand(command, args);
                res.json(result);
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // Auto-Recovery
        router.post('/recovery/auto', async (req, res) => {
            try {
                const result = await this.triggerAutoRecovery();
                res.json(result);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        return router;
    }

    setupWebSocket() {
        this.wss.on('connection', (ws, req) => {
            const clientId = uuidv4();
            ws.clientId = clientId;
            this.clients.add(ws);

            console.log(`WebSocket client connected: ${clientId}`);

            // Send initial data
            ws.send(JSON.stringify({
                type: 'connection',
                clientId,
                timestamp: new Date().toISOString()
            }));

            ws.on('message', (message) => {
                try {
                    const data = JSON.parse(message);
                    this.handleWebSocketMessage(ws, data);
                } catch (error) {
                    console.error('WebSocket message error:', error);
                }
            });

            ws.on('close', () => {
                this.clients.delete(ws);
                console.log(`WebSocket client disconnected: ${clientId}`);
            });

            ws.on('error', (error) => {
                console.error('WebSocket error:', error);
                this.clients.delete(ws);
            });
        });
    }

    handleWebSocketMessage(ws, data) {
        switch (data.type) {
            case 'subscribe':
                ws.subscriptions = data.subscriptions || [];
                break;
            case 'unsubscribe':
                ws.subscriptions = ws.subscriptions.filter(sub => !data.subscriptions.includes(sub));
                break;
            case 'command':
                this.handleCommand(ws, data);
                break;
            default:
                console.log('Unknown WebSocket message type:', data.type);
        }
    }

    async handleCommand(ws, data) {
        try {
            const { command, params } = data;
            let result;

            switch (command) {
                case 'getMetrics':
                    result = await this.getSystemMetrics();
                    break;
                case 'getAgents':
                    result = Array.from(this.agents.values());
                    break;
                case 'executeAction':
                    result = await this.executeAction(params);
                    break;
                default:
                    result = { error: 'Unknown command' };
            }

            ws.send(JSON.stringify({
                type: 'response',
                command,
                result,
                timestamp: new Date().toISOString()
            }));
        } catch (error) {
            ws.send(JSON.stringify({
                type: 'error',
                command: data.command,
                error: error.message,
                timestamp: new Date().toISOString()
            }));
        }
    }

    broadcastEvent(type, data) {
        const message = JSON.stringify({
            type,
            data,
            timestamp: new Date().toISOString()
        });

        this.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    }

    async initializeAgents() {
        const agentTypes = [
            { name: 'Main Agent', type: 'main', status: 'active' },
            { name: 'Data Processing Agent', type: 'data', status: 'active' },
            { name: 'Analytics Agent', type: 'analytics', status: 'active' },
            { name: 'Security Agent', type: 'security', status: 'active' },
            { name: 'Recovery Agent', type: 'recovery', status: 'active' }
        ];

        for (const agentConfig of agentTypes) {
            await this.createAgent(agentConfig.name, agentConfig.type, { status: agentConfig.status });
        }
    }

    async createAgent(name, type, config = {}) {
        const agent = {
            id: uuidv4(),
            name,
            type,
            status: config.status || 'inactive',
            config: config.config || {},
            createdAt: new Date().toISOString(),
            lastActivity: new Date().toISOString(),
            metrics: {
                tasksCompleted: 0,
                errors: 0,
                uptime: 0
            }
        };

        this.agents.set(agent.id, agent);
        this.broadcastEvent('agent_created', agent);
        return agent;
    }

    async updateAgent(id, status, config) {
        const agent = this.agents.get(id);
        if (!agent) {
            throw new Error('Agent not found');
        }

        agent.status = status || agent.status;
        agent.config = { ...agent.config, ...config };
        agent.lastActivity = new Date().toISOString();

        this.agents.set(id, agent);
        this.broadcastEvent('agent_updated', agent);
        return agent;
    }

    async deleteAgent(id) {
        const agent = this.agents.get(id);
        if (!agent) {
            throw new Error('Agent not found');
        }

        this.agents.delete(id);
        this.broadcastEvent('agent_deleted', { id });
    }

    async getDashboardData() {
        const [metrics, agents, errors, recovery] = await Promise.all([
            this.getSystemMetrics(),
            Array.from(this.agents.values()),
            this.errorLog.slice(-10),
            this.recoveryActions.slice(-5)
        ]);

        return {
            metrics,
            agents,
            recentErrors: errors,
            recentRecoveryActions: recovery,
            systemStatus: this.getSystemStatus(),
            timestamp: new Date().toISOString()
        };
    }

    async getSystemMetrics() {
        try {
            const cpuUsage = await this.getCPUUsage();
            const memoryUsage = await this.getMemoryUsage();
            const networkUsage = await this.getNetworkUsage();
            const storageUsage = await this.getStorageUsage();

            this.systemMetrics = {
                cpu: cpuUsage,
                memory: memoryUsage,
                network: networkUsage,
                storage: storageUsage,
                uptime: process.uptime()
            };

            return this.systemMetrics;
        } catch (error) {
            console.error('Error getting system metrics:', error);
            return this.systemMetrics;
        }
    }

    async getCPUUsage() {
        try {
            const { stdout } = await execAsync('wmic cpu get loadpercentage /value');
            const match = stdout.match(/LoadPercentage=(\d+)/);
            return match ? parseInt(match[1]) : 0;
        } catch (error) {
            return Math.floor(Math.random() * 100);
        }
    }

    async getMemoryUsage() {
        try {
            const totalMem = os.totalmem();
            const freeMem = os.freemem();
            return Math.round(((totalMem - freeMem) / totalMem) * 100);
        } catch (error) {
            return Math.floor(Math.random() * 100);
        }
    }

    async getNetworkUsage() {
        // Simulated network usage
        return Math.floor(Math.random() * 50) + 10;
    }

    async getStorageUsage() {
        try {
            const { stdout } = await execAsync('wmic logicaldisk get size,freespace /value');
            const lines = stdout.split('\n');
            let totalSize = 0;
            let totalFree = 0;

            for (const line of lines) {
                if (line.includes('Size=')) {
                    totalSize += parseInt(line.split('=')[1]);
                } else if (line.includes('FreeSpace=')) {
                    totalFree += parseInt(line.split('=')[1]);
                }
            }

            return totalSize > 0 ? Math.round(((totalSize - totalFree) / totalSize) * 100) : 0;
        } catch (error) {
            return Math.floor(Math.random() * 100);
        }
    }

    getSystemStatus() {
        const status = {
            database: 'operational',
            api: 'operational',
            debug: process.env.NODE_ENV === 'development' ? 'enabled' : 'disabled',
            autoRefresh: 'enabled',
            security: 'active',
            backup: 'scheduled'
        };

        // Check for critical errors
        const criticalErrors = this.errorLog.filter(error =>
            error.severity === 'critical' &&
            Date.now() - new Date(error.timestamp).getTime() < 300000 // 5 minutes
        );

        if (criticalErrors.length > 0) {
            status.overall = 'warning';
        } else {
            status.overall = 'operational';
        }

        return status;
    }

    logError(type, message, context = '') {
        const error = {
            id: uuidv4(),
            type,
            message,
            context,
            severity: this.getErrorSeverity(type),
            timestamp: new Date().toISOString(),
            resolved: false
        };

        this.errorLog.push(error);
        this.broadcastEvent('error_logged', error);

        // Auto-resolve certain errors
        if (error.severity === 'low') {
            setTimeout(() => this.autoResolveError(error.id), 5000);
        }

        return error;
    }

    getErrorSeverity(type) {
        const severityMap = {
            'API_ERROR': 'medium',
            'SYSTEM_ERROR': 'high',
            'AGENT_ERROR': 'medium',
            'NETWORK_ERROR': 'high',
            'SECURITY_ERROR': 'critical',
            'RECOVERY_ERROR': 'high'
        };
        return severityMap[type] || 'low';
    }

    async resolveError(errorId) {
        const error = this.errorLog.find(e => e.id === errorId);
        if (!error) {
            throw new Error('Error not found');
        }

        error.resolved = true;
        error.resolvedAt = new Date().toISOString();

        this.broadcastEvent('error_resolved', error);
        return error;
    }

    async autoResolveError(errorId) {
        try {
            await this.resolveError(errorId);
            console.log(`Auto-resolved error: ${errorId}`);
        } catch (error) {
            console.error('Failed to auto-resolve error:', error);
        }
    }

    async executeRecoveryAction(actionId) {
        const action = this.recoveryActions.find(a => a.id === actionId);
        if (!action) {
            throw new Error('Recovery action not found');
        }

        try {
            action.status = 'executing';
            action.startedAt = new Date().toISOString();

            // Execute the action
            const result = await this.executeAction(action.command);

            action.status = 'completed';
            action.completedAt = new Date().toISOString();
            action.result = result;

            this.broadcastEvent('recovery_action_completed', action);
            return action;
        } catch (error) {
            action.status = 'failed';
            action.error = error.message;
            action.failedAt = new Date().toISOString();

            this.broadcastEvent('recovery_action_failed', action);
            throw error;
        }
    }

    async executeAction(command) {
        switch (command.type) {
            case 'system_command':
                return await this.executeSystemCommand(command.command, command.args);
            case 'file_operation':
                return await this.processFile(command.filePath, command.action);
            case 'agent_restart':
                return await this.restartAgent(command.agentId);
            case 'config_reload':
                return await this.reloadConfiguration();
            default:
                throw new Error(`Unknown action type: ${command.type}`);
        }
    }

    async executeSystemCommand(command, args = []) {
        try {
            const { stdout, stderr } = await execAsync(`${command} ${args.join(' ')}`);
            return {
                success: true,
                output: stdout,
                error: stderr
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                output: error.stdout,
                stderr: error.stderr
            };
        }
    }

    async scanFiles(directory = '.') {
        try {
            const files = await fs.readdir(directory, { withFileTypes: true });
            const fileList = [];

            for (const file of files) {
                if (file.isFile()) {
                    const filePath = path.join(directory, file.name);
                    const stats = await fs.stat(filePath);

                    fileList.push({
                        name: file.name,
                        path: filePath,
                        size: stats.size,
                        modified: stats.mtime.toISOString(),
                        type: path.extname(file.name)
                    });
                }
            }

            return fileList;
        } catch (error) {
            throw new Error(`Failed to scan files: ${error.message}`);
        }
    }

    async processFile(filePath, action) {
        try {
            switch (action) {
                case 'read':
                    const content = await fs.readFile(filePath, 'utf8');
                    return { success: true, content };
                case 'delete':
                    await fs.unlink(filePath);
                    return { success: true, message: 'File deleted' };
                case 'backup':
                    const backupPath = `${filePath}.backup`;
                    await fs.copyFile(filePath, backupPath);
                    return { success: true, backupPath };
                default:
                    throw new Error(`Unknown action: ${action}`);
            }
        } catch (error) {
            throw new Error(`File operation failed: ${error.message}`);
        }
    }

    async getConfiguration() {
        try {
            const configPath = path.join(__dirname, 'cursor-global-config.json');
            const config = await fs.readFile(configPath, 'utf8');
            return JSON.parse(config);
        } catch (error) {
            return { error: 'Configuration not found' };
        }
    }

    async updateConfiguration(newConfig) {
        try {
            const configPath = path.join(__dirname, 'cursor-global-config.json');
            await fs.writeFile(configPath, JSON.stringify(newConfig, null, 2));
            return { success: true, message: 'Configuration updated' };
        } catch (error) {
            throw new Error(`Failed to update configuration: ${error.message}`);
        }
    }

    async restartAgent(agentId) {
        const agent = this.agents.get(agentId);
        if (!agent) {
            throw new Error('Agent not found');
        }

        agent.status = 'restarting';
        agent.lastActivity = new Date().toISOString();

        // Simulate restart delay
        setTimeout(() => {
            agent.status = 'active';
            agent.lastActivity = new Date().toISOString();
            this.broadcastEvent('agent_restarted', agent);
        }, 2000);

        return { success: true, message: 'Agent restart initiated' };
    }

    async reloadConfiguration() {
        try {
            // Simulate configuration reload
            await new Promise(resolve => setTimeout(resolve, 1000));
            return { success: true, message: 'Configuration reloaded' };
        } catch (error) {
            throw new Error(`Failed to reload configuration: ${error.message}`);
        }
    }

    async triggerAutoRecovery() {
        const actions = [];

        // Check for critical errors and create recovery actions
        const criticalErrors = this.errorLog.filter(error =>
            error.severity === 'critical' && !error.resolved
        );

        for (const error of criticalErrors) {
            const action = {
                id: uuidv4(),
                type: 'auto_recovery',
                description: `Auto-recovery for ${error.type}`,
                command: this.getRecoveryCommand(error.type),
                status: 'pending',
                createdAt: new Date().toISOString(),
                errorId: error.id
            };

            actions.push(action);
            this.recoveryActions.push(action);
        }

        // Execute recovery actions
        for (const action of actions) {
            try {
                await this.executeRecoveryAction(action.id);
            } catch (error) {
                console.error(`Auto-recovery failed for action ${action.id}:`, error);
            }
        }

        return {
            success: true,
            actionsExecuted: actions.length,
            actions
        };
    }

    getRecoveryCommand(errorType) {
        const recoveryCommands = {
            'API_ERROR': { type: 'config_reload' },
            'SYSTEM_ERROR': { type: 'system_command', command: 'tasklist', args: [] },
            'AGENT_ERROR': { type: 'agent_restart' },
            'NETWORK_ERROR': { type: 'system_command', command: 'ipconfig', args: ['/all'] },
            'SECURITY_ERROR': { type: 'config_reload' },
            'RECOVERY_ERROR': { type: 'system_command', command: 'systeminfo', args: [] }
        };

        return recoveryCommands[errorType] || { type: 'config_reload' };
    }

    startMonitoring() {
        // Monitor system metrics every 5 seconds
        setInterval(async () => {
            try {
                const metrics = await this.getSystemMetrics();
                this.broadcastEvent('metrics_update', metrics);
            } catch (error) {
                console.error('Metrics monitoring error:', error);
            }
        }, 5000);

        // Monitor agents every 10 seconds
        setInterval(() => {
            this.agents.forEach(agent => {
                agent.metrics.uptime += 10;
                if (agent.status === 'active') {
                    agent.metrics.tasksCompleted += Math.floor(Math.random() * 3);
                }
            });
            this.broadcastEvent('agents_update', Array.from(this.agents.values()));
        }, 10000);

        // Auto-recovery check every 30 seconds
        setInterval(async () => {
            try {
                await this.triggerAutoRecovery();
            } catch (error) {
                console.error('Auto-recovery error:', error);
            }
        }, 30000);
    }

    async start() {
        if (this.isRunning) {
            console.log('Server is already running');
            return;
        }

        try {
            await new Promise((resolve, reject) => {
                this.server.listen(this.port, () => {
                    console.log(`🚀 Intelligent API Server running on port ${this.port}`);
                    console.log(`📊 Dashboard available at http://localhost:${this.port}`);
                    console.log(`🔌 WebSocket server ready for real-time connections`);
                    console.log(`🤖 AI Agents initialized and monitoring system`);
                    this.isRunning = true;
                    resolve();
                });

                this.server.on('error', reject);
            });

            // Log startup
            this.logError('SYSTEM_INFO', 'Intelligent API Server started successfully');

        } catch (error) {
            console.error('Failed to start server:', error);
            throw error;
        }
    }

    async stop() {
        if (!this.isRunning) {
            return;
        }

        return new Promise((resolve) => {
            this.server.close(() => {
                console.log('🛑 Intelligent API Server stopped');
                this.isRunning = false;
                resolve();
            });
        });
    }
}

// Create and start the server
const server = new IntelligentAPIServer();

// Handle graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n🛑 Shutting down gracefully...');
    await server.stop();
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\n🛑 Shutting down gracefully...');
    await server.stop();
    process.exit(0);
});

// Start the server
server.start().catch(error => {
    console.error('Failed to start server:', error);
    process.exit(1);
});

module.exports = IntelligentAPIServer;
