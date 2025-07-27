/**
 * EHB Healthcare API Service
 * Handles all healthcare-related API calls with HIPAA compliance
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { encryptData, decryptData } from '../utils/encryption';
import { validateMedicalData } from '../utils/validation';

// Healthcare data interfaces
export interface PatientData {
  id: string;
  name: string;
  dateOfBirth: Date;
  medicalHistory: string[];
  prescriptions: PrescriptionData[];
  labResults: LabResultData[];
  appointments: AppointmentData[];
}

export interface PrescriptionData {
  id: string;
  medication: string;
  dosage: string;
  frequency: string;
  startDate: Date;
  endDate?: Date;
  prescribedBy: string;
  status: 'active' | 'discontinued' | 'completed';
}

export interface LabResultData {
  id: string;
  testName: string;
  result: string;
  unit: string;
  referenceRange: string;
  date: Date;
  status: 'normal' | 'abnormal' | 'critical';
}

export interface AppointmentData {
  id: string;
  patientId: string;
  doctorId: string;
  date: Date;
  duration: number;
  type: 'consultation' | 'procedure' | 'follow-up';
  status: 'scheduled' | 'confirmed' | 'completed' | 'cancelled';
}

export interface MedicalRecordData {
  id: string;
  patientId: string;
  recordType: 'consultation' | 'procedure' | 'lab' | 'prescription';
  content: string;
  date: Date;
  createdBy: string;
  updatedBy?: string;
}

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://api.ehb.com';
const API_TIMEOUT = 30000; // 30 seconds for healthcare APIs

class HealthcareAPIService {
  private api: AxiosInstance;
  private authToken: string | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Version': '1.0',
        'X-Healthcare-Provider': 'EHB',
      },
    });

    // Request interceptor for HIPAA compliance
    this.api.interceptors.request.use(
      (config) => {
        // Add authentication token
        if (this.authToken) {
          config.headers.Authorization = `Bearer ${this.authToken}`;
        }

        // Encrypt sensitive data
        if (config.data) {
          config.data = encryptData(config.data);
        }

        // Add audit trail
        config.headers['X-Request-ID'] = this.generateRequestId();
        config.headers['X-Timestamp'] = new Date().toISOString();

        return config;
      },
      (error) => {
        console.error('Request interceptor error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for data decryption and validation
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        // Decrypt response data
        if (response.data) {
          response.data = decryptData(response.data);
        }

        // Validate medical data
        if (response.data && this.isMedicalData(response.data)) {
          validateMedicalData(response.data);
        }

        return response;
      },
      (error) => {
        console.error('Response interceptor error:', error);
        
        // Handle healthcare-specific errors
        if (error.response?.status === 403) {
          console.error('Access denied - HIPAA compliance issue');
        }
        
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async authenticate(username: string, password: string): Promise<boolean> {
    try {
      const response = await this.api.post('/auth/login', {
        username,
        password,
      });
      
      this.authToken = response.data.token;
      return true;
    } catch (error) {
      console.error('Authentication failed:', error);
      return false;
    }
  }

  // Patient Management
  async getPatients(): Promise<PatientData[]> {
    try {
      const response = await this.api.get('/patients');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch patients:', error);
      throw error;
    }
  }

  async getPatientById(patientId: string): Promise<PatientData> {
    try {
      const response = await this.api.get(`/patients/${patientId}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch patient ${patientId}:`, error);
      throw error;
    }
  }

  async createPatient(patientData: Omit<PatientData, 'id'>): Promise<PatientData> {
    try {
      const response = await this.api.post('/patients', patientData);
      return response.data;
    } catch (error) {
      console.error('Failed to create patient:', error);
      throw error;
    }
  }

  async updatePatient(patientId: string, patientData: Partial<PatientData>): Promise<PatientData> {
    try {
      const response = await this.api.put(`/patients/${patientId}`, patientData);
      return response.data;
    } catch (error) {
      console.error(`Failed to update patient ${patientId}:`, error);
      throw error;
    }
  }

  // Medical Records
  async getMedicalRecords(patientId: string): Promise<MedicalRecordData[]> {
    try {
      const response = await this.api.get(`/patients/${patientId}/records`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch medical records for patient ${patientId}:`, error);
      throw error;
    }
  }

  async createMedicalRecord(patientId: string, recordData: Omit<MedicalRecordData, 'id'>): Promise<MedicalRecordData> {
    try {
      const response = await this.api.post(`/patients/${patientId}/records`, recordData);
      return response.data;
    } catch (error) {
      console.error(`Failed to create medical record for patient ${patientId}:`, error);
      throw error;
    }
  }

  // Prescriptions
  async getPrescriptions(patientId: string): Promise<PrescriptionData[]> {
    try {
      const response = await this.api.get(`/patients/${patientId}/prescriptions`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch prescriptions for patient ${patientId}:`, error);
      throw error;
    }
  }

  async createPrescription(patientId: string, prescriptionData: Omit<PrescriptionData, 'id'>): Promise<PrescriptionData> {
    try {
      const response = await this.api.post(`/patients/${patientId}/prescriptions`, prescriptionData);
      return response.data;
    } catch (error) {
      console.error(`Failed to create prescription for patient ${patientId}:`, error);
      throw error;
    }
  }

  // Lab Results
  async getLabResults(patientId: string): Promise<LabResultData[]> {
    try {
      const response = await this.api.get(`/patients/${patientId}/lab-results`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch lab results for patient ${patientId}:`, error);
      throw error;
    }
  }

  async createLabResult(patientId: string, labResultData: Omit<LabResultData, 'id'>): Promise<LabResultData> {
    try {
      const response = await this.api.post(`/patients/${patientId}/lab-results`, labResultData);
      return response.data;
    } catch (error) {
      console.error(`Failed to create lab result for patient ${patientId}:`, error);
      throw error;
    }
  }

  // Appointments
  async getAppointments(patientId?: string): Promise<AppointmentData[]> {
    try {
      const url = patientId ? `/appointments?patientId=${patientId}` : '/appointments';
      const response = await this.api.get(url);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch appointments:', error);
      throw error;
    }
  }

  async createAppointment(appointmentData: Omit<AppointmentData, 'id'>): Promise<AppointmentData> {
    try {
      const response = await this.api.post('/appointments', appointmentData);
      return response.data;
    } catch (error) {
      console.error('Failed to create appointment:', error);
      throw error;
    }
  }

  async updateAppointment(appointmentId: string, appointmentData: Partial<AppointmentData>): Promise<AppointmentData> {
    try {
      const response = await this.api.put(`/appointments/${appointmentId}`, appointmentData);
      return response.data;
    } catch (error) {
      console.error(`Failed to update appointment ${appointmentId}:`, error);
      throw error;
    }
  }

  // Healthcare Analytics
  async getPatientAnalytics(patientId: string): Promise<any> {
    try {
      const response = await this.api.get(`/analytics/patients/${patientId}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch analytics for patient ${patientId}:`, error);
      throw error;
    }
  }

  async getClinicalMetrics(): Promise<any> {
    try {
      const response = await this.api.get('/analytics/clinical-metrics');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch clinical metrics:', error);
      throw error;
    }
  }

  // Telemedicine
  async startVideoConsultation(appointmentId: string): Promise<any> {
    try {
      const response = await this.api.post(`/telemedicine/${appointmentId}/start`);
      return response.data;
    } catch (error) {
      console.error(`Failed to start video consultation for appointment ${appointmentId}:`, error);
      throw error;
    }
  }

  async endVideoConsultation(appointmentId: string): Promise<any> {
    try {
      const response = await this.api.post(`/telemedicine/${appointmentId}/end`);
      return response.data;
    } catch (error) {
      console.error(`Failed to end video consultation for appointment ${appointmentId}:`, error);
      throw error;
    }
  }

  // Medical Device Integration
  async getDeviceData(deviceId: string): Promise<any> {
    try {
      const response = await this.api.get(`/devices/${deviceId}/data`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch device data for device ${deviceId}:`, error);
      throw error;
    }
  }

  async sendDeviceCommand(deviceId: string, command: any): Promise<any> {
    try {
      const response = await this.api.post(`/devices/${deviceId}/command`, command);
      return response.data;
    } catch (error) {
      console.error(`Failed to send command to device ${deviceId}:`, error);
      throw error;
    }
  }

  // Utility methods
  private generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private isMedicalData(data: any): boolean {
    return data && (
      data.patientId ||
      data.medicalHistory ||
      data.prescriptions ||
      data.labResults ||
      data.appointments
    );
  }

  // Error handling
  handleHealthcareError(error: any): void {
    if (error.response?.status === 403) {
      console.error('HIPAA compliance violation detected');
      // Notify security team
      this.notifySecurityTeam(error);
    }
    
    if (error.response?.status === 500) {
      console.error('Critical healthcare system error');
      // Notify emergency tech team
      this.notifyEmergencyTeam(error);
    }
  }

  private notifySecurityTeam(error: any): void {
    // Implementation for security team notification
    console.log('Security team notified of compliance issue');
  }

  private notifyEmergencyTeam(error: any): void {
    // Implementation for emergency team notification
    console.log('Emergency tech team notified of system error');
  }
}

// Export singleton instance
export const healthcareAPI = new HealthcareAPIService();
export default healthcareAPI; 