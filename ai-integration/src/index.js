const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const { createServer } = require('http');
const { Server } = require('socket.io');
const cron = require('node-cron');

// Load environment variables
dotenv.config();

// Import routes
const authRoutes = require('./routes/auth');
const documentRoutes = require('./routes/documents');
const analysisRoutes = require('./routes/analysis');
const verificationRoutes = require('./routes/verification');
const chatbotRoutes = require('./routes/chatbot');

// Import middleware
const errorHandler = require('./middleware/errorHandler');
const logger = require('./utils/logger');

// Import services
const DocumentService = require('./services/documentService');
const AnalysisService = require('./services/analysisService');
const VerificationService = require('./services/verificationService');
const ChatbotService = require('./services/chatbotService');

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:6000",
    methods: ["GET", "POST"]
  }
});

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
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/emo_ai', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  logger.info('Connected to MongoDB');
})
.catch((error) => {
  logger.error('MongoDB connection error:', error);
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/documents', documentRoutes);
app.use('/api/analysis', analysisRoutes);
app.use('/api/verification', verificationRoutes);
app.use('/api/chatbot', chatbotRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'EMO AI Integration',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// Socket.IO connection handling
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`);

  // Handle document analysis requests
  socket.on('analyze_document', async (data) => {
    try {
      const result = await DocumentService.analyzeDocument(data);
      socket.emit('analysis_result', result);
    } catch (error) {
      socket.emit('analysis_error', { error: error.message });
    }
  });

  // Handle real-time verification updates
  socket.on('verify_document', async (data) => {
    try {
      const result = await VerificationService.verifyDocument(data);
      socket.emit('verification_result', result);
    } catch (error) {
      socket.emit('verification_error', { error: error.message });
    }
  });

  // Handle chatbot messages
  socket.on('chat_message', async (data) => {
    try {
      const response = await ChatbotService.processMessage(data);
      socket.emit('chat_response', response);
    } catch (error) {
      socket.emit('chat_error', { error: error.message });
    }
  });

  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

// Scheduled tasks
cron.schedule('0 2 * * *', async () => {
  // Daily document verification cleanup
  try {
    await DocumentService.cleanupOldDocuments();
    logger.info('Daily document cleanup completed');
  } catch (error) {
    logger.error('Document cleanup error:', error);
  }
});

cron.schedule('0 */6 * * *', async () => {
  // Every 6 hours - AI model updates
  try {
    await AnalysisService.updateModels();
    logger.info('AI models updated');
  } catch (error) {
    logger.error('Model update error:', error);
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

const PORT = process.env.PORT || 5001;

server.listen(PORT, () => {
  logger.info(`EMO AI Integration server running on port ${PORT}`);
  logger.info(`Health check: http://localhost:${PORT}/health`);
  logger.info(`WebSocket server ready for real-time communication`);
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