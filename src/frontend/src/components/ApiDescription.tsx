import React from "react";
import { DetailedApi } from "../types/apiTypes";
import { toast } from "react-toastify";
import { FaRegCopy } from "react-icons/fa";

interface ApiDescriptionProps {
  api: DetailedApi;
}

const ApiDescription: React.FC<ApiDescriptionProps> = ({ api }) => {
  const textToCopy = api.endpoint;
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy); // Write text to the clipboard
      toast.success("Copied to clipboard!");
    } catch (err) {
      console.log("Failed to copy!");
    }
  };

  return (
    <div className="w-1/2 bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">Endpoint</h2>
      <div className="flex items-center rounded-xl px-5 my-5 min-h-12 bg-gray-100 border-2 border-gray-500">
        <p className="break-words font-semibold">{api.endpoint}</p>
        <button
          onClick={copyToClipboard}
          className="ml-auto p-2 hover:bg-gray-400 rounded-xl min-h-5"
        >
          <FaRegCopy />
        </button>
      </div>
      <div className="border border-gray-100 w-full mb-5"></div>
      <h2 className="text-xl font-bold mb-4">Description</h2>
      <p className="break-words text-justify">{api.description}</p>
    </div>
  );
};

export default ApiDescription;
