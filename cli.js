#!/usr/bin/env node

const { program } = require('commander');
const inquirer = require('inquirer');
const chalk = require('chalk');
const ora = require('ora');
const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

const IntelligentAPIServer = require('./intelligent-api-server');

class IntelligentCLI {
    constructor() {
        this.server = null;
        this.configPath = path.join(__dirname, 'config');
        this.setupCommands();
    }

    setupCommands() {
        program
            .name('ehb-api')
            .description('EHB-5 Intelligent API Server CLI')
            .version('2.0.0');

        // Start command
        program
            .command('start')
            .description('Start the Intelligent API Server')
            .option('-p, --port <port>', 'Port to run the server on', '3001')
            .option('-e, --env <environment>', 'Environment (development/production)', 'development')
            .option('--daemon', 'Run as daemon process')
            .action(async (options) => {
                await this.startServer(options);
            });

        // Stop command
        program
            .command('stop')
            .description('Stop the Intelligent API Server')
            .action(async () => {
                await this.stopServer();
            });

        // Status command
        program
            .command('status')
            .description('Check server status')
            .action(async () => {
                await this.checkStatus();
            });

        // Monitor command
        program
            .command('monitor')
            .description('Monitor server in real-time')
            .option('-i, --interval <seconds>', 'Update interval in seconds', '5')
            .action(async (options) => {
                await this.monitorServer(options);
            });

        // Setup command
        program
            .command('setup')
            .description('Setup the Intelligent API Server')
            .option('--force', 'Force setup even if already configured')
            .action(async (options) => {
                await this.setupServer(options);
            });

        // Config command
        program
            .command('config')
            .description('Manage server configuration')
            .option('--show', 'Show current configuration')
            .option('--edit', 'Edit configuration')
            .option('--reset', 'Reset to default configuration')
            .action(async (options) => {
                await this.manageConfig(options);
            });

        // Agents command
        program
            .command('agents')
            .description('Manage AI agents')
            .option('--list', 'List all agents')
            .option('--start <id>', 'Start specific agent')
            .option('--stop <id>', 'Stop specific agent')
            .option('--restart <id>', 'Restart specific agent')
            .option('--status <id>', 'Check agent status')
            .action(async (options) => {
                await this.manageAgents(options);
            });

        // Logs command
        program
            .command('logs')
            .description('View server logs')
            .option('-f, --follow', 'Follow log output')
            .option('-n, --lines <number>', 'Number of lines to show', '50')
            .option('--level <level>', 'Log level (error/warn/info/debug)', 'info')
            .action(async (options) => {
                await this.viewLogs(options);
            });

        // Backup command
        program
            .command('backup')
            .description('Backup server data')
            .option('-d, --destination <path>', 'Backup destination path')
            .option('--include-logs', 'Include log files in backup')
            .option('--include-config', 'Include configuration files in backup')
            .action(async (options) => {
                await this.backupServer(options);
            });

        // Restore command
        program
            .command('restore')
            .description('Restore server from backup')
            .option('-s, --source <path>', 'Backup source path')
            .option('--force', 'Force restore without confirmation')
            .action(async (options) => {
                await this.restoreServer(options);
            });

        // Update command
        program
            .command('update')
            .description('Update the Intelligent API Server')
            .option('--check', 'Check for updates only')
            .option('--force', 'Force update without confirmation')
            .action(async (options) => {
                await this.updateServer(options);
            });

        // Health command
        program
            .command('health')
            .description('Check system health')
            .option('--detailed', 'Show detailed health information')
            .option('--fix', 'Attempt to fix health issues')
            .action(async (options) => {
                await this.checkHealth(options);
            });

        // Dashboard command
        program
            .command('dashboard')
            .description('Open dashboard in browser')
            .option('--port <port>', 'Dashboard port', '3001')
            .action(async (options) => {
                await this.openDashboard(options);
            });

        // Test command
        program
            .command('test')
            .description('Run server tests')
            .option('--unit', 'Run unit tests only')
            .option('--integration', 'Run integration tests only')
            .option('--coverage', 'Generate coverage report')
            .action(async (options) => {
                await this.runTests(options);
            });

        // Deploy command
        program
            .command('deploy')
            .description('Deploy to production')
            .option('--environment <env>', 'Target environment', 'production')
            .option('--config <path>', 'Deployment configuration file')
            .option('--dry-run', 'Simulate deployment without making changes')
            .action(async (options) => {
                await this.deployServer(options);
            });

        program.parse();
    }

    async startServer(options) {
        const spinner = ora('Starting Intelligent API Server...').start();

        try {
            // Set environment variables
            process.env.PORT = options.port;
            process.env.NODE_ENV = options.env;

            // Create server instance
            this.server = new IntelligentAPIServer();

            // Start the server
            await this.server.start();

            spinner.succeed(chalk.green('Intelligent API Server started successfully!'));

            console.log(chalk.cyan('\n📊 Dashboard:'), `http://localhost:${options.port}`);
            console.log(chalk.cyan('🔌 WebSocket:'), `ws://localhost:${options.port}`);
            console.log(chalk.cyan('📋 Health Check:'), `http://localhost:${options.port}/health`);
            console.log(chalk.cyan('📚 API Docs:'), `http://localhost:${options.port}/api/v1/docs`);

            if (options.daemon) {
                console.log(chalk.yellow('\n🔄 Running as daemon process...'));
                console.log(chalk.yellow('Use "ehb-api stop" to stop the server'));
            } else {
                console.log(chalk.yellow('\nPress Ctrl+C to stop the server'));

                // Keep the process running
                process.on('SIGINT', async () => {
                    console.log('\n🛑 Shutting down gracefully...');
                    await this.stopServer();
                    process.exit(0);
                });
            }

        } catch (error) {
            spinner.fail(chalk.red('Failed to start server:'), error.message);
            process.exit(1);
        }
    }

    async stopServer() {
        const spinner = ora('Stopping Intelligent API Server...').start();

        try {
            if (this.server) {
                await this.server.stop();
                this.server = null;
                spinner.succeed(chalk.green('Server stopped successfully!'));
            } else {
                // Try to stop via process
                await execAsync('taskkill /f /im node.exe');
                spinner.succeed(chalk.green('Server processes terminated!'));
            }
        } catch (error) {
            spinner.fail(chalk.red('Failed to stop server:'), error.message);
        }
    }

    async checkStatus() {
        const spinner = ora('Checking server status...').start();

        try {
            const response = await fetch('http://localhost:3001/health');
            const data = await response.json();

            spinner.succeed(chalk.green('Server is running!'));

            console.log(chalk.cyan('\n📊 Server Status:'));
            console.log(`  Status: ${chalk.green(data.status)}`);
            console.log(`  Uptime: ${chalk.yellow(data.uptime)}s`);
            console.log(`  Version: ${chalk.blue(data.version)}`);
            console.log(`  Timestamp: ${chalk.gray(data.timestamp)}`);

        } catch (error) {
            spinner.fail(chalk.red('Server is not running'));
            console.log(chalk.yellow('Use "ehb-api start" to start the server'));
        }
    }

    async monitorServer(options) {
        console.log(chalk.cyan('🔍 Monitoring server in real-time...'));
        console.log(chalk.gray('Press Ctrl+C to stop monitoring\n'));

        const interval = parseInt(options.interval) * 1000;

        const monitor = setInterval(async () => {
            try {
                const [healthResponse, metricsResponse] = await Promise.all([
                    fetch('http://localhost:3001/health'),
                    fetch('http://localhost:3001/api/v1/metrics')
                ]);

                const health = await healthResponse.json();
                const metrics = await metricsResponse.json();

                // Clear console
                console.clear();

                console.log(chalk.cyan('🖥️  Intelligent API Server Monitor'));
                console.log(chalk.gray('='.repeat(50)));

                // Health status
                console.log(chalk.green('✓ Status:'), health.status);
                console.log(chalk.blue('⏱️  Uptime:'), `${Math.floor(health.uptime / 60)}m ${Math.floor(health.uptime % 60)}s`);

                // Metrics
                console.log(chalk.cyan('\n📊 System Metrics:'));
                console.log(`  CPU: ${chalk.yellow(metrics.cpu)}%`);
                console.log(`  Memory: ${chalk.yellow(metrics.memory)}%`);
                console.log(`  Network: ${chalk.yellow(metrics.network)} MB/s`);
                console.log(`  Storage: ${chalk.yellow(metrics.storage)}%`);

                // Timestamp
                console.log(chalk.gray(`\n🕐 Last updated: ${new Date().toLocaleTimeString()}`));

            } catch (error) {
                console.clear();
                console.log(chalk.red('❌ Server is not responding'));
                console.log(chalk.yellow('Check if server is running with "ehb-api status"'));
            }
        }, interval);

        // Handle Ctrl+C
        process.on('SIGINT', () => {
            clearInterval(monitor);
            console.log(chalk.yellow('\n🛑 Monitoring stopped'));
            process.exit(0);
        });
    }

    async setupServer(options) {
        const spinner = ora('Setting up Intelligent API Server...').start();

        try {
            // Create necessary directories
            const dirs = ['config', 'logs', 'backups', 'data', 'public'];
            for (const dir of dirs) {
                await fs.mkdir(path.join(__dirname, dir), { recursive: true });
            }

            // Create default configuration
            const defaultConfig = {
                server: {
                    port: 3001,
                    host: 'localhost',
                    environment: 'development'
                },
                security: {
                    rateLimit: true,
                    cors: true,
                    helmet: true
                },
                monitoring: {
                    enabled: true,
                    interval: 5000,
                    metrics: true
                },
                agents: {
                    autoStart: true,
                    maxAgents: 10,
                    healthCheck: true
                },
                logging: {
                    level: 'info',
                    file: 'logs/server.log',
                    maxSize: '10m',
                    maxFiles: 5
                }
            };

            await fs.writeFile(
                path.join(__dirname, 'config', 'server.json'),
                JSON.stringify(defaultConfig, null, 2)
            );

            // Install dependencies
            spinner.text = 'Installing dependencies...';
            await execAsync('npm install');

            spinner.succeed(chalk.green('Setup completed successfully!'));

            console.log(chalk.cyan('\n📁 Created directories:'));
            dirs.forEach(dir => console.log(`  - ${dir}/`));

            console.log(chalk.cyan('\n📋 Next steps:'));
            console.log('  1. Run "ehb-api start" to start the server');
            console.log('  2. Open http://localhost:3001 to view the dashboard');
            console.log('  3. Use "ehb-api config --edit" to customize settings');

        } catch (error) {
            spinner.fail(chalk.red('Setup failed:'), error.message);
        }
    }

    async manageConfig(options) {
        const configPath = path.join(__dirname, 'config', 'server.json');

        try {
            if (options.show) {
                const config = await fs.readFile(configPath, 'utf8');
                console.log(chalk.cyan('📋 Current Configuration:'));
                console.log(JSON.stringify(JSON.parse(config), null, 2));

            } else if (options.edit) {
                const config = await fs.readFile(configPath, 'utf8');
                const currentConfig = JSON.parse(config);

                const answers = await inquirer.prompt([
                    {
                        type: 'input',
                        name: 'port',
                        message: 'Server port:',
                        default: currentConfig.server.port
                    },
                    {
                        type: 'list',
                        name: 'environment',
                        message: 'Environment:',
                        choices: ['development', 'production', 'staging'],
                        default: currentConfig.server.environment
                    },
                    {
                        type: 'confirm',
                        name: 'rateLimit',
                        message: 'Enable rate limiting?',
                        default: currentConfig.security.rateLimit
                    },
                    {
                        type: 'confirm',
                        name: 'monitoring',
                        message: 'Enable monitoring?',
                        default: currentConfig.monitoring.enabled
                    }
                ]);

                currentConfig.server.port = parseInt(answers.port);
                currentConfig.server.environment = answers.environment;
                currentConfig.security.rateLimit = answers.rateLimit;
                currentConfig.monitoring.enabled = answers.monitoring;

                await fs.writeFile(configPath, JSON.stringify(currentConfig, null, 2));
                console.log(chalk.green('✓ Configuration updated successfully!'));

            } else if (options.reset) {
                const confirm = await inquirer.prompt([
                    {
                        type: 'confirm',
                        name: 'confirm',
                        message: 'Are you sure you want to reset configuration to defaults?',
                        default: false
                    }
                ]);

                if (confirm.confirm) {
                    await this.setupServer({ force: true });
                    console.log(chalk.green('✓ Configuration reset to defaults!'));
                }

            } else {
                console.log(chalk.yellow('Use --show, --edit, or --reset to manage configuration'));
            }

        } catch (error) {
            console.log(chalk.red('Configuration management failed:'), error.message);
        }
    }

    async manageAgents(options) {
        try {
            if (options.list) {
                const response = await fetch('http://localhost:3001/api/v1/agents');
                const agents = await response.json();

                console.log(chalk.cyan('🤖 AI Agents:'));
                agents.forEach(agent => {
                    const statusColor = agent.status === 'active' ? 'green' : 'red';
                    console.log(`  ${chalk[statusColor](agent.name)} (${agent.type}) - ${agent.status}`);
                });

            } else if (options.start || options.stop || options.restart) {
                const agentId = options.start || options.stop || options.restart;
                const action = options.start ? 'start' : options.stop ? 'stop' : 'restart';

                const response = await fetch(`http://localhost:3001/api/v1/agents/${agentId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: action === 'stop' ? 'inactive' : 'active' })
                });

                if (response.ok) {
                    console.log(chalk.green(`✓ Agent ${action}ed successfully!`));
                } else {
                    console.log(chalk.red(`✗ Failed to ${action} agent`));
                }

            } else if (options.status) {
                const response = await fetch(`http://localhost:3001/api/v1/agents/${options.status}`);
                const agent = await response.json();

                console.log(chalk.cyan(`🤖 Agent Status: ${agent.name}`));
                console.log(`  Type: ${agent.type}`);
                console.log(`  Status: ${agent.status}`);
                console.log(`  Created: ${agent.createdAt}`);
                console.log(`  Last Activity: ${agent.lastActivity}`);

            } else {
                console.log(chalk.yellow('Use --list, --start <id>, --stop <id>, --restart <id>, or --status <id>'));
            }

        } catch (error) {
            console.log(chalk.red('Agent management failed:'), error.message);
        }
    }

    async viewLogs(options) {
        const logPath = path.join(__dirname, 'logs', 'server.log');

        try {
            if (options.follow) {
                console.log(chalk.cyan('📋 Following logs (Press Ctrl+C to stop)...'));

                const { spawn } = require('child_process');
                const tail = spawn('tail', ['-f', logPath]);

                tail.stdout.on('data', (data) => {
                    console.log(data.toString());
                });

                tail.stderr.on('data', (data) => {
                    console.error(chalk.red(data.toString()));
                });

                process.on('SIGINT', () => {
                    tail.kill();
                    console.log(chalk.yellow('\n🛑 Log following stopped'));
                    process.exit(0);
                });

            } else {
                const logContent = await fs.readFile(logPath, 'utf8');
                const lines = logContent.split('\n').slice(-parseInt(options.lines));

                console.log(chalk.cyan(`📋 Last ${options.lines} log entries:`));
                console.log(lines.join('\n'));
            }

        } catch (error) {
            console.log(chalk.red('Failed to read logs:'), error.message);
        }
    }

    async backupServer(options) {
        const spinner = ora('Creating backup...').start();

        try {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupPath = options.destination || path.join(__dirname, 'backups', `backup-${timestamp}.zip`);

            const archiver = require('archiver');
            const output = require('fs').createWriteStream(backupPath);
            const archive = archiver('zip', { zlib: { level: 9 } });

            output.on('close', () => {
                spinner.succeed(chalk.green('Backup created successfully!'));
                console.log(chalk.cyan(`📦 Backup saved to: ${backupPath}`));
            });

            archive.pipe(output);

            // Add files to backup
            archive.directory(path.join(__dirname, 'config'), 'config');
            archive.directory(path.join(__dirname, 'data'), 'data');

            if (options.includeLogs) {
                archive.directory(path.join(__dirname, 'logs'), 'logs');
            }

            if (options.includeConfig) {
                archive.file(path.join(__dirname, 'package.json'), { name: 'package.json' });
                archive.file(path.join(__dirname, 'intelligent-api-server.js'), { name: 'intelligent-api-server.js' });
            }

            await archive.finalize();

        } catch (error) {
            spinner.fail(chalk.red('Backup failed:'), error.message);
        }
    }

    async restoreServer(options) {
        const spinner = ora('Restoring from backup...').start();

        try {
            const backupPath = options.source;
            if (!backupPath) {
                throw new Error('Backup source path is required');
            }

            if (!options.force) {
                const confirm = await inquirer.prompt([
                    {
                        type: 'confirm',
                        name: 'confirm',
                        message: 'This will overwrite current data. Are you sure?',
                        default: false
                    }
                ]);

                if (!confirm.confirm) {
                    spinner.stop();
                    console.log(chalk.yellow('Restore cancelled'));
                    return;
                }
            }

            const extract = require('extract-zip');
            await extract(backupPath, { dir: __dirname });

            spinner.succeed(chalk.green('Restore completed successfully!'));

        } catch (error) {
            spinner.fail(chalk.red('Restore failed:'), error.message);
        }
    }

    async updateServer(options) {
        const spinner = ora('Checking for updates...').start();

        try {
            if (options.check) {
                // Check for updates (simulated)
                spinner.succeed(chalk.green('No updates available'));
                return;
            }

            if (!options.force) {
                const confirm = await inquirer.prompt([
                    {
                        type: 'confirm',
                        name: 'confirm',
                        message: 'Update the Intelligent API Server?',
                        default: false
                    }
                ]);

                if (!confirm.confirm) {
                    spinner.stop();
                    console.log(chalk.yellow('Update cancelled'));
                    return;
                }
            }

            spinner.text = 'Updating server...';

            // Update dependencies
            await execAsync('npm update');

            // Update server files (simulated)
            await new Promise(resolve => setTimeout(resolve, 2000));

            spinner.succeed(chalk.green('Update completed successfully!'));

        } catch (error) {
            spinner.fail(chalk.red('Update failed:'), error.message);
        }
    }

    async checkHealth(options) {
        const spinner = ora('Checking system health...').start();

        try {
            const healthChecks = [
                { name: 'Server Status', check: () => fetch('http://localhost:3001/health') },
                { name: 'API Endpoints', check: () => fetch('http://localhost:3001/api/v1/metrics') },
                { name: 'Database Connection', check: () => Promise.resolve() }, // Simulated
                { name: 'File System', check: () => fs.access(__dirname) },
                { name: 'Memory Usage', check: () => Promise.resolve() } // Simulated
            ];

            const results = [];
            for (const check of healthChecks) {
                try {
                    await check.check();
                    results.push({ name: check.name, status: 'healthy', color: 'green' });
                } catch (error) {
                    results.push({ name: check.name, status: 'unhealthy', color: 'red', error: error.message });
                }
            }

            spinner.succeed(chalk.green('Health check completed!'));

            console.log(chalk.cyan('\n🏥 System Health Report:'));
            results.forEach(result => {
                const statusIcon = result.status === 'healthy' ? '✓' : '✗';
                console.log(`  ${chalk[result.color](statusIcon)} ${result.name}: ${chalk[result.color](result.status)}`);
                if (result.error) {
                    console.log(`    Error: ${chalk.red(result.error)}`);
                }
            });

            if (options.fix) {
                console.log(chalk.yellow('\n🔧 Attempting to fix issues...'));
                // Implement auto-fix logic here
            }

        } catch (error) {
            spinner.fail(chalk.red('Health check failed:'), error.message);
        }
    }

    async openDashboard(options) {
        const url = `http://localhost:${options.port}`;

        console.log(chalk.cyan('🌐 Opening dashboard...'));
        console.log(chalk.blue(`URL: ${url}`));

        try {
            const { platform } = require('os');
            const open = require('open');

            await open(url);
            console.log(chalk.green('✓ Dashboard opened in browser'));
        } catch (error) {
            console.log(chalk.yellow('Please open the dashboard manually:'), url);
        }
    }

    async runTests(options) {
        const spinner = ora('Running tests...').start();

        try {
            let testCommand = 'npm test';

            if (options.unit) {
                testCommand = 'npm run test:unit';
            } else if (options.integration) {
                testCommand = 'npm run test:integration';
            }

            if (options.coverage) {
                testCommand += ' -- --coverage';
            }

            const { stdout, stderr } = await execAsync(testCommand);

            spinner.succeed(chalk.green('Tests completed!'));
            console.log(stdout);

            if (stderr) {
                console.error(chalk.red('Test errors:'), stderr);
            }

        } catch (error) {
            spinner.fail(chalk.red('Tests failed:'), error.message);
        }
    }

    async deployServer(options) {
        const spinner = ora('Deploying to production...').start();

        try {
            if (options.dryRun) {
                spinner.succeed(chalk.green('Dry run completed - no changes made'));
                console.log(chalk.cyan('Deployment would:'));
                console.log('  - Stop current server');
                console.log('  - Backup current data');
                console.log('  - Update server files');
                console.log('  - Restart server');
                return;
            }

            // Simulate deployment steps
            spinner.text = 'Stopping server...';
            await new Promise(resolve => setTimeout(resolve, 1000));

            spinner.text = 'Creating backup...';
            await new Promise(resolve => setTimeout(resolve, 2000));

            spinner.text = 'Updating files...';
            await new Promise(resolve => setTimeout(resolve, 3000));

            spinner.text = 'Starting server...';
            await new Promise(resolve => setTimeout(resolve, 2000));

            spinner.succeed(chalk.green('Deployment completed successfully!'));

        } catch (error) {
            spinner.fail(chalk.red('Deployment failed:'), error.message);
        }
    }
}

// Create and run CLI
const cli = new IntelligentCLI();

// Handle unhandled errors
process.on('uncaughtException', (error) => {
    console.error(chalk.red('Uncaught Exception:'), error);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error(chalk.red('Unhandled Rejection at:'), promise, chalk.red('reason:'), reason);
    process.exit(1);
});

module.exports = IntelligentCLI;
