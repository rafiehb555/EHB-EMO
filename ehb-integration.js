#!/usr/bin/env node

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
                console.log(`✅ Found: ${agent}`);
            } else {
                console.log(`❌ Missing: ${agent}`);
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
