# 🎯 EDR (Exam Decision Registration) - Complete Specifications

## 📋 Company Context
- **Company**: EHB Technologies
- **Business Type**: Multi-service platform ecosystem
- **Target Industry**: Service providers (mechanics, teachers, doctors, riders, etc.)
- **Business Model**: Skill verification and service quality management platform

---

## 🏗️ EDR System Overview

### 🎯 Mission
EDR har user (mechanic, teacher, doctor, rider, etc.) ka skill test, exam verification, aur levelling system manage karta hai taake unki Service Quality Level (SQL) clear aur transparent ho — AI + blockchain use karke tamper-proof, real-time verified skill ecosystem banaya jaye.

### 📊 System Statistics
- **Total Phases**: 7
- **Completed**: 0
- **Remaining**: 7
- **Technology Stack**: Next.js + AI + Blockchain (Polkadot + Moonbeam)

---

## 🔰 Phase 1: Skill Registration System

### 🎯 Phase 1 Goal
Har service provider apni skill choose kare, verify karwaye, aur exam registration kar sake.

### ✳️ Key Features
- Skill List Browser (By Department)
- EDR Form (Auto-Connected to PSS Profile)
- SQL Target Level Selector (Free → VIP)
- Exam Fee Payment (Trusty Wallet)
- Centre Location Selection (If Physical Test Required)

### 🔐 Blockchain Integration
- Store skill registration on Polkadot
- Use Moonbeam to log payment and SQL tier requests

### 🤖 AI Features
- Auto-match the user's profession with possible skills
- Detect duplicate/misleading skill submissions

### 🔧 Frontend Components

- `/edr/register-skill`
- `/components/SkillSelector.tsx`
- `/components/ExamBookingCard.tsx`

### 🧩 Backend APIs

- `/api/edr/submitSkill`
- `/api/edr/getExamSlots`
- `/api/wallet/payExamFee`

---

## 🔰 Phase 2: Exam Scheduling + AI Exam Generator

### 🎯 Phase 2 Goal
Skill-wise test schedule + auto-generated MCQs, coding, or scenario-based exams

### ✳️ Key Features
- Auto exam generator by AI
- Slot booking for virtual/physical exams
- Real-time countdown, mock tests
- SQL upgrade locked until pass

### 🔐 Blockchain Integration
- Immutable timestamp for scheduled exam on Polkadot
- Moonbeam smart contract holds a pass/fail score + fees

### 🤖 AI Features
- Generate exams by skill tag
- Create adaptive difficulty questions
- Auto-evaluate MCQ and structured answers

### 🔧 Frontend Components

- `/edr/exam-centre`
- `/components/ExamSlotCalendar.tsx`
- `/components/ExamPreview.tsx`

### 🧩 Backend APIs

- `/api/edr/generateExam`
- `/api/edr/bookSlot`
- `/api/edr/submitAnswer`

---

## 🔰 Phase 3: Result, Rank, SQL Level Update

### 🎯 Phase 3 Goal
Result declare karna, rank assign karna, aur auto SQL level update karna

### ✳️ Key Features
- Scorecard UI
- Blockchain rank hash generation
- Automatic level downgrade if failed
- Leaderboard for public review (optional)

### 🔐 Blockchain Integration
- Rank hash + SQL level on-chain (Polkadot)
- Immutable badge with timestamp

### 🤖 AI Features
- Score normalization
- Detect cheating patterns
- Suggest a retry duration

### 🔧 Frontend Components

- `/edr/result`
- `/components/SQLRankMeter.tsx`
- `/components/BadgeNFT.tsx`

### 🧩 Backend APIs

- `/api/edr/getResult`
- `/api/sql/updateLevel`
- `/api/blockchain/mintRankHash`

---

## 🔰 Phase 4: EDR Badge NFT + Onchain Identity

### 🎯 Phase 4 Goal
Her successful candidate verified NFT badge issue karna (on-chain)

### ✳️ Key Features
- Unique badge for each SQL
- EHBGC locking is required for badge minting
- Display on JPS profile, GoSellr, EMO, etc.

### 🔐 Blockchain Integration
- NFT Minting on Moonbeam
- Metadata (rank, skill, expiry, verification level)

### 🤖 AI Features
- Skill-based badge visualisation generator

### 🔧 Frontend Components
- `/edr/badge-minting`
- `/components/BadgePreview.tsx`

### 🧩 Backend APIs
- `/api/nft/mint`
- `/api/sql/fetchUserNFTs`

---

## 🔰 Phase 5: Re-Test Flow + Penalties

### 🎯 Phase 5 Goal
Fail hone wale users ke liye retest system + automatic fine

### ✳️ Key Features
- Retest request panel
- Auto fine from wallet (based on SQL tier)
- Retake limitation (e.g. after 15 days)

### 🔐 Blockchain Integration
- Retest record on Polkadot
- Auto-fine on Moonbeam

### 🤖 AI Features
- Personalised suggestions for weak areas

### 🔧 Frontend Components
- `/edr/retest-request`
- `/components/FailureReasonAI.tsx`

### 🧩 Backend APIs
- `/api/edr/retest`
- `/api/finance/deductPenalty`

---

## 🔰 Phase 6: Institute Panel for Physical Exams

### 🎯 Phase 6 Goal
Colleges/institutes register karein for conduct physical exams

### ✳️ Key Features
- Location-based exam centre dashboard
- Staff panel with score upload
- Student verification (via PSS)

### 🔐 Blockchain Integration
- Centre registration on Polkadot
- Exam data hash on Moonbeam

### 🔧 Frontend Components
- `/edr/institute-panel`
- `/components/CenterSlotManager.tsx`

### 🧩 Backend APIs
- `/api/edr/registerInstitute`
- `/api/edr/uploadExamResult`

---

## 🔰 Phase 7: Admin Panel + Analytics

### 🎯 Phase 7 Goal
Admin ko full control dena for SQL monitoring, EDR exams, and feedback

### ✳️ Key Features
- Dashboard: Passed/failed stats
- Retest frequency monitor
- Badge mint volume
- Region-wise skill graph

### 🔧 Admin Panel Routes
- `/admin/edr/dashboard`
- `/admin/edr/sqlControl`
- `/admin/edr/examMonitoring`

---

## 📊 SQL Level System

### 🎯 SQL Levels
- **Free**: Basic access
- **Basic**: After PSS verification
- **Normal**: After basic skill test
- **High**: After advanced skill test
- **VIP**: Premium level with special privileges

### 🔗 Integration Points
- **JPS**: User profile management
- **GoSellr**: E-commerce platform
- **EMO**: Business verification
- **Trusty Wallet**: Payment system
- **SQL Engine**: Central level management

---

## 🛠️ Technical Stack

### Frontend
- **Framework**: Next.js
- **UI Components**: React components
- **Styling**: CSS/SCSS
- **State Management**: React hooks/Context

### Backend
- **Runtime**: Node.js
- **Framework**: Next.js API routes
- **Database**: MongoDB/PostgreSQL
- **ORM**: Prisma

### Blockchain
- **Polkadot**: Immutable records
- **Moonbeam**: Smart contracts
- **EHBGC**: Native token

### AI Integration
- **Test Generation**: AI-powered exam creation
- **Proctoring**: AI-based cheating detection
- **Scoring**: Automated result evaluation
- **Recommendations**: Personalized suggestions

---

## 📁 Project Structure

```
/app
  /edr
    register-skill.tsx
    exam-centre.tsx
    result.tsx
    badge-minting.tsx
    retest-request.tsx
    institute-panel.tsx
    components/
      SkillSelector.tsx
      SQLLevelBar.tsx
      ExamSlotCalendar.tsx
      ResultCard.tsx
      BadgePreview.tsx
      WalletPaymentModal.tsx

/pages/api
  /edr
    submitSkill.ts
    generateExam.ts
    getResult.ts
    retest.ts
    registerInstitute.ts
    analytics.ts

/prisma
  schema.prisma
  migrations/

/blockchain
  contracts/
  scripts/
```

---

## 🚀 Development Status

### ✅ Ready for Development
- Complete specifications available
- All phases defined
- Technical stack confirmed
- Integration points mapped

### 📋 Next Steps
1. **Database Schema Design**
2. **API Endpoints Development**
3. **Frontend Components Creation**
4. **Blockchain Integration**
5. **AI Model Integration**
6. **Testing & Deployment**

---

## 💡 Development Commands

```bash
# Start EDR Frontend Development
npm run dev

# Start EDR Backend Development
npm run build && npm start

# Generate Database Schema
npx prisma generate

# Deploy Smart Contracts
npm run deploy:contracts
```

---

**Status**: ✅ Complete specifications ready for development
**Next Action**: Awaiting development start command 