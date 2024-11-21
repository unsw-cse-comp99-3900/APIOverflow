import React, { useEffect, useState } from "react";
import { PendingVersion } from "../types/apiTypes";
import { FaCrown } from "react-icons/fa";
import Tag from "./Tag";
import { apiGetIcon } from "../services/apiServices";
import PendingNewVersionCard from "./PendingNewVersionCard";

interface PendingVersionsTableProps {
  pendingVersions: PendingVersion[];
  setCurrentPendingVersion: React.Dispatch<
    React.SetStateAction<PendingVersion | null>
  >;
}

const PendingVersionsTable: React.FC<PendingVersionsTableProps> = ({
  pendingVersions,
  setCurrentPendingVersion,
}) => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Pending Versions
      </h1>
      {pendingVersions.length === 0 && (
        <p className="text-lg font-semibold text-gray-600">
          There are no pending versions at the moment, go touch some grass~
        </p>
      )}

      {pendingVersions.length !== 0 &&
        pendingVersions.map((version) => (
          <PendingNewVersionCard
            version={version}
            key={version.version_name}
            setCurrentPendingVersion={setCurrentPendingVersion}
          />
        ))}
    </div>
  );
};

export default PendingVersionsTable;
