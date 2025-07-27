#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');

class NewRepositoryCreator {
    constructor() {
        this.token = 'YOUR_SECRET_HERE';
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

    // Create new repository
    async createRepository() {
        try {
            console.log('🆕 Creating new repository for EHB-4...');
            
            const repoName = 'ehb-5';
            const createRepoUrl = 'https://api.github.com/user/repos';
            const repoData = {
                name: repoName,
                description: 'EHB AI System - Healthcare Automation Platform',
                private: false,
                auto_init: false,
                gitignore_template: 'Node',
                license_template: 'mit'
            };
            
            const curlCommand = `curl -X POST -H "Authorization: token ${this.token}" -H "Content-Type: application/json" -d '${JSON.stringify(repoData)}' ${createRepoUrl}`;
            
            const result = execSync(curlCommand, { encoding: 'utf8' });
            const repoInfo = JSON.parse(result);
            
            console.log('✅ Repository created successfully!');
            console.log('📁 Repository URL:', repoInfo.html_url);
            console.log('🔗 Clone URL:', repoInfo.clone_url);
            
            // Update remote to new repository
            this.updateRemote(repoInfo.clone_url);
            
            return repoInfo;
        } catch (error) {
            console.error('❌ Error creating repository:', error.message);
            throw error;
        }
    }

    // Update remote to new repository
    updateRemote(cloneUrl) {
        try {
            console.log('🔄 Updating remote to new repository...');
            
            // Remove existing remote
            try {
                this.executeCommand('git remote remove origin');
            } catch (e) {
                console.log('No existing remote to remove');
            }
            
            // Add new remote with authentication
            const authUrl = cloneUrl.replace('https://', `https://${this.token}@`);
            this.executeCommand(`git remote add origin ${authUrl}`);
            
            // Configure Git user
            this.executeCommand('git config user.name "EHB-4"');
            this.executeCommand('git config user.email "rafi.cdm5@gmail.com"');
            
            // Set branch to main
            this.executeCommand('git branch -M main');
            
            // Test connection
            console.log('🔍 Testing new connection...');
            this.executeCommand('git remote -v');
            
            // Push to new repository
            console.log('🚀 Pushing to new repository...');
            this.executeCommand('git push -u origin main');
            
            console.log('✅ Successfully pushed to new repository!');
            
        } catch (error) {
            console.error('❌ Error updating remote:', error.message);
            throw error;
        }
    }

    // Complete setup
    async completeSetup() {
        try {
            console.log('🚀 Starting new repository setup...');
            console.log('='.repeat(50));
            
            const repoInfo = await this.createRepository();
            
            console.log('='.repeat(50));
            console.log('✅ New repository setup completed!');
            console.log('🎉 Your EHB AI System is now in your own repository');
            console.log(`📁 Repository: ${repoInfo.html_url}`);
            
            // Create success report
            this.createSuccessReport(repoInfo);
            
        } catch (error) {
            console.error('❌ New repository setup failed:', error.message);
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
                clone_url: repoInfo.clone_url,
                description: repoInfo.description
            },
            user: {
                login: 'EHB-4',
                email: 'rafi.cdm5@gmail.com'
            },
            setup: {
                branch: 'main',
                authentication: 'token-based',
                features: [
                    'New repository created',
                    'Git remote updated',
                    'Authentication configured',
                    'Code pushed to new repository'
                ]
            },
            nextSteps: [
                'Run: node agents/github-integration-agent.js --init',
                'Run: node agents/github-integration-agent.js --start',
                'Monitor: node auto-github-push.js --stats'
            ]
        };

        const reportFile = 'new-repo-setup-success.json';
        fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
        console.log('📊 Success report saved to: new-repo-setup-success.json');
    }
}

// Export for use in other modules
module.exports = NewRepositoryCreator;

// If run directly
if (require.main === module) {
    const creator = new NewRepositoryCreator();
    
    creator.completeSetup()
        .then(() => {
            console.log('🎉 New repository setup finished!');
        })
        .catch((error) => {
            console.error('💥 New repository setup failed:', error.message);
            process.exit(1);
        });
} 