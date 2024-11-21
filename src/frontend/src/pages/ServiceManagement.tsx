// src/pages/ServiceManagement.tsx

import React, { useEffect, useState } from "react";
import ServiceTable from "../components/NewServicesTable";
import NewServiceModal from "../components/NewServiceModal";
import {
  approveGeneralInfo,
  approveNewVersion,
  approveNewService,
  getPendingServices,
} from "../services/apiServices";
import {
  PendingGeneralInfo,
  PendingNewService,
  Version,
} from "../types/apiTypes";
import NewServicesTable from "../components/NewServicesTable";

const ServiceManagement: React.FC = () => {

  // services waiting for approval
  const [newServices, setNewServices] = useState<PendingNewService[]>([]);
  const [newVersions, setNewVersions] = useState<Version[]>([]);
  const [generalInfoUpdates, setGeneralInfoUpdates] = useState<
    PendingGeneralInfo[]
  >([]);

  // currentl open service which has its detail being displayed
  const [selectedNewService, setSelectedNewService] = useState<PendingNewService | null>(
    null
  );
  const [selectedNewVersion, setSelectedNewVersion] = useState<Version | null>(null);
  const [selectedUpdatedGeneralInfo, setSelectedGeneralInfo] = useState<PendingGeneralInfo | null>(null)

  // filter for the services
  const [filter, setFilter] = useState<
    "All" | "NewService" | "NewVersion" | "GeneralInfoUpdate"
  >("All");

  // modal open state
  const [isNewServiceModalOpen, setIsNewServiceModalOpen] = useState(false);
  const [isNewVersionModalOpen, setIsNewVersionModalOpen] = useState(false);
  const [isGeneralInfoModalOpen, setIsGeneralInfoModalOpen] = useState(false);

  // React Hooks

  // Fetch services from the API
  useEffect(() => {
    const fetchPendingApis = async () => {
      // Fetch services from the API
      const data = await getPendingServices();
      setNewServices(data.new_services);
      setNewVersions(data.version_updates);
      setGeneralInfoUpdates(data.global_updates);
      console.log(data);
    };
    fetchPendingApis();
  }, []);

  const openNewServiceModal = (
    newService: PendingNewService
  ) => {
    setSelectedNewService(newService);
    setIsNewServiceModalOpen(true);
  };

  const openNewVersionModal = (
    version: Version
  ) => {
    setSelectedNewVersion(version);
    setIsNewVersionModalOpen(true);
  };

  const openGeneralInfoModal = (
    generalInfo: PendingGeneralInfo
  ) => {
    setSelectedGeneralInfo(generalInfo);
    setIsGeneralInfoModalOpen(true);
  };

  const closeModal = () => {
    setSelectedNewService(null);
    setSelectedNewVersion(null);
    setSelectedGeneralInfo(null);
    setIsNewServiceModalOpen(false);
    setIsGeneralInfoModalOpen(false);
    setIsNewVersionModalOpen(false);
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
              | "All"
              | "NewService"
              | "NewVersion"
              | "GeneralInfoUpdate"
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
      
      <NewServicesTable  />
    </div>
  );
};

export default ServiceManagement;
