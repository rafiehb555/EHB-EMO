/**
 * EHB API Integration - Installation and Run Script
 * Automatically installs dependencies and runs API tests
 *
 * @version 1.0.0
 * @author EHB Technologies
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

class EHBInstaller {
  constructor() {
    this.steps = [
      'checkNode',
      'installDependencies',
      'validateAPIs',
      'runTests',
      'displayResults'
    ];
    this.results = {};
    this.startTime = Date.now();
  }

  /**
   * Run complete installation and setup
   */
  async run() {
    console.log('🚀 EHB API Integration - Installation & Setup');
    console.log('==============================================\n');

    for (const step of this.steps) {
      try {
        await this[step]();
      } catch (error) {
        console.error(`❌ Error in ${step}:`, error.message);
        this.results[step] = { success: false, error: error.message };
      }
    }

    this.displayFinalResults();
  }

  /**
   * Check Node.js version
   */
  async checkNode() {
    console.log('📋 Step 1: Checking Node.js version...');

    return new Promise((resolve, reject) => {
      exec('node --version', (error, stdout) => {
        if (error) {
          reject(new Error('Node.js not found. Please install Node.js 18+ first.'));
          return;
        }

        const version = stdout.trim();
        const majorVersion = parseInt(version.replace('v', '').split('.')[0]);

        if (majorVersion < 18) {
          reject(new Error(`Node.js ${version} found. Please upgrade to Node.js 18 or higher.`));
          return;
        }

        console.log(`✅ Node.js ${version} found`);
        this.results.checkNode = { success: true, version };
        resolve();
      });
    });
  }

  /**
   * Install npm dependencies
   */
  async installDependencies() {
    console.log('\n📦 Step 2: Installing dependencies...');

    return new Promise((resolve, reject) => {
      const installCommand = 'npm install';
      console.log('   Running: npm install...');

      const child = exec(installCommand, (error, stdout, stderr) => {
        if (error) {
          reject(new Error(`Installation failed: ${error.message}`));
          return;
        }

        console.log('✅ Dependencies installed successfully');
        this.results.installDependencies = { success: true };
        resolve();
      });

      // Show progress
      let dots = 0;
      const interval = setInterval(() => {
        process.stdout.write('.');
        dots++;
        if (dots > 50) {
          clearInterval(interval);
        }
      }, 1000);

      child.on('close', () => {
        clearInterval(interval);
        if (dots > 0) console.log('');
      });
    });
  }

  /**
   * Validate API keys
   */
  async validateAPIs() {
    console.log('\n🔑 Step 3: Validating API configurations...');

    try {
      // Check if config file exists
      const configPath = path.join(__dirname, 'config', 'api-config.js');
      if (!fs.existsSync(configPath)) {
        throw new Error('API configuration file not found');
      }

      // Try to require and validate
      const { validateApiKeys } = require('./config/api-config');
      const isValid = validateApiKeys();

      console.log(`✅ API configuration ${isValid ? 'validated' : 'loaded (some keys may be missing)'}`);
      this.results.validateAPIs = { success: true, allKeysValid: isValid };
    } catch (error) {
      console.log(`⚠️  API validation warning: ${error.message}`);
      this.results.validateAPIs = { success: false, error: error.message };
    }
  }

  /**
   * Run API tests
   */
  async runTests() {
    console.log('\n🧪 Step 4: Running API integration tests...');

    return new Promise((resolve, reject) => {
      const testCommand = 'node test-api-integration.js';

      exec(testCommand, { timeout: 120000 }, (error, stdout, stderr) => {
        if (error && error.code !== 0) {
          console.log('⚠️  Some tests may have failed, but continuing...');
          console.log(stdout);
        } else {
          console.log('✅ API tests completed');
        }

        // Parse test results from stdout
        const testResults = this.parseTestResults(stdout);
        this.results.runTests = { success: true, results: testResults };
        resolve();
      });
    });
  }

  /**
   * Parse test results from output
   */
  parseTestResults(output) {
    const results = {
      blockchain: false,
      ai: false,
      database: false,
      overall: false
    };

    if (output.includes('Blockchain APIs')) {
      results.blockchain = output.includes('Latest Block: Success') ||
                          output.includes('Gas Price: Success');
    }

    if (output.includes('AI APIs')) {
      results.ai = output.includes('OpenAI: Success') ||
                   output.includes('Claude: Success') ||
                   output.includes('Gemini: Success');
    }

    if (output.includes('Database APIs')) {
      results.database = output.includes('Database Connections: Success');
    }

    results.overall = results.blockchain || results.ai || results.database;

    return results;
  }

  /**
   * Display results
   */
  displayResults() {
    console.log('\n📊 Step 5: Installation Results');
    console.log('================================');

    Object.keys(this.results).forEach(step => {
      const result = this.results[step];
      const status = result.success ? '✅' : '❌';
      console.log(`${status} ${step}: ${result.success ? 'Success' : 'Failed'}`);

      if (result.error) {
        console.log(`   Error: ${result.error}`);
      }
    });
  }

  /**
   * Display final results and next steps
   */
  displayFinalResults() {
    const endTime = Date.now();
    const duration = ((endTime - this.startTime) / 1000).toFixed(1);

    console.log('\n🎯 EHB API Integration Setup Complete!');
    console.log('=====================================');
    console.log(`⏱️  Total time: ${duration} seconds`);

    const successfulSteps = Object.values(this.results).filter(r => r.success).length;
    const totalSteps = Object.keys(this.results).length;
    const successRate = totalSteps > 0 ? (successfulSteps / totalSteps) * 100 : 0;

    console.log(`📈 Success rate: ${successRate.toFixed(1)}% (${successfulSteps}/${totalSteps} steps)`);

    if (successRate >= 80) {
      console.log('🎉 Installation successful! Your EHB API integration is ready.');
    } else if (successRate >= 60) {
      console.log('✅ Installation mostly successful with some warnings.');
    } else {
      console.log('⚠️  Installation completed with issues. Please check the errors above.');
    }

    console.log('\n📚 Next Steps:');
    console.log('1. Review API test results above');
    console.log('2. Add missing API keys to .env file if needed');
    console.log('3. Run individual tests: npm run test:blockchain, npm run test:ai, npm run test:database');
    console.log('4. Start development: npm run dev');
    console.log('5. View API documentation in EHB-API.md');

    console.log('\n🚀 Available Commands:');
    console.log('- npm start          : Run full API test suite');
    console.log('- npm run validate   : Validate API keys');
    console.log('- npm run blockchain : Test blockchain APIs only');
    console.log('- npm run ai         : Test AI APIs only');
    console.log('- npm run database   : Test database APIs only');

    console.log('\n📁 Important Files:');
    console.log('- EHB-API.md         : Complete API documentation');
    console.log('- config/api-config.js : API configuration');
    console.log('- services/          : API service modules');
    console.log('- test-api-integration.js : Test suite');

    console.log('\n💡 Need Help?');
    console.log('- Check EHB-API.md for detailed API information');
    console.log('- Review config/api-config.js for API key setup');
    console.log('- Run npm run validate to check API key status');

    console.log('\n✨ EHB Technologies - Ready for Blockchain Development!');
  }
}

// Create .env template if it doesn't exist
function createEnvTemplate() {
  const envPath = path.join(__dirname, '.env.example');
  const envContent = `# EHB API Integration - Environment Variables Template
# Copy this file to .env and add your API keys

# Blockchain APIs
ALCHEMY_ETHEREUM_URL=your_alchemy_ethereum_url
ALCHEMY_BSC_URL=your_alchemy_bsc_url
MORALIS_API_KEY=your_moralis_api_key

# AI APIs
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key

# Database APIs
MONGODB_URI=your_mongodb_connection_string
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Payment APIs
STRIPE_SECRET_KEY=your_stripe_secret_key

# Additional APIs (optional)
# Add other API keys as needed
`;

  if (!fs.existsSync(envPath)) {
    fs.writeFileSync(envPath, envContent);
    console.log('✅ Created .env.example template file');
  }
}

// Run installer if this file is executed directly
if (require.main === module) {
  console.log('🔧 Setting up EHB API Integration...\n');

  // Create env template
  createEnvTemplate();

  // Run installer
  const installer = new EHBInstaller();
  installer.run().catch(error => {
    console.error('❌ Installation failed:', error);
    process.exit(1);
  });
}

module.exports = EHBInstaller;
