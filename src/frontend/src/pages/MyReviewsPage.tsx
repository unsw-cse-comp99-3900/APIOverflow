import { PhotoIcon } from "@heroicons/react/24/solid";
import React, { useState, useEffect } from 'react'
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { UserProfile } from "../types/userTypes";
import { ReviewDetail } from "../types/miscTypes";
import ReviewCard from "../components/ReviewCard";
import ReviewModal from "../components/ReviewModal";
import ReviewDetailModal from "../components/ReviewDetailModal";
import { Review } from "../types/miscTypes";
import ReviewCardHeader from "../components/ReviewCardHeader";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";

// Dummy data for testing
const reviews: ReviewDetail[] = [
    {
      id: "1",
      rid: "R001",
      reviewer: "Jane Doe",
      reviewerName: "hihi",
      service: "Service001",
      title: "Great Service",
      comment: "I had an amazing experience with this service!",
      type: "positive",
      status: "approved",
      upvotes: "5",
      downvotes: "20",
    },
    {
      id: "2",
      rid: "R002",
      reviewer: "John Smith",
      reviewerName: "hihi",
      service: "Service002",
      title: "Not Satisfied",
      comment: "The service quality was below my expectations.",
      type: "negative",
      status: "pending",
      upvotes: "20",
      downvotes: "5",
    },
  ];

const MyReviewsPage = () => {
  const navigate = useNavigate();
  const [selectedReview, setSelectedReview] = useState<ReviewDetail | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [numRating, setNumRating] = useState<number>(0);

  const handleOpenModal = (review: ReviewDetail) => {
    setSelectedReview(review);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedReview(null);
    setIsModalOpen(false);
  };

  const handleEdit = (reviewId: string) => {
    console.log(`Approved review with ID: ${reviewId}`);
    handleCloseModal();
  };

  const handleDelete = (reviewId: string, reason: string) => {
    console.log(`Rejected review with ID: ${reviewId}, Reason: ${reason}`);
    handleCloseModal();
  };

  return (
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        My Reviews
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {reviews.map((review) => ( 
            <div key={review.id} className="shadow-lg rounded-xl p-4 transition-transform transform hover:scale-105">
                <ReviewCardHeader reviewID={review.id} service={review.service} />
                <div className="border border-gray-100 mx-4 mb-5"></div>
                <ReviewCard review={review} />
                <div className="grid grid-cols-3 gap-50">
                    <div>
                      <button
                      className="mt-4 bg-gradient-to-r from-blue-500 to-blue-700 text-white font-semibold py-2 px-6 rounded-full hover:from-blue-600 hover:to-blue-800 transition-all shadow-lg"
                      onClick={() => handleOpenModal(review)}
                      >
                      Edit Review
                      </button>
                    </div>
                    <div className="grid grid-cols-2 gap=0">
                      <div className="mt-4 flex items-center bg-green-500 py-2 px-6 rounded-tl-full rounded-bl-full">
                        <div className="flex items-center justify-center text-md text-white rounded-md mr-2">
                          <FaThumbsUp />
                        </div>
                        <span className="text-white text-md font-medium">
                          {review.upvotes}
                        </span>
                      </div>
                      <div className="justify-end mt-4 flex items-center bg-red-500 py-2 px-6 rounded-tr-full rounded-br-full">
                        <span className="text-white text-md font-medium">
                          {review.downvotes}
                        </span>
                        <div className="flex items-center justify-center text-md text-white rounded-md mt-1 ml-2">
                          <FaThumbsDown />
                        </div>
                      </div>
                    </div>
                    <div>
                      <button
                        className="absolute right-4 mt-4 bg-red-500 text-white font-semibold py-2 px-6 rounded-full hover:from-red-600 hover:to-red-800 transition-all shadow-lg"
                        onClick={() => handleOpenModal(review)}
                        >
                        Delete Review
                      </button>
                    </div>
                </div>
            </div>
        ))}
      </div>

      {selectedReview && (
        <ReviewDetailModal
          isOpen={isModalOpen}
          onRequestClose={handleCloseModal}
          review={selectedReview}
          onSave={handleDelete}
        />
      )}
    </div>
  );
}

export default MyReviewsPage;