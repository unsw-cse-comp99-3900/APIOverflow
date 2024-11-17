import React, { createContext, useContext, useEffect, useState } from "react";
import { userCheckPerm, userLogout } from "../services/apiServices";

export interface AuthContextType {
  isLoggedIn: boolean;
  isAdmin: boolean;
  isSuperAdmin: boolean;
  login: (token: string) => void;
  logout: () => void;
}

// Create a Login Context
const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token")); // Set initial state based on whether token exists
  const [isAdmin, setIsAdmin] = useState(false);
  const [isSuperAdmin, setIsSuperAdmin] = useState(false);

  const fetchPermissions = async () => {
    const perm = await userCheckPerm();
    setIsAdmin(perm.isAdmin);
    setIsSuperAdmin(perm.isSuperAdmin);
  };

  useEffect(() => {
    fetchPermissions();
  }, []);

  const login = async (token: string) => {
    localStorage.setItem("token", token); // Save token on login
    const perm = await userCheckPerm();
    
    setIsLoggedIn(true);
    setIsAdmin(perm.isAdmin);
    setIsSuperAdmin(perm.isSuperAdmin);
  };

  const logout = () => {
    localStorage.removeItem("token"); // Remove token on logout
    userLogout();

    // Reset perms
    setIsLoggedIn(false);
    setIsAdmin(false);
    setIsSuperAdmin(false);
  };

  return (
    <AuthContext.Provider
      value={{ isLoggedIn, isAdmin, isSuperAdmin, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Hook for using authentication
export const useAuth = () => useContext(AuthContext);
