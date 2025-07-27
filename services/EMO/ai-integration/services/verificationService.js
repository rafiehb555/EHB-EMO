const express = require('express');
const router = express.Router();

// AI Verification Service for EMO Business Management
class VerificationService {
  constructor() {
    this.verifications = new Map();
    this.documents = new Map();
  }

  async verifyBusinessDocument(documentData) {
    try {
      const {
        documentType,
        documentContent,
        businessId,
        userId,
        documentHash
      } = documentData;

      // AI-powered document verification
      const verification = {
        documentType,
        businessId,
        userId,
        documentHash,
        aiAnalysis: await this.analyzeDocument(documentContent, documentType),
        verificationScore: this.calculateVerificationScore(documentContent),
        recommendations: this.generateRecommendations(documentContent),
        status: 'pending',
        timestamp: new Date().toISOString()
      };

      // Store verification
      this.verifications.set(verification.documentHash, verification);

      return {
        success: true,
        verificationId: verification.documentHash,
        score: verification.verificationScore,
        status: verification.status,
        timestamp: verification.timestamp
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async analyzeDocument(content, documentType) {
    // AI analysis based on document type
    const analysis = {
      authenticity: this.checkAuthenticity(content),
      completeness: this.checkCompleteness(content, documentType),
      consistency: this.checkConsistency(content),
      riskFactors: this.identifyRiskFactors(content, documentType)
    };

    return analysis;
  }

  checkAuthenticity(content) {
    // Simulate AI authenticity check
    const authenticityIndicators = [
      'official_letterhead',
      'digital_signature',
      'watermark',
      'registration_number',
      'government_stamp'
    ];

    let score = 0;
    authenticityIndicators.forEach(indicator => {
      if (content.toLowerCase().includes(indicator)) {
        score += 20;
      }
    });

    return {
      score: Math.min(score, 100),
      indicators: authenticityIndicators.filter(indicator => 
        content.toLowerCase().includes(indicator)
      )
    };
  }

  checkCompleteness(content, documentType) {
    const requiredFields = this.getRequiredFields(documentType);
    let completeness = 0;

    requiredFields.forEach(field => {
      if (content.toLowerCase().includes(field.toLowerCase())) {
        completeness += (100 / requiredFields.length);
      }
    });

    return {
      score: Math.round(completeness),
      missingFields: requiredFields.filter(field => 
        !content.toLowerCase().includes(field.toLowerCase())
      )
    };
  }

  checkConsistency(content) {
    // Check for consistency in document information
    const consistencyChecks = [
      'date_format_consistent',
      'business_name_consistent',
      'address_format_consistent',
      'contact_info_consistent'
    ];

    let consistencyScore = 0;
    consistencyChecks.forEach(check => {
      if (this.performConsistencyCheck(content, check)) {
        consistencyScore += 25;
      }
    });

    return {
      score: consistencyScore,
      issues: consistencyChecks.filter(check => 
        !this.performConsistencyCheck(content, check)
      )
    };
  }

  identifyRiskFactors(content, documentType) {
    const riskFactors = [];

    // Check for suspicious patterns
    if (content.includes('expired') || content.includes('invalid')) {
      riskFactors.push('expired_document');
    }

    if (content.includes('copy') && !content.includes('certified')) {
      riskFactors.push('non_certified_copy');
    }

    if (content.includes('handwritten') && documentType === 'business_license') {
      riskFactors.push('handwritten_official_document');
    }

    return riskFactors;
  }

  getRequiredFields(documentType) {
    const fieldMaps = {
      'business_license': [
        'business name',
        'license number',
        'issue date',
        'expiry date',
        'authority'
      ],
      'tax_certificate': [
        'business name',
        'tax number',
        'filing period',
        'amount',
        'authority'
      ],
      'bank_statement': [
        'account holder',
        'account number',
        'bank name',
        'statement period',
        'balance'
      ],
      'utility_bill': [
        'service provider',
        'account number',
        'billing period',
        'amount',
        'address'
      ]
    };

    return fieldMaps[documentType] || [];
  }

  performConsistencyCheck(content, checkType) {
    // Simulate consistency checks
    switch (checkType) {
      case 'date_format_consistent':
        return /^\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}$/.test(content.match(/\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}/)?.[0] || '');
      case 'business_name_consistent':
        return content.match(/business name|company name|organization name/i)?.length === 1;
      case 'address_format_consistent':
        return content.match(/street|avenue|road|drive/i)?.length > 0;
      case 'contact_info_consistent':
        return content.match(/phone|email|contact/i)?.length > 0;
      default:
        return true;
    }
  }

  calculateVerificationScore(content) {
    let score = 0;

    // Document quality indicators
    if (content.length > 100) score += 20;
    if (content.includes('official')) score += 15;
    if (content.includes('certified')) score += 15;
    if (content.includes('government')) score += 10;
    if (content.includes('stamp')) score += 10;
    if (content.includes('seal')) score += 10;
    if (content.includes('signature')) score += 10;
    if (content.includes('registration')) score += 10;

    return Math.min(score, 100);
  }

  generateRecommendations(content) {
    const recommendations = [];

    if (content.length < 100) {
      recommendations.push('Document appears incomplete - please provide full document');
    }

    if (!content.includes('official') && !content.includes('certified')) {
      recommendations.push('Consider providing certified or official copy for better verification');
    }

    if (!content.includes('stamp') && !content.includes('seal')) {
      recommendations.push('Official stamps or seals would improve document authenticity');
    }

    if (!content.includes('signature')) {
      recommendations.push('Signed documents are preferred for verification');
    }

    return recommendations;
  }

  async approveVerification(verificationId, adminId) {
    try {
      const verification = this.verifications.get(verificationId);
      
      if (!verification) {
        throw new Error('Verification not found');
      }

      verification.status = 'approved';
      verification.approvedBy = adminId;
      verification.approvedAt = new Date().toISOString();

      return {
        success: true,
        verificationId,
        status: 'approved',
        approvedAt: verification.approvedAt
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async rejectVerification(verificationId, adminId, reason) {
    try {
      const verification = this.verifications.get(verificationId);
      
      if (!verification) {
        throw new Error('Verification not found');
      }

      verification.status = 'rejected';
      verification.rejectedBy = adminId;
      verification.rejectionReason = reason;
      verification.rejectedAt = new Date().toISOString();

      return {
        success: true,
        verificationId,
        status: 'rejected',
        reason,
        rejectedAt: verification.rejectedAt
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getVerificationStatus(verificationId) {
    try {
      const verification = this.verifications.get(verificationId);
      
      if (!verification) {
        throw new Error('Verification not found');
      }

      return {
        success: true,
        data: {
          verificationId,
          status: verification.status,
          score: verification.verificationScore,
          analysis: verification.aiAnalysis,
          recommendations: verification.recommendations,
          timestamp: verification.timestamp
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

const verificationService = new VerificationService();

// Routes
router.post('/verify', async (req, res) => {
  try {
    const { documentData } = req.body;
    
    if (!documentData || !documentData.documentContent) {
      return res.status(400).json({
        success: false,
        error: 'Document content is required'
      });
    }

    const result = await verificationService.verifyBusinessDocument(documentData);
    
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

router.post('/approve/:verificationId', async (req, res) => {
  try {
    const { verificationId } = req.params;
    const { adminId } = req.body;
    
    const result = await verificationService.approveVerification(verificationId, adminId);
    
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

router.post('/reject/:verificationId', async (req, res) => {
  try {
    const { verificationId } = req.params;
    const { adminId, reason } = req.body;
    
    const result = await verificationService.rejectVerification(verificationId, adminId, reason);
    
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

router.get('/status/:verificationId', async (req, res) => {
  try {
    const { verificationId } = req.params;
    
    const result = await verificationService.getVerificationStatus(verificationId);
    
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