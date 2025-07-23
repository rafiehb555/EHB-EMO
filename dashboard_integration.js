// EHB-5 Dashboard Integration with Auto Git Push System

// ===== AUTO PUSH INTEGRATION =====
class AutoPushIntegration {
    constructor() {
        this.apiEndpoint = '/api/agent-task';
        this.taskTypes = {
            'data_processing': 'Data Processing',
            'configuration': 'Configuration Update',
            'security': 'Security Scan',
            'backup': 'Backup Created',
            'optimization': 'Performance Optimization',
            'api_testing': 'API Test'
        };
    }

    // Log agent task completion
    async logAgentTask(taskType, description, data = {}) {
        try {
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    taskType,
                    description,
                    data,
                    timestamp: new Date().toISOString()
                })
            });

            if (response.ok) {
                console.log(`✅ Agent task logged: ${taskType} - ${description}`);
                this.updateTaskHistory(taskType, description);
                return true;
            } else {
                console.error(`❌ Failed to log task: ${response.statusText}`);
                return false;
            }
        } catch (error) {
            console.error(`❌ Error logging task: ${error.message}`);
            return false;
        }
    }

    // Update task history in dashboard
    updateTaskHistory(taskType, description) {
        const taskHistory = document.getElementById('task-history');
        if (taskHistory) {
            const taskItem = document.createElement('div');
            taskItem.className = 'activity-item';
            taskItem.innerHTML = `
                <div class="activity-icon success">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-text">${this.taskTypes[taskType] || taskType}: ${description}</div>
                    <div class="activity-time">Just now</div>
                </div>
            `;

            // Add to top of list
            taskHistory.insertBefore(taskItem, taskHistory.firstChild);

            // Keep only last 10 items
            const items = taskHistory.querySelectorAll('.activity-item');
            if (items.length > 10) {
                items[items.length - 1].remove();
            }
        }
    }

    // Simulate agent tasks for testing
    simulateAgentTasks() {
        const tasks = [
            {
                type: 'data_processing',
                description: 'Processed user analytics data',
                delay: 2000
            },
            {
                type: 'configuration',
                description: 'Updated API settings',
                delay: 4000
            },
            {
                type: 'security',
                description: 'Completed vulnerability scan',
                delay: 6000
            },
            {
                type: 'backup',
                description: 'Created system backup',
                delay: 8000
            },
            {
                type: 'optimization',
                description: 'Optimized database queries',
                delay: 10000
            }
        ];

        tasks.forEach((task, index) => {
            setTimeout(() => {
                this.logAgentTask(task.type, task.description);
            }, task.delay);
        });
    }
}

// ===== DASHBOARD INTEGRATION =====
class DashboardIntegration {
    constructor() {
        this.autoPush = new AutoPushIntegration();
        this.initializeIntegration();
    }

    initializeIntegration() {
        // Add auto-push buttons to dashboard
        this.addAutoPushButtons();

        // Initialize task monitoring
        this.startTaskMonitoring();

        console.log('🚀 Dashboard integration initialized');
    }

    addAutoPushButtons() {
        const actionsGrid = document.querySelector('.actions-grid');
        if (actionsGrid) {
            // Add auto-push test button
            const testButton = document.createElement('button');
            testButton.className = 'action-btn';
            testButton.innerHTML = `
                <i class="fas fa-robot"></i>
                <span>Test Auto-Push</span>
            `;
            testButton.onclick = () => this.testAutoPush();
            actionsGrid.appendChild(testButton);

            // Add simulate tasks button
            const simulateButton = document.createElement('button');
            simulateButton.className = 'action-btn';
            simulateButton.innerHTML = `
                <i class="fas fa-play"></i>
                <span>Simulate Tasks</span>
            `;
            simulateButton.onclick = () => this.autoPush.simulateAgentTasks();
            actionsGrid.appendChild(simulateButton);
        }
    }

    async testAutoPush() {
        const result = await this.autoPush.logAgentTask(
            'api_testing',
            'Dashboard auto-push test completed',
            { source: 'dashboard', test: true }
        );

        if (result) {
            showNotification('Auto-push test successful!', 'success');
        } else {
            showNotification('Auto-push test failed', 'error');
        }
    }

    startTaskMonitoring() {
        // Monitor for new tasks every 30 seconds
        setInterval(() => {
            this.checkForNewTasks();
        }, 30000);
    }

    async checkForNewTasks() {
        try {
            const response = await fetch('/api/tasks/recent');
            if (response.ok) {
                const tasks = await response.json();
                this.updateTaskDisplay(tasks);
            }
        } catch (error) {
            console.log('Task monitoring: No new tasks');
        }
    }

    updateTaskDisplay(tasks) {
        // Update task statistics
        const stats = this.calculateTaskStats(tasks);
        this.updateStatsDisplay(stats);
    }

    calculateTaskStats(tasks) {
        const stats = {
            total: tasks.length,
            byType: {},
            recent: 0
        };

        const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);

        tasks.forEach(task => {
            // Count by type
            stats.byType[task.type] = (stats.byType[task.type] || 0) + 1;

            // Count recent tasks
            if (new Date(task.timestamp) > oneHourAgo) {
                stats.recent++;
            }
        });

        return stats;
    }

    updateStatsDisplay(stats) {
        // Update task count in dashboard
        const taskCountEl = document.getElementById('agents');
        if (taskCountEl) {
            taskCountEl.textContent = stats.total;
        }

        // Update recent activity count
        const recentCountEl = document.getElementById('recent-tasks');
        if (recentCountEl) {
            recentCountEl.textContent = stats.recent;
        }
    }
}

// ===== ENHANCED NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 1000;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// ===== ENHANCED API TESTING =====
async function testMainAPI() {
    const resultEl = document.getElementById('test-result');
    resultEl.style.display = 'block';
    resultEl.className = 'test-result';
    resultEl.textContent = 'Testing main API...';

    try {
        const response = await fetch('https://ehb-5-rafiehb555s-projects.vercel.app/');
        const data = await response.json();

        resultEl.className = 'test-result success';
        resultEl.textContent = JSON.stringify(data, null, 2);

        // Log the API test
        if (window.dashboardIntegration) {
            window.dashboardIntegration.autoPush.logAgentTask(
                'api_testing',
                'Main API test completed successfully',
                { endpoint: '/', status: response.status }
            );
        }
    } catch (error) {
        resultEl.className = 'test-result error';
        resultEl.textContent = `Error: ${error.message}`;
    }
}

async function testHealth() {
    const resultEl = document.getElementById('test-result');
    resultEl.style.display = 'block';
    resultEl.className = 'test-result';
    resultEl.textContent = 'Testing health endpoint...';

    try {
        const response = await fetch('https://ehb-5-rafiehb555s-projects.vercel.app/health');
        const data = await response.json();

        resultEl.className = 'test-result success';
        resultEl.textContent = JSON.stringify(data, null, 2);

        // Log the API test
        if (window.dashboardIntegration) {
            window.dashboardIntegration.autoPush.logAgentTask(
                'api_testing',
                'Health endpoint test completed',
                { endpoint: '/health', status: response.status }
            );
        }
    } catch (error) {
        resultEl.className = 'test-result error';
        resultEl.textContent = `Error: ${error.message}`;
    }
}

async function testStatus() {
    const resultEl = document.getElementById('test-result');
    resultEl.style.display = 'block';
    resultEl.className = 'test-result';
    resultEl.textContent = 'Testing status endpoint...';

    try {
        const response = await fetch('https://ehb-5-rafiehb555s-projects.vercel.app/api/status');
        const data = await response.json();

        resultEl.className = 'test-result success';
        resultEl.textContent = JSON.stringify(data, null, 2);

        // Log the API test
        if (window.dashboardIntegration) {
            window.dashboardIntegration.autoPush.logAgentTask(
                'api_testing',
                'Status endpoint test completed',
                { endpoint: '/api/status', status: response.status }
            );
        }
    } catch (error) {
        resultEl.className = 'test-result error';
        resultEl.textContent = `Error: ${error.message}`;
    }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard integration
    window.dashboardIntegration = new DashboardIntegration();

    console.log('🎯 Dashboard integration loaded successfully');
});

// ===== EXPORT FUNCTIONS =====
window.showNotification = showNotification;
window.testMainAPI = testMainAPI;
window.testHealth = testHealth;
window.testStatus = testStatus;
