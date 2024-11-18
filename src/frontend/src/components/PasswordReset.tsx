import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const PasswordReset: React.FC = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useParams();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`/auth/reset-password/${token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ newpass: newPassword }),
      });

      if (!response.ok) {
        throw new Error('Failed to reset password');
      }

      navigate('/login', { 
        state: { 
          warning: 'Password reset successful. Please login with your new password.' 
        } 
      });
    } catch (err) {
      setError('Failed to reset password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative w-screen h-screen pt-24">
      <div className="h-full pt-24 bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
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
                onChange={(e) => setNewPassword(e.target.value)}
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
                onChange={(e) => setConfirmPassword(e.target.value)}
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

export default PasswordReset;