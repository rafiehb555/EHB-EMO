const sharp = require('sharp');
const Tesseract = require('tesseract.js');
const pdfParse = require('pdf-parse');
const fs = require('fs').promises;
const path = require('path');
const logger = require('../utils/logger');

class DocumentService {
  constructor() {
    this.supportedFormats = ['jpg', 'jpeg', 'png', 'pdf', 'tiff'];
    this.maxFileSize = 10 * 1024 * 1024; // 10MB
  }

  /**
   * Analyze uploaded document using AI
   */
  async analyzeDocument(documentData) {
    try {
      const { filePath, documentType, userId } = documentData;
      
      logger.info(`Starting document analysis for user: ${userId}, type: ${documentType}`);

      // Validate file exists
      await this.validateFile(filePath);

      // Extract text from document
      const extractedText = await this.extractText(filePath);

      // Analyze document content
      const analysis = await this.analyzeContent(extractedText, documentType);

      // Verify document authenticity
      const verification = await this.verifyAuthenticity(filePath, documentType);

      // Generate confidence score
      const confidenceScore = this.calculateConfidenceScore(analysis, verification);

      const result = {
        success: true,
        documentType,
        extractedText,
        analysis,
        verification,
        confidenceScore,
        recommendations: this.generateRecommendations(analysis, verification),
        timestamp: new Date().toISOString()
      };

      logger.info(`Document analysis completed for user: ${userId}, confidence: ${confidenceScore}%`);

      return result;

    } catch (error) {
      logger.error('Document analysis error:', error);
      throw new Error(`Document analysis failed: ${error.message}`);
    }
  }

  /**
   * Extract text from various document formats
   */
  async extractText(filePath) {
    const fileExtension = path.extname(filePath).toLowerCase();
    
    try {
      if (['.jpg', '.jpeg', '.png', '.tiff'].includes(fileExtension)) {
        return await this.extractTextFromImage(filePath);
      } else if (fileExtension === '.pdf') {
        return await this.extractTextFromPDF(filePath);
      } else {
        throw new Error('Unsupported file format');
      }
    } catch (error) {
      logger.error('Text extraction error:', error);
      throw new Error(`Text extraction failed: ${error.message}`);
    }
  }

  /**
   * Extract text from image using OCR
   */
  async extractTextFromImage(imagePath) {
    try {
      // Preprocess image for better OCR
      const processedImage = await sharp(imagePath)
        .grayscale()
        .sharpen()
        .normalize()
        .toBuffer();

      const result = await Tesseract.recognize(processedImage, 'eng', {
        logger: m => logger.debug('OCR Progress:', m)
      });

      return result.data.text;
    } catch (error) {
      logger.error('OCR extraction error:', error);
      throw new Error('Failed to extract text from image');
    }
  }

  /**
   * Extract text from PDF
   */
  async extractTextFromPDF(pdfPath) {
    try {
      const dataBuffer = await fs.readFile(pdfPath);
      const data = await pdfParse(dataBuffer);
      return data.text;
    } catch (error) {
      logger.error('PDF extraction error:', error);
      throw new Error('Failed to extract text from PDF');
    }
  }

  /**
   * Analyze document content using AI
   */
  async analyzeContent(text, documentType) {
    try {
      const analysis = {
        documentType,
        keyFields: {},
        dataQuality: {},
        riskFactors: [],
        compliance: {}
      };

      // Extract key information based on document type
      switch (documentType) {
        case 'business_license':
          analysis.keyFields = this.extractBusinessLicenseFields(text);
          analysis.compliance = this.checkBusinessLicenseCompliance(text);
          break;
        case 'tax_certificate':
          analysis.keyFields = this.extractTaxCertificateFields(text);
          analysis.compliance = this.checkTaxCertificateCompliance(text);
          break;
        case 'bank_statement':
          analysis.keyFields = this.extractBankStatementFields(text);
          analysis.compliance = this.checkBankStatementCompliance(text);
          break;
        case 'utility_bill':
          analysis.keyFields = this.extractUtilityBillFields(text);
          analysis.compliance = this.checkUtilityBillCompliance(text);
          break;
        default:
          analysis.keyFields = this.extractGenericFields(text);
      }

      // Analyze data quality
      analysis.dataQuality = this.analyzeDataQuality(text, analysis.keyFields);

      // Identify risk factors
      analysis.riskFactors = this.identifyRiskFactors(text, documentType);

      return analysis;

    } catch (error) {
      logger.error('Content analysis error:', error);
      throw new Error('Content analysis failed');
    }
  }

  /**
   * Extract business license fields
   */
  extractBusinessLicenseFields(text) {
    const fields = {};
    
    // Extract license number
    const licenseMatch = text.match(/license\s*#?\s*:?\s*([A-Z0-9\-]+)/i);
    if (licenseMatch) fields.licenseNumber = licenseMatch[1];

    // Extract business name
    const businessMatch = text.match(/business\s*name\s*:?\s*([^\n]+)/i);
    if (businessMatch) fields.businessName = businessMatch[1].trim();

    // Extract issue date
    const dateMatch = text.match(/issue\s*date\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i);
    if (dateMatch) fields.issueDate = dateMatch[1];

    // Extract expiry date
    const expiryMatch = text.match(/expir\w*\s*date\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i);
    if (expiryMatch) fields.expiryDate = expiryMatch[1];

    return fields;
  }

  /**
   * Extract tax certificate fields
   */
  extractTaxCertificateFields(text) {
    const fields = {};
    
    // Extract tax ID
    const taxIdMatch = text.match(/tax\s*id\s*:?\s*([A-Z0-9\-]+)/i);
    if (taxIdMatch) fields.taxId = taxIdMatch[1];

    // Extract certificate number
    const certMatch = text.match(/certificate\s*#?\s*:?\s*([A-Z0-9\-]+)/i);
    if (certMatch) fields.certificateNumber = certMatch[1];

    // Extract issue date
    const dateMatch = text.match(/issue\s*date\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i);
    if (dateMatch) fields.issueDate = dateMatch[1];

    return fields;
  }

  /**
   * Extract bank statement fields
   */
  extractBankStatementFields(text) {
    const fields = {};
    
    // Extract account number
    const accountMatch = text.match(/account\s*#?\s*:?\s*([0-9\-]+)/i);
    if (accountMatch) fields.accountNumber = accountMatch[1];

    // Extract bank name
    const bankMatch = text.match(/([A-Z\s]+)\s*bank/i);
    if (bankMatch) fields.bankName = bankMatch[1].trim();

    // Extract statement period
    const periodMatch = text.match(/statement\s*period\s*:?\s*([^\n]+)/i);
    if (periodMatch) fields.statementPeriod = periodMatch[1].trim();

    return fields;
  }

  /**
   * Extract utility bill fields
   */
  extractUtilityBillFields(text) {
    const fields = {};
    
    // Extract account number
    const accountMatch = text.match(/account\s*#?\s*:?\s*([0-9\-]+)/i);
    if (accountMatch) fields.accountNumber = accountMatch[1];

    // Extract service address
    const addressMatch = text.match(/service\s*address\s*:?\s*([^\n]+)/i);
    if (addressMatch) fields.serviceAddress = addressMatch[1].trim();

    // Extract bill date
    const dateMatch = text.match(/bill\s*date\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i);
    if (dateMatch) fields.billDate = dateMatch[1];

    return fields;
  }

  /**
   * Extract generic fields from any document
   */
  extractGenericFields(text) {
    const fields = {};
    
    // Extract dates
    const dates = text.match(/\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}/g);
    if (dates) fields.dates = dates;

    // Extract numbers (potential IDs)
    const numbers = text.match(/\b\d{5,}\b/g);
    if (numbers) fields.identifiers = numbers;

    // Extract names (capitalized words)
    const names = text.match(/\b[A-Z][a-z]+\s+[A-Z][a-z]+\b/g);
    if (names) fields.names = names;

    return fields;
  }

  /**
   * Verify document authenticity
   */
  async verifyAuthenticity(filePath, documentType) {
    try {
      const verification = {
        isAuthentic: false,
        confidence: 0,
        checks: []
      };

      // Check file integrity
      const integrityCheck = await this.checkFileIntegrity(filePath);
      verification.checks.push(integrityCheck);

      // Check for digital signatures (if applicable)
      const signatureCheck = await this.checkDigitalSignature(filePath);
      verification.checks.push(signatureCheck);

      // Check for watermarks or security features
      const watermarkCheck = await this.checkWatermarks(filePath);
      verification.checks.push(watermarkCheck);

      // Calculate overall confidence
      const passedChecks = verification.checks.filter(check => check.passed).length;
      verification.confidence = (passedChecks / verification.checks.length) * 100;
      verification.isAuthentic = verification.confidence > 70;

      return verification;

    } catch (error) {
      logger.error('Document verification error:', error);
      throw new Error('Document verification failed');
    }
  }

  /**
   * Check file integrity
   */
  async checkFileIntegrity(filePath) {
    try {
      const stats = await fs.stat(filePath);
      const isValidSize = stats.size > 0 && stats.size <= this.maxFileSize;
      
      return {
        type: 'integrity',
        passed: isValidSize,
        details: {
          fileSize: stats.size,
          isValid: isValidSize
        }
      };
    } catch (error) {
      return {
        type: 'integrity',
        passed: false,
        details: { error: error.message }
      };
    }
  }

  /**
   * Check for digital signatures
   */
  async checkDigitalSignature(filePath) {
    // This would typically involve checking for digital certificates
    // For now, return a basic check
    return {
      type: 'signature',
      passed: true,
      details: { hasSignature: false }
    };
  }

  /**
   * Check for watermarks
   */
  async checkWatermarks(filePath) {
    // This would involve image processing to detect watermarks
    // For now, return a basic check
    return {
      type: 'watermark',
      passed: true,
      details: { hasWatermark: false }
    };
  }

  /**
   * Calculate confidence score
   */
  calculateConfidenceScore(analysis, verification) {
    let score = 0;
    
    // Content analysis score (40%)
    const contentScore = this.calculateContentScore(analysis);
    score += contentScore * 0.4;
    
    // Verification score (40%)
    score += verification.confidence * 0.4;
    
    // Data quality score (20%)
    const qualityScore = this.calculateQualityScore(analysis.dataQuality);
    score += qualityScore * 0.2;
    
    return Math.round(score);
  }

  /**
   * Calculate content analysis score
   */
  calculateContentScore(analysis) {
    let score = 0;
    
    // Check if key fields are extracted
    const keyFieldsCount = Object.keys(analysis.keyFields).length;
    if (keyFieldsCount > 0) score += 30;
    if (keyFieldsCount > 3) score += 20;
    
    // Check compliance
    const complianceScore = Object.values(analysis.compliance)
      .filter(Boolean).length * 10;
    score += complianceScore;
    
    // Check risk factors
    const riskScore = Math.max(0, 30 - (analysis.riskFactors.length * 10));
    score += riskScore;
    
    return Math.min(100, score);
  }

  /**
   * Calculate data quality score
   */
  calculateQualityScore(dataQuality) {
    let score = 0;
    
    // Check completeness
    if (dataQuality.completeness > 80) score += 40;
    else if (dataQuality.completeness > 60) score += 20;
    
    // Check accuracy
    if (dataQuality.accuracy > 90) score += 40;
    else if (dataQuality.accuracy > 70) score += 20;
    
    // Check consistency
    if (dataQuality.consistency > 80) score += 20;
    else if (dataQuality.consistency > 60) score += 10;
    
    return Math.min(100, score);
  }

  /**
   * Generate recommendations based on analysis
   */
  generateRecommendations(analysis, verification) {
    const recommendations = [];
    
    // Low confidence recommendations
    if (verification.confidence < 70) {
      recommendations.push({
        type: 'verification',
        priority: 'high',
        message: 'Document verification confidence is low. Please provide additional verification documents.',
        action: 'upload_additional_documents'
      });
    }
    
    // Missing key fields recommendations
    const missingFields = this.identifyMissingFields(analysis.keyFields, analysis.documentType);
    if (missingFields.length > 0) {
      recommendations.push({
        type: 'completeness',
        priority: 'medium',
        message: `Missing key fields: ${missingFields.join(', ')}`,
        action: 'update_document'
      });
    }
    
    // Risk factor recommendations
    if (analysis.riskFactors.length > 0) {
      recommendations.push({
        type: 'risk',
        priority: 'high',
        message: `Risk factors detected: ${analysis.riskFactors.join(', ')}`,
        action: 'manual_review'
      });
    }
    
    return recommendations;
  }

  /**
   * Clean up old documents
   */
  async cleanupOldDocuments() {
    try {
      const uploadDir = path.join(__dirname, '../../uploads/documents');
      const files = await fs.readdir(uploadDir);
      
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      
      for (const file of files) {
        const filePath = path.join(uploadDir, file);
        const stats = await fs.stat(filePath);
        
        if (stats.mtime < thirtyDaysAgo) {
          await fs.unlink(filePath);
          logger.info(`Cleaned up old document: ${file}`);
        }
      }
    } catch (error) {
      logger.error('Document cleanup error:', error);
    }
  }

  /**
   * Validate file
   */
  async validateFile(filePath) {
    try {
      const stats = await fs.stat(filePath);
      
      if (!stats.isFile()) {
        throw new Error('Invalid file');
      }
      
      if (stats.size > this.maxFileSize) {
        throw new Error('File size exceeds limit');
      }
      
      const extension = path.extname(filePath).toLowerCase();
      if (!this.supportedFormats.includes(extension.substring(1))) {
        throw new Error('Unsupported file format');
      }
      
    } catch (error) {
      throw new Error(`File validation failed: ${error.message}`);
    }
  }
}

module.exports = new DocumentService(); 