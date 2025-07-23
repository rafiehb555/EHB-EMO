// 4-Layer Backend Architecture Setup
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

// Layer 1: Presentation Layer (API Gateway)
class PresentationLayer {
  constructor() {
    this.app = express();
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    this.app.use(cors());
    this.app.use(helmet());
    this.app.use(express.json());
  }

  setupRoutes() {
    // API Gateway routes
    this.app.get('/api/health', (req, res) => {
      res.json({ status: 'healthy', layer: 'presentation' });
    });

    this.app.use('/api/v1', require('./routes'));
  }

  start(port = 3000) {
    this.app.listen(port, () => {
      console.log(`🚀 Presentation Layer running on port ${port}`);
    });
  }
}

// Layer 2: Business Logic Layer
class BusinessLogicLayer {
  constructor() {
    this.services = {
      userService: new UserService(),
      walletService: new WalletService(),
      blockchainService: new BlockchainService(),
      aiService: new AIService()
    };
  }

  async processRequest(service, method, data) {
    try {
      const serviceInstance = this.services[service];
      if (!serviceInstance) {
        throw new Error(`Service ${service} not found`);
      }

      const result = await serviceInstance[method](data);
      return { success: true, data: result };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

// Layer 3: Data Access Layer
class DataAccessLayer {
  constructor() {
    this.repositories = {
      userRepository: new UserRepository(),
      walletRepository: new WalletRepository(),
      blockchainRepository: new BlockchainRepository(),
      aiRepository: new AIRepository()
    };
  }

  async getData(repository, method, params) {
    try {
      const repoInstance = this.repositories[repository];
      if (!repoInstance) {
        throw new Error(`Repository ${repository} not found`);
      }

      return await repoInstance[method](params);
    } catch (error) {
      throw new Error(`Data access error: ${error.message}`);
    }
  }
}

// Layer 4: Infrastructure Layer
class InfrastructureLayer {
  constructor() {
    this.database = new Database();
    this.cache = new Cache();
    this.externalAPIs = new ExternalAPIs();
  }

  async connect() {
    await this.database.connect();
    await this.cache.connect();
    console.log('🔧 Infrastructure Layer connected');
  }
}

// Service implementations
class UserService {
  async createUser(userData) {
    // Business logic for user creation
    return { id: Date.now(), ...userData };
  }

  async getUser(userId) {
    // Business logic for getting user
    return { id: userId, name: 'Test User' };
  }
}

class WalletService {
  async createWallet(userId) {
    // Business logic for wallet creation
    return { walletId: Date.now(), userId, balance: 0 };
  }

  async getBalance(walletId) {
    // Business logic for balance check
    return { walletId, balance: 1000 };
  }
}

class BlockchainService {
  async createTransaction(data) {
    // Business logic for blockchain transaction
    return { txHash: '0x123...', status: 'pending' };
  }

  async getTransaction(txHash) {
    // Business logic for transaction status
    return { txHash, status: 'confirmed' };
  }
}

class AIService {
  async processAIRequest(data) {
    // Business logic for AI processing
    return { result: 'AI processed data', confidence: 0.95 };
  }
}

// Repository implementations
class UserRepository {
  async create(userData) {
    // Database operation
    return { id: Date.now(), ...userData };
  }

  async findById(id) {
    // Database operation
    return { id, name: 'Test User', email: 'test@example.com' };
  }
}

class WalletRepository {
  async create(walletData) {
    // Database operation
    return { id: Date.now(), ...walletData };
  }

  async findByUserId(userId) {
    // Database operation
    return { id: Date.now(), userId, balance: 1000 };
  }
}

class BlockchainRepository {
  async saveTransaction(txData) {
    // Database operation
    return { id: Date.now(), ...txData };
  }

  async findByHash(hash) {
    // Database operation
    return { hash, status: 'confirmed', timestamp: Date.now() };
  }
}

class AIRepository {
  async saveAIResult(result) {
    // Database operation
    return { id: Date.now(), ...result };
  }
}

// Infrastructure implementations
class Database {
  async connect() {
    console.log('📊 Database connected');
  }
}

class Cache {
  async connect() {
    console.log('⚡ Cache connected');
  }
}

class ExternalAPIs {
  async connect() {
    console.log('🌐 External APIs connected');
  }
}

// Routes
const express = require('express');
const router = express.Router();

router.get('/users/:id', async (req, res) => {
  try {
    const businessLayer = new BusinessLogicLayer();
    const result = await businessLayer.processRequest('userService', 'getUser', req.params.id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/wallets', async (req, res) => {
  try {
    const businessLayer = new BusinessLogicLayer();
    const result = await businessLayer.processRequest('walletService', 'createWallet', req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;

// Main application
const presentationLayer = new PresentationLayer();
const infrastructureLayer = new InfrastructureLayer();

async function startApplication() {
  try {
    // Start infrastructure layer
    await infrastructureLayer.connect();

    // Start presentation layer
    presentationLayer.start(3000);

    console.log('✅ 4-Layer Backend Architecture Started');
  } catch (error) {
    console.error('❌ Error starting application:', error);
  }
}

module.exports = {
  PresentationLayer,
  BusinessLogicLayer,
  DataAccessLayer,
  InfrastructureLayer,
  startApplication
};
