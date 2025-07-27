// Test setup for EMO Healthcare Platform

// Global test configuration
global.TEST_CONFIG = {
  // Test database configuration
  database: {
    host: process.env.TEST_DB_HOST || 'localhost',
    port: process.env.TEST_DB_PORT || 5432,
    name: process.env.TEST_DB_NAME || 'emo_test',
    user: process.env.TEST_DB_USER || 'test_user',
    password: process.env.TEST_DB_PASSWORD || 'test_password'
  },
  
  // API configuration
  api: {
    baseUrl: process.env.TEST_API_URL || 'http://localhost:3000',
    timeout: 10000
  },
  
  // Test data
  testData: {
    patients: [
      {
        id: 'test-patient-1',
        name: 'John Doe',
        age: 35,
        gender: 'male',
        email: 'john.doe@test.com'
      },
      {
        id: 'test-patient-2',
        name: 'Jane Smith',
        age: 28,
        gender: 'female',
        email: 'jane.smith@test.com'
      }
    ],
    
    providers: [
      {
        id: 'test-provider-1',
        name: 'Dr. Sarah Johnson',
        specialty: 'Cardiology',
        email: 'sarah.johnson@test.com'
      },
      {
        id: 'test-provider-2',
        name: 'Dr. Michael Brown',
        specialty: 'Pediatrics',
        email: 'michael.brown@test.com'
      }
    ],
    
    appointments: [
      {
        id: 'test-appointment-1',
        patientId: 'test-patient-1',
        providerId: 'test-provider-1',
        date: '2024-01-15T10:00:00Z',
        type: 'consultation'
      }
    ]
  }
};

// Mock console methods to reduce noise in tests
const originalConsole = {
  log: console.log,
  error: console.error,
  warn: console.warn,
  info: console.info
};

// Suppress console output during tests unless explicitly needed
if (process.env.NODE_ENV === 'test') {
  console.log = jest.fn();
  console.error = jest.fn();
  console.warn = jest.fn();
  console.info = jest.fn();
}

// Restore console methods after tests
afterAll(() => {
  console.log = originalConsole.log;
  console.error = originalConsole.error;
  console.warn = originalConsole.warn;
  console.info = originalConsole.info;
});

// Global test utilities
global.testUtils = {
  // Generate test data
  generateTestPatient: (overrides = {}) => ({
    id: `test-patient-${Date.now()}`,
    name: 'Test Patient',
    age: 30,
    gender: 'male',
    email: 'test.patient@test.com',
    ...overrides
  }),
  
  generateTestProvider: (overrides = {}) => ({
    id: `test-provider-${Date.now()}`,
    name: 'Dr. Test Provider',
    specialty: 'General Medicine',
    email: 'test.provider@test.com',
    ...overrides
  }),
  
  generateTestAppointment: (overrides = {}) => ({
    id: `test-appointment-${Date.now()}`,
    patientId: 'test-patient-1',
    providerId: 'test-provider-1',
    date: new Date().toISOString(),
    type: 'consultation',
    ...overrides
  }),
  
  // Wait utility
  wait: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
  
  // Clean up test data
  cleanupTestData: async () => {
    // Implementation for cleaning up test data
    console.log('Cleaning up test data...');
  }
};

// Global test matchers
expect.extend({
  toBeValidPatient(received) {
    const pass = received && 
                 typeof received.id === 'string' &&
                 typeof received.name === 'string' &&
                 typeof received.age === 'number' &&
                 typeof received.gender === 'string';
    
    return {
      pass,
      message: () => `Expected ${received} to be a valid patient object`
    };
  },
  
  toBeValidProvider(received) {
    const pass = received && 
                 typeof received.id === 'string' &&
                 typeof received.name === 'string' &&
                 typeof received.specialty === 'string';
    
    return {
      pass,
      message: () => `Expected ${received} to be a valid provider object`
    };
  },
  
  toBeValidAppointment(received) {
    const pass = received && 
                 typeof received.id === 'string' &&
                 typeof received.patientId === 'string' &&
                 typeof received.providerId === 'string' &&
                 typeof received.date === 'string';
    
    return {
      pass,
      message: () => `Expected ${received} to be a valid appointment object`
    };
  }
});

// Setup test environment
beforeAll(async () => {
  console.log('Setting up EMO test environment...');
  
  // Initialize test database if needed
  // await initializeTestDatabase();
  
  console.log('EMO test environment setup complete');
});

// Cleanup after all tests
afterAll(async () => {
  console.log('Cleaning up EMO test environment...');
  
  // Cleanup test database if needed
  // await cleanupTestDatabase();
  
  console.log('EMO test environment cleanup complete');
}); 