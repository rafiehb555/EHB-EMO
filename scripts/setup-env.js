#!/usr/bin/env node
/**
 * EHB Healthcare - Environment Setup Script
 * Automatically creates .env.local from .env.example
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class EnvironmentSetup {
  constructor() {
    this.projectRoot = process.cwd();
    this.envExamplePath = path.join(this.projectRoot, '.env.example');
    this.envLocalPath = path.join(this.projectRoot, '.env.local');
  }

  /**
   * Generate secure random keys
   */
  generateSecureKey(length = 32) {
    return crypto.randomBytes(length).toString('hex');
  }

  /**
   * Generate JWT secret
   */
  generateJWTSecret() {
    return crypto.randomBytes(64).toString('hex');
  }

  /**
   * Generate encryption key
   */
  generateEncryptionKey() {
    return crypto.randomBytes(32).toString('base64');
  }

  /**
   * Check if .env.example exists
   */
  checkEnvExample() {
    if (!fs.existsSync(this.envExamplePath)) {
      console.error('❌ .env.example file not found!');
      console.log('📝 Creating .env.example file...');
      this.createEnvExample();
      return false;
    }
    return true;
  }

  /**
   * Create .env.example if it doesn't exist
   */
  createEnvExample() {
    const envExampleContent = `# ========================================
# EHB Healthcare System - Environment Variables
# ========================================
# Copy this file to .env.local and update the values

# ========================================
# DATABASE CONFIGURATION
# ========================================
DATABASE_URL="postgresql://username:password@localhost:5432/ehb_healthcare"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
DATABASE_NAME="ehb_healthcare"
DATABASE_USER="postgres"
DATABASE_PASSWORD="your-database-password"

# ========================================
# API CONFIGURATION
# ========================================
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_APP_NAME="EHB Healthcare"
NEXT_PUBLIC_APP_VERSION="2.0.0"
API_PORT="8000"
API_HOST="0.0.0.0"

# ========================================
# FRONTEND CONFIGURATION
# ========================================
NEXT_PUBLIC_FRONTEND_URL="http://localhost:3001"
FRONTEND_PORT="3001"
NEXT_PUBLIC_APP_ENVIRONMENT="development"

# ========================================
# AI & EXTERNAL SERVICES
# ========================================
OPENAI_API_KEY="your-openai-api-key-here"
OPENAI_MODEL="gpt-4"
GEMINI_API_KEY="your-gemini-api-key-here"
ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# ========================================
# AWS CONFIGURATION
# ========================================
AWS_ACCESS_KEY_ID="your-aws-access-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
AWS_REGION="us-east-1"
AWS_S3_BUCKET="ehb-healthcare-data"

# ========================================
# HEALTHCARE COMPLIANCE
# ========================================
HIPAA_COMPLIANCE="enabled"
ENCRYPTION_KEY="your-32-character-encryption-key-here"
AUDIT_LOGGING="enabled"
DATA_RETENTION_DAYS="2555"
BREACH_DETECTION="enabled"

# ========================================
# SECURITY CONFIGURATION
# ========================================
JWT_SECRET="your-jwt-secret-key-here"
SESSION_SECRET="your-session-secret-key-here"
BCRYPT_ROUNDS="12"
CORS_ORIGIN="http://localhost:3001"

# ========================================
# MONITORING & ANALYTICS
# ========================================
SENTRY_DSN="your-sentry-dsn-here"
GOOGLE_ANALYTICS_ID="your-ga-id-here"
MIXPANEL_TOKEN="your-mixpanel-token-here"

# ========================================
# EMAIL & NOTIFICATIONS
# ========================================
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
SENDGRID_API_KEY="your-sendgrid-api-key"

# ========================================
# PAYMENT PROCESSING
# ========================================
STRIPE_PUBLISHABLE_KEY="pk_test_your-stripe-key"
STRIPE_SECRET_KEY="sk_test_your-stripe-secret"
PAYPAL_CLIENT_ID="your-paypal-client-id"
PAYPAL_CLIENT_SECRET="your-paypal-secret"

# ========================================
# TELEMEDICINE & VIDEO
# ========================================
TWILIO_ACCOUNT_SID="your-twilio-sid"
TWILIO_AUTH_TOKEN="your-twilio-token"
TWILIO_API_KEY="your-twilio-api-key"
TWILIO_API_SECRET="your-twilio-api-secret"

# ========================================
# DEVELOPMENT SETTINGS
# ========================================
NODE_ENV="development"
DEBUG="ehb:*"
LOG_LEVEL="info"
ENABLE_SWAGGER="true"
ENABLE_GRAPHIQL="true"

# ========================================
# TESTING CONFIGURATION
# ========================================
TEST_DATABASE_URL="postgresql://test_user:test_pass@localhost:5432/ehb_test"
TEST_API_URL="http://localhost:8001"
COVERAGE_THRESHOLD="80"

# ========================================
# DEPLOYMENT CONFIGURATION
# ========================================
DEPLOYMENT_ENVIRONMENT="staging"
DOCKER_REGISTRY="your-registry.com"
KUBERNETES_NAMESPACE="ehb-healthcare"
HELM_CHART_VERSION="1.0.0"

# ========================================
# BACKUP & RECOVERY
# ========================================
BACKUP_SCHEDULE="0 2 * * *"
BACKUP_RETENTION_DAYS="30"
BACKUP_S3_BUCKET="ehb-backups"
RESTORE_POINT_ENABLED="true"

# ========================================
# PERFORMANCE & CACHING
# ========================================
REDIS_URL="redis://localhost:6379"
REDIS_PASSWORD="your-redis-password"
CACHE_TTL="3600"
RATE_LIMIT_WINDOW="900000"
RATE_LIMIT_MAX_REQUESTS="100"

# ========================================
# FEATURE FLAGS
# ========================================
ENABLE_AI_DIAGNOSIS="true"
ENABLE_TELEMEDICINE="true"
ENABLE_PAYMENT_PROCESSING="true"
ENABLE_ANALYTICS="true"
ENABLE_NOTIFICATIONS="true"
ENABLE_AUDIT_LOGGING="true"

# ========================================
# INTEGRATION KEYS
# ========================================
GOOGLE_MAPS_API_KEY="your-google-maps-key"
WEATHER_API_KEY="your-weather-api-key"
PHARMACY_API_KEY="your-pharmacy-api-key"
INSURANCE_API_KEY="your-insurance-api-key"

# ========================================
# MONITORING ENDPOINTS
# ========================================
HEALTH_CHECK_URL="/api/health"
METRICS_ENDPOINT="/api/metrics"
STATUS_ENDPOINT="/api/status"

# ========================================
# DOCUMENTATION
# ========================================
# Copy this file to .env.local
# Update all values with your actual credentials
# Never commit .env.local to version control
# Use different values for development, staging, and production
`;

    fs.writeFileSync(this.envExamplePath, envExampleContent);
    console.log('✅ .env.example file created successfully!');
  }

  /**
   * Create .env.local from .env.example
   */
  createEnvLocal() {
    if (!this.checkEnvExample()) {
      return;
    }

    if (fs.existsSync(this.envLocalPath)) {
      console.log('⚠️  .env.local already exists. Skipping creation.');
      return;
    }

    try {
      // Read .env.example
      const envExampleContent = fs.readFileSync(this.envExamplePath, 'utf8');
      
      // Replace placeholder values with generated ones
      let envLocalContent = envExampleContent
        .replace(/your-jwt-secret-key-here/g, this.generateJWTSecret())
        .replace(/your-session-secret-key-here/g, this.generateSecureKey(32))
        .replace(/your-32-character-encryption-key-here/g, this.generateEncryptionKey())
        .replace(/your-database-password/g, this.generateSecureKey(16))
        .replace(/your-redis-password/g, this.generateSecureKey(16));

      // Write .env.local
      fs.writeFileSync(this.envLocalPath, envLocalContent);
      console.log('✅ .env.local file created successfully!');
      console.log('📝 Please update the API keys and other credentials as needed.');
      
    } catch (error) {
      console.error('❌ Error creating .env.local:', error.message);
    }
  }

  /**
   * Validate environment variables
   */
  validateEnvironment() {
    if (!fs.existsSync(this.envLocalPath)) {
      console.error('❌ .env.local file not found!');
      console.log('📝 Run: npm run env:setup');
      return false;
    }

    const envContent = fs.readFileSync(this.envLocalPath, 'utf8');
    const requiredVars = [
      'DATABASE_URL',
      'NEXT_PUBLIC_API_URL',
      'JWT_SECRET',
      'ENCRYPTION_KEY',
      'NODE_ENV'
    ];

    const missingVars = [];
    requiredVars.forEach(varName => {
      if (!envContent.includes(varName)) {
        missingVars.push(varName);
      }
    });

    if (missingVars.length > 0) {
      console.error('❌ Missing required environment variables:', missingVars);
      return false;
    }

    console.log('✅ Environment validation passed!');
    return true;
  }

  /**
   * Run the setup
   */
  run() {
    console.log('🏥 EHB Healthcare - Environment Setup');
    console.log('=====================================');
    
    this.createEnvLocal();
    this.validateEnvironment();
    
    console.log('\n📋 Next Steps:');
    console.log('1. Update API keys in .env.local');
    console.log('2. Configure database connection');
    console.log('3. Set up external services');
    console.log('4. Run: npm run dev');
  }
}

// Run if called directly
if (require.main === module) {
  const setup = new EnvironmentSetup();
  setup.run();
}

module.exports = EnvironmentSetup; 