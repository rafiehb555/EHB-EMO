require('dotenv').config();

const environments = {
  development: {
    NODE_ENV: 'development',
    PORT: process.env.PORT || 4003,
    MONGODB_URI: process.env.MONGODB_URI || 'mongodb://localhost:27017/emo_dev',
    JWT_SECRET: process.env.JWT_SECRET || 'emo-dev-secret-key-change-in-production',
    JWT_EXPIRE: process.env.JWT_EXPIRE || '7d',
    FRONTEND_URL: process.env.FRONTEND_URL || 'http://localhost:3000',
    ADMIN_URL: process.env.ADMIN_URL || 'http://localhost:6001',
    LOG_LEVEL: process.env.LOG_LEVEL || 'debug',

    // Email configuration
    SMTP_HOST: process.env.SMTP_HOST || 'smtp.gmail.com',
    SMTP_PORT: process.env.SMTP_PORT || 587,
    SMTP_USER: process.env.SMTP_USER || '',
    SMTP_PASS: process.env.SMTP_PASS || '',
    FROM_EMAIL: process.env.FROM_EMAIL || 'noreply@emo.com',

    // SMS configuration
    TWILIO_ACCOUNT_SID: process.env.TWILIO_ACCOUNT_SID || '',
    TWILIO_AUTH_TOKEN: process.env.TWILIO_AUTH_TOKEN || '',
    TWILIO_PHONE_NUMBER: process.env.TWILIO_PHONE_NUMBER || '',

    // File upload configuration
    UPLOAD_PATH: process.env.UPLOAD_PATH || './uploads',
    MAX_FILE_SIZE: process.env.MAX_FILE_SIZE || 10 * 1024 * 1024, // 10MB
    ALLOWED_FILE_TYPES: process.env.ALLOWED_FILE_TYPES || 'jpg,jpeg,png,pdf,doc,docx',

    // AI configuration
    OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
    OPENAI_MODEL: process.env.OPENAI_MODEL || 'gpt-3.5-turbo',

    // Blockchain configuration
    POLKADOT_ENDPOINT: process.env.POLKADOT_ENDPOINT || 'wss://rpc.polkadot.io',
    MOONBEAM_ENDPOINT: process.env.MOONBEAM_ENDPOINT || 'https://rpc.api.moonbeam.network',
    BSC_ENDPOINT: process.env.BSC_ENDPOINT || 'https://bsc-dataseed.binance.org',

    // Rate limiting
    RATE_LIMIT_WINDOW: process.env.RATE_LIMIT_WINDOW || 15 * 60 * 1000, // 15 minutes
    RATE_LIMIT_MAX: process.env.RATE_LIMIT_MAX || 100,

    // Security
    CORS_ORIGIN: process.env.CORS_ORIGIN || 'http://localhost:3000',
    SESSION_SECRET: process.env.SESSION_SECRET || 'emo-session-secret',

    // Database
    DB_NAME: process.env.DB_NAME || 'emo_dev',
    DB_HOST: process.env.DB_HOST || 'localhost',
    DB_PORT: process.env.DB_PORT || 27017,
    DB_USER: process.env.DB_USER || '',
    DB_PASS: process.env.DB_PASS || '',
  },

  staging: {
    NODE_ENV: 'staging',
    PORT: process.env.PORT || 4003,
    MONGODB_URI: process.env.MONGODB_URI || 'mongodb://localhost:27017/emo_staging',
    JWT_SECRET: process.env.JWT_SECRET || 'emo-staging-secret-key',
    JWT_EXPIRE: process.env.JWT_EXPIRE || '7d',
    FRONTEND_URL: process.env.FRONTEND_URL || 'https://staging.emo.com',
    ADMIN_URL: process.env.ADMIN_URL || 'https://admin-staging.emo.com',
    LOG_LEVEL: process.env.LOG_LEVEL || 'info',

    // Email configuration
    SMTP_HOST: process.env.SMTP_HOST || 'smtp.gmail.com',
    SMTP_PORT: process.env.SMTP_PORT || 587,
    SMTP_USER: process.env.SMTP_USER || '',
    SMTP_PASS: process.env.SMTP_PASS || '',
    FROM_EMAIL: process.env.FROM_EMAIL || 'noreply@emo.com',

    // SMS configuration
    TWILIO_ACCOUNT_SID: process.env.TWILIO_ACCOUNT_SID || '',
    TWILIO_AUTH_TOKEN: process.env.TWILIO_AUTH_TOKEN || '',
    TWILIO_PHONE_NUMBER: process.env.TWILIO_PHONE_NUMBER || '',

    // File upload configuration
    UPLOAD_PATH: process.env.UPLOAD_PATH || './uploads',
    MAX_FILE_SIZE: process.env.MAX_FILE_SIZE || 10 * 1024 * 1024, // 10MB
    ALLOWED_FILE_TYPES: process.env.ALLOWED_FILE_TYPES || 'jpg,jpeg,png,pdf,doc,docx',

    // AI configuration
    OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
    OPENAI_MODEL: process.env.OPENAI_MODEL || 'gpt-3.5-turbo',

    // Blockchain configuration
    POLKADOT_ENDPOINT: process.env.POLKADOT_ENDPOINT || 'wss://rpc.polkadot.io',
    MOONBEAM_ENDPOINT: process.env.MOONBEAM_ENDPOINT || 'https://rpc.api.moonbeam.network',
    BSC_ENDPOINT: process.env.BSC_ENDPOINT || 'https://bsc-dataseed.binance.org',

    // Rate limiting
    RATE_LIMIT_WINDOW: process.env.RATE_LIMIT_WINDOW || 15 * 60 * 1000, // 15 minutes
    RATE_LIMIT_MAX: process.env.RATE_LIMIT_MAX || 100,

    // Security
    CORS_ORIGIN: process.env.CORS_ORIGIN || 'https://staging.emo.com',
    SESSION_SECRET: process.env.SESSION_SECRET || 'emo-session-secret',

    // Database
    DB_NAME: process.env.DB_NAME || 'emo_staging',
    DB_HOST: process.env.DB_HOST || 'localhost',
    DB_PORT: process.env.DB_PORT || 27017,
    DB_USER: process.env.DB_USER || '',
    DB_PASS: process.env.DB_PASS || '',
  },

  production: {
    NODE_ENV: 'production',
    PORT: process.env.PORT || 4003,
    MONGODB_URI: process.env.MONGODB_URI || 'mongodb://localhost:27017/emo_prod',
    JWT_SECRET: process.env.JWT_SECRET || 'emo-production-secret-key-change-this',
    JWT_EXPIRE: process.env.JWT_EXPIRE || '7d',
    FRONTEND_URL: process.env.FRONTEND_URL || 'https://emo.com',
    ADMIN_URL: process.env.ADMIN_URL || 'https://admin.emo.com',
    LOG_LEVEL: process.env.LOG_LEVEL || 'warn',

    // Email configuration
    SMTP_HOST: process.env.SMTP_HOST || 'smtp.gmail.com',
    SMTP_PORT: process.env.SMTP_PORT || 587,
    SMTP_USER: process.env.SMTP_USER || '',
    SMTP_PASS: process.env.SMTP_PASS || '',
    FROM_EMAIL: process.env.FROM_EMAIL || 'noreply@emo.com',

    // SMS configuration
    TWILIO_ACCOUNT_SID: process.env.TWILIO_ACCOUNT_SID || '',
    TWILIO_AUTH_TOKEN: process.env.TWILIO_AUTH_TOKEN || '',
    TWILIO_PHONE_NUMBER: process.env.TWILIO_PHONE_NUMBER || '',

    // File upload configuration
    UPLOAD_PATH: process.env.UPLOAD_PATH || './uploads',
    MAX_FILE_SIZE: process.env.MAX_FILE_SIZE || 10 * 1024 * 1024, // 10MB
    ALLOWED_FILE_TYPES: process.env.ALLOWED_FILE_TYPES || 'jpg,jpeg,png,pdf,doc,docx',

    // AI configuration
    OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
    OPENAI_MODEL: process.env.OPENAI_MODEL || 'gpt-4',

    // Blockchain configuration
    POLKADOT_ENDPOINT: process.env.POLKADOT_ENDPOINT || 'wss://rpc.polkadot.io',
    MOONBEAM_ENDPOINT: process.env.MOONBEAM_ENDPOINT || 'https://rpc.api.moonbeam.network',
    BSC_ENDPOINT: process.env.BSC_ENDPOINT || 'https://bsc-dataseed.binance.org',

    // Rate limiting
    RATE_LIMIT_WINDOW: process.env.RATE_LIMIT_WINDOW || 15 * 60 * 1000, // 15 minutes
    RATE_LIMIT_MAX: process.env.RATE_LIMIT_MAX || 100,

    // Security
    CORS_ORIGIN: process.env.CORS_ORIGIN || 'https://emo.com',
    SESSION_SECRET: process.env.SESSION_SECRET || 'emo-session-secret',

    // Database
    DB_NAME: process.env.DB_NAME || 'emo_prod',
    DB_HOST: process.env.DB_HOST || 'localhost',
    DB_PORT: process.env.DB_PORT || 27017,
    DB_USER: process.env.DB_USER || '',
    DB_PASS: process.env.DB_PASS || '',
  }
};

const currentEnv = process.env.NODE_ENV || 'development';
const config = environments[currentEnv];

// Validate required environment variables
const requiredEnvVars = [
  'JWT_SECRET',
  'MONGODB_URI'
];

const missingVars = requiredEnvVars.filter(varName => !config[varName]);

if (missingVars.length > 0) {
  console.error('Missing required environment variables:', missingVars);
  process.exit(1);
}

module.exports = config;
