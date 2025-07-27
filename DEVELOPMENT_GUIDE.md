# EMO Development Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm 8+
- MongoDB (local or Atlas)
- Git

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/ehb-technologies/emo.git
cd emo

# Run automated setup
npm run setup

# Or manually install dependencies
npm run install:all
```

### Start Development Servers
```bash
# Start all services
npm run dev

# Or start individually
npm run dev:backend    # Backend API (Port 4003)
npm run dev:frontend   # Frontend (Port 3000)
npm run dev:admin      # Admin Panel (Port 6001)
```

## 📁 Project Structure

```
EMO/
├── backend/                 # Node.js/Express API
│   ├── src/
│   │   ├── controllers/    # Route controllers
│   │   ├── middleware/     # Custom middleware
│   │   ├── models/         # MongoDB schemas
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   └── index.js        # Server entry point
│   ├── uploads/            # File uploads
│   ├── logs/               # Application logs
│   └── package.json
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── context/        # React context
│   │   ├── hooks/          # Custom hooks
│   │   ├── pages/          # Next.js pages
│   │   ├── styles/         # CSS styles
│   │   └── utils/          # Utilities
│   └── package.json
├── admin-panel/            # Admin Dashboard
│   ├── src/
│   │   ├── components/     # Admin components
│   │   ├── pages/          # Admin pages
│   │   └── utils/          # Admin utilities
│   └── package.json
├── scripts/                # Development scripts
│   ├── setup-dev.js        # Setup script
│   ├── start-dev.js        # Start all services
│   ├── health-check.js     # Health monitoring
│   └── auto-cursor-script.py # Python automation
└── package.json            # Root package.json
```

## 🔧 Development Commands

### Root Level Commands
```bash
npm run setup              # Run complete setup
npm run dev                # Start all development servers
npm run health             # Run health check
npm run install:all        # Install all dependencies
npm run build              # Build all projects
npm run test               # Run all tests
npm run lint               # Lint all code
npm run clean              # Clean build artifacts
npm run reset              # Reset and reinstall everything
```

### Backend Commands
```bash
cd backend
npm run dev                # Start development server
npm run start              # Start production server
npm run build              # Build for production
npm run test               # Run tests
npm run lint               # Lint code
npm run migrate            # Run database migrations
npm run seed               # Seed database
```

### Frontend Commands
```bash
cd frontend
npm run dev                # Start development server
npm run build              # Build for production
npm run start              # Start production server
npm run test               # Run tests
npm run lint               # Lint code
```

### Admin Panel Commands
```bash
cd admin-panel
npm run dev                # Start development server
npm run build              # Build for production
npm run start              # Start production server
npm run test               # Run tests
npm run lint               # Lint code
```

## 🌐 Service URLs

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| Frontend | http://localhost:3000 | 3000 | Main application |
| Backend API | http://localhost:4003 | 4003 | REST API |
| Admin Panel | http://localhost:6001 | 6001 | Admin dashboard |
| Health Check | http://localhost:4003/health | 4003 | API health endpoint |

## 🔐 Environment Configuration

### Backend (.env)
```env
NODE_ENV=development
PORT=4003
MONGODB_URI=mongodb://localhost:27017/emo_dev
JWT_SECRET=your-super-secret-jwt-key
FRONTEND_URL=http://localhost:3000
ADMIN_URL=http://localhost:6001
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:4003
NEXT_PUBLIC_APP_NAME=EMO - Easy Management Office
NEXT_PUBLIC_ENVIRONMENT=development
```

### Admin Panel (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:4003
NEXT_PUBLIC_ADMIN_URL=http://localhost:6001
NEXT_PUBLIC_APP_NAME=EMO Admin Panel
```

## 🗄️ Database Setup

### MongoDB Local
```bash
# Install MongoDB
# Windows: Download from mongodb.com
# macOS: brew install mongodb-community
# Linux: sudo apt install mongodb

# Start MongoDB service
mongod

# Create database
mongo
use emo_dev
```

### MongoDB Atlas
1. Create account at mongodb.com
2. Create new cluster
3. Get connection string
4. Update MONGODB_URI in backend/.env

## 🧪 Testing

### Backend Tests
```bash
cd backend
npm run test               # Run all tests
npm run test:watch         # Watch mode
npm run test:coverage      # Coverage report
```

### Frontend Tests
```bash
cd frontend
npm run test               # Run all tests
npm run test:watch         # Watch mode
```

## 🔍 Debugging

### Backend Debugging
```bash
cd backend
npm run dev                # Development with nodemon
# Check logs in backend/logs/
```

### Frontend Debugging
```bash
cd frontend
npm run dev                # Development with hot reload
# Check browser console
```

### Health Monitoring
```bash
npm run health             # Comprehensive health check
node scripts/health-check.js
```

## 🚀 Deployment

### Development
```bash
npm run dev                # Start all services
```

### Production Build
```bash
npm run build              # Build all projects
npm run start              # Start production servers
```

### Docker Deployment
```bash
npm run docker:build       # Build Docker images
npm run docker:up          # Start containers
npm run docker:down        # Stop containers
npm run docker:logs        # View logs
```

## 📊 Monitoring & Logs

### Application Logs
- Backend: `backend/logs/`
- Frontend: Browser console
- Admin Panel: Browser console

### Health Monitoring
- API Health: http://localhost:4003/health
- Frontend: http://localhost:3000
- Admin Panel: http://localhost:6001

### Performance Monitoring
- Backend: Winston logs
- Frontend: React DevTools
- Database: MongoDB Compass

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :3000
# Kill the process
taskkill /PID <PID> /F
```

#### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongod --version
# Start MongoDB service
net start MongoDB
```

#### Node Modules Issues
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and reinstall
npm run clean
npm run install:all
```

#### Environment Variables
```bash
# Check if .env files exist
ls -la backend/.env
ls -la frontend/.env.local
ls -la admin-panel/.env.local
```

### Health Check Failures
```bash
# Run health check
npm run health

# Common fixes:
# 1. Install missing dependencies
npm run install:all

# 2. Start MongoDB
mongod

# 3. Check ports
netstat -ano | findstr :3000
netstat -ano | findstr :4003
netstat -ano | findstr :6001
```

## 📚 API Documentation

### Authentication
```bash
POST /api/auth/register    # Register user
POST /api/auth/login       # Login user
GET  /api/auth/me          # Get current user
POST /api/auth/logout      # Logout user
```

### Business Management
```bash
GET    /api/businesses     # Get all businesses
POST   /api/businesses     # Create business
GET    /api/businesses/:id # Get business
PUT    /api/businesses/:id # Update business
DELETE /api/businesses/:id # Delete business
```

### User Management
```bash
GET    /api/users          # Get all users
GET    /api/users/:id      # Get user
PUT    /api/users/:id      # Update user
DELETE /api/users/:id      # Delete user
```

## 🤝 Contributing

### Code Style
- Backend: ESLint + Prettier
- Frontend: ESLint + Prettier
- Admin Panel: ESLint + Prettier

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
# Test changes
npm run test
npm run lint

# Commit changes
git add .
git commit -m "feat: add your feature"

# Push changes
git push origin feature/your-feature
```

### Pre-commit Hooks
- Lint code
- Run tests
- Check formatting

## 📞 Support

### Development Team
- Email: dev@ehb.com
- Slack: #emo-dev
- GitHub: Issues

### Emergency Contacts
- Security: security@ehb.com
- Database: db-admin@ehb.com
- Infrastructure: infra@ehb.com

## 📖 Additional Resources

- [EHB Technologies](https://ehb.com)
- [EMO Documentation](https://docs.emo.ehb.com)
- [API Reference](https://api.emo.ehb.com)
- [Development Blog](https://dev.emo.ehb.com)

---

**EMO - Easy Management Office**
*Complete business verification and management platform*
