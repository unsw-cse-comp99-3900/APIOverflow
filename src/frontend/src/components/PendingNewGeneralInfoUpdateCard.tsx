import React, { useEffect, useState } from "react";
import { apiGetIcon } from "../services/apiServices";
import { PendingGeneralInfo } from "../types/apiTypes";
import { FaCrown } from "react-icons/fa";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import Tag from "./Tag";

interface PendingNewGeneralInfoUpdateCardProps {
  generalInfoUpdate: PendingGeneralInfo;
  setCurrentPendingGeneralInfoUpdate: React.Dispatch<React.SetStateAction<PendingGeneralInfo | null>>;
}

const PendingNewGeneralInfoUpdateCard: React.FC<PendingNewGeneralInfoUpdateCardProps> = ({
  generalInfoUpdate,
  setCurrentPendingGeneralInfoUpdate,
}) => {
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [iconURL, setIconURL] = useState<string>("");

  useEffect(() => {
    const fetchIcon = async () => {
      try {
        const iconURL = await apiGetIcon(generalInfoUpdate.id);
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

  const bgColor = {
    Free: "bg-blue-500",
    Freemium: "bg-purple-500",
    Premium: "bg-amber-500",
  };

  let description = generalInfoUpdate.description;

  if (!showFullDescription && description.length > 90) {
    description = description.substring(0, 90) + "...";
  }

  return (
    <div
      className="bg-white rounded-xl shadow-md relative transition-transform transform hover:scale-105 my-4 hover:cursor-pointer"
      onClick={() => setCurrentPendingGeneralInfoUpdate(generalInfoUpdate)}
    >
      <div className="p-4">
        <div className="pb-16">
          <div className="flex items-start mb-2">
            <img
              src={iconURL || defaultApiIcon}
              alt="API Icon"
              className="w-20 h-20 ml-4 mr-4 mt-2 rounded-full object-cover border-2 border-gray-300"
            />

            <div>
              <div className="flex items-center">
                <h3 className="text-xl font-bold my-2">{generalInfoUpdate.name}</h3>
                <div
                  className={`flex items-center ${
                    bgColor[generalInfoUpdate.pay_model]
                  } rounded-md mx-3 px-2`}
                >
                  {(generalInfoUpdate.pay_model === "Premium" ||
                    generalInfoUpdate.pay_model === "Freemium") && (
                    <div className="flex items-center justify-center text-md text-white rounded-md mr-2">
                      <FaCrown />
                    </div>
                  )}

                  <span className="text-white text-md font-medium">
                    {generalInfoUpdate.pay_model}
                  </span>
                </div>
              </div>
              <div className="flex flex-wrap mt-2 mb-3">
                {generalInfoUpdate.tags.map((tag) => (
                  <Tag key={tag} tag={tag} className="mr-3 mb-2" />
                ))}
              </div>
            </div>
          </div>
          <div className="border border-gray-100 mx-4 mb-2"></div>

          <h1 className="text-lg font-semibold text-blue-800 ml-4 mb-2">Description</h1>

          <div className="mx-4 mb-2 text-justify break-words text-gray-700 ">
            {description}
          </div>
          {generalInfoUpdate.description.length > 90 && (
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

export default PendingNewGeneralInfoUpdateCard;
