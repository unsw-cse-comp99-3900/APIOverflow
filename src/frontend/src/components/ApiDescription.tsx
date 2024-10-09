import React from "react";
import { Api } from "../types/apiTypes";

const ApiDescription = ({ api }: { api: Api }) => {
  return (
    <div className="w-1/2 bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">Description</h2>
      {/* API Description */}
      <p className="break-words text-justify">{api.description}</p>
    </div>
  );
};

export default ApiDescription;
