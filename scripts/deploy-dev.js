#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Starting EMO Development Deployment...\n');

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

const runCommand = (command, description) => {
  try {
    log(`📦 ${description}...`, 'blue');
    execSync(command, { stdio: 'inherit' });
    log(`✅ ${description} completed`, 'green');
  } catch (error) {
    log(`❌ ${description} failed: ${error.message}`, 'red');
    process.exit(1);
  }
};

// Check if Node.js version is compatible
const checkNodeVersion = () => {
  const nodeVersion = process.version;
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
  
  if (majorVersion < 18) {
    log('❌ Node.js version 18 or higher is required', 'red');
    log(`Current version: ${nodeVersion}`, 'yellow');
    process.exit(1);
  }
  
  log(`✅ Node.js version ${nodeVersion} is compatible`, 'green');
};

// Create necessary directories
const createDirectories = () => {
  const dirs = [
    'logs',
    'uploads',
    'temp',
    'frontend/public',
    'backend/logs',
    'admin-panel/public',
  ];
  
  dirs.forEach(dir => {
    const fullPath = path.join(process.cwd(), dir);
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
      log(`📁 Created directory: ${dir}`, 'cyan');
    }
  });
};

// Install dependencies for all packages
const installDependencies = () => {
  const packages = ['frontend', 'backend', 'admin-panel', 'ai-integration', 'blockchain'];
  
  packages.forEach(pkg => {
    const pkgPath = path.join(process.cwd(), pkg);
    if (fs.existsSync(path.join(pkgPath, 'package.json'))) {
      log(`📦 Installing dependencies for ${pkg}...`, 'blue');
      runCommand(`cd ${pkgPath} && npm install`, `Dependencies for ${pkg}`);
    }
  });
};

// Setup environment files
const setupEnvironment = () => {
  const envExample = path.join(process.cwd(), '.env.example');
  const envFile = path.join(process.cwd(), '.env');
  
  if (!fs.existsSync(envFile) && fs.existsSync(envExample)) {
    log('📝 Creating .env file from .env.example...', 'blue');
    fs.copyFileSync(envExample, envFile);
    log('✅ .env file created', 'green');
    log('⚠️  Please update .env file with your configuration values', 'yellow');
  }
};

// Build packages
const buildPackages = () => {
  log('🔨 Building packages...', 'blue');
  
  // Build frontend
  if (fs.existsSync(path.join(process.cwd(), 'frontend/package.json'))) {
    runCommand('cd frontend && npm run build', 'Frontend build');
  }
  
  // Build admin panel
  if (fs.existsSync(path.join(process.cwd(), 'admin-panel/package.json'))) {
    runCommand('cd admin-panel && npm run build', 'Admin panel build');
  }
  
  // Build backend
  if (fs.existsSync(path.join(process.cwd(), 'backend/package.json'))) {
    runCommand('cd backend && npm run build', 'Backend build');
  }
};

// Start development servers
const startDevServers = () => {
  log('🚀 Starting development servers...', 'blue');
  
  const commands = [
    { cmd: 'cd frontend && npm run dev', name: 'Frontend (Port 6000)' },
    { cmd: 'cd backend && npm run dev', name: 'Backend (Port 3000)' },
    { cmd: 'cd admin-panel && npm run dev', name: 'Admin Panel (Port 6001)' },
    { cmd: 'cd ai-integration && npm run dev', name: 'AI Integration (Port 5001)' },
    { cmd: 'cd blockchain && npm run dev', name: 'Blockchain (Port 5002)' },
  ];
  
  commands.forEach(({ cmd, name }) => {
    try {
      log(`🔄 Starting ${name}...`, 'yellow');
      execSync(cmd, { stdio: 'inherit', detached: true });
    } catch (error) {
      log(`⚠️  Failed to start ${name}: ${error.message}`, 'yellow');
    }
  });
};

// Health check
const healthCheck = () => {
  log('🏥 Performing health check...', 'blue');
  
  const endpoints = [
    { url: 'http://localhost:3000/health', name: 'Backend API' },
    { url: 'http://localhost:6000', name: 'Frontend' },
    { url: 'http://localhost:6001', name: 'Admin Panel' },
    { url: 'http://localhost:5001/health', name: 'AI Integration' },
    { url: 'http://localhost:5002/health', name: 'Blockchain' },
  ];
  
  setTimeout(() => {
    endpoints.forEach(({ url, name }) => {
      try {
        const response = require('http').getSync(url);
        if (response.statusCode === 200) {
          log(`✅ ${name} is running`, 'green');
        } else {
          log(`⚠️  ${name} returned status ${response.statusCode}`, 'yellow');
        }
      } catch (error) {
        log(`❌ ${name} is not responding`, 'red');
      }
    });
  }, 5000);
};

// Main deployment function
const deploy = async () => {
  try {
    log('🎯 EMO Development Deployment Started', 'magenta');
    log('=====================================', 'magenta');
    
    checkNodeVersion();
    createDirectories();
    setupEnvironment();
    installDependencies();
    buildPackages();
    startDevServers();
    healthCheck();
    
    log('\n🎉 EMO Development Deployment Completed!', 'green');
    log('==========================================', 'green');
    log('\n📋 Services running:', 'cyan');
    log('   • Frontend: http://localhost:6000', 'cyan');
    log('   • Backend API: http://localhost:3000', 'cyan');
    log('   • Admin Panel: http://localhost:6001', 'cyan');
    log('   • AI Integration: http://localhost:5001', 'cyan');
    log('   • Blockchain: http://localhost:5002', 'cyan');
    log('\n📚 Documentation: https://docs.emo-business.com', 'cyan');
    log('🐛 Issues: https://github.com/ehb/emo-business/issues', 'cyan');
    
  } catch (error) {
    log(`❌ Deployment failed: ${error.message}`, 'red');
    process.exit(1);
  }
};

// Run deployment
deploy(); 