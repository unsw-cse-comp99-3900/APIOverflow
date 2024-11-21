import React, { useState } from "react";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import { FaCrown, FaThumbsUp, FaThumbsDown } from "react-icons/fa";
import Tag from "./Tag";
import EditApiButton from "./EditApiButton";
import DeleteApiButton from "./DeleteApiButton";
import { PayModel } from "../types/miscTypes";
import { ServiceStatus } from "../types/apiTypes";

interface ApiGeneralInfoProps {
  apiId: string;
  iconURL: string;
  apiName: string;
  ownerName: string;
  payModel: PayModel;
  status: ServiceStatus;
  tags: string[];
  isMyApi: boolean;
  rating: string;
  isGettingApproved?: boolean;
}

const ApiGeneralInfo: React.FC<ApiGeneralInfoProps> = ({
  apiId,
  iconURL,
  apiName,
  ownerName,
  status,
  payModel,
  tags,
  isMyApi,
  rating,
  isGettingApproved,
}) => {
  const bgColor = {
    Free: "bg-blue-500",
    Freemium: "bg-purple-500",
    Premium: "bg-amber-500",
  };

  const textColor = {
    LIVE: "text-green-600",
    PENDING: "text-amber-600",
    UPDATE_PENDING: "text-amber-600",
    REJECTED: "text-red-600",
    UPDATE_REJECTED: "text-red-600",
  };

  let ratingCol = "bg-gray-500";
  let numRating = 0;
  let displayRating = rating;

  numRating = Number(rating);
  if (numRating > 0) {
    ratingCol = "bg-green-500";
  } else if (numRating < 0) {
    ratingCol = "bg-red-500";
    displayRating = String(numRating * -1);
  }

  return (
    <div className=" border-2 border-gray-100 bg-white rounded-2xl shadow-lg p-10 my-6">
      <div className="flex items-center ">
        <div className="flex flex-shrink-0 items-center">
          <img
            className="w-56 h-56 rounded-full object-cover mx-auto border-2 border-gray-300"
            src={iconURL || defaultApiIcon}
            alt="API Icon"
          />
        </div>

        <div className="ml-10 w-full">
          <div className="flex items-center">
            <h1 className="text-4xl font-bold">{apiName}</h1>
            <div
              className={`flex items-center ${bgColor[payModel]} rounded-md mx-3 px-2`}
            >
              {(payModel === "Premium" || payModel === "Freemium") && (
                <div className="flex items-center justify-center text-white rounded-md mr-2">
                  <FaCrown />
                </div>
              )}
              <span className="text-white text-lg font-medium">{payModel}</span>
            </div>

            {!isGettingApproved && (
              <div className="absolute top-24 right-8 flex space-x-2">
                <div>
                  <div
                    className={`flex items-center ${ratingCol} rounded-md mx-5 px-3`}
                  >
                    {numRating < 0 && (
                      <div className="flex items-center justify-center text-md text-white rounded-md mr-2">
                        <FaThumbsDown />
                      </div>
                    )}
                    {numRating >= 0 && (
                      <div className="flex items-center justify-center text-md text-white rounded-md mr-2">
                        <FaThumbsUp />
                      </div>
                    )}
                    <span className="text-white text-md font-medium">
                      {displayRating}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* <div className="flex justify-between my-2">
            <div className="text-gray-600">{`By: ${ownerName}`}</div>
            <div className={`font-semibold ${textColor[status]}`}>
              status: {status}
            </div>
          </div> */}

          {!isGettingApproved && (
            <div className="text-gray-600">{`By: ${ownerName}`}</div>
          )}
          <div className={`font-semibold my-2 ${textColor[status]}`}>
            status: {status}
          </div>

          <div className="border border-gray-100 w-full"></div>
          <div className="flex flex-wrap max-w-3xl mt-6 mb-5">
            {tags.map((tag, index) => (
              <Tag key={index} tag={tag} className="mr-3 mb-2" />
            ))}
          </div>
        </div>

        {/* Conditionally render buttons if api is available */}
        {isMyApi && (
          <div className="absolute top-8 right-8 flex space-x-2">
            <EditApiButton apiId={apiId} />
            <DeleteApiButton apiId={apiId} apisRoute="/profile/my-apis" />
          </div>
        )}
      </div>
    </div>
  );
};

export default ApiGeneralInfo;
