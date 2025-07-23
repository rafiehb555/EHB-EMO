// Development Tools Setup for High-Level Architecture
const fs = require('fs');
const path = require('path');

console.log('🛠️ Setting up Development Tools for High-Level Architecture...');

// Development tools configuration
const devToolsConfig = {
  // Package.json for development tools
  'package.json': JSON.stringify({
    name: 'ehb5-development-tools',
    version: '1.0.0',
    scripts: {
      'dev': 'concurrently \"npm run dev:backend\" \"npm run dev:frontend\" \"npm run dev:services\"',
      'dev:backend': 'nodemon backend/src/index.js',
      'dev:frontend': 'cd frontend && npm run dev',
      'dev:services': 'concurrently \"npm run dev:dashboard\" \"npm run dev:wallet\" \"npm run dev:blockchain\"',
      'dev:dashboard': 'cd services/EHB-DASHBOARD && npm run dev',
      'dev:wallet': 'cd services/EHB-WALLET && npm run dev',
      'dev:blockchain': 'cd services/EHB-BLOCKCHAIN && npm run dev',
      'test': 'jest --coverage',
      'test:backend': 'cd backend && npm test',
      'test:frontend': 'cd frontend && npm test',
      'test:services': 'npm run test:dashboard && npm run test:wallet && npm run test:blockchain',
      'test:dashboard': 'cd services/EHB-DASHBOARD && npm test',
      'test:wallet': 'cd services/EHB-WALLET && npm test',
      'test:blockchain': 'cd services/EHB-BLOCKCHAIN && npm test',
      'build': 'npm run build:backend && npm run build:frontend && npm run build:services',
      'build:backend': 'cd backend && npm run build',
      'build:frontend': 'cd frontend && npm run build',
      'build:services': 'npm run build:dashboard && npm run build:wallet && npm run build:blockchain',
      'build:dashboard': 'cd services/EHB-DASHBOARD && npm run build',
      'build:wallet': 'cd services/EHB-WALLET && npm run build',
      'build:blockchain': 'cd services/EHB-BLOCKCHAIN && npm run build',
      'deploy': 'vercel --prod',
      'deploy:services': 'npm run deploy:dashboard && npm run deploy:wallet && npm run deploy:blockchain',
      'deploy:dashboard': 'cd services/EHB-DASHBOARD && vercel --prod',
      'deploy:wallet': 'cd services/EHB-WALLET && vercel --prod',
      'deploy:blockchain': 'cd services/EHB-BLOCKCHAIN && vercel --prod',
      'lint': 'eslint .',
      'lint:fix': 'eslint . --fix',
      'format': 'prettier --write .',
      'type-check': 'tsc --noEmit',
      'coverage': 'jest --coverage --watchAll',
      'monitor': 'npm run monitor:backend && npm run monitor:frontend',
      'monitor:backend': 'nodemon --watch backend backend/src/index.js',
      'monitor:frontend': 'cd frontend && npm run dev',
      'db:migrate': 'cd backend && npm run db:migrate',
      'db:seed': 'cd backend && npm run db:seed',
      'cache:clear': 'npm run cache:clear:backend && npm run cache:clear:frontend',
      'cache:clear:backend': 'cd backend && npm run cache:clear',
      'cache:clear:frontend': 'cd frontend && npm run cache:clear'
    },
    dependencies: {
      'concurrently': '^8.2.0',
      'nodemon': '^3.0.0',
      'typescript': '^5.0.0',
      'jest': '^29.0.0',
      '@types/jest': '^29.0.0',
      'eslint': '^8.0.0',
      'prettier': '^3.0.0',
      'husky': '^8.0.0',
      'lint-staged': '^13.0.0'
    },
    devDependencies: {
      '@types/node': '^20.0.0',
      '@types/express': '^4.17.0',
      '@types/cors': '^2.8.0',
      'ts-node': '^10.9.0',
      'cross-env': '^7.0.0'
    }
  }, null, 2),

  // Jest configuration
  'jest.config.js': `module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
};`,

  // ESLint configuration
  '.eslintrc.js': `module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
  ],
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-explicit-any': 'warn',
  },
  env: {
    node: true,
    es6: true,
  },
};`,

  // Prettier configuration
  '.prettierrc': JSON.stringify({
    semi: true,
    trailingComma: 'es5',
    singleQuote: true,
    printWidth: 80,
    tabWidth: 2,
  }, null, 2),

  // TypeScript configuration
  'tsconfig.json': JSON.stringify({
    compilerOptions: {
      target: 'ES2020',
      module: 'commonjs',
      lib: ['ES2020', 'DOM'],
      outDir: './dist',
      rootDir: './src',
      strict: true,
      esModuleInterop: true,
      skipLibCheck: true,
      forceConsistentCasingInFileNames: true,
      resolveJsonModule: true,
      declaration: true,
      declarationMap: true,
      sourceMap: true,
    },
    include: ['src/**/*', 'tests/**/*'],
    exclude: ['node_modules', 'dist'],
  }, null, 2),

  // Vercel configuration
  'vercel.json': JSON.stringify({
    version: 2,
    builds: [
      {
        src: 'backend/src/index.js',
        use: '@vercel/node'
      },
      {
        src: 'frontend/package.json',
        use: '@vercel/next'
      }
    ],
    routes: [
      {
        src: '/api/(.*)',
        dest: '/backend/src/index.js'
      },
      {
        src: '/(.*)',
        dest: '/frontend/$1'
      }
    ],
    env: {
      NODE_ENV: 'production'
    }
  }, null, 2),

  // Docker configuration
  'Dockerfile': `FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]`,

  // Docker Compose
  'docker-compose.yml': `version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:password@db:5432/ehb5
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3001:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:3000/api
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=ehb5
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:`,

  // GitHub Actions
  '.github/workflows/ci.yml': `name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Run linting
      run: npm run lint

    - name: Type check
      run: npm run type-check

    - name: Build
      run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: \${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: \${{ secrets.ORG_ID }}
        vercel-project-id: \${{ secrets.PROJECT_ID }}
        working-directory: ./
        vercel-args: '--prod'`,

  // Monitoring setup
  'monitoring/sentry.js': `const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});

module.exports = Sentry;`,

  // Performance monitoring
  'monitoring/performance.js': `const performance = require('perf_hooks').performance;

class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
  }

  startTimer(name) {
    this.metrics.set(name, performance.now());
  }

  endTimer(name) {
    const startTime = this.metrics.get(name);
    if (startTime) {
      const duration = performance.now() - startTime;
      console.log(\`⏱️ \${name}: \${duration.toFixed(2)}ms\`);
      this.metrics.delete(name);
      return duration;
    }
  }

  measureAsync(name, fn) {
    return async (...args) => {
      this.startTimer(name);
      try {
        const result = await fn(...args);
        this.endTimer(name);
        return result;
      } catch (error) {
        this.endTimer(name);
        throw error;
      }
    };
  }
}

module.exports = new PerformanceMonitor();`,

  // Error handling
  'utils/errorHandler.js': `class ErrorHandler {
  static handle(error, req, res, next) {
    console.error('Error:', error);

    if (error.name === 'ValidationError') {
      return res.status(400).json({
        error: 'Validation Error',
        details: error.message
      });
    }

    if (error.name === 'UnauthorizedError') {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Invalid token or credentials'
      });
    }

    return res.status(500).json({
      error: 'Internal Server Error',
      message: process.env.NODE_ENV === 'development' ? error.message : 'Something went wrong'
    });
  }

  static async wrap(fn) {
    return async (req, res, next) => {
      try {
        await fn(req, res, next);
      } catch (error) {
        ErrorHandler.handle(error, req, res, next);
      }
    };
  }
}

module.exports = ErrorHandler;`,

  // Database utilities
  'utils/database.js': `const { Pool } = require('pg');

class Database {
  constructor() {
    this.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
    });
  }

  async query(text, params) {
    const start = Date.now();
    try {
      const res = await this.pool.query(text, params);
      const duration = Date.now() - start;
      console.log('📊 Database query executed:', { text, duration, rows: res.rowCount });
      return res;
    } catch (error) {
      console.error('❌ Database query error:', error);
      throw error;
    }
  }

  async transaction(callback) {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}

module.exports = new Database();`,

  // Cache utilities
  'utils/cache.js': `const Redis = require('ioredis');

class Cache {
  constructor() {
    this.redis = new Redis(process.env.REDIS_URL);
  }

  async get(key) {
    try {
      const value = await this.redis.get(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }

  async set(key, value, ttl = 3600) {
    try {
      await this.redis.setex(key, ttl, JSON.stringify(value));
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }

  async delete(key) {
    try {
      await this.redis.del(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    }
  }

  async clear() {
    try {
      await this.redis.flushall();
    } catch (error) {
      console.error('Cache clear error:', error);
    }
  }
}

module.exports = new Cache();`,

  // Testing utilities
  'tests/setup.js': `// Test setup file
const { configure } = require('@testing-library/react');

configure({ testIdAttribute: 'data-testid' });

// Mock fetch for tests
global.fetch = jest.fn();

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock sessionStorage
const sessionStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.sessionStorage = sessionStorageMock;`,

  // Development scripts
  'scripts/dev-setup.js': `#!/usr/bin/env node

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
    console.log(\`✅ Created directory: \${dir}\`);
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
console.log('\\n📋 Next steps:');
console.log('1. npm run dev');
console.log('2. Open http://localhost:3000');
console.log('3. Start coding!');`,

  // README for development
  'DEVELOPMENT.md': `# 🛠️ Development Tools Setup

## 🚀 Quick Start

\`\`\`bash
# Install dependencies
npm install

# Start development servers
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Deploy
npm run deploy
\`\`\`

## 🏗️ Architecture

### 4-Layer Backend
1. **Presentation Layer** - API Gateway
2. **Business Logic Layer** - Services
3. **Data Access Layer** - Repository
4. **Infrastructure Layer** - Database/External APIs

### 5-Layer Frontend
1. **Presentation Layer** - UI Components
2. **State Management Layer** - Redux/Zustand
3. **Business Logic Layer** - Services
4. **Data Layer** - API Calls
5. **Infrastructure Layer** - HTTP/WebSocket

## 🛠️ Development Tools

- **TypeScript** - Type safety
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Jest** - Testing framework
- **Husky** - Git hooks
- **Concurrently** - Parallel development
- **Nodemon** - Auto-restart
- **Docker** - Containerization

## 📊 Monitoring

- **Sentry** - Error tracking
- **Performance Monitor** - Performance metrics
- **Database Monitor** - Query performance
- **Cache Monitor** - Cache hit rates

## 🧪 Testing

- **Unit Tests** - Component testing
- **Integration Tests** - API testing
- **E2E Tests** - End-to-end testing
- **Performance Tests** - Load testing

## 🚀 Deployment

- **Vercel** - Frontend deployment
- **Docker** - Container deployment
- **GitHub Actions** - CI/CD pipeline
- **Monitoring** - Production monitoring

## 📋 Scripts

- \`npm run dev\` - Start all development servers
- \`npm test\` - Run all tests
- \`npm run build\` - Build for production
- \`npm run deploy\` - Deploy to production
- \`npm run lint\` - Run linting
- \`npm run format\` - Format code
- \`npm run type-check\` - Type checking
- \`npm run coverage\` - Test coverage
- \`npm run monitor\` - Performance monitoring
\`\`\``
};

// Create development tools files
function createDevToolsFiles() {
  Object.entries(devToolsConfig).forEach(([filename, content]) => {
    const filePath = path.join(filename);

    // Create directory if needed
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(filePath, content);
    console.log(`📄 Created: ${filename}`);
  });
}

// Main execution
try {
  console.log('🚀 Setting up Development Tools...');

  // Create development tools files
  createDevToolsFiles();

  console.log('\n✅ Development Tools Setup Complete!');
  console.log('\n📋 Available Commands:');
  console.log('npm run dev          - Start all development servers');
  console.log('npm test             - Run all tests');
  console.log('npm run build        - Build for production');
  console.log('npm run deploy       - Deploy to production');
  console.log('npm run lint         - Run linting');
  console.log('npm run format       - Format code');
  console.log('npm run type-check   - Type checking');
  console.log('npm run coverage     - Test coverage');
  console.log('npm run monitor      - Performance monitoring');

} catch (error) {
  console.error('❌ Error during setup:', error);
  process.exit(1);
}
