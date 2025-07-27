#!/usr/bin/env node

const axios = require('axios');
const { execSync } = require('child_process');

console.log('🏥 EMO Health Check...\n');

// Colors for console output
const colors = {
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(message, color = 'green') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function error(message) {
  console.log(`${colors.red}❌ ${message}${colors.reset}`);
}

function success(message) {
  console.log(`${colors.green}✅ ${message}${colors.reset}`);
}

function info(message) {
  console.log(`${colors.blue}ℹ️  ${message}${colors.reset}`);
}

function warning(message) {
  console.log(`${colors.yellow}⚠️  ${message}${colors.reset}`);
}

// Check if a port is in use
function checkPort(port) {
  try {
    const result = execSync(`netstat -an | findstr :${port}`, { encoding: 'utf8' });
    return result.includes(`:${port}`);
  } catch (err) {
    return false;
  }
}

// Check if a service is responding
async function checkService(url, name) {
  try {
    const response = await axios.get(url, { timeout: 5000 });
    if (response.status === 200) {
      success(`${name} is running (${response.status})`);
      return true;
    } else {
      warning(`${name} responded with status ${response.status}`);
      return false;
    }
  } catch (err) {
    error(`${name} is not responding: ${err.message}`);
    return false;
  }
}

// Check Node.js version
function checkNodeVersion() {
  try {
    const version = execSync('node --version', { encoding: 'utf8' }).trim();
    const majorVersion = parseInt(version.replace('v', '').split('.')[0]);

    if (majorVersion >= 18) {
      success(`Node.js ${version} (✓ 18+)`);
      return true;
    } else {
      error(`Node.js ${version} (✗ Need 18+)`);
      return false;
    }
  } catch (err) {
    error('Node.js not found');
    return false;
  }
}

// Check npm version
function checkNpmVersion() {
  try {
    const version = execSync('npm --version', { encoding: 'utf8' }).trim();
    success(`npm ${version}`);
    return true;
  } catch (err) {
    error('npm not found');
    return false;
  }
}

// Check if directories exist
function checkDirectories() {
  const dirs = [
    { path: 'backend', name: 'Backend' },
    { path: 'frontend', name: 'Frontend' },
    { path: 'admin-panel', name: 'Admin Panel' }
  ];

  let allExist = true;

  dirs.forEach(({ path, name }) => {
    if (require('fs').existsSync(path)) {
      success(`${name} directory exists`);
    } else {
      error(`${name} directory missing`);
      allExist = false;
    }
  });

  return allExist;
}

// Check if package.json files exist
function checkPackageFiles() {
  const files = [
    { path: 'backend/package.json', name: 'Backend package.json' },
    { path: 'frontend/package.json', name: 'Frontend package.json' },
    { path: 'admin-panel/package.json', name: 'Admin Panel package.json' }
  ];

  let allExist = true;

  files.forEach(({ path, name }) => {
    if (require('fs').existsSync(path)) {
      success(`${name} exists`);
    } else {
      error(`${name} missing`);
      allExist = false;
    }
  });

  return allExist;
}

// Check if node_modules exist
function checkNodeModules() {
  const modules = [
    { path: 'backend/node_modules', name: 'Backend node_modules' },
    { path: 'frontend/node_modules', name: 'Frontend node_modules' },
    { path: 'admin-panel/node_modules', name: 'Admin Panel node_modules' }
  ];

  let allExist = true;

  modules.forEach(({ path, name }) => {
    if (require('fs').existsSync(path)) {
      success(`${name} exists`);
    } else {
      warning(`${name} missing - run npm install`);
      allExist = false;
    }
  });

  return allExist;
}

// Check environment files
function checkEnvironmentFiles() {
  const envFiles = [
    { path: 'backend/.env', name: 'Backend .env' },
    { path: 'frontend/.env.local', name: 'Frontend .env.local' },
    { path: 'admin-panel/.env.local', name: 'Admin Panel .env.local' }
  ];

  let allExist = true;

  envFiles.forEach(({ path, name }) => {
    if (require('fs').existsSync(path)) {
      success(`${name} exists`);
    } else {
      warning(`${name} missing - copy from .env.example`);
      allExist = false;
    }
  });

  return allExist;
}

// Check ports
function checkPorts() {
  const ports = [
    { port: 3000, name: 'Frontend (3000)' },
    { port: 4003, name: 'Backend (4003)' },
    { port: 6001, name: 'Admin Panel (6001)' }
  ];

  let allAvailable = true;

  ports.forEach(({ port, name }) => {
    if (checkPort(port)) {
      warning(`${name} port is in use`);
      allAvailable = false;
    } else {
      success(`${name} port is available`);
    }
  });

  return allAvailable;
}

// Main health check function
async function healthCheck() {
  console.log('🔍 Checking system requirements...\n');

  const checks = [
    { name: 'Node.js Version', check: checkNodeVersion },
    { name: 'npm Version', check: checkNpmVersion },
    { name: 'Directories', check: checkDirectories },
    { name: 'Package Files', check: checkPackageFiles },
    { name: 'Node Modules', check: checkNodeModules },
    { name: 'Environment Files', check: checkEnvironmentFiles },
    { name: 'Ports', check: checkPorts }
  ];

  let allPassed = true;

  for (const { name, check } of checks) {
    info(`Checking ${name}...`);
    const result = await check();
    if (!result) {
      allPassed = false;
    }
    console.log('');
  }

  console.log('🌐 Checking services (if running)...\n');

  const services = [
    { url: 'http://localhost:3000', name: 'Frontend' },
    { url: 'http://localhost:4003/health', name: 'Backend API' },
    { url: 'http://localhost:6001', name: 'Admin Panel' }
  ];

  for (const { url, name } of services) {
    await checkService(url, name);
  }

  console.log('\n📊 Health Check Summary:');

  if (allPassed) {
    success('All basic checks passed!');
    console.log('\n🚀 Ready to start development:');
    console.log('   npm run dev:backend    # Start backend');
    console.log('   npm run dev:frontend   # Start frontend');
    console.log('   npm run dev:admin      # Start admin panel');
    console.log('   npm run dev            # Start all services');
  } else {
    error('Some checks failed. Please fix the issues above.');
    console.log('\n🔧 Setup commands:');
    console.log('   node scripts/setup-dev.js    # Run setup');
    console.log('   npm install                  # Install dependencies');
  }
}

// Run health check
healthCheck().catch(console.error);
