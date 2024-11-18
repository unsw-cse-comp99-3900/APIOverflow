// src/pages/UserManagement.tsx

import React, { useEffect, useState } from "react";
import UserTable from "../components/UserTable";
import { getUsers, userDelete, userDemote, userPromote } from "../services/apiServices";
import { UserBrief } from "../types/userTypes";

const UserManagement: React.FC = () => {
  // Dummy data for testing (you can replace this with fetched data)
  const [users, setUsers] = useState<UserBrief[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      // Fetch services from the API
      const usersData = await getUsers();
      setUsers(usersData);
    };
    fetchUsers();
  }, [users]);

  const handlePromote = (userId: string, userName: string) => {
    userPromote(userId);
    console.log(`User with ID: ${userId} (${userName}) promoted to admin.`);
  };

  const handleDemote = (userId: string, userName: string) => {
    userDemote(userId);
    console.log(`User with ID: ${userId} (${userName}) demoted to general user.`);
  };

  const handleDelete = (userId: string, userName: string) => {
    userDelete(userId);
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
