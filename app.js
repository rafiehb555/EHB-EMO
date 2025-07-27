const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const path = require('path');
require('dotenv').config();

// Import routes
const apiRoutes = require('./api/routes');
const backendRoutes = require('./backend/routes');
const adminRoutes = require('./admin-panel/routes');

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(helmet());
app.use(compression());
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Static files
app.use('/frontend', express.static(path.join(__dirname, 'frontend')));
app.use('/admin', express.static(path.join(__dirname, 'admin-panel')));

// API Routes
app.use('/api', apiRoutes);
app.use('/backend', backendRoutes);
app.use('/admin', adminRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        message: 'EHB-Agent Platform is running',
        timestamp: new Date().toISOString(),
        version: '2.0.0',
        port: PORT
    });
});

// Default route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Something went wrong!',
        message: err.message
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        error: 'Not Found',
        message: 'The requested resource was not found'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 EHB-Agent Platform running on port ${PORT}`);
    console.log(`📊 Admin Panel: http://localhost:${PORT}/admin`);
    console.log(`🔧 API Documentation: http://localhost:${PORT}/api/docs`);
    console.log(`🏥 Healthcare Module: http://localhost:${PORT}/api/healthcare`);
    console.log(`🌐 Main App: http://localhost:${PORT}`);
    console.log(`===============================================`);
});

module.exports = app;
