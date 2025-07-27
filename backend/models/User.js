const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  // Basic Info
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },

  // SQL Level System
  sqlLevel: {
    type: String,
    enum: ['Free', 'Basic', 'Premium', 'Enterprise'],
    default: 'Free'
  },
  sqlExpiryDate: {
    type: Date,
    default: null
  },

  // Wallet Information
  wallet: {
    balance: {
      type: Number,
      default: 0
    },
    currency: {
      type: String,
      default: 'USD'
    },
    walletAddress: {
      type: String,
      default: null
    }
  },

  // Profile Information
  profile: {
    avatar: {
      type: String,
      default: null
    },
    bio: {
      type: String,
      default: ''
    },
    location: {
      type: String,
      default: ''
    },
    phone: {
      type: String,
      default: ''
    }
  },

  // Dashboard Preferences
  dashboardPreferences: {
    theme: {
      type: String,
      enum: ['light', 'dark', 'auto'],
      default: 'light'
    },
    layout: {
      type: String,
      enum: ['grid', 'list', 'compact'],
      default: 'grid'
    },
    autoRefresh: {
      type: Boolean,
      default: true
    },
    refreshInterval: {
      type: Number,
      default: 30000 // 30 seconds
    }
  },

  // Agent Status
  agentStatus: {
    isOnline: {
      type: Boolean,
      default: false
    },
    lastSeen: {
      type: Date,
      default: Date.now
    },
    activeAgents: [{
      agentId: String,
      agentType: String,
      status: {
        type: String,
        enum: ['online', 'offline', 'error'],
        default: 'offline'
      }
    }]
  },

  // Permissions & Roles
  role: {
    type: String,
    enum: ['user', 'admin', 'moderator'],
    default: 'user'
  },
  permissions: [{
    type: String,
    enum: [
      'dashboard_access',
      'card_management',
      'agent_control',
      'admin_panel',
      'user_management',
      'system_monitoring'
    ]
  }],

  // Activity Tracking
  lastLogin: {
    type: Date,
    default: Date.now
  },
  loginCount: {
    type: Number,
    default: 0
  },
  isActive: {
    type: Boolean,
    default: true
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
userSchema.index({ email: 1 });
userSchema.index({ sqlLevel: 1 });
userSchema.index({ 'agentStatus.isOnline': 1 });
userSchema.index({ createdAt: -1 });

// Pre-save middleware to hash password
userSchema.pre('save', async function(next) {
  if (this.isModified('password')) {
    this.password = await bcrypt.hash(this.password, 12);
  }
  next();
});

// Instance method to check password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Instance method to check SQL level access
userSchema.methods.hasSQLAccess = function(requiredLevel) {
  const levels = {
    'Free': 1,
    'Basic': 2,
    'Premium': 3,
    'Enterprise': 4
  };
  
  return levels[this.sqlLevel] >= levels[requiredLevel];
};

// Instance method to get SQL level info
userSchema.methods.getSQLInfo = function() {
  return {
    level: this.sqlLevel,
    expiryDate: this.sqlExpiryDate,
    isExpired: this.sqlExpiryDate ? new Date() > this.sqlExpiryDate : false,
    daysRemaining: this.sqlExpiryDate ? 
      Math.ceil((this.sqlExpiryDate - new Date()) / (1000 * 60 * 60 * 24)) : null
  };
};

// Instance method to update last seen
userSchema.methods.updateLastSeen = function() {
  this.agentStatus.lastSeen = new Date();
  return this.save();
};

// Static method to get users by SQL level
userSchema.statics.getUsersBySQLLevel = function(level) {
  return this.find({ sqlLevel: level, isActive: true });
};

// Static method to get online users
userSchema.statics.getOnlineUsers = function() {
  return this.find({ 'agentStatus.isOnline': true, isActive: true });
};

module.exports = mongoose.model('User', userSchema); 