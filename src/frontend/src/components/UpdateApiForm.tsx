import { PhotoIcon, DocumentIcon } from "@heroicons/react/24/solid";
import React, { useEffect, useState } from "react";
import { DetailedApi, NewApi } from "../types/apiTypes";
import { getApi, updateApi, addApi } from "../services/apiServices";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { ServicePost, ServiceUpdate } from "../types/backendTypes";

const EditApiForm = ({ apiId }: { apiId?: string }) => {
  const [api, setApi] = useState<DetailedApi | null>(null);
  const navigate = useNavigate();
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [endpoint, setEndpoint] = useState<string>("");

  useEffect(() => {
    const fetchApi = async () => {
      if (apiId === undefined) {
        return;
      }
      try {
        const data = await getApi(apiId);
        setApi(data);
        setName(data.name);
        setDescription(data.description);
        setEndpoint(data.endpoint);
      } catch (error) {
        console.log("Error fetching data", error);
        toast.error("Error loading API data");
      }
    };
    fetchApi();
  }, []); // Ensure the effect runs whenever the id changes


  const submitApiUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

		if (apiId) {
      const updatedApi:ServiceUpdate = {
        sid: apiId,
        name,
        description,
        endpoint,
        tags: ["sample_tag"],
      };
      
      await updateApi(updatedApi);
      navigate(`/profile/my-apis/${apiId}`);
    } else {
      const newApi:ServicePost = {
        name,
        description,
        endpoint,
        x_start : 0,
        x_end : 100,
        y_start : 0,
        y_end : 100,
        icon_url: "",
        tags: ["sample_tag"],

      }; 
      const newId = await addApi(newApi);
      console.log(newId)
      navigate(`/profile/my-apis/${newId}`);
    }
    console.log(apiId)
    
    toast.success('Success!');
    
  };


  return (
    <div className="container-xl lg:container mx-auto px-10">
      <h2 className="text-3xl font-bold text-blue-800 mb-6 mt-6 text-left">
        {apiId ? `Edit API` : "Add API"}
      </h2>

      <form onSubmit={submitApiUpdate}>
        <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
          <div className="mt-10 grid gap-x-6 gap-y-8 grid-cols-6">
            <div className="col-span-full flex flex-col items-center mt-6 -mx-2">
              <button
                type="button"
                className="rounded-full bg-white h-56 w-56 px-5 py-5 ring-2 ring-inset ring-gray-300 hover:bg-gray-50 flex justify-center items-center"
              >
                <PhotoIcon className="h-32 w-32 text-gray-400" />
              </button>
            </div>

            <div className="col-span-full">
              <label
                htmlFor="apiName"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Name
              </label>

              <div className="mt-2">
                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
                  <input
                    id="apiName"
                    name="apiName"
                    required
                    type="text"
                    onChange={(e) => setName(e.target.value)}
                    placeholder="API Overflow"
                    defaultValue={api?.name}
                    className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                  />
                </div>
              </div>
            </div>

            <div className="col-span-full">
              <label
                htmlFor="apiName"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Endpoint
              </label>

              <div className="mt-2">
                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600">
                  <input
                    id="endpoint"
                    name="endpoint"
                    required
                    type="text"
                    onChange={(e) => setEndpoint(e.target.value)}
                    placeholder="https://api-overflow.com/non-playable-coders/example-endpoint"
                    defaultValue={api?.endpoint}
                    className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 text-md leading-6"
                  />
                </div>
              </div>
            </div>


            <div className="col-span-full">
              <label
                htmlFor="description"
                className="block text-2xl font-semibold py-4 leading-6 text-blue-800"
              >
                Description
              </label>
              <div className="mt-2">
                <textarea
                  id="description"
                  name="description"
                  placeholder="A library of Apis and Microservices"
                  required
                  onChange={(e) => setDescription(e.target.value)}
                  value={description}
                  className="block w-full rounded-md border-0 py-2 pl-3 min-h-10 text-black text-md shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 leading-6"
                  defaultValue={api?.description}
                />
              </div>
            </div>

            <div className="col-span-full">
              <label
                htmlFor="Documentation"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Documentations
              </label>
              <div className="mt-2 flex justify-center rounded-lg border border-dashed border-blue-800/25 px-6 py-10">
                <div className="text-center">
                  <DocumentIcon
                    aria-hidden="true"
                    className="mx-auto h-12 w-12 text-gray-300"
                  />
                  <div className="mt-4 flex text-2xl leading-6 text-gray-600">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer hover:underline rounded-md bg-white font-semibold text-indigo-600 hover:text-indigo-500"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        className="sr-only"
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs leading-5 pt-1 text-gray-600">
                    PDF up to 10MB
                  </p>
                </div>
              </div>
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
      </form>
    </div>
  );
};

export default EditApiForm;
