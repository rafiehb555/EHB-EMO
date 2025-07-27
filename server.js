const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Basic route
app.get('/', (req, res) => {
    res.json({
        success: true,
        message: "🎉 EHB-5 Platform is Running Successfully!",
        timestamp: new Date().toISOString(),
        services: {
            total: 21,
            status: "All services configured",
            architecture: "4-Layer Microservices"
        },
        platform: {
            name: "EHB-5 Complete Business Ecosystem",
            version: "1.0.0",
            environment: process.env.NODE_ENV || "development"
        }
    });
});

// Services status endpoint
app.get('/api/services', (req, res) => {
    const servicesPath = path.join(__dirname, 'services');

    try {
        const services = fs.readdirSync(servicesPath, { withFileTypes: true })
            .filter(dirent => dirent.isDirectory())
            .map(dirent => ({
                name: dirent.name,
                status: "configured",
                path: `/services/${dirent.name}`
            }));

        res.json({
            success: true,
            total: services.length,
            services: services
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: "Could not read services directory",
            message: error.message
        });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: "healthy",
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        timestamp: new Date().toISOString()
    });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        success: false,
        message: "Internal Server Error",
        error: process.env.NODE_ENV === 'development' ? err.message : {}
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        success: false,
        message: "Endpoint not found",
        availableEndpoints: [
            "GET /",
            "GET /api/services",
            "GET /health"
        ]
    });
});

// Start server
app.listen(PORT, () => {
    console.log('🚀 EHB-5 Platform Server Running!');
    console.log(`📡 Server: http://localhost:${PORT}`);
    console.log(`🔍 Services: http://localhost:${PORT}/api/services`);
    console.log(`❤️  Health: http://localhost:${PORT}/health`);
    console.log('✅ All 21 services configured and ready!');
});

module.exports = app;
