import React, { useEffect, useState } from "react";
import { Endpoint } from "../types/backendTypes";
import { FaPlus, FaCode, FaUpload } from "react-icons/fa";

interface EndpointsSidebarProps {
  endpoints: Endpoint[];
  currPage: "Overview" | "Endpoint";
  currEndpointIdx: number;
  currEndpoint: Endpoint;
  setCurrPage: React.Dispatch<React.SetStateAction<"Overview" | "Endpoint">>;
  setEndpoints: React.Dispatch<React.SetStateAction<Endpoint[]>>;
  setCurrEndpointIdx: React.Dispatch<React.SetStateAction<number>>;
  setCurrEndpoint: React.Dispatch<React.SetStateAction<Endpoint>>;
  submitApi: () => void;
}

const EndpointsSidebar: React.FC<EndpointsSidebarProps> = ({
  endpoints,
  currPage,
  currEndpoint,
  currEndpointIdx,
  setEndpoints,
  setCurrPage,
  setCurrEndpointIdx,
  setCurrEndpoint,
  submitApi,
}) => {
  const endpointBg = (endpointIdx: number) => {
    if (endpointIdx === currEndpointIdx) return "bg-gray-100";
    else return "bg-white";
  };

  const bgDark = {
    GET: "bg-blue-500",
    POST: "bg-emerald-500",
    PUT: "bg-yellow-500",
    DELETE: "bg-red-500",
  };

  const newEndpoint: Endpoint = {
    link: "/endpoint/testing",
    method: "GET",
    title_description: "",
    main_description: "",
    tab: "",
    parameters: [],
    responses: [],
  };

  <div className="border-2 border-gray-300 background-gray-100 rounded-md"></div>;

  return (
    <aside className="fixed right-0 w-1/6 h-full px-4 py-8 overflow-y-auto bg-white border-l">
      <div
        className=" drop-shadow-md  flex items-center justify-center px-4 py-4  bg-blue-500 rounded-lg my-8 hover:bg-blue-600 mt-3 text-white hover:cursor-pointer"
        onClick={() => {}}
      >
        <button
          className="flex text-lg font-medium items-center"
          onClick={() => submitApi()}
        >
          <FaUpload />
          <div className="px-3">Submit</div>
        </button>
      </div>

      <div
        className="flex border drop-shadow-md border-gray-300 items-center justify-center px-4 py-4 my-8 text-gray-900 bg-white rounded-lg hover:bg-gray-100 mt-3 hover:cursor-pointer"
        onClick={() => {
          setCurrPage("Overview");
          setCurrEndpoint(newEndpoint);
          setCurrEndpointIdx(-1);
        }}
      >
        <span className="flex text-lg font-medium items-center">
          <FaCode />
          <div className="px-3">Overview</div>
        </span>
      </div>

      <div
        className="flex border drop-shadow-md border-gray-300 items-center justify-center px-4 py-4 my-8 text-gray-900 bg-white rounded-lg hover:bg-gray-100 mt-3 hover:cursor-pointer"
        onClick={() => {
          setCurrPage("Endpoint");
          setEndpoints((prevEndpoints) => [...prevEndpoints, currEndpoint]);
          setCurrEndpointIdx(endpoints.length);
        }}
      >
        <span className="flex text-lg font-medium items-center">
          <FaPlus />
          <div className="px-3">New Endpoint</div>
        </span>
      </div>

      <div className="border border-gray-200 my-2"></div>

      <div className="grid grid-cols-1 gap-1">
        {endpoints.map((endpoint, index) => (
          <span
            key={index}
            className={`flex items-center  px-4 py-2 text-gray-900 ${endpointBg(
              index
            )} rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3 hover:cursor-pointer`}
            onClick={() => {
              setCurrPage("Endpoint");
              setCurrEndpointIdx(index);
              setCurrEndpoint(endpoint);
            }}
          >
            <span className="font-medium flex items-center">
              <div
                className={`rounded-md w-16 h-8 flex items-center justify-center text-white ${
                  bgDark[endpoint.method]
                }`}
              >
                <h2 className="break-words font-semibold text-md">
                  {endpoint.method}
                </h2>
              </div>
              <div className="px-4">{endpoint.link}</div>
            </span>
          </span>
        ))}
      </div>
    </aside>
  );
};

export default EndpointsSidebar;
