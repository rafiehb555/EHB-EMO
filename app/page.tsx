'use client';

import { useEffect, useState } from 'react';
import Navigation from './components/Navigation';
import './globals.css';

interface ProjectTemplate {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  features: string[];
}

interface DevelopmentStep {
  id: string;
  title: string;
  status: 'pending' | 'in-progress' | 'completed' | 'error';
  progress: number;
}

export default function HomePage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedTemplate, setSelectedTemplate] = useState<ProjectTemplate | null>(null);
  const [projectDescription, setProjectDescription] = useState('');
  const [developmentSteps, setDevelopmentSteps] = useState<DevelopmentStep[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{type: 'user' | 'ai', message: string}>>([]);
  const [showChat, setShowChat] = useState(false);

  const projectTemplates: ProjectTemplate[] = [
    {
      id: 'healthcare',
      name: '🏥 Healthcare Management',
      description: 'Patient registration, appointments, medical records',
      icon: '🏥',
      category: 'Healthcare',
      features: ['Patient Portal', 'Appointment Booking', 'Medical Records', 'Prescription Management']
    },
    {
      id: 'ecommerce',
      name: '🛒 E-commerce Platform',
      description: 'Online store with payment processing',
      icon: '🛒',
      category: 'Business',
      features: ['Product Catalog', 'Shopping Cart', 'Payment Gateway', 'Order Management']
    },
    {
      id: 'blockchain',
      name: '⛓️ Blockchain Application',
      description: 'Decentralized applications with smart contracts',
      icon: '⛓️',
      category: 'Blockchain',
      features: ['Smart Contracts', 'Wallet Integration', 'Token Management', 'DeFi Features']
    },
    {
      id: 'social',
      name: '👥 Social Network',
      description: 'Community platform with messaging',
      icon: '👥',
      category: 'Social',
      features: ['User Profiles', 'Messaging', 'Content Sharing', 'Groups']
    },
    {
      id: 'dashboard',
      name: '📊 Business Dashboard',
      description: 'Analytics and reporting platform',
      icon: '📊',
      category: 'Business',
      features: ['Data Visualization', 'Reports', 'KPI Tracking', 'Real-time Updates']
    },
    {
      id: 'custom',
      name: '🎨 Custom Application',
      description: 'Build anything you can imagine',
      icon: '🎨',
      category: 'Custom',
      features: ['AI-Powered', 'Scalable', 'Modern UI', 'Mobile Ready']
    }
  ];

  const developmentStepsData = [
    { id: 'planning', title: '📋 Project Planning', status: 'pending' as const, progress: 0 },
    { id: 'frontend', title: '🎨 Frontend Development', status: 'pending' as const, progress: 0 },
    { id: 'backend', title: '⚙️ Backend Development', status: 'pending' as const, progress: 0 },
    { id: 'database', title: '💾 Database Setup', status: 'pending' as const, progress: 0 },
    { id: 'ai', title: '🤖 AI Features', status: 'pending' as const, progress: 0 },
    { id: 'testing', title: '🧪 Testing & Security', status: 'pending' as const, progress: 0 },
    { id: 'deployment', title: '🚀 Deployment', status: 'pending' as const, progress: 0 },
    { id: 'monitoring', title: '📊 Monitoring Setup', status: 'pending' as const, progress: 0 }
  ];

  useEffect(() => {
    setDevelopmentSteps(developmentStepsData);
  }, []);

  const handleTemplateSelect = (template: ProjectTemplate) => {
    setSelectedTemplate(template);
    setCurrentStep(2);
    addChatMessage('ai', `Great choice! I'll help you build a ${template.name} application. What specific features do you need?`);
  };

  const handleStartBuilding = async () => {
    setIsBuilding(true);
    setCurrentStep(3);

    // Simulate development process
    for (let i = 0; i < developmentStepsData.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 2000));

      setDevelopmentSteps(prev => prev.map((step, index) => {
        if (index === i) {
          return { ...step, status: 'in-progress', progress: 50 };
        }
        return step;
      }));

      await new Promise(resolve => setTimeout(resolve, 1500));

      setDevelopmentSteps(prev => prev.map((step, index) => {
        if (index === i) {
          return { ...step, status: 'completed', progress: 100 };
        }
        return step;
      }));
    }

    setIsBuilding(false);
    setCurrentStep(4);
  };

  const addChatMessage = (type: 'user' | 'ai', message: string) => {
    setChatMessages(prev => [...prev, { type, message }]);
  };

  const handleChatSubmit = (message: string) => {
    addChatMessage('user', message);
    // Simulate AI response
    setTimeout(() => {
      addChatMessage('ai', `I understand you want "${message}". Let me help you implement that feature!`);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Main Content */}
        {currentStep === 1 && (
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Build Your Dream Application
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Choose a template or describe your idea. Our AI will build it for you!
            </p>

            {/* Quick Start Options */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
              {[
                { icon: '🎯', label: 'Quick Start', desc: 'Choose template' },
                { icon: '💬', label: 'Chat with AI', desc: 'Describe your idea' },
                { icon: '🎨', label: 'Visual Builder', desc: 'Drag & drop' },
                { icon: '📊', label: 'Dashboard', desc: 'Monitor progress' }
              ].map((option, index) => (
                <div key={index} className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                  <div className="text-3xl mb-2">{option.icon}</div>
                  <h3 className="font-semibold text-gray-900">{option.label}</h3>
                  <p className="text-sm text-gray-600">{option.desc}</p>
                </div>
              ))}
            </div>

            {/* Project Templates */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projectTemplates.map((template) => (
                <div
                  key={template.id}
                  onClick={() => handleTemplateSelect(template)}
                  className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all cursor-pointer border-2 border-transparent hover:border-blue-200"
                >
                  <div className="text-4xl mb-4">{template.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{template.name}</h3>
                  <p className="text-gray-600 mb-4">{template.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {template.features.slice(0, 2).map((feature, index) => (
                      <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Project Configuration */}
        {currentStep === 2 && selectedTemplate && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="flex items-center mb-6">
                <div className="text-4xl mr-4">{selectedTemplate.icon}</div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{selectedTemplate.name}</h2>
                  <p className="text-gray-600">{selectedTemplate.description}</p>
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Describe your specific requirements:
                </label>
                <textarea
                  value={projectDescription}
                  onChange={(e) => setProjectDescription(e.target.value)}
                  placeholder="Tell me more about your project... For example: 'I need a patient management system that can handle 1000 patients, track appointments, and send SMS reminders'"
                  className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows={4}
                />
              </div>

              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Features included:</h3>
                <div className="grid grid-cols-2 gap-3">
                  {selectedTemplate.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <div className="text-green-500">✓</div>
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex space-x-4">
                <button
                  onClick={() => setCurrentStep(1)}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  ← Back
                </button>
                <button
                  onClick={handleStartBuilding}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
                >
                  <span>🚀 Start Building</span>
                  <span>→</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Development Progress */}
        {currentStep === 3 && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Building Your Application</h2>
                <p className="text-gray-600">Our AI is working hard to create your project...</p>
              </div>

              <div className="space-y-4">
                {developmentSteps.map((step) => (
                  <div key={step.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                          step.status === 'completed' ? 'bg-green-100 text-green-800' :
                          step.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-600'
                        }`}>
                          {step.status === 'completed' ? '✓' : step.status === 'in-progress' ? '⟳' : '○'}
                        </div>
                        <span className="font-medium text-gray-900">{step.title}</span>
                      </div>
                      <span className="text-sm text-gray-500">{step.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${step.progress}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Completion */}
        {currentStep === 4 && (
          <div className="max-w-4xl mx-auto text-center">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Your Application is Ready!</h2>
              <p className="text-xl text-gray-600 mb-8">
                Your {selectedTemplate?.name} has been successfully built and deployed.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-green-50 p-6 rounded-lg">
                  <div className="text-2xl mb-2">🌐</div>
                  <h3 className="font-semibold text-gray-900">Live URL</h3>
                  <p className="text-sm text-gray-600">https://your-app.ehb.ai</p>
                </div>
                <div className="bg-blue-50 p-6 rounded-lg">
                  <div className="text-2xl mb-2">📱</div>
                  <h3 className="font-semibold text-gray-900">Mobile App</h3>
                  <p className="text-sm text-gray-600">Available on App Store</p>
                </div>
                <div className="bg-purple-50 p-6 rounded-lg">
                  <div className="text-2xl mb-2">📊</div>
                  <h3 className="font-semibold text-gray-900">Analytics</h3>
                  <p className="text-sm text-gray-600">Real-time monitoring</p>
                </div>
              </div>

              <div className="flex justify-center space-x-4">
                <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  🚀 Launch Application
                </button>
                <button
                  onClick={() => setCurrentStep(1)}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  🆕 Build Another
                </button>
              </div>
            </div>
          </div>
        )}

        {/* AI Chat Assistant */}
        {showChat && (
          <div className="fixed bottom-4 right-4 w-96 h-96 bg-white rounded-xl shadow-2xl border border-gray-200">
            <div className="bg-blue-600 text-white p-4 rounded-t-xl flex justify-between items-center">
              <h3 className="font-semibold">🤖 AI Assistant</h3>
              <button onClick={() => setShowChat(false)} className="text-white hover:text-gray-200">
                ✕
              </button>
            </div>
            <div className="p-4 h-80 overflow-y-auto">
              {chatMessages.map((msg, index) => (
                <div key={index} className={`mb-3 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-3 rounded-lg ${
                    msg.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    {msg.message}
                  </div>
                </div>
              ))}
            </div>
            <div className="p-4 border-t">
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Ask me anything..."
                  className="flex-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && e.currentTarget.value.trim()) {
                      handleChatSubmit(e.currentTarget.value);
                      e.currentTarget.value = '';
                    }
                  }}
                />
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Send
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
