import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../authentication/AuthProvider';
import { toast } from 'react-toastify';

const ProtectedRoute = () => {
  const auth = useAuth();
  const { isLoggedIn } = auth!;

  if (!isLoggedIn) {
    toast.error('You must be logged in to view this page');
    return <Navigate to="/login" replace />; // Redirect to login if not logged in
  }
  // If authenticated, render the children components (Outlet is for nested routes)
  return <Outlet />;
};

export default ProtectedRoute;
