// src/pages/ReviewManagement.tsx

import React, { useState } from "react";
import ReviewCard from "../components/ReviewCard";
import ReviewModal from "../components/ReviewModal";
import { Review } from "../types/miscTypes";

// Dummy data for testing
const reviews: Review[] = [
  // {
  //   rid: "R001",
  //   reviewer: "Jane Doe",
  //   reviewerName: "hihi",
  //   service: "Service001",
  //   title: "Great Service",
  //   comment: "I had an amazing experience with this service!",
  //   type: "positive",

  // },
  //   rid: "R002",
  //   reviewer: "John Smith",
  //   reviewerName: "hihi",
  //   service: "Service002",
  //   title: "Not Satisfied",
  //   comment: "The service quality was below my expectations.",
  //   type: "negative",
  // },
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
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Reviews
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {reviews.map((review) => (
          <div key={review.rid} className="shadow-lg rounded-xl p-4 transition-transform transform hover:scale-105">
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
