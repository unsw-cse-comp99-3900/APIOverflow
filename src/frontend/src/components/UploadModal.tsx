import React, { useState } from "react";
import { DocumentIcon } from "@heroicons/react/24/solid";
import YFileCard from "./YFileCard";
import { uploadYAML } from "../services/apiServices";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

interface UploadModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  onErrorReset: (toggle: boolean) => void;
}

const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onRequestClose,
  onErrorReset,
}) => {
  const [selectedYFile, setSelectedYFile] = useState<File | null>(null);

  const navigate = useNavigate();

  if (!isOpen) return null; // If the modal is not open, return null

  const handleYFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedYFile(e.target.files[0]);
    }
  };

  const onProcess = async () => {
    if (selectedYFile) {
      try {
        const sid = await uploadYAML(selectedYFile);
        if (sid === '') {
          toast.error("Something went wrong with your YAML file. Please try again!");
        } else {
          navigate(`/profile/my-apis/${sid}`);
        }
      } catch (error) {
        toast.error("Something went wrong with your YAML file. Please try again!");
      }
    } else {
      toast.error("Must upload YAML configuration file!");
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-3xl bg-white rounded-lg shadow-lg p-6 mx-4">
        <h2 className="text-2xl font-bold mb-4 text-center text-blue-800">
          Add an API
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col items-center justify-center h-full">
            {" "}
            {/* Add `justify-center` and `h-full` */}
            <button className="bg-blue-500 text-white font-semibold py-2 px-6 rounded-full hover:bg-blue-600 transition-all shadow-lg"
              onClick={onRequestClose}>
              Create Service Manually
            </button>
          </div>

          <div className="flex flex-col items-center">
            <div className="mt-2 flex w-full justify-center rounded-lg border border-dashed border-blue-800/25 px-6 py-10">
              <div className="text-center">
                <DocumentIcon
                  aria-hidden="true"
                  className="mx-auto h-12 w-12 text-gray-300"
                />
                <div className="mt-4 flex flex-col items-center text-2xl leading-6 text-gray-600">
                  <label
                    htmlFor="yfile-upload"
                    className="relative cursor-pointer hover:underline rounded-md bg-white font-semibold text-indigo-600 hover:text-indigo-500"
                  >
                    <span>Upload a YAML file</span>
                    <input
                      id="yfile-upload"
                      name="yfile-upload"
                      type="file"
                      accept=".yaml"
                      className="sr-only"
                      onChange={handleYFileChange}
                    />
                  </label>
                  {selectedYFile && YFileCard({ fileName: selectedYFile.name })}
                </div>
                <p className="text-xs leading-5 pt-1 text-gray-600">
                  YAML up to 10MB
                </p>
              </div>
            </div>
            <button className="mt-4 bg-blue-500 text-white font-semibold py-2 px-6 rounded-full  hover:bg-blue-600 transition-all shadow-lg"
              onClick={onProcess}>
              Create API via YAML
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadModal;
