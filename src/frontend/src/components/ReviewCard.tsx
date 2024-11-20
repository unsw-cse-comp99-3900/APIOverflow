import React, { useEffect, useState } from "react";
import { Review } from "../types/miscTypes";
import { FaArrowDown, FaArrowUp, FaEdit, FaThumbsDown, FaThumbsUp, FaTrash } from "react-icons/fa";
import { apiGetOwner, userDownvoteReview, userGetId, userRemoveVote, userUpvoteReview } from "../services/apiServices";

interface ReviewCardProps {
  review: Review;
}

interface Reply {
  rid: string;
  reviewer: string;
  service: string;
  comment: string;
  edited: boolean;
  timestamp: string;
  e_timestamp: string;
}

const ReviewCard: React.FC<ReviewCardProps> = ({ review }) => {
  const bgColor50 = review.type === "positive" ? "bg-blue-50" : "bg-red-50";
  const borderColor300 = review.type === "positive" ? "border-blue-300" : "border-red-300";
  const textColor800 = review.type === "positive" ? "text-blue-800" : "text-red-800";
  const textColor500 = review.type === "positive" ? "text-blue-500" : "text-red-500";

  const [voted, setVoted] = useState<string>(review.voted);
  const [voteTotal, setVoteTotal] = useState<number>(Number(review.upvotes) - Number(review.downvotes));
  const [isReplying, setIsReplying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [editContent, setEditContent] = useState('');
  const [error, setError] = useState('');
  const [replies, setReplies] = useState<Reply[]>([]);
  const [visitor, setVisitor] = useState<string>('');
  const [owner, setOwner] = useState<string>('-1');
  const [refetch, setRefetch] = useState<boolean>(true);
  const baseUrl = process.env.REACT_APP_API_BASE_URL;

  useEffect(() => {

    if (!refetch) {
      return;
    }
    setRefetch(false);
    
    const getVisitor = async () => {
      const v_id = await userGetId();
      setVisitor(v_id);
    };

    const getOwner = async () => {
      const owner_id = await apiGetOwner(review.service);
      setOwner(owner_id);
    };
    fetchReplies();
    getVisitor();
    getOwner();
  }, [review.rid]);

  const reviewUpvote = async () => {
    try {
      let status;

      if (voted === "up") {
        setVoted("");
        await userRemoveVote(review.rid);
        setVoteTotal(voteTotal - 1);
      } else {
        let total = 1;
        if (voted === "down") {
          await userRemoveVote(review.rid);
          total += 1
        }
        status = await userUpvoteReview(review.rid);
        if (status) {
          setVoted("up")
          setVoteTotal(voteTotal + total);
        }
      }
    } catch (error) {
      console.log(error);
    }
  };

  const reviewDownvote = async () => {
    try {
      let status;

      if (voted === "down") {
        setVoted("");
        await userRemoveVote(review.rid);
        setVoteTotal(voteTotal + 1);
      } else {
        let total = 1;
        if (voted === "up") {
          await userRemoveVote(review.rid);
          total += 1;
        }
        status = await userDownvoteReview(review.rid);
        if (status) {
          setVoted("down")
          setVoteTotal(voteTotal - total);
        }
      }
    } catch (error) {
      console.log(error);
    }
  };

  const fetchReplies = async () => {
    try {
      const response = await fetch(`${baseUrl}/review/get/replies?rid=${review.rid}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch replies');
      }

      const data = await response.json();
      if (data.rid === "-1") {
        setReplies([]); // Means no reply exists
        return;
      }
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
      console.log(response.json());

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
      };

      fetchReplies();
    } catch (err) {
      console.error('Delete error:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete reply');
    }
  };
  // console.log(`Visitor: ${visitor} | Owner: ${owner}`);
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
      <div className={`flex items-center justify-between`}>
        <div className="grid grid-cols-3 justify-items-center">
          <div className="flex">
            <button
              type="button"
              className={`mt-4 w-4 h-4 flex items-center justify-center ${voted === "up"
                ? "text-orange-400"
                : "text-black"
                }`}
              onClick={async () => {
                await reviewUpvote()
              }}
            >
              <FaArrowUp />
            </button>
          </div>
          <div className="flex mt-3 mx-2 font-semibold text-black">
            {voteTotal}
          </div>
          <div className="flex">
            <button
              type="button"
              className={`mt-4 w-4 h-4 flex items-center justify-center ${voted === "down"
                ? "text-orange-400"
                : "text-black"
                }`}
              onClick={async () => {
                await reviewDownvote()
              }
              }
            >
              <FaArrowDown />
            </button>
          </div>
        </div>
        <div className="text-right mt-2 text-gray-500">
          {`${review.edited === true
            ? `Edited on ${review.e_timestamp}`
            : `Posted on ${review.timestamp}`
            }`}
        </div>
      </div>

      {/* Display Replies */}
      {replies.length > 0 && (
        <div className="mt-4 space-y-2">
          {replies.map((reply, index) => (
            <div key={index} className="ml-6 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-800 font-semibold">Reply from Creator</span>
                <div className="flex gap-2">
                  {/* Conditionally render buttons if api is available */}
                  {visitor === reply.reviewer && (
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
                  )}
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
              <div className="text-right mt-2 text-gray-500 text-sm">
                {`${reply.edited === true && !isEditing
                  ? `Edited on ${reply.e_timestamp}`
                  : `Posted on ${reply.timestamp}`
                  }`}
              </div>
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

      {!isReplying && !replies.length && visitor === owner && (
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