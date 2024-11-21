// src/components/ApiReviews.tsx
import React, { useEffect, useState } from "react";
import { FaThumbsDown, FaThumbsUp, FaChevronDown } from "react-icons/fa"; // Add FaChevronDown import
import { Rating, Review } from "../types/miscTypes";
import { apiAddReview, apiGetReviews } from "../services/apiServices";
import ReviewCard from "./ReviewCard";

interface ApiReviewsProps {
  sid: string;
}

const ApiReviews: React.FC<ApiReviewsProps> = ({ sid }) => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [reviewRating, setReviewRating] = useState<Rating | null>(null);
  const [reviewComment, setReviewComment] = useState<string>("");
  const [warning, setWarning] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"" | "best" | "worst">("");

  useEffect(() => {
    fetchApi();
  }, [filter, sid]);

  const fetchApi = async () => {
    try {
      setLoading(true);
      const data = await apiGetReviews(sid, filter);
      setReviews(data);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewRating) {
      setWarning("Please select a rating");
      return;
    }
    if (reviewComment.trim() === "") {
      setWarning("Please enter a review comment");
      return;
    }
    try {
      await apiAddReview(sid, reviewRating, "reviewTitle", reviewComment);
      setReviewComment("");
      setReviewRating(null);
      setWarning("");
      await fetchApi();
    } catch (error) {
      if (error instanceof Error && error.message === "Unauthorized") {
        setWarning("You need to login to submit a review");
      }
      else if (error instanceof Error) {
        setWarning(error.message);
      }
    }
  };

  return (
    <div className="w-1/3 bg-white rounded-2xl shadow-lg p-6">
      {/* Header with Sort Control */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Reviews</h2>
        <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as "" | "best" | "worst")}
            className="px-3 py-2 pr-8 border rounded-lg focus:outline-none focus:border-blue-500 appearance-none cursor-pointer bg-white"
          >
            <option value="">Default Order</option>
            <option value="best">Highest Rated</option>
            <option value="worst">Lowest Rated</option>
          </select>
          <div className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2">
            <FaChevronDown 
              className={`transition-transform duration-200 ${
                filter ? 'text-blue-600' : 'text-gray-400'
              }`}
            />
          </div>
        </div>

      {/* Review Form - Moved to top */}
      <form onSubmit={handleReviewSubmit} className="mb-6">
        <textarea
          value={reviewComment}
          onChange={(e) => setReviewComment(e.target.value)}
          className="w-full h-24 p-2 border rounded-lg focus:outline-none focus:border-blue-500"
          placeholder="Write your review..."
        />
        <div className="flex items-center justify-between space-x-2 mt-2">
          {/* Rating Buttons */}
          <div className="flex space-x-2">
            <button
              type="button"
              className={`ring-2 ring-blue-500 w-10 h-10 flex items-center justify-center ${
                reviewRating === "positive"
                  ? "bg-blue-500 text-white"
                  : "bg-white text-blue-500"
              } rounded-xl`}
              onClick={() => {
                setReviewRating((prev) =>
                  prev === "positive" ? null : "positive"
                );
                setWarning("");
              }}
            >
              <FaThumbsUp />
            </button>
            <button
              type="button"
              className={`ring-2 ring-red-500 w-10 h-10 flex items-center justify-center ${
                reviewRating === "negative"
                  ? "bg-red-500 text-white"
                  : "bg-white text-red-500"
              } rounded-xl`}
              onClick={() => {
                setReviewRating((prev) =>
                  prev === "negative" ? null : "negative"
                );
                setWarning("");
              }}
            >
              <FaThumbsDown />
            </button>
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-800 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Submit Review
          </button>
        </div>
        {warning && <p className="text-red-500 text-sm mt-2">{warning}</p>}
      </form>

      <div className="border-t border-gray-200 mb-4"></div>

      {/* Scrollable Reviews Section */}
      <div className="max-h-[500px] overflow-y-auto">
        {loading ? (
          <div className="flex justify-center py-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        ) : reviews.length === 0 ? (
          <p className="text-gray-500 text-center py-4">No reviews yet</p>
        ) : (
          <div className="space-y-4 pr-2">
            {reviews.map((review) => (
              <div key={review.rid}>
                <ReviewCard review={review} />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ApiReviews;
