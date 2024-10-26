import React, { createContext, useContext, useState } from 'react';
import { AuthContextType } from '../types/authTypes';

// Create a Login Context
const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token')); // Set initial state based on whether token exists

  const login = (token:string) => {
    localStorage.setItem('token', token); // Save token on login
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem('token'); // Remove token on logout
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook for using authentication
export const useAuth = () => useContext(AuthContext);
