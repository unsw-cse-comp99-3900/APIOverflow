import React, { useState } from 'react';
import { FaThumbsDown, FaThumbsUp } from 'react-icons/fa';

const ApiReviews: React.FC = () => {
  const [reviews, setReviews] = useState<string[]>([]);
  const [newReview, setNewReview] = useState<string>('');

  const handleReviewSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newReview.trim() !== '') {
      setReviews([...reviews, newReview]);
      setNewReview(''); // Clear the input after submission
    }
  };

  return (
    <div className="w-1/3 bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">Reviews</h2>

      {/* Review Form */}
      <form onSubmit={handleReviewSubmit} className="mb-4">
        <textarea
          value={newReview}
          onChange={(e) => setNewReview(e.target.value)}
          className="w-full h-24 p-2 border rounded-lg focus:outline-none focus:border-blue-500"
          placeholder="Write your review..."
        />
        <div className="flex items-center justify-between space-x-2 mt-2">
          <div className="flex space-x-2">
            <button
              type="button"
              className="w-10 h-10 flex items-center justify-center bg-blue-500 text-white rounded-xl"
            >
              <FaThumbsUp />
            </button>
            <button
              type="button"
              className="w-10 h-10 flex items-center justify-center bg-red-500 text-white rounded-xl"
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
      </form>

      {/* Display Reviews */}
      {reviews.length === 0 ? (
        <p className="text-gray-500">No reviews yet</p>
      ) : (
        <ul className="space-y-2">
          {reviews.map((review, index) => (
            <li
              key={index}
              className="p-3 border-b last:border-none bg-gray-50 rounded-md"
            >
              {review}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ApiReviews;
