import React, { useEffect, useState } from "react";
import { PendingGeneralInfo } from "../types/apiTypes";
import { FaCrown } from "react-icons/fa";
import Tag from "./Tag";
import { apiGetIcon } from "../services/apiServices";
import PendingNewGeneralInfoUpdateCard from "./PendingNewGeneralInfoUpdateCard";

interface PendingGeneralInfoUpdatesTableProps {
  pendingGeneralInfoUpdates: PendingGeneralInfo[];
  setCurrentPendingGeneralInfo: React.Dispatch<
    React.SetStateAction<PendingGeneralInfo | null>
  >;
}

const PendingGeneralInfoUpdatesTable: React.FC<PendingGeneralInfoUpdatesTableProps> = ({
  pendingGeneralInfoUpdates,
  setCurrentPendingGeneralInfo,
}) => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Pending General Info Updates
      </h1>
      {pendingGeneralInfoUpdates.length === 0 && (
        <p className="text-lg font-semibold text-gray-600">
          There are no pending general info updates at the moment, go touch some grass~
        </p>
      )}

      {pendingGeneralInfoUpdates.length !== 0 &&
        pendingGeneralInfoUpdates.map((generalInfo) => (
          <PendingNewGeneralInfoUpdateCard
          generalInfoUpdate={generalInfo}
            key={generalInfo.id}
            setCurrentPendingGeneralInfoUpdate={setCurrentPendingGeneralInfo}
          />
        ))}
    </div>
  );
};

export default PendingGeneralInfoUpdatesTable;
