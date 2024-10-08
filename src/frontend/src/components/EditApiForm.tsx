import { PhotoIcon } from "@heroicons/react/24/solid";
import React from "react";

const EditApiForm = () => {
  return (
    <div className="container-xl lg:container mx-auto px-10">
      <h2 className="text-3xl font-bold text-blue-800 mb-6 mt-6 text-left">
        New API
      </h2>
      <form className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
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
              htmlFor="username"
              className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
            >
              Title
            </label>

            <div className="mt-2">
              <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
                <input
                  id="username"
                  name="username"
                  type="text"
                  placeholder="MyAwesomeAPI"
                  autoComplete="username"
                  className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                />
              </div>
            </div>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="about"
              className="block text-2xl font-semibold py-4 leading-6 text-blue-800"
            >
              Description
            </label>
            <div className="mt-2">
              <textarea
                id="description"
                name="description"
                placeholder="Write a few sentences about your API."
                rows={3}
                className="block w-full rounded-md border-0 py-2 pl-3 min-h-10 text-black text-md shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 leading-6"
                // defaultValue={""}
              />
            </div>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="cover-photo"
              className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
            >
              Documentations
            </label>
            <div className="mt-2 flex justify-center rounded-lg border border-dashed border-blue-800/25 px-6 py-10">
              <div className="text-center">
                <PhotoIcon
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
      </form>
    </div>
  );
};

export default EditApiForm;
