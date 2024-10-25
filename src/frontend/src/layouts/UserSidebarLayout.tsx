import React from 'react';
import { Outlet } from 'react-router-dom';
import UserSideBar from '../components/UserSideBar';


const UserSidebarLayout = () => {
  return (
    <div className="flex">
      <UserSideBar />
      <section className="flex-1 ml-80">
        <Outlet />
      </section>
    </div>
  );
};

export default UserSidebarLayout;
