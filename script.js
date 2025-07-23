// EHB-5 Professional Dashboard JavaScript

// ===== GLOBAL VARIABLES =====
let currentTheme = 'light';
let notifications = [];
let systemStatus = {
    server: 'online',
    database: 'connected',
    security: 'active',
    agents: 'running'
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 EHB-5 Professional Dashboard Initializing...');

    // Initialize dashboard
    initializeDashboard();

    // Load system data
    loadSystemData();

    // Start real-time updates
    startRealTimeUpdates();

    // Initialize animations
    initializeAnimations();

    console.log('✅ Dashboard initialized successfully');
});

// ===== DASHBOARD INITIALIZATION =====
function initializeDashboard() {
    // Update system stats
    updateSystemStats();

    // Update last updated time
    updateLastUpdated();

    // Initialize navigation
    initializeNavigation();

    // Load initial data
    loadInitialData();
}

// ===== SYSTEM DATA LOADING =====
function loadSystemData() {
    // Simulate loading system data
    setTimeout(() => {
        updateSystemStatus();
        updatePerformanceMetrics();
        updateActivityLog();
    }, 1000);
}

// ===== REAL-TIME UPDATES =====
function startRealTimeUpdates() {
    // Update stats every 30 seconds
    setInterval(updateSystemStats, 30000);

    // Update performance metrics every 10 seconds
    setInterval(updatePerformanceMetrics, 10000);

    // Update activity log every 60 seconds
    setInterval(updateActivityLog, 60000);
}

// ===== ANIMATIONS =====
function initializeAnimations() {
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    document.querySelectorAll('.card, .status-card, .metric-card').forEach(el => {
        observer.observe(el);
    });
}

// ===== NAVIGATION =====
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));

            // Add active class to clicked link
            this.classList.add('active');

            // Smooth scroll to section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== SYSTEM STATS =====
function updateSystemStats() {
    // Simulate real-time data
    const stats = {
        dataFiles: Math.floor(Math.random() * 100) + 50,
        configFiles: Math.floor(Math.random() * 20) + 10,
        scripts: Math.floor(Math.random() * 30) + 15,
        agents: Math.floor(Math.random() * 10) + 5,
        users: Math.floor(Math.random() * 10) + 3,
        uptime: (99.5 + Math.random() * 0.4).toFixed(1)
    };

    // Update DOM elements
    Object.keys(stats).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            element.textContent = stats[key];
        }
    });
}

// ===== SYSTEM STATUS =====
function updateSystemStatus() {
    const statusCards = document.querySelectorAll('.status-card');

    statusCards.forEach(card => {
        const icon = card.querySelector('.status-icon');
        const label = card.querySelector('.status-label');

        if (label && icon) {
            const status = label.textContent.toLowerCase();

            // Update icon color based on status
            if (status.includes('online') || status.includes('connected') || status.includes('active') || status.includes('running')) {
                icon.className = 'status-icon success';
            } else {
                icon.className = 'status-icon error';
            }
        }
    });
}

// ===== PERFORMANCE METRICS =====
function updatePerformanceMetrics() {
    const metrics = [
        { value: (95 + Math.random() * 5).toFixed(1) + '%', label: 'CPU Usage' },
        { value: (2 + Math.random() * 1).toFixed(1) + 'GB', label: 'Memory Used' },
        { value: (40 + Math.random() * 20).toFixed(0) + 'ms', label: 'Response Time' },
        { value: (1 + Math.random() * 2).toFixed(1) + 'K', label: 'Requests/Min' }
    ];

    const metricCards = document.querySelectorAll('.metric-card');

    metricCards.forEach((card, index) => {
        if (metrics[index]) {
            const valueEl = card.querySelector('.metric-value');
            if (valueEl) {
                valueEl.textContent = metrics[index].value;
            }
        }
    });
}

// ===== ACTIVITY LOG =====
function updateActivityLog() {
    const activities = [
        'Script executed successfully',
        'Database backup completed',
        'New user registered',
        'System update applied',
        'Security scan completed',
        'Data processed successfully'
    ];

    const activityList = document.querySelector('.activity-list');
    if (activityList) {
        // Keep only the first 3 activities
        const activityItems = activityList.querySelectorAll('.activity-item');
        if (activityItems.length >= 3) {
            activityItems[activityItems.length - 1].remove();
        }

        // Add new activity at the top
        const newActivity = document.createElement('div');
        newActivity.className = 'activity-item';
        newActivity.innerHTML = `
            <div class="activity-icon success">
                <i class="fas fa-check"></i>
            </div>
            <div class="activity-content">
                <div class="activity-text">${activities[Math.floor(Math.random() * activities.length)]}</div>
                <div class="activity-time">Just now</div>
            </div>
        `;

        activityList.insertBefore(newActivity, activityList.firstChild);
    }
}

// ===== LAST UPDATED =====
function updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const dateString = now.toLocaleDateString();

    const lastUpdatedEl = document.getElementById('lastUpdated');
    if (lastUpdatedEl) {
        lastUpdatedEl.textContent = `${dateString} ${timeString}`;
    }
}

// ===== QUICK ACTIONS =====
function runScript() {
    showNotification('Script execution started...', 'info');
    setTimeout(() => {
        showNotification('Script executed successfully!', 'success');
    }, 2000);
}

function loadConfig() {
    showNotification('Loading configuration...', 'info');
    setTimeout(() => {
        showNotification('Configuration loaded successfully!', 'success');
    }, 1500);
}

function processData() {
    showNotification('Processing data...', 'info');
    setTimeout(() => {
        showNotification('Data processing completed!', 'success');
    }, 3000);
}

function scanFiles() {
    showNotification('Scanning files...', 'info');
    setTimeout(() => {
        showNotification('File scan completed!', 'success');
    }, 2500);
}

function backupSystem() {
    showNotification('Creating backup...', 'info');
    setTimeout(() => {
        showNotification('System backup completed!', 'success');
    }, 4000);
}

function manageApp() {
    showNotification('Opening app management...', 'info');
}

function openAIAgents() {
    showNotification('Opening AI Agents Management...', 'info');
    // Open AI Agents page in new tab
    window.open('ai_agents_management_with_main_agent.html', '_blank');
}

// ===== HERO ACTIONS =====
function quickStart() {
    showNotification('Starting system...', 'info');
    setTimeout(() => {
        showNotification('System started successfully!', 'success');
    }, 2000);
}

function openTutorial() {
    showNotification('Opening tutorial...', 'info');
}

// ===== API TESTING =====
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
    } catch (error) {
        resultEl.className = 'test-result error';
        resultEl.textContent = `Error: ${error.message}`;
    }
}

// ===== NOTIFICATIONS =====
function toggleNotifications() {
    showNotification('Notifications toggled', 'info');
}

function openProfile() {
    showNotification('Opening user profile...', 'info');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add styles
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
    `;

    // Add to page
    document.body.appendChild(notification);

    // Remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// ===== UTILITY FUNCTIONS =====
function loadInitialData() {
    // Simulate loading initial data
    console.log('📊 Loading initial system data...');

    // Update notification count
    const notificationCount = document.querySelector('.notification-count');
    if (notificationCount) {
        notificationCount.textContent = Math.floor(Math.random() * 5) + 1;
    }
}

// ===== CSS ANIMATIONS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .notification {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .notification-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: background 0.2s;
    }

    .notification-close:hover {
        background: rgba(255,255,255,0.2);
    }
`;
document.head.appendChild(style);

// ===== EXPORT FUNCTIONS =====
window.runScript = runScript;
window.loadConfig = loadConfig;
window.processData = processData;
window.scanFiles = scanFiles;
window.backupSystem = backupSystem;
window.manageApp = manageApp;
window.quickStart = quickStart;
window.openTutorial = openTutorial;
window.testMainAPI = testMainAPI;
window.testHealth = testHealth;
window.testStatus = testStatus;
window.toggleNotifications = toggleNotifications;
window.openProfile = openProfile;

console.log('🎯 EHB-5 Professional Dashboard JavaScript loaded successfully');
