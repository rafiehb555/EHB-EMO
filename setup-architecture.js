const fs = require('fs');
const path = require('path');

console.log('🏗️ Setting up High-Level Architecture (4-5 Layers)...');

// Project structure
const projectStructure = {
  'backend': {
    'api-gateway': {
      'src': {
        'controllers': {},
        'middleware': {},
        'routes': {},
        'utils': {}
      },
      'tests': {},
      'package.json': JSON.stringify({
        name: 'ehb5-api-gateway',
        version: '1.0.0',
        scripts: {
          'dev': 'ts-node src/index.ts',
          'build': 'tsc',
          'test': 'jest'
        },
        dependencies: {
          'express': '^4.18.2',
          'cors': '^2.8.5',
          'helmet': '^7.0.0'
        }
      }, null, 2)
    },
    'services': {
      'business-logic': {
        'src': {
          'services': {},
          'validators': {},
          'utils': {}
        },
        'tests': {}
      },
      'data-access': {
        'src': {
          'repositories': {},
          'models': {},
          'migrations': {}
        },
        'tests': {}
      },
      'infrastructure': {
        'src': {
          'database': {},
          'cache': {},
          'external-apis': {}
        },
        'tests': {}
      }
    }
  },
  'frontend': {
    'src': {
      'components': {
        'ui': {},
        'layout': {},
        'pages': {}
      },
      'store': {
        'actions': {},
        'reducers': {},
        'selectors': {}
      },
      'services': {
        'api': {},
        'auth': {},
        'utils': {}
      },
      'infrastructure': {
        'http': {},
        'websocket': {},
        'cache': {}
      }
    },
    'public': {},
    'tests': {}
  },
  'shared': {
    'types': {},
    'utils': {},
    'constants': {}
  },
  'docs': {
    'architecture': {},
    'api': {},
    'deployment': {}
  }
};

// Create directory structure
function createDirectories(structure, basePath = '') {
  Object.entries(structure).forEach(([name, content]) => {
    const fullPath = path.join(basePath, name);

    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
      console.log(`✅ Created: ${fullPath}`);
    }

    if (typeof content === 'object' && !Array.isArray(content)) {
      if (name === 'package.json') {
        fs.writeFileSync(fullPath, content);
        console.log(`📄 Created: ${fullPath}`);
      } else {
        createDirectories(content, fullPath);
      }
    }
  });
}

// Create base files
function createBaseFiles() {
  const baseFiles = {
    'package.json': JSON.stringify({
      name: 'ehb5-high-level-architecture',
      version: '1.0.0',
      scripts: {
        'dev': 'concurrently \"npm run dev:backend\" \"npm run dev:frontend\"',
        'dev:backend': 'cd backend && npm run dev',
        'dev:frontend': 'cd frontend && npm run dev',
        'build': 'npm run build:backend && npm run build:frontend',
        'build:backend': 'cd backend && npm run build',
        'build:frontend': 'cd frontend && npm run build',
        'test': 'npm run test:backend && npm run test:frontend',
        'test:backend': 'cd backend && npm run test',
        'test:frontend': 'cd frontend && npm run test'
      },
      dependencies: {
        'concurrently': '^8.2.0',
        'typescript': '^5.0.0'
      }
    }, null, 2),

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
        forceConsistentCasingInFileNames: true
      },
      include: ['src/**/*'],
      exclude: ['node_modules', 'dist']
    }, null, 2),

    'README.md': `# 🏗️ EHB-5 High-Level Architecture

## 🎯 4-Layer Backend Architecture
1. **Presentation Layer** - API Gateway
2. **Business Logic Layer** - Services
3. **Data Access Layer** - Repository
4. **Infrastructure Layer** - Database/External APIs

## 🎨 5-Layer Frontend Architecture
1. **Presentation Layer** - UI Components
2. **State Management Layer** - Redux/Zustand
3. **Business Logic Layer** - Services
4. **Data Layer** - API Calls
5. **Infrastructure Layer** - HTTP/WebSocket

## 🚀 Quick Start
\`\`\`bash
npm install
npm run dev
\`\`\`
`
  };

  Object.entries(baseFiles).forEach(([filename, content]) => {
    fs.writeFileSync(filename, content);
    console.log(`📄 Created: ${filename}`);
  });
}

// Create service templates
function createServiceTemplates() {
  const services = [
    'EHB-DASHBOARD',
    'EHB-WALLET',
    'EHB-BLOCKCHAIN',
    'EHB-AI-MARKETPLACE',
    'EHB-ROBOT',
    'EHB-TUBE',
    'EHB-COMPLAINTS',
    'EHB-EDR',
    'EHB-AFFILIATE',
    'EHB-SQL-LEVEL',
    'EHB-TRUSTY-WALLET',
    'EHB-VALIDATOR',
    'EHB-FRANCHISE',
    'EHB-GOSELLER',
    'EHB-JPS',
    'EHB-OBS'
  ];

  services.forEach(service => {
    const servicePath = `services/${service}`;
    if (!fs.existsSync(servicePath)) {
      fs.mkdirSync(servicePath, { recursive: true });

      // Create service structure
      const serviceStructure = {
        'src': {
          'components': {},
          'pages': {},
          'services': {},
          'utils': {}
        },
        'public': {},
        'tests': {},
        'package.json': JSON.stringify({
          name: service.toLowerCase(),
          version: '1.0.0',
          scripts: {
            'dev': 'next dev',
            'build': 'next build',
            'start': 'next start',
            'test': 'jest'
          },
          dependencies: {
            'next': '^14.0.0',
            'react': '^18.0.0',
            'react-dom': '^18.0.0',
            'typescript': '^5.0.0'
          }
        }, null, 2)
      };

      createDirectories(serviceStructure, servicePath);
      console.log(`🏗️ Created service: ${service}`);
    }
  });
}

// Main execution
try {
  console.log('🚀 Starting High-Level Architecture Setup...');

  // Create main structure
  createDirectories(projectStructure);

  // Create base files
  createBaseFiles();

  // Create service templates
  createServiceTemplates();

  console.log('\n✅ High-Level Architecture Setup Complete!');
  console.log('\n📋 Next Steps:');
  console.log('1. npm install');
  console.log('2. npm run dev');
  console.log('3. Start developing your services!');

} catch (error) {
  console.error('❌ Error during setup:', error);
  process.exit(1);
}
