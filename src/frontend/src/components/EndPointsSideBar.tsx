import React, { useEffect, useState } from "react";
import { Endpoint } from "../types/backendTypes";

interface EndpointsSidebarProps {
  endpoints: Endpoint[];
  setEndpoints: React.Dispatch<React.SetStateAction<Endpoint[]>>;
}


const EndpointsSidebar: React.FC<EndpointsSidebarProps> = ({endpoints, setEndpoints}) => {

  return (
    <aside className="fixed right-0 w-80 h-full px-4 py-8 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700">
      <div className="flex justify-between items-center px-4">
        <h4 className="font-bold text-gray-800 dark:text-gray-200 ml-3">
          Endpoints
        </h4>
        
      </div>
      <div className="border border-gray-100 mb-5 mt-5"></div>
      <div className="grid grid-cols-1 gap-1">
        {endpoints.map((endpoint, index) => (
          <span
            key={index}
            className="flex items-center px-4 py-2 text-gray-900 bg-white rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3 hover:cursor-pointer"
            onClick = {() => setEndpoints((prevEndpoints) => [...prevEndpoints, endpoint])}
          >
            <span className="ml-3 font-medium flex items-center">
              {endpoint.link}
            </span>
          </span>
        ))}
      </div>
    </aside>
  );
};

export default EndpointsSidebar;
