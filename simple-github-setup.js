#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');

class SimpleGitHubSetup {
    constructor() {
        this.token = 'YOUR_SECRET_HERE';
        this.username = 'EHB-4';
        this.email = 'rafi.cdm5@gmail.com';
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

    // Create repository for current user
    async createUserRepository() {
        try {
            console.log('🆕 Creating repository for EHB-4...');
            
            const repoName = 'ehb-5';
            const createRepoUrl = 'https://api.github.com/user/repos';
            const repoData = {
                name: repoName,
                description: 'EHB AI System - Healthcare Automation Platform',
                private: false,
                auto_init: false
            };
            
            const dataString = JSON.stringify(repoData);
            const curlCommand = `curl -X POST -H "Authorization: token ${this.token}" -H "Content-Type: application/json" -d "${dataString.replace(/"/g, '\\"')}" ${createRepoUrl}`;
            
            console.log('Creating repository with command:', curlCommand);
            const result = execSync(curlCommand, { encoding: 'utf8' });
            console.log('Raw result:', result);
            
            const repoInfo = JSON.parse(result);
            console.log('✅ Repository created successfully!');
            console.log('📁 Repository URL:', repoInfo.html_url);
            console.log('🔗 Clone URL:', repoInfo.clone_url);
            
            return repoInfo;
        } catch (error) {
            console.error('❌ Error creating repository:', error.message);
            console.log('Trying alternative approach...');
            return this.createRepositoryAlternative();
        }
    }

    // Alternative repository creation
    createRepositoryAlternative() {
        try {
            console.log('🔄 Trying alternative repository creation...');
            
            const repoName = 'ehb-5';
            const createRepoUrl = 'https://api.github.com/user/repos';
            
            // Use simpler data format
            const data = `{"name":"${repoName}","description":"EHB AI System","private":false}`;
            const curlCommand = `curl -X POST -H "Authorization: token ${this.token}" -H "Content-Type: application/json" -d '${data}' ${createRepoUrl}`;
            
            const result = execSync(curlCommand, { encoding: 'utf8' });
            const repoInfo = JSON.parse(result);
            
            console.log('✅ Repository created with alternative method!');
            return repoInfo;
        } catch (error) {
            console.error('❌ Alternative creation failed:', error.message);
            throw error;
        }
    }

    // Setup Git with new repository
    async setupGit(repoInfo) {
        try {
            console.log('🔧 Setting up Git with new repository...');
            
            // Remove existing remote
            try {
                this.executeCommand('git remote remove origin');
            } catch (e) {
                console.log('No existing remote to remove');
            }
            
            // Add new remote
            const authUrl = repoInfo.clone_url.replace('https://', `https://${this.token}@`);
            this.executeCommand(`git remote add origin ${authUrl}`);
            
            // Configure Git user
            this.executeCommand(`git config user.name "${this.username}"`);
            this.executeCommand(`git config user.email "${this.email}"`);
            
            // Set branch to main
            this.executeCommand('git branch -M main');
            
            // Test connection
            console.log('🔍 Testing connection...');
            this.executeCommand('git remote -v');
            
            // Push to repository
            console.log('🚀 Pushing to repository...');
            this.executeCommand('git push -u origin main');
            
            console.log('✅ Successfully pushed to repository!');
            
        } catch (error) {
            console.error('❌ Error setting up Git:', error.message);
            throw error;
        }
    }

    // Complete setup
    async completeSetup() {
        try {
            console.log('🚀 Starting simple GitHub setup...');
            console.log('='.repeat(50));
            
            // Step 1: Create repository
            const repoInfo = await this.createUserRepository();
            
            // Step 2: Setup Git
            await this.setupGit(repoInfo);
            
            console.log('='.repeat(50));
            console.log('✅ Simple GitHub setup completed!');
            console.log('🎉 Your EHB AI System is now in your repository');
            console.log(`📁 Repository: ${repoInfo.html_url}`);
            
            // Create success report
            this.createSuccessReport(repoInfo);
            
        } catch (error) {
            console.error('❌ Simple setup failed:', error.message);
            throw error;
        }
    }

    // Create success report
    createSuccessReport(repoInfo) {
        const report = {
            timestamp: new Date().toISOString(),
            status: 'success',
            repository: {
                name: repoInfo.name,
                url: repoInfo.html_url,
                clone_url: repoInfo.clone_url
            },
            user: {
                login: this.username,
                email: this.email
            },
            setup: {
                branch: 'main',
                authentication: 'token-based',
                features: [
                    'Repository created',
                    'Git remote configured',
                    'Authentication setup',
                    'Code pushed successfully'
                ]
            },
            nextSteps: [
                'Run: node agents/github-integration-agent.js --init',
                'Run: node agents/github-integration-agent.js --start',
                'Monitor: node auto-github-push.js --stats'
            ]
        };

        const reportFile = 'simple-github-setup-success.json';
        fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
        console.log('📊 Success report saved to: simple-github-setup-success.json');
    }
}

// Export for use in other modules
module.exports = SimpleGitHubSetup;

// If run directly
if (require.main === module) {
    const setup = new SimpleGitHubSetup();
    
    setup.completeSetup()
        .then(() => {
            console.log('🎉 Simple setup finished!');
        })
        .catch((error) => {
            console.error('💥 Simple setup failed:', error.message);
            process.exit(1);
        });
} 