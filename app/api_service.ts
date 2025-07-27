// EHB AI Dev Agent - API Service
// Complete API integration for frontend

const API_BASE_URL = 'http://localhost:8000';

// Types
export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  sql_level: string;
  is_active: boolean;
  last_login?: string;
  login_count: number;
  created_at: string;
}

export interface AIAgent {
  id: string;
  name: string;
  agent_type: string;
  status: string;
  performance_score: number;
  current_task: string;
  configuration: any;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
  owner_id: string;
  assigned_agents: string[];
  progress: number;
}

export interface Analytics {
  metric_name: string;
  metric_value: number;
  metric_data: any;
  category: string;
  tags: string[];
}

export interface Dashboard {
  metrics: {
    active_agents: number;
    total_projects: number;
    avg_performance: number;
    system_uptime: number;
  };
  agents: AIAgent[];
  projects: Project[];
  analytics: Analytics[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  role?: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  token?: string;
  user?: User;
  error?: string;
}

// API Service Class
class APIService {
  private token: string | null = null;
  private ws: WebSocket | null = null;

  constructor() {
    // Load token from localStorage (only in browser environment)
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  // Authentication methods
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (data.success && data.token) {
        this.token = data.token;
        localStorage.setItem('auth_token', data.token);
        return data;
      } else {
        return { success: false, message: 'Login failed', error: data.error || 'Login failed' };
      }
    } catch (error) {
      return { success: false, message: 'Network error', error: 'Network error' };
    }
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (data.success && data.token) {
        this.token = data.token;
        localStorage.setItem('auth_token', data.token);
        return data;
      } else {
        return { success: false, message: 'Registration failed', error: data.error || 'Registration failed' };
      }
    } catch (error) {
      return { success: false, message: 'Network error', error: 'Network error' };
    }
  }

  async getCurrentUser(): Promise<User | null> {
    if (!this.token) return null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${this.token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        return data.user;
      }
    } catch (error) {
      console.error('Error getting current user:', error);
    }

    return null;
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
    this.disconnectWebSocket();
  }

  // AI Agents methods
  async getAgents(): Promise<AIAgent[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/agents`);
      const data = await response.json();

      if (data.success) {
        return data.agents;
      }
      return [];
    } catch (error) {
      console.error('Error fetching agents:', error);
      return [];
    }
  }

  async getAgent(agentId: string): Promise<AIAgent | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/agents/${agentId}`);
      const data = await response.json();

      if (data.success) {
        return data.agent;
      }
      return null;
    } catch (error) {
      console.error('Error fetching agent:', error);
      return null;
    }
  }

  async createAgentTask(agentId: string, task: {
    task_type: string;
    description: string;
    priority?: string;
  }): Promise<boolean> {
    if (!this.token) return false;

    try {
      const response = await fetch(`${API_BASE_URL}/api/agents/${agentId}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`,
        },
        body: JSON.stringify(task),
      });

      const data = await response.json();
      return data.success;
    } catch (error) {
      console.error('Error creating agent task:', error);
      return false;
    }
  }

  // Projects methods
  async getProjects(): Promise<Project[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/projects`);
      const data = await response.json();

      if (data.success) {
        return data.projects;
      }
      return [];
    } catch (error) {
      console.error('Error fetching projects:', error);
      return [];
    }
  }

  async createProject(project: {
    name: string;
    description: string;
    assigned_agents?: string[];
  }): Promise<boolean> {
    if (!this.token) return false;

    try {
      const response = await fetch(`${API_BASE_URL}/api/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`,
        },
        body: JSON.stringify(project),
      });

      const data = await response.json();
      return data.success;
    } catch (error) {
      console.error('Error creating project:', error);
      return false;
    }
  }

  // Analytics methods
  async getAnalytics(): Promise<Analytics[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics`);
      const data = await response.json();

      if (data.success) {
        return data.analytics;
      }
      return [];
    } catch (error) {
      console.error('Error fetching analytics:', error);
      return [];
    }
  }

  async getMetric(metricName: string): Promise<Analytics | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/${metricName}`);
      const data = await response.json();

      if (data.success) {
        return data.metric;
      }
      return null;
    } catch (error) {
      console.error('Error fetching metric:', error);
      return null;
    }
  }

  // Dashboard methods
  async getDashboard(): Promise<Dashboard | null> {
    if (!this.token) return null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/dashboard`, {
        headers: {
          'Authorization': `Bearer ${this.token}`,
        },
      });

      const data = await response.json();

      if (data.success) {
        return data.dashboard;
      }
      return null;
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      return null;
    }
  }

  // WebSocket methods for real-time updates
  connectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
    }

    this.ws = new WebSocket(`ws://localhost:8000/ws`);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      // Subscribe to agent updates
      this.ws?.send(JSON.stringify({ type: 'subscribe_agents' }));
      this.ws?.send(JSON.stringify({ type: 'subscribe_projects' }));
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleWebSocketMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      // Reconnect after 5 seconds
      setTimeout(() => {
        this.connectWebSocket();
      }, 5000);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  private handleWebSocketMessage(data: any): void {
    switch (data.type) {
      case 'agent_status_update':
        // Dispatch event for agent updates
        window.dispatchEvent(new CustomEvent('agentStatusUpdate', { detail: data.agents }));
        break;
      case 'project_status_update':
        // Dispatch event for project updates
        window.dispatchEvent(new CustomEvent('projectStatusUpdate', { detail: data.projects }));
        break;
      case 'agent_task_created':
        // Dispatch event for new task
        window.dispatchEvent(new CustomEvent('agentTaskCreated', { detail: data }));
        break;
      case 'pong':
        // Handle ping response
        break;
      default:
        console.log('Unknown WebSocket message type:', data.type);
    }
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  // Utility methods
  isAuthenticated(): boolean {
    return !!this.token;
  }

  getToken(): string | null {
    return this.token;
  }
}

// Create singleton instance
export const apiService = new APIService();
