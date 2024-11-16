// src/pages/UserManagement.tsx

import React, { useState } from "react";
import UserTable from "../components/UserTable";

const UserManagement: React.FC = () => {
  // Dummy data for testing (you can replace this with fetched data)
  const [users, setUsers] = useState([
    { id: "1", name: "John Doe", role: "general" as "general" },
    { id: "2", name: "Jane Smith", role: "admin" as "admin" },
    { id: "3", name: "Mike Johnson", role: "general" as "general" },
  ]);

  const handlePromote = (userId: string, userName: string) => {
    console.log(`User with ID: ${userId} (${userName}) promoted to admin.`);
  };

  const handleDemote = (userId: string, userName: string) => {
    console.log(`User with ID: ${userId} (${userName}) demoted to general user.`);
  };

  const handleDelete = (userId: string, userName: string) => {
    console.log(`User with ID: ${userId} (${userName}) deleted.`);
  };

  return (
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Users
      </h1>
      <UserTable users={users} onPromote={handlePromote} onDemote={handleDemote} onDelete={handleDelete} />
    </div>
  );
};

export default UserManagement;
