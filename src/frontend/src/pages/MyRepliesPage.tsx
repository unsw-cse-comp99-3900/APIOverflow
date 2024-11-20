import { PhotoIcon } from "@heroicons/react/24/solid";
import React, { useState, useEffect } from 'react'
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { UserProfile } from "../types/userTypes";
import {
  getUser,
  updateDisplayName,
  uploadImage,
  userAddIcon,
  userDeleteReply,
  userEditReply,
  userGetReplies,
} from "../services/apiServices";
import { ReplyDetail } from "../types/miscTypes";
import ReviewCardHeader from "../components/ReviewCardHeader";
import ReplyDetailCard from "../components/ReplyDetailCard";
import ReplyDetailModal from "../components/ReplyDetailModal";

const MyRepliesPage = () => {
  const navigate = useNavigate();
  const [selectedReply, setSelectedReply] = useState<ReplyDetail | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [replies, setReplies] = useState<ReplyDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [reload, setReload] = useState(true);

  useEffect (() => {

    const fetchReplies = async () => {
      
      if (!reload) {return};
      
      try {
        const data = await userGetReplies();
        setReplies(data);
  
      } catch(error) {
        console.log(error);
      }
      setLoading(false);
      setReload(false);
    }
    fetchReplies();
  }, [reload]);

  const handleOpenModal = (reply: ReplyDetail) => {
    setSelectedReply(reply);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedReply(null);
    setIsModalOpen(false);
    setReload(true);
  };

  const handleEdit = async (replyId: string, content: string) => {
    await userEditReply(replyId, content); 
    handleCloseModal();
    setReload(true);
  };

  const handleDelete = async (replyId: string) => {
    await userDeleteReply(replyId);
    setReload(true);
  };

  return (
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        My Replies
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {replies.map((reply) => ( 
            <div key={reply.rid} className="shadow-lg rounded-xl p-4 transition-transform transform hover:scale-105">
                <ReviewCardHeader reviewID={reply.rid} service={reply.service} />
                <div className="border border-gray-100 mx-4 mb-5"></div>
                <ReplyDetailCard review={reply} />
                <div className="grid grid-cols-3 gap-50">
                    <div>
                      <button
                      className="mt-4 bg-gradient-to-r from-blue-500 to-blue-700 text-white font-semibold py-2 px-6 rounded-full hover:from-blue-600 hover:to-blue-800 transition-all shadow-lg"
                      onClick={() => handleOpenModal(reply)}
                      >
                      Edit Reply
                      </button>
                    </div>
                    <div>
                      <button
                        className="absolute right-4 mt-4 bg-red-500 text-white font-semibold py-2 px-6 rounded-full hover:from-red-600 hover:to-red-800 transition-all shadow-lg"
                        onClick={() => handleDelete(reply.rid)}
                        >
                        Delete Reply
                      </button>
                    </div>
                </div>
            </div>
        ))}
      </div>

      {selectedReply && (
        <ReplyDetailModal
          isOpen={isModalOpen}
          onRequestClose={handleCloseModal}
          reply={selectedReply}
          onSave={handleEdit}
        />
      )}
    </div>
  );
}

export default MyRepliesPage;