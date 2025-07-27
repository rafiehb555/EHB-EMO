'use client';

import { useEffect, useState } from 'react';
import Navigation from '../components/Navigation';

interface Project {
  id: string;
  name: string;
  status: string;
  progress: number;
  type: string;
  lastUpdated: string;
}

interface AIAgent {
  id: string;
  name: string;
  status: string;
  currentTask: string;
  performance: number;
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [agents, setAgents] = useState<AIAgent[]>([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading data
    setTimeout(() => {
      setProjects([
        {
          id: '1',
          name: 'Patient Management System',
          status: 'In Progress',
          progress: 75,
          type: 'Healthcare',
          lastUpdated: '2 hours ago'
        },
        {
          id: '2',
          name: 'E-commerce Platform',
          status: 'Completed',
          progress: 100,
          type: 'Business',
          lastUpdated: '1 day ago'
        },
        {
          id: '3',
          name: 'Blockchain Wallet',
          status: 'Planning',
          progress: 25,
          type: 'Blockchain',
          lastUpdated: '3 hours ago'
        }
      ]);

      setAgents([
        {
          id: '1',
          name: 'Frontend Developer AI',
          status: 'Active',
          currentTask: 'Building React components',
          performance: 95
        },
        {
          id: '2',
          name: 'Backend Developer AI',
          status: 'Active',
          currentTask: 'API development',
          performance: 88
        },
        {
          id: '3',
          name: 'Database AI',
          status: 'Idle',
          currentTask: 'Waiting for tasks',
          performance: 92
        },
        {
          id: '4',
          name: 'Security AI',
          status: 'Active',
          currentTask: 'Security audit',
          performance: 97
        }
      ]);

      setIsLoading(false);
    }, 2000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed': return 'bg-green-100 text-green-800';
      case 'In Progress': return 'bg-blue-100 text-blue-800';
      case 'Planning': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getAgentStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'bg-green-100 text-green-800';
      case 'Idle': return 'bg-gray-100 text-gray-800';
      default: return 'bg-yellow-100 text-yellow-800';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="mb-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: '📊 Overview', icon: '📊' },
              { id: 'projects', label: '📁 Projects', icon: '📁' },
              { id: 'agents', label: '🤖 AI Agents', icon: '🤖' },
              { id: 'analytics', label: '📈 Analytics', icon: '📈' },
              { id: 'settings', label: '⚙️ Settings', icon: '⚙️' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { label: 'Active Projects', value: projects.length, icon: '📁', color: 'blue' },
                { label: 'AI Agents', value: agents.length, icon: '🤖', color: 'green' },
                { label: 'Avg Performance', value: '92%', icon: '📈', color: 'purple' },
                { label: 'System Uptime', value: '99.9%', icon: '🟢', color: 'green' }
              ].map((stat, index) => (
                <div key={index} className="bg-white p-6 rounded-xl shadow-sm">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                      <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                    </div>
                    <div className="text-3xl">{stat.icon}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Projects</h3>
                <div className="space-y-4">
                  {projects.slice(0, 3).map((project) => (
                    <div key={project.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h4 className="font-medium text-gray-900">{project.name}</h4>
                        <p className="text-sm text-gray-600">{project.type}</p>
                      </div>
                      <div className="text-right">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                          {project.status}
                        </span>
                        <p className="text-sm text-gray-600 mt-1">{project.progress}%</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Agent Status</h3>
                <div className="space-y-4">
                  {agents.slice(0, 3).map((agent) => (
                    <div key={agent.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h4 className="font-medium text-gray-900">{agent.name}</h4>
                        <p className="text-sm text-gray-600">{agent.currentTask}</p>
                      </div>
                      <div className="text-right">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAgentStatusColor(agent.status)}`}>
                          {agent.status}
                        </span>
                        <p className="text-sm text-gray-600 mt-1">{agent.performance}%</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Projects Tab */}
        {activeTab === 'projects' && (
          <div className="bg-white rounded-xl shadow-sm">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">All Projects</h3>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  🆕 Create Project
                </button>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {projects.map((project) => (
                  <div key={project.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h4 className="text-xl font-semibold text-gray-900">{project.name}</h4>
                        <p className="text-gray-600">{project.type} • Updated {project.lastUpdated}</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}>
                        {project.status}
                      </span>
                    </div>
                    <div className="mb-4">
                      <div className="flex justify-between text-sm text-gray-600 mb-2">
                        <span>Progress</span>
                        <span>{project.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${project.progress}%` }}
                        />
                      </div>
                    </div>
                    <div className="flex space-x-3">
                      <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        👁️ View
                      </button>
                      <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                        ⚙️ Settings
                      </button>
                      <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                        📊 Analytics
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* AI Agents Tab */}
        {activeTab === 'agents' && (
          <div className="bg-white rounded-xl shadow-sm">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">AI Agents</h3>
                <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                  🤖 Add Agent
                </button>
              </div>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {agents.map((agent) => (
                  <div key={agent.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900">{agent.name}</h4>
                        <p className="text-sm text-gray-600">{agent.currentTask}</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getAgentStatusColor(agent.status)}`}>
                        {agent.status}
                      </span>
                    </div>
                    <div className="mb-4">
                      <div className="flex justify-between text-sm text-gray-600 mb-2">
                        <span>Performance</span>
                        <span>{agent.performance}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${agent.performance}%` }}
                        />
                      </div>
                    </div>
                    <div className="flex space-x-3">
                      <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                        🎯 Assign Task
                      </button>
                      <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                        📊 Monitor
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Development Speed</h3>
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-600 mb-2">3.2x</div>
                  <p className="text-gray-600">Faster than traditional development</p>
                </div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Cost Savings</h3>
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">75%</div>
                  <p className="text-gray-600">Reduction in development costs</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Success Rate</h3>
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">98%</div>
                <p className="text-gray-600">Projects completed successfully</p>
              </div>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">System Settings</h3>
            <div className="space-y-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-3">AI Configuration</h4>
                <div className="space-y-3">
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-3" defaultChecked />
                    <span>Auto-deploy completed projects</span>
                  </label>
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-3" defaultChecked />
                    <span>Send notifications on completion</span>
                  </label>
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-3" />
                    <span>Enable advanced AI features</span>
                  </label>
                </div>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Security</h4>
                <div className="space-y-3">
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-3" defaultChecked />
                    <span>Enable two-factor authentication</span>
                  </label>
                  <label className="flex items-center">
                    <input type="checkbox" className="mr-3" defaultChecked />
                    <span>Automatic security scans</span>
                  </label>
                </div>
              </div>
              <div className="pt-4">
                <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  💾 Save Settings
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
