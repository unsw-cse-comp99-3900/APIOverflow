import React from "react";
import { Review } from "../types/miscTypes";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";

interface ReviewCardProps {
  review: Review;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review }) => {
  const themeColor = review.type === "positive" ? "blue" : "red";

  return (
    <div
      className={`p-3  bg-${themeColor}-100 border-2 border-${themeColor}-300 rounded-lg`}
    >
      <div className={`flex items-center justify-between`}>
        <h2 className={`text-lg font-bold items-center justify-center text-${themeColor}-800`}>
          ReviewerNamePlaceholder
        </h2>
        <div
          className={`pr-3 flex items-center text-lg justify-center text-${themeColor}-500 rounded-xl`}
        >
          {review.type === "positive" ? <FaThumbsUp /> : <FaThumbsDown />}
        </div>
      </div>
      <div className={`border border-${themeColor}-300 w-full my-5`}></div>
      <div
        className={` bg-${themeColor}-50  text-${themeColor}-800 font-semibold rounded-lg py-3 px-3`}
      >
        {review.comment}
      </div>
    </div>
  );
};

export default ReviewCard;
