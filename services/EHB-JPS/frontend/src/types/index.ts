// User Types
export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  user_type: 'jobseeker' | 'company' | 'admin'
  phone?: string
  profile_image?: string
  resume_url?: string
  is_verified: boolean
  is_active: boolean
  last_login?: string
  preferences?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface UserProfile extends User {
  company?: Company
  applications?: Application[]
}

// Job Types
export interface Job {
  id: number
  company_id: number
  title: string
  description: string
  requirements?: string
  salary_min?: number
  salary_max?: number
  location: string
  job_type: 'full-time' | 'part-time' | 'contract' | 'internship'
  experience_level?: string
  skills?: string[]
  status: 'active' | 'inactive' | 'filled' | 'expired'
  is_featured: boolean
  is_remote: boolean
  application_deadline?: string
  views_count: number
  applications_count: number
  tags?: string[]
  created_at: string
  updated_at: string
  company?: Company
}

export interface JobWithCompany extends Job {
  company: Company
}

// Company Types
export interface Company {
  id: number
  user_id: number
  company_name: string
  industry: string
  company_size?: string
  website?: string
  description?: string
  logo_url?: string
  location: string
  founded_year?: number
  revenue?: string
  is_verified: boolean
  is_active: boolean
  contact_email?: string
  contact_phone?: string
  social_links?: Record<string, string>
  created_at: string
  updated_at: string
  user?: User
  jobs?: Job[]
}

// Application Types
export interface Application {
  id: number
  job_id: number
  user_id: number
  resume_url?: string
  cover_letter?: string
  status: 'pending' | 'reviewed' | 'shortlisted' | 'rejected' | 'hired'
  applied_at: string
  reviewed_at?: string
  reviewed_by?: number
  review_notes?: string
  interview_date?: string
  interview_location?: string
  interview_notes?: string
  salary_expectation?: number
  availability?: string
  additional_files?: Record<string, any>
  created_at: string
  updated_at: string
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
  first_name: string
  last_name: string
  user_type: 'jobseeker' | 'company'
}

export interface AuthResponse {
  success: boolean
  data: {
    user: User
    token: string
  }
  message?: string
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
  errors?: string[]
}

export interface PaginatedResponse<T> {
  items: T[]
  pagination: {
    current_page: number
    total_pages: number
    total_items: number
    items_per_page: number
  }
}

// Search and Filter Types
export interface JobFilters {
  keyword?: string
  location?: string
  job_type?: string
  experience_level?: string
  salary_min?: number
  salary_max?: number
  is_remote?: boolean
  skills?: string[]
  company_id?: number
  status?: string
  page?: number
  limit?: number
}

export interface CompanyFilters {
  keyword?: string
  industry?: string
  location?: string
  company_size?: string
  is_verified?: boolean
  page?: number
  limit?: number
}

// Form Types
export interface JobFormData {
  title: string
  description: string
  requirements?: string
  salary_min?: number
  salary_max?: number
  location: string
  job_type: 'full-time' | 'part-time' | 'contract' | 'internship'
  experience_level?: string
  skills?: string[]
  is_remote: boolean
  application_deadline?: string
  tags?: string[]
}

export interface CompanyFormData {
  company_name: string
  industry: string
  company_size?: string
  website?: string
  description?: string
  location: string
  founded_year?: number
  revenue?: string
  contact_email?: string
  contact_phone?: string
  social_links?: Record<string, string>
}

export interface ApplicationFormData {
  job_id: number
  cover_letter?: string
  salary_expectation?: number
  availability?: string
}

// Dashboard Types
export interface DashboardStats {
  total_jobs: number
  total_applications: number
  total_companies: number
  active_jobs: number
  pending_applications: number
  recent_jobs: Job[]
  recent_applications: Application[]
}

export interface AdminDashboardStats {
  total_users: number
  total_jobs: number
  total_companies: number
  total_applications: number
  active_users: number
  active_jobs: number
  active_companies: number
  user_types: Array<{
    user_type: string
    count: number
  }>
  recent_users: User[]
  recent_jobs: Job[]
  recent_applications: Application[]
}

// UI Types
export interface BreadcrumbItem {
  label: string
  href?: string
  current?: boolean
}

export interface MenuItem {
  label: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  badge?: string
  children?: MenuItem[]
}

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

// Theme Types
export type Theme = 'light' | 'dark' | 'system'

// File Upload Types
export interface FileUpload {
  file: File
  preview?: string
  progress?: number
  uploaded?: boolean
  error?: string
}

// Chart Types
export interface ChartData {
  labels: string[]
  datasets: Array<{
    label: string
    data: number[]
    backgroundColor?: string[]
    borderColor?: string[]
    borderWidth?: number
  }>
}

// Pagination Types
export interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
  totalItems: number
  itemsPerPage: number
}

// Filter Types
export interface FilterOption {
  value: string
  label: string
  count?: number
}

export interface FilterGroup {
  name: string
  options: FilterOption[]
  multiple?: boolean
}

// Status Types
export type JobStatus = 'active' | 'inactive' | 'filled' | 'expired'
export type ApplicationStatus = 'pending' | 'reviewed' | 'shortlisted' | 'rejected' | 'hired'
export type UserType = 'jobseeker' | 'company' | 'admin'

// Route Types
export interface RouteConfig {
  path: string
  element: React.ComponentType
  protected?: boolean
  allowedRoles?: UserType[]
  public?: boolean
}

// Error Types
export interface ApiError {
  message: string
  status?: number
  errors?: Record<string, string[]>
}

// Loading States
export interface LoadingState {
  isLoading: boolean
  error?: string
  data?: any
}

// Form Validation Types
export interface ValidationError {
  field: string
  message: string
}

export interface FormState<T> {
  data: T
  errors: Record<string, string>
  isValid: boolean
  isDirty: boolean
}

// Search Types
export interface SearchSuggestion {
  id: string
  text: string
  type: 'job' | 'company' | 'skill' | 'location'
  count?: number
}

export interface SearchResult {
  jobs: Job[]
  companies: Company[]
  suggestions: SearchSuggestion[]
}

// Notification Types
export interface NotificationSettings {
  email_notifications: boolean
  job_alerts: boolean
  application_updates: boolean
  marketing_emails: boolean
}

// Settings Types
export interface UserSettings {
  theme: Theme
  language: string
  timezone: string
  notifications: NotificationSettings
  privacy: {
    profile_visibility: 'public' | 'private'
    show_salary: boolean
    show_contact: boolean
  }
}
