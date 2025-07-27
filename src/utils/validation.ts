/**
 * EHB Healthcare Data Validation Utilities
 * HIPAA-compliant validation for medical data
 */

// Healthcare data validation interfaces
export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export interface PatientValidationData {
  id?: string;
  name: string;
  dateOfBirth: Date;
  medicalHistory: string[];
  prescriptions?: any[];
  labResults?: any[];
  appointments?: any[];
}

export interface MedicalRecordValidationData {
  id?: string;
  patientId: string;
  recordType: 'consultation' | 'procedure' | 'lab' | 'prescription';
  content: string;
  date: Date;
  createdBy: string;
}

export interface PrescriptionValidationData {
  id?: string;
  medication: string;
  dosage: string;
  frequency: string;
  startDate: Date;
  endDate?: Date;
  prescribedBy: string;
  status: 'active' | 'discontinued' | 'completed';
}

export interface LabResultValidationData {
  id?: string;
  testName: string;
  result: string;
  unit: string;
  referenceRange: string;
  date: Date;
  status: 'normal' | 'abnormal' | 'critical';
}

/**
 * Validate medical data for HIPAA compliance
 * @param data - Medical data to validate
 * @returns Validation result
 */
export function validateMedicalData(data: any): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  try {
    // Check if data exists
    if (!data) {
      result.isValid = false;
      result.errors.push('Medical data is required');
      return result;
    }

    // Validate patient data
    if (data.patientId || data.name) {
      const patientValidation = validatePatientData(data);
      if (!patientValidation.isValid) {
        result.isValid = false;
        result.errors.push(...patientValidation.errors);
      }
      result.warnings.push(...patientValidation.warnings);
    }

    // Validate medical records
    if (data.recordType) {
      const recordValidation = validateMedicalRecord(data);
      if (!recordValidation.isValid) {
        result.isValid = false;
        result.errors.push(...recordValidation.errors);
      }
      result.warnings.push(...recordValidation.warnings);
    }

    // Validate prescriptions
    if (data.medication) {
      const prescriptionValidation = validatePrescription(data);
      if (!prescriptionValidation.isValid) {
        result.isValid = false;
        result.errors.push(...prescriptionValidation.errors);
      }
      result.warnings.push(...prescriptionValidation.warnings);
    }

    // Validate lab results
    if (data.testName) {
      const labValidation = validateLabResult(data);
      if (!labValidation.isValid) {
        result.isValid = false;
        result.errors.push(...labValidation.errors);
      }
      result.warnings.push(...labValidation.warnings);
    }

    // Check for sensitive data exposure
    if (hasSensitiveDataExposure(data)) {
      result.warnings.push('Potential sensitive data exposure detected');
    }

    // Validate data format
    if (!isValidDataFormat(data)) {
      result.isValid = false;
      result.errors.push('Invalid data format');
    }

  } catch (error) {
    result.isValid = false;
    result.errors.push(`Validation error: ${error}`);
  }

  return result;
}

/**
 * Validate patient data
 * @param data - Patient data to validate
 * @returns Validation result
 */
export function validatePatientData(data: PatientValidationData): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  // Validate name
  if (!data.name || typeof data.name !== 'string' || data.name.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Patient name is required');
  } else if (data.name.length > 100) {
    result.warnings.push('Patient name is unusually long');
  }

  // Validate date of birth
  if (!data.dateOfBirth) {
    result.isValid = false;
    result.errors.push('Date of birth is required');
  } else {
    const dob = new Date(data.dateOfBirth);
    const now = new Date();
    const age = now.getFullYear() - dob.getFullYear();
    
    if (age < 0 || age > 150) {
      result.isValid = false;
      result.errors.push('Invalid date of birth');
    }
  }

  // Validate medical history
  if (!Array.isArray(data.medicalHistory)) {
    result.isValid = false;
    result.errors.push('Medical history must be an array');
  } else {
    data.medicalHistory.forEach((item, index) => {
      if (typeof item !== 'string' || item.trim().length === 0) {
        result.isValid = false;
        result.errors.push(`Invalid medical history item at index ${index}`);
      }
    });
  }

  return result;
}

/**
 * Validate medical record data
 * @param data - Medical record data to validate
 * @returns Validation result
 */
export function validateMedicalRecord(data: MedicalRecordValidationData): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  // Validate patient ID
  if (!data.patientId || typeof data.patientId !== 'string') {
    result.isValid = false;
    result.errors.push('Patient ID is required');
  }

  // Validate record type
  const validRecordTypes = ['consultation', 'procedure', 'lab', 'prescription'];
  if (!data.recordType || !validRecordTypes.includes(data.recordType)) {
    result.isValid = false;
    result.errors.push('Valid record type is required');
  }

  // Validate content
  if (!data.content || typeof data.content !== 'string' || data.content.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Record content is required');
  } else if (data.content.length > 10000) {
    result.warnings.push('Record content is unusually long');
  }

  // Validate date
  if (!data.date) {
    result.isValid = false;
    result.errors.push('Record date is required');
  } else {
    const recordDate = new Date(data.date);
    const now = new Date();
    
    if (recordDate > now) {
      result.isValid = false;
      result.errors.push('Record date cannot be in the future');
    }
  }

  // Validate created by
  if (!data.createdBy || typeof data.createdBy !== 'string') {
    result.isValid = false;
    result.errors.push('Created by field is required');
  }

  return result;
}

/**
 * Validate prescription data
 * @param data - Prescription data to validate
 * @returns Validation result
 */
export function validatePrescription(data: PrescriptionValidationData): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  // Validate medication
  if (!data.medication || typeof data.medication !== 'string' || data.medication.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Medication name is required');
  }

  // Validate dosage
  if (!data.dosage || typeof data.dosage !== 'string' || data.dosage.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Dosage is required');
  }

  // Validate frequency
  if (!data.frequency || typeof data.frequency !== 'string' || data.frequency.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Frequency is required');
  }

  // Validate start date
  if (!data.startDate) {
    result.isValid = false;
    result.errors.push('Start date is required');
  } else {
    const startDate = new Date(data.startDate);
    const now = new Date();
    
    if (startDate > now) {
      result.isValid = false;
      result.errors.push('Start date cannot be in the future');
    }
  }

  // Validate end date if provided
  if (data.endDate) {
    const startDate = new Date(data.startDate);
    const endDate = new Date(data.endDate);
    
    if (endDate <= startDate) {
      result.isValid = false;
      result.errors.push('End date must be after start date');
    }
  }

  // Validate prescribed by
  if (!data.prescribedBy || typeof data.prescribedBy !== 'string') {
    result.isValid = false;
    result.errors.push('Prescribed by field is required');
  }

  // Validate status
  const validStatuses = ['active', 'discontinued', 'completed'];
  if (!data.status || !validStatuses.includes(data.status)) {
    result.isValid = false;
    result.errors.push('Valid status is required');
  }

  return result;
}

/**
 * Validate lab result data
 * @param data - Lab result data to validate
 * @returns Validation result
 */
export function validateLabResult(data: LabResultValidationData): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  // Validate test name
  if (!data.testName || typeof data.testName !== 'string' || data.testName.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Test name is required');
  }

  // Validate result
  if (!data.result || typeof data.result !== 'string' || data.result.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Test result is required');
  }

  // Validate unit
  if (!data.unit || typeof data.unit !== 'string' || data.unit.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Unit is required');
  }

  // Validate reference range
  if (!data.referenceRange || typeof data.referenceRange !== 'string' || data.referenceRange.trim().length === 0) {
    result.isValid = false;
    result.errors.push('Reference range is required');
  }

  // Validate date
  if (!data.date) {
    result.isValid = false;
    result.errors.push('Test date is required');
  } else {
    const testDate = new Date(data.date);
    const now = new Date();
    
    if (testDate > now) {
      result.isValid = false;
      result.errors.push('Test date cannot be in the future');
    }
  }

  // Validate status
  const validStatuses = ['normal', 'abnormal', 'critical'];
  if (!data.status || !validStatuses.includes(data.status)) {
    result.isValid = false;
    result.errors.push('Valid status is required');
  }

  return result;
}

/**
 * Check for sensitive data exposure
 * @param data - Data to check
 * @returns True if sensitive data exposure is detected
 */
export function hasSensitiveDataExposure(data: any): boolean {
  const sensitivePatterns = [
    /\b\d{3}-\d{2}-\d{4}\b/, // SSN pattern
    /\b\d{3}\.\d{3}\.\d{4}\b/, // Phone pattern
    /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/, // Email pattern
    /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, // IP address pattern
  ];

  const dataString = JSON.stringify(data);
  
  return sensitivePatterns.some(pattern => pattern.test(dataString));
}

/**
 * Validate data format
 * @param data - Data to validate
 * @returns True if data format is valid
 */
export function isValidDataFormat(data: any): boolean {
  try {
    // Check if data is an object
    if (typeof data !== 'object' || data === null) {
      return false;
    }

    // Check for required fields based on data type
    if (data.patientId && typeof data.patientId !== 'string') {
      return false;
    }

    if (data.name && typeof data.name !== 'string') {
      return false;
    }

    if (data.date && !(data.date instanceof Date) && isNaN(Date.parse(data.date))) {
      return false;
    }

    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Sanitize medical data for display
 * @param data - Data to sanitize
 * @returns Sanitized data
 */
export function sanitizeMedicalData(data: any): any {
  if (typeof data === 'string') {
    // Remove potential XSS
    return data.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  }

  if (Array.isArray(data)) {
    return data.map(item => sanitizeMedicalData(item));
  }

  if (typeof data === 'object' && data !== null) {
    const sanitized: any = {};
    for (const [key, value] of Object.entries(data)) {
      sanitized[key] = sanitizeMedicalData(value);
    }
    return sanitized;
  }

  return data;
}

/**
 * Validate HIPAA compliance
 * @param data - Data to validate for HIPAA compliance
 * @returns Validation result
 */
export function validateHIPAACompliance(data: any): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  // Check for required HIPAA fields
  if (!data.auditTrail) {
    result.warnings.push('Audit trail missing');
  }

  if (!data.accessControl) {
    result.warnings.push('Access control missing');
  }

  if (!data.dataRetention) {
    result.warnings.push('Data retention policy missing');
  }

  // Check for sensitive data handling
  if (hasSensitiveDataExposure(data)) {
    result.isValid = false;
    result.errors.push('Sensitive data exposure detected');
  }

  // Check for encryption
  if (!data.encrypted) {
    result.warnings.push('Data encryption status unknown');
  }

  return result;
}

/**
 * Validate medical device data
 * @param data - Device data to validate
 * @returns Validation result
 */
export function validateDeviceData(data: any): ValidationResult {
  const result: ValidationResult = {
    isValid: true,
    errors: [],
    warnings: []
  };

  // Validate device ID
  if (!data.deviceId || typeof data.deviceId !== 'string') {
    result.isValid = false;
    result.errors.push('Device ID is required');
  }

  // Validate device type
  if (!data.deviceType || typeof data.deviceType !== 'string') {
    result.isValid = false;
    result.errors.push('Device type is required');
  }

  // Validate readings
  if (!data.readings || !Array.isArray(data.readings)) {
    result.isValid = false;
    result.errors.push('Device readings are required');
  }

  // Validate timestamp
  if (!data.timestamp) {
    result.isValid = false;
    result.errors.push('Timestamp is required');
  }

  return result;
}

// Export all validation utilities
export default {
  validateMedicalData,
  validatePatientData,
  validateMedicalRecord,
  validatePrescription,
  validateLabResult,
  hasSensitiveDataExposure,
  isValidDataFormat,
  sanitizeMedicalData,
  validateHIPAACompliance,
  validateDeviceData
}; 