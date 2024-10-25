import React from 'react';
import { Outlet } from 'react-router-dom';
import TagsSideBar from '../components/TagsSideBar';


const TagsSidebarLayout = () => {
  return (
    <div className="flex">
      <TagsSideBar />
      <section className="flex-1 ml-80">
        <Outlet />
      </section>
    </div>
  );
};

export default TagsSidebarLayout;
