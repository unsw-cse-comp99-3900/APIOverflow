import React, { useEffect, useState } from "react";
import {
  Endpoint,
  EndpointParameter,
  EndpointResponse,
} from "../types/backendTypes";
import { AllowedEndpointTypes } from "../types/miscTypes";
import { FaPlus } from "react-icons/fa";
import NewParameter from "./NewParameter";
import ParameterCard from "./ParameterCard";
import NewResponse from "./NewResponse";
import ResponseCard from "./ResponseCard";
import { toast } from "react-toastify";

interface EndpointUpdateFormProps {
  currEndpoint: Endpoint;
  endpoints: Endpoint[];
  currEndpointIdx: number;
  setCurrEndpoint: React.Dispatch<React.SetStateAction<Endpoint>>;
  setEndpoints: React.Dispatch<React.SetStateAction<Endpoint[]>>;
  setCurrEndpointIdx: React.Dispatch<React.SetStateAction<number>>;
  setVersionUpdated: React.Dispatch<React.SetStateAction<boolean>>;
}

const EndpointUpdateForm: React.FC<EndpointUpdateFormProps> = ({
  currEndpoint,
  endpoints,
  currEndpointIdx,
  setCurrEndpoint,
  setEndpoints,
  setCurrEndpointIdx,
  setVersionUpdated,
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

  useEffect(() => {
    setLink(currEndpoint.link);
    setMainDescription(currEndpoint.main_description);
    setTab(currEndpoint.tab);
    setParameters(currEndpoint.parameters);
    setMethod(currEndpoint.method);
    setResponses(currEndpoint.responses);
  }, [currEndpoint]);

  const deleteEndpoint = () => {
    if (currEndpointIdx !== -1) {
      toast.success("Endpoint Deleted");
      setEndpoints(endpoints.filter((_, index) => index !== currEndpointIdx));
      setVersionUpdated(true);
      setCurrEndpointIdx(-1);
      setCurrEndpoint({
        link: "",
        method: "GET",
        title_description: "title_description place holder",
        main_description: "",
        tab: "",
        parameters: [],
        responses: [],
      });
    } else {
      toast.error("No endpoint selected");
    }
  };

  const submitEndpoint = () => {
    if (link === "") {
      toast.error("Link cannot be empty");
      return;
    } else if (mainDescription === "") {
      toast.error("Description cannot be empty");
      return;
    } else if (tab === "") {
      toast.error("Tab cannot be empty");
      return;
    } else if (parameters.length === 0) {
      toast.error("Parameters cannot be empty");
      return;
    } else if (responses.length === 0) {
      toast.error("Responses cannot be empty");
      return;
    }

    if (currEndpointIdx === -1) {
      // Add a new endpoint
      setEndpoints([
        ...endpoints,
        {
          title_description: "title_description place holder",
          link,
          main_description: mainDescription,
          tab,
          parameters,
          method,
          responses,
        },
      ]);
    } else {
      // Update an existing endpoint
      const updatedEndpoints = endpoints.map((endpoint, index) =>
        index === currEndpointIdx
          ? {
              ...endpoint,
              title_description: "title_description place holder",
              link,
              main_description: mainDescription,
              tab,
              parameters,
              method,
              responses,
            }
          : endpoint
      );
      
      setEndpoints(updatedEndpoints);
    }
    console.log("Endpoint Updated");
    setVersionUpdated(true);
    setCurrEndpoint({
      link: "",
      method: "GET",
      title_description: "title_description place holder",
      main_description: "",
      tab: "",
      parameters: [],
      responses: [],
    });
    setCurrEndpointIdx(-1);
  };

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

  const bgLight = {
    GET: "bg-blue-100",
    POST: "bg-green-100",
    PUT: "bg-yellow-100",
    DELETE: "bg-red-100",
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
            className={`border-2 ${borderDark[method]} rounded-lg shadow-md`}
          >
            <div
              className={`cursor-pointer ${bgLight[method]} rounded-md px-4 py-2 flex justify-between items-center`}
            >
              <div className="flex items-center">
                {/* Method Badge */}
                <div>
                  <div className="flex">
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
                          value={link}
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
            <div className="text-2xl font-semibold pt-10 pb-2 leading-6 text-blue-800">
              Category
            </div>
            <div className="mt-2">
              <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
                <input
                  id="apiTag"
                  name="apiTag"
                  required
                  type="text"
                  onChange={(e) => setTab(e.target.value)}
                  placeholder="Send Information"
                  value={tab}
                  className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                />
              </div>
            </div>
          </div>

          <div className="col-span-full">
            <div className=" text-2xl font-semibold leading-6 pt-10 pb-2  text-blue-800">
              Description
            </div>

            <div className="items-center py-2">
              <textarea
                id="mainDescription"
                name="mainDescription"
                required
                onChange={(e) => setMainDescription(e.target.value)}
                onInput={(e) => {
                  const textarea = e.target as HTMLTextAreaElement;
                  textarea.style.height = "auto";
                  textarea.style.height = textarea.scrollHeight + "px"; // Set height to content
                }}
                placeholder="Description for this endpoint"
                value={mainDescription}
                style={{ overflow: "hidden" }}
                className=" w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
              />
            </div>
          </div>

          <div className=" text-2xl font-semibold py-4 leading-6 text-blue-800">
            Parameters
          </div>

          <NewParameter parameters={parameters} setParameters={setParameters} />

          {parameters.map((parameter) => (
            <ParameterCard key={parameter.id} parameter={parameter} />
          ))}

          <div className="col-span-full block text-2xl pt-10 pb-2 font-semibold py-6 leading-6 text-blue-800">
            Responses
          </div>
          <NewResponse responses={responses} setResponses={setResponses} />

          {responses.map((response) => (
            <ResponseCard
              key={response.code}
              responseCode={response.code}
              responseConditions={response.conditions}
              responseDescription={response.description}
              responseExample={response.example}
            />
          ))}
          <div className="mt-6 flex items-center justify-end gap-x-6">
            <button
              className="rounded-md bg-red-500 px-3 py-2 text-lg font-semibold text-white shadow-sm hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              onClick={() => {
                deleteEndpoint();
              }}
            >
              Delete
            </button>
            <button
              className="rounded-md bg-blue-500 px-3 py-2 text-lg font-semibold text-white shadow-sm hover:bg-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              onClick={() => {
                submitEndpoint();
              }}
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
