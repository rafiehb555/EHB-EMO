/**
 * EHB Healthcare Encryption Module
 * HIPAA-compliant data encryption for patient information
 */

const crypto = require('crypto');

class HealthcareEncryption {
  constructor() {
    this.algorithm = 'aes-256-gcm';
    this.keyLength = 32;
    this.ivLength = 16;
    this.tagLength = 16;
  }

  /**
   * Generate encryption key
   * @returns {Buffer} Encryption key
   */
  generateKey() {
    return crypto.randomBytes(this.keyLength);
  }

  /**
   * Generate initialization vector
   * @returns {Buffer} IV
   */
  generateIV() {
    return crypto.randomBytes(this.ivLength);
  }

  /**
   * Encrypt patient data
   * @param {string} data - Data to encrypt
   * @param {Buffer} key - Encryption key
   * @returns {Object} Encrypted data with metadata
   */
  encryptPatientData(data, key) {
    try {
      const iv = this.generateIV();
      const cipher = crypto.createCipher(this.algorithm, key);
      cipher.setAAD(Buffer.from('EHB-PATIENT-DATA', 'utf8'));

      let encrypted = cipher.update(data, 'utf8', 'hex');
      encrypted += cipher.final('hex');

      const tag = cipher.getAuthTag();

      return {
        encrypted: encrypted,
        iv: iv.toString('hex'),
        tag: tag.toString('hex'),
        algorithm: this.algorithm,
        timestamp: new Date().toISOString(),
        version: '1.0',
      };
    } catch (error) {
      throw new Error(`Encryption failed: ${error.message}`);
    }
  }

  /**
   * Decrypt patient data
   * @param {Object} encryptedData - Encrypted data object
   * @param {Buffer} key - Decryption key
   * @returns {string} Decrypted data
   */
  decryptPatientData(encryptedData, key) {
    try {
      const decipher = crypto.createDecipher(this.algorithm, key);
      decipher.setAAD(Buffer.from('EHB-PATIENT-DATA', 'utf8'));
      decipher.setAuthTag(Buffer.from(encryptedData.tag, 'hex'));

      let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
      decrypted += decipher.final('utf8');

      return decrypted;
    } catch (error) {
      throw new Error(`Decryption failed: ${error.message}`);
    }
  }

  /**
   * Hash sensitive data (one-way)
   * @param {string} data - Data to hash
   * @returns {string} Hashed data
   */
  hashSensitiveData(data) {
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Generate secure random token
   * @param {number} length - Token length
   * @returns {string} Secure token
   */
  generateSecureToken(length = 32) {
    return crypto.randomBytes(length).toString('hex');
  }

  /**
   * Verify data integrity
   * @param {string} data - Original data
   * @param {string} hash - Expected hash
   * @returns {boolean} Integrity check result
   */
  verifyDataIntegrity(data, hash) {
    const calculatedHash = this.hashSensitiveData(data);
    return crypto.timingSafeEqual(
      Buffer.from(calculatedHash, 'hex'),
      Buffer.from(hash, 'hex')
    );
  }
}

module.exports = HealthcareEncryption;
