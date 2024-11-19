import { PhotoIcon, DocumentIcon } from "@heroicons/react/24/solid";
import React, { useState } from "react";
import { FaCrown, FaPlus, FaTrash } from "react-icons/fa";
import TagsOverlay from "./TagsOverlay";
import { PayModel, Tag } from "../types/miscTypes";
import FileCard from "./FileCard";

interface OverviewUpdateFormProps {
  name: string;
  description: string;
  selectedTags: Tag[];
  newTags: Tag[];
  selectedImage: string;
  selectedImageData: File | null;
  selectedFile: File | null;
  payModel: PayModel;
  setName: React.Dispatch<React.SetStateAction<string>>;
  setDescription: React.Dispatch<React.SetStateAction<string>>;
  setSelectedTags: React.Dispatch<React.SetStateAction<Tag[]>>;
  setNewTags: React.Dispatch<React.SetStateAction<Tag[]>>;
  setSelectedImage: React.Dispatch<React.SetStateAction<string>>;
  setSelectedImageData: React.Dispatch<React.SetStateAction<File | null>>;
  setSelectedFile: React.Dispatch<React.SetStateAction<File | null>>;
  setPayModel: React.Dispatch<React.SetStateAction<PayModel>>;
}

const OverviewUpdateForm: React.FC<OverviewUpdateFormProps> = ({
  name,
  description,
  selectedTags,
  newTags,
  payModel,
  selectedImage,
  selectedImageData,
  selectedFile,
  setName,
  setDescription,
  setSelectedTags,
  setNewTags,
  setPayModel,
  setSelectedImage,
  setSelectedImageData,
  setSelectedFile,
}) => {
  const [warning, setWarning] = useState<string>("");
  // const [selectedFileData, setSelectedFileData] = useState<File | null>(null);

  // whether the overlay window for adding new tags is open
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);

  // operations for opening and closing the overlay
  const openOverlay = () => setIsOverlayOpen(true);
  const closeOverlay = () => setIsOverlayOpen(false);

  const handleTagClick = (tag: Tag) => {
    if (
      selectedTags.includes("API") !== selectedTags.includes("Microservice") &&
      (tag === "API" || tag === "Microservice")
    ) {
      setWarning("You must select either API or Microservice");
      return;
    }
    setWarning("");
    setSelectedTags(selectedTags.filter((t) => t !== tag));
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const iconImage = event.target.files?.[0];
    if (iconImage) {
      const reader = new FileReader();
      reader.onload = () => {
        setSelectedImage(reader.result as string);
      };
      setSelectedImageData(iconImage);
      reader.readAsDataURL(iconImage);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  return (
    <div className="container-xl lg:container mx-auto p-10">
      <div>
        <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
          <h1 className="text-lg font-semibold text-gray-600 mb-10">
            *Note: Editing the Documentation or Endpoints will create a new
            version of the service.
          </h1>

          <div className="col-span-full flex flex-col items-center py-6 mx-2">
            <button
              type="button"
              className="rounded-full bg-white h-56 w-56 border-2 border-gray-300 hover:bg-gray-50 flex justify-center items-center"
            >
              <label className="flex items-center justify-center cursor-pointer">
                {selectedImage ? (
                  // Display the uploaded image
                  <img
                    src={selectedImage}
                    alt="Uploaded"
                    className="h-full w-full object-cover rounded-full"
                  />
                ) : (
                  // Display the placeholder icon if no image is uploaded
                  <PhotoIcon className="h-32 w-32 text-gray-400" />
                )}
                <input
                  id="icon-upload"
                  name="icon-upload"
                  type="file"
                  accept="image/*"
                  className="sr-only"
                  onChange={(e) => handleImageUpload(e)}
                />
              </label>
            </button>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="apiName"
              className="block text-2xl font-semibold pt-10 pb-4 leading-6 text-blue-800"
            >
              Name
            </label>

              <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
                <input
                  id="apiName"
                  name="apiName"
                  required
                  type="text"
                  onChange={(e) => setName(e.target.value)}
                  placeholder="API Overflow"
                  defaultValue={name}
                  className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                />
              </div>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="payModel"
              className="block text-2xl font-semibold pt-10 pb-6 leading-6 text-blue-800"
            >
              Pay Model
            </label>
            <div className="space-y-4">
              {/* Premium Option */}
              <div className="flex items-center">
                <label className="flex items-center space-x-3">
                  <input
                    type="radio"
                    name="payModel"
                    value="Premium"
                    checked={payModel === "Premium"}
                    onChange={() => setPayModel("Premium")}
                    className="h-5 w-5 text-amber-500 focus:ring-amber-500"
                  />
                  <div
                    className={`py-1 flex items-center justify-center bg-amber-500 rounded-md px-4 w-36`}
                  >
                    <FaCrown className="text-white mr-2" />
                    <span className="text-white text-lg font-medium">
                      Premium
                    </span>
                  </div>
                </label>
                <div className="font-semibold text-gray-700 ml-4">
                  Premium services are available to users with a subscription
                </div>
              </div>

              {/* Freemium Option */}
              <div className="flex items-center">
                <label className="flex items-center space-x-3">
                  <input
                    type="radio"
                    name="payModel"
                    value="Freemium"
                    checked={payModel === "Freemium"}
                    onChange={() => setPayModel("Freemium")}
                    className="h-5 w-5 text-purple-500 focus:ring-purple-500"
                  />
                  <div
                    className={`py-1 flex items-center justify-center bg-purple-500 rounded-md px-4 w-36`}
                  >
                    <FaCrown className="text-white mr-2" />
                    <span className="text-white text-lg font-medium">
                      Freemium
                    </span>
                  </div>
                </label>
                <div className="font-semibold text-gray-700 ml-4">
                  Freemium services are available to all users with some
                  limitations
                </div>
              </div>

              {/* Free Option */}
              <div className="flex items-center">
                <label className="flex items-center space-x-3">
                  <input
                    type="radio"
                    name="payModel"
                    value="Free"
                    checked={payModel === "Free"}
                    onChange={() => setPayModel("Free")}
                    className="h-5 w-5 text-blue-500 focus:ring-blue-500"
                  />
                  <div
                    className={`py-1 flex items-center justify-center bg-blue-500 rounded-md px-4 w-36`}
                  >
                    <span className="text-white text-lg font-medium">Free</span>
                  </div>
                </label>
                <div className="font-semibold text-gray-700 ml-4">
                  Free services are available to all users
                </div>
              </div>
            </div>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="apiName"
              className="block text-2xl font-semibold pt-10 pb-4 leading-6 text-blue-800"
            >
              Tags
            </label>

            <div className="flex flex-wrap">
              {selectedTags.map((tag) => (
                <button
                  key={tag}
                  type="button" // Prevent form submission
                  onClick={() => handleTagClick(tag)}
                  className="relative bg-blue-800 text-white flex items-center justify-center rounded-md text-sm font-semibold px-3 py-1 mx-1 my-1"
                >
                  <span className="transition-opacity duration-200 hover:opacity-0">
                    {tag}
                  </span>

                  <span className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-red-500 rounded-md transition-opacity duration-200">
                    <FaTrash />
                  </span>
                </button>
              ))}
              {/* Overlay button for more tags */}
              <button
                type="button" // Prevent form submission
                onClick={() => {
                  setWarning("");
                  openOverlay();
                }}
                className="border-blue-800 border-2 bg-white hover:bg-blue-800 hover:text-white text-blue-800 w-7 h-7 flex items-center justify-center rounded-md mx-1 my-1"
              >
                <FaPlus className="text-sm" />
              </button>
            </div>
            {warning && (
              <p className="text-red-500 text-sm my-2 mx-2">{warning}</p>
            )}
            {/* Overlay Window */}
            <TagsOverlay
              isOpen={isOverlayOpen}
              onClose={closeOverlay}
              selectedTags={selectedTags}
              newTags={newTags}
              setSelectedTags={setSelectedTags}
              setNewTags={setNewTags}
            />
          </div>

          <div className="col-span-full">
            <label
              htmlFor="description"
              className="block text-2xl font-semibold pt-10 pb-2 leading-6 text-blue-800"
            >
              Description
            </label>

            <div className="items-center py-2">
              <textarea
                id="description"
                name="description"
                required
                onChange={(e) => setDescription(e.target.value)}
                onInput={(e) => {
                  const textarea = e.target as HTMLTextAreaElement;
                  textarea.style.height = "auto";
                  textarea.style.height = textarea.scrollHeight + "px"; // Set height to content
                }}
                placeholder="Description for this endpoint"
                value={description}
                style={{ overflow: "hidden" }}
                className=" w-full border rounded-md p-2 shadow-sm focus:ring-2 focus:ring-indigo-600"
              />
            </div>
          </div>

          <div className="col-span-full">
            <label
              htmlFor="Documentation"
              className="block text-2xl font-semibold pt-10 pb-2 leading-6 text-blue-800"
            >
              Documentation
            </label>
            <div className="mt-2 flex justify-center rounded-lg border border-dashed border-blue-800/25 px-6 py-10">
              <div className="text-center">
                <DocumentIcon
                  aria-hidden="true"
                  className="mx-auto h-12 w-12 text-gray-300"
                />
                <div className="mt-4 flex flex-col items-center text-2xl leading-6 text-gray-600">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer hover:underline rounded-md bg-white font-semibold text-indigo-600 hover:text-indigo-500"
                  >
                    <span>Upload a file</span>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      accept="application/pdf" // Only accept PDF files
                      className="sr-only"
                      onChange={handleFileChange} // Capture file selection here
                    />
                  </label>
                  {/* <p className="pl-1">or drag and drop</p>  Todo: Support drag and drop */}

                  {selectedFile && FileCard({ fileName: selectedFile.name })}
                </div>
                <p className="text-xs leading-5 pt-1 text-gray-600">
                  PDF up to 10MB
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OverviewUpdateForm;
