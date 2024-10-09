import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../authentication/AuthProvider';

const ProtectedRoute = () => {
  const auth = useAuth();
  const { isLoggedIn } = auth!;

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />; // Redirect to login if not logged in
  }
  // If authenticated, render the children components (Outlet is for nested routes)
  return <Outlet />;
};

export default ProtectedRoute;
