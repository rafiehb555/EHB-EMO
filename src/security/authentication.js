/**
 * EHB Healthcare Authentication System
 * HIPAA-compliant authentication for healthcare professionals
 */

const crypto = require('crypto');
const jwt = require('jsonwebtoken');

class HealthcareAuthentication {
  constructor() {
    this.secretKey =
      process.env.JWT_SECRET || crypto.randomBytes(64).toString('hex');
    this.tokenExpiry = '8h'; // Healthcare standard - 8 hour sessions
    this.maxLoginAttempts = 5;
    this.lockoutDuration = 30 * 60 * 1000; // 30 minutes
    this.failedAttempts = new Map();
  }

  /**
   * Hash password with salt
   * @param {string} password - Plain text password
   * @returns {Object} Hashed password with salt
   */
  hashPassword(password) {
    const salt = crypto.randomBytes(32).toString('hex');
    const hash = crypto
      .pbkdf2Sync(password, salt, 10000, 64, 'sha512')
      .toString('hex');

    return {
      hash: hash,
      salt: salt,
    };
  }

  /**
   * Verify password
   * @param {string} password - Plain text password
   * @param {string} hash - Stored hash
   * @param {string} salt - Stored salt
   * @returns {boolean} Password verification result
   */
  verifyPassword(password, hash, salt) {
    const verifyHash = crypto
      .pbkdf2Sync(password, salt, 10000, 64, 'sha512')
      .toString('hex');
    return crypto.timingSafeEqual(
      Buffer.from(hash, 'hex'),
      Buffer.from(verifyHash, 'hex')
    );
  }

  /**
   * Generate JWT token for healthcare professional
   * @param {Object} user - User object
   * @returns {string} JWT token
   */
  generateToken(user) {
    const payload = {
      userId: user.id,
      email: user.email,
      role: user.role,
      permissions: user.permissions,
      healthcareId: user.healthcareId,
      department: user.department,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + 8 * 60 * 60, // 8 hours
      aud: 'EHB-Healthcare',
      iss: 'EHB-Auth-Service',
    };

    return jwt.sign(payload, this.secretKey, {
      algorithm: 'HS256',
      expiresIn: this.tokenExpiry,
    });
  }

  /**
   * Verify JWT token
   * @param {string} token - JWT token
   * @returns {Object} Decoded token payload
   */
  verifyToken(token) {
    try {
      const decoded = jwt.verify(token, this.secretKey, {
        algorithms: ['HS256'],
        audience: 'EHB-Healthcare',
        issuer: 'EHB-Auth-Service',
      });

      return {
        valid: true,
        payload: decoded,
      };
    } catch (error) {
      return {
        valid: false,
        error: error.message,
      };
    }
  }

  /**
   * Check if user is locked out
   * @param {string} email - User email
   * @returns {boolean} Lockout status
   */
  isLockedOut(email) {
    const attempts = this.failedAttempts.get(email);
    if (!attempts) return false;

    const { count, timestamp } = attempts;
    const now = Date.now();

    if (
      count >= this.maxLoginAttempts &&
      now - timestamp < this.lockoutDuration
    ) {
      return true;
    }

    // Reset if lockout period has passed
    if (now - timestamp >= this.lockoutDuration) {
      this.failedAttempts.delete(email);
    }

    return false;
  }

  /**
   * Record failed login attempt
   * @param {string} email - User email
   */
  recordFailedAttempt(email) {
    const attempts = this.failedAttempts.get(email) || {
      count: 0,
      timestamp: Date.now(),
    };
    attempts.count += 1;
    attempts.timestamp = Date.now();
    this.failedAttempts.set(email, attempts);
  }

  /**
   * Clear failed attempts for user
   * @param {string} email - User email
   */
  clearFailedAttempts(email) {
    this.failedAttempts.delete(email);
  }

  /**
   * Generate multi-factor authentication code
   * @returns {string} MFA code
   */
  generateMFACode() {
    return crypto.randomInt(100000, 999999).toString();
  }

  /**
   * Validate healthcare professional credentials
   * @param {Object} credentials - Login credentials
   * @returns {Object} Validation result
   */
  async validateHealthcareCredentials(credentials) {
    const { email, password, mfaCode } = credentials;

    // Check lockout status
    if (this.isLockedOut(email)) {
      return {
        success: false,
        error: 'Account temporarily locked due to multiple failed attempts',
        lockoutRemaining: this.getLockoutRemaining(email),
      };
    }

    try {
      // In real implementation, this would query the database
      const user = await this.getUserByEmail(email);

      if (!user) {
        this.recordFailedAttempt(email);
        return {
          success: false,
          error: 'Invalid credentials',
        };
      }

      // Verify password
      if (
        !this.verifyPassword(password, user.passwordHash, user.passwordSalt)
      ) {
        this.recordFailedAttempt(email);
        return {
          success: false,
          error: 'Invalid credentials',
        };
      }

      // Verify MFA if required
      if (user.mfaEnabled && mfaCode !== user.mfaCode) {
        this.recordFailedAttempt(email);
        return {
          success: false,
          error: 'Invalid MFA code',
        };
      }

      // Clear failed attempts on successful login
      this.clearFailedAttempts(email);

      // Generate token
      const token = this.generateToken(user);

      return {
        success: true,
        token: token,
        user: {
          id: user.id,
          email: user.email,
          role: user.role,
          healthcareId: user.healthcareId,
          department: user.department,
          permissions: user.permissions,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: 'Authentication failed',
      };
    }
  }

  /**
   * Get user by email (mock implementation)
   * @param {string} email - User email
   * @returns {Object} User object
   */
  async getUserByEmail(email) {
    // Mock user data - in real implementation, this would query the database
    const mockUsers = {
      'doctor@ehb.com': {
        id: 'U001',
        email: 'doctor@ehb.com',
        passwordHash: 'hashed_password_here',
        passwordSalt: 'salt_here',
        role: 'physician',
        healthcareId: 'HC001',
        department: 'cardiology',
        permissions: ['read_patient', 'write_patient', 'prescribe_medication'],
        mfaEnabled: true,
        mfaCode: '123456',
      },
      'nurse@ehb.com': {
        id: 'U002',
        email: 'nurse@ehb.com',
        passwordHash: 'hashed_password_here',
        passwordSalt: 'salt_here',
        role: 'nurse',
        healthcareId: 'HC002',
        department: 'emergency',
        permissions: ['read_patient', 'update_vitals'],
        mfaEnabled: false,
        mfaCode: null,
      },
    };

    return mockUsers[email] || null;
  }

  /**
   * Get remaining lockout time
   * @param {string} email - User email
   * @returns {number} Remaining time in milliseconds
   */
  getLockoutRemaining(email) {
    const attempts = this.failedAttempts.get(email);
    if (!attempts) return 0;

    const remaining = this.lockoutDuration - (Date.now() - attempts.timestamp);
    return Math.max(0, remaining);
  }

  /**
   * Refresh token
   * @param {string} token - Current token
   * @returns {Object} Refresh result
   */
  refreshToken(token) {
    const verification = this.verifyToken(token);

    if (!verification.valid) {
      return {
        success: false,
        error: 'Invalid token',
      };
    }

    const payload = verification.payload;
    const newToken = this.generateToken(payload);

    return {
      success: true,
      token: newToken,
    };
  }
}

module.exports = HealthcareAuthentication;
