# PSS - Personal Security System Development Guide

## 🚀 Quick Start

### Prerequisites
- Node.js v18+ 
- npm v8+
- Python 3.8+
- MongoDB (local or cloud)
- Supabase account

### Installation

1. **Clone and Setup**
```bash
cd pss
npm install
cd backend
npm install
```

2. **Environment Configuration**
```bash
cp env.example .env
# Edit .env with your credentials
```

3. **Start Development Servers**
```bash
# Terminal 1 - Frontend
cd pss
npm run dev

# Terminal 2 - Backend  
cd pss/backend
npm run dev
```

4. **Access Applications**
- Frontend: http://localhost:5002
- Backend API: http://localhost:6000

## 📁 Project Structure

```
PSS/
├── pss/                          # Main Next.js application
│   ├── app/                      # Next.js app router
│   │   ├── api/                  # API routes
│   │   ├── auth/                 # Authentication pages
│   │   ├── dashboard/            # Dashboard pages
│   │   └── admin/               # Admin pages
│   ├── components/               # React components
│   │   ├── ui/                  # UI components
│   │   ├── auth/                # Auth components
│   │   ├── dashboard/           # Dashboard components
│   │   ├── admin/               # Admin components
│   │   └── kyc/                # KYC components
│   ├── backend/                 # Express.js backend
│   │   ├── src/
│   │   │   ├── controllers/     # API controllers
│   │   │   ├── routes/          # API routes
│   │   │   └── config/          # Configuration
│   │   └── package.json
│   ├── models/                  # Data models
│   ├── types/                   # TypeScript types
│   ├── utils/                   # Utility functions
│   └── config/                  # Configuration files
├── auto_cursor_script.py        # Auto setup script
└── setup_report.json           # Setup status report
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pss

# JWT
JWT_SECRET=your_jwt_secret_here

# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Blockchain
POLKADOT_RPC_URL=wss://rpc.polkadot.io
MOONBEAM_CONTRACT_ADDRESS=your_contract_address

# AI/ML
TENSORFLOW_MODEL_PATH=your_model_path
OPENCV_CONFIG=your_opencv_config

# SMS/Email
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
SENDGRID_API_KEY=your_sendgrid_key

# App Configuration
NEXTAUTH_URL=http://localhost:5002
NEXTAUTH_SECRET=your_nextauth_secret
```

## 🛠️ Development Commands

### Frontend (Next.js)
```bash
cd pss
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Backend (Express.js)
```bash
cd pss/backend
npm run dev          # Start development server
npm run start        # Start production server
npm run test         # Run tests
npm run lint         # Run ESLint
```

### Auto Setup Script
```bash
python auto_cursor_script.py
```

## 🔐 Security Features

### Authentication
- JWT-based authentication
- Role-based access control
- Multi-factor authentication support
- Session management

### Data Protection
- File upload security
- Input validation
- Rate limiting
- CORS configuration
- Helmet security headers

### Healthcare Compliance
- HIPAA-ready architecture
- Data encryption
- Audit logging
- Access control

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### KYC (Know Your Customer)
- `POST /api/documents/upload` - Upload documents
- `GET /api/documents/user` - Get user documents
- `POST /api/kyc/verify` - Verify documents

### Admin
- `GET /api/admin/stats` - Get system statistics
- `GET /api/admin/users` - Get all users
- `POST /api/admin/approve` - Approve KYC

### Blockchain
- `POST /api/blockchain/store` - Store data on blockchain
- `GET /api/blockchain/verify` - Verify blockchain data

### AI/ML
- `POST /api/ai/analyze` - Analyze documents
- `POST /api/ai/fraud` - Fraud detection

## 🧪 Testing

### Frontend Tests
```bash
cd pss
npm test
```

### Backend Tests
```bash
cd pss/backend
npm test
```

### API Testing
```bash
# Using curl
curl -X POST http://localhost:6000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 🚀 Deployment

### Frontend Deployment
```bash
cd pss
npm run build
npm run start
```

### Backend Deployment
```bash
cd pss/backend
npm run build
npm run start
```

### Environment Variables for Production
- Set `NODE_ENV=production`
- Configure production database URLs
- Set up SSL certificates
- Configure CDN for static assets

## 📊 Monitoring

### Health Checks
- Frontend: http://localhost:5002/api/health
- Backend: http://localhost:6000/api/health

### Logging
- Winston logging configuration
- Daily log rotation
- Error tracking

### Performance
- Response time monitoring
- Memory usage tracking
- Database query optimization

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find process using port
netstat -ano | findstr :5002
# Kill process
taskkill /PID <process_id>
```

2. **MongoDB Connection Error**
- Check MongoDB URI in .env
- Ensure MongoDB is running
- Verify network connectivity

3. **Dependencies Issues**
```bash
# Clear npm cache
npm cache clean --force
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

4. **Build Errors**
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Express.js Documentation](https://expressjs.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Polkadot Documentation](https://wiki.polkadot.network/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Technical Issues**: Create GitHub issue
- **Security Issues**: Contact security@ehb.com
- **Emergency**: Contact emergency-tech@ehb.com

---

**PSS - Personal Security System**  
*Healthcare-focused security and KYC platform* 