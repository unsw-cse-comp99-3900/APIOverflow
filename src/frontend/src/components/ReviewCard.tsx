import React, { useState } from "react";
import { Review } from "../types/miscTypes";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";
import { submitReviewReply } from "../services/apiServices";

interface ReviewCardProps {
  review: Review;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review }) => {
  const [isReplying, setIsReplying] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [error, setError] = useState('');

  const bgColor50 = review.type === "positive" ? "bg-blue-50" : "bg-red-50";
  const borderColor300 = review.type === "positive" ? "border-blue-300" : "border-red-300";
  const textColor800 = review.type === "positive" ? "text-blue-800" : "text-red-800";
  const textColor500 = review.type === "positive" ? "text-blue-500" : "text-red-500";

  const handleSubmitReply = async () => {
    if (!replyContent.trim()) {
      setError('Reply cannot be empty');
      return;
    }

    try {
      console.log('Submitting reply:', {
        reviewId: review.id,
        content: replyContent.trim()
      });
      
      await submitReviewReply(review.id, replyContent.trim());
      setReplyContent('');
      setIsReplying(false);
      setError('');
    } catch (err) {
      console.error('Reply submission error:', err);
      setError((err as Error).message || 'Failed to submit reply');
    }
  };

  return (
    <div className={`p-3 bg-white border-2 ${borderColor300} rounded-lg`}>
      <div className={`flex items-center justify-between`}>
        <h2 className={`text-lg font-bold items-center justify-center ${textColor800}`}>
          {review.reviewer || 'ReviewerNamePlaceholder'}
        </h2>
        <div className={`pr-3 flex items-center text-lg justify-center ${textColor500} rounded-xl`}>
          {review.type === "positive" ? <FaThumbsUp /> : <FaThumbsDown />}
        </div>
      </div>
      
      <div className={`border ${borderColor300} w-full my-5`}></div>
      
      <div className={`${bgColor50} ${textColor800} font-semibold rounded-lg py-3 px-3 mb-4`}>
        {review.comment}
      </div>

      {/* Reply Section */}
      {isReplying ? (
        <div className="mt-2">
          <textarea
            value={replyContent}
            onChange={(e) => setReplyContent(e.target.value)}
            className="w-full p-2 bg-gray-900 border border-gray-700 rounded text-white"
            placeholder="Write your reply..."
            rows={3}
          />
          {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
          <div className="flex justify-end space-x-2 mt-2">
            <button
              onClick={() => {
                setIsReplying(false);
                setError('');
                setReplyContent('');
              }}
              className="px-4 py-1 text-gray-300 bg-gray-800 rounded hover:bg-gray-700"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmitReply}
              className="px-4 py-1 text-white bg-blue-600 rounded hover:bg-blue-700"
            >
              Submit Reply
            </button>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsReplying(true)}
          className="mt-2 text-blue-500 hover:text-blue-600"
        >
          Reply
        </button>
      )}
    </div>
  );
};

export default ReviewCard;