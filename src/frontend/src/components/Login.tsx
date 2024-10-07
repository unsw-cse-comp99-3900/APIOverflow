import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Import the blob SVG
import Blob1 from '../assets/images/blobs/blob1.svg';
import Blob2 from '../assets/images/blobs/blob2.svg';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (email === '' || password === '') {
      setError('Please fill in both fields.');
      return;
    }

    setError('');
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      console.log('Login successful:', { email, password });
      navigate('/dashboard');
    }, 2000);
  };

  return (
    <div className="relative w-screen h-screen bg-gradient-to-b from-[#171785] to-[#63b3de] flex justify-center items-center">
      {/* Add the blob as an SVG image   */}
      <img src={Blob1} alt="Blob 1" className="absolute top-0 right-0 w-[400px] h-auto" />
      <img src={Blob2} alt="Blob 2" className="absolute bottom-0 left-0 w-[400px] h-auto" />

      {/* Login Form */}
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8 z-10">
        <h1 className="text-2xl font-bold text-center mb-6">Login</h1>

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-bold text-gray-700 mb-2">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              className="w-full px-3 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-bold text-gray-700 mb-2">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              className="w-full px-3 py-2 border rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {isLoading ? (
            <div className="text-center">
              <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </div>
          ) : (
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none"
            >
              Login
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default Login;
