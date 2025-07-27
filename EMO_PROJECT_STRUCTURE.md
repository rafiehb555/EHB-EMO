# EMO (Easy Management Office) - Complete Project Structure

## 📁 **Project Root Structure**

```
EMO/
├── 📁 frontend/                 # Next.js Frontend Application
├── 📁 backend/                  # Node.js/Express Backend API
├── 📁 admin-panel/              # Admin Dashboard Application
├── 📁 database/                 # Database schemas and migrations
├── 📁 blockchain/               # Blockchain integration files
├── 📁 ai-integration/           # AI/ML integration files
├── 📁 docs/                     # Documentation
├── 📁 config/                   # Configuration files
├── 📁 scripts/                  # Build and deployment scripts
├── 📁 tests/                    # Test files
├── 📄 vercel.json              # Vercel deployment config
├── 📄 aws-deployment.yml       # AWS deployment config
├── 📄 EMO_DEVELOPMENT_GUIDE.md # Main development guide
└── 📄 EMO_PROJECT_STRUCTURE.md # This file
```

## 🎯 **Frontend Structure (Next.js)**

```
frontend/
├── 📁 src/
│   ├── 📁 components/           # Reusable React components
│   │   ├── 📁 ui/              # Basic UI components
│   │   ├── 📁 forms/           # Form components
│   │   ├── 📁 dashboard/       # Dashboard components
│   │   ├── 📁 business/        # Business-related components
│   │   ├── 📁 franchise/       # Franchise components
│   │   └── 📁 complaints/      # Complaint components
│   ├── 📁 pages/               # Next.js pages
│   │   ├── 📁 dashboard/       # Dashboard pages
│   │   ├── 📁 business/        # Business pages
│   │   ├── 📁 franchise/       # Franchise pages
│   │   ├── 📁 complaints/      # Complaint pages
│   │   └── 📁 wallet/          # Wallet pages
│   ├── 📁 styles/              # CSS/Tailwind styles
│   ├── 📁 utils/               # Utility functions
│   ├── 📁 hooks/               # Custom React hooks
│   ├── 📁 context/             # React context providers
│   ├── 📁 types/               # TypeScript type definitions
│   └── 📁 assets/              # Static assets (images, icons)
├── 📁 public/                  # Public static files
├── 📄 package.json             # Frontend dependencies
├── 📄 next.config.js          # Next.js configuration
├── 📄 tailwind.config.js      # Tailwind CSS configuration
└── 📄 tsconfig.json           # TypeScript configuration
```

## 🔧 **Backend Structure (Node.js/Express)**

```
backend/
├── 📁 src/
│   ├── 📄 index.js             # Main server file
│   ├── 📁 routes/              # API route handlers
│   │   ├── 📄 auth.js          # Authentication routes
│   │   ├── 📄 users.js         # User management routes
│   │   ├── 📄 businesses.js    # Business routes
│   │   ├── 📄 franchises.js    # Franchise routes
│   │   ├── 📄 complaints.js    # Complaint routes
│   │   ├── 📄 wallet.js        # Wallet routes
│   │   └── 📄 admin.js         # Admin routes
│   ├── 📁 controllers/         # Business logic controllers
│   │   ├── 📄 authController.js
│   │   ├── 📄 userController.js
│   │   ├── 📄 businessController.js
│   │   ├── 📄 franchiseController.js
│   │   ├── 📄 complaintController.js
│   │   └── 📄 walletController.js
│   ├── 📁 models/              # Database models
│   │   ├── 📄 User.js
│   │   ├── 📄 Business.js
│   │   ├── 📄 Franchise.js
│   │   ├── 📄 Complaint.js
│   │   └── 📄 Wallet.js
│   ├── 📁 middleware/          # Express middleware
│   │   ├── 📄 auth.js          # JWT authentication
│   │   ├── 📄 validation.js    # Input validation
│   │   ├── 📄 rateLimit.js     # Rate limiting
│   │   └── 📄 errorHandler.js  # Error handling
│   ├── 📁 services/            # Business services
│   │   ├── 📄 emailService.js  # Email notifications
│   │   ├── 📄 smsService.js    # SMS notifications
│   │   ├── 📄 aiService.js     # AI integration
│   │   └── 📄 blockchainService.js # Blockchain integration
│   └── 📁 utils/               # Utility functions
│       ├── 📄 database.js       # Database connection
│       ├── 📄 jwt.js           # JWT utilities
│       └── 📄 helpers.js       # Helper functions
├── 📁 config/                  # Configuration files
├── 📁 tests/                   # Test files
└── 📄 package.json             # Backend dependencies
```

## 👨‍💼 **Admin Panel Structure**

```
admin-panel/
├── 📁 src/
│   ├── 📁 components/          # Admin components
│   │   ├── 📁 dashboard/       # Dashboard widgets
│   │   ├── 📁 tables/          # Data tables
│   │   ├── 📁 forms/           # Admin forms
│   │   ├── 📁 charts/          # Analytics charts
│   │   └── 📁 modals/          # Modal components
│   ├── 📁 pages/               # Admin pages
│   │   ├── 📁 dashboard/       # Main dashboard
│   │   ├── 📁 users/           # User management
│   │   ├── 📁 businesses/      # Business management
│   │   ├── 📁 franchises/      # Franchise management
│   │   ├── 📁 complaints/      # Complaint management
│   │   ├── 📁 reports/         # Reports and analytics
│   │   └── 📁 settings/        # System settings
│   ├── 📁 styles/              # Admin styles
│   ├── 📁 utils/               # Admin utilities
│   └── 📁 hooks/               # Admin hooks
├── 📄 package.json             # Admin dependencies
└── 📄 next.config.js          # Admin Next.js config
```

## 🗄️ **Database Structure**

```
database/
├── 📄 schema.sql               # Database schema (SQL reference)
├── 📁 migrations/              # Database migrations
├── 📁 seeds/                   # Seed data
└── 📁 models/                  # MongoDB models
    ├── 📄 User.js
    ├── 📄 Business.js
    ├── 📄 Franchise.js
    ├── 📄 Complaint.js
    ├── 📄 Document.js
    ├── 📄 Wallet.js
    └── 📄 Notification.js
```

## ⛓️ **Blockchain Integration**

```
blockchain/
├── 📁 polkadot/               # Polkadot integration
│   ├── 📄 connection.js
│   ├── 📄 sqlMinting.js
│   └── 📄 verification.js
├── 📁 moonbeam/               # Moonbeam integration
│   ├── 📄 wallet.js
│   ├── 📄 transactions.js
│   └── 📄 penalties.js
├── 📁 bsc/                    # BSC integration
│   ├── 📄 nftBadges.js
│   └── 📄 verification.js
└── 📄 index.js                # Main blockchain service
```

## 🤖 **AI Integration**

```
ai-integration/
├── 📁 openai/                 # OpenAI integration
│   ├── 📄 documentValidator.js
│   ├── 📄 sqlEstimator.js
│   ├── 📄 businessClassifier.js
│   └── 📄 complaintAnalyzer.js
├── 📁 custom/                  # Custom AI models
│   ├── 📄 fraudDetector.js
│   └── 📄 recommendationEngine.js
└── 📄 index.js                # Main AI service
```

## 📋 **Key Features by Phase**

### **Phase 1: Profile Manager**
- User registration and role selection
- JPS profile synchronization
- Role-based dashboard cards

### **Phase 2: Verification Center**
- Business registration forms
- Document upload system
- AI-powered document validation
- SQL level estimation

### **Phase 3: Franchise Dashboard**
- Franchise area management
- Team management tools
- Income tracking
- Complaint handling

### **Phase 4: Complaint System**
- Complaint filing interface
- Auto-routing to franchises
- Escalation logic
- Penalty calculation

### **Phase 5: Wallet Integration**
- EHBGC wallet connection
- Transaction management
- Balance tracking
- Blockchain integration

### **Phase 6: SQL Monitoring**
- SQL level tracking
- Expiry notifications
- Upgrade requests
- Blockchain verification

### **Phase 7: Notifications**
- Email notifications
- SMS alerts
- Push notifications
- In-app notifications

### **Phase 8: AI Assistant**
- Chat interface
- Smart suggestions
- Document analysis
- Business insights

### **Phase 9: Admin Panel**
- Global dashboard
- User management
- Business verification
- System settings

## 🚀 **Deployment Configuration**

### **Vercel Deployment**
- `vercel.json` - Vercel configuration
- Environment variables setup
- API route handling

### **AWS Deployment**
- `aws-deployment.yml` - AWS CodeBuild configuration
- S3 bucket setup
- CloudFront distribution

## 🔐 **Security Features**

- JWT authentication
- Role-based access control
- Rate limiting
- Input validation
- File upload security
- Blockchain verification
- GDPR compliance

## 📊 **Monitoring & Analytics**

- User activity tracking
- Performance monitoring
- Error logging
- Blockchain transaction logs
- AI interaction logs
- Complaint resolution metrics

---

*This structure supports all 9 phases of EMO development with scalable architecture for future enhancements.* 