#!/usr/bin/env node

/**
 * EHB-JPS Backend Quick Start Script
 * This script helps you test the backend API with sample data
 */

const axios = require('axios');
const readline = require('readline');

const API_BASE_URL = 'http://localhost:3001/api';

// Colors for console output
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m'
};

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Sample data
const sampleUsers = [
    {
        email: 'admin@ehb-jps.com',
        password: 'admin123',
        first_name: 'Admin',
        last_name: 'User',
        user_type: 'admin'
    },
    {
        email: 'company@techcorp.com',
        password: 'company123',
        first_name: 'John',
        last_name: 'Company',
        user_type: 'company'
    },
    {
        email: 'jobseeker@example.com',
        password: 'jobseeker123',
        first_name: 'Jane',
        last_name: 'Doe',
        user_type: 'jobseeker'
    }
];

const sampleJobs = [
    {
        title: 'Senior Full Stack Developer',
        description: 'We are looking for an experienced full-stack developer...',
        salary_min: 80000,
        salary_max: 120000,
        location: 'Remote',
        job_type: 'full-time',
        skills: ['JavaScript', 'React', 'Node.js', 'PostgreSQL']
    },
    {
        title: 'Frontend Developer',
        description: 'Join our team as a frontend developer...',
        salary_min: 60000,
        salary_max: 90000,
        location: 'New York',
        job_type: 'full-time',
        skills: ['React', 'TypeScript', 'CSS', 'HTML']
    }
];

const sampleCompanies = [
    {
        company_name: 'Tech Corp',
        industry: 'Technology',
        description: 'Leading technology company...',
        location: 'San Francisco',
        website: 'https://techcorp.com'
    },
    {
        company_name: 'Innovation Labs',
        industry: 'Software Development',
        description: 'Innovative software solutions...',
        location: 'Austin',
        website: 'https://innovationlabs.com'
    }
];

// Helper functions
function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSuccess(message) {
    log(`✅ ${message}`, 'green');
}

function logError(message) {
    log(`❌ ${message}`, 'red');
}

function logInfo(message) {
    log(`ℹ️ ${message}`, 'blue');
}

function logWarning(message) {
    log(`⚠️ ${message}`, 'yellow');
}

// API helper
async function makeRequest(method, endpoint, data = null, token = null) {
    try {
        const config = {
            method,
            url: `${API_BASE_URL}${endpoint}`,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        if (data) {
            config.data = data;
        }

        const response = await axios(config);
        return { success: true, data: response.data };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data || error.message
        };
    }
}

// Test functions
async function testHealthCheck() {
    logInfo('Testing health check...');
    const result = await makeRequest('GET', '/health');

    if (result.success) {
        logSuccess('Health check passed');
        return true;
    } else {
        logError('Health check failed');
        return false;
    }
}

async function testUserRegistration() {
    logInfo('Testing user registration...');
    const tokens = [];

    for (const user of sampleUsers) {
        const result = await makeRequest('POST', '/auth/register', user);

        if (result.success) {
            logSuccess(`Registered ${user.email}`);
            tokens.push(result.data.data.token);
        } else {
            logError(`Failed to register ${user.email}: ${result.error.message}`);
        }
    }

    return tokens;
}

async function testUserLogin() {
    logInfo('Testing user login...');
    const tokens = [];

    for (const user of sampleUsers) {
        const result = await makeRequest('POST', '/auth/login', {
            email: user.email,
            password: user.password
        });

        if (result.success) {
            logSuccess(`Logged in ${user.email}`);
            tokens.push(result.data.data.token);
        } else {
            logError(`Failed to login ${user.email}: ${result.error.message}`);
        }
    }

    return tokens;
}

async function testCompanyCreation(tokens) {
    logInfo('Testing company creation...');
    const companyToken = tokens.find((_, index) => sampleUsers[index].user_type === 'company');

    if (!companyToken) {
        logError('No company user token found');
        return;
    }

    for (const company of sampleCompanies) {
        const result = await makeRequest('POST', '/companies', company, companyToken);

        if (result.success) {
            logSuccess(`Created company: ${company.company_name}`);
        } else {
            logError(`Failed to create company ${company.company_name}: ${result.error.message}`);
        }
    }
}

async function testJobCreation(tokens) {
    logInfo('Testing job creation...');
    const companyToken = tokens.find((_, index) => sampleUsers[index].user_type === 'company');

    if (!companyToken) {
        logError('No company user token found');
        return;
    }

    // First get company ID
    const companiesResult = await makeRequest('GET', '/companies', null, companyToken);

    if (!companiesResult.success || !companiesResult.data.data.companies.length) {
        logError('No companies found for job creation');
        return;
    }

    const companyId = companiesResult.data.data.companies[0].id;

    for (const job of sampleJobs) {
        const jobData = { ...job, company_id: companyId };
        const result = await makeRequest('POST', '/jobs', jobData, companyToken);

        if (result.success) {
            logSuccess(`Created job: ${job.title}`);
        } else {
            logError(`Failed to create job ${job.title}: ${result.error.message}`);
        }
    }
}

async function testJobSearch() {
    logInfo('Testing job search...');
    const result = await makeRequest('GET', '/jobs?limit=5');

    if (result.success) {
        const jobs = result.data.data.jobs;
        logSuccess(`Found ${jobs.length} jobs`);
        jobs.forEach(job => {
            log(`  - ${job.title} at ${job.company?.company_name}`, 'blue');
        });
    } else {
        logError(`Failed to search jobs: ${result.error.message}`);
    }
}

async function testUserProfile(tokens) {
    logInfo('Testing user profile...');
    const jobseekerToken = tokens.find((_, index) => sampleUsers[index].user_type === 'jobseeker');

    if (!jobseekerToken) {
        logError('No jobseeker user token found');
        return;
    }

    const result = await makeRequest('GET', '/users/profile', null, jobseekerToken);

    if (result.success) {
        logSuccess('Retrieved user profile');
        log(`  User: ${result.data.data.user.first_name} ${result.data.data.user.last_name}`, 'blue');
    } else {
        logError(`Failed to get user profile: ${result.error.message}`);
    }
}

async function testAdminDashboard(tokens) {
    logInfo('Testing admin dashboard...');
    const adminToken = tokens.find((_, index) => sampleUsers[index].user_type === 'admin');

    if (!adminToken) {
        logError('No admin user token found');
        return;
    }

    const result = await makeRequest('GET', '/admin/dashboard', null, adminToken);

    if (result.success) {
        logSuccess('Retrieved admin dashboard');
        const stats = result.data.data.stats;
        log(`  Total Users: ${stats.total_users}`, 'blue');
        log(`  Total Jobs: ${stats.total_jobs}`, 'blue');
        log(`  Total Companies: ${stats.total_companies}`, 'blue');
        log(`  Total Applications: ${stats.total_applications}`, 'blue');
    } else {
        logError(`Failed to get admin dashboard: ${result.error.message}`);
    }
}

// Main test function
async function runTests() {
    log('🚀 Starting EHB-JPS Backend Tests', 'green');
    log('=====================================', 'green');

    // Test 1: Health Check
    const healthOk = await testHealthCheck();
    if (!healthOk) {
        logError('Server is not running. Please start the server first.');
        logInfo('Run: npm run dev');
        process.exit(1);
    }

    // Test 2: User Registration
    log('\n📝 Testing User Registration', 'yellow');
    await testUserRegistration();

    // Test 3: User Login
    log('\n🔐 Testing User Login', 'yellow');
    const tokens = await testUserLogin();

    if (tokens.length === 0) {
        logError('No valid tokens obtained. Stopping tests.');
        return;
    }

    // Test 4: Company Creation
    log('\n🏢 Testing Company Creation', 'yellow');
    await testCompanyCreation(tokens);

    // Test 5: Job Creation
    log('\n💼 Testing Job Creation', 'yellow');
    await testJobCreation(tokens);

    // Test 6: Job Search
    log('\n🔍 Testing Job Search', 'yellow');
    await testJobSearch();

    // Test 7: User Profile
    log('\n👤 Testing User Profile', 'yellow');
    await testUserProfile(tokens);

    // Test 8: Admin Dashboard
    log('\n📊 Testing Admin Dashboard', 'yellow');
    await testAdminDashboard(tokens);

    log('\n🎉 All tests completed!', 'green');
    log('=====================================', 'green');
}

// CLI interface
function showMenu() {
    log('\n📋 EHB-JPS Backend Test Menu', 'green');
    log('1. Run all tests', 'blue');
    log('2. Test health check only', 'blue');
    log('3. Test user registration', 'blue');
    log('4. Test job search', 'blue');
    log('5. Exit', 'blue');

    rl.question('\nSelect an option (1-5): ', async (answer) => {
        switch (answer) {
            case '1':
                await runTests();
                rl.close();
                break;
            case '2':
                await testHealthCheck();
                rl.close();
                break;
            case '3':
                await testUserRegistration();
                rl.close();
                break;
            case '4':
                await testJobSearch();
                rl.close();
                break;
            case '5':
                log('Goodbye!', 'green');
                rl.close();
                break;
            default:
                log('Invalid option. Please try again.', 'red');
                showMenu();
        }
    });
}

// Check if server is running
async function checkServer() {
    try {
        await axios.get(`${API_BASE_URL.replace('/api', '')}/health`);
        return true;
    } catch (error) {
        return false;
    }
}

// Main execution
async function main() {
    log('🔍 Checking if server is running...', 'blue');
    const serverRunning = await checkServer();

    if (!serverRunning) {
        logError('Server is not running on http://localhost:3001');
        logInfo('Please start the server first:');
        logInfo('1. cd services/EHB-JPS/backend');
        logInfo('2. npm install');
        logInfo('3. npm run dev');
        process.exit(1);
    }

    logSuccess('Server is running!');
    showMenu();
}

// Run if this file is executed directly
if (require.main === module) {
    main().catch(error => {
        logError(`Unexpected error: ${error.message}`);
        process.exit(1);
    });
}

module.exports = {
    runTests,
    testHealthCheck,
    testUserRegistration,
    testJobSearch
};
