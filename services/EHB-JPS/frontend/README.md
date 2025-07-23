# 🚀 EHB-JPS Frontend

A modern, responsive Job Portal System frontend built with React, TypeScript, and Tailwind CSS.

## 🎯 Features

### **Core Features**
- **Modern UI/UX** - Clean, responsive design with dark/light mode
- **Job Search & Browse** - Advanced job search with filters and pagination
- **Company Profiles** - Company listings and detailed profiles
- **User Authentication** - Secure login/register with JWT
- **User Dashboard** - Personalized dashboard for job seekers
- **Company Dashboard** - Job posting and application management
- **Admin Panel** - Complete admin interface with analytics
- **Real-time Updates** - Live notifications and status updates

### **Technical Features**
- **React 18** - Latest React with hooks and concurrent features
- **TypeScript** - Full type safety and better development experience
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Zustand** - Lightweight state management
- **React Hook Form** - Form handling with validation
- **Lucide React** - Beautiful icons
- **Framer Motion** - Smooth animations

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running (see backend README)

## 🛠️ Installation

1. **Navigate to frontend directory**
   ```bash
   cd services/EHB-JPS/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the frontend directory:

```env
# API Configuration
VITE_API_URL=http://localhost:3001/api

# App Configuration
VITE_APP_NAME=EHB-JPS
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_SENTRY=false
```

### **Vite Configuration**
The project uses Vite with the following features:
- **Path Aliases** - Easy imports with `@/` prefix
- **Proxy Configuration** - API requests proxied to backend
- **Code Splitting** - Automatic chunk splitting
- **Hot Module Replacement** - Fast development

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/            # Basic UI components
│   ├── auth/          # Authentication components
│   ├── jobs/          # Job-related components
│   ├── companies/     # Company components
│   └── layout/        # Layout components
├── pages/             # Page components
│   ├── auth/          # Authentication pages
│   ├── admin/         # Admin pages
│   └── ...           # Other pages
├── hooks/             # Custom React hooks
├── services/          # API services
├── contexts/          # React contexts
├── types/             # TypeScript type definitions
├── utils/             # Utility functions
├── styles/            # Global styles
└── store/             # State management
```

## 🎨 UI Components

### **Design System**
- **Colors** - Primary, secondary, success, warning, error
- **Typography** - Inter font family with consistent sizing
- **Spacing** - Consistent spacing scale
- **Shadows** - Soft, medium, and large shadows
- **Animations** - Smooth transitions and micro-interactions

### **Component Library**
- **Buttons** - Primary, secondary, outline, ghost variants
- **Forms** - Input fields, selects, checkboxes, radio buttons
- **Cards** - Job cards, company cards, application cards
- **Modals** - Confirmation dialogs, forms, details
- **Navigation** - Header, sidebar, breadcrumbs
- **Tables** - Data tables with sorting and pagination

## 🔐 Authentication

### **User Types**
- **Jobseeker** - Browse jobs, apply, manage profile
- **Company** - Post jobs, manage applications
- **Admin** - System administration

### **Protected Routes**
- Route-based authentication
- Role-based access control
- Automatic token refresh
- Session management

## 📊 State Management

### **React Query**
- Server state management
- Automatic caching and background updates
- Optimistic updates
- Error handling and retries

### **Zustand**
- Client state management
- Simple and lightweight
- TypeScript support
- DevTools integration

## 🎯 Key Pages

### **Public Pages**
- **Home** - Landing page with job search
- **Jobs** - Job listings with filters
- **Job Details** - Individual job information
- **Companies** - Company listings
- **Company Details** - Company profiles

### **Authentication Pages**
- **Login** - User authentication
- **Register** - User registration
- **Forgot Password** - Password recovery

### **Protected Pages**
- **Dashboard** - User dashboard
- **Profile** - User profile management
- **Applications** - Job applications
- **Post Job** - Job posting (companies)

### **Admin Pages**
- **Admin Dashboard** - System overview
- **User Management** - User administration
- **Job Management** - Job moderation
- **Analytics** - System statistics

## 🧪 Testing

### **Unit Testing**
```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### **E2E Testing**
```bash
# Run E2E tests
npm run test:e2e
```

## 📦 Build & Deployment

### **Development**
```bash
npm run dev
```

### **Production Build**
```bash
npm run build
```

### **Preview Build**
```bash
npm run preview
```

### **Deployment**
The app can be deployed to:
- **Vercel** - Zero-config deployment
- **Netlify** - Static site hosting
- **AWS S3** - Static website hosting
- **Docker** - Container deployment

## 🔧 Development

### **Code Quality**
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **TypeScript** - Type checking
- **Husky** - Git hooks

### **Scripts**
```bash
# Development
npm run dev

# Build
npm run build

# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

## 🎨 Styling

### **Tailwind CSS**
- Utility-first approach
- Custom design system
- Dark mode support
- Responsive design

### **Custom Components**
- Reusable component library
- Consistent design patterns
- Accessibility features
- Performance optimized

## 📱 Responsive Design

### **Breakpoints**
- **Mobile** - 320px to 768px
- **Tablet** - 768px to 1024px
- **Desktop** - 1024px and above

### **Features**
- Mobile-first approach
- Touch-friendly interfaces
- Optimized for all screen sizes
- Progressive enhancement

## 🚀 Performance

### **Optimizations**
- **Code Splitting** - Automatic chunk splitting
- **Lazy Loading** - Component and route lazy loading
- **Image Optimization** - WebP support and lazy loading
- **Caching** - Browser and service worker caching
- **Bundle Analysis** - Build size monitoring

### **Metrics**
- **First Contentful Paint** - < 1.5s
- **Largest Contentful Paint** - < 2.5s
- **Cumulative Layout Shift** - < 0.1
- **First Input Delay** - < 100ms

## 🔒 Security

### **Features**
- **HTTPS** - Secure connections
- **CSP** - Content Security Policy
- **XSS Protection** - Input sanitization
- **CSRF Protection** - Cross-site request forgery protection
- **Token Management** - Secure JWT handling

## 📈 Analytics

### **Tracking**
- **Page Views** - Route-based tracking
- **User Actions** - Button clicks, form submissions
- **Performance** - Core Web Vitals
- **Errors** - Error tracking and reporting

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### **Development Guidelines**
- Follow TypeScript best practices
- Write meaningful commit messages
- Add tests for new features
- Update documentation
- Follow the design system

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For support, email support@ehb-jps.com or create an issue in the repository.

---

**🎉 EHB-JPS Frontend is ready for development!**

The frontend provides a modern, responsive interface for the job portal system with all essential features implemented and ready for production deployment.
