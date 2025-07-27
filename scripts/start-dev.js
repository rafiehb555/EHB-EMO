#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting EMO Development Environment...\n');

// Colors for console output
const colors = {
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
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

// Store child processes
const processes = [];

// Function to start a service
function startService(name, command, cwd, port) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, [], {
      cwd: path.resolve(cwd),
      stdio: 'pipe',
      shell: true
    });

    processes.push(child);

    child.stdout.on('data', (data) => {
      const output = data.toString();
      if (output.includes('ready') || output.includes('started') || output.includes('listening')) {
        success(`${name} is running on port ${port}`);
        resolve();
      }
      console.log(`${colors.cyan}[${name}]${colors.reset} ${output.trim()}`);
    });

    child.stderr.on('data', (data) => {
      const output = data.toString();
      if (output.includes('error') || output.includes('failed')) {
        error(`${name} error: ${output.trim()}`);
      } else {
        console.log(`${colors.yellow}[${name}]${colors.reset} ${output.trim()}`);
      }
    });

    child.on('error', (err) => {
      error(`Failed to start ${name}: ${err.message}`);
      reject(err);
    });

    child.on('close', (code) => {
      if (code !== 0) {
        error(`${name} process exited with code ${code}`);
      }
    });

    // Timeout after 30 seconds
    setTimeout(() => {
      if (!child.killed) {
        info(`${name} is starting...`);
        resolve();
      }
    }, 30000);
  });
}

// Function to stop all processes
function stopAllProcesses() {
  console.log('\n🛑 Stopping all development servers...');
  processes.forEach(process => {
    if (!process.killed) {
      process.kill('SIGTERM');
    }
  });
  process.exit(0);
}

// Handle process termination
process.on('SIGINT', stopAllProcesses);
process.on('SIGTERM', stopAllProcesses);

// Main function
async function startDevelopment() {
  try {
    log('Starting development servers...\n');

    // Start backend
    info('Starting Backend (Port 4003)...');
    await startService('Backend', 'npm', 'backend', 4003);

    // Wait a bit for backend to fully start
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Start frontend
    info('Starting Frontend (Port 3000)...');
    await startService('Frontend', 'npm', 'frontend', 3000);

    // Wait a bit for frontend to start
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Start admin panel
    info('Starting Admin Panel (Port 6001)...');
    await startService('Admin Panel', 'npm', 'admin-panel', 6001);

    console.log('\n🎉 All development servers are running!');
    console.log('\n🌐 Access your application:');
    console.log('   - Frontend: http://localhost:3000');
    console.log('   - Backend API: http://localhost:4003');
    console.log('   - Admin Panel: http://localhost:6001');
    console.log('\n📝 Press Ctrl+C to stop all servers');

  } catch (err) {
    error('Failed to start development environment');
    console.error(err);
    process.exit(1);
  }
}

// Check if all required directories exist
function checkDirectories() {
  const requiredDirs = ['backend', 'frontend', 'admin-panel'];
  const missingDirs = requiredDirs.filter(dir => !require('fs').existsSync(dir));

  if (missingDirs.length > 0) {
    error(`Missing required directories: ${missingDirs.join(', ')}`);
    console.log('Please run the setup script first: node scripts/setup-dev.js');
    process.exit(1);
  }
}

// Check if package.json files exist
function checkPackageFiles() {
  const packageFiles = [
    'backend/package.json',
    'frontend/package.json',
    'admin-panel/package.json'
  ];

  const missingFiles = packageFiles.filter(file => !require('fs').existsSync(file));

  if (missingFiles.length > 0) {
    error(`Missing package.json files: ${missingFiles.join(', ')}`);
    console.log('Please run the setup script first: node scripts/setup-dev.js');
    process.exit(1);
  }
}

// Main execution
function main() {
  checkDirectories();
  checkPackageFiles();
  startDevelopment();
}

main();
