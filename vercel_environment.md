# EHB-5 Vercel Environment Configuration

## 🌍 Environment Variables Setup

This document provides complete environment configuration for deploying EHB-5 on Vercel.

### 📋 Required Environment Variables

Set these variables in your Vercel project settings:

| Variable | Value | Description | Required |
|----------|-------|-------------|----------|
| `EHB5_ENVIRONMENT` | `production` | Application environment | ✅ |
| `EHB5_HOST` | `0.0.0.0` | Host binding for serverless | ✅ |
| `EHB5_PORT` | `5000` | API server port | ✅ |
| `EHB5_DASHBOARD_PORT` | `8000` | Dashboard port | ✅ |
| `JWT_SECRET` | `your-secure-secret-here` | JWT token signing secret | ✅ |
| `DATABASE_PATH` | `ehb5.db` | SQLite database path | ✅ |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) | ✅ |
| `DEBUG` | `false` | Debug mode (true/false) | ✅ |

### 🔐 Security Variables

For production deployment, use strong, unique values:

```bash

## JWT Secret (generate a strong random string)

JWT_SECRET=ehb5-production-jwt-secret-2024-$(openssl rand -hex 32)

## Environment

EHB5_ENVIRONMENT=production

## Debug mode (should be false in production)

DEBUG=false

```

### 🚀 Vercel Dashboard Setup

#### Step 1: Access Environment Variables

1. Go to your Vercel project dashboard
2. Click on "Settings" tab
3. Select "Environment Variables" from the left sidebar

#### Step 2: Add Variables

Add each variable with the following settings:

| Variable | Value | Environment | Description |
|----------|-------|-------------|-------------|
| `EHB5_ENVIRONMENT` | `production` | Production, Preview, Development | App environment |
| `EHB5_HOST` | `0.0.0.0` | Production, Preview, Development | Server host |
| `EHB5_PORT` | `5000` | Production, Preview, Development | API port |
| `EHB5_DASHBOARD_PORT` | `8000` | Production, Preview, Development | Dashboard port |
| `JWT_SECRET` | `your-secure-secret` | Production, Preview, Development | JWT secret |
| `DATABASE_PATH` | `ehb5.db` | Production, Preview, Development | Database path |
| `LOG_LEVEL` | `INFO` | Production, Preview, Development | Log level |
| `DEBUG` | `false` | Production, Preview, Development | Debug mode |

#### Step 3: Environment Selection

For each variable, select:

- ✅ **Production**: Deployed to production
- ✅ **Preview**: Deployed to preview branches
- ✅ **Development**: Local development

### 🔧 Environment-Specific Configurations

#### Production Environment

```bash

EHB5_ENVIRONMENT=production
EHB5_HOST=0.0.0.0
EHB5_PORT=5000
EHB5_DASHBOARD_PORT=8000
JWT_SECRET=your-production-secret-here
DATABASE_PATH=ehb5.db
LOG_LEVEL=INFO
DEBUG=false

```

#### Preview Environment

```bash

EHB5_ENVIRONMENT=preview
EHB5_HOST=0.0.0.0
EHB5_PORT=5000
EHB5_DASHBOARD_PORT=8000
JWT_SECRET=your-preview-secret-here
DATABASE_PATH=ehb5.db
LOG_LEVEL=INFO
DEBUG=false

```

#### Development Environment

```bash

EHB5_ENVIRONMENT=development
EHB5_HOST=0.0.0.0
EHB5_PORT=5000
EHB5_DASHBOARD_PORT=8000
JWT_SECRET=your-dev-secret-here
DATABASE_PATH=ehb5.db
LOG_LEVEL=DEBUG
DEBUG=true

```

### 🔍 Environment Validation

#### Test Environment Variables

```bash

## Test health endpoint

curl https://your-project-name.vercel.app/api/health

## Expected response

{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "version": "2.0.0",
  "environment": "production",
  "deployment": "vercel"
}

```

#### Validate Environment in Code

```python

import os

## Check environment variables

environment = os.getenv('EHB5_ENVIRONMENT', 'development')
debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
jwt_secret = os.getenv('JWT_SECRET', 'default-secret')

print(f"Environment: {environment}")
print(f"Debug Mode: {debug_mode}")
print(f"JWT Secret Set: {bool(jwt_secret)}")

```

### 🛡️ Security Best Practices

#### 1. JWT Secret Generation

```bash

## Generate a secure JWT secret

openssl rand -hex 32

## Or use Python

python -c "import secrets; print(secrets.token_hex(32))"

```

#### 2. Environment Variable Security

- ✅ Use different secrets for each environment
- ✅ Never commit secrets to version control
- ✅ Rotate secrets regularly
- ✅ Use Vercel's secret management

#### 3. Database Security

```bash

## For production, consider using external database

DATABASE_URL=postgresql://user:password@host:port/database

```

### 📊 Monitoring Environment Variables

#### Check Variable Status

```bash

## Test environment variables via API

curl https://your-project-name.vercel.app/api/system/status

## Expected response includes environment info

{
  "status": "operational",
  "environment": "production",
  "deployment": "vercel",
  "components": {
    "database": "healthy",
    "api": "healthy",
    "ai_agents": "active"
  }
}

```

#### Environment Health Check

```python

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'EHB5_ENVIRONMENT',
        'JWT_SECRET',
        'DATABASE_PATH',
        'LOG_LEVEL'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        return {
            "status": "error",
            "missing_variables": missing_vars
        }

    return {
        "status": "healthy",
        "environment": os.getenv('EHB5_ENVIRONMENT'),
        "debug_mode": os.getenv('DEBUG', 'false').lower() == 'true'
    }

```

### 🔄 Environment Updates

#### Update Environment Variables

1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Edit the variable value
3. Click "Save"
4. Redeploy the project

#### Redeploy After Changes

```bash

## Trigger redeploy via Vercel CLI

vercel --prod

## Or via GitHub push

git push origin main

```

### 🚨 Troubleshooting

#### Common Issues

1. **Missing Environment Variables**

   ```bash

   # Check if variables are set
   curl https://your-project-name.vercel.app/api/health

   ```

2. **Invalid JWT Secret**

   ```bash

   # Test authentication
   curl -X POST https://your-project-name.vercel.app/api/auth/login \
     - H "Content-Type: application/json" \
     - d '{"username": "admin", "password": "admin123"}'

   ```

3. **Database Issues**

   ```bash

   # Check database status
   curl https://your-project-name.vercel.app/api/system/status

   ```

#### Debug Mode

```bash

## Enable debug mode for troubleshooting

DEBUG=true
LOG_LEVEL=DEBUG

```

### 📈 Environment Monitoring

#### Health Check Endpoint

```bash

## Monitor environment health

curl https://your-project-name.vercel.app/api/health

```

#### System Status Endpoint

```bash

## Get detailed system status

curl https://your-project-name.vercel.app/api/system/status

```

#### Logs Endpoint

```bash

## Get system logs

curl https://your-project-name.vercel.app/api/system/logs?level=INFO&limit=10

```

### 🎯 Environment Optimization

#### Performance Settings

```bash

## Optimize for production

EHB5_ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

```

#### Development Settings

```bash

## Optimize for development

EHB5_ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

```

### 📞 Support

For environment variable issues:

1. **Check Vercel Logs**: Dashboard → Functions → View Logs
2. **Verify Variables**: Dashboard → Settings → Environment Variables
3. **Test Locally**: Use `.env` file for local testing
4. **Contact Support**: Vercel support for platform issues

### 🔗 Related Documentation

- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes/python)
- [EHB-5 API Documentation](./api_documentation.py)
- [Vercel Deployment Guide](./vercel_deployment.md)
