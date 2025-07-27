# EMO (Easy Management Office) - Business Verification & Management Platform

[![EMO Logo](https://img.shields.io/badge/EMO-Easy%20Management%20Office-blue)](https://emo.com)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green)](https://nodejs.org)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black)](https://nextjs.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-blue)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Overview

EMO (Easy Management Office) is a comprehensive business verification and management platform designed for EHB Technologies. It provides complete solutions for business verification, SQL level management, franchise operations, and complaint handling.

## ✨ Features

### 🔐 **Authentication & User Management**
- Secure JWT-based authentication
- Role-based access control (User, Business, Franchise, Admin, Super Admin)
- Two-factor authentication support
- Password reset functionality
- Account lockout protection

### 🏢 **Business Verification System**
- Complete business registration and verification
- Document upload and AI-powered validation
- SQL level management (Free → Basic → Normal → High → VIP)
- Real-time verification status tracking
- Blockchain-based verification records

### 🏪 **Franchise Management**
- Multi-level franchise system (Sub → Master → Corporate)
- Franchise area management with GPS coordinates
- Team management and staff controls
- Income tracking and commission handling
- Performance analytics and reporting

### 📋 **Complaint Management**
- Automated complaint routing system
- 6-hour escalation timer
- Penalty calculation (2-5% of order value)
- Complaint resolution tracking
- Integration with PSS and EDR systems

### 💰 **Wallet Integration**
- EHBGC token integration via Moonbeam
- Automated payment processing
- Transaction history and reporting
- Balance tracking and notifications

### 🤖 **AI-Powered Features**
- Document authenticity detection
- SQL level recommendations
- Business category classification
- Smart service suggestions
- Revenue forecasting

### 📊 **Analytics & Reporting**
- Real-time dashboard metrics
- Performance analytics
- SQL level monitoring
- Franchise performance tracking
- Custom report generation

## 🏗️ Architecture

### **Frontend Stack**
- **Framework:** Next.js 14 with React 18
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **HTTP Client:** Axios
- **UI Components:** Lucide React Icons
- **Animations:** Framer Motion

### **Backend Stack**
- **Runtime:** Node.js 18+
- **Framework:** Express.js
- **Database:** MongoDB Atlas
- **Authentication:** JWT
- **Validation:** Express Validator
- **File Upload:** Multer
- **Logging:** Winston
- **Email:** Nodemailer
- **SMS:** Twilio

### **Blockchain Integration**
- **Polkadot:** Metadata audit trails
- **Moonbeam:** Payment processing
- **BSC:** NFT badges and verification

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- MongoDB (local or Atlas)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ehb-technologies/emo.git
cd emo
```

2. **Install dependencies**
```bash
# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install

# Install admin panel dependencies
cd ../admin-panel
npm install
```

3. **Environment Setup**
```bash
# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp admin-panel/.env.example admin-panel/.env
```

4. **Configure Environment Variables**

**Backend (.env)**
```env
NODE_ENV=development
PORT=4003
MONGODB_URI=mongodb://localhost:27017/emo_dev
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRE=7d
FRONTEND_URL=http://localhost:3000
ADMIN_URL=http://localhost:6001
```

**Frontend (.env)**
```env
NEXT_PUBLIC_API_URL=http://localhost:4003
NEXT_PUBLIC_APP_NAME=EMO - Easy Management Office
```

5. **Start Development Servers**
```bash
# Start backend (Terminal 1)
cd backend
npm run dev

# Start frontend (Terminal 2)
cd frontend
npm run dev

# Start admin panel (Terminal 3)
cd admin-panel
npm run dev
```

6. **Access the Application**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:4003
- **Admin Panel:** http://localhost:6001

## 📁 Project Structure

```
EMO/
├── 📁 frontend/                 # Next.js Frontend Application
│   ├── 📁 src/
│   │   ├── 📁 components/       # React components
│   │   ├── 📁 pages/           # Next.js pages
│   │   ├── 📁 context/         # React contexts
│   │   ├── 📁 hooks/           # Custom hooks
│   │   ├── 📁 utils/           # Utility functions
│   │   └── 📁 styles/          # CSS styles
│   └── 📄 package.json
├── 📁 backend/                  # Node.js/Express Backend
│   ├── 📁 src/
│   │   ├── 📁 routes/          # API routes
│   │   ├── 📁 controllers/     # Business logic
│   │   ├── 📁 models/          # Database models
│   │   ├── 📁 middleware/      # Express middleware
│   │   └── 📁 utils/           # Utility functions
│   └── 📄 package.json
├── 📁 admin-panel/              # Admin Dashboard
├── 📁 database/                 # Database schemas
├── 📁 blockchain/               # Blockchain integration
├── 📁 ai-integration/           # AI/ML services
└── 📄 README.md
```

## 🔧 Development

### **Available Scripts**

**Backend**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run test         # Run tests
npm run lint         # Lint code
```

**Frontend**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Lint code
npm run type-check   # TypeScript check
```

### **Database Setup**
```bash
# Create database
mongo
use emo_dev

# Run migrations (if any)
npm run migrate
```

### **Testing**
```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- --grep "User"
```

## 🛡️ Security Features

- **JWT Authentication** with secure token management
- **Rate Limiting** to prevent abuse
- **Input Validation** with express-validator
- **Password Hashing** with bcrypt
- **CORS Protection** for cross-origin requests
- **Helmet.js** for security headers
- **Account Lockout** after failed login attempts
- **File Upload Security** with type and size validation

## 📊 API Documentation

### **Authentication Endpoints**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### **Business Endpoints**
- `GET /api/businesses` - Get all businesses
- `POST /api/businesses` - Create business
- `GET /api/businesses/:id` - Get business by ID
- `PUT /api/businesses/:id` - Update business
- `DELETE /api/businesses/:id` - Delete business
- `POST /api/businesses/:id/documents` - Upload document

### **User Endpoints**
- `GET /api/users` - Get all users (Admin)
- `GET /api/users/:id` - Get user by ID
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

## 🚀 Deployment

### **Production Deployment**

1. **Environment Setup**
```bash
# Set production environment
NODE_ENV=production
```

2. **Build Applications**
```bash
# Build frontend
cd frontend
npm run build

# Build backend
cd ../backend
npm run build
```

3. **Deploy to Platform**

**Vercel (Frontend)**
```bash
vercel --prod
```

**Render (Backend)**
```bash
# Connect to Render dashboard
# Deploy from GitHub repository
```

**AWS (Alternative)**
```bash
# Use AWS CodeBuild and CodeDeploy
# Or deploy manually to EC2
```

### **Environment Variables for Production**

```env
NODE_ENV=production
PORT=4003
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/emo_prod
JWT_SECRET=your-super-secure-production-jwt-secret
JWT_EXPIRE=7d
FRONTEND_URL=https://emo.com
ADMIN_URL=https://admin.emo.com
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
OPENAI_API_KEY=your-openai-api-key
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```
3. **Commit your changes**
```bash
git commit -m 'Add amazing feature'
```
4. **Push to the branch**
```bash
git push origin feature/amazing-feature
```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [docs.emo.com](https://docs.emo.com)
- **Issues:** [GitHub Issues](https://github.com/ehb-technologies/emo/issues)
- **Email:** support@emo.com
- **Discord:** [EMO Community](https://discord.gg/emo)

## 🙏 Acknowledgments

- **EHB Technologies** - For the vision and support
- **Next.js Team** - For the amazing React framework
- **Express.js Team** - For the robust backend framework
- **MongoDB Team** - For the flexible database solution
- **Tailwind CSS** - For the utility-first CSS framework

---

**Made with ❤️ by EHB Technologies**

*EMO - Easy Management Office - Transforming Business Management*
