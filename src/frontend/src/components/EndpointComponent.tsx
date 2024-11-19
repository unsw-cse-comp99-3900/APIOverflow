import React, { useState } from "react";
import { FaAngleDown, FaAngleUp, FaCopy } from "react-icons/fa";
import { toast } from "react-toastify";
import { Endpoint } from "../types/backendTypes";

interface EndpointComponentProps {
  endpoint: Endpoint;
}

const EndpointComponent: React.FC<EndpointComponentProps> = ({ endpoint }) => {
  const textToCopy = endpoint.link;
  const [isOpen, setIsOpen] = useState(false);

  const borderDark = {
    GET: "border-blue-500",
    POST: "border-emerald-500",
    PUT: "border-yellow-500",
    DELETE: "border-red-500",
  };

  const bgDark = {
    GET: "bg-blue-500",
    POST: "bg-emerald-500",
    PUT: "bg-yellow-500",
    DELETE: "bg-red-500",
  };

  const hoverBgDark = {
    GET: "hover:bg-blue-500",
    POST: "hover:bg-emerald-500",
    PUT: "hover:bg-yellow-500",
    DELETE: "hover:bg-red-500",
  };

  const bgLight = {
    GET: "bg-blue-100",
    POST: "bg-green-100",
    PUT: "bg-yellow-100",
    DELETE: "bg-red-100",
  };

  const textDark = {
    GET: "text-blue-800",
    POST: "text-green-800",
    PUT: "text-yellow-800",
    DELETE: "text-red-800",
  };

  const bgDarkColor = bgDark[endpoint.method];
  const bgLightColor = bgLight[endpoint.method];
  const borderDarkColor = borderDark[endpoint.method];
  const textDarkColor = textDark[endpoint.method];
  const hoverBgDarkColor = hoverBgDark[endpoint.method];

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      toast.success("Copied to clipboard!");
    } catch (err) {
      console.log("Failed to copy!");
      toast.error("Failed to copy to clipboard");
    }
  };
  const toggleSection = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`border-2 ${borderDarkColor} rounded-lg shadow-md my-4`}>
      <div
        onClick={toggleSection}
        className={`cursor-pointer ${bgLightColor} rounded-md px-4 py-2 flex justify-between items-center`}
      >
        <div className="flex items-center">
          {/* Method Badge */}
          <div
            className={`rounded-md w-20 h-10 flex items-center justify-center text-white ${bgDarkColor}`}
          >
            <h2 className="break-words font-semibold text-lg">
              {endpoint.method}
            </h2>
          </div>
          {/* Endpoint Link */}
          <div>
            <h2 className="font-bold text-lg ml-3">{endpoint.link}</h2>
          </div>
        </div>

        {/* Button Container */}
        <div className="flex items-center space-x-4">
          {/* Copy Button */}
          <button
            onClick={(e) => {
              e.stopPropagation(); // Stops the click event from propagating
              copyToClipboard();
            }}
            className={`w-10 h-10 flex items-center justify-center rounded-full ${textDarkColor}  ${hoverBgDarkColor}  hover:text-white`}
          >
            <FaCopy />
          </button>
          {/* Expand/Collapse Button */}
          <button
            className={`w-10 h-10 flex items-center justify-center rounded-full ${textDarkColor} ${hoverBgDarkColor}  hover:text-white`}
            aria-label={isOpen ? "Collapse section" : "Expand section"}
          >
            {isOpen ? <FaAngleUp /> : <FaAngleDown />}
          </button>
        </div>
      </div>
      {isOpen && (
        <>
          <div className="p-4">
            <div className="flex mb-2">
              <h3 className="font-semibold">Category: </h3>
              <h3 className="font-bold ml-2">{endpoint.tab}</h3>
            </div>

            <p className="text-gray-700">{endpoint.main_description}</p>
          </div>
          <div className={`border ${borderDarkColor} `}></div>
          <div
            className={`cursor-pointer ${bgLightColor}   px-4 py-2 flex justify-between items-center`}
          >
            <h2 className="font-bold text-lg">Parameters</h2>
          </div>

          <div className="">
            {/* Grid Header Row */}
            <div
              className={`grid px-4 grid-cols-4 gap-4 bg-gray-100 font-semibold py-2 rounded-t`}
            >
              <div>Name</div>
              <div>Component</div>
              <div>Endpoint Link</div>
              <div>Example</div>
            </div>

            {/* Grid Content Rows */}
            {endpoint.parameters.map((param, index) => (
              <div
                key={index}
                className="grid grid-cols-4 gap-4 border-b py-2 px-4 text-gray-700"
              >
                <div>
                  <div className="flex font-semibold">
                    {param.name}
                    {param.required && <h3 className=" text-red-500">*</h3>}
                  </div>
                  {`(${param.value_type})`}
                </div>
                <div>{param.type}</div>
                <div>{param.endpoint_link}</div>
                <div>{param.example}</div>
              </div>
            ))}
          </div>
          <div className={`border ${borderDarkColor} `}></div>
          <div
            className={`cursor-pointer ${bgLightColor}  px-4 py-2 flex justify-between items-center`}
          >
            <h2 className="font-bold text-lg">Response</h2>
          </div>
          <div className="px-4 pb-4">
            {endpoint.responses.map((response, index) => (
              // each individual response box
              <div key={index} className="my-4">
                {/* General info */}
                <div className={`bg-gray-50 border-2 border-gray-300 rounded p-4`}>
                  <h3 className="font-semibold mb-2">{`Response Code: ${response.code}`}</h3>
                  <div className="mb-2">{response.description}</div>

                  {/* Example Value */}
                  <div className={`border-2 border-gray-300 my-4`}></div>
                  <h4 className="font-semibold">Example Value</h4>
                  <div className="bg-black text-white p-2 rounded mt-2">
                    <code>{response.example}</code>
                  </div>

                  {/* Conditions */}
                  <div className={`border-2 border-gray-300 my-4`}></div>
                  <h3 className="font-semibold my-2">Conditions</h3>
                  {response.conditions.map((condition, index) => (
                    <div
                      key={index}
                      className={`bg-white border-2 border-gray-300 p-2 rounded mt-2`}
                    >
                      <code>{condition}</code>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default EndpointComponent;
