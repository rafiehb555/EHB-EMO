const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// Email validation
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Password strength validation
const isStrongPassword = (password) => {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  return password.length >= minLength && 
         hasUpperCase && 
         hasLowerCase && 
         hasNumbers && 
         hasSpecialChar;
};

// Generate secure random string
const generateRandomString = (length = 32) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
};

// Hash password
const hashPassword = async (password) => {
  const saltRounds = parseInt(process.env.BCRYPT_ROUNDS) || 12;
  return await bcrypt.hash(password, saltRounds);
};

// Compare password
const comparePassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};

// Generate JWT token
const generateToken = (payload, expiresIn = '7d') => {
  return jwt.sign(payload, process.env.JWT_SECRET, { expiresIn });
};

// Verify JWT token
const verifyToken = (token) => {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (error) {
    return null;
  }
};

// Sanitize data for HIPAA compliance
const sanitizePatientData = (patient) => {
  const { contact, medicalHistory, ...sanitizedData } = patient;
  return sanitizedData;
};

// Format date for display
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// Calculate age from birth date
const calculateAge = (birthDate) => {
  const today = new Date();
  const birth = new Date(birthDate);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
};

// Validate phone number
const isValidPhoneNumber = (phone) => {
  const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
  return phoneRegex.test(phone);
};

// Generate patient ID
const generatePatientId = () => {
  const timestamp = Date.now().toString();
  const random = Math.random().toString(36).substr(2, 5);
  return `PAT-${timestamp}-${random}`.toUpperCase();
};

// Validate medical record data
const validateMedicalRecord = (record) => {
  const errors = [];
  
  if (!record.diagnosis || record.diagnosis.trim().length === 0) {
    errors.push('Diagnosis is required');
  }
  
  if (!record.treatment || record.treatment.trim().length === 0) {
    errors.push('Treatment is required');
  }
  
  if (!record.doctor || record.doctor.trim().length === 0) {
    errors.push('Doctor information is required');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

// Log activity for audit
const logActivity = (action, userId, details = {}) => {
  const logEntry = {
    timestamp: new Date().toISOString(),
    action,
    userId,
    details,
    ipAddress: 'system' // In production, get from request
  };
  
  console.log('[AUDIT]', JSON.stringify(logEntry));
  return logEntry;
};

// Calculate success rate
const calculateSuccessRate = (completed, total) => {
  if (total === 0) return 0;
  return Math.round((completed / total) * 100 * 10) / 10; // Round to 1 decimal
};

// Generate system health report
const generateHealthReport = () => {
  return {
    timestamp: new Date().toISOString(),
    status: 'healthy',
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: process.version,
    environment: process.env.NODE_ENV || 'development'
  };
};

// Validate API request
const validateApiRequest = (req, requiredFields = []) => {
  const errors = [];
  
  requiredFields.forEach(field => {
    if (!req.body[field] || req.body[field].toString().trim() === '') {
      errors.push(`${field} is required`);
    }
  });
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

// Format error response
const formatErrorResponse = (error, statusCode = 500) => {
  return {
    success: false,
    error: error.message || 'Internal server error',
    statusCode,
    timestamp: new Date().toISOString()
  };
};

// Format success response
const formatSuccessResponse = (data, message = 'Success') => {
  return {
    success: true,
    message,
    data,
    timestamp: new Date().toISOString()
  };
};

module.exports = {
  isValidEmail,
  isStrongPassword,
  generateRandomString,
  hashPassword,
  comparePassword,
  generateToken,
  verifyToken,
  sanitizePatientData,
  formatDate,
  calculateAge,
  isValidPhoneNumber,
  generatePatientId,
  validateMedicalRecord,
  logActivity,
  calculateSuccessRate,
  generateHealthReport,
  validateApiRequest,
  formatErrorResponse,
  formatSuccessResponse
}; 