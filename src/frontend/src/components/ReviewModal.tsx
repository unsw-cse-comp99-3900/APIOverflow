import React, { useState } from "react";
import { FaThumbsDown, FaThumbsUp } from "react-icons/fa";
import { Review } from "../types/miscTypes";

interface ReviewModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  review: Review;
  onApprove: (reviewId: string) => void;
  onReject: (reviewId: string, reason: string) => void;
}

const ReviewModal: React.FC<ReviewModalProps> = ({
  isOpen,
  onRequestClose,
  review,
  onApprove,
  onReject,
}) => {
  const [reason, setReason] = useState("");

  if (!isOpen) return null; // If the modal is not open, return null

  const handleReject = () => {
    if (reason.trim()) {
      onReject(review.rid, reason); // Pass review ID and rejection reason
      onRequestClose();
    } else {
      alert("Please provide a reason for rejection.");
    }
  };

  const bgColor50 = review.type === "positive" ? "bg-blue-50" : "bg-red-50";
  const borderColor300 = review.type === "positive" ? "border-blue-300" : "border-red-300";
  const textColor800 = review.type === "positive" ? "text-blue-800" : "text-red-800";
  const textColor500 = review.type === "positive" ? "text-blue-500" : "text-red-500";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-3xl bg-white rounded-lg shadow-lg p-6 mx-4">
        <h2 className="text-2xl font-bold mb-4">Review Details</h2>

        <div className={`p-3 bg-white border-2 ${borderColor300} rounded-lg`}>
          <div className="flex items-center justify-between">
            <h2 className={`text-lg font-bold ${textColor800}`}>{review.reviewer}</h2>
            <div className={`pr-3 flex items-center text-lg ${textColor500} rounded-xl`}>
              {review.type === "positive" ? <FaThumbsUp /> : <FaThumbsDown />}
            </div>
          </div>
          <div className={`border ${borderColor300} w-full my-5`}></div>
          <div className={`${bgColor50} ${textColor800} font-semibold rounded-lg py-3 px-3`}>
            {review.comment}
          </div>
        </div>

        {/* Reason for rejection */}
        <div className="mt-6">
          <label htmlFor="reason" className="block mb-2 font-semibold">Reason for Rejection:</label>
          <textarea
            id="reason"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Provide a reason for rejection..."
            className="w-full p-2 border rounded"
            rows={3}
          />
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4 mt-6">
          <button
            onClick={() => onApprove(review.rid)} // Pass review ID for approval
            className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
          >
            Approve
          </button>
          <button
            onClick={handleReject} // Handle rejection with ID and reason
            className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
          >
            Reject
          </button>
          <button
            onClick={onRequestClose}
            className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReviewModal;
