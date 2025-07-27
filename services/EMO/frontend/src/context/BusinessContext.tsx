import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

interface Business {
  id: string;
  businessName: string;
  businessType: string;
  industry: string;
  email: string;
  phone: string;
  address: {
    street: string;
    city: string;
    state: string;
    country: string;
    postalCode: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
  };
  description?: string;
  yearEstablished?: number;
  employeeCount?: number;
  annualRevenue?: number;
  verificationStatus: 'pending' | 'in_progress' | 'verified' | 'rejected' | 'expired';
  verificationScore: number;
  verifiedAt?: Date;
  documents: Array<{
    type: string;
    filename: string;
    originalName: string;
    status: 'pending' | 'approved' | 'rejected';
    uploadedAt: Date;
  }>;
  services: Array<{
    name: string;
    description?: string;
    price?: number;
    category?: string;
    isActive: boolean;
  }>;
  metrics: {
    totalOrders: number;
    totalRevenue: number;
    averageRating: number;
    totalReviews: number;
    completionRate: number;
  };
  status: 'active' | 'inactive' | 'suspended' | 'pending';
  createdAt: Date;
  updatedAt: Date;
}

interface BusinessContextType {
  business: Business | null;
  isLoading: boolean;
  error: string | null;
  createBusiness: (businessData: CreateBusinessData) => Promise<void>;
  updateBusiness: (businessId: string, businessData: Partial<Business>) => Promise<void>;
  uploadDocument: (businessId: string, file: File, documentType: string) => Promise<void>;
  getBusiness: (businessId: string) => Promise<void>;
  refreshBusiness: () => Promise<void>;
  clearError: () => void;
}

interface CreateBusinessData {
  businessName: string;
  businessType: string;
  industry: string;
  email: string;
  phone: string;
  address: {
    street: string;
    city: string;
    state: string;
    country: string;
    postalCode: string;
  };
  description?: string;
  yearEstablished?: number;
  employeeCount?: number;
  annualRevenue?: number;
}

const BusinessContext = createContext<BusinessContextType | undefined>(undefined);

export const useBusiness = () => {
  const context = useContext(BusinessContext);
  if (context === undefined) {
    throw new Error('useBusiness must be used within a BusinessProvider');
  }
  return context;
};

interface BusinessProviderProps {
  children: ReactNode;
}

export const BusinessProvider: React.FC<BusinessProviderProps> = ({ children }) => {
  const [business, setBusiness] = useState<Business | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, isAuthenticated } = useAuth();

  // Load business data when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      loadUserBusiness();
    }
  }, [isAuthenticated, user]);

  const loadUserBusiness = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/businesses/my-business`);
      setBusiness(response.data.business);
    } catch (error: any) {
      if (error.response?.status !== 404) {
        setError(error.response?.data?.message || 'Failed to load business data');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const createBusiness = async (businessData: CreateBusinessData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/businesses`, businessData);
      setBusiness(response.data.business);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to create business');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateBusiness = async (businessId: string, businessData: Partial<Business>) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axios.put(`${process.env.NEXT_PUBLIC_API_URL}/api/businesses/${businessId}`, businessData);
      setBusiness(response.data.business);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to update business');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const uploadDocument = async (businessId: string, file: File, documentType: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const formData = new FormData();
      formData.append('document', file);
      formData.append('type', documentType);

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/businesses/${businessId}/documents`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setBusiness(response.data.business);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to upload document');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const getBusiness = async (businessId: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/businesses/${businessId}`);
      setBusiness(response.data.business);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Failed to get business');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const refreshBusiness = async () => {
    if (business) {
      await getBusiness(business.id);
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value: BusinessContextType = {
    business,
    isLoading,
    error,
    createBusiness,
    updateBusiness,
    uploadDocument,
    getBusiness,
    refreshBusiness,
    clearError,
  };

  return (
    <BusinessContext.Provider value={value}>
      {children}
    </BusinessContext.Provider>
  );
};
