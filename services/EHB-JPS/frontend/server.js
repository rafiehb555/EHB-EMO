const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 8000;

// Serve static files
app.use(express.static('public'));

// JPS routes
app.use('/jps', express.static(path.join(__dirname, 'dist')));

// Serve JPS entry point
app.get('/jps', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'jps.html'));
});

// Proxy API requests to backend
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:3001',
    changeOrigin: true,
    secure: false,
}));

// Default route - serve main project
app.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EHB-5 Platform</title>
            <style>
                body {
                    font-family: 'Inter', sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    padding: 40px;
                    text-align: center;
                    color: white;
                    max-width: 800px;
                    margin: 20px;
                }
                .title {
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 20px;
                }
                .subtitle {
                    font-size: 1.2rem;
                    margin-bottom: 30px;
                    opacity: 0.9;
                }
                .projects {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                .project-card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: all 0.3s ease;
                }
                .project-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
                }
                .project-title {
                    font-size: 1.5rem;
                    font-weight: 600;
                    margin-bottom: 10px;
                }
                .project-description {
                    margin-bottom: 15px;
                    opacity: 0.9;
                }
                .project-button {
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    border: none;
                    border-radius: 25px;
                    padding: 12px 24px;
                    color: white;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                }
                .project-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="title">EHB-5 Platform</h1>
                <p class="subtitle">Advanced AI-Powered Data Processing & Management System</p>

                <div class="projects">
                    <div class="project-card">
                        <div class="project-title">🏢 EHB-JPS</div>
                        <div class="project-description">
                            Advanced Job Portal System with AI-powered features,
                            smart search, and comprehensive job management.
                        </div>
                        <a href="/jps" class="project-button">🚀 Launch JPS</a>
                    </div>

                    <div class="project-card">
                        <div class="project-title">🤖 AI Dashboard</div>
                        <div class="project-description">
                            Advanced AI Platform with quantum computing,
                            BCI interface, and AGI development tools.
                        </div>
                        <a href="/dashboard" class="project-button">🚀 Launch AI Dashboard</a>
                    </div>

                    <div class="project-card">
                        <div class="project-title">💼 Job Portal</div>
                        <div class="project-description">
                            Modern job portal with real-time applications,
                            company profiles, and advanced analytics.
                        </div>
                        <a href="/jobs" class="project-button">🚀 Launch Job Portal</a>
                    </div>
                </div>

                <div style="margin-top: 30px; opacity: 0.8;">
                    <p>EHB-5 Platform - Next Generation AI & Job Management System</p>
                    <p>Powered by React, TypeScript, Node.js & Advanced AI</p>
                </div>
            </div>
        </body>
        </html>
    `);
});

app.listen(PORT, () => {
    console.log(`🚀 EHB-5 Platform Server running on http://localhost:${PORT}`);
    console.log(`🏢 JPS Dashboard available at http://localhost:${PORT}/jps`);
    console.log(`🤖 AI Dashboard available at http://localhost:${PORT}/dashboard`);
});
