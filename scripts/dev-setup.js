#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🚀 Setting up development environment...');

// Create necessary directories
const dirs = [
  'backend/src',
  'backend/tests',
  'frontend/src',
  'frontend/public',
  'services',
  'shared',
  'docs',
  'monitoring',
  'utils',
  'tests'
];

dirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`✅ Created directory: ${dir}`);
  }
});

// Install dependencies
console.log('📦 Installing dependencies...');
try {
  execSync('npm install', { stdio: 'inherit' });
  console.log('✅ Dependencies installed');
} catch (error) {
  console.error('❌ Error installing dependencies:', error.message);
}

// Setup Git hooks
console.log('🔧 Setting up Git hooks...');
try {
  execSync('npx husky install', { stdio: 'inherit' });
  execSync('npx husky add .husky/pre-commit "npm run lint-staged"', { stdio: 'inherit' });
  console.log('✅ Git hooks configured');
} catch (error) {
  console.error('❌ Error setting up Git hooks:', error.message);
}

console.log('🎉 Development environment setup complete!');
console.log('\n📋 Next steps:');
console.log('1. npm run dev');
console.log('2. Open http://localhost:3000');
console.log('3. Start coding!');