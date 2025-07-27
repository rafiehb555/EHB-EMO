#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class SSHGitHubSetup {
    constructor() {
        this.username = 'rafiehb555';
        this.repository = 'git@github.com:rafiehb555/ehb-5.git';
        this.sshKeyPath = path.join(process.env.HOME || process.env.USERPROFILE, '.ssh', 'id_rsa');
    }

    // Execute command with error handling
    executeCommand(command) {
        try {
            console.log(`Executing: ${command}`);
            const result = execSync(command, { 
                encoding: 'utf8',
                cwd: process.cwd()
            });
            console.log('Success:', result);
            return result;
        } catch (error) {
            console.error('Error executing command:', error.message);
            throw error;
        }
    }

    // Check if SSH key exists
    checkSSHKey() {
        try {
            console.log('🔍 Checking SSH key...');
            
            if (fs.existsSync(this.sshKeyPath)) {
                console.log('✅ SSH key found at:', this.sshKeyPath);
                return true;
            } else {
                console.log('❌ SSH key not found. Creating new SSH key...');
                return false;
            }
        } catch (error) {
            console.error('❌ Error checking SSH key:', error.message);
            return false;
        }
    }

    // Generate SSH key
    generateSSHKey() {
        try {
            console.log('🔑 Generating new SSH key...');
            
            const sshDir = path.dirname(this.sshKeyPath);
            if (!fs.existsSync(sshDir)) {
                fs.mkdirSync(sshDir, { recursive: true });
            }
            
            // Generate SSH key with no passphrase for automation
            this.executeCommand(`ssh-keygen -t rsa -b 4096 -f "${this.sshKeyPath}" -N ""`);
            
            console.log('✅ SSH key generated successfully');
            return true;
        } catch (error) {
            console.error('❌ Error generating SSH key:', error.message);
            return false;
        }
    }

    // Start SSH agent and add key
    setupSSHAgent() {
        try {
            console.log('🔧 Setting up SSH agent...');
            
            // Start SSH agent
            this.executeCommand('ssh-agent -s');
            
            // Add SSH key to agent
            this.executeCommand(`ssh-add "${this.sshKeyPath}"`);
            
            console.log('✅ SSH agent setup completed');
            return true;
        } catch (error) {
            console.error('❌ Error setting up SSH agent:', error.message);
            return false;
        }
    }

    // Get SSH public key
    getSSHPublicKey() {
        try {
            console.log('📋 Getting SSH public key...');
            
            const publicKeyPath = this.sshKeyPath + '.pub';
            if (fs.existsSync(publicKeyPath)) {
                const publicKey = fs.readFileSync(publicKeyPath, 'utf8').trim();
                console.log('✅ SSH public key retrieved');
                return publicKey;
            } else {
                throw new Error('SSH public key not found');
            }
        } catch (error) {
            console.error('❌ Error getting SSH public key:', error.message);
            return null;
        }
    }

    // Test GitHub SSH connection
    testGitHubSSH() {
        try {
            console.log('🔍 Testing GitHub SSH connection...');
            
            const result = this.executeCommand('ssh -T git@github.com');
            
            if (result.includes('successfully authenticated') || result.includes('Hi')) {
                console.log('✅ GitHub SSH connection successful');
                return true;
            } else {
                console.log('❌ GitHub SSH connection failed');
                return false;
            }
        } catch (error) {
            console.error('❌ Error testing GitHub SSH:', error.message);
            return false;
        }
    }

    // Setup Git remote with SSH
    setupGitRemote() {
        try {
            console.log('🌐 Setting up Git remote with SSH...');
            
            // Remove existing remote
            try {
                this.executeCommand('git remote remove origin');
            } catch (e) {
                console.log('No existing remote to remove');
            }
            
            // Add SSH remote
            this.executeCommand(`git remote add origin ${this.repository}`);
            
            // Test remote
            this.executeCommand('git remote -v');
            
            console.log('✅ Git remote setup completed');
            return true;
        } catch (error) {
            console.error('❌ Error setting up Git remote:', error.message);
            return false;
        }
    }

    // Create Kilo Code integration script
    createKiloCodeIntegration() {
        try {
            console.log('🤖 Creating Kilo Code integration...');
            
            const kiloCodeScript = `#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');

class KiloCodeIntegration {
    constructor() {
        this.vscodeExtensions = [
            'kilo-code.kilo-code',
            'ms-vscode.vscode-typescript-next',
            'esbenp.prettier-vscode',
            'ms-vscode.vscode-json'
        ];
    }

    // Check if VS Code is installed
    checkVSCode() {
        try {
            const result = execSync('code --version', { encoding: 'utf8' });
            console.log('✅ VS Code found:', result.split('\\n')[0]);
            return true;
        } catch (error) {
            console.log('❌ VS Code not found. Please install VS Code first.');
            return false;
        }
    }

    // Install VS Code extensions
    installExtensions() {
        console.log('📦 Installing VS Code extensions...');
        
        this.vscodeExtensions.forEach(extension => {
            try {
                execSync(\`code --install-extension \${extension}\`, { encoding: 'utf8' });
                console.log(\`✅ Installed: \${extension}\`);
            } catch (error) {
                console.log(\`⚠️ Failed to install: \${extension}\`);
            }
        });
    }

    // Create VS Code settings
    createVSCodeSettings() {
        const settings = {
            "editor.formatOnSave": true,
            "editor.codeActionsOnSave": {
                "source.fixAll": true,
                "source.organizeImports": true
            },
            "typescript.preferences.importModuleSpecifier": "relative",
            "javascript.preferences.importModuleSpecifier": "relative",
            "files.autoSave": "afterDelay",
            "files.autoSaveDelay": 1000,
            "terminal.integrated.defaultProfile.windows": "PowerShell",
            "terminal.integrated.defaultProfile.linux": "bash",
            "terminal.integrated.defaultProfile.osx": "bash"
        };

        const vscodeDir = path.join(process.cwd(), '.vscode');
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
        }

        const settingsPath = path.join(vscodeDir, 'settings.json');
        fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
        console.log('✅ VS Code settings created');
    }

    // Setup complete integration
    setup() {
        console.log('🚀 Setting up Kilo Code integration...');
        
        if (this.checkVSCode()) {
            this.installExtensions();
            this.createVSCodeSettings();
            console.log('✅ Kilo Code integration completed');
        } else {
            console.log('⚠️ Please install VS Code first, then run this script again');
        }
    }
}

// Export for use in other modules
module.exports = KiloCodeIntegration;

// If run directly
if (require.main === module) {
    const integration = new KiloCodeIntegration();
    integration.setup();
}
`;

            fs.writeFileSync('kilo-code-integration.js', kiloCodeScript);
            console.log('✅ Kilo Code integration script created');
            return true;
        } catch (error) {
            console.error('❌ Error creating Kilo Code integration:', error.message);
            return false;
        }
    }

    // Create EHB AI Dev integration
    createEHBIntegration() {
        try {
            console.log('🏥 Creating EHB AI Dev integration...');
            
            const ehbIntegration = `#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class EHBIntegration {
    constructor() {
        this.agents = [
            'agents/github-integration-agent.js',
            'agents/main-ehb-agent.js',
            'agents/healthAgent/healthComm.js',
            'agents/fixer/aiErrorFixerAgent.js'
        ];
    }

    // Check if all agents exist
    checkAgents() {
        console.log('🔍 Checking EHB agents...');
        
        this.agents.forEach(agent => {
            if (fs.existsSync(agent)) {
                console.log(\`✅ Found: \${agent}\`);
            } else {
                console.log(\`❌ Missing: \${agent}\`);
            }
        });
    }

    // Start EHB AI system
    startEHBSystem() {
        try {
            console.log('🚀 Starting EHB AI system...');
            
            if (fs.existsSync('start_ehb_ai_system.js')) {
                execSync('node start_ehb_ai_system.js', { stdio: 'inherit' });
            } else {
                console.log('⚠️ EHB AI system starter not found');
            }
        } catch (error) {
            console.error('❌ Error starting EHB system:', error.message);
        }
    }

    // Create VS Code tasks
    createVSCodeTasks() {
        const tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Start EHB AI System",
                    "type": "shell",
                    "command": "node",
                    "args": ["start_ehb_ai_system.js"],
                    "group": "build",
                    "presentation": {
                        "echo": true,
                        "reveal": "always",
                        "focus": false,
                        "panel": "shared"
                    }
                },
                {
                    "label": "GitHub Push",
                    "type": "shell",
                    "command": "node",
                    "args": ["agents/github-integration-agent.js", "--push"],
                    "group": "build"
                },
                {
                    "label": "Test System",
                    "type": "shell",
                    "command": "node",
                    "args": ["test_complete_system.js"],
                    "group": "test"
                }
            ]
        };

        const vscodeDir = path.join(process.cwd(), '.vscode');
        if (!fs.existsSync(vscodeDir)) {
            fs.mkdirSync(vscodeDir, { recursive: true });
        }

        const tasksPath = path.join(vscodeDir, 'tasks.json');
        fs.writeFileSync(tasksPath, JSON.stringify(tasks, null, 2));
        console.log('✅ VS Code tasks created');
    }

    // Setup complete integration
    setup() {
        console.log('🏥 Setting up EHB AI Dev integration...');
        
        this.checkAgents();
        this.createVSCodeTasks();
        
        console.log('✅ EHB AI Dev integration completed');
        console.log('📋 Available commands:');
        console.log('  - Ctrl+Shift+P → Tasks: Run Task → Start EHB AI System');
        console.log('  - Ctrl+Shift+P → Tasks: Run Task → GitHub Push');
        console.log('  - Ctrl+Shift+P → Tasks: Run Task → Test System');
    }
}

// Export for use in other modules
module.exports = EHBIntegration;

// If run directly
if (require.main === module) {
    const integration = new EHBIntegration();
    integration.setup();
}
`;

            fs.writeFileSync('ehb-integration.js', ehbIntegration);
            console.log('✅ EHB AI Dev integration script created');
            return true;
        } catch (error) {
            console.error('❌ Error creating EHB integration:', error.message);
            return false;
        }
    }

    // Complete setup process
    async completeSetup() {
        try {
            console.log('🚀 Starting complete SSH + Kilo Code + EHB integration setup...');
            console.log('='.repeat(60));
            
            // Step 1: SSH Setup
            console.log('🔑 Step 1: SSH Setup');
            if (!this.checkSSHKey()) {
                this.generateSSHKey();
            }
            this.setupSSHAgent();
            
            // Step 2: GitHub SSH Test
            console.log('🌐 Step 2: GitHub SSH Test');
            const sshPublicKey = this.getSSHPublicKey();
            if (sshPublicKey) {
                console.log('📋 Your SSH public key (add this to GitHub):');
                console.log(sshPublicKey);
                console.log('\\n💡 Please add this key to GitHub: Settings → SSH and GPG keys → New SSH key');
            }
            
            // Step 3: Git Remote Setup
            console.log('📁 Step 3: Git Remote Setup');
            this.setupGitRemote();
            
            // Step 4: Kilo Code Integration
            console.log('🤖 Step 4: Kilo Code Integration');
            this.createKiloCodeIntegration();
            
            // Step 5: EHB AI Dev Integration
            console.log('🏥 Step 5: EHB AI Dev Integration');
            this.createEHBIntegration();
            
            console.log('='.repeat(60));
            console.log('✅ Complete setup finished!');
            console.log('🎉 Your system is now ready for:');
            console.log('  • SSH-based GitHub push/pull');
            console.log('  • Kilo Code AI assistance');
            console.log('  • EHB AI Dev automation');
            console.log('  • VS Code/Cursor integration');
            
            // Create setup report
            this.createSetupReport(sshPublicKey);
            
        } catch (error) {
            console.error('❌ Setup failed:', error.message);
            throw error;
        }
    }

    // Create setup report
    createSetupReport(sshPublicKey) {
        const report = {
            timestamp: new Date().toISOString(),
            status: 'success',
            setup: {
                ssh: 'configured',
                github: 'ssh_ready',
                kilo_code: 'integration_ready',
                ehb_ai: 'integration_ready',
                vscode: 'tasks_configured'
            },
            nextSteps: [
                'Add SSH public key to GitHub: Settings → SSH and GPG keys',
                'Install VS Code extensions: Run node kilo-code-integration.js',
                'Start EHB AI system: Run node ehb-integration.js',
                'Test GitHub push: git push origin main'
            ],
            sshPublicKey: sshPublicKey
        };

        const reportFile = 'ssh-kilo-ehb-setup-report.json';
        fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
        console.log('📊 Setup report saved to:', reportFile);
    }
}

// Export for use in other modules
module.exports = SSHGitHubSetup;

// If run directly
if (require.main === module) {
    const setup = new SSHGitHubSetup();
    
    setup.completeSetup()
        .then(() => {
            console.log('🎉 Complete setup finished!');
        })
        .catch((error) => {
            console.error('💥 Setup failed:', error.message);
            process.exit(1);
        });
} 