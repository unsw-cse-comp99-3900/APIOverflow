// src/components/GeneralInfoUpdateModal.tsx
import React, { useEffect, useState } from "react";
import { PendingGeneralInfo } from "../types/apiTypes";
import ApiGeneralInfo from "./ApiGeneralInfo";
import { toast } from "react-toastify";
import { apiGetIcon, approveGeneralInfo } from "../services/apiServices";
import ApiDescription from "./ApiDescription";
import VersionFields from "./VersionFields";
import FetchStatus from "./FetchStatus";

interface PendingGeneralInfoUpdateModalProps {
  pendingGeneralInfoUpdate: PendingGeneralInfo;
  refreshData: () => Promise<void>;
  setCurrentPendingGeneralInfoUpdate: React.Dispatch<
    React.SetStateAction<PendingGeneralInfo | null>
  >;
}

const PendingGeneralInfoUpdateModal: React.FC<PendingGeneralInfoUpdateModalProps> = ({
  pendingGeneralInfoUpdate,
  refreshData,
  setCurrentPendingGeneralInfoUpdate,
}) => {
  const [reason, setReason] = useState("");
  const [iconURL, setIconURL] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string>("");

  useEffect(() => {
    const fetchApi = async () => {
      try {
        const iconURL = await apiGetIcon(pendingGeneralInfoUpdate.id);
        setIconURL(iconURL);
      } catch (error) {
        console.log("Error fetching data", error);
        if (error instanceof Error) {
          setError(error.message);
        }
        toast.error("Error loading API data");
      } finally {
        setLoading(false);
      }
    };

    fetchApi();

    // Cleanup the object URL to avoid memory leaks
    return () => {
      if (iconURL) {
        URL.revokeObjectURL(iconURL);
      }
    };
  }, []);

  const handleApproval = async (approval: boolean) => {
    if (reason.trim() === "") {
      setWarning("Please provide a reason for your decision");
      return;
    }

    try {
      await approveGeneralInfo(
        pendingGeneralInfoUpdate.id,
        approval,
        reason,
      );
      toast.success(`General Info Update ${approval ? "approved" : "rejected"} successfully`);
      await refreshData();
      setCurrentPendingGeneralInfoUpdate(null);
    } catch (error) {
      console.log("Error approving general info update", error);
      if (error instanceof Error) {
        setError(error.message);
      }
    }
  };

  return (
    <FetchStatus loading={loading} error={error} data={iconURL}>
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div
        className="bg-white w-4/5 p-6 rounded-lg flex flex-col"
        style={{ maxHeight: "90vh" }} // Fix the height to 90% of the viewport height
      >
        <div
          className="overflow-y-auto flex-1 px-6 rounded-lg" // Add scrollable content area
          style={{ maxHeight: "calc(90vh - 120px)" }} // Account for padding and buttons
        >
          <h1 className="text-2xl text-blue-800 font-bold">General Info Update Approval</h1>
          <textarea
            className="w-full h-32 p-2 border rounded-lg mt-6"
            placeholder={`Reason for accepting/rejecting ${pendingGeneralInfoUpdate.name}`}
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />

          <div className="text-red-500">{warning}</div>

          <ApiGeneralInfo
            apiId={pendingGeneralInfoUpdate.id}
            apiName={pendingGeneralInfoUpdate.name}
            iconURL={iconURL}
            ownerName=""
            payModel={pendingGeneralInfoUpdate.pay_model}
            status={"PENDING"}
            tags={pendingGeneralInfoUpdate.tags}
            isMyApi={false}
            rating={"0"}
            isGettingApproved={true}
          />

          <ApiDescription description={pendingGeneralInfoUpdate.description} />
        </div>

        <div className="flex justify-between mt-6 ml-6">
          <button
            className="bg-gray-400 hover:bg-gray-500 text-white font-semibold rounded w-20 h-10"
            onClick={() => setCurrentPendingGeneralInfoUpdate(null)}
          >
            Cancel
          </button>

          <div>
            <button
              className="bg-red-500 hover:bg-red-600 text-white font-semibold rounded w-20 h-10 mx-2"
              onClick={() => handleApproval(false)}
            >
              Reject
            </button>
            <button
              className="bg-green-500 hover:bg-green-600 text-white font-semibold rounded w-20 h-10 mx-2"
              onClick={() => handleApproval(true)}
            >
              Approve
            </button>
          </div>
        </div>
      </div>
    </div>
    </FetchStatus>
  );
};

export default PendingGeneralInfoUpdateModal;
