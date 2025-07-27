// EMO Business Management System - Environment Configuration

const config = {
  // Application Settings
  app: {
    name: 'EMO Business Management System',
    version: '1.0.0',
    port: process.env.PORT || 3000,
    environment: process.env.NODE_ENV || 'development',
    frontendUrl: process.env.FRONTEND_URL || 'http://localhost:6000',
    adminUrl: process.env.ADMIN_URL || 'http://localhost:6001',
    aiUrl: process.env.AI_URL || 'http://localhost:5001',
    blockchainUrl: process.env.BLOCKCHAIN_URL || 'http://localhost:5002',
  },

  // Database Configuration
  database: {
    uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/emo-business',
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      maxPoolSize: 10,
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
    },
  },

  // JWT Authentication
  jwt: {
    secret: process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-this-in-production',
    expiresIn: process.env.JWT_EXPIRES_IN || '24h',
    refreshSecret: process.env.JWT_REFRESH_SECRET || 'your-refresh-token-secret',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d',
  },

  // Email Configuration
  email: {
    host: process.env.EMAIL_HOST || 'smtp.gmail.com',
    port: process.env.EMAIL_PORT || 587,
    user: process.env.EMAIL_USER || 'your-email@gmail.com',
    pass: process.env.EMAIL_PASS || 'your-app-password',
    from: process.env.EMAIL_FROM || 'noreply@emo-business.com',
  },

  // SMS Configuration (Twilio)
  sms: {
    accountSid: process.env.TWILIO_ACCOUNT_SID || 'your-twilio-account-sid',
    authToken: process.env.TWILIO_AUTH_TOKEN || 'your-twilio-auth-token',
    phoneNumber: process.env.TWILIO_PHONE_NUMBER || '+1234567890',
  },

  // File Storage (AWS S3)
  storage: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'your-aws-access-key',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'your-aws-secret-key',
    region: process.env.AWS_REGION || 'us-east-1',
    bucket: process.env.AWS_S3_BUCKET || 'emo-business-documents',
    bucketUrl: process.env.AWS_S3_BUCKET_URL || 'https://emo-business-documents.s3.amazonaws.com',
  },

  // AI Services (OpenAI)
  ai: {
    apiKey: process.env.OPENAI_API_KEY || 'your-openai-api-key',
    model: process.env.OPENAI_MODEL || 'gpt-4',
    maxTokens: process.env.OPENAI_MAX_TOKENS || 2000,
  },

  // Blockchain Configuration
  blockchain: {
    polkadot: {
      rpcUrl: process.env.POLKADOT_RPC_URL || 'wss://rpc.polkadot.io',
      privateKey: process.env.POLKADOT_PRIVATE_KEY || 'your-polkadot-private-key',
    },
    moonbeam: {
      rpcUrl: process.env.MOONBEAM_RPC_URL || 'wss://wss.api.moonbeam.network',
      privateKey: process.env.MOONBEAM_PRIVATE_KEY || 'your-moonbeam-private-key',
    },
    bsc: {
      rpcUrl: process.env.BSC_RPC_URL || 'https://bsc-dataseed.binance.org',
    },
  },

  // Redis Configuration
  redis: {
    url: process.env.REDIS_URL || 'redis://localhost:6379',
    password: process.env.REDIS_PASSWORD || 'your-redis-password',
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    filePath: process.env.LOG_FILE_PATH || './logs',
  },

  // Security
  security: {
    bcryptRounds: parseInt(process.env.BCRYPT_ROUNDS) || 12,
    rateLimitWindowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 900000,
    rateLimitMaxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
    slowDownDelayMs: parseInt(process.env.SLOW_DOWN_DELAY_MS) || 500,
  },

  // Business Rules
  business: {
    verificationTimeoutHours: parseInt(process.env.VERIFICATION_TIMEOUT_HOURS) || 24,
    complaintEscalationHours: parseInt(process.env.COMPLAINT_ESCALATION_HOURS) || 6,
    sqlUpgradeCooldownDays: parseInt(process.env.SQL_UPGRADE_COOLDOWN_DAYS) || 30,
    maxFileSizeMb: parseInt(process.env.MAX_FILE_SIZE_MB) || 10,
    allowedFileTypes: (process.env.ALLOWED_FILE_TYPES || 'pdf,jpg,jpeg,png,doc,docx').split(','),
  },

  // Payment Configuration
  payment: {
    stripe: {
      secretKey: process.env.STRIPE_SECRET_KEY || 'your-stripe-secret-key',
      publishableKey: process.env.STRIPE_PUBLISHABLE_KEY || 'your-stripe-publishable-key',
      webhookSecret: process.env.STRIPE_WEBHOOK_SECRET || 'your-stripe-webhook-secret',
    },
  },

  // Monitoring
  monitoring: {
    sentryDsn: process.env.SENTRY_DSN || 'your-sentry-dsn',
    newRelicLicenseKey: process.env.NEW_RELIC_LICENSE_KEY || 'your-new-relic-key',
  },

  // Development
  development: {
    debug: process.env.DEBUG === 'true' || false,
    enableSwagger: process.env.ENABLE_SWAGGER === 'true' || false,
    enableLogging: process.env.ENABLE_LOGGING === 'true' || true,
  },
};

// Validate required configuration
const validateConfig = () => {
  const required = [
    'jwt.secret',
    'database.uri',
    'email.user',
    'email.pass',
  ];

  const missing = required.filter(key => {
    const value = key.split('.').reduce((obj, k) => obj?.[k], config);
    return !value || value.includes('your-');
  });

  if (missing.length > 0) {
    console.warn('⚠️  Missing or default configuration values:', missing);
    console.warn('Please update your environment variables for production use.');
  }
};

// Export configuration
module.exports = {
  ...config,
  validateConfig,
}; 