# EMO Healthcare Platform Documentation

## Overview

EMO (Electronic Medical Operations) is a comprehensive healthcare platform designed to streamline medical operations, enhance patient care, and ensure compliance with healthcare regulations. This platform integrates AI-powered diagnostics, blockchain-secured health records, and modern web technologies to provide a complete healthcare management solution.

## 🏥 Platform Architecture

### Core Services

1. **Frontend Application** (Port: 6000)
   - React.js with TypeScript
   - Material-UI components
   - Patient portal interface
   - Responsive design for mobile devices

2. **Backend API** (Port: 3000)
   - Node.js with Express
   - RESTful API endpoints
   - JWT authentication
   - Database integration

3. **AI Integration** (Port: 5001)
   - Symptom analysis
   - Diagnosis prediction
   - Treatment recommendations
   - Healthcare chatbot

4. **Blockchain Integration** (Port: 5002)
   - Secure health records
   - Patient consent management
   - Audit trail
   - HIPAA compliance

5. **Admin Panel** (Port: 6001)
   - Healthcare provider dashboard
   - Patient management
   - Analytics and reporting
   - System administration

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ or 20+
- PostgreSQL 14+
- Redis (optional, for caching)
- Docker (optional, for containerization)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ehb/emo-healthcare.git
   cd emo-healthcare
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install
   
   # Install service dependencies
   cd frontend && npm install
   cd ../backend && npm install
   cd ../admin-panel && npm install
   cd ../ai-integration && npm install
   cd ../blockchain && npm install
   ```

3. **Environment setup**
   ```bash
   # Copy environment template
   cp config/environment.js.example config/environment.js
   
   # Edit environment variables
   nano config/environment.js
   ```

4. **Database setup**
   ```bash
   # Run database migrations
   npm run db:migrate
   
   # Seed initial data
   npm run db:seed
   ```

5. **Start development servers**
   ```bash
   # Start all services
   npm run dev
   
   # Or start individually
   npm run dev:frontend
   npm run dev:backend
   npm run dev:ai
   npm run dev:blockchain
   npm run dev:admin
   ```

## 📚 Documentation Sections

### [API Documentation](./api/)
- REST API endpoints
- Authentication methods
- Request/response examples
- Error handling

### [Database Schema](./database/)
- Entity relationship diagrams
- Table structures
- Indexes and constraints
- Migration scripts

### [Security Guide](./security/)
- HIPAA compliance
- Data encryption
- Access controls
- Audit logging

### [Deployment Guide](./deployment/)
- Production setup
- Docker configuration
- Cloud deployment
- Monitoring and logging

### [User Manuals](./user-manuals/)
- Patient portal guide
- Provider dashboard guide
- Admin panel guide
- Mobile app guide

### [Development Guide](./development/)
- Code standards
- Testing procedures
- Contribution guidelines
- Troubleshooting

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emo
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/emo_test

# Authentication
JWT_SECRET=your-jwt-secret-key
JWT_EXPIRES_IN=24h

# Encryption
ENCRYPTION_KEY=your-encryption-key

# AI Services
OPENAI_API_KEY=your-openai-api-key
AI_MODEL_PATH=/path/to/ai/models

# Blockchain
BLOCKCHAIN_NETWORK=ethereum
BLOCKCHAIN_PRIVATE_KEY=your-private-key

# Email/SMS
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# File Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=emo-healthcare-files
```

### Port Configuration

| Service | Default Port | Environment Variable |
|---------|-------------|-------------------|
| Frontend | 6000 | FRONTEND_PORT |
| Backend | 3000 | BACKEND_PORT |
| AI Integration | 5001 | AI_PORT |
| Blockchain | 5002 | BLOCKCHAIN_PORT |
| Admin Panel | 6001 | ADMIN_PORT |

## 🧪 Testing

### Run Tests
```bash
# All tests
npm test

# Unit tests only
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

### Test Coverage Requirements
- Unit tests: 80% minimum
- Integration tests: 70% minimum
- E2E tests: Critical user flows

## 🔒 Security Features

### HIPAA Compliance
- Data encryption at rest and in transit
- Access control and authentication
- Audit logging and monitoring
- Patient consent management
- Data backup and recovery

### Security Measures
- JWT token authentication
- Role-based access control (RBAC)
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

## 📊 Monitoring

### Health Checks
```bash
# Manual health check
npm run health:check

# Continuous monitoring
npm run health:check --continuous --interval 30
```

### Performance Monitoring
- Response time tracking
- Error rate monitoring
- Database performance
- Memory usage
- CPU utilization

## 🚀 Deployment

### Development
```bash
npm run deploy:dev
```

### Staging
```bash
npm run deploy:staging
```

### Production
```bash
npm run deploy:prod
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Standards
- Follow ESLint configuration
- Use Prettier for formatting
- Write meaningful commit messages
- Include JSDoc comments
- Follow TypeScript best practices

## 📞 Support

### Emergency Contacts
- **Security Incidents**: security@ehb.com
- **Data Breaches**: privacy@ehb.com
- **System Outages**: emergency-tech@ehb.com
- **Patient Safety**: safety@ehb.com

### Documentation Issues
- Create an issue in the repository
- Contact: docs@ehb.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🏥 Healthcare Compliance

EMO is designed to meet healthcare industry standards:

- **HIPAA Compliance**: Full compliance with Health Insurance Portability and Accountability Act
- **HITECH**: Health Information Technology for Economic and Clinical Health Act compliance
- **GDPR**: General Data Protection Regulation compliance
- **SOC 2**: Service Organization Control 2 certification ready

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Maintainer**: EHB Healthcare Team 