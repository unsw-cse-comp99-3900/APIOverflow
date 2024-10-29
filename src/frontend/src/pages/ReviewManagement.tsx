// src/pages/ReviewManagement.tsx

import React, { useState } from "react";
import ReviewCard from "../components/ReviewCard";
import ReviewModal from "../components/ReviewModal";
import { Review } from "../types/miscTypes";

// Dummy data for testing
const reviews: Review[] = [
  {
    id: "1",
    rid: "R001",
    reviewer: "Jane Doe",
    service: "Service001",
    title: "Great Service",
    comment: "I had an amazing experience with this service!",
    type: "positive",
    status: "approved"
  },
  {
    id: "2",
    rid: "R002",
    reviewer: "John Smith",
    service: "Service002",
    title: "Not Satisfied",
    comment: "The service quality was below my expectations.",
    type: "negative",
    status: "pending"
  },
];

const ReviewManagement: React.FC = () => {
  const [selectedReview, setSelectedReview] = useState<Review | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = (review: Review) => {
    setSelectedReview(review);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedReview(null);
    setIsModalOpen(false);
  };

  const handleApprove = (reviewId: string) => {
    console.log(`Approved review with ID: ${reviewId}`);
    handleCloseModal();
  };

  const handleReject = (reviewId: string, reason: string) => {
    console.log(`Rejected review with ID: ${reviewId}, Reason: ${reason}`);
    handleCloseModal();
  };

  return (
    <div className="p-6">
      <h1 className="text-4xl font-extrabold text-center mb-8 text-blue-800 underline underline-offset-8">
        Review Management
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {reviews.map((review) => (
          <div key={review.id} className="shadow-lg rounded-xl p-4 transition-transform transform hover:scale-105">
            <ReviewCard review={review} />
            <button
              className="mt-4 bg-gradient-to-r from-blue-500 to-blue-700 text-white font-semibold py-2 px-6 rounded-full hover:from-blue-600 hover:to-blue-800 transition-all shadow-lg"
              onClick={() => handleOpenModal(review)}
            >
              Review
            </button>
          </div>
        ))}
      </div>

      {selectedReview && (
        <ReviewModal
          isOpen={isModalOpen}
          onRequestClose={handleCloseModal}
          review={selectedReview}
          onApprove={handleApprove}
          onReject={handleReject}
        />
      )}
    </div>
  );
};

export default ReviewManagement;
