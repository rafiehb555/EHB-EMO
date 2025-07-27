#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🚀 Setting up EMO Development Environment...\n');

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

// Check if Node.js is installed
function checkNodeVersion() {
  try {
    const version = execSync('node --version', { encoding: 'utf8' }).trim();
    const majorVersion = parseInt(version.replace('v', '').split('.')[0]);

    if (majorVersion < 18) {
      error('Node.js 18+ is required. Please upgrade Node.js.');
      process.exit(1);
    }

    success(`Node.js ${version} detected`);
    return true;
  } catch (err) {
    error('Node.js is not installed. Please install Node.js 18+');
    process.exit(1);
  }
}

// Check if npm is installed
function checkNpm() {
  try {
    const version = execSync('npm --version', { encoding: 'utf8' }).trim();
    success(`npm ${version} detected`);
    return true;
  } catch (err) {
    error('npm is not installed. Please install npm');
    process.exit(1);
  }
}

// Install dependencies for a project
function installDependencies(projectPath, projectName) {
  try {
    log(`Installing dependencies for ${projectName}...`);
    execSync('npm install', { cwd: projectPath, stdio: 'inherit' });
    success(`${projectName} dependencies installed`);
  } catch (err) {
    error(`Failed to install dependencies for ${projectName}`);
    return false;
  }
}

// Create necessary directories
function createDirectories() {
  const dirs = [
    'backend/uploads',
    'backend/logs',
    'frontend/public',
    'admin-panel/public'
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      success(`Created directory: ${dir}`);
    }
  });
}

// Copy environment files
function setupEnvironment() {
  const envFiles = [
    { src: 'backend/env.example', dest: 'backend/.env' },
    { src: 'frontend/env.example', dest: 'frontend/.env.local' },
    { src: 'admin-panel/env.example', dest: 'admin-panel/.env.local' }
  ];

  envFiles.forEach(({ src, dest }) => {
    if (fs.existsSync(src) && !fs.existsSync(dest)) {
      fs.copyFileSync(src, dest);
      success(`Created ${dest}`);
    }
  });
}

// Check if MongoDB is running
function checkMongoDB() {
  try {
    execSync('mongod --version', { stdio: 'ignore' });
    info('MongoDB detected. Make sure MongoDB service is running.');
  } catch (err) {
    info('MongoDB not found. Please install MongoDB or use MongoDB Atlas.');
  }
}

// Main setup function
function setup() {
  log('Starting EMO development setup...\n');

  // Check prerequisites
  checkNodeVersion();
  checkNpm();
  checkMongoDB();

  console.log('\n📦 Installing dependencies...\n');

  // Install dependencies for all projects
  const projects = [
    { path: 'backend', name: 'Backend' },
    { path: 'frontend', name: 'Frontend' },
    { path: 'admin-panel', name: 'Admin Panel' }
  ];

  projects.forEach(({ path, name }) => {
    if (fs.existsSync(path)) {
      installDependencies(path, name);
    } else {
      error(`${name} directory not found`);
    }
  });

  console.log('\n📁 Creating directories...\n');
  createDirectories();

  console.log('\n⚙️  Setting up environment...\n');
  setupEnvironment();

  console.log('\n🎉 Setup complete!');
  console.log('\n📋 Next steps:');
  console.log('1. Configure your environment variables in .env files');
  console.log('2. Start MongoDB service');
  console.log('3. Run development servers:');
  console.log('   - Backend: cd backend && npm run dev');
  console.log('   - Frontend: cd frontend && npm run dev');
  console.log('   - Admin Panel: cd admin-panel && npm run dev');
  console.log('\n🌐 Access your application:');
  console.log('   - Frontend: http://localhost:3000');
  console.log('   - Backend API: http://localhost:4003');
  console.log('   - Admin Panel: http://localhost:6001');
}

// Run setup
setup();
