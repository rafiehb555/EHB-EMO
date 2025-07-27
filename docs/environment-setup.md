# EHB Healthcare - Environment Setup Guide

## Overview

This guide explains how to set up the environment variables for the EHB
Healthcare platform using the `.env.example` file.

## Quick Setup

### 1. Automatic Setup

```bash

# Run the automatic environment setup

npm run setup

# Or run individual commands

npm run env:setup    # Creates .env.local from .env.example

npm run env:check    # Validates environment configuration

```

### 2. Manual Setup

```bash

# Copy the example file

cp .env.example .env.local

# Edit the file with your actual values

nano .env.local
```

## Environment Variables Categories

### Database Configuration

```env
DATABASE_URL="postgresql://username:password@localhost:5432/ehb_healthcare"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
DATABASE_NAME="ehb_healthcare"
DATABASE_USER="postgres"
DATABASE_PASSWORD="your-database-password"
```

**Required for:** Patient data storage, medical records, analytics

### API Configuration

```env
NEXT_PUBLIC_API_URL="<http://localhost:8000">
NEXT_PUBLIC_APP_NAME="EHB Healthcare"
NEXT_PUBLIC_APP_VERSION="2.0.0"
API_PORT="8000"
API_HOST="0.0.0.0"
```

**Required for:** Frontend-backend communication, API endpoints

### Security Configuration

```env
JWT_SECRET="your-jwt-secret-key-here"
SESSION_SECRET="your-session-secret-key-here"
ENCRYPTION_KEY="your-32-character-encryption-key-here"
BCRYPT_ROUNDS="12"
CORS_ORIGIN="<http://localhost:3001">
```

**Required for:** User authentication, data encryption, security compliance

### Healthcare Compliance

```env
HIPAA_COMPLIANCE="enabled"
AUDIT_LOGGING="enabled"
DATA_RETENTION_DAYS="2555"
BREACH_DETECTION="enabled"
```

**Required for:** HIPAA compliance, audit trails, data protection

### AI & External Services

```env
OPENAI_API_KEY="your-openai-api-key-here"
OPENAI_MODEL="gpt-4"
GEMINI_API_KEY="your-gemini-api-key-here"
ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

**Required for:** AI-powered diagnosis, medical insights, automation

### AWS Configuration

```env
AWS_ACCESS_KEY_ID="your-aws-access-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
AWS_REGION="us-east-1"
AWS_S3_BUCKET="ehb-healthcare-data"
```

**Required for:** File storage, backups, cloud services

### Email & Notifications

```env
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
SENDGRID_API_KEY="your-sendgrid-api-key"
```

**Required for:** Patient notifications, appointment reminders, alerts

### Payment Processing

```env
STRIPE_PUBLISHABLE_KEY="pk_test_your-stripe-key"
STRIPE_SECRET_KEY="sk_test_your-stripe-secret"
PAYPAL_CLIENT_ID="your-paypal-client-id"
PAYPAL_CLIENT_SECRET="your-paypal-secret"
```

**Required for:** Payment processing, billing, insurance claims

### Telemedicine & Video

```env
TWILIO_ACCOUNT_SID="your-twilio-sid"
TWILIO_AUTH_TOKEN="your-twilio-token"
TWILIO_API_KEY="your-twilio-api-key"
TWILIO_API_SECRET="your-twilio-api-secret"
```

**Required for:** Video consultations, telemedicine features

## Environment Validation

### Automatic Validation

```bash
npm run env:check
```

This command checks:

- ✅ Required variables are present

- ✅ Security keys are properly configured

- ✅ Database connection is valid

- ✅ API configuration is correct

- ✅ Healthcare compliance settings

- ✅ Development environment settings

### Manual Validation Checklist

#### Security Requirements

- [ ] JWT_SECRET is at least 32 characters

- [ ] ENCRYPTION_KEY is at least 32 characters

- [ ] HIPAA_COMPLIANCE is set to "enabled"

- [ ] AUDIT_LOGGING is set to "enabled"

#### Database Requirements

- [ ] DATABASE_URL is a valid PostgreSQL connection string

- [ ] Database credentials are correct

- [ ] Database server is accessible

#### API Requirements

- [ ] NEXT_PUBLIC_API_URL is a valid HTTP URL

- [ ] API_PORT is a valid number

- [ ] CORS_ORIGIN matches your frontend URL

#### Healthcare Requirements

- [ ] All HIPAA compliance settings are enabled

- [ ] Data retention policies are configured

- [ ] Breach detection is enabled

## Environment-Specific Configurations

### Development Environment

```env
NODE_ENV="development"
DEBUG="ehb:*"
LOG_LEVEL="debug"
ENABLE_SWAGGER="true"
ENABLE_GRAPHIQL="true"
```

### Production Environment

```env
NODE_ENV="production"
LOG_LEVEL="info"
ENABLE_SWAGGER="false"
ENABLE_GRAPHIQL="false"
HIPAA_COMPLIANCE="enabled"
AUDIT_LOGGING="enabled"
```

### Testing Environment

```env
NODE_ENV="test"
TEST_DATABASE_URL="postgresql://test_user:test_pass@localhost:5432/ehb_test"
TEST_API_URL="<http://localhost:8001">
COVERAGE_THRESHOLD="80"
```

## Security Best Practices

### 1. Never Commit Secrets

```bash

# Add to .gitignore

.env.local
.env.production
.env.staging
```

### 2. Use Strong Secrets

```bash

# Generate secure keys

node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### 3. Rotate Keys Regularly

- JWT secrets: Every 90 days

- Encryption keys: Every 180 days

- API keys: As needed

### 4. Environment Isolation

- Use different databases for each environment

- Separate API keys for development/production

- Isolate patient data between environments

## Troubleshooting

### Common Issues

#### 1. Missing Environment File

```bash
Error: .env.local file not found!
Solution: npm run env:setup
```

#### 2. Invalid Database Connection

```bash
Error: Database connection failed
Solution: Check DATABASE_URL and credentials
```

#### 3. Security Validation Failed

```bash
Error: JWT_SECRET too short
Solution: Generate a new 32+ character secret

```

#### 4. API Configuration Error

```bash
Error: Invalid API URL
Solution: Ensure NEXT_PUBLIC_API_URL is a valid HTTP URL
```

### Debug Commands

```bash

# Check environment variables

npm run env:check

# Validate specific category

node scripts/check-env.js --category=security

# Generate environment report

node scripts/check-env.js --report
```

## Next Steps

After setting up your environment:

1. **Install Dependencies**
   ```bash

   npm install
   ```

2. **Setup Database**
   ```bash

   npm run db:setup
   ```

3. **Start Development Server**
   ```bash

   npm run dev
   ```

4. **Run Tests**
   ```bash

   npm test
   ```

## Support

For environment setup issues:

- Check the troubleshooting section above

- Review the validation output

- Contact the development team

- Check the project documentation

## Security Notice

⚠️ **Important:** Never commit `.env.local` or any file containing real
credentials to version control. Always use `.env.example` as a template and keep
actual credentials secure.