# EMO (Easy Management Office) - Business Management System

## 🎯 **Project Overview**

**EMO** (Easy Management Office) is a comprehensive business management system designed for EHB Technologies. It serves as the main control hub for business verification, franchise management, complaint handling, and user profile management.

### **Core Purpose:**
- Business and franchise verification
- User profile management with role-based access
- Complaint management system
- Franchise dashboard integration
- SQL level monitoring and upgrades
- Wallet integration with EHBGC

## 🏗️ **System Architecture**

### **Technology Stack:**
- **Frontend:** Next.js + React + Tailwind CSS
- **Backend:** Node.js + Express
- **Database:** MongoDB Atlas
- **Authentication:** JWT + 2FA
- **Blockchain:** Polkadot, Moonbeam, BSC
- **AI Integration:** OpenAI API
- **Deployment:** Vercel (Frontend) + Render (Backend)

### **Port Configuration:**
- **EMO Main:** Port 4003
- **Frontend:** Port 6000
- **Backend API:** Port 3000
- **Admin Panel:** Port 6001

## 📦 **System Modules**

### **Phase 1: Profile Manager** ✅
- User business profile creation
- Role-based access (Franchise, School, Seller, Service Provider, Agent)
- Dynamic dashboard customization
- JPS user profile sync

### **Phase 2: Verification Center** ✅
- Business and service verification
- Document upload and AI verification
- SQL Level Selector (Free/Basic/Normal/High/VIP)
- Blockchain integration for verification logs

### **Phase 3: Franchise Dashboard** ✅
- Sub, Master, and Corporate franchise dashboards
- Role-specific panels (Seller, Service Provider, School)
- Team management and income tracking

### **Phase 4: Complaint Management** ✅
- Auto-complaint routing system
- 6-hour escalation timer
- Penalty calculation (2-5% of order value)
- PSS and EDR integration

### **Phase 5: Wallet Integration** ✅
- EHBGC wallet connection
- Order volume tracking
- Income summary and analytics
- AI-powered suggestions

### **Phase 6: SQL Level Monitor** ✅
- SQL status tracking (Free → Basic → Normal → High → VIP)
- Level upgrade management
- Expiry monitoring

## 🚀 **Quick Start**

### **Prerequisites:**
```bash
Node.js 18+ or 20+
MongoDB Atlas account
Vercel account (for frontend)
Render account (for backend)
```

### **Installation:**
```bash
# Clone repository
git clone https://github.com/ehb/emo-business.git
cd emo-business

# Install dependencies
npm install

# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Start development
npm run dev
```

### **Environment Variables:**
```bash
# Database
MONGODB_URI=your-mongodb-atlas-uri

# Authentication
JWT_SECRET=your-jwt-secret
JWT_EXPIRES_IN=24h

# Blockchain
POLKADOT_RPC_URL=your-polkadot-rpc
MOONBEAM_RPC_URL=your-moonbeam-rpc

# AI Services
OPENAI_API_KEY=your-openai-key

# File Storage
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

## 📊 **User Roles & Access**

### **Business Roles:**
1. **Franchise Owner** - Complete business management
2. **Seller** - Product listing and order management
3. **Service Provider** - Service booking and time management
4. **School/Teacher** - Class and student management
5. **Agent** - Sales and commission tracking

### **Admin Roles:**
1. **Super Admin** - Full system access
2. **Verification Admin** - Document verification
3. **Complaint Admin** - Complaint management
4. **Franchise Admin** - Franchise oversight

## 🔧 **API Endpoints**

### **Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/verify-2fa` - 2FA verification

### **Profile Management:**
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `POST /api/emo/role-selection` - Role selection

### **Business Verification:**
- `POST /api/verification/submit` - Submit verification
- `GET /api/verification/status` - Check status
- `POST /api/verification/approve` - Admin approval

### **Complaint Management:**
- `POST /api/complaints/create` - Create complaint
- `GET /api/complaints/list` - List complaints
- `PUT /api/complaints/resolve` - Resolve complaint

### **Franchise Management:**
- `GET /api/franchise/dashboard` - Franchise dashboard
- `POST /api/franchise/team/add` - Add team member
- `GET /api/franchise/income` - Income reports

## 🏥 **Business Features**

### **Verification System:**
- Document upload and validation
- AI-powered authenticity detection
- Blockchain verification logging
- Multi-level approval process

### **Complaint Handling:**
- Automatic routing to appropriate franchise
- Escalation timer (6 hours)
- Penalty calculation system
- Resolution tracking

### **SQL Level Management:**
- Level upgrade tracking
- Expiry monitoring
- Benefits management
- Payment integration

### **Analytics Dashboard:**
- Order volume tracking
- Income analysis
- Complaint ratio monitoring
- Regional traffic analysis

## 🔒 **Security Features**

### **Data Protection:**
- JWT token authentication
- Role-based access control (RBAC)
- Data encryption at rest and in transit
- Audit logging for all actions

### **Business Security:**
- Document verification system
- Fraud detection algorithms
- Secure payment processing
- Compliance monitoring

## 📈 **Monitoring & Analytics**

### **Performance Metrics:**
- User engagement tracking
- Business verification success rate
- Complaint resolution time
- Revenue generation analysis

### **System Health:**
- Real-time service monitoring
- Error tracking and alerting
- Performance optimization
- Backup and recovery

## 🚀 **Deployment**

### **Development:**
```bash
npm run dev
```

### **Production:**
```bash
npm run build
npm start
```

### **Docker Deployment:**
```bash
docker-compose up -d
```

## 📞 **Support**

### **Technical Support:**
- **Email:** tech-support@ehb.com
- **Documentation:** https://docs.emo-business.com
- **Status Page:** https://status.emo-business.com

### **Business Support:**
- **Verification Issues:** verification@ehb.com
- **Complaint Escalation:** complaints@ehb.com
- **Franchise Support:** franchise@ehb.com

## 📄 **License**

This project is proprietary software owned by EHB Technologies.

---

**Version:** 1.0.0  
**Last Updated:** January 2024  
**Maintainer:** EHB Technologies Team 