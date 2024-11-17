import React, { useEffect, useState } from "react";
import { DetailedApi } from "../types/apiTypes";
import { toast } from "react-toastify";
import { FaRegCopy } from "react-icons/fa";
import { getDoc } from "../services/apiServices";

interface ApiDescriptionProps {
  api: DetailedApi;
}

const ApiDescription: React.FC<ApiDescriptionProps> = ({ api }) => {
  return (
    <div className=" bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">Description</h2>
      <p className="break-words text-justify">{api.description}</p>
      <div className="border border-gray-100 w-full my-5"></div>
    </div>
  );
};

export default ApiDescription;
