const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.AI_PORT || 5001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// AI Services
const verificationService = require('./services/verificationService');
const businessAnalysisService = require('./services/businessAnalysisService');

// Routes
app.use('/api/ai/verification', verificationService);
app.use('/api/ai/business-analysis', businessAnalysisService);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'EMO AI Integration',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`EMO AI Integration Server running on port ${PORT}`);
});

module.exports = app; 