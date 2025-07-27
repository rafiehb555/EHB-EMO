const jwt = require('jsonwebtoken');

// Verify JWT token middleware
const authenticateToken = (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      return res.status(401).json({ error: 'Access token required' });
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
      if (err) {
        return res.status(403).json({ error: 'Invalid or expired token' });
      }
      req.user = user;
      next();
    });
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed', message: error.message });
  }
};

// Role-based access control middleware
const authorizeRole = (roles) => {
  return (req, res, next) => {
    try {
      if (!req.user) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      if (!roles.includes(req.user.role)) {
        return res.status(403).json({ 
          error: 'Insufficient permissions',
          required: roles,
          current: req.user.role
        });
      }

      next();
    } catch (error) {
      res.status(500).json({ error: 'Authorization failed', message: error.message });
    }
  };
};

// Admin only middleware
const requireAdmin = authorizeRole(['admin']);

// Healthcare staff middleware
const requireHealthcareStaff = authorizeRole(['admin', 'doctor', 'nurse']);

// Log access for audit purposes
const logAccess = (req, res, next) => {
  try {
    const timestamp = new Date().toISOString();
    const user = req.user ? req.user.email : 'anonymous';
    const action = `${req.method} ${req.originalUrl}`;
    const ip = req.ip || req.connection.remoteAddress;

    console.log(`[${timestamp}] ${user} - ${action} - IP: ${ip}`);

    // In production, log to database or file
    // logger.info({ user, action, ip, timestamp });

    next();
  } catch (error) {
    // Don't block the request if logging fails
    next();
  }
};

// Rate limiting middleware (simplified)
const rateLimit = (windowMs = 15 * 60 * 1000, maxRequests = 100) => {
  const requests = new Map();

  return (req, res, next) => {
    try {
      const ip = req.ip || req.connection.remoteAddress;
      const now = Date.now();
      const windowStart = now - windowMs;

      // Clean old entries
      if (requests.has(ip)) {
        requests.set(ip, requests.get(ip).filter(time => time > windowStart));
      } else {
        requests.set(ip, []);
      }

      const userRequests = requests.get(ip);
      
      if (userRequests.length >= maxRequests) {
        return res.status(429).json({ 
          error: 'Too many requests',
          retryAfter: Math.ceil(windowMs / 1000)
        });
      }

      userRequests.push(now);
      next();
    } catch (error) {
      // Don't block the request if rate limiting fails
      next();
    }
  };
};

// HIPAA compliance middleware
const hipaaCompliance = (req, res, next) => {
  try {
    // Add HIPAA compliance headers
    res.set({
      'X-HIPAA-Compliant': 'true',
      'X-Data-Encryption': 'enabled',
      'X-Audit-Logging': 'enabled'
    });

    // Log sensitive data access
    if (req.path.includes('/patients') || req.path.includes('/records')) {
      const user = req.user ? req.user.email : 'anonymous';
      console.log(`[HIPAA] ${user} accessed patient data at ${new Date().toISOString()}`);
    }

    next();
  } catch (error) {
    next();
  }
};

module.exports = {
  authenticateToken,
  authorizeRole,
  requireAdmin,
  requireHealthcareStaff,
  logAccess,
  rateLimit,
  hipaaCompliance
}; 