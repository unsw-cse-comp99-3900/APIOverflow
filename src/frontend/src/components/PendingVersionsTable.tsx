import React from "react";
import { PendingVersion } from "../types/apiTypes";

interface PendingVersionsTableProps {
  pendingVersions: PendingVersion[];
}

const PendingVersionsTable: React.FC<PendingVersionsTableProps> = ({
  pendingVersions,
}) => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Pending Versions
      </h1>
      GeneralInfoUpdatesTabls
    </div>
  );
};

export default PendingVersionsTable;
