import React, { useEffect } from "react";
import { PendingNewService } from "../types/apiTypes";

interface PendingServicesTableProps {
  pendingServices: PendingNewService[];
  openModal: (newService: PendingNewService) => void;
  closeModal: () => void;
}

const PendingServicesTable: React.FC<PendingServicesTableProps> = ({
  pendingServices,
  openModal,
  closeModal,
}) => {

  useEffect(() => {
    console.log(pendingServices);
  }, [pendingServices]
)
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Pending Services
      </h1>
      NewServicesTable
    </div>
  );
};

export default PendingServicesTable;
