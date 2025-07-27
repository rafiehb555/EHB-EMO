const mongoose = require('mongoose');

const businessSchema = new mongoose.Schema({
  // Basic Information
  owner: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  businessName: {
    type: String,
    required: [true, 'Business name is required'],
    trim: true,
    maxlength: [100, 'Business name cannot exceed 100 characters']
  },
  businessType: {
    type: String,
    enum: ['seller', 'service_provider', 'school', 'franchise', 'agent'],
    required: [true, 'Business type is required']
  },
  industry: {
    type: String,
    required: [true, 'Industry is required'],
    trim: true
  },

  // Contact Information
  email: {
    type: String,
    required: [true, 'Business email is required'],
    lowercase: true,
    trim: true
  },
  phone: {
    type: String,
    required: [true, 'Business phone is required'],
    trim: true
  },
  website: {
    type: String,
    trim: true,
    match: [/^https?:\/\/.+/, 'Please enter a valid website URL']
  },

  // Address Information
  address: {
    street: {
      type: String,
      required: [true, 'Street address is required']
    },
    city: {
      type: String,
      required: [true, 'City is required']
    },
    state: {
      type: String,
      required: [true, 'State is required']
    },
    country: {
      type: String,
      required: [true, 'Country is required']
    },
    postalCode: {
      type: String,
      required: [true, 'Postal code is required']
    },
    coordinates: {
      lat: Number,
      lng: Number
    }
  },

  // Business Details
  description: {
    type: String,
    maxlength: [1000, 'Description cannot exceed 1000 characters']
  },
  yearEstablished: {
    type: Number,
    min: [1900, 'Year established must be after 1900'],
    max: [new Date().getFullYear(), 'Year established cannot be in the future']
  },
  employeeCount: {
    type: Number,
    min: [1, 'Employee count must be at least 1']
  },
  annualRevenue: {
    type: Number,
    min: [0, 'Annual revenue cannot be negative']
  },
  currency: {
    type: String,
    default: 'USD'
  },

  // Verification Status
  verificationStatus: {
    type: String,
    enum: ['pending', 'in_progress', 'verified', 'rejected', 'expired'],
    default: 'pending'
  },
  verificationScore: {
    type: Number,
    min: [0, 'Verification score cannot be negative'],
    max: [100, 'Verification score cannot exceed 100'],
    default: 0
  },
  verifiedAt: {
    type: Date
  },
  verifiedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  rejectionReason: {
    type: String,
    maxlength: [500, 'Rejection reason cannot exceed 500 characters']
  },

  // Documents
  documents: [{
    type: {
      type: String,
      enum: ['business_license', 'tax_certificate', 'bank_statement', 'utility_bill', 'insurance_certificate', 'other']
    },
    filename: String,
    originalName: String,
    mimeType: String,
    size: Number,
    uploadedAt: {
      type: Date,
      default: Date.now
    },
    status: {
      type: String,
      enum: ['pending', 'approved', 'rejected'],
      default: 'pending'
    },
    verifiedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    verifiedAt: Date,
    rejectionReason: String
  }],

  // Services/Products
  services: [{
    name: {
      type: String,
      required: true,
      trim: true
    },
    description: String,
    price: {
      type: Number,
      min: [0, 'Price cannot be negative']
    },
    currency: {
      type: String,
      default: 'USD'
    },
    category: String,
    isActive: {
      type: Boolean,
      default: true
    }
  }],

  // Operating Hours
  operatingHours: {
    monday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    },
    tuesday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    },
    wednesday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    },
    thursday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    },
    friday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    },
    saturday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    },
    sunday: {
      open: String,
      close: String,
      isOpen: { type: Boolean, default: true }
    }
  },

  // Franchise Information
  franchiseId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Franchise'
  },
  franchiseType: {
    type: String,
    enum: ['sub', 'master', 'corporate'],
    default: null
  },
  parentFranchise: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Franchise'
  },

  // Performance Metrics
  metrics: {
    totalOrders: {
      type: Number,
      default: 0
    },
    totalRevenue: {
      type: Number,
      default: 0
    },
    averageRating: {
      type: Number,
      min: [0, 'Average rating cannot be negative'],
      max: [5, 'Average rating cannot exceed 5'],
      default: 0
    },
    totalReviews: {
      type: Number,
      default: 0
    },
    completionRate: {
      type: Number,
      min: [0, 'Completion rate cannot be negative'],
      max: [100, 'Completion rate cannot exceed 100'],
      default: 0
    }
  },

  // Settings
  settings: {
    autoAcceptOrders: {
      type: Boolean,
      default: false
    },
    notifications: {
      email: { type: Boolean, default: true },
      sms: { type: Boolean, default: true },
      push: { type: Boolean, default: true }
    },
    visibility: {
      type: String,
      enum: ['public', 'private', 'franchise_only'],
      default: 'public'
    }
  },

  // Status
  status: {
    type: String,
    enum: ['active', 'inactive', 'suspended', 'pending'],
    default: 'pending'
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

// Indexes
businessSchema.index({ owner: 1 });
businessSchema.index({ businessName: 1 });
businessSchema.index({ businessType: 1 });
businessSchema.index({ industry: 1 });
businessSchema.index({ verificationStatus: 1 });
businessSchema.index({ status: 1 });
businessSchema.index({ 'address.coordinates': '2dsphere' });
businessSchema.index({ franchiseId: 1 });

// Virtual for full address
businessSchema.virtual('fullAddress').get(function() {
  const addr = this.address;
  return `${addr.street}, ${addr.city}, ${addr.state} ${addr.postalCode}, ${addr.country}`;
});

// Virtual for isVerified
businessSchema.virtual('isVerified').get(function() {
  return this.verificationStatus === 'verified';
});

// Virtual for isActive
businessSchema.virtual('isActive').get(function() {
  return this.status === 'active' && !this.isDeleted;
});

// Pre-save middleware
businessSchema.pre('save', function(next) {
  // Auto-update verification status based on documents
  if (this.documents && this.documents.length > 0) {
    const approvedDocs = this.documents.filter(doc => doc.status === 'approved');
    const totalDocs = this.documents.length;

    if (approvedDocs.length === totalDocs && totalDocs > 0) {
      this.verificationStatus = 'verified';
      this.verificationScore = 100;
      this.verifiedAt = new Date();
    } else if (approvedDocs.length > 0) {
      this.verificationStatus = 'in_progress';
      this.verificationScore = Math.round((approvedDocs.length / totalDocs) * 100);
    }
  }

  next();
});

// Static method to find verified businesses
businessSchema.statics.findVerified = function() {
  return this.find({
    verificationStatus: 'verified',
    status: 'active',
    isDeleted: false
  });
};

// Static method to find businesses by type
businessSchema.statics.findByType = function(type) {
  return this.find({
    businessType: type,
    status: 'active',
    isDeleted: false
  });
};

// Static method to find businesses by location
businessSchema.statics.findByLocation = function(coordinates, maxDistance = 10000) {
  return this.find({
    'address.coordinates': {
      $near: {
        $geometry: {
          type: 'Point',
          coordinates: [coordinates.lng, coordinates.lat]
        },
        $maxDistance: maxDistance
      }
    },
    status: 'active',
    isDeleted: false
  });
};

// Method to update metrics
businessSchema.methods.updateMetrics = function(orderData) {
  this.metrics.totalOrders += orderData.orders || 0;
  this.metrics.totalRevenue += orderData.revenue || 0;

  if (orderData.rating) {
    const currentTotal = this.metrics.averageRating * this.metrics.totalReviews;
    this.metrics.totalReviews += 1;
    this.metrics.averageRating = (currentTotal + orderData.rating) / this.metrics.totalReviews;
  }

  return this.save();
};

module.exports = mongoose.model('Business', businessSchema);
