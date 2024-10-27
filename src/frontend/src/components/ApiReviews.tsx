import React, { useState } from 'react';

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
        <button
          type="submit"
          className="mt-2 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          Submit Review
        </button>
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
