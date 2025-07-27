#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');

class GitHubAuthFixer {
    constructor() {
        this.token = 'YOUR_SECRET_HERE';
        this.repository = 'https://github.com/rafiehb555/ehb-5.git';
        this.username = 'rafiehb555';
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

    // Fix authentication
    async fixAuth() {
        try {
            console.log('🔧 Fixing GitHub authentication...');
            
            // Step 1: Remove existing remote
            try {
                this.executeCommand('git remote remove origin');
            } catch (e) {
                console.log('No existing remote to remove');
            }
            
            // Step 2: Add remote with proper authentication
            const authUrl = `https://${this.token}@github.com/rafiehb555/ehb-5.git`;
            this.executeCommand(`git remote add origin ${authUrl}`);
            
            // Step 3: Configure Git user
            this.executeCommand(`git config user.name "${this.username}"`);
            this.executeCommand(`git config user.email "rafiehb555@gmail.com"`);
            
            // Step 4: Set branch to main
            this.executeCommand('git branch -M main');
            
            // Step 5: Test connection
            console.log('🔍 Testing connection...');
            this.executeCommand('git remote -v');
            
            // Step 6: Try push
            console.log('🚀 Attempting push...');
            this.executeCommand('git push -u origin main');
            
            console.log('✅ Authentication fixed successfully!');
            
        } catch (error) {
            console.error('❌ Error fixing authentication:', error.message);
            
            // Alternative approach
            console.log('🔄 Trying alternative approach...');
            this.tryAlternativeAuth();
        }
    }

    // Alternative authentication method
    tryAlternativeAuth() {
        try {
            console.log('🔄 Using alternative authentication method...');
            
            // Use HTTPS with token in URL
            const altUrl = `https://${this.token}@github.com/rafiehb555/ehb-5.git`;
            this.executeCommand(`git remote set-url origin ${altUrl}`);
            
            // Try push again
            this.executeCommand('git push -u origin main');
            
            console.log('✅ Alternative authentication successful!');
            
        } catch (error) {
            console.error('❌ Alternative authentication failed:', error.message);
            console.log('💡 Please check your GitHub token permissions');
        }
    }

    // Check token validity
    checkToken() {
        try {
            console.log('🔍 Checking token validity...');
            
            // Test with curl
            const testUrl = 'https://api.github.com/user';
            const curlCommand = `curl -H "Authorization: token ${this.token}" ${testUrl}`;
            
            const result = execSync(curlCommand, { encoding: 'utf8' });
            console.log('✅ Token is valid');
            console.log('User info:', result);
            
        } catch (error) {
            console.error('❌ Token validation failed:', error.message);
            console.log('💡 Please check your GitHub token');
        }
    }
}

// Export for use in other modules
module.exports = GitHubAuthFixer;

// If run directly
if (require.main === module) {
    const fixer = new GitHubAuthFixer();
    
    // Check token first
    fixer.checkToken();
    
    // Fix authentication
    fixer.fixAuth()
        .then(() => {
            console.log('🎉 Authentication fix completed!');
        })
        .catch((error) => {
            console.error('💥 Authentication fix failed:', error.message);
        });
} 