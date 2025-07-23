# EHB-JPS Backend API

A comprehensive Job Portal System backend built with Node.js, Express, and PostgreSQL.

## 🚀 Features

- **User Authentication & Authorization** - JWT-based authentication with role-based access
- **Job Management** - CRUD operations for job postings with advanced search
- **Company Management** - Company profiles and verification system
- **Application System** - Job applications with status tracking
- **Admin Dashboard** - Complete admin panel with analytics
- **File Upload** - Resume and company logo upload support
- **Email Notifications** - Automated email system
- **Rate Limiting** - API protection against abuse
- **Security** - Helmet, CORS, input validation

## 📋 Prerequisites

- Node.js (v16 or higher)
- PostgreSQL (v12 or higher)
- npm or yarn

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   cd services/EHB-JPS/backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Setup**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb ehb_jps_db

   # Or using psql
   psql -U postgres
   CREATE DATABASE ehb_jps_db;
   ```

5. **Start the server**
   ```bash
   # Development
   npm run dev

   # Production
   npm start
   ```

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```env
# Server
PORT=3001
NODE_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ehb_jps_db
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=7d

# Frontend
FRONTEND_URL=http://localhost:3000
```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "jobseeker"
}
```

#### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### Job Endpoints

#### Get All Jobs
```http
GET /api/jobs?page=1&limit=10&keyword=developer&location=remote
```

#### Get Job by ID
```http
GET /api/jobs/:id
```

#### Create Job (Company only)
```http
POST /api/jobs
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Developer",
  "description": "We are looking for...",
  "company_id": 1,
  "salary_min": 80000,
  "salary_max": 120000,
  "location": "Remote",
  "job_type": "full-time",
  "skills": ["JavaScript", "React", "Node.js"]
}
```

### User Endpoints

#### Get User Profile
```http
GET /api/users/profile
Authorization: Bearer <token>
```

#### Update Profile
```http
PUT /api/users/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

#### Apply for Job
```http
POST /api/users/applications
Authorization: Bearer <token>
Content-Type: application/json

{
  "job_id": 1,
  "cover_letter": "I am interested in...",
  "salary_expectation": 90000
}
```

### Company Endpoints

#### Get All Companies
```http
GET /api/companies?page=1&limit=10&industry=technology
```

#### Create Company Profile
```http
POST /api/companies
Authorization: Bearer <token>
Content-Type: application/json

{
  "company_name": "Tech Corp",
  "industry": "Technology",
  "description": "Leading tech company...",
  "location": "San Francisco"
}
```

### Admin Endpoints

#### Get Dashboard Stats
```http
GET /api/admin/dashboard
Authorization: Bearer <admin_token>
```

#### Get All Users
```http
GET /api/admin/users?page=1&limit=10&user_type=jobseeker
Authorization: Bearer <admin_token>
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### User Types

- `jobseeker` - Can apply for jobs, manage profile
- `company` - Can post jobs, manage applications
- `admin` - Full system access

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  user_type ENUM('jobseeker', 'company', 'admin') DEFAULT 'jobseeker',
  is_verified BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Jobs Table
```sql
CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  salary_min INTEGER,
  salary_max INTEGER,
  location VARCHAR(255),
  job_type ENUM('full-time', 'part-time', 'contract', 'internship'),
  status ENUM('active', 'inactive', 'filled', 'expired') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch
```

## 📝 Scripts

```bash
# Development
npm run dev

# Production
npm start

# Linting
npm run lint

# Format code
npm run format
```

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - bcrypt with 12 rounds
- **Input Validation** - express-validator for all inputs
- **Rate Limiting** - Protection against abuse
- **CORS** - Cross-origin resource sharing
- **Helmet** - Security headers
- **SQL Injection Protection** - Sequelize ORM

## 📈 Performance

- **Database Indexing** - Optimized queries
- **Connection Pooling** - Efficient database connections
- **Response Compression** - Reduced bandwidth usage
- **Caching** - Redis integration (optional)

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3001
CMD ["npm", "start"]
```

### Environment Variables for Production

```env
NODE_ENV=production
DB_HOST=your-production-db-host
JWT_SECRET=your-production-secret
FRONTEND_URL=https://your-frontend-domain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For support, email support@ehb-jps.com or create an issue in the repository.

---

**EHB-JPS Backend** - Built with ❤️ by EHB-5 Team
