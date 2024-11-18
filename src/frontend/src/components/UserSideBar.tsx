import React, { useState, useEffect } from "react";
import {
  FaSignOutAlt,
  FaCode,
  FaPlusSquare,
  FaUser,
  FaUserFriends,
  FaFolderOpen,
  FaCommentDots,
} from "react-icons/fa";
import { NavLink, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useAuth } from "../contexts/AuthContext";
import { getUser, getUserIcon } from "../services/apiServices";

const UserSideBar = () => {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? "flex items-center px-4 py-2 text-gray-900 bg-gray-100 rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3"
      : "flex items-center px-4 py-2 text-gray-900 bg-white rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3";
  const navigate = useNavigate();
  const auth = useAuth();
  const { logout, isAdmin, isSuperAdmin } = auth!;

  const onLogOutClick = async () => {
    const confirm = window.confirm("Are you sure you want to sign out?");
    if (!confirm) return;
    logout();
    toast.success("Signed out successfully");
    navigate("/");
  };

  const [displayName, setDisplayName] = useState("Guest");
  const [email, setEmail] = useState("guest@apioverflow.com");
  const [iconURL, setIconURL] = useState("https://img.freepik.com/premium-vector/anonymous-user-circle-icon-vector-illustration-flat-style-with-long-shadow_520826-1931.jpg?semt=ais_hybrid");

  useEffect(() => {
    let ignore = false;
    const getUserInfo = async (...args: never[]) =>  {
      try {
          const res = await getUser();
          setDisplayName(`${res.displayName}`);
          setEmail(`${res.email}`);
          console.log("Starting req");
          setIconURL(await getUserIcon());
          console.log("Finished req");
        } catch (error) {
          console.log(`!Something went wrong: ${error}`);
        }
    }
    if (!ignore) getUserInfo();
  return () => { ignore = true;}
  },[]);
  
  

  return (
    <aside className="fixed left-0 w-80 h-full px-4 py-8 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700 flex flex-col justify-between">
      <div className="flex flex-col items-center mt-6 -mx-2">
        <img
          className="object-cover w-40 h-40 mx-2 rounded-full border-2 border-gray-300"
          src={iconURL}
          alt="User Avatar"
        />
        <h4 className="mx-2 mt-2 font-medium text-gray-800 dark:text-gray-200">
          {displayName}
        </h4>
        <p className="mx-2 mt-1 text-sm font-medium text-gray-600 dark:text-gray-400">
          {email}
        </p>
      </div>
      <div className="border border-gray-100 mb-5 mt-5"></div>
      <div className="flex flex-col justify-between flex-1">
        <nav>
          {/* Functional Tabs */}
          <NavLink to="/profile/my-profile" className={linkClass}>
            <span className="ml-3 font-medium flex items-center">
              <FaUser className="mr-2" /> My Profile
            </span>
          </NavLink>
          <NavLink to="/profile/my-apis" className={linkClass}>
            <span className="ml-3 font-medium flex items-center">
              <FaCode className="mr-2" /> My APIs
            </span>
          </NavLink>
          <NavLink to="/profile/add-api" className={linkClass}>
            <span className="ml-3 font-medium flex items-center">
              <FaPlusSquare className="mr-2" /> New API
            </span>
          </NavLink>

          {/* Admin Tabs */}

          {isAdmin && (
            <>
              <div className="border border-gray-100 mb-5 mt-5"></div>
              <NavLink to="/profile/admin/services" className={linkClass}>
                <span className="ml-3 font-medium flex items-center">
                  <FaFolderOpen className="mr-2" /> Service Management
                </span>
              </NavLink>
            </>
          )}

          {isSuperAdmin && (
              <NavLink to="/profile/admin/users" className={linkClass}>
                <span className="ml-3 font-medium flex items-center">
                  <FaUserFriends className="mr-2" /> User Management
                </span>
              </NavLink>
          )}

          {/* Setting tabs */}
          <div className="border border-gray-100 mb-5 mt-5"></div>
          <button
            className="flex w-full items-center px-4 py-2 text-white bg-red-500 rounded-lg  hover:bg-red-600 group mt-3"
            onClick={onLogOutClick}
          >
            <span className="ml-3 font-medium flex items-center ">
              <FaSignOutAlt className="mr-2" /> Sign Out
            </span>
          </button>
        </nav>
      </div>
    </aside>
  );
};

export default UserSideBar;
