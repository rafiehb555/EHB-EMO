const { Sequelize } = require('sequelize');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../.env') });

// Database configuration
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './database.sqlite',
  logging: process.env.NODE_ENV === 'development' ? console.log : false,
  define: {
    timestamps: true,
    underscored: false,
    freezeTableName: true
  }
});

// Test database connection
const testConnection = async () => {
  try {
    await sequelize.authenticate();
    console.log('✅ Database connection established successfully.');
  } catch (error) {
    console.error('❌ Unable to connect to the database:', error);
  }
};

// Initialize database with models
const initializeDatabase = async () => {
  try {
    // Import models
    const User = require('../models/User');
    const Company = require('../models/Company');
    const Job = require('../models/Job');
    const Application = require('../models/Application');

    // Define associations
    User.hasOne(Company, { foreignKey: 'userId', as: 'company' });
    Company.belongsTo(User, { foreignKey: 'userId', as: 'user' });

    Company.hasMany(Job, { foreignKey: 'companyId', as: 'jobs' });
    Job.belongsTo(Company, { foreignKey: 'companyId', as: 'company' });

    User.hasMany(Application, { foreignKey: 'userId', as: 'userApplications' });
    Application.belongsTo(User, { foreignKey: 'userId', as: 'user' });

    Job.hasMany(Application, { foreignKey: 'jobId', as: 'jobApplications' });
    Application.belongsTo(Job, { foreignKey: 'jobId', as: 'job' });

    console.log('✅ Database models and associations initialized.');
  } catch (error) {
    console.error('❌ Error initializing database:', error);
  }
};

module.exports = {
  sequelize,
  testConnection,
  initializeDatabase
};
