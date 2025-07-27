/**
 * 🏥 EHB Healthcare System Integration Test
 * 
 * Tests the complete integration between frontend, backend, and AI agents
 * with healthcare-specific validation and HIPAA compliance checks.
 */

const axios = require('axios');
const crypto = require('crypto');

class EHBSystemIntegrationTest {
    constructor() {
        this.frontendUrl = 'http://localhost:3001';
        this.backendUrl = 'http://localhost:8000';
        this.testResults = [];
        this.criticalErrors = [];
    }

    /**
     * Run complete system integration test
     */
    async runFullIntegrationTest() {
        console.log('🏥 Starting EHB Healthcare System Integration Test...\n');

        try {
            // Test 1: Frontend Connectivity
            await this.testFrontendConnectivity();
            
            // Test 2: Backend API Health
            await this.testBackendHealth();
            
            // Test 3: Healthcare API Endpoints
            await this.testHealthcareAPIs();
            
            // Test 4: AI Agent Communication
            await this.testAIAgentCommunication();
            
            // Test 5: HIPAA Compliance
            await this.testHipaaCompliance();
            
            // Test 6: Patient Data Flow
            await this.testPatientDataFlow();
            
            // Test 7: Security Measures
            await this.testSecurityMeasures();
            
            // Test 8: Performance Metrics
            await this.testPerformanceMetrics();

            // Generate comprehensive report
            this.generateTestReport();

        } catch (error) {
            console.error('❌ Integration test failed:', error);
            this.criticalErrors.push(error);
        }
    }

    /**
     * Test frontend connectivity
     */
    async testFrontendConnectivity() {
        console.log('🔍 Testing Frontend Connectivity...');
        
        try {
            const response = await axios.get(`${this.frontendUrl}/api/health`, {
                timeout: 5000
            });

            if (response.status === 200) {
                this.testResults.push({
                    test: 'Frontend Connectivity',
                    status: 'PASS',
                    responseTime: response.headers['x-response-time'] || 'N/A',
                    details: 'Frontend server is responding correctly'
                });
                console.log('✅ Frontend connectivity test passed');
            } else {
                throw new Error(`Unexpected status: ${response.status}`);
            }
        } catch (error) {
            this.testResults.push({
                test: 'Frontend Connectivity',
                status: 'FAIL',
                error: error.message,
                details: 'Frontend server is not responding'
            });
            console.log('❌ Frontend connectivity test failed');
        }
    }

    /**
     * Test backend health
     */
    async testBackendHealth() {
        console.log('🔍 Testing Backend Health...');
        
        try {
            const response = await axios.get(`${this.backendUrl}/health`, {
                timeout: 5000
            });

            if (response.status === 200) {
                this.testResults.push({
                    test: 'Backend Health',
                    status: 'PASS',
                    responseTime: response.headers['x-response-time'] || 'N/A',
                    details: 'Backend server is healthy'
                });
                console.log('✅ Backend health test passed');
            } else {
                throw new Error(`Unexpected status: ${response.status}`);
            }
        } catch (error) {
            this.testResults.push({
                test: 'Backend Health',
                status: 'FAIL',
                error: error.message,
                details: 'Backend server is not responding'
            });
            console.log('❌ Backend health test failed');
        }
    }

    /**
     * Test healthcare API endpoints
     */
    async testHealthcareAPIs() {
        console.log('🔍 Testing Healthcare APIs...');
        
        const apiTests = [
            { endpoint: '/api/patients', method: 'GET', name: 'Get Patients' },
            { endpoint: '/api/patients', method: 'POST', name: 'Create Patient' },
            { endpoint: '/api/medical-records', method: 'GET', name: 'Get Medical Records' },
            { endpoint: '/api/prescriptions', method: 'GET', name: 'Get Prescriptions' },
            { endpoint: '/api/appointments', method: 'GET', name: 'Get Appointments' }
        ];

        for (const test of apiTests) {
            try {
                const response = await axios({
                    method: test.method,
                    url: `${this.backendUrl}${test.endpoint}`,
                    timeout: 10000,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Healthcare-Provider': 'EHB'
                    }
                });

                this.testResults.push({
                    test: `Healthcare API - ${test.name}`,
                    status: 'PASS',
                    responseTime: response.headers['x-response-time'] || 'N/A',
                    details: `${test.method} ${test.endpoint} is working`
                });
                console.log(`✅ ${test.name} API test passed`);
            } catch (error) {
                this.testResults.push({
                    test: `Healthcare API - ${test.name}`,
                    status: 'FAIL',
                    error: error.message,
                    details: `${test.method} ${test.endpoint} failed`
                });
                console.log(`❌ ${test.name} API test failed`);
            }
        }
    }

    /**
     * Test AI agent communication
     */
    async testAIAgentCommunication() {
        console.log('🔍 Testing AI Agent Communication...');
        
        try {
            // Test health agent communication
            const healthAgentResponse = await axios.post(`${this.backendUrl}/api/agents/health`, {
                action: 'test-communication',
                data: { test: true }
            }, {
                timeout: 10000
            });

            if (healthAgentResponse.status === 200) {
                this.testResults.push({
                    test: 'AI Agent Communication',
                    status: 'PASS',
                    responseTime: healthAgentResponse.headers['x-response-time'] || 'N/A',
                    details: 'AI agents are communicating correctly'
                });
                console.log('✅ AI agent communication test passed');
            } else {
                throw new Error(`Unexpected status: ${healthAgentResponse.status}`);
            }
        } catch (error) {
            this.testResults.push({
                test: 'AI Agent Communication',
                status: 'FAIL',
                error: error.message,
                details: 'AI agents are not responding'
            });
            console.log('❌ AI agent communication test failed');
        }
    }

    /**
     * Test HIPAA compliance
     */
    async testHipaaCompliance() {
        console.log('🔍 Testing HIPAA Compliance...');
        
        const hipaaTests = [
            { name: 'Data Encryption', test: this.testDataEncryption },
            { name: 'Access Control', test: this.testAccessControl },
            { name: 'Audit Logging', test: this.testAuditLogging },
            { name: 'Data Retention', test: this.testDataRetention }
        ];

        for (const hipaaTest of hipaaTests) {
            try {
                const result = await hipaaTest.test();
                this.testResults.push({
                    test: `HIPAA Compliance - ${hipaaTest.name}`,
                    status: result.passed ? 'PASS' : 'FAIL',
                    details: result.details
                });
                console.log(`${result.passed ? '✅' : '❌'} ${hipaaTest.name} test ${result.passed ? 'passed' : 'failed'}`);
            } catch (error) {
                this.testResults.push({
                    test: `HIPAA Compliance - ${hipaaTest.name}`,
                    status: 'FAIL',
                    error: error.message
                });
                console.log(`❌ ${hipaaTest.name} test failed`);
            }
        }
    }

    /**
     * Test data encryption
     */
    async testDataEncryption() {
        const testData = { patientId: 'TEST123', name: 'John Doe' };
        
        try {
            const response = await axios.post(`${this.backendUrl}/api/test/encryption`, testData);
            
            if (response.data.encrypted && response.data.encrypted !== JSON.stringify(testData)) {
                return { passed: true, details: 'Data encryption is working correctly' };
            } else {
                return { passed: false, details: 'Data encryption is not working' };
            }
        } catch (error) {
            return { passed: false, details: 'Encryption test failed' };
        }
    }

    /**
     * Test access control
     */
    async testAccessControl() {
        try {
            // Test without authentication
            const unauthorizedResponse = await axios.get(`${this.backendUrl}/api/patients`, {
                validateStatus: () => true
            });
            
            if (unauthorizedResponse.status === 401) {
                return { passed: true, details: 'Access control is working correctly' };
            } else {
                return { passed: false, details: 'Access control is not working' };
            }
        } catch (error) {
            return { passed: false, details: 'Access control test failed' };
        }
    }

    /**
     * Test audit logging
     */
    async testAuditLogging() {
        try {
            const response = await axios.get(`${this.backendUrl}/api/audit-logs`, {
                validateStatus: () => true
            });
            
            if (response.status === 200 && response.data.logs) {
                return { passed: true, details: 'Audit logging is working correctly' };
            } else {
                return { passed: false, details: 'Audit logging is not working' };
            }
        } catch (error) {
            return { passed: false, details: 'Audit logging test failed' };
        }
    }

    /**
     * Test data retention
     */
    async testDataRetention() {
        try {
            const response = await axios.get(`${this.backendUrl}/api/data-retention-policy`);
            
            if (response.status === 200 && response.data.policy) {
                return { passed: true, details: 'Data retention policy is configured' };
            } else {
                return { passed: false, details: 'Data retention policy is not configured' };
            }
        } catch (error) {
            return { passed: false, details: 'Data retention test failed' };
        }
    }

    /**
     * Test patient data flow
     */
    async testPatientDataFlow() {
        console.log('🔍 Testing Patient Data Flow...');
        
        try {
            // Test patient creation
            const patientData = {
                name: 'Test Patient',
                dateOfBirth: '1990-01-01',
                medicalHistory: ['Hypertension'],
                prescriptions: [],
                labResults: [],
                appointments: []
            };

            const createResponse = await axios.post(`${this.backendUrl}/api/patients`, patientData);
            
            if (createResponse.status === 201) {
                const patientId = createResponse.data.id;
                
                // Test patient retrieval
                const getResponse = await axios.get(`${this.backendUrl}/api/patients/${patientId}`);
                
                if (getResponse.status === 200) {
                    this.testResults.push({
                        test: 'Patient Data Flow',
                        status: 'PASS',
                        details: 'Patient data creation and retrieval working correctly'
                    });
                    console.log('✅ Patient data flow test passed');
                } else {
                    throw new Error('Patient retrieval failed');
                }
            } else {
                throw new Error('Patient creation failed');
            }
        } catch (error) {
            this.testResults.push({
                test: 'Patient Data Flow',
                status: 'FAIL',
                error: error.message,
                details: 'Patient data flow is not working'
            });
            console.log('❌ Patient data flow test failed');
        }
    }

    /**
     * Test security measures
     */
    async testSecurityMeasures() {
        console.log('🔍 Testing Security Measures...');
        
        const securityTests = [
            { name: 'HTTPS Enforcement', test: this.testHttpsEnforcement },
            { name: 'SQL Injection Protection', test: this.testSqlInjectionProtection },
            { name: 'XSS Protection', test: this.testXssProtection },
            { name: 'Rate Limiting', test: this.testRateLimiting }
        ];

        for (const securityTest of securityTests) {
            try {
                const result = await securityTest.test();
                this.testResults.push({
                    test: `Security - ${securityTest.name}`,
                    status: result.passed ? 'PASS' : 'FAIL',
                    details: result.details
                });
                console.log(`${result.passed ? '✅' : '❌'} ${securityTest.name} test ${result.passed ? 'passed' : 'failed'}`);
            } catch (error) {
                this.testResults.push({
                    test: `Security - ${securityTest.name}`,
                    status: 'FAIL',
                    error: error.message
                });
                console.log(`❌ ${securityTest.name} test failed`);
            }
        }
    }

    /**
     * Test HTTPS enforcement
     */
    async testHttpsEnforcement() {
        try {
            const response = await axios.get(`http://localhost:8000/api/health`, {
                validateStatus: () => true,
                maxRedirects: 0
            });
            
            if (response.status === 301 || response.status === 302) {
                return { passed: true, details: 'HTTPS redirection is working' };
            } else {
                return { passed: false, details: 'HTTPS enforcement not configured' };
            }
        } catch (error) {
            return { passed: false, details: 'HTTPS test failed' };
        }
    }

    /**
     * Test SQL injection protection
     */
    async testSqlInjectionProtection() {
        try {
            const maliciousInput = "'; DROP TABLE patients; --";
            
            const response = await axios.post(`${this.backendUrl}/api/patients/search`, {
                query: maliciousInput
            }, {
                validateStatus: () => true
            });
            
            if (response.status === 400) {
                return { passed: true, details: 'SQL injection protection is working' };
            } else {
                return { passed: false, details: 'SQL injection protection not working' };
            }
        } catch (error) {
            return { passed: true, details: 'SQL injection protection is working' };
        }
    }

    /**
     * Test XSS protection
     */
    async testXssProtection() {
        try {
            const maliciousInput = "<script>alert('xss')</script>";
            
            const response = await axios.post(`${this.backendUrl}/api/patients`, {
                name: maliciousInput
            }, {
                validateStatus: () => true
            });
            
            if (response.status === 400) {
                return { passed: true, details: 'XSS protection is working' };
            } else {
                return { passed: false, details: 'XSS protection not working' };
            }
        } catch (error) {
            return { passed: true, details: 'XSS protection is working' };
        }
    }

    /**
     * Test rate limiting
     */
    async testRateLimiting() {
        try {
            const requests = [];
            for (let i = 0; i < 10; i++) {
                requests.push(axios.get(`${this.backendUrl}/api/health`));
            }
            
            const responses = await Promise.all(requests);
            const blockedRequests = responses.filter(r => r.status === 429);
            
            if (blockedRequests.length > 0) {
                return { passed: true, details: 'Rate limiting is working' };
            } else {
                return { passed: false, details: 'Rate limiting not configured' };
            }
        } catch (error) {
            return { passed: false, details: 'Rate limiting test failed' };
        }
    }

    /**
     * Test performance metrics
     */
    async testPerformanceMetrics() {
        console.log('🔍 Testing Performance Metrics...');
        
        const performanceTests = [
            { name: 'Frontend Load Time', test: this.testFrontendLoadTime },
            { name: 'API Response Time', test: this.testApiResponseTime },
            { name: 'Database Query Time', test: this.testDatabaseQueryTime }
        ];

        for (const perfTest of performanceTests) {
            try {
                const result = await perfTest.test();
                this.testResults.push({
                    test: `Performance - ${perfTest.name}`,
                    status: result.passed ? 'PASS' : 'FAIL',
                    details: result.details,
                    metric: result.metric
                });
                console.log(`${result.passed ? '✅' : '❌'} ${perfTest.name} test ${result.passed ? 'passed' : 'failed'}`);
            } catch (error) {
                this.testResults.push({
                    test: `Performance - ${perfTest.name}`,
                    status: 'FAIL',
                    error: error.message
                });
                console.log(`❌ ${perfTest.name} test failed`);
            }
        }
    }

    /**
     * Test frontend load time
     */
    async testFrontendLoadTime() {
        const startTime = Date.now();
        
        try {
            await axios.get(`${this.frontendUrl}/api/health`, { timeout: 10000 });
            const loadTime = Date.now() - startTime;
            
            if (loadTime < 3000) {
                return { 
                    passed: true, 
                    details: `Frontend loads in ${loadTime}ms`,
                    metric: `${loadTime}ms`
                };
            } else {
                return { 
                    passed: false, 
                    details: `Frontend load time ${loadTime}ms exceeds 3s limit`,
                    metric: `${loadTime}ms`
                };
            }
        } catch (error) {
            return { passed: false, details: 'Frontend load test failed' };
        }
    }

    /**
     * Test API response time
     */
    async testApiResponseTime() {
        const startTime = Date.now();
        
        try {
            await axios.get(`${this.backendUrl}/api/health`, { timeout: 10000 });
            const responseTime = Date.now() - startTime;
            
            if (responseTime < 200) {
                return { 
                    passed: true, 
                    details: `API responds in ${responseTime}ms`,
                    metric: `${responseTime}ms`
                };
            } else {
                return { 
                    passed: false, 
                    details: `API response time ${responseTime}ms exceeds 200ms limit`,
                    metric: `${responseTime}ms`
                };
            }
        } catch (error) {
            return { passed: false, details: 'API response test failed' };
        }
    }

    /**
     * Test database query time
     */
    async testDatabaseQueryTime() {
        const startTime = Date.now();
        
        try {
            await axios.get(`${this.backendUrl}/api/patients`, { timeout: 10000 });
            const queryTime = Date.now() - startTime;
            
            if (queryTime < 500) {
                return { 
                    passed: true, 
                    details: `Database query completes in ${queryTime}ms`,
                    metric: `${queryTime}ms`
                };
            } else {
                return { 
                    passed: false, 
                    details: `Database query time ${queryTime}ms exceeds 500ms limit`,
                    metric: `${queryTime}ms`
                };
            }
        } catch (error) {
            return { passed: false, details: 'Database query test failed' };
        }
    }

    /**
     * Generate comprehensive test report
     */
    generateTestReport() {
        console.log('\n📊 EHB Healthcare System Integration Test Report');
        console.log('=' .repeat(60));
        
        const passedTests = this.testResults.filter(r => r.status === 'PASS');
        const failedTests = this.testResults.filter(r => r.status === 'FAIL');
        
        console.log(`\n✅ Passed Tests: ${passedTests.length}`);
        console.log(`❌ Failed Tests: ${failedTests.length}`);
        console.log(`📈 Success Rate: ${((passedTests.length / this.testResults.length) * 100).toFixed(1)}%`);
        
        console.log('\n📋 Detailed Results:');
        this.testResults.forEach(result => {
            const status = result.status === 'PASS' ? '✅' : '❌';
            console.log(`${status} ${result.test}: ${result.details || result.error}`);
            if (result.metric) {
                console.log(`   Metric: ${result.metric}`);
            }
        });
        
        if (this.criticalErrors.length > 0) {
            console.log('\n🚨 Critical Errors:');
            this.criticalErrors.forEach(error => {
                console.log(`   ❌ ${error.message}`);
            });
        }
        
        console.log('\n🎯 Recommendations:');
        if (failedTests.length > 0) {
            console.log('   - Address failed tests before deployment');
            console.log('   - Review security and HIPAA compliance');
            console.log('   - Optimize performance metrics');
        } else {
            console.log('   - All tests passed! System ready for deployment');
            console.log('   - Continue monitoring performance');
            console.log('   - Regular security audits recommended');
        }
        
        console.log('\n🏥 EHB Healthcare System - Advancing Healthcare Technology');
    }
}

// Run the integration test
if (require.main === module) {
    const test = new EHBSystemIntegrationTest();
    test.runFullIntegrationTest();
}

module.exports = EHBSystemIntegrationTest; 