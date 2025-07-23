const request = require('supertest');
const WebSocket = require('ws');
const { IntelligentAPIServer } = require('../intelligent-api-server');

describe('Intelligent API Server', () => {
    let server;
    let app;

    beforeAll(async () => {
        server = new IntelligentAPIServer();
        await server.start();
        app = server.app;
    });

    afterAll(async () => {
        await server.stop();
    });

    describe('Health Check', () => {
        test('should return healthy status', async () => {
            const response = await request(app)
                .get('/health')
                .expect(200);

            expect(response.body).toHaveProperty('status', 'healthy');
            expect(response.body).toHaveProperty('timestamp');
            expect(response.body).toHaveProperty('uptime');
            expect(response.body).toHaveProperty('version', '2.0.0');
        });
    });

    describe('Dashboard API', () => {
        test('should return dashboard data', async () => {
            const response = await request(app)
                .get('/api/v1/dashboard')
                .expect(200);

            expect(response.body).toHaveProperty('metrics');
            expect(response.body).toHaveProperty('agents');
            expect(response.body).toHaveProperty('recentErrors');
            expect(response.body).toHaveProperty('recentRecoveryActions');
            expect(response.body).toHaveProperty('systemStatus');
            expect(response.body).toHaveProperty('timestamp');
        });

        test('should return system metrics', async () => {
            const response = await request(app)
                .get('/api/v1/metrics')
                .expect(200);

            expect(response.body).toHaveProperty('cpu');
            expect(response.body).toHaveProperty('memory');
            expect(response.body).toHaveProperty('network');
            expect(response.body).toHaveProperty('storage');
            expect(response.body).toHaveProperty('uptime');
        });
    });

    describe('AI Agents Management', () => {
        test('should list all agents', async () => {
            const response = await request(app)
                .get('/api/v1/agents')
                .expect(200);

            expect(Array.isArray(response.body)).toBe(true);
            expect(response.body.length).toBeGreaterThan(0);

            const agent = response.body[0];
            expect(agent).toHaveProperty('id');
            expect(agent).toHaveProperty('name');
            expect(agent).toHaveProperty('type');
            expect(agent).toHaveProperty('status');
            expect(agent).toHaveProperty('createdAt');
            expect(agent).toHaveProperty('lastActivity');
            expect(agent).toHaveProperty('metrics');
        });

        test('should create new agent', async () => {
            const agentData = {
                name: 'Test Agent',
                type: 'test',
                config: { status: 'active' }
            };

            const response = await request(app)
                .post('/api/v1/agents')
                .send(agentData)
                .expect(200);

            expect(response.body).toHaveProperty('id');
            expect(response.body.name).toBe(agentData.name);
            expect(response.body.type).toBe(agentData.type);
            expect(response.body.status).toBe('active');
        });

        test('should update agent', async () => {
            // First create an agent
            const createResponse = await request(app)
                .post('/api/v1/agents')
                .send({
                    name: 'Update Test Agent',
                    type: 'test',
                    config: { status: 'inactive' }
                });

            const agentId = createResponse.body.id;

            // Update the agent
            const updateResponse = await request(app)
                .put(`/api/v1/agents/${agentId}`)
                .send({
                    status: 'active',
                    config: { newSetting: 'value' }
                })
                .expect(200);

            expect(updateResponse.body.status).toBe('active');
            expect(updateResponse.body.config).toHaveProperty('newSetting', 'value');
        });

        test('should delete agent', async () => {
            // First create an agent
            const createResponse = await request(app)
                .post('/api/v1/agents')
                .send({
                    name: 'Delete Test Agent',
                    type: 'test'
                });

            const agentId = createResponse.body.id;

            // Delete the agent
            await request(app)
                .delete(`/api/v1/agents/${agentId}`)
                .expect(200);

            // Verify agent is deleted
            const listResponse = await request(app)
                .get('/api/v1/agents');

            const deletedAgent = listResponse.body.find(agent => agent.id === agentId);
            expect(deletedAgent).toBeUndefined();
        });
    });

    describe('Error Management', () => {
        test('should list errors', async () => {
            const response = await request(app)
                .get('/api/v1/errors')
                .expect(200);

            expect(Array.isArray(response.body)).toBe(true);
        });

        test('should resolve error', async () => {
            // First create an error by making an invalid request
            await request(app)
                .get('/api/v1/nonexistent')
                .expect(404);

            // Get the error list
            const errorsResponse = await request(app)
                .get('/api/v1/errors');

            if (errorsResponse.body.length > 0) {
                const errorId = errorsResponse.body[0].id;

                const resolveResponse = await request(app)
                    .post('/api/v1/errors/resolve')
                    .send({ errorId })
                    .expect(200);

                expect(resolveResponse.body).toHaveProperty('resolved', true);
                expect(resolveResponse.body).toHaveProperty('resolvedAt');
            }
        });
    });

    describe('Recovery Actions', () => {
        test('should list recovery actions', async () => {
            const response = await request(app)
                .get('/api/v1/recovery')
                .expect(200);

            expect(Array.isArray(response.body)).toBe(true);
        });

        test('should execute recovery action', async () => {
            // Create a recovery action
            const action = {
                id: 'test-action-id',
                type: 'auto_recovery',
                description: 'Test recovery action',
                command: { type: 'config_reload' },
                status: 'pending',
                createdAt: new Date().toISOString()
            };

            server.recoveryActions.push(action);

            const response = await request(app)
                .post('/api/v1/recovery/execute')
                .send({ actionId: action.id })
                .expect(200);

            expect(response.body).toHaveProperty('status', 'completed');
            expect(response.body).toHaveProperty('result');
        });
    });

    describe('File Operations', () => {
        test('should scan files', async () => {
            const response = await request(app)
                .get('/api/v1/files')
                .expect(200);

            expect(Array.isArray(response.body)).toBe(true);
        });

        test('should process file', async () => {
            const testFilePath = './test-file.txt';
            const fs = require('fs').promises;

            // Create a test file
            await fs.writeFile(testFilePath, 'test content');

            const response = await request(app)
                .post('/api/v1/files/process')
                .send({
                    filePath: testFilePath,
                    action: 'read'
                })
                .expect(200);

            expect(response.body).toHaveProperty('success', true);
            expect(response.body).toHaveProperty('content');

            // Clean up
            await fs.unlink(testFilePath);
        });
    });

    describe('Configuration Management', () => {
        test('should get configuration', async () => {
            const response = await request(app)
                .get('/api/v1/config')
                .expect(200);

            expect(response.body).toBeDefined();
        });

        test('should update configuration', async () => {
            const newConfig = {
                testSetting: 'testValue',
                updatedAt: new Date().toISOString()
            };

            const response = await request(app)
                .put('/api/v1/config')
                .send({ config: newConfig })
                .expect(200);

            expect(response.body).toHaveProperty('success', true);
        });
    });

    describe('System Commands', () => {
        test('should execute system command', async () => {
            const response = await request(app)
                .post('/api/v1/system/command')
                .send({
                    command: 'echo',
                    args: ['test']
                })
                .expect(200);

            expect(response.body).toHaveProperty('success');
            expect(response.body).toHaveProperty('output');
        });
    });

    describe('Auto-Recovery', () => {
        test('should trigger auto-recovery', async () => {
            const response = await request(app)
                .post('/api/v1/recovery/auto')
                .expect(200);

            expect(response.body).toHaveProperty('success', true);
            expect(response.body).toHaveProperty('actionsExecuted');
            expect(response.body).toHaveProperty('actions');
        });
    });

    describe('WebSocket Connections', () => {
        test('should establish WebSocket connection', (done) => {
            const ws = new WebSocket('ws://localhost:3001');

            ws.on('open', () => {
                expect(ws.readyState).toBe(WebSocket.OPEN);
                ws.close();
                done();
            });

            ws.on('error', (error) => {
                done(error);
            });
        });

        test('should receive connection message', (done) => {
            const ws = new WebSocket('ws://localhost:3001');

            ws.on('message', (data) => {
                const message = JSON.parse(data);
                expect(message).toHaveProperty('type', 'connection');
                expect(message).toHaveProperty('clientId');
                expect(message).toHaveProperty('timestamp');
                ws.close();
                done();
            });

            ws.on('error', (error) => {
                done(error);
            });
        });

        test('should handle subscriptions', (done) => {
            const ws = new WebSocket('ws://localhost:3001');

            ws.on('open', () => {
                ws.send(JSON.stringify({
                    type: 'subscribe',
                    subscriptions: ['metrics', 'agents']
                }));
            });

            ws.on('message', (data) => {
                const message = JSON.parse(data);
                if (message.type === 'metrics_update' || message.type === 'agents_update') {
                    ws.close();
                    done();
                }
            });

            ws.on('error', (error) => {
                done(error);
            });
        });

        test('should handle commands', (done) => {
            const ws = new WebSocket('ws://localhost:3001');

            ws.on('open', () => {
                ws.send(JSON.stringify({
                    type: 'command',
                    command: 'getMetrics'
                }));
            });

            ws.on('message', (data) => {
                const message = JSON.parse(data);
                if (message.type === 'response' && message.command === 'getMetrics') {
                    expect(message.result).toHaveProperty('cpu');
                    expect(message.result).toHaveProperty('memory');
                    ws.close();
                    done();
                }
            });

            ws.on('error', (error) => {
                done(error);
            });
        });
    });

    describe('Error Handling', () => {
        test('should handle 404 errors', async () => {
            await request(app)
                .get('/api/v1/nonexistent')
                .expect(404);
        });

        test('should handle invalid JSON', async () => {
            await request(app)
                .post('/api/v1/agents')
                .send('invalid json')
                .set('Content-Type', 'application/json')
                .expect(400);
        });

        test('should handle rate limiting', async () => {
            // Make multiple requests to trigger rate limiting
            const requests = Array(101).fill().map(() =>
                request(app).get('/api/v1/dashboard')
            );

            const responses = await Promise.all(requests);
            const rateLimited = responses.some(res => res.status === 429);
            expect(rateLimited).toBe(true);
        });
    });

    describe('Security', () => {
        test('should have security headers', async () => {
            const response = await request(app)
                .get('/health');

            expect(response.headers).toHaveProperty('x-frame-options');
            expect(response.headers).toHaveProperty('x-content-type-options');
            expect(response.headers).toHaveProperty('x-xss-protection');
        });

        test('should handle CORS', async () => {
            const response = await request(app)
                .get('/health')
                .set('Origin', 'http://localhost:3000');

            expect(response.headers).toHaveProperty('access-control-allow-origin');
        });
    });

    describe('Performance', () => {
        test('should respond within reasonable time', async () => {
            const startTime = Date.now();

            await request(app)
                .get('/health')
                .expect(200);

            const responseTime = Date.now() - startTime;
            expect(responseTime).toBeLessThan(1000); // Should respond within 1 second
        });

        test('should handle concurrent requests', async () => {
            const concurrentRequests = 10;
            const requests = Array(concurrentRequests).fill().map(() =>
                request(app).get('/health')
            );

            const startTime = Date.now();
            const responses = await Promise.all(requests);
            const totalTime = Date.now() - startTime;

            expect(responses.every(res => res.status === 200)).toBe(true);
            expect(totalTime).toBeLessThan(5000); // Should handle 10 requests within 5 seconds
        });
    });

    describe('Integration Tests', () => {
        test('should handle complete workflow', async () => {
            // 1. Check health
            await request(app).get('/health').expect(200);

            // 2. Get dashboard data
            const dashboardResponse = await request(app)
                .get('/api/v1/dashboard')
                .expect(200);

            expect(dashboardResponse.body).toHaveProperty('metrics');

            // 3. Create an agent
            const agentResponse = await request(app)
                .post('/api/v1/agents')
                .send({
                    name: 'Integration Test Agent',
                    type: 'integration',
                    config: { status: 'active' }
                })
                .expect(200);

            const agentId = agentResponse.body.id;

            // 4. Update the agent
            await request(app)
                .put(`/api/v1/agents/${agentId}`)
                .send({ status: 'inactive' })
                .expect(200);

            // 5. Delete the agent
            await request(app)
                .delete(`/api/v1/agents/${agentId}`)
                .expect(200);

            // 6. Trigger auto-recovery
            await request(app)
                .post('/api/v1/recovery/auto')
                .expect(200);
        });
    });
});

describe('IntelligentAPIServer Class', () => {
    let server;

    beforeEach(() => {
        server = new IntelligentAPIServer();
    });

    afterEach(async () => {
        if (server && server.isRunning) {
            await server.stop();
        }
    });

    test('should initialize with default values', () => {
        expect(server.port).toBe(3001);
        expect(server.clients).toBeInstanceOf(Set);
        expect(server.agents).toBeInstanceOf(Map);
        expect(server.errorLog).toBeInstanceOf(Array);
        expect(server.recoveryActions).toBeInstanceOf(Array);
        expect(server.isRunning).toBe(false);
    });

    test('should create agent', async () => {
        const agent = await server.createAgent('Test Agent', 'test', { status: 'active' });

        expect(agent).toHaveProperty('id');
        expect(agent.name).toBe('Test Agent');
        expect(agent.type).toBe('test');
        expect(agent.status).toBe('active');
        expect(server.agents.has(agent.id)).toBe(true);
    });

    test('should update agent', async () => {
        const agent = await server.createAgent('Test Agent', 'test');
        const updatedAgent = await server.updateAgent(agent.id, 'inactive', { newSetting: 'value' });

        expect(updatedAgent.status).toBe('inactive');
        expect(updatedAgent.config).toHaveProperty('newSetting', 'value');
    });

    test('should delete agent', async () => {
        const agent = await server.createAgent('Test Agent', 'test');
        await server.deleteAgent(agent.id);

        expect(server.agents.has(agent.id)).toBe(false);
    });

    test('should log errors', () => {
        const error = server.logError('TEST_ERROR', 'Test error message', 'test context');

        expect(error).toHaveProperty('id');
        expect(error.type).toBe('TEST_ERROR');
        expect(error.message).toBe('Test error message');
        expect(error.context).toBe('test context');
        expect(error.resolved).toBe(false);
        expect(server.errorLog).toContain(error);
    });

    test('should resolve errors', async () => {
        const error = server.logError('TEST_ERROR', 'Test error message');
        const resolvedError = await server.resolveError(error.id);

        expect(resolvedError.resolved).toBe(true);
        expect(resolvedError).toHaveProperty('resolvedAt');
    });

    test('should get system metrics', async () => {
        const metrics = await server.getSystemMetrics();

        expect(metrics).toHaveProperty('cpu');
        expect(metrics).toHaveProperty('memory');
        expect(metrics).toHaveProperty('network');
        expect(metrics).toHaveProperty('storage');
        expect(metrics).toHaveProperty('uptime');
    });

    test('should get system status', () => {
        const status = server.getSystemStatus();

        expect(status).toHaveProperty('database');
        expect(status).toHaveProperty('api');
        expect(status).toHaveProperty('debug');
        expect(status).toHaveProperty('autoRefresh');
        expect(status).toHaveProperty('security');
        expect(status).toHaveProperty('backup');
        expect(status).toHaveProperty('overall');
    });

    test('should execute recovery actions', async () => {
        const action = {
            id: 'test-action',
            type: 'auto_recovery',
            description: 'Test action',
            command: { type: 'config_reload' },
            status: 'pending',
            createdAt: new Date().toISOString()
        };

        server.recoveryActions.push(action);
        const result = await server.executeRecoveryAction(action.id);

        expect(result.status).toBe('completed');
        expect(result).toHaveProperty('result');
    });

    test('should scan files', async () => {
        const files = await server.scanFiles('.');

        expect(Array.isArray(files)).toBe(true);
        files.forEach(file => {
            expect(file).toHaveProperty('name');
            expect(file).toHaveProperty('path');
            expect(file).toHaveProperty('size');
            expect(file).toHaveProperty('modified');
            expect(file).toHaveProperty('type');
        });
    });

    test('should process files', async () => {
        const fs = require('fs').promises;
        const testFile = './test-process-file.txt';

        // Create test file
        await fs.writeFile(testFile, 'test content');

        const result = await server.processFile(testFile, 'read');

        expect(result.success).toBe(true);
        expect(result.content).toBe('test content');

        // Clean up
        await fs.unlink(testFile);
    });

    test('should broadcast events', () => {
        const mockClient = {
            readyState: 1, // WebSocket.OPEN
            send: jest.fn()
        };

        server.clients.add(mockClient);
        server.broadcastEvent('test_event', { data: 'test' });

        expect(mockClient.send).toHaveBeenCalledWith(
            JSON.stringify({
                type: 'test_event',
                data: { data: 'test' },
                timestamp: expect.any(String)
            })
        );
    });
});
