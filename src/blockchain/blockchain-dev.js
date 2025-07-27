#!/usr/bin/env node
/**
 * EHB Blockchain Development Environment
 * Supports: Ethereum, Solana, DeFi, NFTs, Smart Contracts
 */

const { ethers } = require('ethers');
const Web3 = require('web3');
const chalk = require('chalk');
const ora = require('ora');
const fs = require('fs-extra');
const path = require('path');

class BlockchainDevEnvironment {
  constructor() {
    this.providers = new Map();
    this.contracts = new Map();
    this.accounts = [];
    this.networks = {
      ethereum: {
        mainnet: 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
        testnet: 'https://goerli.infura.io/v3/YOUR_PROJECT_ID',
        local: 'http://localhost:8545',
      },
      solana: {
        mainnet: 'https://api.mainnet-beta.solana.com',
        testnet: 'https://api.testnet.solana.com',
        devnet: 'https://api.devnet.solana.com',
      },
    };
  }

  async initialize() {
    console.log(
      chalk.blue('🔗 Initializing Blockchain Development Environment...')
    );

    await this.setupProviders();
    await this.setupAccounts();
    await this.loadTemplates();

    console.log(chalk.green('✅ Blockchain environment ready!'));
  }

  async setupProviders() {
    const spinner = ora('Setting up blockchain providers...').start();

    try {
      // Setup Ethereum providers
      const ethereumProvider = new ethers.providers.JsonRpcProvider(
        this.networks.ethereum.local
      );
      this.providers.set('ethereum', ethereumProvider);

      // Setup Web3 provider
      const web3 = new Web3(this.networks.ethereum.local);
      this.providers.set('web3', web3);

      spinner.succeed('Blockchain providers configured');
    } catch (error) {
      spinner.fail('Failed to setup providers');
      console.error(error);
    }
  }

  async setupAccounts() {
    const spinner = ora('Setting up development accounts...').start();

    try {
      // Generate test accounts
      for (let i = 0; i < 5; i++) {
        const wallet = ethers.Wallet.createRandom();
        this.accounts.push({
          address: wallet.address,
          privateKey: wallet.privateKey,
          balance: '0',
        });
      }

      spinner.succeed(`Created ${this.accounts.length} test accounts`);
    } catch (error) {
      spinner.fail('Failed to setup accounts');
      console.error(error);
    }
  }

  async loadTemplates() {
    const templates = {
      'smart-contract': {
        name: 'Basic Smart Contract',
        description: 'Simple Ethereum smart contract template',
        files: [
          {
            name: 'contracts/BasicContract.sol',
            content: this.getBasicContractTemplate(),
          },
          {
            name: 'scripts/deploy.js',
            content: this.getDeployScriptTemplate(),
          },
          {
            name: 'test/BasicContract.test.js',
            content: this.getTestTemplate(),
          },
        ],
      },
      'defi-protocol': {
        name: 'DeFi Protocol',
        description: 'Decentralized Finance protocol template',
        files: [
          {
            name: 'contracts/DeFiProtocol.sol',
            content: this.getDeFiProtocolTemplate(),
          },
          {
            name: 'scripts/deploy.js',
            content: this.getDeFiDeployTemplate(),
          },
        ],
      },
      'nft-collection': {
        name: 'NFT Collection',
        description: 'Non-Fungible Token collection template',
        files: [
          {
            name: 'contracts/NFTCollection.sol',
            content: this.getNFTCollectionTemplate(),
          },
          {
            name: 'scripts/deploy.js',
            content: this.getNFTDeployTemplate(),
          },
        ],
      },
    };

    this.templates = templates;
  }

  getBasicContractTemplate() {
    return `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BasicContract {
    string public name;
    uint256 public value;
    
    event ValueChanged(uint256 newValue);
    
    constructor(string memory _name) {
        name = _name;
        value = 0;
    }
    
    function setValue(uint256 _value) public {
        value = _value;
        emit ValueChanged(_value);
    }
    
    function getValue() public view returns (uint256) {
        return value;
    }
}`;
  }

  getDeFiProtocolTemplate() {
    return `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract DeFiProtocol is ReentrancyGuard {
    IERC20 public token;
    mapping(address => uint256) public deposits;
    
    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    
    constructor(address _token) {
        token = IERC20(_token);
    }
    
    function deposit(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        
        deposits[msg.sender] += amount;
        emit Deposited(msg.sender, amount);
    }
    
    function withdraw(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        require(deposits[msg.sender] >= amount, "Insufficient balance");
        
        deposits[msg.sender] -= amount;
        require(token.transfer(msg.sender, amount), "Transfer failed");
        
        emit Withdrawn(msg.sender, amount);
    }
}`;
  }

  getNFTCollectionTemplate() {
    return `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract NFTCollection is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    uint256 public mintPrice = 0.01 ether;
    uint256 public maxSupply = 1000;
    
    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}
    
    function mint() external payable {
        require(msg.value >= mintPrice, "Insufficient payment");
        require(_tokenIds.current() < maxSupply, "Max supply reached");
        
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        _mint(msg.sender, newTokenId);
    }
    
    function setMintPrice(uint256 _price) external onlyOwner {
        mintPrice = _price;
    }
    
    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}`;
  }

  getDeployScriptTemplate() {
    return `const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with account:", deployer.address);
    
    const BasicContract = await ethers.getContractFactory("BasicContract");
    const contract = await BasicContract.deploy("My Contract");
    await contract.deployed();
    
    console.log("BasicContract deployed to:", contract.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });`;
  }

  getTestTemplate() {
    return `const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BasicContract", function () {
    let contract;
    let owner;
    
    beforeEach(async function () {
        [owner] = await ethers.getSigners();
        const BasicContract = await ethers.getContractFactory("BasicContract");
        contract = await BasicContract.deploy("Test Contract");
        await contract.deployed();
    });
    
    it("Should set the correct name", async function () {
        expect(await contract.name()).to.equal("Test Contract");
    });
    
    it("Should set and get value correctly", async function () {
        await contract.setValue(42);
        expect(await contract.getValue()).to.equal(42);
    });
});`;
  }

  async createProject(projectName, templateType) {
    const spinner = ora(
      `Creating ${templateType} project: ${projectName}`
    ).start();

    try {
      const projectPath = path.join('projects', projectName);
      await fs.ensureDir(projectPath);

      const template = this.templates[templateType];
      if (!template) {
        throw new Error(`Template ${templateType} not found`);
      }

      // Create project structure
      await fs.ensureDir(path.join(projectPath, 'contracts'));
      await fs.ensureDir(path.join(projectPath, 'scripts'));
      await fs.ensureDir(path.join(projectPath, 'test'));

      // Copy template files
      for (const file of template.files) {
        const filePath = path.join(projectPath, file.name);
        await fs.ensureDir(path.dirname(filePath));
        await fs.writeFile(filePath, file.content);
      }

      // Create package.json
      const packageJson = {
        name: projectName,
        version: '1.0.0',
        description: `EHB Blockchain Project: ${template.name}`,
        scripts: {
          compile: 'hardhat compile',
          test: 'hardhat test',
          deploy: 'hardhat run scripts/deploy.js',
          node: 'hardhat node',
        },
        dependencies: {
          hardhat: '^2.12.0',
          '@openzeppelin/contracts': '^4.8.0',
          ethers: '^5.7.0',
        },
        devDependencies: {
          '@nomicfoundation/hardhat-toolbox': '^2.0.0',
        },
      };

      await fs.writeJson(path.join(projectPath, 'package.json'), packageJson, {
        spaces: 2,
      });

      spinner.succeed(`Project ${projectName} created successfully!`);
      return projectPath;
    } catch (error) {
      spinner.fail(`Failed to create project: ${error.message}`);
      throw error;
    }
  }

  async deployContract(projectPath, contractName) {
    const spinner = ora(`Deploying ${contractName}...`).start();

    try {
      // Simulate deployment
      const provider = this.providers.get('ethereum');
      const wallet = new ethers.Wallet(this.accounts[0].privateKey, provider);

      // In real implementation, this would compile and deploy the actual contract
      const deploymentAddress = ethers.Wallet.createRandom().address;

      this.contracts.set(contractName, {
        address: deploymentAddress,
        deployedBy: wallet.address,
        deployedAt: new Date().toISOString(),
        network: 'local',
      });

      spinner.succeed(`${contractName} deployed to: ${deploymentAddress}`);
      return deploymentAddress;
    } catch (error) {
      spinner.fail(`Failed to deploy contract: ${error.message}`);
      throw error;
    }
  }

  async interactWithContract(contractAddress, functionName, ...args) {
    const spinner = ora(`Calling ${functionName} on contract...`).start();

    try {
      // Simulate contract interaction
      const result = `Transaction successful: ${functionName}(${args.join(', ')})`;

      spinner.succeed(result);
      return result;
    } catch (error) {
      spinner.fail(`Contract interaction failed: ${error.message}`);
      throw error;
    }
  }

  getAccountInfo() {
    return this.accounts.map((account) => ({
      address: account.address,
      balance: account.balance,
      privateKey: account.privateKey.substring(0, 10) + '...',
    }));
  }

  getContractInfo() {
    return Array.from(this.contracts.entries()).map(([name, contract]) => ({
      name,
      address: contract.address,
      deployedBy: contract.deployedBy,
      deployedAt: contract.deployedAt,
      network: contract.network,
    }));
  }
}

// Export for use in main agent
module.exports = BlockchainDevEnvironment;

// Start if run directly
if (require.main === module) {
  const env = new BlockchainDevEnvironment();
  env
    .initialize()
    .then(() => {
      console.log(
        chalk.green('🔗 Blockchain Development Environment is ready!')
      );
      console.log(chalk.blue('Available templates:'));
      for (const [key, template] of Object.entries(env.templates)) {
        console.log(chalk.cyan(`  - ${key}: ${template.name}`));
      }
    })
    .catch(console.error);
}
