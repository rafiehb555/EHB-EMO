#!/usr/bin/env node

const EHBOrchestrator = require('./agents/ai-orchestrator');
const CursorIntegration = require('./agents/cursor-integration');
const CursorAgentIntegration = require('./agents/cursor-agent-integration');
const MainEHBAgent = require('./agents/main-ehb-agent');
const winston = require('winston');
const chalk = require('chalk').default;

class EHBAISystem {
    constructor() {
        this.orchestrator = null;
        this.cursorIntegration = null;
        this.cursorAgentIntegration = null;
        this.mainAgent = null;
        this.setupLogging();
    }

    setupLogging() {
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            ),
            transports: [
                new winston.transports.File({ filename: 'logs/ehb-ai-system.log' }),
                new winston.transports.Console({
                    format: winston.format.simple()
                })
            ]
        });
    }

    async initialize() {
        this.logger.info('🚀 Starting EHB AI System...');
        console.log(chalk.blue('\n🎯 EHB AI Development System'));
        console.log(chalk.blue('================================\n'));

        try {
            // Initialize the AI Orchestrator
            this.logger.info('🧠 Initializing AI Orchestrator...');
            this.orchestrator = new EHBOrchestrator();
            
            // Wait for agents to be ready
            await new Promise((resolve) => {
                this.orchestrator.on('agents-ready', () => {
                    this.logger.info('✅ All AI Agents are ready');
                    resolve();
                });
            });

            // Initialize Cursor Integration
            this.logger.info('💻 Initializing Cursor Integration...');
            this.cursorIntegration = new CursorIntegration();
            await this.cursorIntegration.initialize(this.orchestrator);

            // Wait for Cursor to be ready
            await new Promise((resolve) => {
                this.cursorIntegration.on('cursor-ready', () => {
                    this.logger.info('✅ Cursor Integration is ready');
                    resolve();
                });
            });

            // Initialize Main EHB Agent
            this.logger.info('🏥 Initializing Main EHB Agent...');
            this.mainAgent = new MainEHBAgent();
            await this.mainAgent.initialize();

            // Wait for Main EHB Agent to be ready
            await new Promise((resolve) => {
                this.mainAgent.on('main-agent-ready', () => {
                    this.logger.info('✅ Main EHB Agent is ready');
                    resolve();
                });
            });

            // Initialize Cursor Agent Integration
            this.logger.info('🤖 Initializing Cursor Agent Integration...');
            this.cursorAgentIntegration = new CursorAgentIntegration();
            await this.cursorAgentIntegration.initialize(this.orchestrator, this.mainAgent);

            // Wait for Cursor Agent Integration to be ready
            await new Promise((resolve) => {
                this.cursorAgentIntegration.on('cursor-agents-ready', () => {
                    this.logger.info('✅ Cursor Agent Integration is ready');
                    resolve();
                });
            });

            this.logger.info('🎉 EHB AI System initialized successfully!');
            this.displaySystemStatus();

        } catch (error) {
            this.logger.error('❌ EHB AI System initialization failed:', error);
            console.error(chalk.red('❌ System initialization failed:', error.message));
            process.exit(1);
        }
    }

    displaySystemStatus() {
        console.log(chalk.green('\n✅ EHB AI System is Online!'));
        console.log(chalk.cyan('\n📊 System Status:'));
        console.log(chalk.cyan('├── 🧠 AI Orchestrator: Ready'));
        console.log(chalk.cyan('├── 🤖 GPT-4 Agent: Active'));
        console.log(chalk.cyan('├── 🔍 Gemini Agent: Active'));
        console.log(chalk.cyan('├── 🎤 Whisper Agent: Active'));
        console.log(chalk.cyan('├── 🎨 Midjourney Agent: Active'));
        console.log(chalk.cyan('├── 💻 Cursor Integration: Connected'));
        console.log(chalk.cyan('├── 🤝 Cursor Agent Integration: Active'));
        console.log(chalk.cyan('└── 🏥 Main EHB Agent: Active'));
        
        console.log(chalk.yellow('\n🌐 Available Services:'));
        console.log(chalk.yellow('├── Frontend: http://localhost:3000'));
        console.log(chalk.yellow('├── Backend: http://localhost:5000'));
        console.log(chalk.yellow('├── Health Check: http://localhost:5000/health'));
        console.log(chalk.yellow('└── Agent Status: http://localhost:5000/api/agents'));
        
        console.log(chalk.magenta('\n🎯 Ready for Development!'));
        console.log(chalk.magenta('Use Cursor IDE with AI agents for seamless development.'));
        
        this.displayUsageExamples();
    }

    displayUsageExamples() {
        console.log(chalk.blue('\n📝 Usage Examples:'));
        console.log(chalk.blue('1. Code Generation:'));
        console.log(chalk.gray('   - Ask Cursor to generate React components'));
        console.log(chalk.gray('   - Request API endpoints with authentication'));
        console.log(chalk.gray('   - Create healthcare-specific features'));
        
        console.log(chalk.blue('\n2. Design Requests:'));
        console.log(chalk.gray('   - Generate UI/UX designs for healthcare apps'));
        console.log(chalk.gray('   - Create medical dashboard layouts'));
        console.log(chalk.gray('   - Design patient management interfaces'));
        
        console.log(chalk.blue('\n3. Voice Processing:'));
        console.log(chalk.gray('   - Transcribe patient voice complaints'));
        console.log(chalk.gray('   - Process medical dictations'));
        console.log(chalk.gray('   - Analyze voice sentiment'));
        
        console.log(chalk.blue('\n4. Research & Analysis:'));
        console.log(chalk.gray('   - Research healthcare regulations'));
        console.log(chalk.gray('   - Analyze medical data trends'));
        console.log(chalk.gray('   - Review clinical guidelines'));
    }

    async runHealthCheck() {
        console.log(chalk.blue('\n🏥 Running System Health Check...'));
        
        try {
            const orchestratorHealth = await this.orchestrator.healthCheck();
            const cursorHealth = await this.cursorIntegration.healthCheck();
            
            console.log(chalk.green('\n✅ Health Check Results:'));
            console.log(chalk.green(`├── Orchestrator: ${orchestratorHealth.status}`));
            console.log(chalk.green(`└── Cursor Integration: ${cursorHealth.status}`));
            
            if (orchestratorHealth.status === 'healthy' && cursorHealth.status === 'healthy') {
                console.log(chalk.green('\n🎉 All systems are healthy!'));
            } else {
                console.log(chalk.yellow('\n⚠️ Some systems need attention'));
            }
            
        } catch (error) {
            console.error(chalk.red('\n❌ Health check failed:', error.message));
        }
    }

    async runDemo() {
        console.log(chalk.blue('\n🎬 Running EHB AI System Demo...'));
        
        try {
            // Demo 1: Code Generation
            console.log(chalk.cyan('\n1. 🧠 Code Generation Demo'));
            const codeTask = {
                type: 'code-generation',
                language: 'typescript',
                requirements: 'Create a React component for patient data display with HIPAA compliance',
                context: 'Healthcare application frontend'
            };
            
            const codeResult = await this.orchestrator.processTask(codeTask);
            console.log(chalk.green('✅ Code generation completed'));
            
            // Demo 2: Design Generation
            console.log(chalk.cyan('\n2. 🎨 Design Generation Demo'));
            const designTask = {
                type: 'design-request',
                requirements: 'Create a modern healthcare dashboard with patient monitoring widgets',
                style: 'medical',
                context: 'Healthcare dashboard UI'
            };
            
            const designResult = await this.orchestrator.processTask(designTask);
            console.log(chalk.green('✅ Design generation completed'));
            
            // Demo 3: Research Analysis
            console.log(chalk.cyan('\n3. 🔍 Research Analysis Demo'));
            const researchTask = {
                type: 'research-analysis',
                query: 'Latest HIPAA compliance requirements for healthcare applications',
                sources: ['official', 'medical'],
                depth: 'comprehensive'
            };
            
            const researchResult = await this.orchestrator.processTask(researchTask);
            console.log(chalk.green('✅ Research analysis completed'));
            
            console.log(chalk.green('\n🎉 All demos completed successfully!'));
            
        } catch (error) {
            console.error(chalk.red('\n❌ Demo failed:', error.message));
        }
    }

    async startInteractiveMode() {
        console.log(chalk.blue('\n🎮 Starting Interactive Mode...'));
        console.log(chalk.gray('Type "help" for available commands, "exit" to quit'));
        
        const readline = require('readline');
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        const askQuestion = (question) => {
            return new Promise((resolve) => {
                rl.question(question, resolve);
            });
        };

        while (true) {
            try {
                const input = await askQuestion(chalk.cyan('\n🤖 EHB AI > '));
                const command = input.trim().toLowerCase();

                switch (command) {
                    case 'help':
                        this.displayHelp();
                        break;
                    case 'status':
                        await this.runHealthCheck();
                        break;
                    case 'demo':
                        await this.runDemo();
                        break;
                    case 'agents':
                        this.displayAgentStatus();
                        break;
                    case 'exit':
                    case 'quit':
                        console.log(chalk.yellow('\n👋 Shutting down EHB AI System...'));
                        rl.close();
                        process.exit(0);
                        break;
                    default:
                        if (command) {
                            console.log(chalk.gray('Type "help" for available commands'));
                        }
                }
            } catch (error) {
                console.error(chalk.red('Error:', error.message));
            }
        }
    }

    displayHelp() {
        console.log(chalk.blue('\n📚 Available Commands:'));
        console.log(chalk.blue('├── help     - Show this help message'));
        console.log(chalk.blue('├── status   - Run system health check'));
        console.log(chalk.blue('├── demo     - Run system demonstration'));
        console.log(chalk.blue('├── agents   - Show agent status'));
        console.log(chalk.blue('└── exit     - Exit the system'));
    }

    displayAgentStatus() {
        const status = this.orchestrator.getAgentStatus();
        console.log(chalk.blue('\n🤖 Agent Status:'));
        
        for (const [name, agentStatus] of Object.entries(status)) {
            const statusColor = agentStatus.initialized ? chalk.green : chalk.red;
            const statusText = agentStatus.initialized ? '✅ Active' : '❌ Inactive';
            console.log(chalk.blue(`├── ${name}: ${statusColor(statusText)}`));
        }
    }

    async start() {
        await this.initialize();
        
        // Start interactive mode
        await this.startInteractiveMode();
    }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log(chalk.yellow('\n👋 Shutting down EHB AI System...'));
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log(chalk.yellow('\n👋 Shutting down EHB AI System...'));
    process.exit(0);
});

// Start the system
if (require.main === module) {
    const system = new EHBAISystem();
    system.start().catch(error => {
        console.error(chalk.red('❌ Failed to start EHB AI System:', error.message));
        process.exit(1);
    });
}

module.exports = EHBAISystem; 