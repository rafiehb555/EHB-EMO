const { Sequelize } = require('sequelize');
require('dotenv').config();

// Database configuration
const config = {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'ehb_jps_db',
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'your_password',
    dialect: 'postgres',
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    pool: {
        max: 10,
        min: 0,
        acquire: 30000,
        idle: 10000
    },
    dialectOptions: {
        ssl: process.env.NODE_ENV === 'production' ? {
            require: true,
            rejectUnauthorized: false
        } : false
    }
};

// Create Sequelize instance
const sequelize = new Sequelize(
    config.database,
    config.username,
    config.password,
    {
        host: config.host,
        port: config.port,
        dialect: config.dialect,
        logging: config.logging,
        pool: config.pool,
        dialectOptions: config.dialectOptions,
        define: {
            timestamps: true,
            underscored: true,
            freezeTableName: true
        }
    }
);

// Test database connection
const testConnection = async () => {
    try {
        await sequelize.authenticate();
        console.log('✅ Database connection established successfully.');

        // Sync models with database
        if (process.env.NODE_ENV === 'development') {
            await sequelize.sync({ alter: true });
            console.log('✅ Database models synchronized.');
        }

        return true;
    } catch (error) {
        console.error('❌ Unable to connect to the database:', error);
        return false;
    }
};

// Initialize database
const initializeDatabase = async () => {
    try {
        // Test connection
        const isConnected = await testConnection();

        if (!isConnected) {
            console.error('❌ Database connection failed. Please check your configuration.');
            process.exit(1);
        }

        // Import models
        require('../models/User');
        require('../models/Job');
        require('../models/Company');
        require('../models/Application');

        // Set up associations
        const User = require('../models/User');
        const Job = require('../models/Job');
        const Company = require('../models/Company');
        const Application = require('../models/Application');

        // User associations
        User.hasMany(Application, { foreignKey: 'user_id', as: 'applications' });
        User.hasOne(Company, { foreignKey: 'user_id', as: 'company' });

        // Company associations
        Company.belongsTo(User, { foreignKey: 'user_id', as: 'user' });
        Company.hasMany(Job, { foreignKey: 'company_id', as: 'jobs' });

        // Job associations
        Job.belongsTo(Company, { foreignKey: 'company_id', as: 'company' });
        Job.hasMany(Application, { foreignKey: 'job_id', as: 'applications' });

        // Application associations
        Application.belongsTo(User, { foreignKey: 'user_id', as: 'user' });
        Application.belongsTo(Job, { foreignKey: 'job_id', as: 'job' });

        console.log('✅ Database models and associations set up successfully.');

        return sequelize;
    } catch (error) {
        console.error('❌ Database initialization failed:', error);
        throw error;
    }
};

// Export functions and sequelize instance
module.exports = {
    sequelize,
    testConnection,
    initializeDatabase
};
