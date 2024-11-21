// src/pages/UserManagement.tsx

import React, { useEffect, useState } from "react";
import UserTable from "../components/UserTable";
import { getUsers, userDelete, userDemote, userPromote } from "../services/apiServices";
import { UserBrief } from "../types/userTypes";
import { toast } from "react-toastify";

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
    try{
      userPromote(userId);
      toast.success(`User Promoted Successfully`);
    } catch (error) {
      console.log(error);
    }
  };

  const handleDemote = (userId: string, userName: string) => {
    try{
      userDemote(userId);
      toast.success(`User Demoted Successfully`);
    } catch (error) {
      console.log(error);
    }

  };

  const handleDelete = (userId: string, userName: string) => {
    try{
      userDelete(userId);
      toast.success(`User Deleted Successfully`);
    } catch (error) {
      console.log(error);
    }
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
