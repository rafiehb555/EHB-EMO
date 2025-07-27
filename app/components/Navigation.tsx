'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();

  const navItems = [
    { href: '/', label: '🏠 Home', icon: '🏠' },
    { href: '/dashboard', label: '📊 Dashboard', icon: '📊' },
  ];

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-3">
            <div className="text-3xl">🚀</div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">EHB AI Dev Studio</h1>
              <p className="text-sm text-gray-600">Your AI Development Partner</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex space-x-2">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    pathname === item.href
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </div>

            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              💬 AI Assistant
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
