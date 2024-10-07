import React from 'react';
import UserSideBar from '../components/UserSideBar';
import ApiListings from '../components/ApiListings';

const MyApisPage = () => {
  return (
    <div className="flex"> {/* Added flex to make it horizontal */}
      <UserSideBar />  {/* Sidebar */}
      <section className="flex-1 bg-gradient-to-b from-blue-50 px-4 py-6"> {/* Takes remaining space */}
        <ApiListings isMyAPis={true}/>
      </section>
    </div>
  );
};

export default MyApisPage;
