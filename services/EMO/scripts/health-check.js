#!/usr/bin/env node

const axios = require('axios');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🏥 Starting EMO System Health Check...\n');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

const log = (message, color = 'reset') => {
  console.log(`${colors[color]}${message}${colors.reset}`);
};

// Health check endpoints
const endpoints = [
  {
    name: 'Backend API',
    url: 'http://localhost:3000/health',
    port: 3000,
    service: 'backend'
  },
  {
    name: 'Frontend',
    url: 'http://localhost:6000',
    port: 6000,
    service: 'frontend'
  },
  {
    name: 'Admin Panel',
    url: 'http://localhost:6001',
    port: 6001,
    service: 'admin-panel'
  },
  {
    name: 'AI Integration',
    url: 'http://localhost:5001/health',
    port: 5001,
    service: 'ai-integration'
  },
  {
    name: 'Blockchain',
    url: 'http://localhost:5002/health',
    port: 5002,
    service: 'blockchain'
  }
];

// Check if port is in use
const isPortInUse = (port) => {
  try {
    execSync(`netstat -an | grep :${port}`, { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
};

// Check service health
const checkServiceHealth = async (endpoint) => {
  try {
    const response = await axios.get(endpoint.url, { timeout: 5000 });
    
    if (response.status === 200) {
      log(`✅ ${endpoint.name} is healthy`, 'green');
      
      // Log additional health data if available
      if (response.data) {
        const healthData = response.data;
        if (healthData.uptime) {
          log(`   📊 Uptime: ${Math.round(healthData.uptime / 60)} minutes`, 'cyan');
        }
        if (healthData.environment) {
          log(`   🌍 Environment: ${healthData.environment}`, 'cyan');
        }
        if (healthData.version) {
          log(`   📦 Version: ${healthData.version}`, 'cyan');
        }
      }
      
      return { healthy: true, data: response.data };
    } else {
      log(`⚠️  ${endpoint.name} returned status ${response.status}`, 'yellow');
      return { healthy: false, status: response.status };
    }
  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      log(`❌ ${endpoint.name} is not running`, 'red');
    } else if (error.code === 'ETIMEDOUT') {
      log(`⏰ ${endpoint.name} is slow to respond`, 'yellow');
    } else {
      log(`❌ ${endpoint.name} error: ${error.message}`, 'red');
    }
    return { healthy: false, error: error.message };
  }
};

// Check database connection
const checkDatabase = async () => {
  try {
    const response = await axios.get('http://localhost:3000/api/health/database', { timeout: 5000 });
    if (response.status === 200) {
      log('✅ Database connection is healthy', 'green');
      return true;
    }
  } catch (error) {
    log('❌ Database connection failed', 'red');
    return false;
  }
};

// Check file system
const checkFileSystem = () => {
  const requiredDirs = [
    'logs',
    'uploads',
    'temp',
    'frontend/public',
    'backend/logs',
    'admin-panel/public'
  ];
  
  const missingDirs = [];
  
  requiredDirs.forEach(dir => {
    const fullPath = path.join(process.cwd(), dir);
    if (!fs.existsSync(fullPath)) {
      missingDirs.push(dir);
    }
  });
  
  if (missingDirs.length > 0) {
    log('⚠️  Missing directories:', 'yellow');
    missingDirs.forEach(dir => log(`   📁 ${dir}`, 'yellow'));
    return false;
  } else {
    log('✅ File system is healthy', 'green');
    return true;
  }
};

// Check environment variables
const checkEnvironment = () => {
  const requiredEnvVars = [
    'NODE_ENV',
    'MONGODB_URI',
    'JWT_SECRET'
  ];
  
  const missingEnvVars = [];
  
  requiredEnvVars.forEach(envVar => {
    if (!process.env[envVar]) {
      missingEnvVars.push(envVar);
    }
  });
  
  if (missingEnvVars.length > 0) {
    log('⚠️  Missing environment variables:', 'yellow');
    missingEnvVars.forEach(envVar => log(`   🔧 ${envVar}`, 'yellow'));
    return false;
  } else {
    log('✅ Environment variables are set', 'green');
    return true;
  }
};

// Check package.json files
const checkPackages = () => {
  const packages = ['frontend', 'backend', 'admin-panel', 'ai-integration', 'blockchain'];
  const missingPackages = [];
  
  packages.forEach(pkg => {
    const pkgPath = path.join(process.cwd(), pkg, 'package.json');
    if (!fs.existsSync(pkgPath)) {
      missingPackages.push(pkg);
    }
  });
  
  if (missingPackages.length > 0) {
    log('⚠️  Missing package.json files:', 'yellow');
    missingPackages.forEach(pkg => log(`   📦 ${pkg}/package.json`, 'yellow'));
    return false;
  } else {
    log('✅ Package files are present', 'green');
    return true;
  }
};

// Check system resources
const checkSystemResources = () => {
  try {
    // Check memory usage
    const memUsage = process.memoryUsage();
    const memUsageMB = {
      rss: Math.round(memUsage.rss / 1024 / 1024),
      heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024),
      heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024),
      external: Math.round(memUsage.external / 1024 / 1024)
    };
    
    log('📊 System Resources:', 'blue');
    log(`   💾 Memory Usage: ${memUsageMB.heapUsed}MB / ${memUsageMB.heapTotal}MB`, 'cyan');
    log(`   🔧 RSS: ${memUsageMB.rss}MB`, 'cyan');
    
    // Check disk space (simplified)
    const diskUsage = execSync('df -h .', { encoding: 'utf8' });
    log('💽 Disk Usage:', 'blue');
    log(`   ${diskUsage.split('\n')[1]}`, 'cyan');
    
    return true;
  } catch (error) {
    log('⚠️  Could not check system resources', 'yellow');
    return false;
  }
};

// Generate health report
const generateReport = (results) => {
  const healthyServices = results.filter(r => r.healthy).length;
  const totalServices = results.length;
  const healthPercentage = Math.round((healthyServices / totalServices) * 100);
  
  log('\n📋 Health Check Report', 'magenta');
  log('====================', 'magenta');
  log(`\n🏥 Overall Health: ${healthPercentage}%`, healthPercentage >= 80 ? 'green' : healthPercentage >= 60 ? 'yellow' : 'red');
  log(`✅ Healthy Services: ${healthyServices}/${totalServices}`, 'green');
  
  if (healthPercentage < 80) {
    log('\n⚠️  Recommendations:', 'yellow');
    if (healthPercentage < 60) {
      log('   • Check if all services are running', 'yellow');
      log('   • Verify environment variables', 'yellow');
      log('   • Check database connection', 'yellow');
    } else {
      log('   • Some services may need attention', 'yellow');
    }
  }
  
  log('\n🔧 Quick Commands:', 'blue');
  log('   • Start all services: npm run dev', 'cyan');
  log('   • Check logs: tail -f logs/combined.log', 'cyan');
  log('   • Restart backend: cd backend && npm run dev', 'cyan');
  log('   • Restart frontend: cd frontend && npm run dev', 'cyan');
};

// Main health check function
const performHealthCheck = async () => {
  log('🎯 EMO System Health Check Started', 'magenta');
  log('==================================', 'magenta');
  
  const results = [];
  
  // Check environment and packages first
  log('\n🔧 System Checks:', 'blue');
  checkEnvironment();
  checkPackages();
  checkFileSystem();
  checkSystemResources();
  
  // Check service health
  log('\n🏥 Service Health Checks:', 'blue');
  for (const endpoint of endpoints) {
    const result = await checkServiceHealth(endpoint);
    results.push({ ...endpoint, ...result });
  }
  
  // Check database
  log('\n🗄️  Database Check:', 'blue');
  await checkDatabase();
  
  // Generate report
  generateReport(results);
  
  log('\n🎉 Health check completed!', 'green');
};

// Run health check
performHealthCheck().catch(error => {
  log(`❌ Health check failed: ${error.message}`, 'red');
  process.exit(1);
}); 