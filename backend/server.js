const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const winston = require('winston');
const chalk = require('chalk');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Configure logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    service: 'EHB AI Dev Backend',
    version: '2.0.0'
  });
});

// API Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/agents', require('./routes/agents'));
app.use('/api/healthcare', require('./routes/healthcare'));
app.use('/api/dashboard', require('./routes/dashboard')); // New dashboard routes

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error(err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/ehb-ai-dev', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  logger.info(chalk.green('✅ Connected to MongoDB'));
})
.catch((err) => {
  logger.error(chalk.red('❌ MongoDB connection error:'), err);
});

// Start server
app.listen(PORT, () => {
  logger.info(chalk.blue(`🚀 EHB AI Dev Backend running on port ${PORT}`));
  console.log(chalk.green(`\n🎯 Server Status: ONLINE`));
  console.log(chalk.cyan(`📍 URL: http://localhost:${PORT}`));
  console.log(chalk.yellow(`🔍 Health Check: http://localhost:${PORT}/health`));
  console.log(chalk.magenta(`📊 Environment: ${process.env.NODE_ENV || 'development'}`));
  console.log(chalk.blue(`🎛️  Dashboard API: http://localhost:${PORT}/api/dashboard/health`));
  console.log(chalk.green(`\n✅ Phase 2 Backend API Ready!\n`));
});

module.exports = app; 