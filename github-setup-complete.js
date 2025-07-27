#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class CompleteGitHubSetup {
    constructor() {
        this.token = 'YOUR_SECRET_HERE';
        this.repository = 'https://github.com/rafiehb555/ehb-5.git';
        this.username = 'rafiehb555';
        this.email = 'rafiehb555@gmail.com';
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

    // Check current user from token
    async checkTokenUser() {
        try {
            console.log('🔍 Checking token user...');
            
            const testUrl = 'https://api.github.com/user';
            const curlCommand = `curl -H "Authorization: token ${this.token}" ${testUrl}`;
            
            const result = execSync(curlCommand, { encoding: 'utf8' });
            const userInfo = JSON.parse(result);
            
            console.log('✅ Token user:', userInfo.login);
            console.log('📧 Email:', userInfo.email);
            console.log('🏢 Company:', userInfo.company);
            
            return userInfo;
        } catch (error) {
            console.error('❌ Error checking token user:', error.message);
            return null;
        }
    }

    // Create new repository for current user
    async createNewRepository() {
        try {
            console.log('🆕 Creating new repository for current user...');
            
            const userInfo = await this.checkTokenUser();
            if (!userInfo) {
                throw new Error('Cannot get user info from token');
            }
            
            const repoName = 'ehb-5';
            const createRepoUrl = 'https://api.github.com/user/repos';
            const repoData = {
                name: repoName,
                description: 'EHB AI System - Healthcare Automation Platform',
                private: false,
                auto_init: false
            };
            
            const curlCommand = `curl -X POST -H "Authorization: token ${this.token}" -H "Content-Type: application/json" -d '${JSON.stringify(repoData)}' ${createRepoUrl}`;
            
            const result = execSync(curlCommand, { encoding: 'utf8' });
            const repoInfo = JSON.parse(result);
            
            console.log('✅ Repository created:', repoInfo.html_url);
            
            // Update repository URL
            this.repository = repoInfo.clone_url;
            
            return repoInfo;
        } catch (error) {
            console.error('❌ Error creating repository:', error.message);
            return null;
        }
    }

    // Setup repository with proper authentication
    async setupRepository() {
        try {
            console.log('🔧 Setting up repository...');
            
            // Step 1: Check current user
            const userInfo = await this.checkTokenUser();
            if (!userInfo) {
                throw new Error('Cannot authenticate with GitHub');
            }
            
            // Step 2: Update username to match token user
            this.username = userInfo.login;
            this.email = userInfo.email || 'rafi.cdm5@gmail.com';
            
            console.log(`👤 Using user: ${this.username}`);
            console.log(`📧 Using email: ${this.email}`);
            
            // Step 3: Remove existing remote
            try {
                this.executeCommand('git remote remove origin');
            } catch (e) {
                console.log('No existing remote to remove');
            }
            
            // Step 4: Create new repository if needed
            let repoInfo = null;
            try {
                // Try to access the original repository
                const testUrl = 'https://api.github.com/repos/rafiehb555/ehb-5';
                const testCommand = `curl -H "Authorization: token ${this.token}" ${testUrl}`;
                execSync(testCommand, { encoding: 'utf8' });
                console.log('✅ Original repository accessible');
            } catch (e) {
                console.log('❌ Original repository not accessible, creating new one...');
                repoInfo = await this.createNewRepository();
                if (repoInfo) {
                    this.repository = repoInfo.clone_url;
                }
            }
            
            // Step 5: Add remote with authenticated URL
            const authUrl = this.repository.replace('https://', `https://${this.token}@`);
            this.executeCommand(`git remote add origin ${authUrl}`);
            
            // Step 6: Configure Git user
            this.executeCommand(`git config user.name "${this.username}"`);
            this.executeCommand(`git config user.email "${this.email}"`);
            
            // Step 7: Set branch to main
            this.executeCommand('git branch -M main');
            
            // Step 8: Test connection
            console.log('🔍 Testing connection...');
            this.executeCommand('git remote -v');
            
            // Step 9: Push to repository
            console.log('🚀 Pushing to repository...');
            this.executeCommand('git push -u origin main');
            
            console.log('✅ Repository setup completed successfully!');
            
            // Create success report
            this.createSuccessReport(userInfo, repoInfo);
            
        } catch (error) {
            console.error('❌ Error setting up repository:', error.message);
            throw error;
        }
    }

    // Create success report
    createSuccessReport(userInfo, repoInfo) {
        const report = {
            timestamp: new Date().toISOString(),
            status: 'success',
            user: {
                login: userInfo.login,
                email: userInfo.email,
                company: userInfo.company
            },
            repository: repoInfo ? {
                name: repoInfo.name,
                url: repoInfo.html_url,
                clone_url: repoInfo.clone_url
            } : {
                name: 'ehb-5',
                url: 'https://github.com/rafiehb555/ehb-5',
                clone_url: this.repository
            },
            setup: {
                branch: 'main',
                authentication: 'token-based',
                features: [
                    'Git repository initialized',
                    'Git user configured',
                    'Remote repository setup',
                    'Authentication configured',
                    'Code pushed to GitHub'
                ]
            },
            nextSteps: [
                'Run: node agents/github-integration-agent.js --init',
                'Run: node agents/github-integration-agent.js --start',
                'Monitor: node auto-github-push.js --stats'
            ]
        };

        const reportFile = path.join(__dirname, 'github-setup-success.json');
        fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
        console.log('📊 Success report saved to: github-setup-success.json');
        
        console.log('\n🎉 GitHub Setup Summary:');
        console.log(`👤 User: ${userInfo.login}`);
        console.log(`📧 Email: ${userInfo.email}`);
        console.log(`🏢 Company: ${userInfo.company}`);
        if (repoInfo) {
            console.log(`📁 Repository: ${repoInfo.html_url}`);
        } else {
            console.log(`📁 Repository: https://github.com/rafiehb555/ehb-5`);
        }
        console.log(`🔗 Clone URL: ${this.repository}`);
    }

    // Complete setup process
    async completeSetup() {
        try {
            console.log('🚀 Starting complete GitHub setup...');
            console.log('='.repeat(50));
            
            await this.setupRepository();
            
            console.log('='.repeat(50));
            console.log('✅ Complete GitHub setup finished successfully!');
            console.log('🎉 Your EHB AI System is now connected to GitHub');
            
        } catch (error) {
            console.error('❌ Complete setup failed:', error.message);
            console.log('💡 Please check your GitHub token and permissions');
            throw error;
        }
    }
}

// Export for use in other modules
module.exports = CompleteGitHubSetup;

// If run directly
if (require.main === module) {
    const setup = new CompleteGitHubSetup();
    
    setup.completeSetup()
        .then(() => {
            console.log('🎉 Complete setup finished!');
        })
        .catch((error) => {
            console.error('💥 Complete setup failed:', error.message);
            process.exit(1);
        });
} 