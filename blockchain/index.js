const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();
const PORT = process.env.BLOCKCHAIN_PORT || 5002;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Blockchain Services
const businessRecordService = require('./services/healthRecordService');
const consentService = require('./services/consentService');
const auditService = require('./services/auditService');

// Routes
app.use('/api/blockchain/business-records', businessRecordService);
app.use('/api/blockchain/consent', consentService);
app.use('/api/blockchain/audit', auditService);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'EMO Blockchain Integration',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`EMO Blockchain Integration Server running on port ${PORT}`);
});

module.exports = app; 