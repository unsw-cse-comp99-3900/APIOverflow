import React, { useEffect, useState } from "react";
import { Review } from "../types/miscTypes";
import { FaArrowDown, FaArrowUp, FaThumbsDown, FaThumbsUp } from "react-icons/fa";
import { userDownvoteReview, userRemoveVote, userUpvoteReview } from "../services/apiServices";

interface ReviewCardProps {
  review: Review;
}

interface Reply {
  rid: string;
  reviewer: string;
  service: string;
  comment: string;
  edited: boolean;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review }) => {
  const bgColor50 = review.type === "positive" ? "bg-blue-50" : "bg-red-50";
  const borderColor300 = review.type === "positive" ? "border-blue-300" : "border-red-300";
  const textColor800 = review.type === "positive" ? "text-blue-800" : "text-red-800";
  const textColor500 = review.type === "positive" ? "text-blue-500" : "text-red-500";

  const [voted, setVoted] = useState<string>(review.voted);
  const [voteTotal, setVoteTotal] = useState<number>(Number(review.upvotes) - Number(review.downvotes));
  
  const reviewUpvote = async () => {
    try {
      let status;
      
      if (voted === "up") { 
        setVoted("");
        await userRemoveVote(review.rid);
        setVoteTotal(voteTotal - 1);
      } else {
        let total = 1;
        if (voted === "down") {
          await userRemoveVote(review.rid);
          total += 1
        } 
        status = await userUpvoteReview(review.rid);
        if (status) {
          setVoted("up")
          setVoteTotal(voteTotal + total);
        }
      }
    } catch (error) {
      console.log(error);
    }
  };

  const reviewDownvote = async () => {
    try {
      let status;

      if (voted === "down") {
        setVoted("");
        await userRemoveVote(review.rid);
        setVoteTotal(voteTotal + 1);
      } else {
        let total = 1;
        if (voted === "up") {
          await userRemoveVote(review.rid);
          total += 1;
        } 
        status = await userDownvoteReview(review.rid);
        if (status) {
          setVoted("down")
          setVoteTotal(voteTotal - total);
        }
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className={`p-3 bg-white border-2 ${review.type === "positive" ? "border-blue-300" : "border-red-300"} rounded-lg`}>
      <div className={`flex items-center justify-between`}>
        <h2 className={`text-lg font-bold ${review.type === "positive" ? "text-blue-800" : "text-red-800"}`}>
          {review.reviewerName || 'ReviewerNamePlaceholder'}
        </h2>
        <div className={`pr-3 flex items-center text-lg ${review.type === "positive" ? "text-blue-500" : "text-red-500"} rounded-xl`}>
          {review.type === "positive" ? <FaThumbsUp /> : <FaThumbsDown />}
        </div>
      </div>
      
      <div className={`border ${review.type === "positive" ? "border-blue-300" : "border-red-300"} w-full my-5`}></div>
      
      <div className={`${review.type === "positive" ? "bg-blue-50 text-blue-800" : "bg-red-50 text-red-800"} font-semibold rounded-lg py-3 px-3`}>
        {review.comment}
      </div>
      <div className={`flex items-center justify-between`}>
        <div className="grid grid-cols-3 justify-items-center">
          <div className="flex">
            <button
              type="button"
              className={`mt-4 w-4 h-4 flex items-center justify-center ${voted === "up"
                ? "text-orange-400"
                : "text-black"
                }`}
              onClick={async () => {
                await reviewUpvote()
              }}
            >
              <FaArrowUp />
            </button>
          </div>
          <div className="flex mt-3 mx-2 font-semibold text-black">
            {voteTotal}
          </div>
          <div className="flex">
            <button
              type="button"
              className={`mt-4 w-4 h-4 flex items-center justify-center ${voted === "down"
                ? "text-orange-400"
                : "text-black"
                }`}
              onClick={async () => {
                await reviewDownvote()}
              }
            >
              <FaArrowDown />
            </button>
          </div>
        </div>
        <div className="text-right mt-2 text-gray-500">
          {`${review.edited === true 
            ? `Edited on ${review.e_timestamp}`
            : `Posted on ${review.timestamp}`
          }`}
        </div>
      </div>

    </div>
  );
};

export default ReviewCard;