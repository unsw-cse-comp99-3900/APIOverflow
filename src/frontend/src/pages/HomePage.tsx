import React from 'react';
import Blob1 from '../assets/images/blobs/blob1.svg';  // Adjust path as needed
import Blob2 from '../assets/images/blobs/blob2.svg';  // Adjust path as needed
import Logo from '../assets/images/logo.svg';  // Import the logo
import { NavLink } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div className="relative w-screen h-screen pt-24">
    <div className="h-full pt-24 bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
      {/* Blobs */}
      <img src={Blob1} alt="Blob 1" className="absolute top-0 right-0 w-[400px] h-auto" />
      <img src={Blob2} alt="Blob 2" className="absolute bottom-0 left-0 w-[400px] h-auto" />

      {/* Main Content */}
      <div className="flex flex-col justify-center items-center w-full max-w-lg">
        {/* Logo and Title */}
        <div className="flex items-center mb-6">
          <img src={Logo} alt="API Overflow Logo" className="w-[60px] h-auto mr-4" />
          <h1 className="text-white text-5xl font-bold text-center">
            API Overflow
          </h1>
        </div>

        <p className="text-white text-2xl text-center mb-8">
          A library of APIs and Microservices
        </p>

        {/* Search Bar and Button Container */}
        <div className="flex flex-col justify-center items-center">
          <div className="flex justify-center items-center gap-4 mb-4">
            {/* Search Bar */}
            <div className="w-[612px] h-[50px] px-4 py-3 bg-white rounded-full border border-[#d9d9d9] flex justify-start items-center gap-2">
              <input
                type="text"
                placeholder="Search API >:)"
                className="w-full px-4 py-2 text-gray-700 focus:outline-none focus:ring-0 border-none"
              />
              <button className="text-indigo-600">
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </button>
            </div>

          </div>

          {/* Add API Button */}
          <div className='py-6'>
            <NavLink to="/profile/add-api" className=" my-4 px-6 py-3 bg-blue-800 text-white font-bold rounded hover:bg-blue-700 focus:outline-none">
              Add an API/Microservice
            </NavLink>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
};

export default HomePage;
