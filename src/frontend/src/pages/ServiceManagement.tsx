// src/pages/ServiceManagement.tsx

import React, { useState } from "react";
import ServiceTable from "../components/ServiceTable";
import ServiceModal from "../components/ServiceModal";
import { Status } from "../types/miscTypes"; // Import Status type

const ServiceManagement: React.FC = () => {
  // Dummy data for testing (you can replace this with fetched data)
  const [services, setServices] = useState([
    { id: "1", name: "Service One", description: "Description of Service One", status: "pending" as Status },
    { id: "2", name: "Service Two", description: "Description of Service Two", status: "approved" as Status },
    { id: "3", name: "Service Three", description: "Description of Service Three", status: "rejected" as Status },
  ]);

  const [selectedService, setSelectedService] = useState<{ id: string; name: string } | null>(null);
  const [modalActionType, setModalActionType] = useState<"approve" | "reject">("approve");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = (serviceId: string, serviceName: string, actionType: "approve" | "reject") => {
    setSelectedService({ id: serviceId, name: serviceName });
    setModalActionType(actionType);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedService(null);
    setIsModalOpen(false);
  };

  const handleApprove = (serviceId: string, reason: string) => {
    console.log(`Service with ID: ${serviceId} approved. Reason: ${reason}`);
  };

  const handleReject = (serviceId: string, reason: string) => {
    console.log(`Service with ID: ${serviceId} rejected. Reason: ${reason}`);
  };

  return (
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Services
      </h1>
      <ServiceTable
        services={services}
        onApprove={(serviceId, serviceName) => handleOpenModal(serviceId, serviceName, "approve")}
        onReject={(serviceId, serviceName) => handleOpenModal(serviceId, serviceName, "reject")}
      />

      {selectedService && (
        <ServiceModal
          isOpen={isModalOpen}
          onRequestClose={handleCloseModal}
          serviceName={selectedService.name}
          actionType={modalActionType}
          onSubmit={(reason) => {
            if (modalActionType === "approve") {
              handleApprove(selectedService.id, reason);
            } else {
              handleReject(selectedService.id, reason);
            }
          }}
        />
      )}
    </div>
  );
};

export default ServiceManagement;
