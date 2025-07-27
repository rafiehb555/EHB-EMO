const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const { createServer } = require('http');
const { Server } = require('socket.io');
const cron = require('node-cron');
const Web3 = require('web3');
const { ethers } = require('ethers');

// Load environment variables
dotenv.config();

// Import routes
const authRoutes = require('./routes/auth');
const verificationRoutes = require('./routes/verification');
const auditRoutes = require('./routes/audit');
const contractRoutes = require('./routes/contracts');

// Import middleware
const errorHandler = require('./middleware/errorHandler');
const logger = require('./utils/logger');

// Import services
const BlockchainService = require('./services/blockchainService');
const VerificationService = require('./services/verificationService');
const AuditService = require('./services/auditService');
const ContractService = require('./services/contractService');

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:6000",
    methods: ["GET", "POST"]
  }
});

// Initialize Web3
const web3 = new Web3(process.env.ETHEREUM_RPC_URL || 'http://localhost:8545');
const provider = new ethers.providers.JsonRpcProvider(process.env.ETHEREUM_RPC_URL || 'http://localhost:8545');

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:6000",
  credentials: true
}));
app.use(morgan('combined'));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/emo_blockchain', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  logger.info('Connected to MongoDB');
})
.catch((error) => {
  logger.error('MongoDB connection error:', error);
});

// Initialize blockchain services
const blockchainService = new BlockchainService(web3, provider);
const verificationService = new VerificationService(blockchainService);
const auditService = new AuditService(blockchainService);
const contractService = new ContractService(web3, provider);

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/verification', verificationRoutes);
app.use('/api/audit', auditRoutes);
app.use('/api/contracts', contractRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'EMO Blockchain',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    network: process.env.ETHEREUM_NETWORK || 'localhost',
    contractAddress: process.env.CONTRACT_ADDRESS || 'Not deployed'
  });
});

// Blockchain status endpoint
app.get('/api/blockchain/status', async (req, res) => {
  try {
    const status = await blockchainService.getNetworkStatus();
    res.json({
      success: true,
      status
    });
  } catch (error) {
    logger.error('Blockchain status error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get blockchain status'
    });
  }
});

// Socket.IO connection handling
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`);

  // Handle document verification requests
  socket.on('verify_document', async (data) => {
    try {
      const result = await verificationService.verifyDocumentOnChain(data);
      socket.emit('verification_result', result);
    } catch (error) {
      socket.emit('verification_error', { error: error.message });
    }
  });

  // Handle audit trail requests
  socket.on('get_audit_trail', async (data) => {
    try {
      const trail = await auditService.getAuditTrail(data);
      socket.emit('audit_trail_result', trail);
    } catch (error) {
      socket.emit('audit_trail_error', { error: error.message });
    }
  });

  // Handle contract events
  socket.on('subscribe_contract_events', async (data) => {
    try {
      const events = await contractService.subscribeToEvents(data);
      socket.emit('contract_events', events);
    } catch (error) {
      socket.emit('contract_events_error', { error: error.message });
    }
  });

  // Handle real-time blockchain updates
  socket.on('get_blockchain_updates', async () => {
    try {
      const updates = await blockchainService.getLatestUpdates();
      socket.emit('blockchain_updates', updates);
    } catch (error) {
      socket.emit('blockchain_updates_error', { error: error.message });
    }
  });

  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

// Scheduled tasks
cron.schedule('0 */10 * * * *', async () => {
  // Every 10 minutes - Sync blockchain data
  try {
    await blockchainService.syncBlockchainData();
    logger.info('Blockchain data synced');
  } catch (error) {
    logger.error('Blockchain sync error:', error);
  }
});

cron.schedule('0 2 * * *', async () => {
  // Daily - Clean up old audit logs
  try {
    await auditService.cleanupOldLogs();
    logger.info('Old audit logs cleaned up');
  } catch (error) {
    logger.error('Audit cleanup error:', error);
  }
});

cron.schedule('0 */30 * * * *', async () => {
  // Every 30 minutes - Check contract health
  try {
    const health = await contractService.checkContractHealth();
    if (!health.isHealthy) {
      logger.warn('Contract health check failed:', health.issues);
    }
  } catch (error) {
    logger.error('Contract health check error:', error);
  }
});

// Error handling middleware
app.use(errorHandler);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    error: 'Route not found'
  });
});

const PORT = process.env.PORT || 5002;

server.listen(PORT, () => {
  logger.info(`EMO Blockchain server running on port ${PORT}`);
  logger.info(`Health check: http://localhost:${PORT}/health`);
  logger.info(`Blockchain network: ${process.env.ETHEREUM_NETWORK || 'localhost'}`);
  logger.info(`Contract address: ${process.env.CONTRACT_ADDRESS || 'Not deployed'}`);
  logger.info(`WebSocket server ready for real-time blockchain updates`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  server.close(() => {
    logger.info('Process terminated');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully');
  server.close(() => {
    logger.info('Process terminated');
    process.exit(0);
  });
});

module.exports = app; 