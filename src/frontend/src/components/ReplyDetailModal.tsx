import React, { useState } from "react";
import { ReplyDetail } from "../types/miscTypes";

interface ReplyDetailModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  reply: ReplyDetail;
  onSave: (replyId: string, content: string) => void;
}

const ReplyDetailModal: React.FC<ReplyDetailModalProps> = ({
  isOpen,
  onRequestClose,
  reply,
  onSave,
}) => {
  const [content, setContent] = useState(reply.comment);

  if (!isOpen) return null; // If the modal is not open, return null

  const handleSave = () => {
    if (content.trim()) {
      onSave(reply.rid, content);
      onRequestClose();
    } else {
      alert("Reply cannot be empty.");
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-3xl bg-white rounded-lg shadow-lg p-6 mx-4">
        <h2 className="text-2xl font-bold mb-4">Edit Review</h2>

        {/* Edited Content */}
        <div className="mt-6">
          <label htmlFor="content" className="block mb-2 font-semibold">Review Content:</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={reply.comment}
            defaultValue={reply.comment}
            className="w-full p-2 border rounded"
            rows={3}
          />
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex items-centergap-x-6 justify-between">
          <div className="flex">
            <button
              onClick={() => handleSave()} // Pass review ID and edited content
              className="flex mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mx-5"
            >
              Save
            </button>
            <button
              onClick={onRequestClose}
              className="mt-4 bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReplyDetailModal;
