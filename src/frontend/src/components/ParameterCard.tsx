import React, { useState } from "react";
import { AllowedParameterTypes } from "../types/miscTypes";
import { EndpointParameter } from "../types/backendTypes";

interface NewPrameterProps {
  parameter: EndpointParameter;
}

const ParameterCard: React.FC<NewPrameterProps> = ({parameter}) => {

  const [name, setName] = useState<string>("");
  const [component, setComponent] = useState<string>("");
  const [type, setType] = useState<AllowedParameterTypes>("BODY");
  const [required, setRequired] = useState<boolean>(false);

  return (
    <div
      className="border drop-shadow-md border-gray-300 px-4 my-4 py-4 text-gray-900 bg-white rounded-lg"
      onClick={() => {}}
    >

      {/* Data Row */}
      <div
        className={`grid grid-cols-5 gap-4 font-semibold py-2 items-center rounded-t`}
      >
        <div className = "text-center">{parameter.name}</div>
        <div className = "text-center">{parameter.type}</div>
        <div className = "text-center">{parameter.value_type}</div>
        <div className = "text-center">{parameter.required ? "YES" : "NO"}</div>
        <div className = "text-center">{parameter.example}</div>
      </div>
    </div>
  );
};

export default ParameterCard;
