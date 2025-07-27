
# EHB Franchise Model

The EHB Franchise Model is a decentralized and scalable ecosystem designed to verify, deliver, and manage services and product quality worldwide. It is structured in a hierarchical format with revenue sharing, territory management, complaint resolution, and SQL level integration.

---

## 🏢 Franchise Types

### 1. **Sub-Franchise**
- **Scope**: Operates at tehsil or small city level.
- **Duties**:
  - Local delivery verification
  - Product/service complaint resolution within 6 hours
  - Registers local service providers and shopkeepers
  - Initial KYC and SQL service management
- **Frontend Role**:
  - Access local dashboard
  - Manage user submissions
- **Backend**:
  - Routes service data to Master Franchise
  - APIs for submission, verification, and complaint tracking

---

### 2. **Master Franchise**
- **Scope**: Operates at district level (manages 10–25 Sub-Franchises)
- **Duties**:
  - Handle escalated complaints (6 hours deadline)
  - Validate Sub-Franchise performance
  - Reports to Corporate Franchise
- **Frontend Role**:
  - Franchise tracking UI
  - SQL fine reporting
- **Backend**:
  - Aggregated data sync from sub-franchise
  - Escalation APIs

---

### 3. **Corporate Franchise**
- **Scope**: Country-level franchise
- **Duties**:
  - National reporting and territory enforcement
  - Manages SQL policy application
  - Approves/Revokes master franchises
- **Frontend Role**:
  - Advanced audit dashboard
  - Global user performance metrics
- **Backend**:
  - Blockchain-based earning tracker
  - Integration with Validator Node (future)

---

## 🌐 Franchise Dashboard

Each franchise level has a unique dashboard based on assigned role:
- **Sub**: Local complaints, earnings, user approvals
- **Master**: Escalation, report generation, training stats
- **Corporate**: Validator options, country data sync, policy control

---

## 🧾 Franchise Home Page Components

- Hero Section (Franchise Earning Opportunities)
- Benefits Grid (Income, Territory, SQL Upgrades)
- Registration Form (Linked to EMO + PSS)
- FAQ and SQL Impact Explanation

---

## 🎛️ Admin Panel Structure

- Franchise Manager Role Setup
- Assign Port Access
- Ban or Suspend Franchise
- View Escalation Chain with Timestamps

---

## ⚙️ APIs and Endpoints

- `POST /api/franchise/register`
- `GET /api/franchise/profile/:id`
- `PUT /api/franchise/verify-sub`
- `POST /api/franchise/report`
- `PATCH /api/franchise/escalate/:ticket_id`
- `GET /api/franchise/income/:franchise_id`

---

## 💡 UI/UX Features

- Role-based dashboards (React + Tailwind)
- Franchise map with performance heatmap
- Complaint timer visualizer (for 6-hour deadline)
- SQL Impact Rating with Level Breakdown
- Admin flagging and warning banners

---

## 🔗 SQL Integration Points

- SQL downgrade on delayed complaint
- SQL upgrade after consistent positive performance
- Penalty System via Wallet + Blockchain
- Physical Verification: Tracked via EDR Department

---

## 🔐 Blockchain Integration

- Penalty and reward system (coin locked in Trusty Wallet)
- Validator path (only High/VIP SQL Master Franchises eligible)
- Each franchise's performance stored in Mosaic Blockchain

---

## 📈 Benefits

- Transparent governance
- Reward-based performance
- Locally scalable with global accountability

---
