// frontend/src/context/AuthContext.tsx
"use client";

import { createContext, useState, useEffect, ReactNode } from "react";
import api from "@/lib/api";
import { User, AuthResponse } from "@/types/auth";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      fetchProfile();
    } else {
      setIsLoading(false);
    }
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get("/api/v1/auth/me");
      setUser(response.data);
    } catch (error) {
      localStorage.removeItem("access_token");
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await api.post<AuthResponse>("/api/v1/auth/login", {
      email,
      password,
    });

    localStorage.setItem("access_token", response.data.access_token);
    setUser(response.data.user);
  };

  const register = async (email: string, password: string, fullName: string) => {
    const response = await api.post<AuthResponse>("/api/v1/auth/register", {
      email,
      password,
      full_name: fullName,
    });

    localStorage.setItem("access_token", response.data.access_token);
    setUser(response.data.user);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    window.location.href = "/";
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}