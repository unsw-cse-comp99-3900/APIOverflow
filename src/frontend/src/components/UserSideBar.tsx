import React from "react";
import { FaSignOutAlt, FaCode } from "react-icons/fa";
import { NavLink } from "react-router-dom";
const UserSideBar = () => {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? "flex items-center px-4 py-2 text-gray-900 bg-gray-100 rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3"
      : "flex items-center px-4 py-2 text-gray-900 bg-white rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3";

  return (
    <aside className="fixed left-0 w-96 h-full px-4 py-8 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700">
      <div className="flex flex-col items-center mt-6 -mx-2">
        <img
          className="object-cover w-48 h-48 mx-2 rounded-full"
          src="https://media.licdn.com/dms/image/v2/D5603AQEr90qaS907Yg/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1698039361377?e=1733961600&v=beta&t=0RQ4b5AZr4o2xoaAOVtgnIwPUaFmcIp3BcnElseUHQ8"
          alt="User Avatar"
        />
        <h4 className="mx-2 mt-2 font-medium text-gray-800 dark:text-gray-200">
          Haoyi Han
        </h4>
        <p className="mx-2 mt-1 text-sm font-medium text-gray-600 dark:text-gray-400">
          Haoyi@example.com
        </p>
      </div>
      <div className="border border-gray-100 mb-5 mt-5"></div>
      <div className="flex flex-col justify-between flex-1">
        <nav>
          {/* MyApis Link */}
          <NavLink to="/profile/myApis" className={linkClass}>
            <span className="ml-3 font-medium flex items-center">
              <FaCode className="mr-2" /> MyAPIs
            </span>
          </NavLink>
          <NavLink to="/profile/Logout" className={linkClass}>
            <span className="ml-3 font-medium flex items-center">
              <FaSignOutAlt className="mr-2" /> LogOut
            </span>
          </NavLink>
        </nav>
      </div>
    </aside>
  );
};

export default UserSideBar;
