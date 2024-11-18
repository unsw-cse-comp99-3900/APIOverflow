import React, { useState } from "react";
import { resetPasswordEmail } from "../services/apiServices";

const ResetPasswordRequestPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setMessage("");
  
    try {
      await resetPasswordEmail(email);
      setMessage("Password reset email sent successfully! Please check your inbox.");
    } catch (err: any) {
      console.error(err);
      setError(
        err.message.includes("Unauthorized")
          ? "Password reset is currently unavailable. Please contact support."
          : "Failed to send password reset email."
      );
    }
  };
  
  

  return (
    <div className="w-full max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold text-center">Reset Password</h1>
      {error && <p className="text-red-500 text-center">{error}</p>}
      {message && <p className="text-green-500 text-center">{message}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="email" className="block text-sm font-bold mb-2">
          Email:
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border px-3 py-2 rounded mb-4"
          placeholder="Enter your email"
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded"
        >
          Send Reset Email
        </button>
      </form>
    </div>
  );
};

export default ResetPasswordRequestPage;
