import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import ReviewCard from "../components/ReviewCard";
import ReviewModal from "../components/ReviewModal";
import { fetchReviews } from "../services/apiServices";
import { Review } from "../types/miscTypes";
import { FaSort } from "react-icons/fa";

const ReviewManagement: React.FC = () => {
  const { sid } = useParams<{ sid: string }>();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [selectedReview, setSelectedReview] = useState<Review | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortType, setSortType] = useState<'best' | 'worst'>('best');

  useEffect(() => {
    if (sid) {
      loadReviews();
    }
  }, [sid, sortType]);

  const loadReviews = async () => {
    if (!sid) return;
    
    try {
      setIsLoading(true);
      setError(null);
      const fetchedReviews = await fetchReviews(sid, false, sortType);
      setReviews(fetchedReviews);
    } catch (err) {
      console.error('Error loading reviews:', err);
      setError(err instanceof Error ? err.message : 'Failed to load reviews');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSortChange = () => {
    const newSortType = sortType === 'best' ? 'worst' : 'best';
    console.log('Changing sort type to:', newSortType); 
    setSortType(newSortType);
  };

  return (
    <div className="p-6 md:p-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <h1 className="text-3xl font-bold text-blue-800">
          Reviews
        </h1>
        <div className="flex flex-col md:flex-row gap-4 w-full md:w-auto">
          <button
            onClick={handleSortChange}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 transition-colors"
          >
            <FaSort className={sortType === 'best' ? 'text-blue-600' : 'text-red-600'} />
            <span>
              {sortType === 'best' ? 'Showing Highest Rated First' : 'Showing Lowest Rated First'}
            </span>
          </button>
        </div>
      </div>

      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {reviews.map((review) => (
          <div key={review.rid} className="transform transition-all duration-200 hover:scale-[1.02]">
            <ReviewCard review={review} />
          </div>
        ))}
      </div>

      {reviews.length === 0 && !isLoading && (
        <div className="text-center py-12 text-gray-500 bg-gray-50 rounded-lg">
          No reviews found
        </div>
      )}
    </div>
  );
};

export default ReviewManagement;