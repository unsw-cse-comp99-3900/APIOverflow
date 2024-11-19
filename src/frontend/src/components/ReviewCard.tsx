import React, { useState, useEffect } from "react";
import { Review } from "../types/miscTypes";
import { FaThumbsDown, FaThumbsUp, FaEdit, FaTrash } from "react-icons/fa";

interface ReviewCardProps {
  review: Review;
}

interface Reply {
  rid: string;
  reviewer: string;
  service: string;
  comment: string;
  edited: boolean;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review }) => {
  const [isReplying, setIsReplying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [editContent, setEditContent] = useState('');
  const [error, setError] = useState('');
  const [replies, setReplies] = useState<Reply[]>([]);
  const baseUrl = process.env.REACT_APP_API_BASE_URL;

  useEffect(() => {
    fetchReplies();
  }, [review.rid]);

  const fetchReplies = async () => {
    try {
      const response = await fetch(`${baseUrl}/review/reply/get?rid=${review.rid}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch replies');
      }

      const data = await response.json();
      if (data) {
        setReplies([data]);
      }
    } catch (err) {
      console.error('Error fetching replies:', err);
    }
  };

  const handleSubmitReply = async () => {
    if (!replyContent.trim()) {
      setError('Reply cannot be empty');
      return;
    }

    try {
      const response = await fetch(`${baseUrl}/review/reply`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rid: review.rid,
          content: replyContent.trim()
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit reply');
      }

      setReplyContent('');
      setIsReplying(false);
      setError('');
      fetchReplies();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit reply');
    }
  };

  const handleEditReply = async (rid: string) => {
    if (!editContent.trim()) {
      setError('Reply cannot be empty');
      return;
    }

    try {
      const response = await fetch(`${baseUrl}/review/reply/edit`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rid: rid,
          content: editContent.trim()
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to edit reply');
      }

      setIsEditing(false);
      setEditContent('');
      fetchReplies();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to edit reply');
    }
  };

  const handleDeleteReply = async (rid: string) => {
    if (!window.confirm('Are you sure you want to delete this reply?')) {
      return;
    }

    try {
      const response = await fetch(`${baseUrl}/review/reply/delete?rid=${rid}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete reply');
      }

      fetchReplies();
    } catch (err) {
      console.error('Delete error:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete reply');
    }
  };

  return (
    <div className={`p-3 bg-white border-2 ${review.type === "positive" ? "border-blue-300" : "border-red-300"} rounded-lg`}>
      <div className={`flex items-center justify-between`}>
        <h2 className={`text-lg font-bold ${review.type === "positive" ? "text-blue-800" : "text-red-800"}`}>
          {review.reviewerName || 'ReviewerNamePlaceholder'}
        </h2>
        <div className={`pr-3 flex items-center text-lg ${review.type === "positive" ? "text-blue-500" : "text-red-500"} rounded-xl`}>
          {review.type === "positive" ? <FaThumbsUp /> : <FaThumbsDown />}
        </div>
      </div>
      
      <div className={`border ${review.type === "positive" ? "border-blue-300" : "border-red-300"} w-full my-5`}></div>
      
      <div className={`${review.type === "positive" ? "bg-blue-50 text-blue-800" : "bg-red-50 text-red-800"} font-semibold rounded-lg py-3 px-3`}>
        {review.comment}
      </div>

      {/* Display Replies */}
      {replies.length > 0 && (
        <div className="mt-4 space-y-2">
          {replies.map((reply, index) => (
            <div key={index} className="ml-6 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-800 font-medium">Creator</span>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setIsEditing(true);
                      setEditContent(reply.comment);
                    }}
                    className="text-blue-600 hover:text-blue-700"
                  >
                    <FaEdit size={16} />
                  </button>
                  <button
                    onClick={() => handleDeleteReply(reply.rid)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <FaTrash size={16} />
                  </button>
                </div>
              </div>
              
              {isEditing ? (
                <div>
                  <textarea
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none mb-2"
                    rows={3}
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => {
                        setIsEditing(false);
                        setEditContent('');
                      }}
                      className="px-3 py-1 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => handleEditReply(reply.rid)}
                      className="px-3 py-1 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                    >
                      Save
                    </button>
                  </div>
                </div>
              ) : (
                <p className="text-gray-700">{reply.comment}</p>
              )}
              {reply.edited && !isEditing && (
                <span className="text-xs text-gray-500 italic mt-1">
                  (edited)
                </span>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Reply Form */}
      {isReplying && (
        <div className="mt-4">
          <textarea
            value={replyContent}
            onChange={(e) => setReplyContent(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
            placeholder="Write your reply..."
            rows={3}
          />
          {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
          <div className="flex justify-end space-x-2 mt-2">
            <button
              onClick={() => {
                setIsReplying(false);
                setReplyContent('');
                setError('');
              }}
              className="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmitReply}
              className="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
            >
              Submit Reply
            </button>
          </div>
        </div>
      )}

      {!isReplying && !replies.length && (
        <button
          onClick={() => setIsReplying(true)}
          className="mt-3 text-blue-600 hover:text-blue-700"
        >
          Reply
        </button>
      )}
    </div>
  );
};

export default ReviewCard;