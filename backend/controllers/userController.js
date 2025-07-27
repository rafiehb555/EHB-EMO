const User = require('../models/User');
const CardConfig = require('../models/CardConfig');

// Get user profile with full details
const getUserProfile = async (req, res) => {
  try {
    const { id } = req.params;
    
    const user = await User.findById(id).select('-password');
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Get user's card configuration
    let cardConfig = await CardConfig.getByUserId(id);
    if (!cardConfig) {
      // Create default card config if doesn't exist
      cardConfig = await CardConfig.createDefaultConfig(id);
    }

    // Get SQL level info
    const sqlInfo = user.getSQLInfo();

    const profile = {
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        sqlLevel: user.sqlLevel,
        sqlInfo: sqlInfo,
        wallet: user.wallet,
        profile: user.profile,
        dashboardPreferences: user.dashboardPreferences,
        agentStatus: user.agentStatus,
        role: user.role,
        permissions: user.permissions,
        lastLogin: user.lastLogin,
        loginCount: user.loginCount,
        isActive: user.isActive,
        createdAt: user.createdAt
      },
      cards: cardConfig.cards,
      cardPreferences: {
        layout: cardConfig.layout,
        columns: cardConfig.columns,
        autoRefresh: cardConfig.autoRefresh,
        refreshInterval: cardConfig.refreshInterval,
        visibility: cardConfig.visibility,
        dragAndDrop: cardConfig.dragAndDrop,
        theme: cardConfig.theme
      }
    };

    res.json({
      success: true,
      data: profile
    });

  } catch (error) {
    console.error('Error getting user profile:', error);
    res.status(500).json({ 
      error: 'Failed to get user profile',
      message: error.message 
    });
  }
};

// Check user's SQL level
const checkSQLLevel = async (req, res) => {
  try {
    const { id } = req.params;
    
    const user = await User.findById(id).select('sqlLevel sqlExpiryDate');
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const sqlInfo = user.getSQLInfo();

    res.json({
      success: true,
      data: {
        userId: user._id,
        sqlLevel: user.sqlLevel,
        sqlInfo: sqlInfo
      }
    });

  } catch (error) {
    console.error('Error checking SQL level:', error);
    res.status(500).json({ 
      error: 'Failed to check SQL level',
      message: error.message 
    });
  }
};

// Update user profile
const updateUserProfile = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    // Remove sensitive fields from updates
    delete updates.password;
    delete updates.email;
    delete updates.role;
    delete updates.permissions;

    const user = await User.findByIdAndUpdate(
      id,
      { ...updates, updatedAt: new Date() },
      { new: true, runValidators: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      success: true,
      data: user
    });

  } catch (error) {
    console.error('Error updating user profile:', error);
    res.status(500).json({ 
      error: 'Failed to update user profile',
      message: error.message 
    });
  }
};

// Update user's SQL level
const updateSQLLevel = async (req, res) => {
  try {
    const { id } = req.params;
    const { sqlLevel, sqlExpiryDate } = req.body;

    const user = await User.findByIdAndUpdate(
      id,
      { 
        sqlLevel,
        sqlExpiryDate: sqlExpiryDate ? new Date(sqlExpiryDate) : null,
        updatedAt: new Date()
      },
      { new: true, runValidators: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const sqlInfo = user.getSQLInfo();

    res.json({
      success: true,
      data: {
        user: user,
        sqlInfo: sqlInfo
      }
    });

  } catch (error) {
    console.error('Error updating SQL level:', error);
    res.status(500).json({ 
      error: 'Failed to update SQL level',
      message: error.message 
    });
  }
};

// Update user's wallet information
const updateWallet = async (req, res) => {
  try {
    const { id } = req.params;
    const { balance, currency, walletAddress } = req.body;

    const user = await User.findByIdAndUpdate(
      id,
      { 
        'wallet.balance': balance,
        'wallet.currency': currency,
        'wallet.walletAddress': walletAddress,
        updatedAt: new Date()
      },
      { new: true, runValidators: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      success: true,
      data: {
        wallet: user.wallet
      }
    });

  } catch (error) {
    console.error('Error updating wallet:', error);
    res.status(500).json({ 
      error: 'Failed to update wallet',
      message: error.message 
    });
  }
};

// Update user's dashboard preferences
const updateDashboardPreferences = async (req, res) => {
  try {
    const { id } = req.params;
    const preferences = req.body;

    const user = await User.findByIdAndUpdate(
      id,
      { 
        dashboardPreferences: preferences,
        updatedAt: new Date()
      },
      { new: true, runValidators: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      success: true,
      data: {
        dashboardPreferences: user.dashboardPreferences
      }
    });

  } catch (error) {
    console.error('Error updating dashboard preferences:', error);
    res.status(500).json({ 
      error: 'Failed to update dashboard preferences',
      message: error.message 
    });
  }
};

// Update user's agent status
const updateAgentStatus = async (req, res) => {
  try {
    const { id } = req.params;
    const { isOnline, activeAgents } = req.body;

    const user = await User.findByIdAndUpdate(
      id,
      { 
        'agentStatus.isOnline': isOnline,
        'agentStatus.activeAgents': activeAgents,
        'agentStatus.lastSeen': new Date(),
        updatedAt: new Date()
      },
      { new: true, runValidators: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({
      success: true,
      data: {
        agentStatus: user.agentStatus
      }
    });

  } catch (error) {
    console.error('Error updating agent status:', error);
    res.status(500).json({ 
      error: 'Failed to update agent status',
      message: error.message 
    });
  }
};

// Get all users (admin only)
const getAllUsers = async (req, res) => {
  try {
    const users = await User.find({ isActive: true })
      .select('-password')
      .sort({ createdAt: -1 });

    res.json({
      success: true,
      data: users
    });

  } catch (error) {
    console.error('Error getting all users:', error);
    res.status(500).json({ 
      error: 'Failed to get users',
      message: error.message 
    });
  }
};

// Get users by SQL level
const getUsersBySQLLevel = async (req, res) => {
  try {
    const { level } = req.params;
    
    const users = await User.getUsersBySQLLevel(level)
      .select('-password')
      .sort({ createdAt: -1 });

    res.json({
      success: true,
      data: users
    });

  } catch (error) {
    console.error('Error getting users by SQL level:', error);
    res.status(500).json({ 
      error: 'Failed to get users by SQL level',
      message: error.message 
    });
  }
};

// Get online users
const getOnlineUsers = async (req, res) => {
  try {
    const users = await User.getOnlineUsers()
      .select('-password')
      .sort({ 'agentStatus.lastSeen': -1 });

    res.json({
      success: true,
      data: users
    });

  } catch (error) {
    console.error('Error getting online users:', error);
    res.status(500).json({ 
      error: 'Failed to get online users',
      message: error.message 
    });
  }
};

module.exports = {
  getUserProfile,
  checkSQLLevel,
  updateUserProfile,
  updateSQLLevel,
  updateWallet,
  updateDashboardPreferences,
  updateAgentStatus,
  getAllUsers,
  getUsersBySQLLevel,
  getOnlineUsers
}; 