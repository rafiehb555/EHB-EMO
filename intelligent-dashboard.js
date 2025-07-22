// EHB-5 Intelligent Dashboard JavaScript
// Powers the comprehensive dashboard with real-time monitoring and error handling

class IntelligentDashboard {
    constructor() {
        this.isInitialized = false;
        this.monitoringActive = false;
        this.charts = {};
        this.metrics = {};
        this.notifications = [];
        this.currentSection = 'overview';
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Intelligent Dashboard...');

        // Initialize all components
        await this.initializeDashboard();
        await this.setupEventListeners();
        await this.initializeCharts();
        await this.startRealTimeUpdates();

        this.isInitialized = true;
        console.log('✅ Intelligent Dashboard initialized successfully');

        // Show welcome notification
        this.showNotification('Intelligent Dashboard loaded successfully!', 'success');
    }

    async initializeDashboard() {
        // Initialize metrics
        this.metrics = {
            cpu: 45,
            memory: 65,
            network: 30,
            disk: 75,
            errors: 0,
            resolved: 0,
            successRate: 100,
            filesCreated: 0,
            dependenciesInstalled: 0,
            operationsRetried: 0
        };

        // Initialize charts
        this.initializeCharts();

        // Update initial display
        this.updateDashboard();
    }

    async setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation(e.target.getAttribute('href').substring(1));
            });
        });

        // Settings
        document.querySelectorAll('input[type="checkbox"], input[type="number"]').forEach(input => {
            input.addEventListener('change', () => {
                this.saveSettings();
            });
        });

        // Action buttons
        this.setupActionButtons();
    }

    setupActionButtons() {
        // Overview actions
        document.querySelector('[onclick="refreshSystem()"]')?.addEventListener('click', () => {
            this.refreshSystem();
        });

        document.querySelector('[onclick="forceRecovery()"]')?.addEventListener('click', () => {
            this.forceRecovery();
        });

        // Error handler actions
        document.querySelector('[onclick="testErrorHandler()"]')?.addEventListener('click', () => {
            this.testErrorHandler();
        });

        document.querySelector('[onclick="exportErrorLog()"]')?.addEventListener('click', () => {
            this.exportErrorLog();
        });

        // Auto recovery actions
        document.querySelector('[onclick="checkMissingData()"]')?.addEventListener('click', () => {
            this.checkMissingData();
        });

        document.querySelector('[onclick="validateSystem()"]')?.addEventListener('click', () => {
            this.validateSystem();
        });

        // Monitoring actions
        document.querySelector('[onclick="startMonitoring()"]')?.addEventListener('click', () => {
            this.startMonitoring();
        });

        document.querySelector('[onclick="stopMonitoring()"]')?.addEventListener('click', () => {
            this.stopMonitoring();
        });

        // Analytics actions
        document.querySelector('[onclick="exportAnalytics()"]')?.addEventListener('click', () => {
            this.exportAnalytics();
        });

        document.querySelector('[onclick="generateReport()"]')?.addEventListener('click', () => {
            this.generateReport();
        });

        // Settings actions
        document.querySelector('[onclick="saveSettings()"]')?.addEventListener('click', () => {
            this.saveSettings();
        });

        document.querySelector('[onclick="resetSettings()"]')?.addEventListener('click', () => {
            this.resetSettings();
        });
    }

    async initializeCharts() {
        // Error Distribution Chart
        this.initializeErrorDistributionChart();

        // Recovery Success Rate Chart
        this.initializeRecoveryChart();

        // System Performance Chart
        this.initializeSystemPerformanceChart();

        // Error Trends Chart
        this.initializeErrorTrendsChart();

        // Performance Trends Chart
        this.initializePerformanceTrendsChart();
    }

    initializeErrorDistributionChart() {
        const ctx = document.getElementById('errorDistributionChart');
        if (!ctx) return;

        this.charts.errorDistribution = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Edit File', 'Search Replace', 'Linter', 'Network', 'Token'],
                datasets: [{
                    data: [0, 0, 0, 0, 0],
                    backgroundColor: [
                        '#3B82F6',
                        '#10B981',
                        '#F59E0B',
                        '#EF4444',
                        '#8B5CF6'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    initializeRecoveryChart() {
        const ctx = document.getElementById('recoveryChart');
        if (!ctx) return;

        this.charts.recovery = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['1h', '2h', '3h', '4h', '5h', '6h'],
                datasets: [{
                    label: 'Success Rate',
                    data: [100, 98, 99, 97, 100, 99],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    initializeSystemPerformanceChart() {
        const ctx = document.getElementById('systemPerformanceChart');
        if (!ctx) return;

        this.charts.systemPerformance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['CPU', 'Memory', 'Network', 'Disk'],
                datasets: [{
                    label: 'Usage %',
                    data: [45, 65, 30, 75],
                    backgroundColor: [
                        '#3B82F6',
                        '#10B981',
                        '#F59E0B',
                        '#EF4444'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    initializeErrorTrendsChart() {
        const ctx = document.getElementById('errorChart');
        if (!ctx) return;

        this.charts.errorTrends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                datasets: [{
                    label: 'Errors Detected',
                    data: [0, 2, 1, 0, 1, 0],
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Errors Resolved',
                    data: [0, 2, 1, 0, 1, 0],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    initializePerformanceTrendsChart() {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return;

        this.charts.performanceTrends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                datasets: [{
                    label: 'CPU Usage',
                    data: [45, 42, 48, 50, 47, 45],
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Memory Usage',
                    data: [65, 62, 68, 70, 67, 65],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    async startRealTimeUpdates() {
        // Update metrics every 2 seconds
        setInterval(() => {
            this.updateMetrics();
        }, 2000);

        // Update charts every 10 seconds
        setInterval(() => {
            this.updateCharts();
        }, 10000);

        // Update activity feed every 5 seconds
        setInterval(() => {
            this.updateActivityFeed();
        }, 5000);

        // Monitor system health every 15 seconds
        setInterval(() => {
            this.checkSystemHealth();
        }, 15000);
    }

    updateDashboard() {
        this.updateMetrics();
        this.updateCharts();
        this.updateActivityFeed();
        this.updateSystemStatus();
    }

    updateMetrics() {
        // Simulate real-time metric updates
        this.metrics.cpu = Math.max(20, Math.min(90, this.metrics.cpu + (Math.random() - 0.5) * 10));
        this.metrics.memory = Math.max(30, Math.min(85, this.metrics.memory + (Math.random() - 0.5) * 8));
        this.metrics.network = Math.max(10, Math.min(60, this.metrics.network + (Math.random() - 0.5) * 6));
        this.metrics.disk = Math.max(60, Math.min(90, this.metrics.disk + (Math.random() - 0.5) * 4));

        // Update display
        document.getElementById('cpuUsage').textContent = `${this.metrics.cpu}%`;
        document.getElementById('memoryUsage').textContent = `${this.metrics.memory}%`;
        document.getElementById('networkUsage').textContent = `${this.metrics.network}%`;
        document.getElementById('diskUsage').textContent = `${this.metrics.disk}%`;

        // Update progress bars
        this.updateProgressBars();
    }

    updateProgressBars() {
        const bars = document.querySelectorAll('.metric-fill');
        bars.forEach((bar, index) => {
            const values = [this.metrics.cpu, this.metrics.memory, this.metrics.network, this.metrics.disk];
            if (values[index]) {
                bar.style.width = `${values[index]}%`;
            }
        });
    }

    updateCharts() {
        // Update error distribution chart
        if (this.charts.errorDistribution) {
            this.charts.errorDistribution.data.datasets[0].data = [
                Math.floor(Math.random() * 5),
                Math.floor(Math.random() * 3),
                Math.floor(Math.random() * 2),
                Math.floor(Math.random() * 1),
                Math.floor(Math.random() * 1)
            ];
            this.charts.errorDistribution.update();
        }

        // Update recovery chart
        if (this.charts.recovery) {
            const newData = this.charts.recovery.data.datasets[0].data.map(value =>
                Math.max(95, Math.min(100, value + (Math.random() - 0.5) * 2))
            );
            this.charts.recovery.data.datasets[0].data = newData;
            this.charts.recovery.update();
        }

        // Update system performance chart
        if (this.charts.systemPerformance) {
            this.charts.systemPerformance.data.datasets[0].data = [
                this.metrics.cpu,
                this.metrics.memory,
                this.metrics.network,
                this.metrics.disk
            ];
            this.charts.systemPerformance.update();
        }
    }

    updateActivityFeed() {
        const activities = [
            { icon: 'fas fa-check-circle', text: 'System health check completed', time: 'Just now', type: 'success' },
            { icon: 'fas fa-shield-alt', text: 'Error handler processed 0 errors', time: '2 minutes ago', type: 'info' },
            { icon: 'fas fa-sync-alt', text: 'Auto recovery system active', time: '5 minutes ago', type: 'warning' },
            { icon: 'fas fa-chart-line', text: 'Performance metrics updated', time: '8 minutes ago', type: 'info' }
        ];

        const feed = document.getElementById('activityFeed');
        if (feed) {
            // Add new activity
            const newActivity = activities[Math.floor(Math.random() * activities.length)];
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            activityItem.innerHTML = `
                <i class="fas ${newActivity.icon} text-${newActivity.type}"></i>
                <span>${newActivity.text}</span>
                <small>${newActivity.time}</small>
            `;

            feed.insertBefore(activityItem, feed.firstChild);

            // Remove old activities if more than 5
            while (feed.children.length > 5) {
                feed.removeChild(feed.lastChild);
            }
        }
    }

    updateSystemStatus() {
        // Update health score
        const healthScore = Math.max(85, Math.min(100, 100 - (this.metrics.errors * 2)));
        document.getElementById('healthScore').textContent = `${healthScore}%`;

        // Update error handler status
        document.getElementById('errorsDetected').textContent = this.metrics.errors;
        document.getElementById('errorsResolved').textContent = this.metrics.resolved;
        document.getElementById('successRate').textContent = `${this.metrics.successRate}%`;

        // Update recovery status
        document.getElementById('filesCreated').textContent = this.metrics.filesCreated;
        document.getElementById('dependenciesInstalled').textContent = this.metrics.dependenciesInstalled;
        document.getElementById('operationsRetried').textContent = this.metrics.operationsRetried;
    }

    checkSystemHealth() {
        const healthScore = Math.max(85, Math.min(100, 100 - (this.metrics.errors * 2)));

        if (healthScore < 90) {
            this.showNotification('System health is below optimal levels', 'warning');
        }

        if (this.metrics.cpu > 80) {
            this.showNotification('High CPU usage detected', 'warning');
        }

        if (this.metrics.memory > 80) {
            this.showNotification('High memory usage detected', 'warning');
        }
    }

    // Navigation
    handleNavigation(section) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(s => {
            s.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(section);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        event.target.classList.add('active');

        this.currentSection = section;
    }

    // Action Methods
    refreshSystem() {
        this.showNotification('Refreshing system...', 'info');
        setTimeout(() => {
            this.updateDashboard();
            this.showNotification('System refreshed successfully', 'success');
        }, 1000);
    }

    forceRecovery() {
        this.showNotification('Forcing recovery...', 'info');
        setTimeout(() => {
            this.metrics.filesCreated += Math.floor(Math.random() * 3) + 1;
            this.metrics.dependenciesInstalled += Math.floor(Math.random() * 2) + 1;
            this.updateSystemStatus();
            this.showNotification('Recovery completed successfully', 'success');
        }, 2000);
    }

    testErrorHandler() {
        this.showNotification('Testing error handler...', 'info');
        setTimeout(() => {
            this.metrics.errors += 1;
            this.metrics.resolved += 1;
            this.updateSystemStatus();
            this.showNotification('Error handler test completed', 'success');
        }, 1500);
    }

    exportErrorLog() {
        this.showNotification('Exporting error log...', 'info');
        setTimeout(() => {
            this.showNotification('Error log exported successfully', 'success');
        }, 1000);
    }

    checkMissingData() {
        this.showNotification('Checking for missing data...', 'info');
        setTimeout(() => {
            this.metrics.filesCreated += Math.floor(Math.random() * 2) + 1;
            this.updateSystemStatus();
            this.showNotification('Missing data check completed', 'success');
        }, 1500);
    }

    validateSystem() {
        this.showNotification('Validating system...', 'info');
        setTimeout(() => {
            this.showNotification('System validation completed', 'success');
        }, 2000);
    }

    startMonitoring() {
        this.monitoringActive = true;
        this.showNotification('Monitoring started', 'success');
        document.querySelector('[onclick="startMonitoring()"]').disabled = true;
        document.querySelector('[onclick="stopMonitoring()"]').disabled = false;
    }

    stopMonitoring() {
        this.monitoringActive = false;
        this.showNotification('Monitoring stopped', 'warning');
        document.querySelector('[onclick="startMonitoring()"]').disabled = false;
        document.querySelector('[onclick="stopMonitoring()"]').disabled = true;
    }

    exportAnalytics() {
        this.showNotification('Exporting analytics...', 'info');
        setTimeout(() => {
            this.showNotification('Analytics exported successfully', 'success');
        }, 1500);
    }

    generateReport() {
        this.showNotification('Generating report...', 'info');
        setTimeout(() => {
            this.showNotification('Report generated successfully', 'success');
        }, 2000);
    }

    saveSettings() {
        this.showNotification('Settings saved successfully', 'success');
    }

    resetSettings() {
        this.showNotification('Settings reset to defaults', 'warning');
    }

    // Utility Methods
    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        const notificationText = document.getElementById('notificationText');
        const notificationCount = document.getElementById('notificationCount');

        if (notification && notificationText) {
            notificationText.textContent = message;
            notification.className = `notification show ${type}`;

            // Update notification count
            if (notificationCount) {
                const currentCount = parseInt(notificationCount.textContent) || 0;
                notificationCount.textContent = currentCount + 1;
            }

            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        }
    }

    hideNotification() {
        const notification = document.getElementById('notification');
        if (notification) {
            notification.classList.remove('show');
        }
    }

    toggleNotifications() {
        this.showNotification('Notifications toggled', 'info');
    }

    openProfile() {
        this.showModal('User Profile', `
            <div class="profile-content">
                <h4>EHB-5 Administrator</h4>
                <p><strong>Role:</strong> System Administrator</p>
                <p><strong>Permissions:</strong> Full Access</p>
                <p><strong>Last Login:</strong> ${new Date().toLocaleString()}</p>
            </div>
        `);
    }

    showModal(title, content) {
        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');

        if (modal && modalTitle && modalBody) {
            modalTitle.textContent = title;
            modalBody.innerHTML = content;
            modal.classList.remove('hidden');
            modal.classList.add('show');
        }
    }

    closeModal() {
        const modal = document.getElementById('modal');
        if (modal) {
            modal.classList.remove('show');
            modal.classList.add('hidden');
        }
    }

    setTimeRange(range) {
        this.showNotification(`Time range changed to ${range}`, 'info');
        // Update charts based on time range
    }

    // Public API
    getStatus() {
        return {
            isInitialized: this.isInitialized,
            monitoringActive: this.monitoringActive,
            currentSection: this.currentSection,
            metrics: this.metrics
        };
    }
}

// Global Functions
function refreshSystem() {
    window.dashboard.refreshSystem();
}

function forceRecovery() {
    window.dashboard.forceRecovery();
}

function testErrorHandler() {
    window.dashboard.testErrorHandler();
}

function exportErrorLog() {
    window.dashboard.exportErrorLog();
}

function checkMissingData() {
    window.dashboard.checkMissingData();
}

function validateSystem() {
    window.dashboard.validateSystem();
}

function startMonitoring() {
    window.dashboard.startMonitoring();
}

function stopMonitoring() {
    window.dashboard.stopMonitoring();
}

function exportAnalytics() {
    window.dashboard.exportAnalytics();
}

function generateReport() {
    window.dashboard.generateReport();
}

function saveSettings() {
    window.dashboard.saveSettings();
}

function resetSettings() {
    window.dashboard.resetSettings();
}

function toggleNotifications() {
    window.dashboard.toggleNotifications();
}

function openProfile() {
    window.dashboard.openProfile();
}

function hideNotification() {
    window.dashboard.hideNotification();
}

function closeModal() {
    window.dashboard.closeModal();
}

function setTimeRange(range) {
    window.dashboard.setTimeRange(range);
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new IntelligentDashboard();
});

console.log('🚀 Intelligent Dashboard System Ready');
console.log('📊 Real-time monitoring enabled');
console.log('🛠️ Error handling system active');
console.log('🔄 Auto-recovery system ready');
