const CardConfig = require('../models/CardConfig');
const User = require('../models/User');

// Get user's dashboard cards
const getUserCards = async (req, res) => {
  try {
    const { userId } = req.params;
    
    // Verify user exists
    const user = await User.findById(userId).select('sqlLevel');
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Get or create card configuration
    let cardConfig = await CardConfig.getByUserId(userId);
    if (!cardConfig) {
      cardConfig = await CardConfig.createDefaultConfig(userId);
    }

    // Filter cards based on user's SQL level
    const accessibleCards = cardConfig.cards.filter(card => {
      return cardConfig.hasCardAccess(card.id, user.sqlLevel);
    });

    res.json({
      success: true,
      data: {
        cards: accessibleCards,
        preferences: {
          layout: cardConfig.layout,
          columns: cardConfig.columns,
          autoRefresh: cardConfig.autoRefresh,
          refreshInterval: cardConfig.refreshInterval,
          visibility: cardConfig.visibility,
          dragAndDrop: cardConfig.dragAndDrop,
          theme: cardConfig.theme
        },
        userSQLLevel: user.sqlLevel
      }
    });

  } catch (error) {
    console.error('Error getting user cards:', error);
    res.status(500).json({ 
      error: 'Failed to get user cards',
      message: error.message 
    });
  }
};

// Update user's card configuration
const updateUserCards = async (req, res) => {
  try {
    const { userId } = req.params;
    const { cards, preferences } = req.body;

    // Verify user exists
    const user = await User.findById(userId).select('sqlLevel');
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Get or create card configuration
    let cardConfig = await CardConfig.getByUserId(userId);
    if (!cardConfig) {
      cardConfig = await CardConfig.createDefaultConfig(userId);
    }

    // Update cards if provided
    if (cards) {
      cardConfig.cards = cards;
    }

    // Update preferences if provided
    if (preferences) {
      Object.assign(cardConfig, preferences);
    }

    // Update analytics
    cardConfig.analytics.lastAccessed = new Date();
    cardConfig.analytics.accessCount += 1;

    await cardConfig.save();

    res.json({
      success: true,
      data: {
        message: 'Card configuration updated successfully',
        cards: cardConfig.cards,
        preferences: {
          layout: cardConfig.layout,
          columns: cardConfig.columns,
          autoRefresh: cardConfig.autoRefresh,
          refreshInterval: cardConfig.refreshInterval,
          visibility: cardConfig.visibility,
          dragAndDrop: cardConfig.dragAndDrop,
          theme: cardConfig.theme
        }
      }
    });

  } catch (error) {
    console.error('Error updating user cards:', error);
    res.status(500).json({ 
      error: 'Failed to update user cards',
      message: error.message 
    });
  }
};

// Reorder user's cards
const reorderCards = async (req, res) => {
  try {
    const { userId } = req.params;
    const { newOrder } = req.body;

    if (!newOrder || !Array.isArray(newOrder)) {
      return res.status(400).json({ error: 'New order array is required' });
    }

    // Get card configuration
    let cardConfig = await CardConfig.getByUserId(userId);
    if (!cardConfig) {
      cardConfig = await CardConfig.createDefaultConfig(userId);
    }

    // Reorder cards
    await cardConfig.reorderCards(newOrder);

    res.json({
      success: true,
      data: {
        message: 'Cards reordered successfully',
        cards: cardConfig.cards
      }
    });

  } catch (error) {
    console.error('Error reordering cards:', error);
    res.status(500).json({ 
      error: 'Failed to reorder cards',
      message: error.message 
    });
  }
};

// Add new card to user's dashboard
const addCard = async (req, res) => {
  try {
    const { userId } = req.params;
    const cardData = req.body;

    // Verify user exists
    const user = await User.findById(userId).select('sqlLevel');
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Get card configuration
    let cardConfig = await CardConfig.getByUserId(userId);
    if (!cardConfig) {
      cardConfig = await CardConfig.createDefaultConfig(userId);
    }

    // Check if user has access to this card's SQL level
    const levels = {
      'Free': 1,
      'Basic': 2,
      'Premium': 3,
      'Enterprise': 4
    };

    if (levels[cardData.sqlLevel] > levels[user.sqlLevel]) {
      return res.status(403).json({ 
        error: 'Insufficient SQL level to add this card',
        requiredLevel: cardData.sqlLevel,
        currentLevel: user.sqlLevel
      });
    }

    // Add card
    await cardConfig.addCard(cardData);

    res.json({
      success: true,
      data: {
        message: 'Card added successfully',
        card: cardConfig.cards[cardConfig.cards.length - 1]
      }
    });

  } catch (error) {
    console.error('Error adding card:', error);
    res.status(500).json({ 
      error: 'Failed to add card',
      message: error.message 
    });
  }
};

// Remove card from user's dashboard
const removeCard = async (req, res) => {
  try {
    const { userId, cardId } = req.params;

    // Get card configuration
    let cardConfig = await CardConfig.getByUserId(userId);
    if (!cardConfig) {
      return res.status(404).json({ error: 'Card configuration not found' });
    }

    // Remove card
    await cardConfig.removeCard(cardId);

    res.json({
      success: true,
      data: {
        message: 'Card removed successfully',
        cards: cardConfig.cards
      }
    });

  } catch (error) {
    console.error('Error removing card:', error);
    res.status(500).json({ 
      error: 'Failed to remove card',
      message: error.message 
    });
  }
};

// Update specific card
const updateCard = async (req, res) => {
  try {
    const { userId, cardId } = req.params;
    const updates = req.body;

    // Get card configuration
    let cardConfig = await CardConfig.getByUserId(userId);
    if (!cardConfig) {
      return res.status(404).json({ error: 'Card configuration not found' });
    }

    // Update card
    await cardConfig.updateCard(cardId, updates);

    res.json({
      success: true,
      data: {
        message: 'Card updated successfully',
        card: cardConfig.getCardById(cardId)
      }
    });

  } catch (error) {
    console.error('Error updating card:', error);
    res.status(500).json({ 
      error: 'Failed to update card',
      message: error.message 
    });
  }
};

// Get card templates (available cards for different SQL levels)
const getCardTemplates = async (req, res) => {
  try {
    const { sqlLevel } = req.params;

    const templates = {
      Free: [
        {
          id: 'emo',
          title: 'EMO',
          description: 'Emotional Intelligence & AI Agent',
          icon: '🧠',
          route: '/dashboard/emo',
          sqlLevel: 'Free'
        },
        {
          id: 'profile',
          title: 'Profile',
          description: 'User Profile & Settings',
          icon: '👤',
          route: '/dashboard/profile',
          sqlLevel: 'Free'
        }
      ],
      Basic: [
        {
          id: 'store',
          title: 'Store',
          description: 'Global EHB Store & Marketplace',
          icon: '🛒',
          route: '/dashboard/store',
          sqlLevel: 'Basic'
        },
        {
          id: 'analytics',
          title: 'Analytics',
          description: 'Data Analytics & Insights',
          icon: '📊',
          route: '/dashboard/analytics',
          sqlLevel: 'Basic'
        }
      ],
      Premium: [
        {
          id: 'wallet',
          title: 'Wallet',
          description: 'Digital Wallet & Transactions',
          icon: '💰',
          route: '/dashboard/wallet',
          sqlLevel: 'Premium'
        },
        {
          id: 'blockchain',
          title: 'Blockchain',
          description: 'Blockchain & Smart Contracts',
          icon: '⛓️',
          route: '/dashboard/blockchain',
          sqlLevel: 'Premium'
        }
      ],
      Enterprise: [
        {
          id: 'admin',
          title: 'Admin Panel',
          description: 'System Administration',
          icon: '⚙️',
          route: '/dashboard/admin',
          sqlLevel: 'Enterprise'
        },
        {
          id: 'monitoring',
          title: 'Monitoring',
          description: 'System Monitoring & Alerts',
          icon: '📡',
          route: '/dashboard/monitoring',
          sqlLevel: 'Enterprise'
        }
      ]
    };

    const availableTemplates = [];
    
    // Add templates for current level and below
    const levels = ['Free', 'Basic', 'Premium', 'Enterprise'];
    const userLevelIndex = levels.indexOf(sqlLevel);
    
    for (let i = 0; i <= userLevelIndex; i++) {
      availableTemplates.push(...templates[levels[i]]);
    }

    res.json({
      success: true,
      data: {
        templates: availableTemplates,
        userLevel: sqlLevel
      }
    });

  } catch (error) {
    console.error('Error getting card templates:', error);
    res.status(500).json({ 
      error: 'Failed to get card templates',
      message: error.message 
    });
  }
};

// Get dashboard suggestions based on user activity
const getDashboardSuggestions = async (req, res) => {
  try {
    const { userId } = req.params;

    // Get user and card configuration
    const user = await User.findById(userId).select('sqlLevel');
    const cardConfig = await CardConfig.getByUserId(userId);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Analyze user activity and generate suggestions
    const suggestions = {
      recommendedCards: [],
      layoutSuggestions: [],
      performanceTips: []
    };

    // Simple recommendation logic (can be enhanced with ML)
    if (cardConfig && cardConfig.analytics.accessCount < 5) {
      suggestions.recommendedCards.push({
        id: 'tutorial',
        title: 'Tutorial',
        description: 'Get started with EHB Dashboard',
        icon: '📚',
        route: '/dashboard/tutorial',
        sqlLevel: 'Free'
      });
    }

    if (user.sqlLevel === 'Free') {
      suggestions.recommendedCards.push({
        id: 'upgrade',
        title: 'Upgrade',
        description: 'Unlock more features',
        icon: '🚀',
        route: '/dashboard/upgrade',
        sqlLevel: 'Basic'
      });
    }

    res.json({
      success: true,
      data: suggestions
    });

  } catch (error) {
    console.error('Error getting dashboard suggestions:', error);
    res.status(500).json({ 
      error: 'Failed to get dashboard suggestions',
      message: error.message 
    });
  }
};

// Reset user's card configuration to default
const resetCardConfiguration = async (req, res) => {
  try {
    const { userId } = req.params;

    // Delete existing configuration
    await CardConfig.findOneAndDelete({ userId });

    // Create new default configuration
    const cardConfig = await CardConfig.createDefaultConfig(userId);

    res.json({
      success: true,
      data: {
        message: 'Card configuration reset to default',
        cards: cardConfig.cards
      }
    });

  } catch (error) {
    console.error('Error resetting card configuration:', error);
    res.status(500).json({ 
      error: 'Failed to reset card configuration',
      message: error.message 
    });
  }
};

module.exports = {
  getUserCards,
  updateUserCards,
  reorderCards,
  addCard,
  removeCard,
  updateCard,
  getCardTemplates,
  getDashboardSuggestions,
  resetCardConfiguration
}; 