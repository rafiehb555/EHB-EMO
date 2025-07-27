/**
 * EHB API Integration Test Demo
 * Tests all integrated APIs and services
 *
 * @version 1.0.0
 * @author EHB Technologies
 */

require('dotenv').config();

const BlockchainService = require('./services/blockchain-service');
const AIService = require('./services/ai-service');
const DatabaseService = require('./services/database-service');
const { validateApiKeys } = require('./config/api-config');

class APITestDemo {
  constructor() {
    this.blockchainService = new BlockchainService();
    this.aiService = new AIService();
    this.databaseService = new DatabaseService();
    this.testResults = {};
  }

  /**
   * Run all API tests
   */
  async runAllTests() {
    console.log('🚀 Starting EHB API Integration Tests...\n');

    // Validate API keys first
    const keysValid = validateApiKeys();
    console.log(`🔑 API Keys Validation: ${keysValid ? '✅ Valid' : '❌ Some keys missing'}\n`);

    // Test all services
    await this.testBlockchainAPIs();
    await this.testAIAPIs();
    await this.testDatabaseAPIs();

    // Display results
    this.displayResults();
  }

  /**
   * Test blockchain APIs
   */
  async testBlockchainAPIs() {
    console.log('⛓️  Testing Blockchain APIs...');
    this.testResults.blockchain = {};

    try {
      // Test latest block
      console.log('   Testing latest block fetch...');
      const blockResult = await this.blockchainService.getLatestBlock('bsc');
      this.testResults.blockchain.latestBlock = blockResult.success;
      console.log(`   ✅ Latest Block: ${blockResult.success ? 'Success' : 'Failed'}`);

      // Test gas price
      console.log('   Testing gas price fetch...');
      const gasResult = await this.blockchainService.getGasPrice('bsc');
      this.testResults.blockchain.gasPrice = gasResult.success;
      console.log(`   ✅ Gas Price: ${gasResult.success ? 'Success' : 'Failed'}`);

      // Test network stats
      console.log('   Testing network statistics...');
      const statsResult = await this.blockchainService.getNetworkStats('bsc');
      this.testResults.blockchain.networkStats = statsResult.success;
      console.log(`   ✅ Network Stats: ${statsResult.success ? 'Success' : 'Failed'}`);

      // Test balance check (using a known address)
      console.log('   Testing balance check...');
      const testAddress = '0x8ba1f109551bD432803012645Hac136c';
      const balanceResult = await this.blockchainService.getBalance(testAddress, 'bsc');
      this.testResults.blockchain.balance = balanceResult.success;
      console.log(`   ✅ Balance Check: ${balanceResult.success ? 'Success' : 'Failed'}`);

    } catch (error) {
      console.error('   ❌ Blockchain API test error:', error.message);
      this.testResults.blockchain.error = error.message;
    }

    console.log('');
  }

  /**
   * Test AI APIs
   */
  async testAIAPIs() {
    console.log('🤖 Testing AI APIs...');
    this.testResults.ai = {};

    try {
      // Test OpenAI
      console.log('   Testing OpenAI GPT...');
      const openaiResult = await this.aiService.generateText(
        'Explain blockchain in one sentence.',
        'gpt-3.5-turbo',
        100
      );
      this.testResults.ai.openai = openaiResult.success;
      console.log(`   ✅ OpenAI: ${openaiResult.success ? 'Success' : 'Failed'}`);
      if (openaiResult.success) {
        console.log(`   📝 Response: ${openaiResult.response.substring(0, 100)}...`);
      }

      // Test Claude
      console.log('   Testing Anthropic Claude...');
      const claudeResult = await this.aiService.generateTextClaude(
        'What is smart contract security?',
        100
      );
      this.testResults.ai.claude = claudeResult.success;
      console.log(`   ✅ Claude: ${claudeResult.success ? 'Success' : 'Failed'}`);

      // Test Google Gemini
      console.log('   Testing Google Gemini...');
      const geminiResult = await this.aiService.generateTextGemini(
        'Explain DeFi in simple terms.'
      );
      this.testResults.ai.gemini = geminiResult.success;
      console.log(`   ✅ Gemini: ${geminiResult.success ? 'Success' : 'Failed'}`);

      // Test sentiment analysis
      console.log('   Testing sentiment analysis...');
      const sentimentResult = await this.aiService.analyzeSentiment(
        'EHB Blockchain is an amazing project!'
      );
      this.testResults.ai.sentiment = sentimentResult.success;
      console.log(`   ✅ Sentiment Analysis: ${sentimentResult.success ? 'Success' : 'Failed'}`);

    } catch (error) {
      console.error('   ❌ AI API test error:', error.message);
      this.testResults.ai.error = error.message;
    }

    console.log('');
  }

  /**
   * Test database APIs
   */
  async testDatabaseAPIs() {
    console.log('💾 Testing Database APIs...');
    this.testResults.database = {};

    try {
      // Test database connections
      console.log('   Testing database connections...');
      const connectionResult = await this.databaseService.testConnections();
      this.testResults.database.connections = connectionResult.success;
      console.log(`   ✅ Database Connections: ${connectionResult.success ? 'Success' : 'Failed'}`);
      console.log(`   📊 MongoDB: ${connectionResult.connections.mongodb ? '✅' : '❌'}`);
      console.log(`   📊 Supabase: ${connectionResult.connections.supabase ? '✅' : '❌'}`);

      // Test user creation
      console.log('   Testing user data save...');
      const testUser = {
        username: 'test_user_' + Date.now(),
        email: 'test@ehb.com',
        walletAddress: '0x1234567890123456789012345678901234567890',
        role: 'user'
      };

      const userResult = await this.databaseService.saveUser(testUser, 'mongodb');
      this.testResults.database.saveUser = userResult.success;
      console.log(`   ✅ Save User: ${userResult.success ? 'Success' : 'Failed'}`);

      // Test transaction save
      console.log('   Testing transaction save...');
      const testTransaction = {
        userId: 'test_user_123',
        transactionHash: '0xabcdef1234567890',
        amount: '1.5',
        network: 'bsc',
        type: 'transfer'
      };

      const txResult = await this.databaseService.saveTransaction(testTransaction);
      this.testResults.database.saveTransaction = txResult.success;
      console.log(`   ✅ Save Transaction: ${txResult.success ? 'Success' : 'Failed'}`);

    } catch (error) {
      console.error('   ❌ Database API test error:', error.message);
      this.testResults.database.error = error.message;
    }

    console.log('');
  }

  /**
   * Test smart contract analysis
   */
  async testSmartContractAnalysis() {
    console.log('📋 Testing Smart Contract Analysis...');

    const sampleContract = `
    pragma solidity ^0.8.0;

    contract EHBToken {
        string public name = "EHB Coin";
        string public symbol = "EHBGC";
        uint256 public totalSupply = 1000000;

        mapping(address => uint256) public balanceOf;

        constructor() {
            balanceOf[msg.sender] = totalSupply;
        }

        function transfer(address to, uint256 amount) public returns (bool) {
            require(balanceOf[msg.sender] >= amount, "Insufficient balance");
            balanceOf[msg.sender] -= amount;
            balanceOf[to] += amount;
            return true;
        }
    }`;

    try {
      const analysisResult = await this.aiService.analyzeSmartContract(sampleContract, 'openai');
      this.testResults.contractAnalysis = analysisResult.success;
      console.log(`   ✅ Contract Analysis: ${analysisResult.success ? 'Success' : 'Failed'}`);

      if (analysisResult.success) {
        console.log('   📝 Analysis Preview:');
        console.log(`   ${analysisResult.contractAnalysis.response.substring(0, 200)}...`);
      }
    } catch (error) {
      console.error('   ❌ Contract analysis error:', error.message);
      this.testResults.contractAnalysis = false;
    }

    console.log('');
  }

  /**
   * Test multi-AI comparison
   */
  async testMultiAIComparison() {
    console.log('🔄 Testing Multi-AI Comparison...');

    try {
      const comparisonResult = await this.aiService.multiAIComparison(
        'What are the benefits of blockchain technology?'
      );

      this.testResults.multiAI = comparisonResult.success;
      console.log(`   ✅ Multi-AI Comparison: ${comparisonResult.success ? 'Success' : 'Failed'}`);

      if (comparisonResult.success) {
        console.log('   📊 AI Responses:');
        console.log(`   OpenAI: ${comparisonResult.responses.openai.success ? '✅' : '❌'}`);
        console.log(`   Claude: ${comparisonResult.responses.claude.success ? '✅' : '❌'}`);
        console.log(`   Gemini: ${comparisonResult.responses.gemini.success ? '✅' : '❌'}`);
      }
    } catch (error) {
      console.error('   ❌ Multi-AI comparison error:', error.message);
      this.testResults.multiAI = false;
    }

    console.log('');
  }

  /**
   * Display test results
   */
  displayResults() {
    console.log('📊 EHB API Integration Test Results');
    console.log('=====================================\n');

    // Blockchain results
    console.log('⛓️  Blockchain APIs:');
    const blockchainTests = this.testResults.blockchain || {};
    console.log(`   Latest Block: ${blockchainTests.latestBlock ? '✅' : '❌'}`);
    console.log(`   Gas Price: ${blockchainTests.gasPrice ? '✅' : '❌'}`);
    console.log(`   Network Stats: ${blockchainTests.networkStats ? '✅' : '❌'}`);
    console.log(`   Balance Check: ${blockchainTests.balance ? '✅' : '❌'}`);

    // AI results
    console.log('\n🤖 AI APIs:');
    const aiTests = this.testResults.ai || {};
    console.log(`   OpenAI: ${aiTests.openai ? '✅' : '❌'}`);
    console.log(`   Claude: ${aiTests.claude ? '✅' : '❌'}`);
    console.log(`   Gemini: ${aiTests.gemini ? '✅' : '❌'}`);
    console.log(`   Sentiment Analysis: ${aiTests.sentiment ? '✅' : '❌'}`);

    // Database results
    console.log('\n💾 Database APIs:');
    const dbTests = this.testResults.database || {};
    console.log(`   Connections: ${dbTests.connections ? '✅' : '❌'}`);
    console.log(`   Save User: ${dbTests.saveUser ? '✅' : '❌'}`);
    console.log(`   Save Transaction: ${dbTests.saveTransaction ? '✅' : '❌'}`);

    // Additional tests
    if (this.testResults.contractAnalysis !== undefined) {
      console.log('\n📋 Additional Tests:');
      console.log(`   Contract Analysis: ${this.testResults.contractAnalysis ? '✅' : '❌'}`);
    }

    if (this.testResults.multiAI !== undefined) {
      console.log(`   Multi-AI Comparison: ${this.testResults.multiAI ? '✅' : '❌'}`);
    }

    // Calculate success rate
    const allTests = Object.values(this.testResults).flat();
    const successfulTests = allTests.filter(result => result === true).length;
    const totalTests = allTests.filter(result => typeof result === 'boolean').length;
    const successRate = totalTests > 0 ? (successfulTests / totalTests) * 100 : 0;

    console.log('\n📈 Overall Results:');
    console.log(`   Success Rate: ${successRate.toFixed(1)}% (${successfulTests}/${totalTests})`);
    console.log(`   Status: ${successRate >= 80 ? '🎉 Excellent' : successRate >= 60 ? '✅ Good' : '⚠️  Needs Attention'}`);

    console.log('\n🎯 EHB API Integration Test Complete!\n');
  }

  /**
   * Save test results to database
   */
  async saveTestResults() {
    try {
      const testReport = {
        timestamp: new Date(),
        results: this.testResults,
        environment: process.env.NODE_ENV || 'development',
        version: '1.0.0'
      };

      await this.databaseService.saveApiUsage({
        apiName: 'API_INTEGRATION_TEST',
        success: true,
        data: testReport
      });

      console.log('✅ Test results saved to database');
    } catch (error) {
      console.error('❌ Error saving test results:', error.message);
    }
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  const demo = new APITestDemo();

  demo.runAllTests()
    .then(() => demo.testSmartContractAnalysis())
    .then(() => demo.testMultiAIComparison())
    .then(() => demo.saveTestResults())
    .then(() => {
      console.log('🏁 All tests completed!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Test execution error:', error);
      process.exit(1);
    });
}

module.exports = APITestDemo;
