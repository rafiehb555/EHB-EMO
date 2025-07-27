# EMO (Easy Management Office) - Complete Development Guide
*This file contains all EMO project information for Cursor agent to use during development*

## 🎯 **PROJECT OVERVIEW**

### **What is EMO?**
- **Full Name:** Easy Management Office
- **Core Purpose:** Main control hub for all services, dashboards, user profiles, business verification, complaint handling, and franchise management under EHB Technologies
- **Phase:** Phase 1 of EHB Technologies
- **Port:** 4003

### **EMO Connections**
- **Connected to:** EHB SQL System, Franchise System, PSS, EDR, JPS, GoSellr, Wallet
- **Integration:** Updates SQL levels (Normal/High), Business verification for EHB ecosystem
- **Role:** Smart digital office management system

---

## 🛠️ **COMPLETE TECHNOLOGY STACK**

| Layer              | Technology                               | Notes                                       |
| ------------------ | ---------------------------------------- | ------------------------------------------- |
| **Frontend**       | `Next.js` + `React`                      | Fast, SEO optimized, server/client render   |
| **Styling**        | `Tailwind CSS`                           | Responsive, utility-first design            |
| **Backend**        | `Node.js` + `Express`                    | Lightweight backend to handle APIs          |
| **Database**       | `MongoDB Atlas`                          | Cloud DB with strong document modeling      |
| **Authentication** | `JWT` + optional `2FA`                   | Secure access with role-based auth          |
| **Storage**        | `Supabase Buckets` or `AWS S3`           | For file uploads (KYC, licenses, etc.)      |
| **Deployment**     | `Vercel` (Frontend) + `Render` (Backend) | Optional switch to AWS for scaling          |
| **Blockchain**     | `Polkadot`, `Moonbeam`, `BSC`            | For token handling, staking, verification   |
| **AI Integration** | OpenAI API / Custom AI                   | To handle user profiling, auto-verification |
| **Dev Agent**      | Cursor (Agent-based dev)                 | For AI-assisted local repo automation       |

---

## 📦 **TOTAL PHASES: 9 PHASES**

### **Phase 1: EMO Profile Manager** ✅ READY
**Function:** Create user business profiles
**UI:** Dynamic registration cards
**Tech:** React + Tailwind, POST API to `api/emo/profile`
**Features:**
- JPS user profile sync
- Role-based access (Franchise, School, Seller, Service Provider, Agent)
- Dashboard view customise karna har role k liye
- GET /user/profile
- POST /emo/role-selection
- Role-based dashboard card loading

### **Phase 2: Verification Center** ✅ READY
**Function:** Business, product, and service verification via PSS + EDR
**AI:** Detect document authenticity
**Tech:** MongoDB schema for `verificationRequests`, Admin Panel approval system
**Features:**
- Business/service registration form
- SQL Level Selector (Free/Basic/Normal/High/VIP)
- Document upload system
- AI SQL Estimator
- Blockchain: Polkadot – service hash + metadata log

### **Phase 3: Franchise Dashboard Integration** ✅ READY
**Function:** Display Sub, Master, and Corporate franchise dashboards
**Tech:** Conditional rendering via `role`, Backend API fetches franchise data
**Panels:**
- **Seller:** Product listing, stock, orders, delivery
- **Service Provider:** Bookings, time slots, location, reviews
- **School/Teacher:** Class mgmt, student assignments, HPS link
- **Franchise:** Team mgmt, income, complaint centre, logs

### **Phase 4: Complaint Management System** ✅ READY
**Function:** Auto-complaint routing to franchises (Sub → Master → Corporate)
**Backend:** Node.js APIs with complaint `status`, `priority`, `franchiseAssigned`
**Timer Logic:** 6-hour countdown triggers escalation
**Penalty Calculation:** 2–5% of order value, depending on tier
**Features:**
- PSS (Docs) integration
- EDR (Skill test) integration
- Admin panel approval
- MongoDB collections: services, verification_logs, sql_tiers
- Status: Unverified, In Progress, Verified, Expired

### **Phase 5: EMO Wallet Integration** ✅ READY
**Function:** Connects with EHBGC wallet
**Tech:** Moonbeam testnet → Trusty Wallet → Auto deduction on franchise/user actions
**Features:**
- Order volume (Past 7/30/90 days)
- Income summary (By SQL type, referral)
- Complaint ratio (Based on resolution time)
- Traffic (Region-wise engagement)
- AI suggestions for time slots and promotions

### **Phase 6: SQL Level Monitor** ✅ READY
**Function:** Track user SQL status (Free → Basic → Normal → High → VIP)
**Display:** Each user dashboard shows badge + expiry
**Backend:** MongoDB field `sqlLevel`, `validUntil`, `status`
**Features:**
- Franchise area map (GPS-based)
- Seller/Service approval (✅/❌)
- Complaint resolutions (Timer-based)
- Team mgmt (Add/Edit staff)
- Income cut system (Automated)

### **Phase 7: Notification & Auto Emailer** ✅ READY
**Function:** Notify users on complaint status, SQL expiry, profile approval
**Tech:** Email + SMS APIs (via SendGrid / Twilio)
**Blockchain Used:**
- ✅ Polkadot – metadata audit trails
- ✅ Binance Smart Chain – payment logs
- 🔜 Mosaic Blockchain – service tokens, franchise coins

### **Phase 8: AI-Powered User Guidance** ✅ READY
**Function:** Onboarding walkthrough + Smart service suggestions
**Tech:** OpenAI GPT API, Chat-style UI, history-based prompts
**AI Functions:**
- Suggest the best SQL based on the market
- Auto-fill service forms
- Detect invalid uploads
- Franchise coaching & hints
- "Why is my income low?" analysis

### **Phase 9: Admin Panel (Global View)** ✅ READY
**Function:** Company-level admin controls for all services
**Modules:**
- Franchise status + income
- Verification queue
- Complaints report
- SQL downgrade tracker
- EMO staff manager
**Tech:** Next.js + Tailwind Admin Layout, protected by JWT + Role-check
**Deployment Includes:**
- Frontend: Next.js + Tailwind
- Backend: Node.js, Express
- DB: MongoDB
- Blockchain: Polkadot + BSC
- Agent: AI SDK (OpenAI or Claude)
- Hosting: Vercel / Render / AWS S3 (files)

---

## 📡 **EMO Inter-Service Integration:**

| Service             | Integration Use                                 |
| ------------------- | ----------------------------------------------- |
| **PSS**             | For initial user KYC                            |
| **EDR**             | For practical skill test-based SQL upgrades     |
| **Franchise Model** | Complaint routing + commission handling         |
| **SQL System**      | Real-time user level and expiration tracking    |
| **GoSellr**         | Verifies business accounts for shop creation    |
| **JPS**             | Links user profiles to jobs & reputation system |

---

## 🔗 **Blockchain Usage (EMO-Specific)**

| Use Case                        | Blockchain               |
| ------------------------------- | ------------------------ |
| Wallet integration for SQL fees | Moonbeam                 |
| Complaint penalty deduction     | Moonbeam                 |
| Franchise lock-in & ROI         | Polkadot                 |
| SQL Badge Verification          | BSC (optional NFT badge) |

---

## 🛡️ **Security & Compliance:**

- ✅ JWT Auth for all protected API routes
- ✅ Encrypted file uploads via Supabase
- ✅ GDPR-aligned document retention
- ✅ Franchise fine and refund enforcement via smart logic

---

## 📋 **CORE FEATURES TO DEVELOP**

### **1. User Interface**
- [ ] Business registration form
- [ ] Document upload system
- [ ] Verification status dashboard
- [ ] User profile management
- [ ] Mobile responsive design
- [ ] Role-based dashboard cards
- [ ] SQL level management
- [ ] Complaint filing system

### **2. Admin Panel**
- [ ] Admin dashboard
- [ ] Verification management tools
- [ ] User management
- [ ] Reports and analytics
- [ ] Document review system
- [ ] Franchise performance monitoring
- [ ] Complaint escalation control
- [ ] Global settings management

### **3. Business Verification Process**
- [ ] Document collection
- [ ] Verification workflow
- [ ] Status tracking
- [ ] Notification system
- [ ] SQL level integration
- [ ] AI-powered document validation
- [ ] Live selfie/video verification

### **4. API Endpoints**
- [ ] User registration
- [ ] Document upload
- [ ] Verification status
- [ ] Admin operations
- [ ] EHB SQL integration
- [ ] Franchise management
- [ ] Complaint handling
- [ ] Wallet integration

---

## 🧠 **AI INTEGRATION**

### **AI Features**
- [ ] Document validator (detect fake/unclear images)
- [ ] SQL estimator (based on completeness + quality)
- [ ] Auto-fill service forms
- [ ] Business category detector
- [ ] Complaint categorizer
- [ ] Revenue forecast AI
- [ ] Franchise coaching bot
- [ ] Global AI admin

---

## ❌ **MISSING INFORMATION**

### **UI/UX Design Preferences**
- [ ] Design style (modern, corporate, simple)
- [ ] Color scheme preferences
- [ ] Logo and branding requirements
- [ ] Mobile app needed or web-only?

### **Business Rules**
- [ ] Verification fees structure
- [ ] SQL level pricing details
- [ ] Complaint resolution timeframes
- [ ] Penalty calculation rules
- [ ] Franchise commission structure

### **Regional Requirements**
- [ ] Multi-language support needed?
- [ ] Country-specific compliance rules
- [ ] Tax calculation requirements
- [ ] Data sovereignty requirements

### **Deployment Requirements**
- [ ] Hosting platform preferences
- [ ] Domain requirements
- [ ] SSL certificates needed?
- [ ] Environment setup (dev/staging/prod)

---

## 📝 **QUESTIONS FOR CLIENT**

1. **Design:** What should the UI look like? (modern, corporate, simple)
2. **Business Rules:** What are the verification fees and SQL pricing?
3. **Regional:** Multi-language support needed? Which countries?
4. **Deployment:** Where should the application be hosted?
5. **Mobile:** Mobile app needed or web-only?

---

## 🚀 **DEVELOPMENT PHASES**

### **Phase 1: Core Setup**
- [ ] Next.js project setup
- [ ] MongoDB Atlas configuration
- [ ] Basic routing
- [ ] JWT authentication system
- [ ] JPS profile sync

### **Phase 2: User Interface**
- [ ] Business registration forms
- [ ] Document upload
- [ ] User dashboard
- [ ] Mobile responsiveness
- [ ] Role-based dashboards

### **Phase 3: Admin Panel**
- [ ] Admin dashboard
- [ ] Verification tools
- [ ] User management
- [ ] Reporting system
- [ ] Franchise controls

### **Phase 4: Integration**
- [ ] EHB SQL system integration
- [ ] Franchise system connection
- [ ] Blockchain integration
- [ ] AI assistant integration
- [ ] Testing and deployment

---

*Last Updated: [Current Date]*
*Status: Ready for development - Awaiting final client requirements*

**Reply with "start EMO phase 1" to begin development!** 