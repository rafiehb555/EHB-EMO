const { Sequelize } = require('sequelize');
const bcrypt = require('bcryptjs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../.env') });

// Use the same connection instance
const { sequelize } = require('./connection');

// Import models
const User = require('../models/User');
const Company = require('../models/Company');
const Job = require('../models/Job');
const Application = require('../models/Application');

// Initialize database associations
const { initializeDatabase } = require('./connection');

async function seed() {
  try {
    console.log('🌱 Starting database seeding...');

    // Test connection
    await sequelize.authenticate();
    console.log('✅ Database connection established.');

    // Initialize database associations
    await initializeDatabase();

    // Create admin user
    const adminPassword = await bcrypt.hash('admin123', 10);
    const admin = await User.create({
      email: 'admin@ehb.com',
      password: adminPassword,
      firstName: 'Admin',
      lastName: 'User',
      userType: 'admin',
      phone: '+1234567890'
    });
    console.log('✅ Admin user created');

    // Create sample job seeker
    const seekerPassword = await bcrypt.hash('seeker123', 10);
    const jobSeeker = await User.create({
      email: 'seeker@example.com',
      password: seekerPassword,
      firstName: 'John',
      lastName: 'Doe',
      userType: 'jobseeker',
      phone: '+1234567891'
    });
    console.log('✅ Sample job seeker created');

    // Create sample company user
    const companyPassword = await bcrypt.hash('company123', 10);
    const companyUser = await User.create({
      email: 'company@example.com',
      password: companyPassword,
      firstName: 'Jane',
      lastName: 'Smith',
      userType: 'company',
      phone: '+1234567892'
    });

    // Create sample company
    const company = await Company.create({
      userId: companyUser.id,
      companyName: 'Tech Solutions Inc.',
      industry: 'Technology',
      companySize: '50-100',
      website: 'https://techsolutions.com',
      description: 'Leading technology solutions provider',
      location: 'New York, NY'
    });
    console.log('✅ Sample company created');

    // Create sample jobs
    const jobs = await Job.bulkCreate([
      {
        companyId: company.id,
        title: 'Senior Software Engineer',
        description: 'We are looking for a senior software engineer to join our team...',
        requirements: '5+ years experience, React, Node.js, PostgreSQL',
        salaryMin: 80000,
        salaryMax: 120000,
        location: 'New York, NY',
        jobType: 'full-time',
        experienceLevel: 'senior',
        skills: ['React', 'Node.js', 'PostgreSQL', 'TypeScript']
      },
      {
        companyId: company.id,
        title: 'Frontend Developer',
        description: 'Join our frontend team to build amazing user experiences...',
        requirements: '3+ years experience, React, TypeScript, CSS',
        salaryMin: 60000,
        salaryMax: 90000,
        location: 'Remote',
        jobType: 'full-time',
        experienceLevel: 'mid-level',
        skills: ['React', 'TypeScript', 'CSS', 'JavaScript']
      },
      {
        companyId: company.id,
        title: 'DevOps Engineer',
        description: 'Help us scale our infrastructure and deployment processes...',
        requirements: '4+ years experience, AWS, Docker, Kubernetes',
        salaryMin: 90000,
        salaryMax: 130000,
        location: 'San Francisco, CA',
        jobType: 'full-time',
        experienceLevel: 'senior',
        skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD']
      }
    ]);
    console.log('✅ Sample jobs created');

    // Create sample application
    await Application.create({
      jobId: jobs[0].id,
      userId: jobSeeker.id,
      coverLetter: 'I am excited to apply for this position...',
      status: 'pending'
    });
    console.log('✅ Sample application created');

    console.log('🎉 Database seeding completed successfully!');
    console.log('\n📋 Sample Data Created:');
    console.log('- Admin: admin@ehb.com / admin123');
    console.log('- Job Seeker: seeker@example.com / seeker123');
    console.log('- Company: company@example.com / company123');
    console.log('- 3 Sample Jobs');
    console.log('- 1 Sample Application');

    process.exit(0);
  } catch (error) {
    console.error('❌ Seeding failed:', error);
    process.exit(1);
  }
}

seed();
