const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const logger = require('../utils/logger');

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../../uploads/documents');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|pdf|doc|docx/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);

    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image, PDF and document files are allowed!'));
    }
  }
});

// Middleware to verify JWT token
const authenticateToken = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Access token required'
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-super-secret-jwt-key');
    const user = await User.findById(decoded.id).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }

    req.user = user;
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        success: false,
        error: 'Invalid token'
      });
    }
    next(error);
  }
};

// Get business profile
router.get('/profile', authenticateToken, async (req, res) => {
  try {
    const user = req.user;

    res.json({
      success: true,
      business: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        sqlLevel: user.sqlLevel,
        isVerified: user.isVerified,
        verificationStatus: user.verificationStatus,
        businessData: user.businessData,
        franchiseData: user.franchiseData,
        walletData: user.walletData,
        documents: user.documents,
        createdAt: user.createdAt,
        updatedAt: user.updatedAt
      }
    });

  } catch (error) {
    logger.error('Business profile fetch error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch business profile'
    });
  }
});

// Update business profile
router.put('/update', [
  body('businessData.businessName').optional().trim().isLength({ min: 2, max: 100 }),
  body('businessData.businessType').optional().isIn(['retail', 'service', 'manufacturing', 'technology', 'healthcare', 'education', 'other']),
  body('businessData.industry').optional().trim(),
  body('businessData.revenue').optional().isNumeric(),
  body('businessData.employeeCount').optional().isInt({ min: 1 }),
  body('businessData.yearsInBusiness').optional().isInt({ min: 0 }),
  body('businessData.phone').optional().trim(),
  body('businessData.website').optional().trim().isURL(),
  body('businessData.description').optional().trim().isLength({ max: 500 }),
], authenticateToken, async (req, res) => {
  try {
    // Check validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: errors.array()
      });
    }

    const user = req.user;
    const { businessData } = req.body;

    // Update business data
    if (businessData) {
      user.businessData = { ...user.businessData, ...businessData };
    }

    await user.save();

    logger.info(`Business profile updated for user: ${user.email}`);

    res.json({
      success: true,
      message: 'Business profile updated successfully',
      business: {
        id: user._id,
        businessData: user.businessData,
        updatedAt: user.updatedAt
      }
    });

  } catch (error) {
    logger.error('Business profile update error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update business profile'
    });
  }
});

// Upload business document
router.post('/upload-document', authenticateToken, upload.single('document'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: 'No file uploaded'
      });
    }

    const user = req.user;
    const { type } = req.body;

    if (!type || !['business_license', 'tax_certificate', 'bank_statement', 'utility_bill', 'other'].includes(type)) {
      return res.status(400).json({
        success: false,
        error: 'Valid document type is required'
      });
    }

    const document = {
      type,
      filename: req.file.filename,
      originalName: req.file.originalname,
      fileSize: req.file.size,
      mimeType: req.file.mimetype,
      uploadDate: new Date(),
      status: 'pending'
    };

    user.documents.push(document);
    await user.save();

    logger.info(`Document uploaded for user: ${user.email}, type: ${type}`);

    res.json({
      success: true,
      message: 'Document uploaded successfully',
      document
    });

  } catch (error) {
    logger.error('Document upload error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to upload document'
    });
  }
});

// Submit business verification
router.post('/submit-verification', authenticateToken, async (req, res) => {
  try {
    const user = req.user;

    // Check if user has uploaded required documents
    if (!user.documents || user.documents.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Please upload at least one document before submitting verification'
      });
    }

    // Check if business data is complete
    if (!user.businessData.businessName || !user.businessData.businessType) {
      return res.status(400).json({
        success: false,
        error: 'Please complete your business information before submitting verification'
      });
    }

    // Update verification status
    user.verificationStatus = 'processing';
    await user.save();

    logger.info(`Verification submitted for user: ${user.email}`);

    res.json({
      success: true,
      message: 'Verification submitted successfully',
      status: 'processing'
    });

  } catch (error) {
    logger.error('Verification submission error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to submit verification'
    });
  }
});

// Get verification status
router.get('/verification-status', authenticateToken, async (req, res) => {
  try {
    const user = req.user;

    res.json({
      success: true,
      verificationStatus: user.verificationStatus,
      isVerified: user.isVerified,
      documents: user.documents,
      sqlLevel: user.sqlLevel
    });

  } catch (error) {
    logger.error('Verification status fetch error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch verification status'
    });
  }
});

// Get business analytics
router.get('/analytics', authenticateToken, async (req, res) => {
  try {
    const user = req.user;

    // Calculate basic analytics
    const analytics = {
      profileCompletion: calculateProfileCompletion(user),
      documentCount: user.documents ? user.documents.length : 0,
      pendingDocuments: user.documents ? user.documents.filter(doc => doc.status === 'pending').length : 0,
      approvedDocuments: user.documents ? user.documents.filter(doc => doc.status === 'approved').length : 0,
      daysSinceRegistration: Math.floor((Date.now() - new Date(user.createdAt)) / (1000 * 60 * 60 * 24)),
      sqlLevel: user.sqlLevel,
      verificationStatus: user.verificationStatus
    };

    res.json({
      success: true,
      analytics
    });

  } catch (error) {
    logger.error('Analytics fetch error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch analytics'
    });
  }
});

// Helper function to calculate profile completion percentage
function calculateProfileCompletion(user) {
  const businessData = user.businessData || {};
  const requiredFields = [
    'businessName',
    'businessType',
    'industry',
    'location.address',
    'location.city',
    'phone'
  ];

  let completedFields = 0;
  requiredFields.forEach(field => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      if (businessData[parent] && businessData[parent][child]) {
        completedFields++;
      }
    } else {
      if (businessData[field]) {
        completedFields++;
      }
    }
  });

  return Math.round((completedFields / requiredFields.length) * 100);
}

// Get business recommendations
router.get('/recommendations', authenticateToken, async (req, res) => {
  try {
    const user = req.user;
    const recommendations = [];

    // Profile completion recommendation
    const profileCompletion = calculateProfileCompletion(user);
    if (profileCompletion < 100) {
      recommendations.push({
        type: 'profile_completion',
        title: 'Complete Your Profile',
        description: `Your profile is ${profileCompletion}% complete. Complete it to improve your verification chances.`,
        priority: 'high'
      });
    }

    // Document upload recommendation
    if (!user.documents || user.documents.length === 0) {
      recommendations.push({
        type: 'document_upload',
        title: 'Upload Business Documents',
        description: 'Upload your business license, tax certificate, and other required documents.',
        priority: 'high'
      });
    }

    // SQL level upgrade recommendation
    if (user.sqlLevel === 'Free' && user.isVerified) {
      recommendations.push({
        type: 'sql_upgrade',
        title: 'Upgrade Your SQL Level',
        description: 'Upgrade to Basic or higher to unlock more features and benefits.',
        priority: 'medium'
      });
    }

    res.json({
      success: true,
      recommendations
    });

  } catch (error) {
    logger.error('Recommendations fetch error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch recommendations'
    });
  }
});

module.exports = router; 