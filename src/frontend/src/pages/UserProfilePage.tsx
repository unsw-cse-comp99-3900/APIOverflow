import { PhotoIcon } from "@heroicons/react/24/solid";
import React, { useState, useEffect } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { UserProfile } from "../types/userTypes";
import {
  getUser,
  updateDisplayName,
  uploadImage,
  userAddIcon,
} from "../services/apiServices";
import FetchStatus from "../components/FetchStatus";

const MyProfilePage = () => {
  const navigate = useNavigate();

  // current api detail for editing
  const [user, setUser] = useState<UserProfile | null>(null);

  // API information
  const [displayName, setDisplayName] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [role, setRole] = useState<string>("");
  const [selectedImage, setSelectedImage] = useState<string>("");
  const [selectedImageData, setSelectedImageData] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const auth = useAuth();
  const { logout } = auth!;

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

  useEffect(() => {
    let ignore = false;
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await getUser();
        setUser(data);
        setUsername(data.username);
        setDisplayName(data.displayName);
        setEmail(data.email);
        setRole(data.role);
      } catch (error) {
        if (error instanceof Error && error.message === "Unauthorized") {
          setError("Unauthorized");
        } else {
          setError("Failed to load API data");
        }
        toast.error("Error loading API data");
      } finally {
        setLoading(false);
      }
    };
    if (!ignore) fetchProfile();
    return () => {
      ignore = true;
    };
  }, []);

  // Submit the API update to the backend
  const submitUserUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Edit existing User Profile
    await updateDisplayName(displayName);
    if (selectedImageData) {
      const doc_id = await uploadImage(selectedImageData);
      await userAddIcon(doc_id).then(() => {
        navigate(0);
      });
    } else {
      navigate(0);
    }
    // window.location.reload();
  };
  return (
    <FetchStatus loading={loading} error={error} data={user}>
      <div className="container-xl lg:container mx-auto p-10">
        <h2 className="text-3xl font-bold text-blue-800 mb-6 mt-6 text-left">
          My Profile
        </h2>

        <form onSubmit={submitUserUpdate}>
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
                htmlFor="displayName"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Display Name:
              </label>
              <div className="mt-2">
                <div className="flex mb-10 rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 max-w-md">
                  <input
                    id="displayName"
                    name="displayName"
                    required
                    type="text"
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="API Overflow"
                    defaultValue={user?.displayName}
                    className="block flex-1 border-0 bg-transparent py-2 pl-3 text-gray-800 placeholder:text-gray-400 focus:ring-0 focus:font-semibold text-md leading-6"
                  />
                </div>
              </div>
            </div>

            <div className="col-span-full">
              <label
                htmlFor="username"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Username
              </label>
              <textarea
                id="username"
                name="username"
                placeholder="default_username"
                required
                onChange={(e) => setUsername(e.target.value)}
                value={username}
                className="block w-full rounded-md border-0 py-2 pl-3 min-h-10 text-black text-md shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 leading-6 p-4 disabled:bg-gray-100"
                disabled
              />
            </div>

            <div className="col-span-full">
              <label
                htmlFor="email"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Email
              </label>
              <div className="mb-10">
                <textarea
                  id="email"
                  name="email"
                  placeholder="A library of Apis and Microservices"
                  required
                  onChange={(e) => setEmail(e.target.value)}
                  value={email}
                  className="block w-full rounded-md border-0 py-2 pl-3 min-h-10 text-black text-md shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 leading-6 p-4 disabled:bg-gray-100"
                  disabled
                />
              </div>
            </div>

            <div className="col-span-full">
              <label
                htmlFor="role"
                className="block text-2xl font-semibold py-6 leading-6 text-blue-800"
              >
                Account Type
              </label>
              <div className="mb-10">
                <textarea
                  id="role"
                  name="role"
                  placeholder="A library of Apis and Microservices"
                  required
                  onChange={(e) => setRole(e.target.value)}
                  value={role}
                  className="block w-full rounded-md border-0 py-2 pl-3 min-h-10 text-black text-md shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 leading-6 p-4 disabled:bg-gray-100"
                  disabled
                />
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
    </FetchStatus>
  );
};

export default MyProfilePage;
