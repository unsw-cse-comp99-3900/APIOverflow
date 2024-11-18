import React, { useState } from "react";
import { resetPassword } from "../services/apiServices";

const ResetPasswordPage: React.FC = () => {
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      await resetPassword(token, newPassword);
      setMessage("Password reset successful!");
    } catch (err: any) {
      setError("Failed to reset password. Ensure the token is valid.");
    }
  };

  return (
    <div className="w-full max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold text-center">Reset Password</h1>
      {error && <p className="text-red-500 text-center">{error}</p>}
      {message && <p className="text-green-500 text-center">{message}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="token" className="block text-sm font-bold mb-2">
          Token:
        </label>
        <input
          type="text"
          id="token"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          className="w-full border px-3 py-2 rounded mb-4"
          placeholder="Enter the reset token"
          required
        />
        <label htmlFor="password" className="block text-sm font-bold mb-2">
          New Password:
        </label>
        <input
          type="password"
          id="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          className="w-full border px-3 py-2 rounded mb-4"
          placeholder="Enter a new password"
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded"
        >
          Reset Password
        </button>
      </form>
    </div>
  );
};

export default ResetPasswordPage;
