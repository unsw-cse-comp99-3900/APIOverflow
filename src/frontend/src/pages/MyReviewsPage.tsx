import { PhotoIcon } from "@heroicons/react/24/solid";
import React, { useState, useEffect } from 'react'
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { UserProfile } from "../types/userTypes";
import { Rating, ReviewDetail } from "../types/miscTypes";
import ReviewCard from "../components/ReviewCard";
import ReviewModal from "../components/ReviewModal";
import ReviewDetailModal from "../components/ReviewDetailModal";
import { Review } from "../types/miscTypes";
import ReviewCardHeader from "../components/ReviewCardHeader";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";
import { apiGetReviews, userDeleteReview, userEditReview, userGetReviews } from "../services/apiServices";
import ReviewDetailCard from "../components/ReviewDetailCard";

const MyReviewsPage = () => {
  const navigate = useNavigate();
  const [selectedReview, setSelectedReview] = useState<ReviewDetail | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [numRating, setNumRating] = useState<number>(0);
  const [reviews, setReviews] = useState<ReviewDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [reload, setReload] = useState(true);

  useEffect (() => {

    const fetchReviews = async () => {
      
      if (!reload) {return};
      
      try {
        const data = await userGetReviews();
        setReviews(data);
  
      } catch(error) {
        console.log(error);
      }
      setLoading(false);
      setReload(false);
    }
    fetchReviews();
  }, [reload]);

  const handleOpenModal = (review: ReviewDetail) => {
    setSelectedReview(review);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedReview(null);
    setIsModalOpen(false);
    setReload(true);
  };

  const handleEdit = async (reviewId: string, content: string, rating: Rating | null) => {
    await userEditReview(reviewId, rating, content); 
    handleCloseModal();
    setReload(true);
  };

  const handleDelete = async (reviewId: string) => {
    await userDeleteReview(reviewId);
    setReload(true);
  };

  return (
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        My Reviews
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {reviews.map((review) => ( 
            <div key={review.rid} className="shadow-lg rounded-xl p-4 transition-transform transform hover:scale-105">
                <ReviewCardHeader reviewID={review.rid} service={review.service} />
                <div className="border border-gray-100 mx-4 mb-5"></div>
                <ReviewDetailCard review={review} />
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
                        onClick={() => handleDelete(review.rid)}
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
          onSave={handleEdit}
        />
      )}
    </div>
  );
}

export default MyReviewsPage;