const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');

// Blockchain Business Record Service for EMO Business Management
class BusinessRecordService {
  constructor() {
    this.records = new Map();
    this.pendingRecords = new Map();
  }

  async createBusinessRecord(businessData) {
    try {
      const recordId = uuidv4();
      const timestamp = new Date().toISOString();
      
      // Create blockchain-ready business record
      const businessRecord = {
        recordId,
        businessId: businessData.businessId,
        data: this.encryptData(businessData.businessData),
        hash: this.generateHash(businessData.businessData),
        timestamp,
        status: 'pending',
        consent: businessData.consent || false,
        accessLevel: businessData.accessLevel || 'restricted'
      };

      // Store in pending records
      this.pendingRecords.set(recordId, businessRecord);

      return {
        success: true,
        recordId,
        hash: businessRecord.hash,
        timestamp,
        message: 'Business record created and pending blockchain confirmation'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async confirmBusinessRecord(recordId) {
    try {
      const record = this.pendingRecords.get(recordId);
      
      if (!record) {
        throw new Error('Record not found in pending records');
      }

      // Simulate blockchain confirmation
      record.status = 'confirmed';
      record.blockchainTx = this.generateTransactionHash();
      record.confirmedAt = new Date().toISOString();

      // Move to confirmed records
      this.records.set(recordId, record);
      this.pendingRecords.delete(recordId);

      return {
        success: true,
        recordId,
        blockchainTx: record.blockchainTx,
        confirmedAt: record.confirmedAt,
        message: 'Business record confirmed on blockchain'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getBusinessRecord(recordId, accessToken) {
    try {
      const record = this.records.get(recordId) || this.pendingRecords.get(recordId);
      
      if (!record) {
        throw new Error('Business record not found');
      }

      // Verify access permissions
      if (!this.verifyAccess(record, accessToken)) {
        throw new Error('Access denied to business record');
      }

      return {
        success: true,
        data: {
          recordId: record.recordId,
          businessId: record.businessId,
          hash: record.hash,
          timestamp: record.timestamp,
          status: record.status,
          blockchainTx: record.blockchainTx,
          confirmedAt: record.confirmedAt
        },
        // Don't return encrypted data directly
        message: 'Business record retrieved successfully'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async updateBusinessRecord(recordId, updates, accessToken) {
    try {
      const record = this.records.get(recordId);
      
      if (!record) {
        throw new Error('Business record not found');
      }

      // Verify access permissions
      if (!this.verifyAccess(record, accessToken)) {
        throw new Error('Access denied to update business record');
      }

      // Create new version
      const newRecordId = uuidv4();
      const updatedRecord = {
        ...record,
        recordId: newRecordId,
        previousVersion: recordId,
        data: this.encryptData(updates.businessData),
        hash: this.generateHash(updates.businessData),
        timestamp: new Date().toISOString(),
        status: 'pending',
        updateReason: updates.reason
      };

      this.pendingRecords.set(newRecordId, updatedRecord);

      return {
        success: true,
        newRecordId,
        previousRecordId: recordId,
        message: 'Business record update created and pending confirmation'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  encryptData(data) {
    // Simplified encryption - in production use proper encryption
    const algorithm = 'aes-256-cbc';
    const key = crypto.scrypt(process.env.ENCRYPTION_KEY || 'default-key', 'salt', 32);
    const iv = crypto.randomBytes(16);
    
    const cipher = crypto.createCipher(algorithm, key);
    let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    return {
      encrypted,
      iv: iv.toString('hex')
    };
  }

  generateHash(data) {
    return crypto.createHash('sha256').update(JSON.stringify(data)).digest('hex');
  }

  generateTransactionHash() {
    return crypto.randomBytes(32).toString('hex');
  }

  verifyAccess(record, accessToken) {
    // Simplified access verification
    // In production, implement proper JWT verification
    return accessToken && accessToken.length > 10;
  }

  async getBusinessRecords(businessId, accessToken) {
    try {
      const businessRecords = [];
      
      // Search in confirmed records
      for (const [recordId, record] of this.records) {
        if (record.businessId === businessId) {
          businessRecords.push({
            recordId: record.recordId,
            timestamp: record.timestamp,
            status: record.status,
            hash: record.hash
          });
        }
      }

      // Search in pending records
      for (const [recordId, record] of this.pendingRecords) {
        if (record.businessId === businessId) {
          businessRecords.push({
            recordId: record.recordId,
            timestamp: record.timestamp,
            status: record.status,
            hash: record.hash
          });
        }
      }

      return {
        success: true,
        data: {
          businessId,
          records: businessRecords,
          totalRecords: businessRecords.length
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

const businessRecordService = new BusinessRecordService();

// Routes
router.post('/create', async (req, res) => {
  try {
    const { businessData } = req.body;
    
    if (!businessData || !businessData.businessId) {
      return res.status(400).json({
        success: false,
        error: 'Business data and businessId are required'
      });
    }

    const result = await businessRecordService.createBusinessRecord(businessData);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.post('/confirm/:recordId', async (req, res) => {
  try {
    const { recordId } = req.params;
    
    const result = await businessRecordService.confirmBusinessRecord(recordId);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.get('/:recordId', async (req, res) => {
  try {
    const { recordId } = req.params;
    const { accessToken } = req.headers;
    
    const result = await businessRecordService.getBusinessRecord(recordId, accessToken);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.put('/:recordId', async (req, res) => {
  try {
    const { recordId } = req.params;
    const { updates, accessToken } = req.body;
    
    const result = await businessRecordService.updateBusinessRecord(recordId, updates, accessToken);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

router.get('/business/:businessId', async (req, res) => {
  try {
    const { businessId } = req.params;
    const { accessToken } = req.headers;
    
    const result = await businessRecordService.getBusinessRecords(businessId, accessToken);
    
    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router; 