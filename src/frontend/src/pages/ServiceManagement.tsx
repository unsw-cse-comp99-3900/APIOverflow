// src/pages/ServiceManagement.tsx

import React, { useEffect, useState } from "react";
import NewServiceModal from "../components/PendingServiceModal";
import { getPendingServices } from "../services/apiServices";
import {
  PendingGeneralInfo,
  PendingNewService,
  PendingVersion,
} from "../types/apiTypes";
import PendingServicesTable from "../components/PendingServicesTable";
import PendingVersionsTable from "../components/PendingVersionsTable";
import PendingGeneralInfoUpdatesTable from "../components/PendingGenralInfoUpdatesTable";
import PendingServiceModal from "../components/PendingServiceModal";

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
    "All" | "PendingServices" | "PendingVersions" | "PendingGeneralInfoUpdates"
  >("All");

  // Fetch services from the API
  useEffect(() => {
    const fetchPendingApis = async () => {
      // Fetch services from the API
      const data = await getPendingServices();
      setNewServices(data.new_services);
      setNewVersions(data.version_updates);
      setGeneralInfoUpdates(data.global_updates);
    };
    fetchPendingApis();
  }, []);

  const refreshData = async () => {
    const data = await getPendingServices();
    setNewServices(data.new_services);
    setNewVersions(data.version_updates);
    setGeneralInfoUpdates(data.global_updates);
  };

  return (
    <div className="container-xl lg:container mx-auto p-10">
      <div className="flex justify-end items-center mb-4">
        <label className="mr-2 text-gray-700 font-semibold">Filter:</label>
        <select
          value={filter}
          onChange={(e) =>
            setFilter(
              e.target.value as
                | "All"
                | "PendingServices"
                | "PendingVersions"
                | "PendingGeneralInfoUpdates"
            )
          }
          className="p-2 border rounded-md w-48 h-10"
        >
          <option className="border rounded-md" value="All">
            All
          </option>
          <option className="border rounded-md" value="PendingServices">
            Pending New Services
          </option>
          <option value="PendingVersions">Pending Versions</option>
          <option value="PendingGeneralInfoUpdates">
            Pending General Info Updates
          </option>
        </select>
      </div>

      {(filter === "All" || filter === "PendingServices") && (
        <PendingServicesTable
          pendingServices={newServices}
          setCurrentPendingService={setSelectedNewService}
        />
      )}

      {(filter === "All" || filter === "PendingVersions") && (
        <PendingVersionsTable pendingVersions={newVersions} />
      )}

      {(filter === "All" || filter === "PendingGeneralInfoUpdates") && (
        <PendingGeneralInfoUpdatesTable
          pendingGeneralInfo={generalInfoUpdates}
        />
      )}

      {selectedNewService && (
        <PendingServiceModal
          pendingService={selectedNewService}
          setCurrentPendingService={setSelectedNewService}
          refreshData={refreshData}
        />
      )}
    </div>
  );
};

export default ServiceManagement;
