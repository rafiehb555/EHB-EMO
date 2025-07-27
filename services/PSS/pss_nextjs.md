
# 🛡️ PSS - Personal Security System

PSS (Personal Security System) is a core verification service for the EHB ecosystem. It handles KYC (Know Your Customer) and document verification to help upgrade user SQL levels and secure the platform from fraud.

---

## 🔧 Technical Stack (Next.js Version)

| Component         | Technology                |
|------------------|---------------------------|
| **Frontend**     | Next.js (App Router) + Tailwind CSS |
| **Backend**      | Node.js (Express.js API routes or Next.js API routes) |
| **Database**     | MongoDB                   |
| **Auth Method**  | JWT (JSON Web Token)      |
| **API Structure**| REST API with OpenAPI spec |

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
- Files stored on secure cloud (e.g., Supabase Bucket or S3)
- Full audit trail per verification
- GDPR-inspired compliance

---

## 🔌 API Integration with SQL System

- `POST /api/sql/update`

Example:

```json
{
  "userId": "xyz123",
  "newLevel": "Basic",
  "source": "PSS"
}
```

- Updates reflect on user’s SQL profile and dashboard

---

## 📈 Business Logic

| Scenario           | Action                 |
|--------------------|------------------------|
| ✅ Valid docs       | SQL → Basic            |
| ❌ Fake or invalid  | SQL → Rejected         |
| ⏳ Incomplete       | Remains at Free level  |
| 📝 Appeal requested | Re-submission allowed  |

---

## 🧠 Roman Urdu Summary

"PSS aik alag se repo hai jo user ki KYC documents verify karta hai jese CNIC, Passport, ya Selfie. Ye Next.js aur Node.js per develop hoga. Jab user verify hota hai to uska SQL level update hota hai. Admin panel se document manual review kiye jate hain. Ye system dashboard aur SQL ke sath integrate hoga aur securely document handle karega."

---

## 📁 Folder Structure (Recommended)

```
pss/
├── app/
│   └── (Next.js pages and components)
├── api/
│   └── verify/
│       └── route.ts (Next.js API Route)
├── components/
│   └── KYCForm.tsx
├── lib/
│   └── mongo.ts
├── utils/
│   └── jwt.ts
└── README.md
```
