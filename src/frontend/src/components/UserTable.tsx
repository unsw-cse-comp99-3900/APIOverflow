// src/components/UserTable.tsx

import React, { useState } from "react";

interface User {
  id: string;
  name: string;
  role: "general" | "admin";
}

interface UserTableProps {
  users: User[];
  onPromote: (userId: string, userName: string) => void;
  onDemote: (userId: string, userName: string) => void;
  onDelete: (userId: string, userName: string) => void;
}

const UserTable: React.FC<UserTableProps> = ({ users, onPromote, onDemote, onDelete }) => {
  const [filter, setFilter] = useState<"all" | "admin" | "general">("all");

  const filteredUsers = users.filter((user) =>
    filter === "all" ? true : user.role === filter
  );

  return (
    <div className="w-full">
      <div className="flex justify-between mb-4">
        <h2 className="text-2xl font-bold text-blue-800">Users</h2>
        <div>
          <label className="mr-2 text-gray-700 font-semibold">Filter:</label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as "all" | "admin" | "general")}
            className="p-2 border rounded-md"
          >
            <option value="all">All Users</option>
            <option value="admin">Admins</option>
            <option value="general">General Users</option>
          </select>
        </div>
      </div>
      <table className="w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-3 text-left">Name</th>
            <th className="p-3 text-left">Role</th>
            <th className="p-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredUsers.map((user) => (
            <tr key={user.id} className="border-b hover:bg-gray-100">
              <td className="p-3">{user.name}</td>
              <td className="p-3">{user.role === "admin" ? "Admin" : "General User"}</td>
              <td className="p-3 flex justify-end space-x-2">
                {user.role === "general" ? (
                  <button
                    className="bg-green-500 hover:bg-green-600 text-white font-medium py-1 px-3 rounded transition-all"
                    onClick={() => onPromote(user.id, user.name)}
                  >
                    Promote
                  </button>
                ) : (
                  <button
                    className="bg-yellow-500 hover:bg-yellow-600 text-white font-medium py-1 px-3 rounded transition-all"
                    onClick={() => onDemote(user.id, user.name)}
                  >
                    Demote
                  </button>
                )}
                <button
                  className="bg-red-500 hover:bg-red-600 text-white font-medium py-1 px-3 rounded transition-all"
                  onClick={() => onDelete(user.id, user.name)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserTable;
