import { apiService } from './api'
import { User, LoginCredentials, RegisterData, AuthResponse, ApiResponse } from '@types'

export const authService = {
  // Login user
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    return apiService.post<AuthResponse>('/auth/login', credentials)
  },

  // Register user
  register: async (data: RegisterData): Promise<AuthResponse> => {
    return apiService.post<AuthResponse>('/auth/register', data)
  },

  // Get current user
  getCurrentUser: async (): Promise<User> => {
    const response = await apiService.get<ApiResponse<User>>('/auth/me')
    return response.data
  },

  // Update user profile
  updateProfile: async (userData: Partial<User>): Promise<ApiResponse<User>> => {
    return apiService.put<ApiResponse<User>>('/users/profile', userData)
  },

  // Upload resume
  uploadResume: async (file: File): Promise<ApiResponse<{ resume_url: string }>> => {
    const formData = new FormData()
    formData.append('resume', file)
    return apiService.upload<ApiResponse<{ resume_url: string }>>('/users/upload-resume', formData)
  },

  // Change password
  changePassword: async (data: { current_password: string; new_password: string }): Promise<ApiResponse<{ message: string }>> => {
    return apiService.post<ApiResponse<{ message: string }>>('/auth/change-password', data)
  },

  // Forgot password
  forgotPassword: async (email: string): Promise<ApiResponse<{ message: string }>> => {
    return apiService.post<ApiResponse<{ message: string }>>('/auth/forgot-password', { email })
  },

  // Reset password
  resetPassword: async (data: { token: string; password: string }): Promise<ApiResponse<{ message: string }>> => {
    return apiService.post<ApiResponse<{ message: string }>>('/auth/reset-password', data)
  },

  // Refresh token
  refreshToken: async (): Promise<AuthResponse> => {
    return apiService.post<AuthResponse>('/auth/refresh')
  },

  // Logout
  logout: async (): Promise<ApiResponse<{ message: string }>> => {
    return apiService.post<ApiResponse<{ message: string }>>('/auth/logout')
  },
}
