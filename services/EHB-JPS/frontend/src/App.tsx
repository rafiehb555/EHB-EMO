import { Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'

import Layout from '@components/Layout'
import LoadingSpinner from '@components/ui/LoadingSpinner'
import ProtectedRoute from '@components/auth/ProtectedRoute'
import PublicRoute from '@components/auth/PublicRoute'

// Lazy load pages for better performance
const HomePage = lazy(() => import('@pages/HomePage'))
const JobsPage = lazy(() => import('@pages/JobsPage'))
const JobDetailPage = lazy(() => import('@pages/JobDetailPage'))
const CompaniesPage = lazy(() => import('@pages/CompaniesPage'))
const CompanyDetailPage = lazy(() => import('@pages/CompanyDetailPage'))
const LoginPage = lazy(() => import('@pages/auth/LoginPage'))
const RegisterPage = lazy(() => import('@pages/auth/RegisterPage'))
const ProfilePage = lazy(() => import('@pages/ProfilePage'))
const DashboardPage = lazy(() => import('@pages/DashboardPage'))
const ApplicationsPage = lazy(() => import('@pages/ApplicationsPage'))
const PostJobPage = lazy(() => import('@pages/PostJobPage'))
const AdminDashboardPage = lazy(() => import('@pages/admin/AdminDashboardPage'))
const NotFoundPage = lazy(() => import('@pages/NotFoundPage'))

function App() {
  return (
    <Layout>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/jobs/:id" element={<JobDetailPage />} />
          <Route path="/companies" element={<CompaniesPage />} />
          <Route path="/companies/:id" element={<CompanyDetailPage />} />

          {/* Auth Routes */}
          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            }
          />

          {/* Protected Routes */}
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/applications"
            element={
              <ProtectedRoute>
                <ApplicationsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/post-job"
            element={
              <ProtectedRoute allowedRoles={['company']}>
                <PostJobPage />
              </ProtectedRoute>
            }
          />

          {/* Admin Routes */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminDashboardPage />
              </ProtectedRoute>
            }
          />

          {/* 404 Route */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </Layout>
  )
}

export default App
