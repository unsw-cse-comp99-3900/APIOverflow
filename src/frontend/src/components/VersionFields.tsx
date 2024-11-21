import React, { useEffect, useState } from "react";
import { DetailedApi, Version } from "../types/apiTypes";
import { toast } from "react-toastify";
import { getDoc } from "../services/apiServices";
import EndpointComponent from "./EndpointComponent";
import { getCurrVersions } from "../utils/versions";

interface VersionFieldsProps {
  versions: Version[];
}

const VersionFields: React.FC<VersionFieldsProps> = ({ versions }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [currVersion, setCurrVersion] = useState<Version | null>(versions[0]);
  const [currVersionName, setCurrVersionName] = useState<string>("");

  useEffect(() => {
    if (versions.length > 0) {
      const defaultVersion =
        versions.find((ver) => ver.version_name === currVersionName) ||
        versions[0]; // Fallback to the first version
      setCurrVersion(defaultVersion);
      setCurrVersionName(defaultVersion.version_name); // Ensure `currVersionName` matches
    }
  }, [versions, currVersionName]);

  useEffect(() => {
    for (const currVer of versions) {
      if (currVer.version_name === currVersionName) {
        setCurrVersion(currVer);
        break;
      }
    }
  }, [currVersionName, versions]);


  useEffect(() => {
    let isCancelled = false; // Cancellation token for this effect
    const fetchDocs = async () => {
      try {
        if (!currVersion) {
          if (!isCancelled) {
            setError(
              "No live version available for this service yet, come back later!"
            );
            setPdfUrl(null);
          }
        } else if (currVersion.docs.length > 0) {
          const docURL = await getDoc(currVersion.docs[0]);
          if (!isCancelled) {
            setPdfUrl(docURL);
            setError("");
          }
        } else {
          if (!isCancelled) {
            setError("No document for this version available");
            setPdfUrl(null);
          }
        }
      } catch (error) {
        if (!isCancelled) {
          if (error instanceof Error) {
            setError(error.message);
          }
          toast.error("Error loading API documentation");
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    };
  
    fetchDocs();
  
    return () => {
      isCancelled = true; // Cancel this effect on cleanup
    };
  }, [currVersion, currVersionName]);
  

  const textColor = {
    "LIVE": "text-green-600",
    "PENDING": "text-amber-600",
    "UPDATE_PENDING": "text-amber-600",
    "REJECTED": "text-red-600",
    "UPDATE_REJECTED": "text-red-600",
  }

  if (versions.length === 0) {
    return null;
  }

  return (
    <>
      <div className="border-2 border-gray-100 bg-white rounded-2xl shadow-lg p-6 my-6">
        <div className="flex justify-between mb-2">
          <div className="flex justify-between items-center">
            <div className="flex text-xl font-bold">
              <h2 className="text-xl font-bold">Version Patch Note</h2>
            </div>
          </div>

          {currVersion !== null && (
            <div className="flex items-center">
              <div className={`mr-2 font-semibold ${textColor[currVersion.status]}`}>status: {currVersion.status}</div>
              <select
                value={currVersionName}
                onChange={(e) => setCurrVersionName(e.target.value)}
                className="p-2 border w-56 rounded-md focus:ring-2 focus:ring-indigo-600"
              >
                {versions.map((version, index) => (
                  <option key={index} value={version.version_name}>
                    {version.version_name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        <p className="break-words text-justify">
          {currVersion
            ? currVersion.version_description
            : "No live version available for this service yet, come back later!"}
        </p>
        <div className="border border-gray-100 w-full my-5"></div>
        <h2 className="text-xl font-bold mb-4">Endpoints</h2>

        {currVersion
          ? currVersion.endpoints.map((endpoint, index) => (
              <EndpointComponent key={index} endpoint={endpoint} />
            ))
          : "No live version available for this service yet, come back later!"}

        <div className="border border-gray-100 w-full my-5"></div>

        <h2 className="text-xl font-bold mb-4">Documentation</h2>
        {loading ? (
          <p>Loading documentation...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : pdfUrl ? (
          <iframe
            src={pdfUrl}
            title="Documentation PDF"
            width="100%"
            height="600px"
            className="border border-gray-300 rounded-lg"
          ></iframe>
        ) : (
          <p>No documentation available</p>
        )}
      </div>
    </>
  );
};

export default VersionFields;
