import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../services/apiServices';

let baseUrl = process.env.REACT_APP_API_BASE_URL;

const PasswordResetRequest: React.FC = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
  
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsLoading(true);
      setError('');
      setMessage('');
  
      try {
        console.log('Sending reset request for email:', email.trim());
        
        const response = await fetch(`${baseUrl}/reset-password`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ content: email.trim() }),
        });
  
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
  
        if (!response.ok) {
          throw new Error(data.detail || 'Failed to send reset email');
        }
  
        setMessage('Password reset email sent successfully. Please check your inbox.');
      } catch (err) {
        console.error('Full error:', err);
        setError((err as Error).message || 'Failed to send reset email. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
  
  return (
    <div className="relative w-screen h-screen pt-24">
      <div className="h-full pt-24 bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8 z-10">
          <h1 className="text-2xl font-bold text-center text-blue-900 mb-6">Reset Password</h1>
          
          {message && <p className="text-green-500 text-center mb-4">{message}</p>}
          {error && <p className="text-red-500 text-center mb-4">{error}</p>}

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label htmlFor="email" className="block text-sm font-bold text-gray-700 mb-2">
                Email:
              </label>
              <input
                type="email"
                id="email"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                Send Reset Link
              </button>
            )}

            <div className="flex justify-center pt-3">
              <Link to="/login" className="text-blue-700 underline font-semibold">
                Back to Login
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PasswordResetRequest;