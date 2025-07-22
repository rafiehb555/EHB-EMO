const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class GlobalPackageManager {
  constructor() {
    this.workspaceRoot = 'C:/CursorWorkspace';
    this.configPath = path.join(this.workspaceRoot, 'config');
    this.packagesPath = path.join(this.workspaceRoot, 'packages');
    this.extensionsPath = path.join(this.workspaceRoot, 'extensions');
  }

  async setupDirectories() {
    const dirs = [this.workspaceRoot, this.configPath, this.packagesPath, this.extensionsPath];
    
    for (const dir of dirs) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`Created directory: ${dir}`);
      }
    }
  }

  async installGlobalPackages() {
    const packages = [
      'typescript', 'eslint', 'prettier', 'nodemon', 
      'concurrently', 'cross-env', 'dotenv', 'yarn', 'pnpm'
    ];

    console.log('Installing global packages...');
    for (const pkg of packages) {
      try {
        execSync(`npm install -g ${pkg}`, { stdio: 'inherit' });
        console.log(`✓ Installed ${pkg}`);
      } catch (error) {
        console.log(`✗ Failed to install ${pkg}: ${error.message}`);
      }
    }
  }

  async setupEnvironment() {
    const envContent = `
# Cursor Global Environment Variables
CURSOR_GLOBAL_CONFIG=${this.configPath}
GLOBAL_PACKAGES_PATH=${this.packagesPath}
SHARED_EXTENSIONS_PATH=${this.extensionsPath}
NODE_ENV=development
    `.trim();

    const envPath = path.join(this.workspaceRoot, '.env');
    fs.writeFileSync(envPath, envContent);
    console.log(`Created environment file: ${envPath}`);
  }

  async createProjectTemplate() {
    const templatePath = path.join(this.workspaceRoot, 'templates');
    if (!fs.existsSync(templatePath)) {
      fs.mkdirSync(templatePath, { recursive: true });
    }

    const packageJson = {
      name: "project-template",
      version: "1.0.0",
      description: "Template for new projects",
      scripts: {
        "dev": "nodemon src/index.js",
        "build": "tsc",
        "start": "node dist/index.js",
        "test": "jest",
        "lint": "eslint src/**/*.js",
        "format": "prettier --write src/**/*.js"
      },
      devDependencies: {
        "typescript": "^4.9.0",
        "eslint": "^8.0.0",
        "prettier": "^2.8.0",
        "nodemon": "^2.0.0",
        "jest": "^29.0.0"
      }
    };

    fs.writeFileSync(
      path.join(templatePath, 'package.json'),
      JSON.stringify(packageJson, null, 2)
    );

    console.log('Created project template');
  }

  async run() {
    console.log('Setting up Cursor Global Configuration...\n');
    
    await this.setupDirectories();
    await this.installGlobalPackages();
    await this.setupEnvironment();
    await this.createProjectTemplate();
    
    console.log('\n✓ Setup complete!');
    console.log('\nNext steps:');
    console.log('1. Copy cursor-settings.json to your Cursor settings');
    console.log('2. Restart Cursor');
    console.log('3. All tools will be available in any new project');
  }
}

// Run the setup
const manager = new GlobalPackageManager();
manager.run().catch(console.error); 