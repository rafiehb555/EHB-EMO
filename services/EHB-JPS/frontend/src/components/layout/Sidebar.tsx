import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  User,
  Briefcase,
  Building2,
  FileText,
  Settings,
  BarChart3,
  Users,
  Calendar,
  MessageSquare
} from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

const Sidebar: React.FC = () => {
  const { user } = useAuth()
  const location = useLocation()

  const getNavigationItems = () => {
    const baseItems = [
      { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
      { name: 'Profile', href: '/profile', icon: User },
    ]

    if (user?.userType === 'admin') {
      return [
        ...baseItems,
        { name: 'Users', href: '/admin/users', icon: Users },
        { name: 'Companies', href: '/admin/companies', icon: Building2 },
        { name: 'Jobs', href: '/admin/jobs', icon: Briefcase },
        { name: 'Applications', href: '/admin/applications', icon: FileText },
        { name: 'Settings', href: '/admin/settings', icon: Settings },
      ]
    }

    if (user?.userType === 'company') {
      return [
        ...baseItems,
        { name: 'Post Job', href: '/post-job', icon: Briefcase },
        { name: 'My Jobs', href: '/dashboard', icon: Building2 },
        { name: 'Applications', href: '/applications', icon: FileText },
        { name: 'Messages', href: '/messages', icon: MessageSquare },
        { name: 'Calendar', href: '/calendar', icon: Calendar },
      ]
    }

    // Job seeker
    return [
      ...baseItems,
      { name: 'My Applications', href: '/applications', icon: FileText },
      { name: 'Saved Jobs', href: '/saved-jobs', icon: Briefcase },
      { name: 'Messages', href: '/messages', icon: MessageSquare },
      { name: 'Settings', href: '/settings', icon: Settings },
    ]
  }

  const navigationItems = getNavigationItems()

  return (
    <aside className="fixed left-0 top-16 h-full w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-y-auto">
      <nav className="p-4">
        <ul className="space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.href

            return (
              <li key={item.name}>
                <Link
                  to={item.href}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'text-blue-600 bg-blue-50 dark:text-blue-400 dark:bg-blue-900/20'
                      : 'text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-50 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar
