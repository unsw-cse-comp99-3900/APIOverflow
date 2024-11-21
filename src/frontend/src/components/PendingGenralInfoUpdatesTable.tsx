import React from "react";
import { PendingGeneralInfo } from "../types/apiTypes";

interface PendingGeneralInfoUpdatesTableProps {
  pendingGeneralInfo: PendingGeneralInfo[];
}

const PendingGeneralInfoUpdatesTable: React.FC<
  PendingGeneralInfoUpdatesTableProps
> = ({ pendingGeneralInfo }) => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Pending General Info Updates
      </h1>
      GeneralInfoUpdatesTabls
    </div>
  );
};

export default PendingGeneralInfoUpdatesTable;
