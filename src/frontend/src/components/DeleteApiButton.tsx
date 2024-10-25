import React from "react";
import { FaTrash } from "react-icons/fa";
import { toast } from "react-toastify";
import { deleteApi } from "../services/apiServices";
import { useNavigate } from "react-router-dom";

interface DeleteApiButtonProps {
  apiId: string;
  apisRoute?: string;
  onDelete?: (id: string) => void;
}

const DeleteApiButton: React.FC<DeleteApiButtonProps> = ({
  apiId,
  apisRoute,
  onDelete,
}) => {
  const navigate = useNavigate();
  const onDeleteClick = async (apiId: string) => {
    const confirm = window.confirm("Are you sure you want to delete this API?");
    if (!confirm) return;

    try {
      await deleteApi(apiId);
      toast.success("API deleted successfully");

      if (onDelete) onDelete(apiId); // Trigger the deletion callback to update the state
      if (apisRoute) navigate(apisRoute); // Redirect to the APIs page
    } catch (error) {
      toast.error("Failed to delete API");
    }
  };

  return (
    <button
      className="bg-white text-red-500 hover:bg-red-500 hover:text-white font-semibold px-3 py-3 rounded-lg"
      onClick={() => onDeleteClick(apiId)}
    >
      <FaTrash />
    </button>
  );
};

export default DeleteApiButton;
