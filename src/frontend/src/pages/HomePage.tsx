import React, { useState, useEffect, useRef } from "react";
import { NavLink } from "react-router-dom";
import Blob1 from "../assets/images/blobs/blob1.svg";
import Blob2 from "../assets/images/blobs/blob2.svg";
import Logo from "../assets/images/logo.svg";
import { searchApis } from "../services/apiServices";
import { BriefApi } from "../types/apiTypes";

const HomePage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [results, setResults] = useState<BriefApi[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  const handleSearch = async (term: string) => {
    if (!term.trim()) {
      setResults([]);
      return;
    }
  
    setIsLoading(true);
    setError(null);
  
    try {
      const data = await searchApis(term);

      // Map the data to match your BriefApi structure
      const validResults: BriefApi[] = data.map((item: any) => ({
        name: item.name || item._name,  // Try both formats
        id: item.id || item._id,        // Try both formats
        owner: item.owner || item._owner || {},
        description: item.description || '',
        serviceGlobal: false,
        versions: [],
        reviews: [],
        tags: item.tags || [],
        type: item.type || 'api',
        upvotes: item.upvotes || 0,
        downvotes: item.downvotes || 0,
        newly_created: false,
        icon: '',
        icon_url: item.icon_url || '',
        pay_model: 'free',
        users: []
      }));
  
      setResults(validResults);
      setShowDropdown(true);
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to fetch results. Please try again.');
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to highlight matching text
  const highlightText = (text: string, query: string) => {
    if (!query.trim()) return text;
    
    try {
      const regex = new RegExp(`(${query})`, 'gi');
      const parts = text.split(regex);
      
      return (
        <>
          {parts.map((part, i) => 
            regex.test(part) ? (
              <span key={i} className="bg-yellow-200">{part}</span>
            ) : (
              part
            )
          )}
        </>
      );
    } catch {
      return text;
    }
  };

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchTerm) {
        handleSearch(searchTerm);
      } else {
        setResults([]);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchTerm]);

  return (
    <div className="relative w-screen h-screen pt-24">
      <div className="h-full pt-24 bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
        <img src={Blob1} alt="Blob 1" className="absolute top-0 right-0 w-[400px] h-auto" />
        <img src={Blob2} alt="Blob 2" className="absolute bottom-0 left-0 w-[400px] h-auto" />

        <div className="flex flex-col justify-center items-center w-full max-w-lg">
          <div className="flex items-center mb-6">
            <img src={Logo} alt="API Overflow Logo" className="w-[60px] h-auto mr-4" />
            <h1 className="text-white text-5xl font-bold text-center">
              API Overflow
            </h1>
          </div>

          <p className="text-white text-2xl text-center mb-8">
            A library of APIs and Microservices
          </p>

          <div className="relative w-full max-w-[612px]" ref={searchRef}>
            <div className="w-full h-[50px] px-4 py-3 bg-white rounded-full border-2 border-gray-200 flex justify-between items-center">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onFocus={() => setShowDropdown(true)}
                placeholder="Search API >:)"
                className="w-full px-4 py-2 text-gray-700 focus:outline-none focus:ring-0 border-none rounded-full"
              />
              <div className="flex items-center">
                {isLoading && (
                  <div className="mr-2 w-4 h-4 border-t-2 border-indigo-600 rounded-full animate-spin" />
                )}
                <button
                  className="text-indigo-600"
                  onClick={() => handleSearch(searchTerm)}
                  disabled={isLoading}
                >
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

            {showDropdown && (searchTerm.trim() !== "" || results.length > 0 || error) && (
              <div className="absolute w-full mt-2 bg-white rounded-lg shadow-lg max-h-96 overflow-y-auto z-50">
                {error ? (
                  <div className="p-4 text-red-600">{error}</div>
                ) : results.length === 0 && searchTerm.trim() !== "" ? (
                  <div className="p-4 text-gray-500">No results found</div>
                ) : (
                  results.map((api) => (
                    <NavLink
                      key={api.id}
                      to={`/apis/${api.id}`}
                      className="block p-4 hover:bg-gray-100 border-b last:border-b-0"
                      onClick={() => setShowDropdown(false)}
                    >
                      <div className="flex items-center">
                        <div className="font-medium text-gray-900">
                          {highlightText(api.name, searchTerm)}
                        </div>
                      </div>
                    </NavLink>
                  ))
                )}
              </div>
            )}
          </div>

          <div className="py-6">
            <NavLink
              to="/profile/add-api"
              className="my-4 px-6 py-3 bg-blue-800 text-white font-bold rounded hover:bg-blue-700 focus:outline-none"
            >
              Add an API/Microservice
            </NavLink>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;