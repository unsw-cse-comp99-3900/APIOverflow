import React, { useEffect, useState } from "react";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";
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

  useEffect(() => {
    const fetchApi = async () => {
      try {
        const data = await apiGetReviews(sid);
        setReviews(data);
      } catch (error) {
        console.log("Error fetching data", error);
        if (error instanceof Error) {
          setError(error.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchApi();
  }, []);

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
      await apiAddReview({
        sid,
        rating: reviewRating,
        comment: reviewComment,
        title: "reviewTitle",
      });
    } catch (error) {
      if (error instanceof Error) {
        setWarning(error.message);
      }
    }
    const data = await apiGetReviews(sid);
    setReviewComment("");
    setReviews(data);
  };

  return (
    <div className="w-1/3 bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">Reviews</h2>

      {/* Review Form */}
      <form onSubmit={handleReviewSubmit} className="mb-4">
        <textarea
          value={reviewComment}
          onChange={(e) => setReviewComment(e.target.value)}
          className="w-full h-24 p-2 border rounded-lg focus:outline-none focus:border-blue-500"
          placeholder="Write your review..."
        />
        <div className="flex items-center justify-between space-x-2 mt-2">
          <div className="flex space-x-2">
            <button
              type="button"
              className={`ring-2 ring-blue-500 w-10 h-10 flex items-center justify-center ${
                reviewRating === "positive"
                  ? "bg-blue-500 text-white"
                  : "bg-white text-blue-500"
              } rounded-xl`}
              onClick={() => {
                if (reviewRating === "positive") {
                  setReviewRating(null);
                } else {
                  setReviewRating("positive");
                }
                setWarning("");
              }}
            >
              <FaThumbsUp />
            </button>
            <button
              type="button"
              className={`ring-2 ring-red-500  w-10 h-10 flex items-center justify-center ${
                reviewRating === "negative"
                  ? "bg-red-500 text-white"
                  : "bg-white text-red-500"
              } rounded-xl`}
              onClick={() => {
                if (reviewRating === "negative") {
                  setReviewRating(null);
                } else {
                  setReviewRating("negative");
                }
                setWarning("");
              }}
            >
              <FaThumbsDown />
            </button>
          </div>

          <button
            type="button"
            onClick={handleReviewSubmit}
            className="px-4 py-2 bg-blue-800 text-white rounded-lg font-semibold"
          >
            Submit Review
          </button>
        </div>
        {warning && <p className="text-red-500 text-sm my-2">{warning}</p>}
      </form>

      <div className="border border-gray-100 w-full my-5"></div>

      {/* Display Reviews */}
      {reviews.length === 0 ? (
        <p className="text-gray-500">No reviews yet</p>
      ) : (
        <ul className="space-y-4">
          {reviews.map((review, index) => (
            <li key={index}>
              <ReviewCard review={review} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ApiReviews;
