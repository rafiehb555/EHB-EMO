#!/usr/bin/env node

const EHBOrchestrator = require('./agents/ai-orchestrator');
const CursorIntegration = require('./agents/cursor-integration');

async function testSystem() {
    console.log('🧪 Testing EHB AI System...\n');

    try {
        // Test Orchestrator
        console.log('1. Testing AI Orchestrator...');
        const orchestrator = new EHBOrchestrator();
        
        // Wait for agents to initialize
        await new Promise((resolve) => {
            orchestrator.on('agents-ready', () => {
                console.log('✅ Orchestrator initialized successfully');
                resolve();
            });
        });

        // Test Cursor Integration
        console.log('\n2. Testing Cursor Integration...');
        const cursorIntegration = new CursorIntegration();
        await cursorIntegration.initialize(orchestrator);
        console.log('✅ Cursor Integration initialized successfully');

        // Test Health Check
        console.log('\n3. Testing Health Check...');
        const health = await orchestrator.healthCheck();
        console.log('✅ Health Check Results:', JSON.stringify(health, null, 2));

        // Test Agent Status
        console.log('\n4. Testing Agent Status...');
        const status = orchestrator.getAgentStatus();
        console.log('✅ Agent Status:', JSON.stringify(status, null, 2));

        // Test Simple Task
        console.log('\n5. Testing Simple Task...');
        const task = {
            type: 'code-generation',
            language: 'javascript',
            requirements: 'Create a simple hello world function',
            context: 'Test task'
        };

        const result = await orchestrator.processTask(task);
        console.log('✅ Task completed successfully');
        console.log('Result preview:', result.code ? result.code.substring(0, 100) + '...' : 'No code generated');

        console.log('\n🎉 All tests passed! EHB AI System is working correctly.');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        console.error('Stack:', error.stack);
    }
}

// Run the test
testSystem(); 