# EHB Company Information Index

## Quick Reference for Cursor Agent

This index provides quick access to all EHB company information that should be
referenced during development.

## 📋 Company Overview

- **[Company Profile](company-profile.md)** - Complete company information,
mission, vision, and core values

- **[Brand Guidelines](brand-guidelines.md)** - Colors, typography, design
standards, and brand identity

- **[Team Structure](team-structure.md)** - Organizational structure, roles, and
collaboration guidelines

- **[Contact Information](contact-info.md)** - All contact details and
communication guidelines

## 🛠️ Development Resources

- **[Development Standards](../development-guidelines/standards.md)** - Coding
standards, security guidelines, and best practices

- **[Project Requirements](../project-docs/requirements.md)** - Common
healthcare project requirements and technical specifications

## 🏥 Healthcare Focus Areas

### Core Business Areas

- **Healthcare Management Systems** - Patient management, appointment scheduling

- **Electronic Health Records (EHR)** - Medical data management and
interoperability

- **Telemedicine Platforms** - Video conferencing and remote care

- **Healthcare Analytics** - Data analysis and predictive insights

- **Medical Device Integration** - IoT and device connectivity

### Technology Stack

- **Frontend:** React.js, Angular, Vue.js

- **Backend:** Node.js, Python, Java

- **Database:** PostgreSQL, MongoDB, MySQL

- **Cloud:** AWS, Azure, Google Cloud

- **Mobile:** React Native, Flutter

- **AI/ML:** TensorFlow, PyTorch, Scikit-learn

## 🔒 Compliance & Security

### HIPAA Compliance

- **Data Protection:** Encryption at rest and in transit

- **Access Controls:** Role-based access control (RBAC)

- **Audit Logging:** Complete audit trails

- **Data Retention:** Proper retention policies

### Security Standards

- **Authentication:** Multi-factor authentication

- **Authorization:** Strict access controls

- **Data Masking:** PII protection

- **Incident Response:** Security breach procedures

## 🎨 Design Standards

### Brand Colors

- **Primary Blue:** #2563EB

- **Healthcare Green:** #10B981

- **Professional Gray:** #6B7280

- **Success Green:** #22C55E

- **Error Red:** #EF4444

### Typography

- **Font Family:** Inter, system fonts

- **Heading Weight:** 600-700

- **Body Weight:** 400-500

### UI Guidelines

- **Buttons:** 8px border-radius

- **Cards:** Subtle shadows, white background

- **Forms:** Clear labels, helpful error messages

- **Accessibility:** WCAG 2.1 AA compliance

## 📊 Development Guidelines

### Code Quality

- **Readability:** Self-documenting code

- **Maintainability:** Easy to modify and extend

- **Performance:** Optimized for healthcare applications

- **Testing:** 80% code coverage minimum

### File Structure

```text

src/
├── components/          # Reusable UI components

├── pages/              # Page components

├── services/           # Business logic and API calls

├── utils/              # Helper functions

├── types/              # TypeScript type definitions

├── hooks/              # Custom React hooks

├── constants/          # Application constants

└── assets/             # Images, icons, etc.

```text

## 🚀 Performance Standards

### Frontend Performance

- **Load Time:** < 3 seconds for initial page load

- **Bundle Size:** < 500KB for main bundle

- **Image Optimization:** WebP format, lazy loading

### Backend Performance

- **Response Time:** < 200ms for API responses

- **Database Queries:** Optimized with proper indexing

- **Caching:** Redis for frequently accessed data

## 🧪 Testing Requirements

### Testing Standards

- **Unit Tests:** Jest for JavaScript, pytest for Python

- **Integration Tests:** API endpoint testing

- **End-to-End Tests:** Critical user flows

- **Healthcare-Specific:** Medical data validation testing

## 📱 User Experience

### Healthcare-Focused Design

- **Clean Interface:** Professional, trustworthy appearance

- **High Contrast:** Accessibility standards

- **Clear Hierarchy:** Information organization

- **Error Prevention:** Clear validation and error messages

### Mobile Responsive

- **Cross-Platform:** Works on all devices

- **Touch-Friendly:** Appropriate touch targets

- **Offline Capability:** Core functionality offline

## 🔗 Integration Requirements

### Healthcare Standards

- **HL7 FHIR:** Healthcare data interoperability

- **ICD-10:** International classification of diseases

- **CPT Codes:** Current procedural terminology

- **LOINC:** Logical observation identifiers

### Third-Party Integrations

- **Payment Gateways:** Stripe, PayPal

- **Email Services:** SendGrid, AWS SES

- **SMS Services:** Twilio, AWS SNS

- **File Storage:** AWS S3, Google Cloud Storage

## 📞 Support & Communication

### Response Times

- **Urgent Issues:** < 1 hour

- **High Priority:** < 4 hours

- **Normal Priority:** < 24 hours

- **Low Priority:** < 48 hours

### Communication Channels

- **Internal:** Slack, email, phone

- **Client:** Email, phone, client portal

- **Emergency:** Dedicated emergency contacts

## 🎯 Development Priorities

### Always Consider

1. **HIPAA Compliance** - All patient data must be protected

2. **User Safety** - Healthcare applications impact patient care

3. **Performance** - Fast, reliable systems for healthcare professionals

4. **Accessibility** - Accessible to all users including those with disabilities

5. **Scalability** - Systems must handle healthcare organization growth

### Quality Assurance

- **Code Review:** All code must be reviewed

- **Testing:** Comprehensive testing before deployment

- **Documentation:** Clear documentation for all features

- **Security Audit:** Regular security assessments

---

**Note for Cursor Agent:** Always reference this information when developing for
EHB. The healthcare industry has strict requirements for security, compliance,
and user experience. Every development decision should align with EHB's
standards and healthcare industry best practices.