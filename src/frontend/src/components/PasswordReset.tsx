import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Blob1 from "../assets/images/blobs/blob1.svg";
import Blob2 from "../assets/images/blobs/blob2.svg";

let baseUrl = process.env.REACT_APP_API_BASE_URL;

const VerifiedPasswordReset: React.FC = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) {
      setError('Invalid reset link');
      return;
    }
    
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`${baseUrl}/auth/reset-password/${token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ newpass: newPassword }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to reset password');
      }

      navigate('/login', { 
        state: { 
          warning: 'Password reset successful. Please login with your new password.' 
        } 
      });
    } catch (err) {
      setError((err as Error).message || 'Failed to reset password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center">
      <div className="h-full w-full bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
        <img
          src={Blob1}
          alt="Blob 1"
          className="absolute top-24 right-0 w-[400px] h-auto"
        />
        <img
          src={Blob2}
          alt="Blob 2"
          className="absolute bottom-0 left-0 w-[400px] h-auto"
        />

        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8 z-10">
          <h1 className="text-2xl font-bold text-center text-blue-900 mb-6">Set New Password</h1>
          
          {error && <p className="text-red-500 text-center mb-4">{error}</p>}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="newPassword" className="block text-sm font-bold text-gray-700 mb-2">
                New Password:
              </label>
              <input
                type="password"
                id="newPassword"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="Enter new password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value.replace(/\s/g, ""))}
                required
              />
            </div>

            <div className="mb-6">
              <label htmlFor="confirmPassword" className="block text-sm font-bold text-gray-700 mb-2">
                Confirm Password:
              </label>
              <input
                type="password"
                id="confirmPassword"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="Confirm new password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value.replace(/\s/g, ""))}
                required
              />
            </div>

            {isLoading ? (
              <div className="flex flex-col items-center text-center">
                <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full mb-2" />
                <span className="visually-hidden">Loading...</span>
              </div>
            ) : (
              <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none font-semibold"
              >
                Reset Password
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default VerifiedPasswordReset;