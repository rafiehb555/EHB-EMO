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

// Navigation functionality
function navigateToSection(section) {
    // Hide all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(s => s.style.display = 'none');

    // Show selected section
    const targetSection = document.getElementById(section);
    if (targetSection) {
        targetSection.style.display = 'block';
    }

    // Update active nav link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));

    const activeLink = document.querySelector(`[href="#${section}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Projects navigation
function openProjects() {
    window.location.href = 'projects_section.html';
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

// AI Agent Prompt System
function openAIAgentPrompt() {
    window.location.href = 'ai_agent_prompt_system.html';
}

// Fix popup issues - replace alerts with proper functionality
function runScript() {
    console.log('Running script...');
    // Simulate script execution
    setTimeout(() => {
        updateActivityLog('Script executed successfully');
        showNotification('Script completed successfully!', 'success');
    }, 1000);
}

function loadConfig() {
    console.log('Loading configuration...');
    // Simulate config loading
    setTimeout(() => {
        updateActivityLog('Configuration loaded successfully');
        showNotification('Configuration loaded!', 'success');
    }, 1000);
}

function processData() {
    console.log('Processing data...');
    // Simulate data processing
    setTimeout(() => {
        updateActivityLog('Data processed successfully');
        showNotification('Data processing completed!', 'success');
    }, 1500);
}

function scanFiles() {
    console.log('Scanning files...');
    // Simulate file scanning
    setTimeout(() => {
        updateActivityLog('File scan completed');
        showNotification('File scan completed!', 'success');
    }, 2000);
}

function backupSystem() {
    console.log('Creating backup...');
    // Simulate backup creation
    setTimeout(() => {
        updateActivityLog('System backup created');
        showNotification('Backup created successfully!', 'success');
    }, 3000);
}

function manageApp() {
    console.log('Opening app management...');
    // Simulate app management
    setTimeout(() => {
        updateActivityLog('App management accessed');
        showNotification('App management opened!', 'success');
    }, 1000);
}

function openAIAgents() {
    console.log('Opening AI Agents...');
    window.location.href = 'ai_agents_management_with_main_agent.html';
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

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check' : 'info'}-circle"></i>
            <span>${message}</span>
        </div>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// API Testing functions
function testMainAPI() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            showNotification('API Test: ' + JSON.stringify(data), 'success');
        })
        .catch(error => {
            showNotification('API Test failed: ' + error.message, 'error');
        });
}

function testHealth() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            showNotification('Health Check: ' + JSON.stringify(data), 'success');
        })
        .catch(error => {
            showNotification('Health Check failed: ' + error.message, 'error');
        });
}

function testStatus() {
    fetch('/api/system/status')
        .then(response => response.json())
        .then(data => {
            showNotification('Status Check: ' + JSON.stringify(data), 'success');
        })
        .catch(error => {
            showNotification('Status Check failed: ' + error.message, 'error');
        });
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
window.openAIAgentPrompt = openAIAgentPrompt;
window.runScript = runScript;
window.loadConfig = loadConfig;
window.processData = processData;
window.scanFiles = scanFiles;
window.backupSystem = backupSystem;
window.manageApp = manageApp;
window.openAIAgents = openAIAgents;
window.showNotification = showNotification;
window.testMainAPI = testMainAPI;
window.testHealth = testHealth;
window.testStatus = testStatus;
window.toggleNotifications = toggleNotifications;
window.openProfile = openProfile;
window.navigateToSection = navigateToSection;
window.openProjects = openProjects;

console.log('🎯 EHB-5 Professional Dashboard JavaScript loaded successfully');
