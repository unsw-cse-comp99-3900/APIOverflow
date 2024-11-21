// src/components/ServiceModal.tsx
import React, { useState } from "react";
import {
  PendingNewService,
} from "../types/apiTypes";

interface PendingServiceModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  modalTitle: string;
  actionType: "approve" | "reject";
  onSubmit: (reason: string) => void;
}

const PendingServiceModal: React.FC<PendingServiceModalProps> = ({
  isOpen,
  onRequestClose,
  modalTitle,
  actionType,
  onSubmit,
}) => {
  const [reason, setReason] = useState("");

  const handleSubmit = () => {
    if (reason.trim() === "") {
      alert("Please provide a reason.");
      return;
    }
    onSubmit(reason);
    onRequestClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div className="bg-white w-11/12 md:w-1/3 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">
          {actionType === "approve" ? "Approve" : "Reject"} Service: {modalTitle}
        </h2>
        <textarea
          className="w-full h-32 p-2 border rounded-lg mb-4"
          placeholder={`Reason for ${actionType}ing the service`}
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        />
        <div className="flex justify-end space-x-4">
          <button
            className="bg-gray-400 hover:bg-gray-500 text-white font-semibold py-2 px-4 rounded"
            onClick={onRequestClose}
          >
            Cancel
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
            onClick={handleSubmit}
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};

export default PendingServiceModal;
