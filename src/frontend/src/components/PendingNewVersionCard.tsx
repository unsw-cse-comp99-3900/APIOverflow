import React, { useEffect, useState } from "react";
import { apiGetIcon } from "../services/apiServices";
import { PendingVersion } from "../types/apiTypes";
import { FaCrown } from "react-icons/fa";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import Tag from "./Tag";

interface PendingNewVersionCardProps {
  version: PendingVersion;
  setCurrentPendingVersion: React.Dispatch<
    React.SetStateAction<PendingVersion | null>
  >;
}

const PendingNewVersionCard: React.FC<PendingNewVersionCardProps> = ({
  version,
  setCurrentPendingVersion,
}) => {
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [iconURL, setIconURL] = useState<string>("");

  useEffect(() => {
    const fetchIcon = async () => {
      try {
        const iconURL = await apiGetIcon(version.id);
        setIconURL(iconURL);
      } catch (error) {
        console.log(error);
      }
    };

    fetchIcon();
    // Cleanup the object URL to avoid memory leaks
    return () => {
      if (iconURL) {
        URL.revokeObjectURL(iconURL);
      }
    };
  }, []);

  let description = version.version_description;

  if (!showFullDescription && description.length > 90) {
    description = description.substring(0, 90) + "...";
  }

  return (
    <div
      className="bg-white rounded-xl shadow-md relative transition-transform transform hover:scale-105 my-4 hover:cursor-pointer"
      onClick={() => setCurrentPendingVersion(version)}
    >
      <div className="p-4">
        <div className="pb-16">
          <div className="flex items-start mb-2">
            <img
              src={iconURL || defaultApiIcon}
              alt="API Icon"
              className="w-20 h-20 ml-4 mr-4 mt-2 rounded-full object-cover border-2 border-gray-300"
            />

            <div className="items-center">
              <h3 className="text-xl font-bold my-2">{version.name}</h3>
              <div className = "flex my-2 text-lg">
              <h3 className="font-semibold text-gray-500">Version Name: </h3>
              <h3 className="text-blue-800 font-semibold ml-2">{version.version_name}</h3>
              </div>
            </div>
          </div>

          <div className="border border-gray-100 mx-4 mb-5"></div>
          <h1 className="text-lg font-semibold text-blue-800 ml-4 mb-2">
            Patch Note
          </h1>
          <div className="mx-4 mb-2 text-justify break-words text-gray-700 ">
            {description}
          </div>
          {version.version_description.length > 90 && (
            <button
              onClick={() => setShowFullDescription((prevState) => !prevState)}
              className="text-indigo-500 hover:text-indigo-600 underline font-semibold ml-4"
            >
              {showFullDescription ? "Less" : "More"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PendingNewVersionCard;
