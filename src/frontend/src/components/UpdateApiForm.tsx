import { PhotoIcon, DocumentIcon } from "@heroicons/react/24/solid";
import React, { useEffect, useState } from "react";
import { DetailedApi } from "../types/apiTypes";
import {
  getApi,
  updateApi,
  addApi,
  addTag,
  uploadImage,
  apiAddIcon,
  uploadPDF,
  uploadDocs,
} from "../services/apiServices";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { FaPlus, FaTrash } from "react-icons/fa";
import TagsOverlay from "./TagsOverlay";
import { Tag } from "../types/miscTypes";
import FileCard from "./FileCard";
import { useAuth } from "../contexts/AuthContext";

const EditApiForm = ({ apiId }: { apiId?: string }) => {
  const navigate = useNavigate();

  // current api detail for editing
  const [api, setApi] = useState<DetailedApi | null>(null);

  // API information
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [endpoint, setEndpoint] = useState<string>("");
  const [selectedTags, setSelectedTags] = useState<Tag[]>(["API"]);
  const [selectedImage, setSelectedImage] = useState<string>("");
  const [selectedImageData, setSelectedImageData] = useState<File | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [warning, setWarning] = useState<string>("");
  // const [selectedFileData, setSelectedFileData] = useState<File | null>(null);

  // whether the overlay window for adding new tags is open
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);

  // New tags that the user has created in the overlay
  const [newTags, setNewTags] = useState<Tag[]>([]);

  // operations for opening and closing the overlay
  const openOverlay = () => setIsOverlayOpen(true);
  const closeOverlay = () => setIsOverlayOpen(false);

  const auth = useAuth();
  const { logout } = auth!;

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
        setSelectedTags(data.tags);
      } catch (error) {
        console.log("Error fetching data", error);
        toast.error("Error loading API data");
      }
    };
    fetchApi();
  }, [apiId]);

  // Submit the API update to the backend
  const submitApiUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      // Add newly created tags to the database
      for (const newTag of newTags) {
        if (selectedTags.includes(newTag)) {
          await addTag(newTag);
        }
      }

      // Edit existing API
      if (apiId) {
        await updateApi(name, description, selectedTags, endpoint, apiId);
        if (selectedImageData) {
          const doc_id = await uploadImage(selectedImageData);
          apiAddIcon(apiId, doc_id);
        }
        if (selectedFile) {
          console.log(selectedFile);
          const doc_id = await uploadPDF(selectedFile);
          console.log(doc_id);
          await uploadDocs(apiId, doc_id);
        }
        navigate(`/profile/my-apis/${apiId}`);

        // Add new API
      } else {
        const newId = await addApi(name, description, selectedTags, endpoint);
        if (selectedImageData) {
          const doc_id = await uploadImage(selectedImageData);
          apiAddIcon(newId, doc_id);
        }

        if (selectedFile) {
          const doc_id = await uploadPDF(selectedFile);
          await uploadDocs(newId, doc_id);
        }
        navigate(`/profile/my-apis/${newId}`);
      }

      toast.success("Success!");
    } catch (error) {
      if (error instanceof Error && error.message === "Unauthorized") {
        logout();
        navigate("/login");
      }

      console.log("Error updating API", error);
      toast.error("Error updating API");
    }
  };

  return (
    <div className="container-xl lg:container mx-auto p-10">
      <h2 className="text-3xl font-bold text-blue-800 mb-6 mt-6 text-left">
        {apiId ? `Edit API` : "Add API"}
      </h2>

      <form onSubmit={submitApiUpdate}>
        <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
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
              className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
            >
              Name
            </label>
            <div className="mt-2">
              <div className="flex mb-10 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
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

          <div className="border border-gray-100 w-full my-3"></div>
          <div className="col-span-full">
            <label
              htmlFor="endpoint"
              className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
            >
              Endpoint
            </label>

            <div className="mt-2">
              <div className="flex mb-10 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600">
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
              className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
            >
              Description
            </label>
            <div className="mb-10">
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
