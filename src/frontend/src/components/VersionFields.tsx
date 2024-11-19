import React, { useEffect, useState } from "react";
import { DetailedApi, Version } from "../types/apiTypes";
import { toast } from "react-toastify";
import { getDoc } from "../services/apiServices";
import EndpointComponent from "./EndpointComponent";
import { notNewVersions } from "../utils/versions";

interface VersionFieldsProps {
  versions: Version[];
}

const VersionFields: React.FC<VersionFieldsProps> = ({ versions }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const currVersions = notNewVersions(versions);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        if (currVersions[0].docs && versions[0].docs.length > 0) {
          const docURL = await getDoc(versions[0].docs[0]);
          setPdfUrl(docURL);
        } else {
          setError("No documentation available.");
        }
      } catch (error) {
        console.log("Error fetching data", error);
        if (error instanceof Error) {
          setError(error.message);
        }
        toast.error("Error loading API documentation");
      } finally {
        setLoading(false);
      }
    };

    fetchDocs();
  }, [versions]);

  return (
    <>
      <div className=" bg-white rounded-2xl shadow-lg p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">Patch Note</h2>
        <p className="break-words text-justify">
          {versions[0].version_description}
        </p>
        <div className="border border-gray-100 w-full my-5"></div>

        <h2 className="text-xl font-bold mb-4">Endpoints</h2>

        {versions[0].endpoints.map((endpoint, index) => (
          <EndpointComponent key={index} endpoint={endpoint} />
        ))}

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
