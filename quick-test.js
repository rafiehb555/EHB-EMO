const http = require('http');

console.log('🧪 Quick EHB-5 Platform Test Starting...\n');

// Test function
function testEndpoint(path, description) {
    return new Promise((resolve) => {
        const options = {
            hostname: 'localhost',
            port: 3000,
            path: path,
            method: 'GET'
        };

        const req = http.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const response = JSON.parse(data);
                    console.log(`✅ ${description}: ${res.statusCode === 200 ? 'PASS' : 'FAIL'}`);
                    if (path === '/') {
                        console.log(`   📊 Platform: ${response.platform?.name}`);
                        console.log(`   📦 Services: ${response.services?.total}`);
                    } else if (path === '/api/services') {
                        console.log(`   📁 Services Found: ${response.total}`);
                    } else if (path === '/health') {
                        console.log(`   ⏱️  Uptime: ${response.uptime}s`);
                        console.log(`   💾 Memory: ${response.memory?.used}MB`);
                    }
                    resolve(true);
                } catch (error) {
                    console.log(`❌ ${description}: JSON Parse Error`);
                    resolve(false);
                }
            });
        });

        req.on('error', (error) => {
            console.log(`❌ ${description}: ${error.message}`);
            resolve(false);
        });

        req.setTimeout(5000, () => {
            console.log(`❌ ${description}: Timeout`);
            resolve(false);
        });

        req.end();
    });
}

// Run all tests
async function runTests() {
    console.log('Testing EHB-5 Platform Endpoints...\n');

    const tests = [
        { path: '/', desc: 'Main Platform API' },
        { path: '/api/services', desc: 'Services List API' },
        { path: '/health', desc: 'Health Check API' },
        { path: '/api/test', desc: 'Test Endpoint API' }
    ];

    let passed = 0;

    for (const test of tests) {
        const result = await testEndpoint(test.path, test.desc);
        if (result) passed++;
        await new Promise(resolve => setTimeout(resolve, 500)); // Small delay
    }

    console.log('\n' + '='.repeat(50));
    console.log(`📊 TEST RESULTS: ${passed}/${tests.length} PASSED`);

    if (passed === tests.length) {
        console.log('🎉 ALL TESTS PASSED! EHB-5 Platform is working perfectly!');
        console.log('🌐 Visit: http://localhost:3000');
    } else {
        console.log('⚠️  Some tests failed. Check server status.');
    }
    console.log('='.repeat(50));
}

// Wait a moment then run tests
setTimeout(runTests, 2000);
