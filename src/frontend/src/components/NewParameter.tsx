import React, { useState } from "react";
import { AllowedParameterTypes } from "../types/miscTypes";
import { EndpointParameter } from "../types/backendTypes";
import { FaPlus } from "react-icons/fa";
import { toast } from "react-toastify";

interface NewPrameterProps {
  parameters: EndpointParameter[];
  setParameters: React.Dispatch<React.SetStateAction<EndpointParameter[]>>;
}

const NewParameter: React.FC<NewPrameterProps> = ({
  parameters,
  setParameters,
}) => {
  const [name, setName] = useState<string>("");
  const [component, setComponent] = useState<AllowedParameterTypes>("BODY");
  const [type, setType] = useState<string>("string");
  const [required, setRequired] = useState<boolean>(false);
  const [example, setExample] = useState<string>("");

  const addNewParameter = () => {
    if (name === "") {
      toast.error("Parameter name cannot be empty");
      return;
    } else if (type === "") {
      toast.error("Parameter type cannot be empty");
      return;
    } else if (example === "") {
      toast.error("Parameter example cannot be empty");
      return;
    }
    setParameters([
      ...parameters,
      {
        id: String(parameters.length),
        endpoint_link: "endpoint_link placeholder",
        name,
        type: component,
        value_type: type,
        required,
        example,
      },
    ]);
    setName("");
    setComponent("BODY");
    setType("string");
    setExample("");
    setRequired(false);
  };

  return (
    <>
      <div
        className="flex border drop-shadow-md border-gray-300 items-center justify-center px-4 py-4  bg-blue-500 text-white rounded-lg hover:bg-blue-600  hover:cursor-pointer"
        onClick={() => addNewParameter()}
      >
        <span className=" flex text-lg font-medium items-center">
          <FaPlus />
          <div className="px-3">Add Parameter</div>
        </span>
      </div>
      <div className="border drop-shadow-md border-gray-300 px-4 my-4 py-4 text-gray-900 bg-white rounded-lg">
        {/* Header Row */}
        <div className="grid grid-cols-5 gap-4 bg-gray-100 font-semibold py-2 rounded-t">
          <div className="text-center">Name</div>
          <div className="text-center">Component</div>
          <div className="text-center">Type</div>
          <div className="text-center">Required</div>
          <div className="text-center">Example</div>
        </div>
        {/* Data Row */}
        <div className="grid grid-cols-5 gap-4 font-semibold py-2 items-center">
          {/* Name Input */}
          <div className="flex items-center">
            <input
              id="parameterName"
              name="parameterName"
              required
              type="text"
              onChange={(e) => setName(e.target.value)}
              placeholder="ParameterName"
              value={name}
              className="w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
            />
          </div>
          {/* Component Dropdown */}
          <div className="flex items-center">
            <select
              value={component}
              onChange={(e) =>
                setComponent(e.target.value as AllowedParameterTypes)
              }
              className="p-2 border rounded-md w-full shadow-sm focus:ring-2 focus:ring-indigo-600"
            >
              <option value="HEADER">HEADER</option>
              <option value="BODY">BODY</option>
              <option value="PATH">PATH</option>
              <option value="QUERY">QUERY</option>
            </select>
          </div>
          {/* Type Placeholder */}
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Type"
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
            />
          </div>
          {/* Required Checkbox */}
          <div className="flex items-center justify-center">
            <input
              type="checkbox"
              checked={required}
              onChange={(e) => setRequired(e.target.checked)}
              className="h-5 w-5 border-gray-300 rounded"
            />
          </div>
          {/* Example Placeholder */}
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Example"
              value={example}
              onChange={(e) => setExample(e.target.value)}
              className="w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
            />
          </div>
          {/* Add Button */}
        </div>
      </div>{" "}
    </>
  );
};

export default NewParameter;
