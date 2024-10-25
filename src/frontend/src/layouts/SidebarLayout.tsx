import React from 'react';
import { Outlet } from 'react-router-dom';

interface SidebarLayoutProps {
  Sidebar: React.FC;
}

const SidebarLayout: React.FC<SidebarLayoutProps> = ({ Sidebar }) => {
  return (
    <div className="flex">
      <Sidebar />
      <section className="flex-1 ml-80">
        <Outlet />
      </section>
    </div>
  );
};

export default SidebarLayout;
