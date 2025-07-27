import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  Building2,
  Shield,
  Users,
  TrendingUp,
  CheckCircle,
  ArrowRight,
  Star,
  Award,
  Globe,
  Zap
} from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState('business');

  const features = [
    {
      icon: <Building2 className="w-8 h-8" />,
      title: 'Business Verification',
      description: 'Complete business verification process with document upload and AI-powered validation.'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'SQL Level Management',
      description: 'Track and upgrade your SQL levels from Free to VIP with automated verification.'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Franchise Management',
      description: 'Manage your franchise network with comprehensive dashboard and team controls.'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Performance Analytics',
      description: 'Monitor your business performance with detailed analytics and insights.'
    }
  ];

  const sqlLevels = [
    {
      level: 'Free',
      features: ['Basic profile', 'Limited services', 'Standard support'],
      price: '$0',
      popular: false
    },
    {
      level: 'Basic',
      features: ['Enhanced profile', 'More services', 'Priority support', 'Analytics'],
      price: '$29/month',
      popular: false
    },
    {
      level: 'Normal',
      features: ['Full verification', 'All services', 'Premium support', 'Advanced analytics'],
      price: '$79/month',
      popular: true
    },
    {
      level: 'High',
      features: ['Priority verification', 'Custom features', 'Dedicated support', 'AI insights'],
      price: '$199/month',
      popular: false
    },
    {
      level: 'VIP',
      features: ['Instant verification', 'Exclusive features', '24/7 support', 'Custom solutions'],
      price: '$499/month',
      popular: false
    }
  ];

  return (
    <>
      <Head>
        <title>EMO - Easy Management Office | Business Verification & Management</title>
        <meta name="description" content="EMO (Easy Management Office) - Complete business verification and management platform. Upgrade your SQL levels, manage franchises, and grow your business." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <Building2 className="w-8 h-8 text-blue-600" />
                <span className="ml-2 text-2xl font-bold text-gray-900">EMO</span>
              </div>
              <nav className="hidden md:flex space-x-8">
                <a href="#features" className="text-gray-600 hover:text-blue-600">Features</a>
                <a href="#pricing" className="text-gray-600 hover:text-blue-600">Pricing</a>
                <a href="#about" className="text-gray-600 hover:text-blue-600">About</a>
              </nav>
              <div className="flex items-center space-x-4">
                <Link href="/login" className="text-gray-600 hover:text-blue-600">
                  Sign In
                </Link>
                <Link href="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                  Get Started
                </Link>
              </div>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                Easy Management
                <span className="text-blue-600"> Office</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Complete business verification and management platform. Upgrade your SQL levels,
                manage franchises, and grow your business with our comprehensive tools.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/register" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 flex items-center justify-center">
                  Start Free Trial
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
                <Link href="/demo" className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 flex items-center justify-center">
                  Watch Demo
                </Link>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Everything you need to manage your business
              </h2>
              <p className="text-xl text-gray-600">
                From verification to analytics, EMO provides all the tools you need
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-gray-50 p-6 rounded-lg hover:shadow-lg transition-shadow"
                >
                  <div className="text-blue-600 mb-4">{feature.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* SQL Levels Section */}
        <section id="pricing" className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Choose Your SQL Level
              </h2>
              <p className="text-xl text-gray-600">
                Upgrade your verification level and unlock more features
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              {sqlLevels.map((plan, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className={`bg-white p-6 rounded-lg shadow-lg ${
                    plan.popular ? 'ring-2 ring-blue-600' : ''
                  }`}
                >
                  {plan.popular && (
                    <div className="bg-blue-600 text-white text-sm font-semibold px-3 py-1 rounded-full text-center mb-4">
                      Most Popular
                    </div>
                  )}
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.level}</h3>
                  <div className="text-3xl font-bold text-blue-600 mb-4">{plan.price}</div>
                  <ul className="space-y-2 mb-6">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center text-gray-600">
                        <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <Link
                    href={`/register?plan=${plan.level.toLowerCase()}`}
                    className={`w-full block text-center py-2 px-4 rounded-lg ${
                      plan.popular
                        ? 'bg-blue-600 text-white hover:bg-blue-700'
                        : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                    }`}
                  >
                    Get Started
                  </Link>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-blue-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to get started?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of businesses using EMO to manage their operations
            </p>
            <Link href="/register" className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-100 inline-flex items-center">
              Start Your Free Trial
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-900 text-white py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div>
                <div className="flex items-center mb-4">
                  <Building2 className="w-8 h-8 text-blue-400" />
                  <span className="ml-2 text-xl font-bold">EMO</span>
                </div>
                <p className="text-gray-400">
                  Easy Management Office - Complete business verification and management platform.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Product</h3>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white">Features</a></li>
                  <li><a href="#" className="hover:text-white">Pricing</a></li>
                  <li><a href="#" className="hover:text-white">API</a></li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Company</h3>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white">About</a></li>
                  <li><a href="#" className="hover:text-white">Blog</a></li>
                  <li><a href="#" className="hover:text-white">Careers</a></li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Support</h3>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white">Help Center</a></li>
                  <li><a href="#" className="hover:text-white">Contact</a></li>
                  <li><a href="#" className="hover:text-white">Status</a></li>
                </ul>
              </div>
            </div>
            <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
              <p>&copy; 2024 EMO. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
