// ReviewReply.tsx
import React, { useState } from 'react';

interface ReplyProps {
  reviewId: string;
  onSubmitReply: (reviewId: string, content: string) => Promise<void>;
}

const ReviewReply: React.FC<ReplyProps> = ({ reviewId, onSubmitReply }) => {
  const [replyContent, setReplyContent] = useState('');
  const [isReplying, setIsReplying] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!replyContent.trim()) {
      setError('Reply cannot be empty');
      return;
    }

    try {
      await onSubmitReply(reviewId, replyContent);
      setReplyContent('');
      setIsReplying(false);
      setError('');
    } catch (err) {
      setError((err as Error).message || 'Failed to submit reply');
    }
  };

  return isReplying ? (
    <div className="mt-3">
      <form onSubmit={handleSubmit} className="space-y-2">
        <textarea
          value={replyContent}
          onChange={(e) => setReplyContent(e.target.value)}
          className="w-full p-2 border rounded-lg focus:outline-none focus:border-blue-500 text-sm"
          placeholder="Write your reply..."
          rows={3}
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={() => setIsReplying(false)}
            className="px-3 py-1 text-gray-600 bg-gray-100 rounded-lg text-sm hover:bg-gray-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-3 py-1 bg-blue-800 text-white rounded-lg text-sm hover:bg-blue-700"
          >
            Submit Reply
          </button>
        </div>
      </form>
    </div>
  ) : (
    <button
      onClick={() => setIsReplying(true)}
      className="mt-2 text-blue-600 text-sm hover:text-blue-800"
    >
      Reply
    </button>
  );
};

export default ReviewReply;