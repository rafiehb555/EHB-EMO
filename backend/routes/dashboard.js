const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const cardController = require('../controllers/cardController');
const auth = require('../middleware/auth');

// User Profile Routes
router.get('/user/profile/:id', auth, userController.getUserProfile);
router.put('/user/profile/:id', auth, userController.updateUserProfile);
router.get('/user/sql-check/:id', auth, userController.checkSQLLevel);
router.put('/user/sql-level/:id', auth, userController.updateSQLLevel);
router.put('/user/wallet/:id', auth, userController.updateWallet);
router.put('/user/dashboard-preferences/:id', auth, userController.updateDashboardPreferences);
router.put('/user/agent-status/:id', auth, userController.updateAgentStatus);

// Card Management Routes
router.get('/user/cards/:userId', auth, cardController.getUserCards);
router.put('/user/cards/:userId', auth, cardController.updateUserCards);
router.post('/user/cards/:userId/reorder', auth, cardController.reorderCards);
router.post('/user/cards/:userId/add', auth, cardController.addCard);
router.delete('/user/cards/:userId/:cardId', auth, cardController.removeCard);
router.put('/user/cards/:userId/:cardId', auth, cardController.updateCard);

// Card Templates and Suggestions
router.get('/card-templates/:sqlLevel', auth, cardController.getCardTemplates);
router.get('/dashboard/suggestions/:userId', auth, cardController.getDashboardSuggestions);
router.post('/user/cards/:userId/reset', auth, cardController.resetCardConfiguration);

// Admin Routes (for user management)
router.get('/admin/users', auth, userController.getAllUsers);
router.get('/admin/users/sql-level/:level', auth, userController.getUsersBySQLLevel);
router.get('/admin/users/online', auth, userController.getOnlineUsers);

// Health check for dashboard
router.get('/health', (req, res) => {
  res.json({
    success: true,
    message: 'Dashboard API is running',
    timestamp: new Date().toISOString(),
    endpoints: {
      userProfile: '/api/dashboard/user/profile/:id',
      userCards: '/api/dashboard/user/cards/:userId',
      sqlCheck: '/api/dashboard/user/sql-check/:id',
      cardTemplates: '/api/dashboard/card-templates/:sqlLevel',
      suggestions: '/api/dashboard/suggestions/:userId'
    }
  });
});

// Error handling middleware for dashboard routes
router.use((err, req, res, next) => {
  console.error('Dashboard route error:', err);
  res.status(500).json({
    success: false,
    error: 'Dashboard API error',
    message: err.message
  });
});

module.exports = router; 