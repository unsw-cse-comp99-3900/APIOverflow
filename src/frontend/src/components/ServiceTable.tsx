// src/components/ServiceTable.tsx

import {  ServiceAdminBrief } from "../types/apiTypes";

interface ServiceTableProps {
  services: ServiceAdminBrief[];
  onApprove: (service: ServiceAdminBrief) => void;
  onReject: (service: ServiceAdminBrief) => void;
}

const ServiceTable: React.FC<ServiceTableProps> = ({
  services,
  onApprove,
  onReject,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-8">
      {services.map((service, index) => (
        <div
          key={index}
          className="relative shadow-md rounded-lg p-4 bg-white border transition-transform transform hover:scale-105 border-gray-200"
        >
          <h2 className="text-2xl font-bold text-blue-800 mb-3">
            {service.name}
          </h2>
          <p className="text-gray-600 mb-3">{(service.description)}</p>
          <div className="mt-4 flex justify-between">
            <button
              className="bg-green-500 hover:bg-green-600 text-white font-medium py-1 px-4 rounded shadow-md transition-all"
              onClick={() => onApprove(service)}
            >
              Approve
            </button>
            <button
              className="bg-red-500 hover:bg-red-600 text-white font-medium py-1 px-4 rounded shadow-md transition-all"
              onClick={() => onReject(service)}
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
