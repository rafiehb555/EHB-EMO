#!/usr/bin/env node

const GitHubPusher = require('./github-push.js');
const fs = require('fs');
const path = require('path');

class AutoGitHubPusher {
    constructor() {
        this.pusher = new GitHubPusher();
        this.lastPushTime = null;
        this.pushInterval = 5 * 60 * 1000; // 5 minutes
    }

    // Check if files have changed since last push
    hasChanges() {
        try {
            const status = this.pusher.executeGitCommand('git status --porcelain');
            return status.trim().length > 0;
        } catch (error) {
            console.error('Error checking for changes:', error.message);
            return false;
        }
    }

    // Get list of changed files
    getChangedFiles() {
        try {
            const status = this.pusher.executeGitCommand('git status --porcelain');
            return status.split('\n').filter(line => line.trim().length > 0);
        } catch (error) {
            console.error('Error getting changed files:', error.message);
            return [];
        }
    }

    // Generate commit message based on changes
    generateCommitMessage() {
        const changedFiles = this.getChangedFiles();
        const categories = {
            'agents/': '🤖 Agent updates',
            'src/': '💻 Source code changes',
            'frontend/': '🎨 Frontend updates',
            'backend/': '⚙️ Backend updates',
            'deployment/': '🚀 Deployment changes',
            'docs/': '📚 Documentation updates',
            'tests/': '🧪 Test updates',
            'config/': '⚙️ Configuration changes'
        };

        let message = '🔄 EHB AI System - Auto update\n\n';
        message += `📅 ${new Date().toLocaleString()}\n`;
        message += `📁 Files changed: ${changedFiles.length}\n\n`;

        // Categorize changes
        const categoriesFound = new Set();
        changedFiles.forEach(file => {
            for (const [pattern, category] of Object.entries(categories)) {
                if (file.includes(pattern)) {
                    categoriesFound.add(category);
                    break;
                }
            }
        });

        if (categoriesFound.size > 0) {
            message += '📋 Categories:\n';
            categoriesFound.forEach(category => {
                message += `  • ${category}\n`;
            });
        }

        return message;
    }

    // Auto push with intelligent commit messages
    async autoPush() {
        try {
            console.log('🔍 Checking for changes...');
            
            if (!this.hasChanges()) {
                console.log('✅ No changes detected, skipping push');
                return true;
            }

            console.log('📝 Changes detected, preparing push...');
            
            // Generate intelligent commit message
            const commitMessage = this.generateCommitMessage();
            
            // Perform push
            const success = await this.pusher.pushAll(commitMessage);
            
            if (success) {
                this.lastPushTime = new Date();
                console.log('✅ Auto push completed successfully!');
                
                // Log push activity
                this.logPushActivity(commitMessage);
            }
            
            return success;
        } catch (error) {
            console.error('❌ Auto push failed:', error.message);
            return false;
        }
    }

    // Log push activity
    logPushActivity(commitMessage) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            commitMessage: commitMessage,
            status: 'success'
        };

        const logFile = path.join(__dirname, 'logs', 'github-push.log');
        const logDir = path.dirname(logFile);
        
        // Create logs directory if it doesn't exist
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // Append to log file
        fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
    }

    // Start auto push monitoring
    startAutoPush() {
        console.log('🚀 Starting auto GitHub push monitoring...');
        console.log(`⏰ Push interval: ${this.pushInterval / 1000} seconds`);
        
        // Initial push
        this.autoPush();
        
        // Set up interval for auto push
        setInterval(() => {
            this.autoPush();
        }, this.pushInterval);
    }

    // Manual push with custom message
    async manualPush(customMessage = null) {
        try {
            console.log('🔄 Performing manual push...');
            
            const message = customMessage || this.generateCommitMessage();
            const success = await this.pusher.pushAll(message);
            
            if (success) {
                console.log('✅ Manual push completed successfully!');
            }
            
            return success;
        } catch (error) {
            console.error('❌ Manual push failed:', error.message);
            return false;
        }
    }

    // Get push statistics
    getPushStats() {
        try {
            const logFile = path.join(__dirname, 'logs', 'github-push.log');
            
            if (!fs.existsSync(logFile)) {
                return {
                    totalPushes: 0,
                    lastPush: null,
                    successRate: 0
                };
            }

            const logs = fs.readFileSync(logFile, 'utf8')
                .split('\n')
                .filter(line => line.trim().length > 0)
                .map(line => JSON.parse(line));

            const totalPushes = logs.length;
            const successfulPushes = logs.filter(log => log.status === 'success').length;
            const lastPush = logs.length > 0 ? logs[logs.length - 1] : null;

            return {
                totalPushes,
                lastPush: lastPush?.timestamp || null,
                successRate: totalPushes > 0 ? (successfulPushes / totalPushes) * 100 : 0
            };
        } catch (error) {
            console.error('Error getting push stats:', error.message);
            return {
                totalPushes: 0,
                lastPush: null,
                successRate: 0
            };
        }
    }
}

// Export for use in other modules
module.exports = AutoGitHubPusher;

// If run directly
if (require.main === module) {
    const autoPusher = new AutoGitHubPusher();
    
    // Check command line arguments
    const args = process.argv.slice(2);
    
    if (args.includes('--manual')) {
        // Manual push
        const customMessage = args.find(arg => arg.startsWith('--message='))?.split('=')[1];
        autoPusher.manualPush(customMessage);
    } else if (args.includes('--stats')) {
        // Show statistics
        const stats = autoPusher.getPushStats();
        console.log('📊 GitHub Push Statistics:');
        console.log(`Total pushes: ${stats.totalPushes}`);
        console.log(`Last push: ${stats.lastPush || 'Never'}`);
        console.log(`Success rate: ${stats.successRate.toFixed(1)}%`);
    } else if (args.includes('--auto')) {
        // Start auto push monitoring
        autoPusher.startAutoPush();
    } else {
        // Default: single push
        autoPusher.autoPush();
    }
} 