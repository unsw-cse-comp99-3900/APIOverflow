import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

// Import the blob SVG
import Blob1 from "../assets/images/blobs/blob1.svg";
import Blob2 from "../assets/images/blobs/blob2.svg";
import { useAuth } from "../contexts/AuthContext";
import { userRegister } from "../services/apiServices";
import { UserCreate } from "../types/backendTypes";
import { toast } from "react-toastify";

const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [displayname, setDisplayname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (username === "" || password === "") {
      toast.error("Please fill in both fields.");
      setError("Please fill in both fields.");
      return;
    }
    try{
      await userRegister(email, username, password, displayname);
      toast.success("Please verify your email to signin");
      setIsLoading(true);
      navigate("/login", {
        state: {
          username: username,
          password: password,
          warning: "Please verify your email first",
        },
      });
    } catch (error) {
      if (error instanceof Error && error.message === "DuplicateCredentials") {
        toast.error("Username or email already exists");
        setError("Username or email already exists");
      }
    }
  };

  return (
    <div className="relative w-screen h-screen pt-24">
      <div className="h-full pt-24 bg-gradient-to-b from-blue-900 to-[#63b3de] flex justify-center items-center">
        {/* Add the blob as an SVG image   */}
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

        {/* Login Form */}
        <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8 z-10">
          <h1 className="text-2xl font-bold text-center text-blue-900 mb-6">
            Sign Up
          </h1>
          {error && <p className="text-red-500 text-center mb-4">{error}</p>}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                htmlFor="email"
                className="block text-sm font-bold text-gray-700 mb-2"
              >
                Email:
              </label>
              <input
                type="email"
                id="email"
                name="email"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value.replace(/\s/g, ""))}
                required
              />
            </div>
            <div className="mb-4">
              <label
                htmlFor="displayname"
                className="block text-sm font-bold text-gray-700 mb-2"
              >
                Display Name:
              </label>
              <input
                type="displayname"
                id="displayname"
                name="displayname"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="The name that you show to others"
                value={displayname}
                onChange={(e) => setDisplayname(e.target.value)}
                required
              />
            </div>
            <div className="mb-4">
              <label
                htmlFor="username"
                className="block text-sm font-bold text-gray-700 mb-2"
              >
                Username:
              </label>
              <input
                type="username"
                id="username"
                name="username"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="Enter your username"
                value={username}

                // remove all spaces from the username
                onChange={(e) => setUsername(e.target.value.replace(/\s/g, ""))}
                required
              />
            </div>

            <div className="mb-6">
              <label
                htmlFor="password"
                className="block text-sm font-bold text-gray-700 mb-2"
              >
                Password:
              </label>
              <input
                type="password"
                id="password"
                name="password"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg text-gray-700 focus:outline-none focus:border-blue-500"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value.replace(/\s/g, ""))}
                required
              />
            </div>

            {isLoading ? (
              <div className="flex flex-col items-center text-center">
                <div
                  className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full mb-2"
                  role="status"
                ></div>
                <span className="visually-hidden">Loading...</span>
              </div>
            ) : (
              <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none font-semibold"
              >
                Sign Up
              </button>
            )}
            <div className="flex justify-center pt-3">
              <span className="font-semibold text-gray-700">
                Already have an account?
              </span>
              <Link
                to="/login"
                className="pl-2 text-blue-700 underline font-semibold"
              >
                Sign In
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
