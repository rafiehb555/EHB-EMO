const axios = require('axios');
const fs = require('fs');
const path = require('path');

class EHB5PlatformTester {
    constructor() {
        this.baseURL = 'http://localhost:3000';
        this.results = {
            server: false,
            services: false,
            health: false,
            filesCount: 0,
            servicesCount: 0
        };
    }

    async testServer() {
        try {
            console.log('🔍 Testing EHB-5 Server...');
            const response = await axios.get(this.baseURL);

            if (response.data.success) {
                console.log('✅ Server is running successfully!');
                console.log(`📊 Platform: ${response.data.platform.name}`);
                console.log(`🏗️ Architecture: ${response.data.services.architecture}`);
                console.log(`📦 Services: ${response.data.services.total}`);
                this.results.server = true;
                return true;
            }
            return false;
        } catch (error) {
            console.log('❌ Server test failed:', error.message);
            return false;
        }
    }

    async testServices() {
        try {
            console.log('\n🔍 Testing Services API...');
            const response = await axios.get(`${this.baseURL}/api/services`);

            if (response.data.success) {
                console.log(`✅ Found ${response.data.total} services!`);
                response.data.services.forEach(service => {
                    console.log(`   📁 ${service.name}`);
                });
                this.results.services = true;
                this.results.servicesCount = response.data.total;
                return true;
            }
            return false;
        } catch (error) {
            console.log('❌ Services test failed:', error.message);
            return false;
        }
    }

    async testHealth() {
        try {
            console.log('\n🔍 Testing Health Check...');
            const response = await axios.get(`${this.baseURL}/health`);

            if (response.data.status === 'healthy') {
                console.log('✅ Health check passed!');
                console.log(`⏱️  Uptime: ${Math.round(response.data.uptime)} seconds`);
                console.log(`💾 Memory: ${Math.round(response.data.memory.heapUsed / 1024 / 1024)}MB used`);
                this.results.health = true;
                return true;
            }
            return false;
        } catch (error) {
            console.log('❌ Health test failed:', error.message);
            return false;
        }
    }

    testFileStructure() {
        console.log('\n🔍 Testing File Structure...');

        // Count total files
        const countFiles = (dir) => {
            let count = 0;
            try {
                const items = fs.readdirSync(dir, { withFileTypes: true });
                for (const item of items) {
                    if (item.isFile()) {
                        count++;
                    } else if (item.isDirectory() && !item.name.startsWith('.') && item.name !== 'node_modules') {
                        count += countFiles(path.join(dir, item.name));
                    }
                }
            } catch (error) {
                // Ignore errors for directories we can't read
            }
            return count;
        };

        const totalFiles = countFiles('.');
        this.results.filesCount = totalFiles;

        // Check key directories
        const keyDirs = ['services', 'frontend', 'backend', 'docs'];
        let foundDirs = 0;

        keyDirs.forEach(dir => {
            if (fs.existsSync(dir)) {
                console.log(`✅ Found ${dir}/ directory`);
                foundDirs++;
            } else {
                console.log(`❌ Missing ${dir}/ directory`);
            }
        });

        console.log(`📁 Total files: ${totalFiles}`);
        console.log(`📂 Key directories: ${foundDirs}/${keyDirs.length}`);

        return foundDirs === keyDirs.length;
    }

    async runAllTests() {
        console.log('🚀 Starting EHB-5 Platform Tests...\n');

        const fileTest = this.testFileStructure();
        const serverTest = await this.testServer();
        const servicesTest = await this.testServices();
        const healthTest = await this.testHealth();

        console.log('\n📊 TEST RESULTS:');
        console.log('='.repeat(50));
        console.log(`Server Test:     ${serverTest ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Services Test:   ${servicesTest ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Health Test:     ${healthTest ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`File Structure:  ${fileTest ? '✅ PASS' : '❌ FAIL'}`);
        console.log('='.repeat(50));

        const allPassed = serverTest && servicesTest && healthTest && fileTest;

        if (allPassed) {
            console.log('🎉 ALL TESTS PASSED! EHB-5 Platform is working perfectly!');
            console.log(`📦 ${this.results.servicesCount} services configured`);
            console.log(`📁 ${this.results.filesCount} files organized`);
        } else {
            console.log('⚠️  Some tests failed. Please check the issues above.');
        }

        return allPassed;
    }
}

// Run tests
if (require.main === module) {
    const tester = new EHB5PlatformTester();

    // Wait a moment for server to start if it's starting
    setTimeout(() => {
        tester.runAllTests().then(success => {
            process.exit(success ? 0 : 1);
        });
    }, 2000);
}

module.exports = EHB5PlatformTester;
