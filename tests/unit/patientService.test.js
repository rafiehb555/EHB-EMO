const request = require('supertest');
const { app } = require('../../backend/index');

describe('Patient Service Unit Tests', () => {
  let testPatient;
  
  beforeEach(() => {
    testPatient = testUtils.generateTestPatient();
  });

  describe('POST /api/patients', () => {
    it('should create a new patient successfully', async () => {
      const patientData = {
        name: 'John Doe',
        age: 35,
        gender: 'male',
        email: 'john.doe@test.com',
        phone: '+1234567890',
        address: '123 Main St, City, State'
      };

      const response = await request(app)
        .post('/api/patients')
        .send(patientData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toBeValidPatient();
      expect(response.body.data.name).toBe(patientData.name);
      expect(response.body.data.age).toBe(patientData.age);
    });

    it('should return 400 for invalid patient data', async () => {
      const invalidData = {
        name: '', // Invalid: empty name
        age: -5,  // Invalid: negative age
        gender: 'invalid' // Invalid: invalid gender
      };

      const response = await request(app)
        .post('/api/patients')
        .send(invalidData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toBeDefined();
    });

    it('should handle duplicate email addresses', async () => {
      const patientData = {
        name: 'Jane Smith',
        age: 28,
        gender: 'female',
        email: 'jane.smith@test.com'
      };

      // Create first patient
      await request(app)
        .post('/api/patients')
        .send(patientData)
        .expect(201);

      // Try to create second patient with same email
      const response = await request(app)
        .post('/api/patients')
        .send(patientData)
        .expect(409);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('email already exists');
    });
  });

  describe('GET /api/patients/:id', () => {
    it('should retrieve a patient by ID', async () => {
      // First create a patient
      const createResponse = await request(app)
        .post('/api/patients')
        .send(testPatient)
        .expect(201);

      const patientId = createResponse.body.data.id;

      // Then retrieve the patient
      const response = await request(app)
        .get(`/api/patients/${patientId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toBeValidPatient();
      expect(response.body.data.id).toBe(patientId);
    });

    it('should return 404 for non-existent patient', async () => {
      const response = await request(app)
        .get('/api/patients/non-existent-id')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('Patient not found');
    });
  });

  describe('PUT /api/patients/:id', () => {
    it('should update a patient successfully', async () => {
      // First create a patient
      const createResponse = await request(app)
        .post('/api/patients')
        .send(testPatient)
        .expect(201);

      const patientId = createResponse.body.data.id;
      const updateData = {
        name: 'Updated Name',
        age: 36,
        phone: '+1987654321'
      };

      // Update the patient
      const response = await request(app)
        .put(`/api/patients/${patientId}`)
        .send(updateData)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.name).toBe(updateData.name);
      expect(response.body.data.age).toBe(updateData.age);
      expect(response.body.data.phone).toBe(updateData.phone);
    });

    it('should return 404 for updating non-existent patient', async () => {
      const updateData = { name: 'Updated Name' };

      const response = await request(app)
        .put('/api/patients/non-existent-id')
        .send(updateData)
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('Patient not found');
    });
  });

  describe('DELETE /api/patients/:id', () => {
    it('should delete a patient successfully', async () => {
      // First create a patient
      const createResponse = await request(app)
        .post('/api/patients')
        .send(testPatient)
        .expect(201);

      const patientId = createResponse.body.data.id;

      // Delete the patient
      const response = await request(app)
        .delete(`/api/patients/${patientId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toContain('Patient deleted successfully');

      // Verify patient is deleted
      await request(app)
        .get(`/api/patients/${patientId}`)
        .expect(404);
    });

    it('should return 404 for deleting non-existent patient', async () => {
      const response = await request(app)
        .delete('/api/patients/non-existent-id')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('Patient not found');
    });
  });

  describe('GET /api/patients', () => {
    it('should retrieve all patients with pagination', async () => {
      // Create multiple patients
      const patients = [
        testUtils.generateTestPatient({ name: 'Patient 1' }),
        testUtils.generateTestPatient({ name: 'Patient 2' }),
        testUtils.generateTestPatient({ name: 'Patient 3' })
      ];

      for (const patient of patients) {
        await request(app)
          .post('/api/patients')
          .send(patient)
          .expect(201);
      }

      // Retrieve all patients
      const response = await request(app)
        .get('/api/patients')
        .query({ page: 1, limit: 10 })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.patients).toBeInstanceOf(Array);
      expect(response.body.data.total).toBeGreaterThanOrEqual(patients.length);
    });

    it('should filter patients by search criteria', async () => {
      // Create a patient with specific name
      const specificPatient = testUtils.generateTestPatient({ 
        name: 'John Smith',
        email: 'john.smith@test.com'
      });

      await request(app)
        .post('/api/patients')
        .send(specificPatient)
        .expect(201);

      // Search for the patient
      const response = await request(app)
        .get('/api/patients')
        .query({ search: 'John Smith' })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.patients).toHaveLength(1);
      expect(response.body.data.patients[0].name).toBe('John Smith');
    });
  });

  describe('Healthcare-specific validations', () => {
    it('should validate required healthcare fields', async () => {
      const patientData = {
        name: 'Test Patient',
        age: 25,
        gender: 'male',
        // Missing required fields: email, emergency contact
      };

      const response = await request(app)
        .post('/api/patients')
        .send(patientData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('email is required');
    });

    it('should validate age constraints', async () => {
      const patientData = {
        name: 'Test Patient',
        age: 150, // Invalid: too old
        gender: 'male',
        email: 'test@test.com'
      };

      const response = await request(app)
        .post('/api/patients')
        .send(patientData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('age must be between 0 and 120');
    });

    it('should validate email format for healthcare communications', async () => {
      const patientData = {
        name: 'Test Patient',
        age: 30,
        gender: 'male',
        email: 'invalid-email' // Invalid email format
      };

      const response = await request(app)
        .post('/api/patients')
        .send(patientData)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error).toContain('valid email format');
    });
  });
}); 