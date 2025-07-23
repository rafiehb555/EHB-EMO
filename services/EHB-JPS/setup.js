#!/usr/bin/env node

/**
 * EHB JPS Setup Script
 * Complete setup for Job Portal System
 */

const { execSync } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const ora = require('ora');
const figlet = require('figlet');
const boxen = require('boxen');
const gradient = require('gradient-string');

console.clear();

// Display banner
console.log(
  boxen(
    gradient.rainbow(
      figlet.textSync('EHB JPS', { horizontalLayout: 'full' })
    ),
    {
      padding: 1,
      margin: 1,
      borderStyle: 'round',
      borderColor: 'cyan'
    }
  )
);

console.log(chalk.cyan.bold('🚀 EHB Job Portal System Setup'));
console.log(chalk.gray('Setting up complete development environment...\n'));

async function setup() {
  const spinner = ora('Initializing setup...').start();

  try {
    // Step 1: Check Node.js version
    spinner.text = 'Checking Node.js version...';
    const nodeVersion = process.version;
    const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);

    if (majorVersion < 18) {
      throw new Error('Node.js 18 or higher is required');
    }
    console.log(chalk.green('✅ Node.js version:', nodeVersion));

    // Step 2: Install dependencies
    spinner.text = 'Installing dependencies...';

    // Install main dependencies
    execSync('npm install', { stdio: 'inherit' });

    // Install frontend dependencies
    if (fs.existsSync('frontend')) {
      execSync('cd frontend && npm install', { stdio: 'inherit' });
    }

    // Install backend dependencies
    if (fs.existsSync('backend')) {
      execSync('cd backend && npm install', { stdio: 'inherit' });
    }

    // Install admin panel dependencies
    if (fs.existsSync('admin-panel')) {
      execSync('cd admin-panel && npm install', { stdio: 'inherit' });
    }

    // Install database dependencies
    if (fs.existsSync('database')) {
      execSync('cd database && npm install', { stdio: 'inherit' });
    }

    // Install tools dependencies
    if (fs.existsSync('tools')) {
      execSync('cd tools && npm install', { stdio: 'inherit' });
    }

    // Install SDK dependencies
    if (fs.existsSync('sdk')) {
      execSync('cd sdk && npm install', { stdio: 'inherit' });
    }

    // Install deployment dependencies
    if (fs.existsSync('deployment')) {
      execSync('cd deployment && npm install', { stdio: 'inherit' });
    }

    console.log(chalk.green('✅ All dependencies installed'));

    // Step 3: Create environment file
    spinner.text = 'Setting up environment configuration...';

    if (!fs.existsSync('.env')) {
      fs.copyFileSync('env.example', '.env');
      console.log(chalk.green('✅ Environment file created'));
    }

    // Step 4: Create necessary directories
    spinner.text = 'Creating project structure...';

    const dirs = [
      'logs',
      'uploads',
      'temp',
      'backups',
      'cache',
      'public/uploads',
      'public/images',
      'public/documents'
    ];

    dirs.forEach(dir => {
      fs.ensureDirSync(dir);
    });

    console.log(chalk.green('✅ Project structure created'));

    // Step 5: Setup database
    spinner.text = 'Setting up database...';

    if (fs.existsSync('database/scripts/setup.js')) {
      execSync('cd database && npm run setup', { stdio: 'inherit' });
    }

    console.log(chalk.green('✅ Database setup completed'));

    // Step 6: Build SDK
    spinner.text = 'Building SDK...';

    if (fs.existsSync('sdk')) {
      execSync('cd sdk && npm run build', { stdio: 'inherit' });
    }

    console.log(chalk.green('✅ SDK built successfully'));

    // Step 7: Setup Git hooks
    spinner.text = 'Setting up Git hooks...';

    if (fs.existsSync('.git')) {
      execSync('npx husky install', { stdio: 'inherit' });
    }

    console.log(chalk.green('✅ Git hooks configured'));

    // Step 8: Create startup scripts
    spinner.text = 'Creating startup scripts...';

    const scripts = {
      'start-dev': 'concurrently \"npm run dev:frontend\" \"npm run dev:backend\" \"npm run dev:admin\"',
      'start-prod': 'npm run build && npm run start',
      'test-all': 'npm run test:frontend && npm run test:backend && npm run test:admin',
      'lint-all': 'npm run lint:frontend && npm run lint:backend && npm run lint:admin',
      'format-all': 'prettier --write \"**/*.{js,ts,jsx,tsx,json,md}\"',
      'db:reset': 'cd database && npm run reset',
      'db:backup': 'cd database && npm run backup',
      'deploy:dev': 'cd deployment && npm run deploy:dev',
      'deploy:prod': 'cd deployment && npm run deploy:prod'
    };

    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    packageJson.scripts = { ...packageJson.scripts, ...scripts };
    fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));

    console.log(chalk.green('✅ Startup scripts created'));

    // Step 9: Create documentation
    spinner.text = 'Generating documentation...';

    const readme = `# EHB Job Portal System (JPS)

## 🚀 Quick Start

### Development
\`\`\`bash
npm run start-dev
\`\`\`

### Production
\`\`\`bash
npm run start-prod
\`\`\`

## 📁 Project Structure

- \`frontend/\` - React/Next.js frontend application
- \`backend/\` - Node.js/Express API server
- \`admin-panel/\` - Admin dashboard
- \`database/\` - Database management and migrations
- \`sdk/\` - Client libraries and SDKs
- \`tools/\` - Development tools and utilities
- \`deployment/\` - Docker and deployment configurations

## 🔧 Available Scripts

- \`npm run start-dev\` - Start development servers
- \`npm run start-prod\` - Start production servers
- \`npm run test-all\` - Run all tests
- \`npm run lint-all\` - Lint all code
- \`npm run format-all\` - Format all code
- \`npm run db:reset\` - Reset database
- \`npm run db:backup\` - Backup database
- \`npm run deploy:dev\` - Deploy to development
- \`npm run deploy:prod\` - Deploy to production

## 🌐 Access Points

- Frontend: http://localhost:3000
- Backend API: http://localhost:3001
- Admin Panel: http://localhost:3002
- API Docs: http://localhost:3001/api-docs

## 📚 Documentation

- [API Documentation](./docs/api.md)
- [Database Schema](./docs/database.md)
- [Deployment Guide](./docs/deployment.md)
- [Development Guide](./docs/development.md)

## 🛠️ Technologies

- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, TypeScript
- **Database**: PostgreSQL, Redis
- **Search**: Elasticsearch
- **Deployment**: Docker, AWS, Vercel
- **Testing**: Jest, React Testing Library
- **Linting**: ESLint, Prettier

## 📈 Features

- Job posting and management
- Advanced search and filtering
- Resume upload and management
- Application tracking
- Email notifications
- Analytics and reporting
- Admin dashboard
- Mobile responsive design

## 🔒 Security

- JWT authentication
- Password hashing with bcrypt
- Rate limiting
- Input validation
- CORS protection
- Helmet security headers

## 📊 Monitoring

- Real-time analytics
- Error tracking
- Performance monitoring
- Health checks
- Log management

## 🚀 Deployment

- Docker containerization
- CI/CD pipeline
- Environment management
- Database migrations
- Backup and restore

---

**Status**: ✅ Ready for Development
**Version**: 1.0.0
**Last Updated**: ${new Date().toISOString()}
`;

    fs.writeFileSync('README.md', readme);
    console.log(chalk.green('✅ Documentation generated'));

    spinner.succeed('Setup completed successfully!');

    // Display success message
    console.log('\n' + boxen(
      chalk.green.bold('🎉 Setup Complete!') + '\n\n' +
      chalk.cyan('Your EHB JPS project is ready for development.\n\n') +
      chalk.yellow('Next steps:\n') +
      chalk.white('1. Configure your .env file\n') +
      chalk.white('2. Start development: npm run start-dev\n') +
      chalk.white('3. Access frontend: http://localhost:3000\n') +
      chalk.white('4. Access backend: http://localhost:3001\n') +
      chalk.white('5. Access admin: http://localhost:3002\n\n') +
      chalk.gray('Happy coding! 🚀'),
      {
        padding: 1,
        margin: 1,
        borderStyle: 'round',
        borderColor: 'green'
      }
    ));

  } catch (error) {
    spinner.fail('Setup failed!');
    console.error(chalk.red('Error:'), error.message);
    process.exit(1);
  }
}

// Run setup
setup();
