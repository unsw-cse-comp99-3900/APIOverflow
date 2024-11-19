import React, { useState, useEffect } from "react";
import { Review } from "../types/miscTypes";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";
import { getApi, apiGetIcon } from "../services/apiServices";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";

interface ReviewCardHeaderProps {
  reviewID: string;
  service: string;
}

const ReviewCardHeader: React.FC<ReviewCardHeaderProps> = ({ reviewID, service }) => {

  const [serviceName, setServiceName] = useState<string>("Placeholder");
  const [owner, setOwner] = useState<string>("User 1");
  const [iconURL, setIconURL] = useState<string>("");

  useEffect(() => {
       
    const fetchService = async (sid: string) => {
      try {
        const service = await getApi(sid);
        setServiceName(service.name);
        setOwner(service.owner.displayName);
      } catch (error) {
        console.log(error);
      }
    };

    const fetchIcon = async (sid: string) => {
      try {
        const iconURL = await apiGetIcon(sid);
        setIconURL(iconURL);
      } catch (error) {
        console.log(error);
      }
    };
    fetchService(service);
    fetchIcon(service);
    // Cleanup the object URL to avoid memory leaks
    return () => {
      if (iconURL) {
        URL.revokeObjectURL(iconURL);
      }
    };
  }, []);

  return (
          <div className="flex items-start mb-2">
            <img
              src={iconURL || defaultApiIcon}
              alt="API Icon"
              className="w-20 h-20 ml-4 mr-4 mt-2 rounded-full object-cover border-2 border-gray-300"
            />

            <div>
              <div className="flex items-center">
                <h3 className="text-xl font-bold my-2">{serviceName}</h3>
              </div>
              <div className="text-gray-600">{`By: ${owner}`}</div>
            </div>
          </div>
  );
};

export default ReviewCardHeader;
