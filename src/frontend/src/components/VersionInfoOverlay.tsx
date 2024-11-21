// src/components/ServiceModal.tsx
import React, { useState } from "react";
import { toast } from "react-toastify";

interface VersionInfoOverlayProps {
  isVersionInfoOverlayOpen: boolean;
  versionName: string;
  versionDescription: string;
  setIsVersionInfoOverlayOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setVersionName: React.Dispatch<React.SetStateAction<string>>;
  setVersionDescription: React.Dispatch<React.SetStateAction<string>>;
  onSubmit: () => void;
}

const VersionInfoOverlay: React.FC<VersionInfoOverlayProps> = ({
  isVersionInfoOverlayOpen,
  versionName,
  versionDescription,
  setIsVersionInfoOverlayOpen,
  setVersionName,
  setVersionDescription,
  onSubmit,
}) => {
  const onRequestClose = () => {
    setVersionName("");
    setVersionDescription("");
    setIsVersionInfoOverlayOpen(false);
  };

  const handleSubmit = () => {
    if (versionName.trim() === "") {
      toast.error("Please enter a version name");
      return;
    } else if (versionName.length > 30) {
      
      toast.error("Version name must be less than 30 characters");
      return;
    }
     else if (versionDescription.trim() === "") {
      toast.error("Please provide a version description");
      return;
    }
    onSubmit();
  };

  if (!isVersionInfoOverlayOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div className="bg-white w-11/12 md:w-1/3 p-6 rounded-lg shadow-lg">
        <h2 className="block text-2xl font-bold pb-4 leading-6 text-blue-800">
          Version Info
        </h2>

        <div className="col-span-full">
          <label
            htmlFor="versionName"
            className="block text-lg font-semibold py-4 leading-6 text-black"
          >
            Version Name
          </label>

          <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
            <input
              id="versionName"
              name="versionName"
              required
              type="text"
              onChange={(e) => setVersionName(e.target.value)}
              placeholder="v1.0.0"
              value={versionName}
              className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 text-md leading-6"
            />
          </div>
        </div>

        <div className="col-span-full">
          <div className="block text-lg font-semibold py-4 leading-6 text-black">
            Version Description
          </div>
          <textarea
            className="w-full h-32 p-2 border rounded-lg mb-4"
            placeholder={`Provide a description for this version`}
            value={versionDescription}
            onChange={(e) => setVersionDescription(e.target.value)}
          />
        </div>

        <div className="flex justify-end space-x-4">
          <button
            className="bg-gray-400 hover:bg-gray-500 text-white font-semibold py-2 px-4 rounded"
            onClick={onRequestClose}
          >
            Cancel
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
            onClick={handleSubmit}
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};

export default VersionInfoOverlay;
