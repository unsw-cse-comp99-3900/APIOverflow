import React, { useEffect, useState } from "react";
import { apiGetIcon } from "../services/apiServices";
import { PendingNewService } from "../types/apiTypes";
import { FaCrown } from "react-icons/fa";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import Tag from "./Tag";

interface PendingNewServiceCardProps {
  service: PendingNewService;
  setCurrentPendingService: React.Dispatch<React.SetStateAction<PendingNewService | null>>;
}

const PendingNewServiceCard: React.FC<PendingNewServiceCardProps> = ({
  service,
  setCurrentPendingService,
}) => {
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [iconURL, setIconURL] = useState<string>("");

  useEffect(() => {
    const fetchIcon = async () => {
      try {
        const iconURL = await apiGetIcon(service.id);
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

  let description = service.description;

  if (!showFullDescription && description.length > 90) {
    description = description.substring(0, 90) + "...";
  }

  return (
    <div
      className="bg-white rounded-xl shadow-md relative transition-transform transform hover:scale-105 my-4 hover:cursor-pointer"
      onClick={() => setCurrentPendingService(service)}
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
                <h3 className="text-xl font-bold my-2">{service.name}</h3>
                <div
                  className={`flex items-center ${
                    bgColor[service.pay_model]
                  } rounded-md mx-3 px-2`}
                >
                  {(service.pay_model === "Premium" ||
                    service.pay_model === "Freemium") && (
                    <div className="flex items-center justify-center text-md text-white rounded-md mr-2">
                      <FaCrown />
                    </div>
                  )}

                  <span className="text-white text-md font-medium">
                    {service.pay_model}
                  </span>
                </div>
              </div>
              <div className="flex flex-wrap mt-2 mb-3">
                {service.tags.map((tag) => (
                  <Tag key={tag} tag={tag} className="mr-3 mb-2" />
                ))}
              </div>
            </div>
          </div>
          <div className="border border-gray-100 mx-4 mb-5"></div>

          <div className="mx-4 mb-2 text-justify break-words text-gray-700 ">
            {description}
          </div>
          {service.description.length > 90 && (
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

export default PendingNewServiceCard;
