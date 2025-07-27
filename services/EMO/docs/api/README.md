# EMO Healthcare Platform API Documentation

## Overview

The EMO Healthcare Platform provides a comprehensive REST API for managing healthcare operations, patient data, appointments, and medical records. All endpoints are designed with HIPAA compliance and healthcare security standards in mind.

## Base URL

- **Development**: `http://localhost:3000/api`
- **Staging**: `https://staging-api.emo-healthcare.com/api`
- **Production**: `https://api.emo-healthcare.com/api`

## Authentication

All API requests require authentication using JWT tokens.

### Headers
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

### Getting a Token
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation successful",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `500` - Internal Server Error

## API Endpoints

### Authentication

#### POST /auth/login
Authenticate a user and receive a JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user-123",
      "email": "user@example.com",
      "role": "patient",
      "name": "John Doe"
    }
  }
}
```

#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "password123",
  "name": "Jane Smith",
  "role": "patient"
}
```

### Patients

#### GET /patients
Retrieve a list of patients with pagination and filtering.

**Query Parameters:**
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 10)
- `search` (string): Search by name or email
- `status` (string): Filter by status (active, inactive)

**Response:**
```json
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": "patient-123",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "dateOfBirth": "1990-01-15",
        "gender": "male",
        "status": "active",
        "createdAt": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 50,
      "pages": 5
    }
  }
}
```

#### POST /patients
Create a new patient record.

**Request:**
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone": "+1234567890",
  "dateOfBirth": "1985-03-20",
  "gender": "female",
  "address": "123 Main St, City, State",
  "emergencyContact": {
    "name": "John Smith",
    "phone": "+1234567891",
    "relationship": "spouse"
  }
}
```

#### GET /patients/:id
Retrieve a specific patient by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "patient-123",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "dateOfBirth": "1990-01-15",
    "gender": "male",
    "address": "123 Main St, City, State",
    "emergencyContact": {
      "name": "Jane Doe",
      "phone": "+1234567891",
      "relationship": "spouse"
    },
    "medicalHistory": [],
    "appointments": [],
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
}
```

#### PUT /patients/:id
Update a patient record.

**Request:**
```json
{
  "name": "John Updated",
  "phone": "+1987654321",
  "address": "456 New St, City, State"
}
```

#### DELETE /patients/:id
Delete a patient record (soft delete).

### Providers

#### GET /providers
Retrieve a list of healthcare providers.

**Query Parameters:**
- `page` (number): Page number
- `limit` (number): Items per page
- `specialty` (string): Filter by specialty
- `search` (string): Search by name

**Response:**
```json
{
  "success": true,
  "data": {
    "providers": [
      {
        "id": "provider-123",
        "name": "Dr. Sarah Johnson",
        "email": "sarah.johnson@example.com",
        "specialty": "Cardiology",
        "license": "MD123456",
        "phone": "+1234567890",
        "status": "active"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

#### POST /providers
Create a new healthcare provider.

**Request:**
```json
{
  "name": "Dr. Michael Brown",
  "email": "michael.brown@example.com",
  "specialty": "Pediatrics",
  "license": "MD789012",
  "phone": "+1234567890",
  "address": "789 Medical Center Dr"
}
```

### Appointments

#### GET /appointments
Retrieve appointments with filtering.

**Query Parameters:**
- `patientId` (string): Filter by patient
- `providerId` (string): Filter by provider
- `date` (string): Filter by date (YYYY-MM-DD)
- `status` (string): Filter by status (scheduled, completed, cancelled)

**Response:**
```json
{
  "success": true,
  "data": {
    "appointments": [
      {
        "id": "appointment-123",
        "patientId": "patient-123",
        "providerId": "provider-123",
        "date": "2024-01-20T14:00:00Z",
        "duration": 30,
        "type": "consultation",
        "status": "scheduled",
        "notes": "Follow-up appointment"
      }
    ]
  }
}
```

#### POST /appointments
Create a new appointment.

**Request:**
```json
{
  "patientId": "patient-123",
  "providerId": "provider-123",
  "date": "2024-01-20T14:00:00Z",
  "duration": 30,
  "type": "consultation",
  "notes": "Initial consultation"
}
```

### Health Records

#### GET /health-records/:patientId
Retrieve patient health records.

**Headers:**
```
Authorization: Bearer <token>
X-Consent: <consent-id>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "patientId": "patient-123",
    "records": [
      {
        "id": "record-123",
        "type": "diagnosis",
        "date": "2024-01-15T10:30:00Z",
        "provider": "Dr. Sarah Johnson",
        "content": "Hypertension diagnosis",
        "attachments": []
      }
    ]
  }
}
```

#### POST /health-records
Create a new health record.

**Request:**
```json
{
  "patientId": "patient-123",
  "type": "diagnosis",
  "content": "Patient diagnosed with hypertension",
  "attachments": []
}
```

### AI Integration

#### POST /ai/diagnosis
Get AI-powered symptom analysis.

**Request:**
```json
{
  "symptoms": [
    {
      "name": "headache",
      "severity": "moderate",
      "duration": "2 days"
    }
  ],
  "patientId": "patient-123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis": {
      "primarySymptoms": ["headache"],
      "riskLevel": "low",
      "possibleConditions": [
        {
          "condition": "Tension Headache",
          "confidence": 0.85
        }
      ],
      "recommendations": [
        "Rest and hydration",
        "Over-the-counter pain relievers"
      ]
    }
  }
}
```

### Blockchain

#### POST /blockchain/health-records/create
Create a blockchain-secured health record.

**Request:**
```json
{
  "patientData": {
    "patientId": "patient-123",
    "medicalData": {
      "diagnosis": "Hypertension",
      "medications": ["Lisinopril"],
      "vitalSigns": {
        "bloodPressure": "140/90",
        "heartRate": 72
      }
    },
    "consent": true,
    "accessLevel": "restricted"
  }
}
```

#### GET /blockchain/consent/patient/:patientId
Retrieve patient consent records.

**Response:**
```json
{
  "success": true,
  "data": {
    "patientId": "patient-123",
    "consents": [
      {
        "consentId": "consent-123",
        "providerId": "provider-123",
        "dataTypes": ["medical_records", "billing"],
        "status": "active",
        "expiresAt": "2025-01-15T10:30:00Z"
      }
    ]
  }
}
```

## Rate Limiting

API requests are rate-limited to ensure fair usage:

- **Authentication endpoints**: 5 requests per minute
- **Patient data endpoints**: 100 requests per minute
- **Health record endpoints**: 50 requests per minute
- **AI endpoints**: 20 requests per minute

## Webhooks

EMO supports webhooks for real-time notifications:

### Available Events
- `patient.created`
- `appointment.scheduled`
- `health_record.created`
- `consent.granted`
- `consent.revoked`

### Webhook Configuration
```json
{
  "url": "https://your-app.com/webhooks/emo",
  "events": ["patient.created", "appointment.scheduled"],
  "secret": "your-webhook-secret"
}
```

## SDKs and Libraries

### JavaScript/Node.js
```bash
npm install emo-healthcare-sdk
```

```javascript
const EMO = require('emo-healthcare-sdk');

const client = new EMO({
  apiKey: 'your-api-key',
  environment: 'production'
});

const patients = await client.patients.list();
```

### Python
```bash
pip install emo-healthcare-python
```

```python
from emo_healthcare import EMO

client = EMO(api_key='your-api-key', environment='production')
patients = client.patients.list()
```

## Support

For API support and questions:
- **Email**: api-support@ehb.com
- **Documentation**: https://docs.emo-healthcare.com/api
- **Status Page**: https://status.emo-healthcare.com

---

**API Version**: v1.0  
**Last Updated**: January 2024 