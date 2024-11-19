import React, { useState } from "react";
import {
  Endpoint,
  EndpointParameter,
  EndpointResponse,
} from "../types/backendTypes";
import { AllowedEndpointTypes } from "../types/miscTypes";

interface EndpointUpdateFormProps {
  currEndpoint: Endpoint;
  setCurrEndpoint: React.Dispatch<React.SetStateAction<Endpoint>>;
}

const EndpointUpdateForm: React.FC<EndpointUpdateFormProps> = ({
  currEndpoint,
  setCurrEndpoint,
}) => {
  const [link, setLink] = useState<string>(currEndpoint.link);
  const [mainDescription, setMainDescription] = useState<string>(
    currEndpoint.main_description
  );
  const [tab, setTab] = useState<string>(currEndpoint.tab);
  const [parameters, setParameters] = useState<EndpointParameter[]>(
    currEndpoint.parameters
  );
  const [method, setMethod] = useState<AllowedEndpointTypes>(
    currEndpoint.method
  );
  const [responses, setResponses] = useState<EndpointResponse[]>(
    currEndpoint.responses
  );
  const [isOpen, setIsOpen] = useState(false);

  const methods: AllowedEndpointTypes[] = ["GET", "POST", "PUT", "DELETE"];
  const borderDark = {
    GET: "border-blue-500",
    POST: "border-emerald-500",
    PUT: "border-yellow-500",
    DELETE: "border-red-500",
  };

  const hoverBorderDark = {
    GET: "hover:border-blue-700",
    POST: "hover:border-emerald-700",
    PUT: "hover:border-yellow-700",
    DELETE: "hover:border-red-700",
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

  return (
    <div className="container-xl lg:container mx-auto p-10">
      <div>
        <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
          <div className="col-span-full">
            <label
              htmlFor="apiLInk"
              className="block text-2xl font-semibold py-2 leading-6 text-blue-800"
            >
              Link
            </label>
          </div>

          {/*  */}
          <div
            className={`border-2 ${borderDark[method]} rounded-lg shadow-md my-4`}
          >
            <div
              className={`cursor-pointer ${bgLight[method]} rounded-md px-4 py-2 flex justify-between items-center`}
            >
              <div className="flex items-center">
                {/* Method Badge */}
                <div>
                  <div className = "flex">
                    <div
                      className={`rounded-md my-2 w-20 h-10 flex items-center justify-center text-white ${bgDark[method]} hover:border-2 ${hoverBorderDark[method]} hover:transition-transform hover:scale-105`}
                      onClick={() => {
                        setIsOpen(!isOpen);
                      }}
                    >
                      <h2 className="break-words font-semibold text-lg">
                        {method}
                      </h2>
                    </div>
                    <div className="mt-2">
                      <div className="flex w-full bg-white ml-4 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600">
                        <input
                          id="apiLink"
                          name="apiLink"
                          required
                          type="text"
                          onChange={(e) => setLink(e.target.value)}
                          placeholder="/example/endpoint"
                          defaultValue={link}
                          className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                        />
                      </div>
                    </div>
                  </div>
                  {isOpen &&
                    methods
                      .filter((m) => m !== method) // Filter out the current method
                      .map((m: AllowedEndpointTypes) => (
                        <div
                          key={m}
                          className={`rounded-md my-2 w-20 h-10 flex items-center justify-center text-white ${bgDark[m]} hover:border-2 ${hoverBorderDark[m]} hover hover:transition-transform hover:scale-105`}
                          onClick={() => {
                            setIsOpen(!isOpen);
                            setMethod(m as AllowedEndpointTypes);
                          }}
                        >
                          <h2 className="break-words font-semibold text-lg">
                            {m}
                          </h2>
                        </div>
                      ))}
                </div>
              </div>
            </div>
          </div>

          {/*  */}
          <div className="col-span-full">
            <label
              htmlFor="apiTab"
              className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
            >
              Category
            </label>
            <div className="mt-2">
              <div className="flex mb-10 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
                <input
                  id="apiTag"
                  name="apiTag"
                  required
                  type="text"
                  onChange={(e) => setTab(e.target.value)}
                  placeholder="Send Information"
                  defaultValue={tab}
                  className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                />
              </div>
            </div>
          </div>


          <div className="col-span-full">
            <label
              htmlFor="mainDescription"
              className="block text-2xl mt-10 font-semibold py-6 leading-6 text-blue-800"
            >
              Description
            </label>
            <div className="mb-10">
              <textarea
                id="mainDescription"
                name="mainDescription"
                placeholder="This Endpoint sends information to the server"
                required
                onChange={(e) => setMainDescription(e.target.value)}
                value={mainDescription}
                className="block w-full rounded-md border-0 py-2 pl-3 min-h-10 text-black text-md shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 leading-6"
              />
            </div>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="description"
              className="block text-2xl mt-10 font-semibold py-6 leading-6 text-blue-800"
            >
              Parameters
            </label>
            <div className="mb-10">

            </div>
          </div>


          <div className="mt-6 flex items-center justify-end gap-x-6">
            <button
              type="submit"
              className="rounded-md bg-blue-800 px-3 py-2 text-lg font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EndpointUpdateForm;
