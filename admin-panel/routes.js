const express = require('express');
const router = express.Router();
const path = require('path');

// Admin dashboard
router.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// System monitoring
router.get('/monitoring', (req, res) => {
    res.json({
        system: {
            cpu: '45%',
            memory: '60%',
            disk: '35%',
            uptime: '72h 45m'
        },
        agents: {
            active: 12,
            inactive: 3,
            errors: 1
        },
        healthcare: {
            patients: 1250,
            records: 5600,
            lastSync: new Date().toISOString()
        }
    });
});

// User management
router.get('/users', (req, res) => {
    res.json({
        users: [
            { id: 1, name: 'Admin', role: 'administrator', active: true },
            { id: 2, name: 'Doctor', role: 'healthcare_provider', active: true },
            { id: 3, name: 'Nurse', role: 'healthcare_staff', active: true }
        ]
    });
});

// Configuration management
router.get('/config', (req, res) => {
    res.json({
        platform: {
            name: 'EHB-Agent',
            version: '2.0.0',
            environment: 'production'
        },
        features: {
            ai_processing: true,
            healthcare_module: true,
            real_time_monitoring: true,
            automated_deployment: true
        }
    });
});

router.post('/config', (req, res) => {
    res.json({
        message: 'Configuration updated',
        config: req.body
    });
});

module.exports = router;
