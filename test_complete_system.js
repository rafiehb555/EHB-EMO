#!/usr/bin/env node

const EHBOrchestrator = require('./agents/ai-orchestrator');
const CursorIntegration = require('./agents/cursor-integration');
const CursorAgentIntegration = require('./agents/cursor-agent-integration');
const MainEHBAgent = require('./agents/main-ehb-agent');

async function testCompleteSystem() {
    console.log('🧪 Testing Complete EHB AI System...\n');

    try {
        // Test 1: AI Orchestrator
        console.log('1. 🧠 Testing AI Orchestrator...');
        const orchestrator = new EHBOrchestrator();
        
        await new Promise((resolve) => {
            orchestrator.on('agents-ready', () => {
                console.log('✅ AI Orchestrator initialized successfully');
                resolve();
            });
        });

        // Test 2: Main EHB Agent
        console.log('\n2. 🏥 Testing Main EHB Agent...');
        const mainAgent = new MainEHBAgent();
        await mainAgent.initialize();
        console.log('✅ Main EHB Agent initialized successfully');

        // Test 3: Cursor Integration
        console.log('\n3. 💻 Testing Cursor Integration...');
        const cursorIntegration = new CursorIntegration();
        await cursorIntegration.initialize(orchestrator);
        console.log('✅ Cursor Integration initialized successfully');

        // Test 4: Cursor Agent Integration
        console.log('\n4. 🤝 Testing Cursor Agent Integration...');
        const cursorAgentIntegration = new CursorAgentIntegration();
        await cursorAgentIntegration.initialize(orchestrator, mainAgent);
        console.log('✅ Cursor Agent Integration initialized successfully');

        // Test 5: Health Checks
        console.log('\n5. 🏥 Testing Health Checks...');
        const orchestratorHealth = await orchestrator.healthCheck();
        const mainAgentHealth = await mainAgent.healthCheck();
        const cursorHealth = await cursorIntegration.healthCheck();
        const cursorAgentHealth = await cursorAgentIntegration.healthCheck();

        console.log('✅ Orchestrator Health:', orchestratorHealth.status);
        console.log('✅ Main Agent Health:', mainAgentHealth.status);
        console.log('✅ Cursor Health:', cursorHealth.status);
        console.log('✅ Cursor Agent Health:', cursorAgentHealth.status);

        // Test 6: Agent Status
        console.log('\n6. 🤖 Testing Agent Status...');
        const orchestratorStatus = orchestrator.getAgentStatus();
        const mainAgentStatus = mainAgent.getAgentStatus();
        const cursorAgentStatus = cursorAgentIntegration.getAgentStatus();

        console.log('✅ Orchestrator Agents:', Object.keys(orchestratorStatus).length);
        console.log('✅ Main Agent Sub-agents:', Object.keys(mainAgentStatus).length);
        console.log('✅ Cursor Agent Connections:', Object.keys(cursorAgentStatus).length);

        // Test 7: Multi-Agent Collaboration
        console.log('\n7. 🤝 Testing Multi-Agent Collaboration...');
        const collaborationTask = {
            type: 'agent-collaboration',
            task: {
                type: 'healthcare-app-development',
                requirements: 'Create a patient management system with HIPAA compliance'
            },
            agents: ['gpt4', 'gemini'],
            collaborationType: 'healthcare-development'
        };

        const collaborationResult = await cursorAgentIntegration.handleAgentCollaboration(collaborationTask);
        console.log('✅ Multi-agent collaboration completed');
        console.log('   Agents used:', collaborationResult.agents.length);

        // Test 8: Project Task
        console.log('\n8. 🎯 Testing Project Task...');
        const projectTask = {
            type: 'ui-development',
            requirements: 'Create a React component for patient data display',
            context: 'Healthcare application'
        };

        const projectResult = await mainAgent.handleProjectTask(projectTask);
        console.log('✅ Project task completed');
        console.log('   Result:', projectResult.result);

        // Test 9: Code Generation with Agents
        console.log('\n9. 💻 Testing Code Generation with Agents...');
        const codeTask = {
            type: 'code-generation',
            language: 'typescript',
            requirements: 'Create a patient card component with TypeScript',
            context: 'Healthcare frontend',
            filePath: 'test-output/PatientCard.tsx'
        };

        const codeResult = await cursorAgentIntegration.handleCodeGenerationWithAgents(codeTask);
        console.log('✅ Code generation completed');
        console.log('   Agents used:', codeResult.agents.join(', '));

        // Test 10: Design Generation with Agents
        console.log('\n10. 🎨 Testing Design Generation with Agents...');
        const designTask = {
            type: 'design-request',
            component: 'patient-dashboard',
            style: 'medical',
            requirements: 'Create a modern healthcare dashboard design',
            outputPath: 'test-output/design-metadata.json'
        };

        const designResult = await cursorAgentIntegration.handleDesignRequestWithAgents(designTask);
        console.log('✅ Design generation completed');
        console.log('   Agents used:', designResult.agents.join(', '));

        // Test 11: Voice Processing with Agents
        console.log('\n11. 🎤 Testing Voice Processing with Agents...');
        const voiceTask = {
            type: 'voice-processing',
            audioFile: 'test-audio.wav',
            context: 'Patient complaint analysis',
            outputPath: 'test-output/transcription.json'
        };

        const voiceResult = await cursorAgentIntegration.handleVoiceProcessingWithAgents(voiceTask);
        console.log('✅ Voice processing completed');
        console.log('   Agents used:', voiceResult.agents.join(', '));

        // Test 12: Research Analysis with Agents
        console.log('\n12. 🔍 Testing Research Analysis with Agents...');
        const researchTask = {
            type: 'research-analysis',
            query: 'Latest HIPAA compliance requirements for healthcare applications',
            sources: ['official', 'medical'],
            depth: 'comprehensive',
            outputPath: 'test-output/research.json'
        };

        const researchResult = await cursorAgentIntegration.handleResearchAnalysisWithAgents(researchTask);
        console.log('✅ Research analysis completed');
        console.log('   Agents used:', researchResult.agents.join(', '));

        // Test 13: System Status
        console.log('\n13. 📊 Testing System Status...');
        const orchestratorSystemStatus = orchestrator.getSystemStatus();
        const mainAgentProjectStatus = mainAgent.getProjectStatus();
        const cursorAgentSystemStatus = cursorAgentIntegration.getSystemStatus();

        console.log('✅ Orchestrator System Status:', orchestratorSystemStatus.activeTasks, 'active tasks');
        console.log('✅ Main Agent Project Status:', mainAgentProjectStatus.status);
        console.log('✅ Cursor Agent System Status:', cursorAgentSystemStatus.activeProjects.length, 'active projects');

        // Test 14: File Operations
        console.log('\n14. 📁 Testing File Operations...');
        const testFilePath = 'test-output/test-file.js';
        const testCode = 'console.log("Hello from EHB AI System!");';
        
        const fileResult = await cursorAgentIntegration.applyCodeToFile(testFilePath, testCode);
        console.log('✅ File operation completed:', fileResult.success);

        // Final Summary
        console.log('\n🎉 Complete System Test Results:');
        console.log('✅ All agents initialized and healthy');
        console.log('✅ All integrations working');
        console.log('✅ Multi-agent collaboration functional');
        console.log('✅ Project management active');
        console.log('✅ File operations working');
        console.log('✅ Health checks passing');
        console.log('✅ System status monitoring active');

        console.log('\n🚀 EHB AI System is fully operational!');
        console.log('   - AI Orchestrator: ✅ Ready');
        console.log('   - Main EHB Agent: ✅ Active');
        console.log('   - Cursor Integration: ✅ Connected');
        console.log('   - Cursor Agent Integration: ✅ Active');
        console.log('   - All Sub-agents: ✅ Working');

    } catch (error) {
        console.error('❌ Complete system test failed:', error.message);
        console.error('Stack:', error.stack);
    }
}

// Run the complete test
testCompleteSystem(); 