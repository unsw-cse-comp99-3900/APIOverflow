import React, { useEffect, useState } from "react";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";
import { Rating, ReviewDetail } from "../types/miscTypes";

interface ReviewDetailModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  review: ReviewDetail;
  onSave: (reviewId: string, content: string, rating: Rating | null) => void;
}

const ReviewDetailModal: React.FC<ReviewDetailModalProps> = ({
  isOpen,
  onRequestClose,
  review,
  onSave,
}) => {
  const [content, setContent] = useState(review.comment);
  const [reviewRating, setReviewRating] = useState<Rating | null>(review.type);

  if (!isOpen) return null; // If the modal is not open, return null

  const handleSave = () => {
    if (content.trim() || reviewRating === null) {
      onSave(review.rid, content, reviewRating);
      onRequestClose();
    } else {
      alert("Review cannot be empty.");
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-3xl bg-white rounded-lg shadow-lg p-6 mx-4">
        <h2 className="text-2xl font-bold mb-4">Edit Review</h2>

        {/* Edited Content */}
        <div className="mt-6">
          <label htmlFor="content" className="block mb-2 font-semibold">Review Content:</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={review.comment}
            defaultValue={review.comment}
            className="w-full p-2 border rounded"
            rows={3}
          />
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex items-centergap-x-6 justify-between">
          <div className="flex">
            <button
              type="button"
              className={`mt-4 ring-2 ring-blue-500 w-10 h-10 flex items-center justify-center ${reviewRating === "positive"
                ? "bg-blue-500 text-white"
                : "bg-white text-blue-500"
                } rounded-xl`}
              onClick={() => {
                if (reviewRating === "positive") {
                  setReviewRating(null);
                } else {
                  setReviewRating("positive");
                }
              }}
            >
              <FaThumbsUp />
            </button>
            <button
              type="button"
              className={`mt-4 ring-2 ring-red-500  w-10 h-10 flex items-center justify-center mx-5 ${reviewRating === "negative"
                ? "bg-red-500 text-white"
                : "bg-white text-red-500"
                } rounded-xl`}
              onClick={() => {
                if (reviewRating === "negative") {
                  setReviewRating(null);
                } else {
                  setReviewRating("negative");
                }
              }}
            >
              <FaThumbsDown />
            </button>
          </div>
          <div className="flex">
            <button
              onClick={() => handleSave()} // Pass review ID and edited content
              className="flex mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mx-5"
            >
              Save
            </button>
            <button
              onClick={onRequestClose}
              className="mt-4 bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewDetailModal;
