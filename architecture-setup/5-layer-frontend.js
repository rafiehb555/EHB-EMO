// 5-Layer Frontend Architecture Setup
import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk';
import axios from 'axios';

// Layer 1: Presentation Layer (UI Components)
class PresentationLayer {
  constructor() {
    this.components = {
      Button: this.createButton(),
      Card: this.createCard(),
      Modal: this.createModal(),
      Form: this.createForm()
    };
  }

  createButton() {
    return ({ children, onClick, variant = 'primary', ...props }) => (
      <button
        className={`btn btn-${variant}`}
        onClick={onClick}
        {...props}
      >
        {children}
      </button>
    );
  }

  createCard() {
    return ({ title, children, ...props }) => (
      <div className="card" {...props}>
        {title && <div className="card-header">{title}</div>}
        <div className="card-body">{children}</div>
      </div>
    );
  }

  createModal() {
    return ({ isOpen, onClose, title, children }) => (
      isOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>{title}</h3>
              <button onClick={onClose}>&times;</button>
            </div>
            <div className="modal-body">{children}</div>
          </div>
        </div>
      )
    );
  }

  createForm() {
    return ({ onSubmit, children, ...props }) => (
      <form onSubmit={onSubmit} {...props}>
        {children}
      </form>
    );
  }
}

// Layer 2: State Management Layer (Redux)
class StateManagementLayer {
  constructor() {
    this.store = this.createStore();
    this.actions = this.createActions();
    this.reducers = this.createReducers();
  }

  createStore() {
    const rootReducer = combineReducers({
      user: this.createUserReducer(),
      wallet: this.createWalletReducer(),
      blockchain: this.createBlockchainReducer(),
      ai: this.createAIReducer()
    });

    return createStore(
      rootReducer,
      applyMiddleware(thunk)
    );
  }

  createActions() {
    return {
      // User actions
      setUser: (user) => ({ type: 'SET_USER', payload: user }),
      updateUser: (updates) => ({ type: 'UPDATE_USER', payload: updates }),

      // Wallet actions
      setWallet: (wallet) => ({ type: 'SET_WALLET', payload: wallet }),
      updateBalance: (balance) => ({ type: 'UPDATE_BALANCE', payload: balance }),

      // Blockchain actions
      setTransaction: (tx) => ({ type: 'SET_TRANSACTION', payload: tx }),
      updateTransactionStatus: (status) => ({ type: 'UPDATE_TX_STATUS', payload: status }),

      // AI actions
      setAIResult: (result) => ({ type: 'SET_AI_RESULT', payload: result })
    };
  }

  createUserReducer() {
    return (state = { user: null, loading: false }, action) => {
      switch (action.type) {
        case 'SET_USER':
          return { ...state, user: action.payload };
        case 'UPDATE_USER':
          return { ...state, user: { ...state.user, ...action.payload } };
        default:
          return state;
      }
    };
  }

  createWalletReducer() {
    return (state = { wallet: null, balance: 0 }, action) => {
      switch (action.type) {
        case 'SET_WALLET':
          return { ...state, wallet: action.payload };
        case 'UPDATE_BALANCE':
          return { ...state, balance: action.payload };
        default:
          return state;
      }
    };
  }

  createBlockchainReducer() {
    return (state = { transactions: [] }, action) => {
      switch (action.type) {
        case 'SET_TRANSACTION':
          return { ...state, transactions: [...state.transactions, action.payload] };
        case 'UPDATE_TX_STATUS':
          return { ...state, transactions: state.transactions.map(tx =>
            tx.hash === action.payload.hash ? { ...tx, status: action.payload.status } : tx
          )};
        default:
          return state;
      }
    };
  }

  createAIReducer() {
    return (state = { results: [] }, action) => {
      switch (action.type) {
        case 'SET_AI_RESULT':
          return { ...state, results: [...state.results, action.payload] };
        default:
          return state;
      }
    };
  }
}

// Layer 3: Business Logic Layer (Services)
class BusinessLogicLayer {
  constructor() {
    this.services = {
      userService: new UserService(),
      walletService: new WalletService(),
      blockchainService: new BlockchainService(),
      aiService: new AIService()
    };
  }

  async processBusinessLogic(service, method, data) {
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

class UserService {
  async login(credentials) {
    // Business logic for login
    const response = await axios.post('/api/auth/login', credentials);
    return response.data;
  }

  async register(userData) {
    // Business logic for registration
    const response = await axios.post('/api/auth/register', userData);
    return response.data;
  }

  async getProfile(userId) {
    // Business logic for getting user profile
    const response = await axios.get(`/api/users/${userId}`);
    return response.data;
  }
}

class WalletService {
  async createWallet(userId) {
    // Business logic for wallet creation
    const response = await axios.post('/api/wallets', { userId });
    return response.data;
  }

  async getBalance(walletId) {
    // Business logic for balance check
    const response = await axios.get(`/api/wallets/${walletId}/balance`);
    return response.data;
  }

  async transfer(fromWallet, toWallet, amount) {
    // Business logic for transfer
    const response = await axios.post('/api/wallets/transfer', {
      fromWallet,
      toWallet,
      amount
    });
    return response.data;
  }
}

class BlockchainService {
  async createTransaction(data) {
    // Business logic for blockchain transaction
    const response = await axios.post('/api/blockchain/transaction', data);
    return response.data;
  }

  async getTransactionStatus(txHash) {
    // Business logic for transaction status
    const response = await axios.get(`/api/blockchain/transaction/${txHash}`);
    return response.data;
  }
}

class AIService {
  async processAIRequest(data) {
    // Business logic for AI processing
    const response = await axios.post('/api/ai/process', data);
    return response.data;
  }

  async getAIRecommendations(userId) {
    // Business logic for AI recommendations
    const response = await axios.get(`/api/ai/recommendations/${userId}`);
    return response.data;
  }
}

// Layer 4: Data Layer (API Calls)
class DataLayer {
  constructor() {
    this.apiClient = this.createAPIClient();
    this.cache = this.createCache();
  }

  createAPIClient() {
    const client = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3000/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Request interceptor
    client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );

    return client;
  }

  createCache() {
    return {
      get: (key) => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
      },
      set: (key, value, ttl = 3600000) => {
        const item = {
          value,
          timestamp: Date.now(),
          ttl
        };
        localStorage.setItem(key, JSON.stringify(item));
      },
      clear: (key) => localStorage.removeItem(key)
    };
  }

  async getData(endpoint, useCache = true) {
    const cacheKey = `api_${endpoint}`;

    if (useCache) {
      const cached = this.cache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < cached.ttl) {
        return cached.value;
      }
    }

    try {
      const response = await this.apiClient.get(endpoint);
      if (useCache) {
        this.cache.set(cacheKey, response.data);
      }
      return response.data;
    } catch (error) {
      throw new Error(`API Error: ${error.message}`);
    }
  }

  async postData(endpoint, data) {
    try {
      const response = await this.apiClient.post(endpoint, data);
      return response.data;
    } catch (error) {
      throw new Error(`API Error: ${error.message}`);
    }
  }
}

// Layer 5: Infrastructure Layer (HTTP/WebSocket)
class InfrastructureLayer {
  constructor() {
    this.http = this.createHTTPClient();
    this.websocket = this.createWebSocket();
    this.storage = this.createStorage();
  }

  createHTTPClient() {
    return {
      get: (url, config) => axios.get(url, config),
      post: (url, data, config) => axios.post(url, data, config),
      put: (url, data, config) => axios.put(url, data, config),
      delete: (url, config) => axios.delete(url, config)
    };
  }

  createWebSocket() {
    return {
      connect: (url) => {
        const ws = new WebSocket(url);
        ws.onopen = () => console.log('WebSocket connected');
        ws.onmessage = (event) => console.log('WebSocket message:', event.data);
        ws.onerror = (error) => console.error('WebSocket error:', error);
        ws.onclose = () => console.log('WebSocket disconnected');
        return ws;
      }
    };
  }

  createStorage() {
    return {
      local: {
        get: (key) => localStorage.getItem(key),
        set: (key, value) => localStorage.setItem(key, value),
        remove: (key) => localStorage.removeItem(key),
        clear: () => localStorage.clear()
      },
      session: {
        get: (key) => sessionStorage.getItem(key),
        set: (key, value) => sessionStorage.setItem(key, value),
        remove: (key) => sessionStorage.removeItem(key),
        clear: () => sessionStorage.clear()
      }
    };
  }
}

// Main App Component
class App extends React.Component {
  constructor(props) {
    super(props);

    // Initialize all layers
    this.presentationLayer = new PresentationLayer();
    this.stateManagementLayer = new StateManagementLayer();
    this.businessLogicLayer = new BusinessLogicLayer();
    this.dataLayer = new DataLayer();
    this.infrastructureLayer = new InfrastructureLayer();
  }

  render() {
    return (
      <Provider store={this.stateManagementLayer.store}>
        <div className="app">
          <header className="app-header">
            <h1>🚀 EHB-5 Frontend Architecture</h1>
          </header>
          <main className="app-main">
            <Dashboard
              presentationLayer={this.presentationLayer}
              businessLogicLayer={this.businessLogicLayer}
              dataLayer={this.dataLayer}
            />
          </main>
        </div>
      </Provider>
    );
  }
}

// Dashboard Component
class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      wallet: null,
      transactions: [],
      loading: false
    };
  }

  async componentDidMount() {
    await this.loadDashboardData();
  }

  async loadDashboardData() {
    this.setState({ loading: true });

    try {
      // Use data layer to fetch data
      const user = await this.props.dataLayer.getData('/users/1');
      const wallet = await this.props.dataLayer.getData('/wallets/1');
      const transactions = await this.props.dataLayer.getData('/transactions');

      this.setState({ user, wallet, transactions, loading: false });
    } catch (error) {
      console.error('Error loading dashboard:', error);
      this.setState({ loading: false });
    }
  }

  render() {
    const { presentationLayer } = this.props;
    const { user, wallet, transactions, loading } = this.state;

    if (loading) {
      return <div>Loading...</div>;
    }

    return (
      <div className="dashboard">
        <presentationLayer.components.Card title="User Info">
          <p>Name: {user?.name}</p>
          <p>Email: {user?.email}</p>
        </presentationLayer.components.Card>

        <presentationLayer.components.Card title="Wallet">
          <p>Balance: ${wallet?.balance}</p>
          <p>Wallet ID: {wallet?.id}</p>
        </presentationLayer.components.Card>

        <presentationLayer.components.Card title="Recent Transactions">
          {transactions.map(tx => (
            <div key={tx.id}>
              <p>Hash: {tx.hash}</p>
              <p>Status: {tx.status}</p>
            </div>
          ))}
        </presentationLayer.components.Card>
      </div>
    );
  }
}

// Start the application
const root = document.getElementById('root');
ReactDOM.render(<App />, root);

console.log('✅ 5-Layer Frontend Architecture Started');

export {
  PresentationLayer,
  StateManagementLayer,
  BusinessLogicLayer,
  DataLayer,
  InfrastructureLayer,
  App
};
