import React from "react";


interface ApiDescriptionProps {
  description: string;
}

const ApiDescription: React.FC<ApiDescriptionProps> = ({ description }) => {
  return (
    <div className=" bg-white border-2 border-gray-100 rounded-2xl shadow-lg p-6 my-6">
      <h2 className="text-xl font-bold mb-4">Description</h2>
      <p className="break-words text-justify">{description}</p>
      <div className="border border-gray-100 w-full my-5"></div>
    </div>
  );
};

export default ApiDescription;
