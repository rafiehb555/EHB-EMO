import React from 'react'
import { Outlet } from 'react-router-dom'
import Header from './layout/Header'
import Footer from './layout/Footer'
import Sidebar from './layout/Sidebar'
import { useAuth } from '@contexts/AuthContext'

const Layout: React.FC = () => {
  const { isAuthenticated, user } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />

      <div className="flex">
        {/* Sidebar for authenticated users */}
        {isAuthenticated && (
          <Sidebar />
        )}

        {/* Main content */}
        <main className={`flex-1 ${isAuthenticated ? 'ml-64' : ''}`}>
          <div className="container mx-auto px-4 py-8">
            <Outlet />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  )
}

export default Layout
