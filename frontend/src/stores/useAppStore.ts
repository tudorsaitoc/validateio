import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  name: string;
}

interface Validation {
  id: string;
  businessIdea: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  createdAt: string;
  results?: {
    marketResearch?: any;
    experiments?: any;
    marketingCampaigns?: any;
  };
}

interface AppState {
  // User state
  user: User | null;
  isAuthenticated: boolean;
  
  // Validation state
  validations: Validation[];
  currentValidation: Validation | null;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setUser: (user: User | null) => void;
  logout: () => void;
  setValidations: (validations: Validation[]) => void;
  addValidation: (validation: Validation) => void;
  updateValidation: (id: string, updates: Partial<Validation>) => void;
  setCurrentValidation: (validation: Validation | null) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        // Initial state
        user: null,
        isAuthenticated: false,
        validations: [],
        currentValidation: null,
        isLoading: false,
        error: null,
        
        // Actions
        setUser: (user) => set({ user, isAuthenticated: !!user }),
        
        logout: () => set({ 
          user: null, 
          isAuthenticated: false,
          validations: [],
          currentValidation: null 
        }),
        
        setValidations: (validations) => set({ validations }),
        
        addValidation: (validation) => set((state) => ({ 
          validations: [...state.validations, validation] 
        })),
        
        updateValidation: (id, updates) => set((state) => ({
          validations: state.validations.map((v) =>
            v.id === id ? { ...v, ...updates } : v
          ),
          currentValidation: state.currentValidation?.id === id
            ? { ...state.currentValidation, ...updates }
            : state.currentValidation,
        })),
        
        setCurrentValidation: (validation) => set({ currentValidation: validation }),
        
        setLoading: (isLoading) => set({ isLoading }),
        
        setError: (error) => set({ error }),
      }),
      {
        name: 'validateio-storage',
        partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
      }
    )
  )
);