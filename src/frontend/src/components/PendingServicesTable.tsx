import React, { useEffect, useState } from "react";
import { PendingNewService } from "../types/apiTypes";
import { FaCrown } from "react-icons/fa";
import Tag from "./Tag";
import { apiGetIcon } from "../services/apiServices";
import PendingNewServiceCard from "./PendingNewServiceCard";

interface PendingServicesTableProps {
  pendingServices: PendingNewService[];
  setCurrentPendingService: React.Dispatch<React.SetStateAction<PendingNewService | null>>;
}

const PendingServicesTable: React.FC<PendingServicesTableProps> = ({
  pendingServices,
  setCurrentPendingService
}) => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Pending Services
      </h1>
      {pendingServices.length === 0 && (
        <p className="text-lg font-semibold text-gray-600">
          There are no pending services at the moment, go touch some grass~
        </p>

      )}

      {pendingServices.length !== 0 && (
      pendingServices.map((service) => (
        <PendingNewServiceCard
          service={service}
          key={service.id}
          setCurrentPendingService={setCurrentPendingService}
        />
      ))


      )}

    </div>
  );
};

export default PendingServicesTable;
