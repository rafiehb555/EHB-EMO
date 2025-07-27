// User Types
export interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  phone?: string
  userType: 'jobseeker' | 'company' | 'admin'
  profileImage?: string
  resumeUrl?: string
  isEmailVerified: boolean
  isActive: boolean
  lastLoginAt?: string
  createdAt: string
  updatedAt: string
}

// Company Types
export interface Company {
  id: number
  userId: number
  companyName: string
  industry?: string
  companySize?: string
  website?: string
  description?: string
  logoUrl?: string
  location?: string
  foundedYear?: number
  isVerified: boolean
  isActive: boolean
  createdAt: string
  updatedAt: string
  user?: User
}

// Job Types
export interface Job {
  id: number
  companyId: number
  title: string
  description: string
  requirements?: string
  salaryMin?: number
  salaryMax?: number
  location?: string
  jobType: 'full-time' | 'part-time' | 'contract' | 'internship'
  experienceLevel?: string
  skills?: string[]
  status: 'active' | 'inactive' | 'filled'
  isRemote: boolean
  benefits?: string[]
  applicationDeadline?: string
  views: number
  applications: number
  createdAt: string
  updatedAt: string
  company?: Company
}

// Application Types
export interface Application {
  id: number
  jobId: number
  userId: number
  resumeUrl?: string
  coverLetter?: string
  status: 'pending' | 'reviewed' | 'shortlisted' | 'rejected' | 'hired'
  appliedAt: string
  reviewedAt?: string
  reviewedBy?: number
  notes?: string
  interviewDate?: string
  interviewLocation?: string
  interviewType?: 'phone' | 'video' | 'in-person'
  createdAt: string
  updatedAt: string
  job?: Job
  user?: User
}

// Auth Types
export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  firstName: string
  lastName: string
  userType: 'jobseeker' | 'company' | 'admin'
  phone?: string
}

export interface AuthResponse {
  success: boolean
  message: string
  data: {
    user: User
    token: string
  }
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  message: string
  data: T
}

// Pagination Types
export interface Pagination {
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
}

// Job Search Types
export interface JobSearchParams {
  page?: number
  limit?: number
  keyword?: string
  location?: string
  jobType?: string
  experienceLevel?: string
  salaryMin?: number
  salaryMax?: number
  companyId?: number
}

// Form Types
export interface JobFormData {
  title: string
  description: string
  requirements?: string
  salaryMin?: number
  salaryMax?: number
  location: string
  jobType: 'full-time' | 'part-time' | 'contract' | 'internship'
  experienceLevel: string
  skills?: string[]
  isRemote: boolean
  benefits?: string[]
  applicationDeadline?: string
}

export interface CompanyFormData {
  companyName: string
  industry?: string
  companySize?: string
  website?: string
  description?: string
  location?: string
  foundedYear?: number
}

export interface ProfileFormData {
  firstName: string
  lastName: string
  phone?: string
  profileImage?: File
}

// Notification Types
export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

// Dashboard Types
export interface DashboardStats {
  totalJobs: number
  totalApplications: number
  activeJobs: number
  pendingApplications: number
  recentJobs: Job[]
  recentApplications: Application[]
}

// Admin Types
export interface AdminStats {
  totalUsers: number
  totalCompanies: number
  totalJobs: number
  totalApplications: number
  userGrowth: number
  jobGrowth: number
  applicationGrowth: number
}
