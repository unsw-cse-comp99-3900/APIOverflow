import React, { useState } from "react";
import { AllowedParameterTypes } from "../types/miscTypes";
import { EndpointResponse } from "../types/backendTypes";
import { FaPlus } from "react-icons/fa";
import { toast } from "react-toastify";

interface NewResponseProps {
  responses: EndpointResponse[];
  setResponses: React.Dispatch<React.SetStateAction<EndpointResponse[]>>;
}

const NewResponse: React.FC<NewResponseProps> = ({
  responses,
  setResponses,
}) => {
  const [code, setCode] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [currCondition, setCurrCondition] = useState<string>("");
  const [conditions, setConditions] = useState<string[]>([]);
  const [example, setExample] = useState<string>("");

  const addNewCondition = () => {
    if (currCondition === "") {
      toast.error("Condition cannot be empty");
      return;
    }
    setConditions([...conditions, currCondition]);
    setCurrCondition("");
  };

  const addNewResponse = () => {
    if (code === "") {
      toast.error("Response ode cannot be empty");
      return;
    } else if (description === "") {
      toast.error("Response description cannot be empty");
      return;
    } else if (example === "") {
      toast.error("Response example cannot be empty");
      return;
    } else if (conditions.length === 0) {
      toast.error("Response conditions cannot be empty");
      return;
    }

    for (const existingResponse of responses) {
      if(existingResponse.code === code){
        toast.error("Duplicate response code");
        return;
      }
    }

    setResponses([
      ...responses,
      {
        code,
        description,
        conditions,
        example,
      },
    ]);
    setCode("");
    setDescription("");
    setExample("");
    setConditions([]);
  };

  // Restrict non-numeric characters and limit to 3 digits
  const handleNumericInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (/^\d*$/.test(value) && value.length <= 3) {
      // Allow only digits and limit to 3 characters
      setCode(value);
    }
  };

  return (
    <>
      <div
        className="flex border drop-shadow-md border-gray-300 items-center justify-center px-4 py-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 hover:cursor-pointer"
        onClick={() => addNewResponse()}
      >
        <span className="flex text-lg font-medium items-center">
          <FaPlus />
          <div className="px-3">Add Response</div>
        </span>
      </div>
      <div className="border drop-shadow-md border-gray-300 px-4 my-4 py-4 text-gray-900 bg-white rounded-lg">
        <div className="items-center py-2">
          <div className="font-semibold pl-2 pb-1">Response Code</div>
          <input
            id="responseCode"
            name="responseCode"
            required
            type="text"
            onChange={handleNumericInput}
            placeholder="200"
            value={code}
            className="w-44 border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
          />
        </div>

        <div className="items-center py-2">
          <div className="font-semibold pl-2 py-1">Description</div>
          <textarea
            id="example"
            name="example"
            required
            onChange={(e) => setDescription(e.target.value)}
            onInput={(e) => {
              const textarea = e.target as HTMLTextAreaElement;
              textarea.style.height = "auto";
              textarea.style.height = textarea.scrollHeight + "px"; // Set height to content
            }}
            placeholder="Description for this response code"
            value={description}
            style={{ overflow: "hidden" }}
            className=" w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
          />
        </div>

        <div className="items-center py-2">
          <div className="font-semibold pl-2 py-1">Example</div>
          <textarea
            id="example"
            name="example"
            required
            onChange={(e) => setExample(e.target.value)}
            onInput={(e) => {
              const textarea = e.target as HTMLTextAreaElement;
              textarea.style.height = "auto";
              textarea.style.height = textarea.scrollHeight + "px"; // Set height to content
            }}
            placeholder="Example response body for this response code"
            value={example}
            style={{ overflow: "hidden" }}
            className=" w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
          />
        </div>

        <div className="items-center py-2">
          <div className="font-semibold pl-2 py-1">Conditions</div>
          <div
            className="flex border drop-shadow-lg border-gray-300 items-center justify-center px-4 py-2 mb-4 bg-gray-100 text-black rounded-lg hover:bg-gray-200 hover:cursor-pointer"
            onClick={() => addNewCondition()}
          >
            <span className="flex text-lg font-medium items-center">
              <FaPlus />
              <div className="px-3">Add Condition</div>
            </span>
          </div>
          <textarea
            id="condition"
            name="condition"
            required
            onChange={(e) => setCurrCondition(e.target.value)}
            onInput={(e) => {
              const textarea = e.target as HTMLTextAreaElement;
              textarea.style.height = "auto";
              textarea.style.height = textarea.scrollHeight + "px"; // Set height to content
            }}
            placeholder="Condition that this response code applies to"
            value={currCondition}
            style={{ overflow: "hidden" }}
            className=" w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
          />

          {conditions.map((condition, index) => (
            <div
              key={index}
              className="bg-white border-2 border-gray-300 p-2 rounded mt-2 whitespace-pre-wrap" // Ensure multi-line text formatting
            >
              {condition}
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default NewResponse;
