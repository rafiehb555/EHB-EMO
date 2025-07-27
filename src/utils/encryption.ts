/**
 * EHB Healthcare System - Encryption Utilities
 * HIPAA-compliant data encryption for healthcare applications
 */

export interface EncryptionConfig {
  algorithm: string;
  keySize: number;
  ivSize: number;
}

export interface EncryptedData {
  encrypted: string;
  iv: string;
  algorithm: string;
}

export class HealthcareEncryption {
  private static readonly DEFAULT_CONFIG: EncryptionConfig = {
    algorithm: 'AES-GCM',
    keySize: 256,
    ivSize: 12
  };

  /**
   * Generate a secure encryption key
   */
  static async generateKey(): Promise<CryptoKey> {
    return await crypto.subtle.generateKey(
      {
        name: this.DEFAULT_CONFIG.algorithm,
        length: this.DEFAULT_CONFIG.keySize
      },
      true,
      ['encrypt', 'decrypt']
    );
  }

  /**
   * Generate a random initialization vector
   */
  static generateIV(): Uint8Array {
    return crypto.getRandomValues(new Uint8Array(this.DEFAULT_CONFIG.ivSize));
  }

  /**
   * Encrypt sensitive healthcare data
   */
  static async encryptData(
    data: string,
    key: CryptoKey
  ): Promise<EncryptedData> {
    try {
      const iv = this.generateIV();
      const encoder = new TextEncoder();
      const encodedData = encoder.encode(data);

      const encryptedBuffer = await crypto.subtle.encrypt(
        {
          name: this.DEFAULT_CONFIG.algorithm,
          iv: iv
        },
        key,
        encodedData
      );

      return {
        encrypted: this.arrayBufferToBase64(encryptedBuffer),
        iv: this.arrayBufferToBase64(iv),
        algorithm: this.DEFAULT_CONFIG.algorithm
      };
    } catch (error) {
      console.error('Encryption error:', error);
      throw new Error('Failed to encrypt data');
    }
  }

  /**
   * Decrypt healthcare data
   */
  static async decryptData(
    encryptedData: EncryptedData,
    key: CryptoKey
  ): Promise<string> {
    try {
      const iv = this.base64ToArrayBuffer(encryptedData.iv);
      const encrypted = this.base64ToArrayBuffer(encryptedData.encrypted);

      const decryptedBuffer = await crypto.subtle.decrypt(
        {
          name: this.DEFAULT_CONFIG.algorithm,
          iv: iv
        },
        key,
        encrypted
      );

      const decoder = new TextDecoder();
      return decoder.decode(decryptedBuffer);
    } catch (error) {
      console.error('Decryption error:', error);
      throw new Error('Failed to decrypt data');
    }
  }

  /**
   * Hash sensitive data for storage
   */
  static async hashData(data: string): Promise<string> {
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(data);
    
    const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
    return this.arrayBufferToBase64(hashBuffer);
  }

  /**
   * Generate a secure random token
   */
  static generateSecureToken(length: number = 32): string {
    const array = new Uint8Array(length);
    crypto.getRandomValues(array);
    return this.arrayBufferToBase64(array);
  }

  /**
   * Validate encryption configuration
   */
  static validateConfig(config: Partial<EncryptionConfig>): boolean {
    const validAlgorithms = ['AES-GCM', 'AES-CBC'];
    const validKeySizes = [128, 192, 256];

    if (config.algorithm && !validAlgorithms.includes(config.algorithm)) {
      return false;
    }

    if (config.keySize && !validKeySizes.includes(config.keySize)) {
      return false;
    }

    return true;
  }

  /**
   * Convert ArrayBuffer to Base64
   */
  private static arrayBufferToBase64(buffer: ArrayBuffer): string {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  /**
   * Convert Base64 to ArrayBuffer
   */
  private static base64ToArrayBuffer(base64: string): ArrayBuffer {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes.buffer;
  }
}

/**
 * HIPAA Compliance Utilities
 */
export class HIPAACompliance {
  /**
   * Check if data contains PHI (Protected Health Information)
   */
  static containsPHI(data: string): boolean {
    const phiPatterns = [
      /\b\d{3}-\d{2}-\d{4}\b/, // SSN
      /\b\d{3}-\d{3}-\d{4}\b/, // Phone
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, // Email
      /\b\d{1,2}\/\d{1,2}\/\d{4}\b/, // Date of birth
      /\b(patient|medical|diagnosis|treatment|prescription)\b/i
    ];

    return phiPatterns.some(pattern => pattern.test(data));
  }

  /**
   * Sanitize data for logging (remove PHI)
   */
  static sanitizeForLogging(data: string): string {
    // Remove or mask sensitive information
    return data
      .replace(/\b\d{3}-\d{2}-\d{4}\b/g, '***-**-****')
      .replace(/\b\d{3}-\d{3}-\d{4}\b/g, '(***) ***-****')
      .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '***@***.com')
      .replace(/\b\d{1,2}\/\d{1,2}\/\d{4}\b/g, '**/**/****');
  }

  /**
   * Generate audit log entry
   */
  static createAuditEntry(
    action: string,
    userId: string,
    resourceType: string,
    resourceId?: string
  ): any {
    return {
      timestamp: new Date().toISOString(),
      action,
      userId,
      resourceType,
      resourceId,
      ipAddress: '127.0.0.1', // In production, get from request
      userAgent: navigator.userAgent,
      complianceStatus: 'HIPAA_COMPLIANT'
    };
  }
}

/**
 * Data Validation Utilities
 */
export class DataValidation {
  /**
   * Validate patient data
   */
  static validatePatientData(data: any): boolean {
    const requiredFields = ['name', 'dateOfBirth', 'contact'];
    return requiredFields.every(field => data[field] && data[field].trim() !== '');
  }

  /**
   * Validate medical record data
   */
  static validateMedicalRecord(data: any): boolean {
    const requiredFields = ['patientId', 'diagnosis', 'treatment'];
    return requiredFields.every(field => data[field] && data[field].trim() !== '');
  }

  /**
   * Sanitize input data
   */
  static sanitizeInput(input: string): string {
    return input
      .trim()
      .replace(/[<>]/g, '') // Remove potential HTML tags
      .replace(/[&]/g, '&amp;') // Encode ampersands
      .replace(/["]/g, '&quot;') // Encode quotes
      .replace(/[']/g, '&#x27;'); // Encode apostrophes
  }
}

/**
 * Security Utilities
 */
export class SecurityUtils {
  /**
   * Check if current environment is secure
   */
  static isSecureEnvironment(): boolean {
    return window.location.protocol === 'https:' || window.location.hostname === 'localhost';
  }

  /**
   * Generate CSRF token
   */
  static generateCSRFToken(): string {
    return HealthcareEncryption.generateSecureToken(32);
  }

  /**
   * Validate CSRF token
   */
  static validateCSRFToken(token: string, storedToken: string): boolean {
    return token === storedToken && token.length === 44; // Base64 encoded 32 bytes
  }
}

export default {
  HealthcareEncryption,
  HIPAACompliance,
  DataValidation,
  SecurityUtils
}; 