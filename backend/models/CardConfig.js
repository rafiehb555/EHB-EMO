const mongoose = require('mongoose');

const cardConfigSchema = new mongoose.Schema({
  // User reference
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    unique: true
  },

  // Card configurations
  cards: [{
    id: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    route: {
      type: String,
      required: true
    },
    sqlLevel: {
      type: String,
      enum: ['Free', 'Basic', 'Premium', 'Enterprise'],
      required: true
    },
    isLocked: {
      type: Boolean,
      default: false
    },
    isActive: {
      type: Boolean,
      default: true
    },
    order: {
      type: Number,
      required: true
    },
    agentStatus: {
      type: String,
      enum: ['online', 'offline', 'error'],
      default: 'offline'
    },
    lastUpdated: {
      type: Date,
      default: Date.now
    },
    customSettings: {
      type: mongoose.Schema.Types.Mixed,
      default: {}
    }
  }],

  // Dashboard layout preferences
  layout: {
    type: String,
    enum: ['grid', 'list', 'compact'],
    default: 'grid'
  },
  columns: {
    type: Number,
    default: 4,
    min: 1,
    max: 6
  },
  autoRefresh: {
    type: Boolean,
    default: true
  },
  refreshInterval: {
    type: Number,
    default: 30000 // 30 seconds
  },

  // Card visibility settings
  visibility: {
    showSQLBadges: {
      type: Boolean,
      default: true
    },
    showAgentStatus: {
      type: Boolean,
      default: true
    },
    showLastUpdated: {
      type: Boolean,
      default: true
    },
    showOrderNumbers: {
      type: Boolean,
      default: false
    }
  },

  // Drag and drop settings
  dragAndDrop: {
    enabled: {
      type: Boolean,
      default: true
    },
    animation: {
      type: Boolean,
      default: true
    },
    snapToGrid: {
      type: Boolean,
      default: false
    }
  },

  // Theme and styling
  theme: {
    primaryColor: {
      type: String,
      default: '#2563EB'
    },
    cardStyle: {
      type: String,
      enum: ['default', 'minimal', 'detailed'],
      default: 'default'
    },
    borderRadius: {
      type: Number,
      default: 8
    },
    shadow: {
      type: String,
      enum: ['none', 'light', 'medium', 'heavy'],
      default: 'medium'
    }
  },

  // Analytics and tracking
  analytics: {
    lastAccessed: {
      type: Date,
      default: Date.now
    },
    accessCount: {
      type: Number,
      default: 0
    },
    favoriteCards: [{
      type: String
    }],
    recentlyUsed: [{
      cardId: String,
      lastUsed: {
        type: Date,
        default: Date.now
      }
    }]
  },

  // Backup and sync
  backup: {
    lastBackup: {
      type: Date,
      default: null
    },
    autoBackup: {
      type: Boolean,
      default: true
    },
    backupFrequency: {
      type: String,
      enum: ['daily', 'weekly', 'monthly'],
      default: 'weekly'
    }
  },

  // Timestamps
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
});

// Indexes for better performance
cardConfigSchema.index({ userId: 1 });
cardConfigSchema.index({ 'cards.id': 1 });
cardConfigSchema.index({ updatedAt: -1 });

// Pre-save middleware to update timestamps
cardConfigSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

// Instance method to get active cards
cardConfigSchema.methods.getActiveCards = function() {
  return this.cards.filter(card => card.isActive);
};

// Instance method to get cards by SQL level
cardConfigSchema.methods.getCardsBySQLLevel = function(level) {
  return this.cards.filter(card => card.sqlLevel === level);
};

// Instance method to reorder cards
cardConfigSchema.methods.reorderCards = function(newOrder) {
  newOrder.forEach((cardId, index) => {
    const card = this.cards.find(c => c.id === cardId);
    if (card) {
      card.order = index + 1;
    }
  });
  return this.save();
};

// Instance method to add card
cardConfigSchema.methods.addCard = function(cardData) {
  const newCard = {
    ...cardData,
    order: this.cards.length + 1,
    lastUpdated: new Date()
  };
  this.cards.push(newCard);
  return this.save();
};

// Instance method to remove card
cardConfigSchema.methods.removeCard = function(cardId) {
  this.cards = this.cards.filter(card => card.id !== cardId);
  // Reorder remaining cards
  this.cards.forEach((card, index) => {
    card.order = index + 1;
  });
  return this.save();
};

// Instance method to update card
cardConfigSchema.methods.updateCard = function(cardId, updates) {
  const card = this.cards.find(c => c.id === cardId);
  if (card) {
    Object.assign(card, updates, { lastUpdated: new Date() });
    return this.save();
  }
  return Promise.reject(new Error('Card not found'));
};

// Instance method to get card by ID
cardConfigSchema.methods.getCardById = function(cardId) {
  return this.cards.find(card => card.id === cardId);
};

// Instance method to check if user has access to card
cardConfigSchema.methods.hasCardAccess = function(cardId, userSQLLevel) {
  const card = this.getCardById(cardId);
  if (!card) return false;
  
  const levels = {
    'Free': 1,
    'Basic': 2,
    'Premium': 3,
    'Enterprise': 4
  };
  
  return levels[userSQLLevel] >= levels[card.sqlLevel];
};

// Static method to get config by user ID
cardConfigSchema.statics.getByUserId = function(userId) {
  return this.findOne({ userId }).populate('userId', 'name email sqlLevel');
};

// Static method to create default config
cardConfigSchema.statics.createDefaultConfig = function(userId) {
  const defaultCards = [
    {
      id: 'emo',
      title: 'EMO',
      description: 'Emotional Intelligence & AI Agent',
      icon: '🧠',
      route: '/dashboard/emo',
      sqlLevel: 'Free',
      isLocked: false,
      isActive: true,
      order: 1,
      agentStatus: 'online'
    },
    {
      id: 'store',
      title: 'Store',
      description: 'Global EHB Store & Marketplace',
      icon: '🛒',
      route: '/dashboard/store',
      sqlLevel: 'Basic',
      isLocked: false,
      isActive: true,
      order: 2,
      agentStatus: 'online'
    },
    {
      id: 'profile',
      title: 'Profile',
      description: 'User Profile & Settings',
      icon: '👤',
      route: '/dashboard/profile',
      sqlLevel: 'Free',
      isLocked: false,
      isActive: true,
      order: 3,
      agentStatus: 'online'
    },
    {
      id: 'wallet',
      title: 'Wallet',
      description: 'Digital Wallet & Transactions',
      icon: '💰',
      route: '/dashboard/wallet',
      sqlLevel: 'Premium',
      isLocked: true,
      isActive: false,
      order: 4,
      agentStatus: 'offline'
    }
  ];

  return this.create({
    userId,
    cards: defaultCards
  });
};

module.exports = mongoose.model('CardConfig', cardConfigSchema); 