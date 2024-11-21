// src/pages/ServiceManagement.tsx

import React, { useEffect, useState } from "react";
import NewServiceModal from "../components/PendingServiceModal";
import {
  getPendingServices,
} from "../services/apiServices";
import {
  PendingGeneralInfo,
  PendingNewService,
  PendingVersion,
} from "../types/apiTypes";
import PendingServicesTable from "../components/PendingServicesTable";
import PendingVersionsTable from "../components/PendingVersionsTable";
import PendingGeneralInfoUpdatesTable from "../components/PendingGenralInfoUpdatesTable";

const ServiceManagement: React.FC = () => {
  // services waiting for approval
  const [newServices, setNewServices] = useState<PendingNewService[]>([]);
  const [newVersions, setNewVersions] = useState<PendingVersion[]>([]);
  const [generalInfoUpdates, setGeneralInfoUpdates] = useState<
    PendingGeneralInfo[]
  >([]);

  // currentl open service which has its detail being displayed
  const [selectedNewService, setSelectedNewService] =
    useState<PendingNewService | null>(null);
  const [selectedNewVersion, setSelectedNewVersion] =
    useState<PendingVersion | null>(null);
  const [selectedUpdatedGeneralInfo, setSelectedGeneralInfo] =
    useState<PendingGeneralInfo | null>(null);

  // filter for the services
  const [filter, setFilter] = useState<
    "All" | "NewServices" | "NewVersions" | "GeneralInfoUpdates"
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

  const openNewServiceModal = (newService: PendingNewService) => {
    setSelectedNewService(newService);
    setIsNewServiceModalOpen(true);
  };

  const openNewVersionModal = (version: PendingVersion) => {
    setSelectedNewVersion(version);
    setIsNewVersionModalOpen(true);
  };

  const openGeneralInfoModal = (generalInfo: PendingGeneralInfo) => {
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
      <div></div>
      <label className="mr-2 text-gray-700 font-semibold">Filter:</label>
      <select
        value={filter}
        onChange={(e) =>
          setFilter(
            e.target.value as
              | "All"
              | "NewServices"
              | "NewVersions"
              | "GeneralInfoUpdates"
          )
        }
        className="p-2 border rounded-md w-48 h-10"
      >
        <option className="border rounded-md" value="All">
          All
        </option>
        <option className="border rounded-md" value="newServices">
          New Services
        </option>
        <option value="newVersions">New Versions</option>
        <option value="generalInfoUpdates">General Info Updates</option>
      </select>

      {(filter === "All" || filter === "NewServices") && (
        <PendingServicesTable
          pendingServices={newServices}
          openModal={openNewServiceModal}
          closeModal={closeModal}
        />
      )}

      {(filter === "All" || filter === "NewServices") && (
        <PendingVersionsTable
          pendingVersions={newVersions}
          openModal={openNewVersionModal}
          closeModal={closeModal}
        />
      )}

      {(filter === "All" || filter === "GeneralInfoUpdates") && (
        <PendingGeneralInfoUpdatesTable
          pendingGeneralInfo={generalInfoUpdates}
          openModal={openGeneralInfoModal}
          closeModal={closeModal}
        />
      )}
    </div>
  );
};

export default ServiceManagement;
