// src/pages/ServiceManagement.tsx

import React, { useEffect, useState } from "react";
import ServiceTable from "../components/ServiceTable";
import ServiceModal from "../components/ServiceModal";
import { approveService, getPendingServices } from "../services/apiServices";
import {
  ServiceAdminBrief,
  ServiceUpdateDataAdminView,
} from "../types/apiTypes";

const ServiceManagement: React.FC = () => {
  // Dummy data for testing (you can replace this with fetched data)
  const [updateData, setUpdateData] =
    useState<ServiceUpdateDataAdminView | null>(null);
  const [services, setServices] = useState<ServiceAdminBrief[]>([]);
  const [selectedService, setSelectedService] = useState<ServiceAdminBrief | null>(null);
  const [modalActionType, setModalActionType] = useState<"approve" | "reject">(
    "approve"
  );
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [filter, setFilter] = useState<
    "newServices" | "newVersions" | "generalInfoUpdates"
  >("newServices");

  useEffect(() => {
    const fetchPendingApis = async () => {
      // Fetch services from the API
      const res = await getPendingServices();
      setUpdateData(res);
    };
    fetchPendingApis();
  }, [updateData]);

  useEffect(() => {
    if (filter === "newServices") 
      setServices(updateData?.newServices || []);
     else if (filter === "newVersions")
      setServices(updateData?.newVersions || []);
    else if (filter === "generalInfoUpdates")
      setServices(updateData?.generalInfoUpdates || []);
  }, [filter, updateData]);


  const handleOpenModal = (
    service: ServiceAdminBrief,
    actionType: "approve" | "reject"
  ) => {
    setSelectedService(service);
    setModalActionType(actionType);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedService(null);
    setIsModalOpen(false);
  };

  const handleApprove = (service: ServiceAdminBrief, reason: string) => {
    approveService(service.id, true, reason, service.serviceGlobal, service.versionName)
    console.log(`Service with ID: ${service.id} approved. Reason: ${reason}`);
  };

  const handleReject = (service: ServiceAdminBrief, reason: string) => {
    approveService(service.id, false, reason, service.serviceGlobal, service.versionName)
    console.log(`Service with ID: ${service.id} rejected. Reason: ${reason}`);
  };

  return (
    <div className="p-12">
      <h1 className="text-3xl font-bold mb-8 text-blue-800 underline-offset-8">
        Services
      </h1>
      <label className="mr-2 text-gray-700 font-semibold">Filter:</label>
      <select
        value={filter}
        onChange={(e) =>
          setFilter(
            e.target.value as
              | "newServices"
              | "newVersions"
              | "generalInfoUpdates"
          )
        }
        className="p-2 border rounded-md w-48 h-10"
      >
        <option className="border rounded-md" value="newServices">
          New Services
        </option>
        <option value="newVersions">New Versions</option>
        <option value="generalInfoUpdates">General Info Update</option>
      </select>
      <ServiceTable
        services={services}
        onApprove={(service:ServiceAdminBrief) =>
          handleOpenModal(service, "approve")
        }
        onReject={(service) =>
          handleOpenModal(service, "reject")
        }
      />

      {selectedService && (
        <ServiceModal
          isOpen={isModalOpen}
          onRequestClose={handleCloseModal}
          serviceName={selectedService.name}
          actionType={modalActionType}
          onSubmit={(reason) => {
            if (modalActionType === "approve") {
              handleApprove(selectedService, reason);
            } else {
              handleReject(selectedService, reason);
            }
          }}
        />
      )}
    </div>
  );
};

export default ServiceManagement;
