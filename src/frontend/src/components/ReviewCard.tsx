import React, { useState } from "react";
import { Review } from "../types/miscTypes";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";

interface ReviewCardProps {
  review: Review;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review }) => {
  const bgColor50 = review.type === "positive" ? "bg-blue-50" : "bg-red-50";
  const borderColor300 = review.type === "positive" ? "border-blue-300" : "border-red-300";
  const textColor800 = review.type === "positive" ? "text-blue-800" : "text-red-800";
  const textColor500 = review.type === "positive" ? "text-blue-500" : "text-red-500";
  console.log(review);
  return (
    <div
      className={`p-3 bg-white border-2 ${borderColor300} rounded-lg`}
    >
      <div className={`flex items-center justify-between`}>
        <h2 className={`text-lg font-bold items-center justify-center ${textColor800}`}>
          {review.reviewerName}
        </h2>
        <div
          className={`pr-3 flex items-center text-lg justify-center ${textColor500} rounded-xl`}
        >
          {review.type === "positive" ? <FaThumbsUp /> : <FaThumbsDown />}
        </div>
      </div>
      <div className={`border ${borderColor300} w-full my-5`}></div>
      <div
        className={` ${bgColor50}  ${textColor800} font-semibold rounded-lg py-3 px-3`}
      >
        {review.comment}
      </div>
    </div>
  );
};

export default ReviewCard;
