import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface Business {
  id: string;
  name: string;
  type: string;
  industry: string;
  revenue: number;
  employeeCount: number;
  location: string;
  yearsInBusiness: number;
  verificationStatus: 'pending' | 'approved' | 'rejected' | 'processing';
  sqlLevel: 'Free' | 'Basic' | 'Normal' | 'High' | 'VIP';
  documents: BusinessDocument[];
  createdAt: string;
  updatedAt: string;
}

interface BusinessDocument {
  id: string;
  type: string;
  filename: string;
  status: 'pending' | 'approved' | 'rejected';
  uploadedAt: string;
  verifiedAt?: string;
}

interface BusinessContextType {
  business: Business | null;
  documents: BusinessDocument[];
  verificationStatus: string;
  sqlLevel: string;
  isLoading: boolean;
  updateBusiness: (data: Partial<Business>) => Promise<void>;
  uploadDocument: (file: File, type: string) => Promise<void>;
  getBusinessProfile: () => Promise<void>;
  submitVerification: () => Promise<void>;
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
  const [documents, setDocuments] = useState<BusinessDocument[]>([]);
  const [verificationStatus, setVerificationStatus] = useState<string>('pending');
  const [sqlLevel, setSqlLevel] = useState<string>('Free');
  const [isLoading, setIsLoading] = useState(false);

  const getBusinessProfile = async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('emo_token');
      
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/business/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setBusiness(data.business);
        setDocuments(data.documents || []);
        setVerificationStatus(data.verificationStatus || 'pending');
        setSqlLevel(data.sqlLevel || 'Free');
      }
    } catch (error) {
      console.error('Error fetching business profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateBusiness = async (data: Partial<Business>) => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('emo_token');
      
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/business/update`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const updatedData = await response.json();
        setBusiness(prev => ({ ...prev, ...updatedData.business }));
      }
    } catch (error) {
      console.error('Error updating business:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const uploadDocument = async (file: File, type: string) => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('emo_token');
      
      if (!token) {
        throw new Error('No authentication token');
      }

      const formData = new FormData();
      formData.append('document', file);
      formData.append('type', type);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/business/upload-document`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setDocuments(prev => [...prev, data.document]);
      }
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const submitVerification = async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('emo_token');
      
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/business/submit-verification`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setVerificationStatus(data.status);
        if (business) {
          setBusiness(prev => ({ ...prev!, verificationStatus: data.status }));
        }
      }
    } catch (error) {
      console.error('Error submitting verification:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Load business profile on mount
    getBusinessProfile();
  }, []);

  const value: BusinessContextType = {
    business,
    documents,
    verificationStatus,
    sqlLevel,
    isLoading,
    updateBusiness,
    uploadDocument,
    getBusinessProfile,
    submitVerification,
  };

  return (
    <BusinessContext.Provider value={value}>
      {children}
    </BusinessContext.Provider>
  );
}; 