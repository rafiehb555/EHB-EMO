const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true,
    minlength: [2, 'Name must be at least 2 characters'],
    maxlength: [50, 'Name cannot exceed 50 characters']
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters'],
    select: false // Don't include password in queries by default
  },
  role: {
    type: String,
    required: [true, 'Role is required'],
    enum: {
      values: ['franchise', 'seller', 'service_provider', 'school', 'agent', 'admin'],
      message: 'Role must be one of: franchise, seller, service_provider, school, agent, admin'
    },
    default: 'franchise'
  },
  sqlLevel: {
    type: String,
    enum: {
      values: ['Free', 'Basic', 'Normal', 'High', 'VIP'],
      message: 'SQL level must be one of: Free, Basic, Normal, High, VIP'
    },
    default: 'Free'
  },
  isVerified: {
    type: Boolean,
    default: false
  },
  businessData: {
    businessName: {
      type: String,
      trim: true,
      maxlength: [100, 'Business name cannot exceed 100 characters']
    },
    businessType: {
      type: String,
      enum: ['retail', 'service', 'manufacturing', 'technology', 'healthcare', 'education', 'other']
    },
    industry: {
      type: String,
      trim: true
    },
    revenue: {
      type: Number,
      min: [0, 'Revenue cannot be negative']
    },
    employeeCount: {
      type: Number,
      min: [1, 'Employee count must be at least 1']
    },
    location: {
      address: String,
      city: String,
      state: String,
      country: String,
      postalCode: String
    },
    yearsInBusiness: {
      type: Number,
      min: [0, 'Years in business cannot be negative']
    },
    phone: {
      type: String,
      trim: true
    },
    website: {
      type: String,
      trim: true
    },
    description: {
      type: String,
      maxlength: [500, 'Description cannot exceed 500 characters']
    }
  },
  verificationStatus: {
    type: String,
    enum: ['pending', 'approved', 'rejected', 'processing'],
    default: 'pending'
  },
  documents: [{
    type: {
      type: String,
      enum: ['business_license', 'tax_certificate', 'bank_statement', 'utility_bill', 'other']
    },
    filename: String,
    originalName: String,
    fileSize: Number,
    mimeType: String,
    uploadDate: {
      type: Date,
      default: Date.now
    },
    status: {
      type: String,
      enum: ['pending', 'approved', 'rejected'],
      default: 'pending'
    },
    verifiedAt: Date,
    verifiedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    rejectionReason: String
  }],
  franchiseData: {
    franchiseType: {
      type: String,
      enum: ['sub', 'master', 'corporate']
    },
    parentFranchise: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    subFranchises: [{
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    }],
    territory: {
      type: String,
      trim: true
    },
    commissionRate: {
      type: Number,
      min: [0, 'Commission rate cannot be negative'],
      max: [100, 'Commission rate cannot exceed 100%'],
      default: 0
    }
  },
  walletData: {
    balance: {
      type: Number,
      default: 0,
      min: [0, 'Balance cannot be negative']
    },
    currency: {
      type: String,
      default: 'USD'
    },
    transactions: [{
      type: {
        type: String,
        enum: ['credit', 'debit']
      },
      amount: Number,
      description: String,
      timestamp: {
        type: Date,
        default: Date.now
      },
      status: {
        type: String,
        enum: ['pending', 'completed', 'failed'],
        default: 'pending'
      }
    }]
  },
  settings: {
    notifications: {
      email: {
        type: Boolean,
        default: true
      },
      sms: {
        type: Boolean,
        default: false
      },
      push: {
        type: Boolean,
        default: true
      }
    },
    privacy: {
      profileVisibility: {
        type: String,
        enum: ['public', 'private', 'franchise_only'],
        default: 'franchise_only'
      }
    },
    preferences: {
      language: {
        type: String,
        default: 'en'
      },
      timezone: {
        type: String,
        default: 'UTC'
      }
    }
  },
  lastLogin: {
    type: Date
  },
  loginAttempts: {
    type: Number,
    default: 0
  },
  lockUntil: {
    type: Date
  },
  isActive: {
    type: Boolean,
    default: true
  },
  isDeleted: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Virtual for full name
userSchema.virtual('fullName').get(function() {
  return this.name;
});

// Virtual for business address
userSchema.virtual('businessAddress').get(function() {
  if (!this.businessData.location) return '';
  const location = this.businessData.location;
  return `${location.address || ''}, ${location.city || ''}, ${location.state || ''} ${location.postalCode || ''}`.trim();
});

// Index for better query performance
userSchema.index({ email: 1 });
userSchema.index({ role: 1 });
userSchema.index({ sqlLevel: 1 });
userSchema.index({ verificationStatus: 1 });
userSchema.index({ 'businessData.businessType': 1 });
userSchema.index({ createdAt: -1 });

// Pre-save middleware to hash password
userSchema.pre('save', async function(next) {
  // Only hash the password if it has been modified (or is new)
  if (!this.isModified('password')) return next();

  try {
    // Hash password with cost of 12
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Instance method to check password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Instance method to check if account is locked
userSchema.methods.isLocked = function() {
  return !!(this.lockUntil && this.lockUntil > Date.now());
};

// Instance method to increment login attempts
userSchema.methods.incLoginAttempts = function() {
  // If we have a previous lock that has expired, restart at 1
  if (this.lockUntil && this.lockUntil < Date.now()) {
    return this.updateOne({
      $unset: { lockUntil: 1 },
      $set: { loginAttempts: 1 }
    });
  }
  
  const updates = { $inc: { loginAttempts: 1 } };
  
  // Lock account after 5 failed attempts
  if (this.loginAttempts + 1 >= 5 && !this.isLocked()) {
    updates.$set = { lockUntil: Date.now() + 2 * 60 * 60 * 1000 }; // 2 hours
  }
  
  return this.updateOne(updates);
};

// Static method to find by email
userSchema.statics.findByEmail = function(email) {
  return this.findOne({ email: email.toLowerCase() });
};

// Static method to get users by role
userSchema.statics.findByRole = function(role) {
  return this.find({ role, isActive: true, isDeleted: false });
};

// Static method to get verified users
userSchema.statics.findVerified = function() {
  return this.find({ isVerified: true, isActive: true, isDeleted: false });
};

// Static method to get users by SQL level
userSchema.statics.findBySQLLevel = function(level) {
  return this.find({ sqlLevel: level, isActive: true, isDeleted: false });
};

module.exports = mongoose.model('User', userSchema); 