import React from "react";
import UserSideBar from "../components/UserSideBar"; // Sidebar Component
import { Outlet } from "react-router-dom"; // Outlet to render the nested routes

const UserProfileLayout = () => {
  return (
    <div className="flex">
      {/* Sidebar */}
      <UserSideBar />

      {/* Content area */}
      <section className="flex-1 ml-80">
        <Outlet /> {/* This will render the children components */}
      </section>
    </div>
  );
};

export default UserProfileLayout;
