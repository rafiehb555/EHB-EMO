const { Sequelize } = require('sequelize');
const bcrypt = require('bcryptjs');

// Create database connection
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './database.sqlite',
  logging: console.log
});

// Define User model
const User = sequelize.define('User', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  email: {
    type: Sequelize.STRING(255),
    allowNull: false,
    unique: true
  },
  password: {
    type: Sequelize.STRING(255),
    allowNull: false
  },
  firstName: {
    type: Sequelize.STRING(100),
    allowNull: false
  },
  lastName: {
    type: Sequelize.STRING(100),
    allowNull: false
  },
  userType: {
    type: Sequelize.ENUM('jobseeker', 'company', 'admin'),
    defaultValue: 'jobseeker'
  }
}, {
  tableName: 'users',
  timestamps: true
});

async function testDatabase() {
  try {
    console.log('🔄 Testing database setup...');

    // Test connection
    await sequelize.authenticate();
    console.log('✅ Database connection established.');

    // Sync models
    await sequelize.sync({ force: true });
    console.log('✅ Tables created successfully.');

    // Create test user
    const hashedPassword = await bcrypt.hash('test123', 10);
    const user = await User.create({
      email: 'test@example.com',
      password: hashedPassword,
      firstName: 'Test',
      lastName: 'User',
      userType: 'admin'
    });
    console.log('✅ Test user created:', user.toJSON());

    // Query user
    const foundUser = await User.findOne({ where: { email: 'test@example.com' } });
    console.log('✅ User found:', foundUser.toJSON());

    console.log('🎉 Database test completed successfully!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Database test failed:', error);
    process.exit(1);
  }
}

testDatabase();
