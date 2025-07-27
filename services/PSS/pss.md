# 🛡️ PSS - Personal Security System (2025-2026)

## 🎯 Vision
PSS is responsible for verifying user identities, protecting sensitive data, and ensuring fraud prevention across GoSellr and all EHB platforms. It uses blockchain, AI, and secure storage systems to provide a transparent, immutable, and highly secure service.

---

## 🔧 Technical Stack (Next.js Version)

| Component         | Technology                |
|------------------|---------------------------|
| **Frontend**     | Next.js (App Router) + Tailwind CSS |
| **Backend**      | Node.js (Express.js API routes or Next.js API routes) |
| **Database**     | MongoDB Atlas             |
| **Auth Method**  | JWT (JSON Web Token)      |
| **API Structure**| REST API with OpenAPI spec |
| **File Storage** | Supabase Bucket           |
| **Deployment**   | Vercel                    |
| **Port**         | 3000 (Next.js default)    |
| **Blockchain**   | Polkadot + Moonbeam       |
| **AI/ML**        | TensorFlow, OpenCV, Scikit-learn |

---

## 📋 KYC Document Verification

PSS supports the following document types:

- CNIC (Front and Back)
- Passport
- Driving License
- Utility Bill (for address verification, optional)
- Live Photo / Selfie (real-time webcam or mobile camera capture)

---

## 🔁 Verification Process Flow

1. User registers and logs in.
2. User uploads required KYC documents.
3. Documents are reviewed manually by admin (with optional AI scan in future).
4. Admin can Approve / Reject with notes.
5. System updates SQL Level via SQL API.

---

## 👥 User Roles

- **User** – Uploads personal KYC docs.
- **Admin / Verifier** – Reviews and takes action.
- **System** – Communicates with SQL system and dashboard.

---

## 📊 Admin Panel Features

- Document preview panel
- Filtering by status (Pending, Approved, Rejected)
- Comment/review area
- Re-verification button
- Export logs
- Audit history per user

---

## 🎨 UI/UX Design

| Feature             | Details                |
|---------------------|------------------------|
| Design Style        | Modern, Material-style |
| Mobile Responsive   | Yes                    |
| UI Framework        | Tailwind CSS           |
| Flow                | Sign Up → Upload Docs → Status Await → SQL Update |

---

## 🔐 Security & Data Protection

- All data encrypted (AES-256)
- HTTPS enforced
- Files stored on secure cloud (Supabase Bucket)
- Full audit trail per verification
- GDPR-inspired compliance

---

## 🔌 API Integration with SQL System

- `POST https://api.ehb.com/sql/update-verification-status`

Example:

```json
{
  "userId": "123",
  "pssStatus": "verified",
  "level": "Basic"
}
```

- Updates reflect on user's SQL profile and dashboard

---

## 📈 Business Logic

| Scenario           | Action                 |
|--------------------|------------------------|
| ✅ Valid docs       | SQL → Basic            |
| ❌ Fake or invalid  | SQL → Rejected         |
| ⏳ Incomplete       | Remains at Free level  |
| 📝 Appeal requested | Re-submission allowed  |

---

## 🚀 Development Setup

### Environment Variables (.env.local)

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

MONGODB_URI=your_mongo_uri
JWT_SECRET=your_random_secret_key

# Blockchain
POLKADOT_RPC_URL=your_polkadot_rpc
MOONBEAM_CONTRACT_ADDRESS=your_contract_address

# AI/ML
TENSORFLOW_MODEL_PATH=your_model_path
OPENCV_CONFIG=your_opencv_config

# SMS/Email
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
SENDGRID_API_KEY=your_sendgrid_key
```

### Setup Sources:
- [Supabase Project Settings](https://app.supabase.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- JWT: Generate using `openssl rand -base64 32`

---

## 📁 Folder Structure (Recommended)

```
pss/
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   ├── api/
│   │   ├── auth/
│   │   ├── documents/
│   │   ├── ai/
│   │   ├── blockchain/
│   │   └── sql/
│   └── globals.css
├── components/
│   ├── KYCForm.tsx
│   ├── DocumentUpload.tsx
│   ├── AdminPanel.tsx
│   ├── StatusCard.tsx
│   ├── AIFraudDetection.tsx
│   ├── BlockchainViewer.tsx
│   └── TwoFactorAuth.tsx
├── lib/
│   ├── mongo.ts
│   ├── supabase.ts
│   ├── jwt.ts
│   ├── blockchain.ts
│   ├── ai-models.ts
│   └── encryption.ts
├── utils/
│   ├── validation.ts
│   ├── fileUpload.ts
│   ├── ai-processing.ts
│   └── blockchain-utils.ts
├── types/
│   └── index.ts
├── models/
│   ├── fraud-detection.ts
│   └── document-verification.ts
└── README.md
```

---

## 🧠 Roman Urdu Summary

"PSS aik alag se repo hai jo user ki KYC documents verify karta hai jese CNIC, Passport, ya Selfie. Ye Next.js aur Node.js per develop hoga. Jab user verify hota hai to uska SQL level update hota hai. Admin panel se document manual review kiye jate hain. Ye system dashboard aur SQL ke sath integrate hoga aur securely document handle karega."

---

## 🏗️ 7-Phase Development Plan

### ✅ Phase 1: KYC Verification System (Advanced)
**Status**: In Progress | 🟡 7 Phases Left

| Feature | Stack | Description |
|---------|-------|-------------|
| KYC Document Upload | React, Node.js | Users upload documents (ID, Passport) |
| Self-Photo Upload | React, AWS S3 | Users upload real-time self-photos |
| Blockchain Storage | Polkadot, Moonbeam | Store encrypted KYC documents as NFTs |
| Multi-Factor Authentication | React, Firebase | SMS + Email verification |
| AI Fraud Detection | AI Algorithm | Detect fake documents or anomalies |

### ✅ Phase 2: AI Fraud Detection System
**Status**: ❌ Not Started | 🟡 6 Phases Left

| Feature | Stack | Description |
|---------|-------|-------------|
| AI Pattern Recognition | TensorFlow, Keras | Train models to identify fraudulent behaviours |
| Behavioural Monitoring AI | Scikit-learn, PyTorch | Analyse user behaviour to flag suspicious activity |
| Manual Fraud Review System | React, Node.js | Provide an admin panel for manual review |
| Fraud Alerts | WebSockets, Node.js | Real-time notifications when fraud is detected |
| Machine Learning Model Retraining | AWS SageMaker | Continuously improve AI models using new data |

### ✅ Phase 3: User Authentication & Verification
**Status**: ❌ Not Started | 🟡 5 Phases Left

| Feature | Stack | Description |
|---------|-------|-------------|
| 2FA (Two-Factor Authentication) | Firebase, Twilio | SMS + Authenticator app integration |
| OTP Generation + Verification | Node.js, Redis | Generate and validate one-time passwords |
| Admin Panel for Verification | React, Node.js | Admin access for verifying users manually |
| User Profile Management | MongoDB, Prisma | Admins can edit user data and security status |
| Security Event Logs | Polkadot Blockchain | Immutable logs for all security-related events |

### ✅ Phase 4: AI-Powered Document Verification
**Status**: ❌ Not Started | 🟡 4 Phases Left

| Feature | Stack | Description |
|---------|-------|-------------|
| Document Upload (ID + Passport) | React, AWS S3 | Upload documents for verification |
| AI Document Analysis | OpenCV, TensorFlow | AI that checks the validity of uploaded documents |
| Blockchain-Based Document Proof | Polkadot, Moonbeam | Store verified documents as NFTs on blockchain |
| ZKP Verification | Polkadot, zk-SNARK | Zero-Knowledge Proof for document validation |
| AI Fraud Alerts | Node.js, TensorFlow | Notify admins when suspicious documents are uploaded |

### ✅ Phase 5: Full Admin Panel Integration
**Status**: ❌ Not Started | 🟡 3 Phases Left

| Feature | Stack | Description |
|---------|-------|-------------|
| Admin Dashboard | React, Node.js | View user data, fraud detection logs, verification statuses |
| Fraud Monitoring Logs | MongoDB, Polkadot | View logs of fraud alerts and actions taken |
| Manual Verification Management | React, Node.js | Admin panel to approve/reject users |
| User Account Management | MongoDB | Manage user profile, security settings, and SQL level |
| Transaction History | Polkadot, MongoDB | View all transactions and fraud events |

### ✅ Phase 6: Data Encryption & Secure Storage
**Status**: ❌ Not Started | 🟡 2 Phases Left

| Feature | Stack | Description |
|---------|-------|-------------|
| End-to-End Encryption | AWS KMS, Polkadot | Encrypt user data, documents, and transactions |
| Secure Document Storage | AWS S3 + Polkadot | Store verified documents securely with encryption |
| Data Integrity Check | Polkadot Blockchain | Ensure data integrity with blockchain hashes |

### ✅ Phase 7: AI Model Training & Feedback Loop
**Status**: ❌ Not Started | 🟡 1 Phase Left

| Feature | Stack | Description |
|---------|-------|-------------|
| AI Training | TensorFlow, PyTorch | Train AI to detect fraudulent accounts and fake documents |
| Feedback Loop | AWS SageMaker | Use real-world fraud data to retrain models |
| Real-Time Alerts | Node.js, AWS SNS | Notify admin when AI model detects fraud |

---

## 🔗 Blockchain Integration

### Core Features:
- **KYC Document Storage**: Use Polkadot blockchain to store user KYC records immutably
- **ZKP (Zero-Knowledge Proof)**: Implement ZKP to verify documents without revealing sensitive data
- **NFT-Based Identity**: Use NFTs to issue secure IDs to verified users
- **Immutable Logs**: All verification events stored on blockchain

### Blockchain Record Example:
```json
{
  "userId": "USR-343299",
  "documentType": "CNIC",
  "docHash": "0xabc123...",
  "verifiedTimestamp": "2025-07-16 13:42",
  "chain": "Polkadot parachain",
  "txLink": "https://explorer.polkadot.io/tx/..."
}
```

---

## 🤖 AI Integration

### Core Components:
- **Behavioural Monitoring**: Detect suspicious activity patterns
- **AI Pattern Recognition**: Use ML algorithms to detect fraudulent documents
- **Real-Time Alerts**: Notify admins of suspicious activity
- **Document Analysis**: AI-powered document validation

### AI Tools & Techniques:
- **TensorFlow/Keras**: Train document fraud detection models
- **Scikit-learn**: Behavioural anomaly detection
- **OpenCV**: Image-based ID analysis
- **PyTorch**: Deep model experimentation

---

## 🔐 Security Features

### Multi-Factor Authentication:
- **SMS Verification**: Send OTP to user's phone
- **Authenticator App**: Google Authenticator integration
- **Backup Codes**: Secure recovery option

### Data Protection:
- **AES-256 Encryption**: All data encrypted
- **HTTPS Enforced**: Secure communication
- **Role-Based Access**: Admin/user permissions
- **Audit Trail**: Complete activity logging

---

## 📊 Admin Panel Features

### Dashboard Cards:
- **Total KYC Requests**: Filtered by time period
- **Verified IDs**: With SQL Level distribution
- **Rejected Submissions**: With reasons
- **Blockchain Verified**: Number of verified documents
- **Fraud Reports**: Suspected fake profiles
- **Fines Collected**: Total from violations

### Roles & Access Levels:
- **Super Admin**: Full access to all tools
- **Corporate Franchise**: National-level data access
- **Master Franchise**: District/City-level access
- **Sub Franchise**: Area-level approvals only
- **Support Officer**: View logs only

---

## 💰 Fine Management Rules

### Fine Structure:
- **Sub-franchise**: 2% of linked orders for fake ID approval
- **Master franchise**: 3% for violations
- **Corporate**: 5% for gross negligence
- **Users**: Fines for forged ID submissions

### Payment Method:
- **EHBGC Tokens**: All fines payable in EHBGC
- **Trusty Wallet**: Integration with wallet system

---

## 🔄 Development Status

**Ready for Development**: All technical requirements and setup information is complete.

**Next Steps**: 
1. Create Next.js project with complete setup
2. Implement Phase 1: KYC Verification System
3. Setup MongoDB Atlas and Supabase
4. Implement JWT authentication
5. Build document upload system
6. Create admin panel
7. Integrate with SQL system API
8. Add blockchain integration
9. Implement AI fraud detection
10. Add 2FA system
11. Complete all 7 phases

---

## 🎯 Final Goal

PSS will be a complete, AI-powered, blockchain-backed personal security system that:
- ✅ Verifies user identities securely
- ✅ Prevents fraud using AI
- ✅ Stores data immutably on blockchain
- ✅ Provides comprehensive admin controls
- ✅ Integrates with EHB ecosystem
- ✅ Scales with franchise system