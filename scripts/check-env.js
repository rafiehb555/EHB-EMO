#!/usr/bin/env node
/**
 * EHB Healthcare - Environment Check Script
 * Validates environment variables and configuration
 */

const fs = require('fs');
const path = require('path');

class EnvironmentChecker {
  constructor() {
    this.projectRoot = process.cwd();
    this.envLocalPath = path.join(this.projectRoot, '.env.local');
    this.envExamplePath = path.join(this.projectRoot, '.env.example');
  }

  /**
   * Check if .env.local exists
   */
  checkEnvLocalExists() {
    if (!fs.existsSync(this.envLocalPath)) {
      console.error('❌ .env.local file not found!');
      console.log('📝 Run: npm run env:setup');
      return false;
    }
    console.log('✅ .env.local file found');
    return true;
  }

  /**
   * Parse environment variables
   */
  parseEnvFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const envVars = {};
    
    content.split('\n').forEach(line => {
      line = line.trim();
      if (line && !line.startsWith('#')) {
        const [key, value] = line.split('=');
        if (key && value) {
          envVars[key.trim()] = value.trim().replace(/"/g, '');
        }
      }
    });
    
    return envVars;
  }

  /**
   * Check required environment variables
   */
  checkRequiredVariables() {
    const envVars = this.parseEnvFile(this.envLocalPath);
    
    const requiredVars = {
      'DATABASE_URL': 'Database connection string',
      'NEXT_PUBLIC_API_URL': 'API server URL',
      'JWT_SECRET': 'JWT signing secret',
      'ENCRYPTION_KEY': 'Data encryption key',
      'NODE_ENV': 'Node environment',
      'HIPAA_COMPLIANCE': 'HIPAA compliance setting',
      'AUDIT_LOGGING': 'Audit logging setting'
    };

    const missingVars = [];
    const placeholderVars = [];

    Object.entries(requiredVars).forEach(([varName, description]) => {
      if (!envVars[varName]) {
        missingVars.push({ name: varName, description });
      } else if (envVars[varName].includes('your-') || envVars[varName].includes('placeholder')) {
        placeholderVars.push({ name: varName, description });
      }
    });

    if (missingVars.length > 0) {
      console.error('❌ Missing required environment variables:');
      missingVars.forEach(({ name, description }) => {
        console.error(`   - ${name}: ${description}`);
      });
      return false;
    }

    if (placeholderVars.length > 0) {
      console.warn('⚠️  Environment variables with placeholder values:');
      placeholderVars.forEach(({ name, description }) => {
        console.warn(`   - ${name}: ${description}`);
      });
    }

    console.log('✅ All required environment variables found');
    return true;
  }

  /**
   * Check security configuration
   */
  checkSecurityConfig() {
    const envVars = this.parseEnvFile(this.envLocalPath);
    
    const securityChecks = [
      {
        name: 'JWT_SECRET',
        condition: envVars.JWT_SECRET && envVars.JWT_SECRET.length >= 32,
        message: 'JWT secret should be at least 32 characters'
      },
      {
        name: 'ENCRYPTION_KEY',
        condition: envVars.ENCRYPTION_KEY && envVars.ENCRYPTION_KEY.length >= 32,
        message: 'Encryption key should be at least 32 characters'
      },
      {
        name: 'HIPAA_COMPLIANCE',
        condition: envVars.HIPAA_COMPLIANCE === 'enabled',
        message: 'HIPAA compliance should be enabled'
      },
      {
        name: 'AUDIT_LOGGING',
        condition: envVars.AUDIT_LOGGING === 'enabled',
        message: 'Audit logging should be enabled'
      }
    ];

    let allPassed = true;
    securityChecks.forEach(check => {
      if (!check.condition) {
        console.error(`❌ Security: ${check.name} - ${check.message}`);
        allPassed = false;
      }
    });

    if (allPassed) {
      console.log('✅ Security configuration is valid');
    }

    return allPassed;
  }

  /**
   * Check API configuration
   */
  checkAPIConfig() {
    const envVars = this.parseEnvFile(this.envLocalPath);
    
    const apiChecks = [
      {
        name: 'NEXT_PUBLIC_API_URL',
        condition: envVars.NEXT_PUBLIC_API_URL && envVars.NEXT_PUBLIC_API_URL.startsWith('http'),
        message: 'API URL should be a valid HTTP URL'
      },
      {
        name: 'API_PORT',
        condition: envVars.API_PORT && !isNaN(envVars.API_PORT),
        message: 'API port should be a valid number'
      },
      {
        name: 'NEXT_PUBLIC_APP_NAME',
        condition: envVars.NEXT_PUBLIC_APP_NAME,
        message: 'App name should be set'
      }
    ];

    let allPassed = true;
    apiChecks.forEach(check => {
      if (!check.condition) {
        console.error(`❌ API Config: ${check.name} - ${check.message}`);
        allPassed = false;
      }
    });

    if (allPassed) {
      console.log('✅ API configuration is valid');
    }

    return allPassed;
  }

  /**
   * Check database configuration
   */
  checkDatabaseConfig() {
    const envVars = this.parseEnvFile(this.envLocalPath);
    
    if (!envVars.DATABASE_URL) {
      console.error('❌ Database: DATABASE_URL is required');
      return false;
    }

    if (!envVars.DATABASE_URL.includes('postgresql://')) {
      console.error('❌ Database: DATABASE_URL should be a PostgreSQL connection string');
      return false;
    }

    console.log('✅ Database configuration is valid');
    return true;
  }

  /**
   * Check development settings
   */
  checkDevelopmentSettings() {
    const envVars = this.parseEnvFile(this.envLocalPath);
    
    const devChecks = [
      {
        name: 'NODE_ENV',
        condition: ['development', 'production', 'test'].includes(envVars.NODE_ENV),
        message: 'NODE_ENV should be development, production, or test'
      },
      {
        name: 'LOG_LEVEL',
        condition: ['debug', 'info', 'warn', 'error'].includes(envVars.LOG_LEVEL),
        message: 'LOG_LEVEL should be debug, info, warn, or error'
      }
    ];

    let allPassed = true;
    devChecks.forEach(check => {
      if (!check.condition) {
        console.error(`❌ Development: ${check.name} - ${check.message}`);
        allPassed = false;
      }
    });

    if (allPassed) {
      console.log('✅ Development settings are valid');
    }

    return allPassed;
  }

  /**
   * Generate environment report
   */
  generateReport() {
    const envVars = this.parseEnvFile(this.envLocalPath);
    
    const report = {
      timestamp: new Date().toISOString(),
      totalVariables: Object.keys(envVars).length,
      categories: {
        database: 0,
        api: 0,
        security: 0,
        monitoring: 0,
        healthcare: 0,
        development: 0
      }
    };

    Object.keys(envVars).forEach(key => {
      if (key.includes('DATABASE') || key.includes('DB')) {
        report.categories.database++;
      } else if (key.includes('API') || key.includes('NEXT_PUBLIC')) {
        report.categories.api++;
      } else if (key.includes('SECRET') || key.includes('KEY') || key.includes('ENCRYPTION')) {
        report.categories.security++;
      } else if (key.includes('SENTRY') || key.includes('ANALYTICS') || key.includes('MONITORING')) {
        report.categories.monitoring++;
      } else if (key.includes('HIPAA') || key.includes('AUDIT') || key.includes('COMPLIANCE')) {
        report.categories.healthcare++;
      } else {
        report.categories.development++;
      }
    });

    return report;
  }

  /**
   * Run all checks
   */
  run() {
    console.log('🏥 EHB Healthcare - Environment Check');
    console.log('=====================================');
    
    const checks = [
      { name: 'Environment File', check: () => this.checkEnvLocalExists() },
      { name: 'Required Variables', check: () => this.checkRequiredVariables() },
      { name: 'Security Config', check: () => this.checkSecurityConfig() },
      { name: 'API Config', check: () => this.checkAPIConfig() },
      { name: 'Database Config', check: () => this.checkDatabaseConfig() },
      { name: 'Development Settings', check: () => this.checkDevelopmentSettings() }
    ];

    let passedChecks = 0;
    checks.forEach(({ name, check }) => {
      console.log(`\n🔍 Checking ${name}...`);
      if (check()) {
        passedChecks++;
      }
    });

    console.log('\n📊 Summary:');
    console.log(`✅ Passed: ${passedChecks}/${checks.length} checks`);
    
    if (passedChecks === checks.length) {
      console.log('🎉 Environment is properly configured!');
      
      const report = this.generateReport();
      console.log(`📈 Total variables: ${report.totalVariables}`);
      console.log(`📁 Categories: ${Object.keys(report.categories).join(', ')}`);
    } else {
      console.log('⚠️  Please fix the issues above before proceeding.');
    }
  }
}

// Run if called directly
if (require.main === module) {
  const checker = new EnvironmentChecker();
  checker.run();
}

module.exports = EnvironmentChecker; 