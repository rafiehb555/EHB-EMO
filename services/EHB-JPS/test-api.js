const axios = require('axios');

const API_BASE = 'http://localhost:3001/api';

async function testAPI() {
  try {
    console.log('🧪 Testing EHB-JPS API...\n');

    // Test health endpoint
    console.log('1. Testing health endpoint...');
    const health = await axios.get(`${API_BASE.replace('/api', '')}/health`);
    console.log('✅ Health check:', health.data);

    // Test user registration
    console.log('\n2. Testing user registration...');
    const registerData = {
      email: 'test@example.com',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe',
      userType: 'jobseeker'
    };

    const register = await axios.post(`${API_BASE}/auth/register`, registerData);
    console.log('✅ Registration successful:', register.data);

    // Test user login
    console.log('\n3. Testing user login...');
    const loginData = {
      email: 'test@example.com',
      password: 'password123'
    };

    const login = await axios.post(`${API_BASE}/auth/login`, loginData);
    console.log('✅ Login successful:', login.data);

    // Test getting jobs
    console.log('\n4. Testing jobs endpoint...');
    const jobs = await axios.get(`${API_BASE}/jobs`);
    console.log('✅ Jobs retrieved:', jobs.data);

    console.log('\n🎉 All API tests completed successfully!');

  } catch (error) {
    console.error('❌ API test failed:', error.response?.data || error.message);
  }
}

testAPI();
