// src/components/ServiceTable.tsx

import React from "react";
import { Status } from "../types/miscTypes";

interface Service {
  id: string;
  name: string;
  description: string;
  status: Status;
}

interface ServiceTableProps {
  services: Service[];
  onApprove: (serviceId: string, serviceName: string) => void;
  onReject: (serviceId: string, serviceName: string) => void;
}

const ServiceTable: React.FC<ServiceTableProps> = ({ services, onApprove, onReject }) => {
  // Sort services: "pending" first, then "approved" and "rejected"
  const sortedServices = [...services].sort((a, b) => {
    if (a.status === "pending") return -1;
    if (b.status === "pending") return 1;
    return 0;
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {sortedServices.map((service) => (
        <div
          key={service.id}
          className="relative shadow-md rounded-lg p-4 bg-white border transition-transform transform hover:scale-105 border-gray-200"
        >
          {/* Status Indicator */}
          <div
            className={`absolute top-3 right-3 w-6 h-6 rounded-full ${
              service.status === "approved"
                ? "bg-green-500"
                : service.status === "rejected"
                ? "bg-red-500"
                : "bg-yellow-500"
            }`}
          ></div>
          <h2 className="text-2xl font-bold text-blue-800 mb-3">{service.name}</h2>
          <p className="text-gray-600 mb-3">{service.description}</p>
          <div className="mt-4 flex justify-between">
            <button
              className="bg-green-500 hover:bg-green-600 text-white font-medium py-1 px-4 rounded shadow-md transition-all"
              onClick={() => onApprove(service.id, service.name)}
            >
              Approve
            </button>
            <button
              className="bg-red-500 hover:bg-red-600 text-white font-medium py-1 px-4 rounded shadow-md transition-all"
              onClick={() => onReject(service.id, service.name)}
            >
              Reject
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ServiceTable;
