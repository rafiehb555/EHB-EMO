const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');

// Blockchain Consent Service for EMO Healthcare Platform
class ConsentService {
  constructor() {
    this.consents = new Map();
    this.pendingConsents = new Map();
  }

  async createConsent(consentData) {
    try {
      const consentId = uuidv4();
      const timestamp = new Date().toISOString();
      
      // Create blockchain-ready consent record
      const consent = {
        consentId,
        patientId: consentData.patientId,
        providerId: consentData.providerId,
        dataTypes: consentData.dataTypes || [],
        accessLevel: consentData.accessLevel || 'limited',
        duration: consentData.duration || '1 year',
        status: 'pending',
        timestamp,
        hash: this.generateHash(consentData),
        revocable: consentData.revocable !== false,
        purpose: consentData.purpose || 'Healthcare treatment'
      };

      // Store in pending consents
      this.pendingConsents.set(consentId, consent);

      return {
        success: true,
        consentId,
        hash: consent.hash,
        timestamp,
        message: 'Consent created and pending blockchain confirmation'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async confirmConsent(consentId) {
    try {
      const consent = this.pendingConsents.get(consentId);
      
      if (!consent) {
        throw new Error('Consent not found in pending consents');
      }

      // Simulate blockchain confirmation
      consent.status = 'active';
      consent.blockchainTx = this.generateTransactionHash();
      consent.confirmedAt = new Date().toISOString();
      consent.expiresAt = this.calculateExpiryDate(consent.duration);

      // Move to active consents
      this.consents.set(consentId, consent);
      this.pendingConsents.delete(consentId);

      return {
        success: true,
        consentId,
        blockchainTx: consent.blockchainTx,
        confirmedAt: consent.confirmedAt,
        expiresAt: consent.expiresAt,
        message: 'Consent confirmed on blockchain'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async revokeConsent(consentId, patientId) {
    try {
      const consent = this.consents.get(consentId);
      
      if (!consent) {
        throw new Error('Consent not found');
      }

      if (consent.patientId !== patientId) {
        throw new Error('Only the patient can revoke consent');
      }

      if (!consent.revocable) {
        throw new Error('This consent is not revocable');
      }

      // Create revocation record
      const revocationId = uuidv4();
      const revocation = {
        revocationId,
        originalConsentId: consentId,
        patientId,
        revokedAt: new Date().toISOString(),
        reason: 'Patient request',
        blockchainTx: this.generateTransactionHash()
      };

      // Update consent status
      consent.status = 'revoked';
      consent.revokedAt = revocation.revokedAt;
      consent.revocationId = revocationId;

      return {
        success: true,
        revocationId,
        originalConsentId: consentId,
        revokedAt: revocation.revokedAt,
        message: 'Consent revoked successfully'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getConsent(consentId, accessToken) {
    try {
      const consent = this.consents.get(consentId) || this.pendingConsents.get(consentId);
      
      if (!consent) {
        throw new Error('Consent not found');
      }

      // Verify access permissions
      if (!this.verifyAccess(consent, accessToken)) {
        throw new Error('Access denied to consent record');
      }

      return {
        success: true,
        data: {
          consentId: consent.consentId,
          patientId: consent.patientId,
          providerId: consent.providerId,
          dataTypes: consent.dataTypes,
          accessLevel: consent.accessLevel,
          status: consent.status,
          timestamp: consent.timestamp,
          expiresAt: consent.expiresAt,
          revocable: consent.revocable,
          purpose: consent.purpose,
          blockchainTx: consent.blockchainTx
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getPatientConsents(patientId, accessToken) {
    try {
      const patientConsents = [];
      
      // Search in active consents
      for (const [consentId, consent] of this.consents) {
        if (consent.patientId === patientId) {
          patientConsents.push({
            consentId: consent.consentId,
            providerId: consent.providerId,
            dataTypes: consent.dataTypes,
            status: consent.status,
            timestamp: consent.timestamp,
            expiresAt: consent.expiresAt
          });
        }
      }

      // Search in pending consents
      for (const [consentId, consent] of this.pendingConsents) {
        if (consent.patientId === patientId) {
          patientConsents.push({
            consentId: consent.consentId,
            providerId: consent.providerId,
            dataTypes: consent.dataTypes,
            status: consent.status,
            timestamp: consent.timestamp
          });
        }
      }

      return {
        success: true,
        data: {
          patientId,
          consents: patientConsents,
          totalConsents: patientConsents.length,
          activeConsents: patientConsents.filter(c => c.status === 'active').length
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async checkConsent(patientId, providerId, dataType) {
    try {
      const activeConsents = [];
      
      for (const [consentId, consent] of this.consents) {
        if (consent.patientId === patientId && 
            consent.providerId === providerId && 
            consent.status === 'active' &&
            (consent.dataTypes.includes(dataType) || consent.dataTypes.includes('all'))) {
          
          // Check if consent is still valid
          if (consent.expiresAt && new Date(consent.expiresAt) > new Date()) {
            activeConsents.push(consent);
          }
        }
      }

      return {
        success: true,
        hasConsent: activeConsents.length > 0,
        consents: activeConsents,
        message: activeConsents.length > 0 ? 'Valid consent found' : 'No valid consent found'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  generateHash(data) {
    return crypto.createHash('sha256').update(JSON.stringify(data)).digest('hex');
  }

  generateTransactionHash() {
    return crypto.randomBytes(32).toString('hex');
  }

  calculateExpiryDate(duration) {
    const now = new Date();
    const durationMap = {
      '1 month': new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000),
      '3 months': new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000),
      '6 months': new Date(now.getTime() + 180 * 24 * 60 * 60 * 1000),
      '1 year': new Date(now.getTime() + 365 * 24 * 60 * 60 * 1000),
      'permanent': null
    };
    
    return durationMap[duration] || durationMap['1 year'];
  }

  verifyAccess(consent, accessToken) {
    // Simplified access verification
    // In production, implement proper JWT verification
    return accessToken && accessToken.length > 10;
  }
}

const consentService = new ConsentService();

// Routes
router.post('/create', async (req, res) => {
  try {
    const { consentData } = req.body;
    
    if (!consentData || !consentData.patientId || !consentData.providerId) {
      return res.status(400).json({
        success: false,
        error: 'Patient ID and Provider ID are required'
      });
    }

    const result = await consentService.createConsent(consentData);
    
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

router.post('/confirm/:consentId', async (req, res) => {
  try {
    const { consentId } = req.params;
    
    const result = await consentService.confirmConsent(consentId);
    
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

router.post('/revoke/:consentId', async (req, res) => {
  try {
    const { consentId } = req.params;
    const { patientId } = req.body;
    
    const result = await consentService.revokeConsent(consentId, patientId);
    
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

router.get('/:consentId', async (req, res) => {
  try {
    const { consentId } = req.params;
    const { accessToken } = req.headers;
    
    const result = await consentService.getConsent(consentId, accessToken);
    
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

router.get('/patient/:patientId', async (req, res) => {
  try {
    const { patientId } = req.params;
    const { accessToken } = req.headers;
    
    const result = await consentService.getPatientConsents(patientId, accessToken);
    
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

router.post('/check', async (req, res) => {
  try {
    const { patientId, providerId, dataType } = req.body;
    
    if (!patientId || !providerId || !dataType) {
      return res.status(400).json({
        success: false,
        error: 'Patient ID, Provider ID, and Data Type are required'
      });
    }

    const result = await consentService.checkConsent(patientId, providerId, dataType);
    
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