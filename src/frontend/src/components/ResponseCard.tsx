import React from "react";

interface ResponseCardProps {
  responseCode: string;
  responseDescription: string;
  responseExample: string;
  responseConditions: string[];
}

const ResponseCard: React.FC<ResponseCardProps> = ({
  responseCode,
  responseDescription,
  responseExample,
  responseConditions,
}) => {
  return (
    <div className="my-4">
      {/* General info */}
      <div className={`bg-gray-50 border-2 border-gray-300 rounded p-4`}>
        <h3 className="font-semibold mb-2">{`Response Code: ${responseCode}`}</h3>
        <div className="bg-white border-2 border-gray-300 p-2 rounded-md mt-2 whitespace-pre-wrap">
          {responseDescription}
        </div>

        {/* Example Value */}

        <h4 className="font-semibold mt-4 mb-2">Example Value</h4>
        <div
          className=" bg-white border-2 border-gray-300 p-2 rounded-md mt-2 whitespace-pre-wrap" // Ensure multi-line text formatting
        >
          {responseExample}
        </div>

        {/* Conditions */}

        <h3 className="font-semibold mt-4 mb-2">Conditions</h3>
        {responseConditions.map((condition, index) => (
          <div
            key={index}
            className="bg-white border-2 border-gray-300 p-2 rounded-md mt-2 whitespace-pre-wrap" // Ensure multi-line text formatting
          >
            {condition}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResponseCard;
