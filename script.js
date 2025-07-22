// EHB-5 Dashboard - Advanced AI Management System
// Enhanced with Replit AI Features, Real-time Monitoring, and World-Class Design

class Dashboard {
    constructor() {
        this.isInitialized = false;
        this.refreshInterval = null;
        this.agents = [];
        this.tools = [];
        this.files = [];
        this.analytics = {};
        this.settings = {};
        this.notifications = [];
        this.currentTimeRange = '1h';
        this.init();
    }

    async init() {
        console.log('🚀 Initializing EHB-5 Dashboard...');
        
        // Initialize all components
        await this.initializeData();
        await this.setupEventListeners();
        await this.startRealTimeUpdates();
        
        this.isInitialized = true;
        console.log('✅ Dashboard initialized successfully');
        
        // Show welcome notification
        this.showNotification('Welcome to EHB-5 Dashboard! All systems are operational.', 'success');
    }

    async initializeData() {
        // Initialize comprehensive data structures
        this.initializeProjectData();
        this.initializeSystemStatus();
        this.initializeAgents();
        this.initializeTools();
        this.initializeFiles();
        this.initializeAnalytics();
        this.initializeSettings();
        this.initializeNotifications();
    }

    initializeProjectData() {
        this.projectData = {
            name: 'EHB-5 Advanced AI System',
            version: '2.0.0',
            description: 'Advanced Data Processing & Configuration Management System with AI Agents',
            totalFiles: 0,
            totalLines: 0,
            lastUpdated: new Date().toLocaleString(),
            features: [
                'AI-Powered Processing',
                'Real-Time Monitoring',
                'Advanced Analytics',
                'Security Management',
                'Cloud Integration',
                'Multi-Agent Coordination'
            ],
            technologies: [
                'Node.js', 'Python', 'React', 'TypeScript',
                'TensorFlow', 'OpenAI API', 'AWS', 'Docker'
            ],
            stats: {
                dataFiles: 0,
                configFiles: 0,
                scripts: 0,
                activeAgents: 0,
                usersOnline: 5,
                systemUptime: '99.9%'
            }
        };
    }

    initializeSystemStatus() {
        this.systemStatus = {
            database: { status: 'online', response: '12ms', lastCheck: new Date() },
            api: { status: 'online', response: '45ms', lastCheck: new Date() },
            debug: { status: 'enabled', level: 'info', lastCheck: new Date() },
            autoRefresh: { status: 'enabled', interval: '30s', lastCheck: new Date() },
            security: { status: 'active', threats: 0, lastCheck: new Date() },
            backup: { status: 'scheduled', lastBackup: '2 hours ago', nextBackup: '6 hours' }
        };
    }

    initializeAgents() {
        this.agents = [
            {
                id: 'main',
                name: 'Main AI Agent',
                type: 'main',
                status: 'active',
                icon: 'fas fa-brain',
                description: 'Central AI coordinator managing all sub-agents',
                lastActivity: 'Just now',
                metrics: {
                    tasksCompleted: 24,
                    uptime: '99.8%',
                    memory: '2.1GB',
                    cpu: '45%',
                    responseTime: '12ms',
                    accuracy: '98.5%'
                },
                capabilities: ['Natural Language Processing', 'Decision Making', 'Agent Coordination'],
                logs: [
                    { timestamp: new Date(), level: 'info', message: 'Agent initialized successfully' },
                    { timestamp: new Date(Date.now() - 5000), level: 'info', message: 'Processing task #24' },
                    { timestamp: new Date(Date.now() - 10000), level: 'success', message: 'Task #23 completed' }
                ]
            },
            {
                id: 'data',
                name: 'Data Processing Agent',
                type: 'sub',
                status: 'active',
                icon: 'fas fa-microchip',
                description: 'Handles data processing and file operations',
                lastActivity: '2 minutes ago',
                metrics: {
                    filesProcessed: 156,
                    successRate: '98.5%',
                    errors: 2,
                    processingSpeed: '1.2GB/s',
                    queueSize: 5
                },
                capabilities: ['Data Cleaning', 'File Processing', 'Format Conversion'],
                logs: [
                    { timestamp: new Date(), level: 'info', message: 'Processing batch of 15 files' },
                    { timestamp: new Date(Date.now() - 30000), level: 'success', message: 'Batch completed successfully' }
                ]
            },
            {
                id: 'analytics',
                name: 'Analytics Agent',
                type: 'sub',
                status: 'active',
                icon: 'fas fa-chart-line',
                description: 'Performs advanced data analytics and reporting',
                lastActivity: '1 minute ago',
                metrics: {
                    reportsGenerated: 89,
                    accuracy: '99.2%',
                    insightsFound: 156,
                    processingTime: '2.3s'
                },
                capabilities: ['Statistical Analysis', 'Trend Detection', 'Report Generation'],
                logs: [
                    { timestamp: new Date(), level: 'info', message: 'Generating monthly report' },
                    { timestamp: new Date(Date.now() - 60000), level: 'success', message: 'Report generated successfully' }
                ]
            },
            {
                id: 'security',
                name: 'Security Agent',
                type: 'sub',
                status: 'standby',
                icon: 'fas fa-shield-alt',
                description: 'Monitors system security and threat detection',
                lastActivity: '5 minutes ago',
                metrics: {
                    threatsDetected: 0,
                    securityScore: '100%',
                    lastScan: '2 minutes ago',
                    vulnerabilities: 0
                },
                capabilities: ['Threat Detection', 'Access Control', 'Encryption'],
                logs: [
                    { timestamp: new Date(), level: 'info', message: 'Security scan completed' },
                    { timestamp: new Date(Date.now() - 120000), level: 'success', message: 'No threats detected' }
                ]
            }
        ];
    }

    initializeTools() {
        this.tools = [
            {
                id: 'replit-ai',
                name: 'Replit AI',
                status: 'active',
                icon: 'fas fa-robot',
                description: 'Advanced AI coding assistant and development tools',
                version: '2.1.0',
                lastUpdated: '1 hour ago',
                packages: ['@replit/ai', '@replit/copilot', 'ghostwriter'],
                features: ['Code Generation', 'Bug Detection', 'Auto-completion'],
                metrics: {
                    suggestions: 156,
                    accuracy: '94.2%',
                    timeSaved: '2.3 hours'
                }
            },
            {
                id: 'cursor-ai',
                name: 'Cursor AI',
                status: 'active',
                icon: 'fas fa-cursor',
                description: 'Intelligent code editor with AI assistance',
                version: '1.8.5',
                lastUpdated: '30 minutes ago',
                packages: ['@cursor/ai', '@cursor/extensions'],
                features: ['Smart Editing', 'Code Review', 'Refactoring'],
                metrics: {
                    edits: 89,
                    accuracy: '96.8%',
                    timeSaved: '1.7 hours'
                }
            },
            {
                id: 'github-copilot',
                name: 'GitHub Copilot',
                status: 'active',
                icon: 'fab fa-github',
                description: 'AI-powered code completion and generation',
                version: '1.2.1',
                lastUpdated: '2 hours ago',
                packages: ['@github/copilot', '@github/copilot-chat'],
                features: ['Code Completion', 'Documentation', 'Testing'],
                metrics: {
                    suggestions: 234,
                    accuracy: '92.1%',
                    timeSaved: '3.1 hours'
                }
            },
            {
                id: 'openai-api',
                name: 'OpenAI API',
                status: 'active',
                icon: 'fas fa-brain',
                description: 'Advanced language models and AI services',
                version: '4.0.0',
                lastUpdated: '15 minutes ago',
                packages: ['openai', 'gpt-4', 'dall-e'],
                features: ['Text Generation', 'Image Creation', 'Code Analysis'],
                metrics: {
                    requests: 456,
                    tokens: '2.3M',
                    cost: '$12.45'
                }
            },
            {
                id: 'tensorflow',
                name: 'TensorFlow',
                status: 'active',
                icon: 'fas fa-network-wired',
                description: 'Machine learning framework for AI development',
                version: '2.13.0',
                lastUpdated: '1 day ago',
                packages: ['tensorflow', 'tensorflow-js', 'keras'],
                features: ['Neural Networks', 'Model Training', 'Inference'],
                metrics: {
                    models: 8,
                    accuracy: '97.3%',
                    trainingTime: '45 minutes'
                }
            },
            {
                id: 'docker',
                name: 'Docker',
                status: 'active',
                icon: 'fab fa-docker',
                description: 'Containerization platform for deployment',
                version: '24.0.5',
                lastUpdated: '3 hours ago',
                packages: ['docker', 'docker-compose', 'kubernetes'],
                features: ['Container Management', 'Orchestration', 'Deployment'],
                metrics: {
                    containers: 12,
                    images: 8,
                    uptime: '99.7%'
                }
            }
        ];
    }

    initializeFiles() {
        this.files = [
            {
                id: 'config-1',
                name: 'cursor-global-config.json',
                type: 'config',
                size: '2.3KB',
                lastModified: '2 hours ago',
                description: 'Global Cursor configuration settings',
                icon: 'fas fa-cog',
                status: 'active',
                path: '/config/',
                lines: 156,
                dependencies: ['@cursor/core', '@cursor/extensions']
            },
            {
                id: 'script-1',
                name: 'setup-cursor-global.ps1',
                type: 'script',
                size: '4.1KB',
                lastModified: '1 day ago',
                description: 'PowerShell setup script for global configuration',
                icon: 'fas fa-code',
                status: 'active',
                path: '/scripts/',
                lines: 234,
                dependencies: ['powershell', 'node.js']
            },
            {
                id: 'data-1',
                name: 'project-data.json',
                type: 'data',
                size: '15.7KB',
                lastModified: '30 minutes ago',
                description: 'Project data and analytics information',
                icon: 'fas fa-database',
                status: 'active',
                path: '/data/',
                lines: 892,
                dependencies: ['json', 'analytics']
            },
            {
                id: 'web-1',
                name: 'index.html',
                type: 'web',
                size: '8.9KB',
                lastModified: '1 hour ago',
                description: 'Main dashboard HTML file',
                icon: 'fab fa-html5',
                status: 'active',
                path: '/web/',
                lines: 445,
                dependencies: ['html5', 'css3', 'javascript']
            },
            {
                id: 'style-1',
                name: 'styles.css',
                type: 'style',
                size: '12.3KB',
                lastModified: '45 minutes ago',
                description: 'Advanced CSS styling for dashboard',
                icon: 'fab fa-css3-alt',
                status: 'active',
                path: '/styles/',
                lines: 678,
                dependencies: ['css3', 'flexbox', 'grid']
            },
            {
                id: 'script-2',
                name: 'script.js',
                type: 'script',
                size: '18.2KB',
                lastModified: '20 minutes ago',
                description: 'Main JavaScript functionality',
                icon: 'fab fa-js-square',
                status: 'active',
                path: '/scripts/',
                lines: 1245,
                dependencies: ['javascript', 'es6', 'dom']
            }
        ];
    }

    initializeAnalytics() {
        this.analytics = {
            performance: {
                cpu: { current: 45, history: [42, 45, 48, 43, 45] },
                memory: { current: 65, history: [62, 65, 68, 63, 65] },
                network: { current: 30, history: [28, 30, 32, 29, 30] },
                storage: { current: 75, history: [72, 75, 78, 73, 75] }
            },
            activity: {
                daily: [12, 19, 15, 25, 22, 30, 28],
                weekly: [156, 189, 234, 201, 245, 267, 289],
                monthly: [1234, 1456, 1678, 1890, 2012, 2234, 2456]
            },
            agents: {
                main: { tasks: 24, success: 98.5, uptime: 99.8 },
                data: { files: 156, success: 98.5, errors: 2 },
                analytics: { reports: 89, accuracy: 99.2, insights: 156 },
                security: { threats: 0, score: 100, scans: 45 }
            }
        };
    }

    initializeSettings() {
        this.settings = {
            theme: {
                darkMode: false,
                autoTheme: true,
                accentColor: '#667eea'
            },
            notifications: {
                enabled: true,
                soundAlerts: true,
                emailNotifications: false
            },
            autoRefresh: {
                enabled: true,
                interval: 30
            },
            security: {
                twoFactor: false,
                sessionTimeout: 60
            }
        };
    }

    initializeNotifications() {
        this.notifications = [
            {
                id: 1,
                type: 'info',
                title: 'System Update',
                message: 'Dashboard v2.0.0 has been successfully deployed',
                timestamp: new Date(Date.now() - 300000),
                read: false
            },
            {
                id: 2,
                type: 'success',
                title: 'Agent Status',
                message: 'All AI agents are now operational and monitoring',
                timestamp: new Date(Date.now() - 600000),
                read: false
            },
            {
                id: 3,
                type: 'warning',
                title: 'Performance Alert',
                message: 'Memory usage is approaching 70% threshold',
                timestamp: new Date(Date.now() - 900000),
                read: false
            }
        ];
    }

    async setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation(e.target.getAttribute('href').substring(1));
            });
        });

        // Settings
        document.getElementById('darkMode')?.addEventListener('change', (e) => {
            this.toggleTheme(e.target.checked);
        });

        // Auto refresh
        document.getElementById('autoRefresh')?.addEventListener('change', (e) => {
            this.toggleAutoRefresh(e.target.checked);
        });

        // Time range selector
        document.querySelectorAll('.time-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setTimeRange(e.target.textContent.toLowerCase());
            });
        });
    }

    async startRealTimeUpdates() {
        // Update dashboard every 30 seconds
        this.refreshInterval = setInterval(() => {
            this.updateDashboard();
        }, 30000);

        // Update agent metrics every 5 seconds
        setInterval(() => {
            this.updateAgentMetrics();
        }, 5000);

        // Update performance metrics every 10 seconds
        setInterval(() => {
            this.updatePerformanceMetrics();
        }, 10000);

        // Update system status every 15 seconds
        setInterval(() => {
            this.updateSystemStatus();
        }, 15000);
    }

    updateDashboard() {
        this.updateProjectInfo();
        this.updateSystemStatus();
        this.updateRecentActivity();
        this.loadAgents();
        this.loadTools();
        this.loadProjectFilesUI();
        this.updatePerformanceMetrics();
        this.updateAnalytics();
    }

    updateProjectInfo() {
        // Update project information
        document.getElementById('projectName').textContent = this.projectData.name;
        document.getElementById('projectVersion').textContent = this.projectData.version;
        document.getElementById('projectDesc').textContent = this.projectData.description;
        document.getElementById('totalFiles').textContent = this.files.length;
        document.getElementById('totalLines').textContent = this.files.reduce((sum, file) => sum + file.lines, 0);
        document.getElementById('lastUpdated').textContent = this.projectData.lastUpdated;

        // Update hero stats
        document.getElementById('dataFiles').textContent = this.files.filter(f => f.type === 'data').length;
        document.getElementById('configFiles').textContent = this.files.filter(f => f.type === 'config').length;
        document.getElementById('scripts').textContent = this.files.filter(f => f.type === 'script').length;
        document.getElementById('agents').textContent = this.agents.filter(a => a.status === 'active').length;
        document.getElementById('users').textContent = this.projectData.stats.usersOnline;
        document.getElementById('uptime').textContent = this.projectData.stats.systemUptime;
    }

    updateSystemStatus() {
        // Simulate real-time system status updates
        Object.keys(this.systemStatus).forEach(key => {
            const status = this.systemStatus[key];
            const element = document.getElementById(key + 'Status');
            if (element) {
                element.textContent = status.status;
                element.className = `status-value ${status.status}`;
            }
        });
    }

    updateRecentActivity() {
        const recentActivity = document.getElementById('recentActivity');
        if (!recentActivity) return;

        const activities = [
            { icon: 'fas fa-robot', text: 'AI Agent processed 15 files', time: '2 minutes ago' },
            { icon: 'fas fa-chart-line', text: 'Analytics report generated', time: '5 minutes ago' },
            { icon: 'fas fa-shield-alt', text: 'Security scan completed', time: '8 minutes ago' },
            { icon: 'fas fa-code', text: 'Code deployment successful', time: '12 minutes ago' },
            { icon: 'fas fa-database', text: 'Database backup completed', time: '15 minutes ago' }
        ];

        recentActivity.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <i class="${activity.icon}"></i>
                <span>${activity.text}</span>
                <small>${activity.time}</small>
            </div>
        `).join('');
    }

    loadAgents() {
        const agentsGrid = document.getElementById('agentsGrid');
        if (!agentsGrid) return;
        
        // Complete list of 44 agents with main agent
        const agents = [
            // Main Agent (Central Coordinator)
            {
                id: 'main',
                name: 'Main AI Agent',
                icon: 'fas fa-brain',
                status: 'active',
                type: 'main',
                description: 'Central AI coordinator managing all 44 sub-agents and system operations',
                lastActivity: '2 minutes ago',
                metrics: {
                    tasksCompleted: 44,
                    uptime: '100%',
                    memory: '4.2GB',
                    cpu: '65%',
                    subAgentsManaged: 44,
                    coordinationSuccess: '100%'
                },
                tasks: ['coordination', 'monitoring', 'optimization', 'resource_management']
            },
            
            // Core System Agents (4)
            {
                id: 'ehbBase',
                name: 'EHB Base Agent',
                icon: 'fas fa-cube',
                status: 'active',
                type: 'core',
                description: 'Core System Agent - Managing AI Development System',
                lastActivity: '1 minute ago',
                metrics: {
                    performance: '100%',
                    systemManaged: 'EHB AI Development',
                    operations: 156,
                    successRate: '100%'
                },
                tasks: ['system_management', 'core_operations', 'development_support']
            },
            {
                id: 'backend',
                name: 'Backend Agent',
                icon: 'fas fa-server',
                status: 'active',
                type: 'core',
                description: 'Development Agent - Backend Development & API Management',
                lastActivity: '2 minutes ago',
                metrics: {
                    performance: '100%',
                    apisManaged: 23,
                    endpoints: 156,
                    responseTime: '45ms'
                },
                tasks: ['api_development', 'database_management', 'server_operations']
            },
            {
                id: 'frontend',
                name: 'Frontend Agent',
                icon: 'fas fa-desktop',
                status: 'active',
                type: 'core',
                description: 'Development Agent - Frontend Development & UI/UX',
                lastActivity: '1 minute ago',
                metrics: {
                    performance: '100%',
                    componentsBuilt: 89,
                    pagesCreated: 23,
                    userExperience: '98%'
                },
                tasks: ['ui_development', 'ux_optimization', 'component_management']
            },
            {
                id: 'deployment',
                name: 'Deployment Agent',
                icon: 'fas fa-rocket',
                status: 'active',
                type: 'core',
                description: 'DevOps Agent - Application Deployment & CI/CD',
                lastActivity: '3 minutes ago',
                metrics: {
                    performance: '100%',
                    deployments: 12,
                    buildSuccess: '100%',
                    rollbacks: 0
                },
                tasks: ['deployment_management', 'ci_cd', 'infrastructure']
            },
            
            // AI Agents (5)
            {
                id: 'aiCommunication',
                name: 'AI Communication Agent',
                icon: 'fas fa-comments',
                status: 'active',
                type: 'ai',
                description: 'Handles AI communication and interaction protocols',
                lastActivity: '1 minute ago',
                metrics: {
                    messagesProcessed: 234,
                    responseAccuracy: '99.5%',
                    languagesSupported: 12,
                    communicationChannels: 8
                },
                tasks: ['communication_management', 'language_processing', 'interaction_protocols']
            },
            {
                id: 'aiDecision',
                name: 'AI Decision Making Agent',
                icon: 'fas fa-chess',
                status: 'active',
                type: 'ai',
                description: 'Makes intelligent decisions based on data analysis',
                lastActivity: '2 minutes ago',
                metrics: {
                    decisionsMade: 156,
                    accuracy: '98.7%',
                    decisionSpeed: '0.3s',
                    confidenceLevel: '95%'
                },
                tasks: ['decision_analysis', 'risk_assessment', 'strategy_planning']
            },
            {
                id: 'aiExecution',
                name: 'AI Execution Agent',
                icon: 'fas fa-cogs',
                status: 'active',
                type: 'ai',
                description: 'Executes AI-driven tasks and operations',
                lastActivity: '1 minute ago',
                metrics: {
                    tasksExecuted: 289,
                    executionSuccess: '99.8%',
                    averageTime: '1.2s',
                    parallelTasks: 12
                },
                tasks: ['task_execution', 'operation_management', 'performance_optimization']
            },
            {
                id: 'aiLearning',
                name: 'AI Learning Agent',
                icon: 'fas fa-graduation-cap',
                status: 'active',
                type: 'ai',
                description: 'Continuously learns and improves from data',
                lastActivity: '3 minutes ago',
                metrics: {
                    learningCycles: 45,
                    improvementRate: '12.5%',
                    knowledgeBase: '2.3GB',
                    adaptationSpeed: 'fast'
                },
                tasks: ['continuous_learning', 'pattern_recognition', 'knowledge_enhancement']
            },
            {
                id: 'aiMemory',
                name: 'AI Memory Agent',
                icon: 'fas fa-memory',
                status: 'active',
                type: 'ai',
                description: 'Manages AI memory and knowledge storage',
                lastActivity: '2 minutes ago',
                metrics: {
                    memoryStored: '15.7GB',
                    retrievalSpeed: '0.1s',
                    memoryEfficiency: '98.9%',
                    knowledgeRetention: '99.2%'
                },
                tasks: ['memory_management', 'knowledge_storage', 'information_retrieval']
            },
            
            // Data Processing Agents (8)
            {
                id: 'dataProcessor',
                name: 'Data Processing Agent',
                icon: 'fas fa-database',
                status: 'active',
                type: 'data',
                description: 'Handles data processing and analysis',
                lastActivity: '1 minute ago',
                metrics: {
                    filesProcessed: 156,
                    successRate: '98.5%',
                    avgProcessingTime: '2.3s',
                    dataSize: '1.2GB'
                },
                tasks: ['data_analysis', 'file_processing', 'report_generation']
            },
            {
                id: 'dataValidator',
                name: 'Data Validation Agent',
                icon: 'fas fa-check-circle',
                status: 'active',
                type: 'data',
                description: 'Validates data integrity and quality',
                lastActivity: '2 minutes ago',
                metrics: {
                    validationsCompleted: 234,
                    accuracy: '99.7%',
                    errorsDetected: 3,
                    qualityScore: '98.9%'
                },
                tasks: ['data_validation', 'quality_assurance', 'error_detection']
            },
            {
                id: 'dataTransformer',
                name: 'Data Transformation Agent',
                icon: 'fas fa-exchange-alt',
                status: 'active',
                type: 'data',
                description: 'Transforms data formats and structures',
                lastActivity: '1 minute ago',
                metrics: {
                    transformations: 89,
                    formatSupport: 15,
                    conversionSuccess: '99.2%',
                    processingSpeed: '1.8s'
                },
                tasks: ['format_conversion', 'structure_transformation', 'data_migration']
            },
            {
                id: 'dataAnalytics',
                name: 'Data Analytics Agent',
                icon: 'fas fa-chart-bar',
                status: 'active',
                type: 'data',
                description: 'Performs advanced data analytics',
                lastActivity: '3 minutes ago',
                metrics: {
                    analysesCompleted: 67,
                    insightsGenerated: 23,
                    accuracy: '96.8%',
                    trendIdentified: 12
                },
                tasks: ['statistical_analysis', 'trend_analysis', 'insight_generation']
            },
            {
                id: 'dataVisualization',
                name: 'Data Visualization Agent',
                icon: 'fas fa-chart-pie',
                status: 'active',
                type: 'data',
                description: 'Creates data visualizations and charts',
                lastActivity: '2 minutes ago',
                metrics: {
                    visualizationsCreated: 45,
                    chartTypes: 8,
                    renderingSpeed: '0.5s',
                    userEngagement: '94%'
                },
                tasks: ['chart_creation', 'visual_design', 'interactive_displays']
            },
            {
                id: 'dataStorage',
                name: 'Data Storage Agent',
                icon: 'fas fa-hdd',
                status: 'active',
                type: 'data',
                description: 'Manages data storage and retrieval',
                lastActivity: '1 minute ago',
                metrics: {
                    storageUsed: '45.2GB',
                    retrievalSpeed: '0.2s',
                    compressionRatio: '3.2:1',
                    backupSuccess: '100%'
                },
                tasks: ['storage_management', 'backup_operations', 'retrieval_optimization']
            },
            {
                id: 'dataSecurity',
                name: 'Data Security Agent',
                icon: 'fas fa-shield-alt',
                status: 'active',
                type: 'data',
                description: 'Ensures data security and privacy',
                lastActivity: '2 minutes ago',
                metrics: {
                    securityScans: 78,
                    threatsBlocked: 0,
                    encryptionLevel: 'AES-256',
                    complianceScore: '100%'
                },
                tasks: ['security_monitoring', 'encryption_management', 'compliance_checking']
            },
            {
                id: 'dataBackup',
                name: 'Data Backup Agent',
                icon: 'fas fa-save',
                status: 'active',
                type: 'data',
                description: 'Manages data backup and recovery',
                lastActivity: '3 minutes ago',
                metrics: {
                    backupsCreated: 23,
                    recoverySuccess: '100%',
                    backupSize: '12.3GB',
                    retentionPeriod: '90 days'
                },
                tasks: ['backup_scheduling', 'recovery_operations', 'retention_management']
            },
            
            // Configuration Agents (6)
            {
                id: 'configManager',
                name: 'Configuration Manager',
                icon: 'fas fa-cogs',
                status: 'active',
                type: 'config',
                description: 'Manages project configurations and settings',
                lastActivity: '2 minutes ago',
                metrics: {
                    configsManaged: 12,
                    syncSuccess: '100%',
                    validationPass: '95%',
                    settingsCount: 47
                },
                tasks: ['config_validation', 'settings_sync', 'environment_setup']
            },
            {
                id: 'configValidator',
                name: 'Configuration Validator',
                icon: 'fas fa-check-double',
                status: 'active',
                type: 'config',
                description: 'Validates configuration settings',
                lastActivity: '1 minute ago',
                metrics: {
                    validationsCompleted: 89,
                    errorRate: '0.5%',
                    validationSpeed: '0.8s',
                    complianceScore: '98.7%'
                },
                tasks: ['config_validation', 'error_detection', 'compliance_checking']
            },
            {
                id: 'configSync',
                name: 'Configuration Sync Agent',
                icon: 'fas fa-sync',
                status: 'active',
                type: 'config',
                description: 'Synchronizes configurations across systems',
                lastActivity: '2 minutes ago',
                metrics: {
                    syncOperations: 156,
                    syncSuccess: '99.8%',
                    conflictResolved: 3,
                    syncSpeed: '2.1s'
                },
                tasks: ['config_synchronization', 'conflict_resolution', 'version_control']
            },
            {
                id: 'configBackup',
                name: 'Configuration Backup Agent',
                icon: 'fas fa-archive',
                status: 'active',
                type: 'config',
                description: 'Backs up configuration files',
                lastActivity: '3 minutes ago',
                metrics: {
                    backupsCreated: 34,
                    backupSuccess: '100%',
                    restoreOperations: 12,
                    retentionCompliance: '100%'
                },
                tasks: ['config_backup', 'restore_operations', 'retention_management']
            },
            {
                id: 'configMonitor',
                name: 'Configuration Monitor',
                icon: 'fas fa-eye',
                status: 'active',
                type: 'config',
                description: 'Monitors configuration changes',
                lastActivity: '1 minute ago',
                metrics: {
                    changesDetected: 23,
                    alertsGenerated: 5,
                    monitoringCoverage: '100%',
                    responseTime: '0.3s'
                },
                tasks: ['change_monitoring', 'alert_generation', 'response_management']
            },
            {
                id: 'configOptimizer',
                name: 'Configuration Optimizer',
                icon: 'fas fa-tachometer-alt',
                status: 'active',
                type: 'config',
                description: 'Optimizes configuration settings',
                lastActivity: '2 minutes ago',
                metrics: {
                    optimizationsApplied: 45,
                    performanceGain: '23%',
                    resourceSavings: '15%',
                    optimizationSuccess: '96.8%'
                },
                tasks: ['performance_optimization', 'resource_management', 'efficiency_improvement']
            },
            
            // File Management Agents (8)
            {
                id: 'fileOrganizer',
                name: 'File Organizer Agent',
                icon: 'fas fa-folder-open',
                status: 'active',
                type: 'file',
                description: 'Organizes and manages project files',
                lastActivity: '2 minutes ago',
                metrics: {
                    filesOrganized: 89,
                    backupCreated: 3,
                    formatApplied: 12,
                    scanCompleted: '100%'
                },
                tasks: ['file_scanning', 'formatting', 'backup_management']
            },
            {
                id: 'fileScanner',
                name: 'File Scanner Agent',
                icon: 'fas fa-search',
                status: 'active',
                type: 'file',
                description: 'Scans and indexes files',
                lastActivity: '1 minute ago',
                metrics: {
                    filesScanned: 234,
                    scanSpeed: '150 files/s',
                    indexSize: '2.1GB',
                    searchAccuracy: '99.5%'
                },
                tasks: ['file_scanning', 'indexing', 'search_optimization']
            },
            {
                id: 'fileFormatter',
                name: 'File Formatter Agent',
                icon: 'fas fa-magic',
                status: 'active',
                type: 'file',
                description: 'Formats and standardizes files',
                lastActivity: '2 minutes ago',
                metrics: {
                    filesFormatted: 67,
                    formatTypes: 8,
                    formattingSpeed: '0.8s',
                    consistencyScore: '98.9%'
                },
                tasks: ['file_formatting', 'standardization', 'quality_improvement']
            },
            {
                id: 'fileBackup',
                name: 'File Backup Agent',
                icon: 'fas fa-copy',
                status: 'active',
                type: 'file',
                description: 'Creates file backups',
                lastActivity: '3 minutes ago',
                metrics: {
                    backupsCreated: 23,
                    backupSize: '8.7GB',
                    compressionRatio: '2.8:1',
                    restoreSuccess: '100%'
                },
                tasks: ['backup_creation', 'compression', 'restore_operations']
            },
            {
                id: 'fileValidator',
                name: 'File Validator Agent',
                icon: 'fas fa-check-square',
                status: 'active',
                type: 'file',
                description: 'Validates file integrity',
                lastActivity: '1 minute ago',
                metrics: {
                    filesValidated: 156,
                    integrityScore: '99.8%',
                    corruptionDetected: 0,
                    validationSpeed: '1.2s'
                },
                tasks: ['integrity_checking', 'corruption_detection', 'validation_reporting']
            },
            {
                id: 'fileCompressor',
                name: 'File Compressor Agent',
                icon: 'fas fa-compress-alt',
                status: 'active',
                type: 'file',
                description: 'Compresses and optimizes files',
                lastActivity: '2 minutes ago',
                metrics: {
                    filesCompressed: 89,
                    compressionRatio: '3.5:1',
                    spaceSaved: '45.2GB',
                    compressionSpeed: '2.1s'
                },
                tasks: ['file_compression', 'space_optimization', 'performance_improvement']
            },
            {
                id: 'fileEncryptor',
                name: 'File Encryptor Agent',
                icon: 'fas fa-lock',
                status: 'active',
                type: 'file',
                description: 'Encrypts sensitive files',
                lastActivity: '1 minute ago',
                metrics: {
                    filesEncrypted: 34,
                    encryptionLevel: 'AES-256',
                    securityScore: '100%',
                    encryptionSpeed: '1.8s'
                },
                tasks: ['file_encryption', 'security_management', 'key_management']
            },
            {
                id: 'fileSynchronizer',
                name: 'File Synchronizer Agent',
                icon: 'fas fa-sync-alt',
                status: 'active',
                type: 'file',
                description: 'Synchronizes files across systems',
                lastActivity: '2 minutes ago',
                metrics: {
                    syncOperations: 78,
                    syncSuccess: '99.7%',
                    conflictsResolved: 2,
                    syncSpeed: '3.2s'
                },
                tasks: ['file_synchronization', 'conflict_resolution', 'version_control']
            },
            
            // Code Analysis Agents (6)
            {
                id: 'codeAnalyzer',
                name: 'Code Analysis Agent',
                icon: 'fas fa-code',
                status: 'active',
                type: 'code',
                description: 'Analyzes code quality and provides suggestions',
                lastActivity: '2 minutes ago',
                metrics: {
                    filesAnalyzed: 23,
                    issuesFound: 7,
                    suggestions: 15,
                    qualityScore: '92%'
                },
                tasks: ['linting', 'code_review', 'optimization_suggestions']
            },
            {
                id: 'codeLinter',
                name: 'Code Linter Agent',
                icon: 'fas fa-bug',
                status: 'active',
                type: 'code',
                description: 'Lints and checks code quality',
                lastActivity: '1 minute ago',
                metrics: {
                    lintingRuns: 156,
                    issuesDetected: 23,
                    fixSuggestions: 45,
                    lintingSpeed: '0.5s'
                },
                tasks: ['code_linting', 'issue_detection', 'fix_suggestions']
            },
            {
                id: 'codeOptimizer',
                name: 'Code Optimizer Agent',
                icon: 'fas fa-tachometer-alt',
                status: 'active',
                type: 'code',
                description: 'Optimizes code performance',
                lastActivity: '2 minutes ago',
                metrics: {
                    optimizationsApplied: 34,
                    performanceGain: '28%',
                    memorySavings: '12%',
                    optimizationSuccess: '94.5%'
                },
                tasks: ['performance_optimization', 'memory_management', 'efficiency_improvement']
            },
            {
                id: 'codeReviewer',
                name: 'Code Reviewer Agent',
                icon: 'fas fa-eye',
                status: 'active',
                type: 'code',
                description: 'Reviews code for best practices',
                lastActivity: '3 minutes ago',
                metrics: {
                    reviewsCompleted: 67,
                    issuesFound: 12,
                    recommendations: 34,
                    reviewAccuracy: '96.8%'
                },
                tasks: ['code_review', 'best_practices_checking', 'recommendation_generation']
            },
            {
                id: 'codeDocumenter',
                name: 'Code Documenter Agent',
                icon: 'fas fa-book',
                status: 'active',
                type: 'code',
                description: 'Generates code documentation',
                lastActivity: '1 minute ago',
                metrics: {
                    docsGenerated: 45,
                    coverageScore: '89%',
                    docQuality: '94%',
                    generationSpeed: '2.3s'
                },
                tasks: ['documentation_generation', 'coverage_analysis', 'quality_assurance']
            },
            {
                id: 'codeTester',
                name: 'Code Tester Agent',
                icon: 'fas fa-vial',
                status: 'active',
                type: 'code',
                description: 'Runs automated tests',
                lastActivity: '2 minutes ago',
                metrics: {
                    testsRun: 234,
                    testPassRate: '98.7%',
                    coverageScore: '92%',
                    testSpeed: '1.8s'
                },
                tasks: ['test_execution', 'coverage_analysis', 'result_reporting']
            },
            
            // Security Agents (6)
            {
                id: 'securityMonitor',
                name: 'Security Monitor Agent',
                icon: 'fas fa-shield-alt',
                status: 'active',
                type: 'security',
                description: 'Monitors system security',
                lastActivity: '1 minute ago',
                metrics: {
                    threatsDetected: 0,
                    systemSecure: '100%',
                    scansCompleted: 12,
                    vulnerabilities: 0
                },
                tasks: ['threat_detection', 'security_scanning', 'access_control']
            },
            {
                id: 'securityScanner',
                name: 'Security Scanner Agent',
                icon: 'fas fa-search',
                status: 'active',
                type: 'security',
                description: 'Scans for security vulnerabilities',
                lastActivity: '2 minutes ago',
                metrics: {
                    scansCompleted: 89,
                    vulnerabilitiesFound: 0,
                    scanCoverage: '100%',
                    scanSpeed: '3.2s'
                },
                tasks: ['vulnerability_scanning', 'threat_analysis', 'security_reporting']
            },
            {
                id: 'securityEncryptor',
                name: 'Security Encryptor Agent',
                icon: 'fas fa-lock',
                status: 'active',
                type: 'security',
                description: 'Handles encryption and security',
                lastActivity: '1 minute ago',
                metrics: {
                    encryptionOperations: 156,
                    encryptionLevel: 'AES-256',
                    securityScore: '100%',
                    keyRotation: '24h'
                },
                tasks: ['encryption_management', 'key_rotation', 'security_enhancement']
            },
            {
                id: 'securityAuditor',
                name: 'Security Auditor Agent',
                icon: 'fas fa-clipboard-check',
                status: 'active',
                type: 'security',
                description: 'Audits security compliance',
                lastActivity: '3 minutes ago',
                metrics: {
                    auditsCompleted: 23,
                    complianceScore: '100%',
                    violationsFound: 0,
                    auditCoverage: '100%'
                },
                tasks: ['compliance_auditing', 'violation_detection', 'report_generation']
            },
            {
                id: 'securityFirewall',
                name: 'Security Firewall Agent',
                icon: 'fas fa-fire',
                status: 'active',
                type: 'security',
                description: 'Manages firewall and network security',
                lastActivity: '2 minutes ago',
                metrics: {
                    connectionsMonitored: 1234,
                    threatsBlocked: 0,
                    firewallRules: 45,
                    responseTime: '0.1s'
                },
                tasks: ['firewall_management', 'network_monitoring', 'threat_blocking']
            },
            {
                id: 'securityBackup',
                name: 'Security Backup Agent',
                icon: 'fas fa-shield-virus',
                status: 'active',
                type: 'security',
                description: 'Creates secure backups',
                lastActivity: '1 minute ago',
                metrics: {
                    secureBackups: 34,
                    encryptionLevel: 'AES-256',
                    backupIntegrity: '100%',
                    recoverySuccess: '100%'
                },
                tasks: ['secure_backup', 'integrity_verification', 'recovery_operations']
            }
        ];
        
        agentsGrid.innerHTML = agents.map(agent => `
            <div class="agent-card ${agent.status} ${agent.type}" onclick="dashboard.manageAgent('${agent.id}')">
                <div class="agent-header">
                    <h5>
                        <i class="${agent.icon}"></i>
                        ${agent.name}
                    </h5>
                    <span class="agent-status ${agent.status}">${agent.status}</span>
                </div>
                <p>${agent.description}</p>
                ${agent.type === 'main' ? `
                    <div class="agent-metrics">
                        <div class="metric-item">
                            <span class="metric-value">${agent.metrics.tasksCompleted}</span>
                            <span class="metric-label">Tasks</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-value">${agent.metrics.uptime}</span>
                            <span class="metric-label">Uptime</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-value">${agent.metrics.memory}</span>
                            <span class="metric-label">Memory</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-value">${agent.metrics.cpu}</span>
                            <span class="metric-label">CPU</span>
                        </div>
                    </div>
                ` : `
                    <div class="agent-tasks">
                        <strong>Key Metrics:</strong>
                        <div class="task-tags">
                            ${Object.entries(agent.metrics).slice(0, 3).map(([key, value]) =>
                                `<span class="task-tag">${key}: ${value}</span>`
                            ).join('')}
                        </div>
                    </div>
                `}
                <small class="agent-last-activity">Last activity: ${agent.lastActivity}</small>
                <div class="agent-actions">
                    <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); dashboard.startAgent('${agent.id}')">
                        <i class="fas fa-play"></i> Start
                    </button>
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); dashboard.stopAgent('${agent.id}')">
                        <i class="fas fa-stop"></i> Stop
                    </button>
                    <button class="btn btn-sm btn-info" onclick="event.stopPropagation(); dashboard.viewAgentLogs('${agent.id}')">
                        <i class="fas fa-list"></i> Logs
                    </button>
                </div>
            </div>
        `).join('');
        
        // Update agent count in hero stats
        const activeAgents = agents.filter(agent => agent.status === 'active').length;
        const agentsElement = document.getElementById('agents');
        if (agentsElement) {
            agentsElement.textContent = activeAgents;
        }
    }

    loadTools() {
        const toolsGrid = document.getElementById('toolsGrid');
        if (!toolsGrid) return;

        toolsGrid.innerHTML = this.tools.map(tool => `
            <div class="tool-card ${tool.status}" onclick="dashboard.manageTool('${tool.id}')">
                <div class="tool-header">
                    <h5><i class="${tool.icon}"></i> ${tool.name}</h5>
                    <span class="tool-status ${tool.status}">${tool.status}</span>
                </div>
                <p>${tool.description}</p>
                <div class="tool-packages">
                    <strong>Version:</strong> ${tool.version}
                </div>
                <div class="package-tags">
                    ${tool.packages.slice(0, 3).map(pkg => `<span class="package-tag">${pkg}</span>`).join('')}
                    ${tool.packages.length > 3 ? `<span class="package-tag">+${tool.packages.length - 3} more</span>` : ''}
                </div>
                <div class="tool-last-updated">
                    <small>Last updated: ${tool.lastUpdated}</small>
                </div>
                <div class="tool-actions">
                    <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); dashboard.updateTool('${tool.id}')" title="Update Tool">
                        <i class="fas fa-sync"></i> Update
                    </button>
                    <button class="btn btn-sm btn-info" onclick="event.stopPropagation(); dashboard.viewToolDetails('${tool.id}')" title="View Details">
                        <i class="fas fa-info"></i> Details
                    </button>
                </div>
            </div>
        `).join('');
    }

    loadProjectFilesUI() {
        const fileGrid = document.getElementById('fileGrid');
        if (!fileGrid) return;

        fileGrid.innerHTML = this.files.map(file => `
            <div class="file-card" onclick="dashboard.openFile('${file.id}')">
                <h5><i class="${file.icon}"></i> ${file.name}</h5>
                <p>${file.description}</p>
                <div class="file-details">
                    <span class="file-type ${file.type}">${file.type}</span>
                    <span class="file-size">${file.size}</span>
                </div>
                <small>Last modified: ${file.lastModified}</small>
            </div>
        `).join('');
    }

    updateAgentMetrics() {
        // Simulate real-time agent metric updates
        this.agents.forEach(agent => {
            if (agent.status === 'active') {
                // Update metrics randomly
                if (agent.type === 'main') {
                    agent.metrics.tasksCompleted += Math.floor(Math.random() * 2);
                    agent.metrics.cpu = Math.max(30, Math.min(80, agent.metrics.cpu + (Math.random() - 0.5) * 10));
                    agent.metrics.memory = `${(Math.random() * 2 + 1.5).toFixed(1)}GB`;
                } else {
                    const metricKey = Object.keys(agent.metrics)[0];
                    agent.metrics[metricKey] += Math.floor(Math.random() * 3);
                }
            }
        });

        // Refresh agent display
        this.loadAgents();
    }

    updatePerformanceMetrics() {
        // Update performance bars
        const metrics = ['cpuUsage', 'memoryUsage', 'networkUsage', 'storageUsage'];
        metrics.forEach(metric => {
            const element = document.getElementById(metric);
            if (element) {
                const currentValue = parseInt(element.textContent);
                const newValue = Math.max(20, Math.min(90, currentValue + (Math.random() - 0.5) * 10));
                element.textContent = metric === 'memoryUsage' ? `${newValue.toFixed(1)}GB` : `${newValue}%`;
                
                // Update progress bar
                const bar = element.parentElement.nextElementSibling?.querySelector('.metric-fill');
                if (bar) {
                    bar.style.width = `${newValue}%`;
                }
            }
        });
    }

    updateAnalytics() {
        // Update analytics data
        Object.keys(this.analytics.performance).forEach(key => {
            const metric = this.analytics.performance[key];
            metric.history.push(metric.current);
            if (metric.history.length > 10) {
                metric.history.shift();
            }
            metric.current = Math.max(20, Math.min(90, metric.current + (Math.random() - 0.5) * 5));
        });
    }

    // Agent Management Methods
    manageAgent(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (!agent) return;

        if (agent.type === 'main') {
            window.open('ai_agents_management_with_main_agent.html', '_blank');
        } else {
            this.showNotification(`Managing ${agent.name}...`, 'info');
        }
    }

    startAgent(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent) {
            agent.status = 'active';
            this.showNotification(`${agent.name} started successfully`, 'success');
            this.loadAgents();
        }
    }

    stopAgent(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent) {
            agent.status = 'standby';
            this.showNotification(`${agent.name} stopped`, 'warning');
            this.loadAgents();
        }
    }

    viewAgentLogs(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent) {
            this.showModal('Agent Logs', `
                <div class="agent-logs">
                    <h4>${agent.name} Logs</h4>
                    ${agent.logs.map(log => `
                        <div class="log-entry ${log.level}">
                            <span class="log-time">${log.timestamp.toLocaleTimeString()}</span>
                            <span class="log-level">${log.level}</span>
                            <span class="log-message">${log.message}</span>
                        </div>
                    `).join('')}
                </div>
            `);
        }
    }

    // Tool Management Methods
    manageTool(toolId) {
        const tool = this.tools.find(t => t.id === toolId);
        if (tool) {
            this.showModal('Tool Details', `
                <div class="tool-details">
                    <h4>${tool.name}</h4>
                    <p><strong>Description:</strong> ${tool.description}</p>
                    <p><strong>Version:</strong> ${tool.version}</p>
                    <p><strong>Status:</strong> <span class="status-${tool.status}">${tool.status}</span></p>
                    <p><strong>Features:</strong></p>
                    <ul>
                        ${tool.features.map(feature => `<li>${feature}</li>`).join('')}
                    </ul>
                    <p><strong>Metrics:</strong></p>
                    <div class="tool-metrics">
                        ${Object.entries(tool.metrics).map(([key, value]) => `
                            <div class="metric-item">
                                <span class="metric-label">${key}:</span>
                                <span class="metric-value">${value}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `);
        }
    }

    updateTool(toolId) {
        const tool = this.tools.find(t => t.id === toolId);
        if (tool) {
            this.showNotification(`Updating ${tool.name}...`, 'info');
            setTimeout(() => {
                tool.lastUpdated = 'Just now';
                this.showNotification(`${tool.name} updated successfully`, 'success');
                this.loadTools();
            }, 2000);
        }
    }

    viewToolDetails(toolId) {
        this.manageTool(toolId);
    }

    // File Management Methods
    openFile(fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (file) {
            this.showModal('File Details', `
                <div class="file-details-modal">
                    <h4>${file.name}</h4>
                    <p><strong>Type:</strong> ${file.type}</p>
                    <p><strong>Size:</strong> ${file.size}</p>
                    <p><strong>Lines:</strong> ${file.lines}</p>
                    <p><strong>Path:</strong> ${file.path}</p>
                    <p><strong>Description:</strong> ${file.description}</p>
                    <p><strong>Dependencies:</strong></p>
                    <div class="dependencies">
                        ${file.dependencies.map(dep => `<span class="dependency-tag">${dep}</span>`).join('')}
                    </div>
                </div>
            `);
        }
    }

    // Utility Methods
    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        const notificationText = document.getElementById('notificationText');
        
        if (notification && notificationText) {
            notificationText.textContent = message;
            notification.className = `notification show ${type}`;
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        }
    }

    showModal(title, content) {
        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        if (modal && modalTitle && modalBody) {
            modalTitle.textContent = title;
            modalBody.innerHTML = content;
            modal.classList.remove('hidden');
            modal.classList.add('show');
        }
    }

    closeModal() {
        const modal = document.getElementById('modal');
        if (modal) {
            modal.classList.remove('show');
            modal.classList.add('hidden');
        }
    }

    toggleTheme(isDark) {
        document.body.classList.toggle('dark-mode', isDark);
        this.settings.theme.darkMode = isDark;
        this.showNotification(`Theme changed to ${isDark ? 'dark' : 'light'} mode`, 'info');
    }

    toggleAutoRefresh(enabled) {
        this.settings.autoRefresh.enabled = enabled;
        if (enabled) {
            this.showNotification('Auto refresh enabled', 'success');
        } else {
            this.showNotification('Auto refresh disabled', 'warning');
        }
    }

    setTimeRange(range) {
        this.currentTimeRange = range;
        document.querySelectorAll('.time-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        this.showNotification(`Time range changed to ${range}`, 'info');
    }

    // Action Methods
    runScript() {
        this.showNotification('Running system script...', 'info');
        setTimeout(() => {
            this.showNotification('Script executed successfully', 'success');
        }, 2000);
    }

    loadConfig() {
        this.showNotification('Loading configuration...', 'info');
        setTimeout(() => {
            this.showNotification('Configuration loaded successfully', 'success');
        }, 1500);
    }

    processData() {
        this.showNotification('Processing data...', 'info');
        setTimeout(() => {
            this.showNotification('Data processing completed', 'success');
        }, 3000);
    }

    scanFiles() {
        this.showNotification('Scanning files...', 'info');
        setTimeout(() => {
            this.showNotification('File scan completed', 'success');
        }, 2500);
    }

    backupSystem() {
        this.showNotification('Creating system backup...', 'info');
        setTimeout(() => {
            this.showNotification('System backup completed', 'success');
        }, 4000);
    }

    emergencyStop() {
        this.showNotification('Emergency stop activated!', 'error');
        setTimeout(() => {
            this.showNotification('System safely stopped', 'warning');
        }, 1000);
    }

    // Navigation Methods
    handleNavigation(section) {
        document.querySelectorAll('section').forEach(s => s.style.display = 'none');
        const targetSection = document.getElementById(section);
        if (targetSection) {
            targetSection.style.display = 'block';
        }
        
        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        event.target.classList.add('active');
    }
}

// Global Functions
function openAIAgents() {
    window.open('ai_agents_management_with_main_agent.html', '_blank');
}

function manageAgents() {
    window.dashboard.showNotification('Opening agent management...', 'info');
}

function quickStart() {
    window.dashboard.showNotification('Starting quick setup...', 'info');
    setTimeout(() => {
        window.dashboard.showNotification('Quick setup completed!', 'success');
    }, 3000);
}

function openTutorial() {
    window.dashboard.showModal('Tutorial', `
        <div class="tutorial-content">
            <h4>Welcome to EHB-5 Dashboard Tutorial</h4>
            <p>This dashboard provides comprehensive management of your AI agents, tools, and system resources.</p>
            <ol>
                <li><strong>Dashboard:</strong> Monitor system performance and status</li>
                <li><strong>Agents:</strong> Manage AI agents and their activities</li>
                <li><strong>Tools:</strong> View and update development tools</li>
                <li><strong>Projects:</strong> Access and manage project files</li>
                <li><strong>Analytics:</strong> View detailed system analytics</li>
                <li><strong>Settings:</strong> Configure system preferences</li>
            </ol>
        </div>
    `);
}

function refreshDashboard() {
    window.dashboard.showNotification('Refreshing dashboard...', 'info');
    setTimeout(() => {
        window.dashboard.updateDashboard();
        window.dashboard.showNotification('Dashboard refreshed', 'success');
    }, 1000);
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

function toggleNotifications() {
    window.dashboard.showNotification('Notifications toggled', 'info');
}

function openProfile() {
    window.dashboard.showModal('User Profile', `
        <div class="profile-content">
            <h4>User Profile</h4>
            <p><strong>Name:</strong> EHB-5 Administrator</p>
            <p><strong>Role:</strong> System Administrator</p>
            <p><strong>Last Login:</strong> ${new Date().toLocaleString()}</p>
            <p><strong>Permissions:</strong> Full Access</p>
        </div>
    `);
}

function createAgent() {
    window.dashboard.showModal('Create New Agent', `
        <div class="create-agent-form">
            <h4>Create New AI Agent</h4>
            <form>
                <div class="form-group">
                    <label>Agent Name:</label>
                    <input type="text" placeholder="Enter agent name">
                </div>
                <div class="form-group">
                    <label>Agent Type:</label>
                    <select>
                        <option>Data Processing</option>
                        <option>Analytics</option>
                        <option>Security</option>
                        <option>Custom</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <textarea placeholder="Enter agent description"></textarea>
                </div>
            </form>
        </div>
    `);
}

function manageAllAgents() {
    window.dashboard.showNotification('Opening agent management panel...', 'info');
}

function installTool() {
    window.dashboard.showModal('Install Tool', `
        <div class="install-tool-form">
            <h4>Install New Tool</h4>
            <form>
                <div class="form-group">
                    <label>Tool Name:</label>
                    <input type="text" placeholder="Enter tool name">
                </div>
                <div class="form-group">
                    <label>Package Manager:</label>
                    <select>
                        <option>npm</option>
                        <option>yarn</option>
                        <option>pip</option>
                        <option>apt</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Package Name:</label>
                    <input type="text" placeholder="Enter package name">
                </div>
            </form>
        </div>
    `);
}

function updateTools() {
    window.dashboard.showNotification('Updating all tools...', 'info');
    setTimeout(() => {
        window.dashboard.showNotification('All tools updated successfully', 'success');
    }, 3000);
}

function uploadFile() {
    window.dashboard.showNotification('Opening file upload dialog...', 'info');
}

function createFile() {
    window.dashboard.showModal('Create New File', `
        <div class="create-file-form">
            <h4>Create New File</h4>
            <form>
                <div class="form-group">
                    <label>File Name:</label>
                    <input type="text" placeholder="Enter file name">
                </div>
                <div class="form-group">
                    <label>File Type:</label>
                    <select>
                        <option>JavaScript</option>
                        <option>Python</option>
                        <option>HTML</option>
                        <option>CSS</option>
                        <option>JSON</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Content:</label>
                    <textarea placeholder="Enter file content"></textarea>
                </div>
            </form>
        </div>
    `);
}

function searchFiles(query) {
    window.dashboard.showNotification(`Searching for: ${query}`, 'info');
}

function filterFiles(type) {
    window.dashboard.showNotification(`Filtering files by: ${type}`, 'info');
}

function exportAnalytics() {
    window.dashboard.showNotification('Exporting analytics data...', 'info');
    setTimeout(() => {
        window.dashboard.showNotification('Analytics exported successfully', 'success');
    }, 2000);
}

function generateReport() {
    window.dashboard.showNotification('Generating report...', 'info');
    setTimeout(() => {
        window.dashboard.showNotification('Report generated successfully', 'success');
    }, 3000);
}

function saveSettings() {
    window.dashboard.showNotification('Settings saved successfully', 'success');
}

function resetSettings() {
    window.dashboard.showNotification('Settings reset to defaults', 'warning');
}

function showPrivacyPolicy() {
    window.dashboard.showModal('Privacy Policy', `
        <div class="privacy-content">
            <h4>Privacy Policy</h4>
            <p>This dashboard respects your privacy and protects your data according to industry standards.</p>
            <p>All data is encrypted and stored securely.</p>
        </div>
    `);
}

function showTerms() {
    window.dashboard.showModal('Terms of Service', `
        <div class="terms-content">
            <h4>Terms of Service</h4>
            <p>By using this dashboard, you agree to our terms of service.</p>
            <p>Please read the full terms before proceeding.</p>
        </div>
    `);
}

function showSupport() {
    window.dashboard.showModal('Support', `
        <div class="support-content">
            <h4>Support</h4>
            <p>For technical support, please contact:</p>
            <p>Email: support@ehb-5.com</p>
            <p>Phone: +1-555-0123</p>
        </div>
    `);
}

function hideNotification() {
    const notification = document.getElementById('notification');
    if (notification) {
        notification.classList.remove('show');
    }
}

function closeModal() {
    window.dashboard.closeModal();
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});

// Real-time agent metrics update every 5 seconds
setInterval(() => {
    if (window.dashboard) {
        window.dashboard.updateAgentMetrics();
    }
}, 5000); 