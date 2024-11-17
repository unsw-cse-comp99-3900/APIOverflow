import React, { useEffect, useState } from "react";
import { DetailedApi } from "../types/apiTypes";
import { toast } from "react-toastify";
import { FaRegCopy } from "react-icons/fa";
import { getDoc } from "../services/apiServices";

interface EndpointAndDocumentationProps {
  api: DetailedApi;
}

const EndpointAndDocumentation: React.FC<EndpointAndDocumentationProps> = ({
  api,
}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        if (api.versions[0].docs && api.versions[0].docs.length > 0) {
          const docURL = await getDoc(api.versions[0].docs[0]);
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
  }, [api.versions]); // Only run when `api.docs` changes

  const textToCopy = api.versions[0].endpoints[0].link;
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      toast.success("Copied to clipboard!");
    } catch (err) {
      console.log("Failed to copy!");
      toast.error("Failed to copy to clipboard");
    }
  };

  return (
    <>
      <div className=" bg-white rounded-2xl shadow-lg p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">Patch Note</h2>
        <p className="break-words text-justify">{api.description}</p>
        <div className="border border-gray-100 w-full my-5"></div>

        <h2 className="text-xl font-bold mb-4">Endpoint</h2>
        <div className="flex items-center rounded-xl px-5 my-5 min-h-12 bg-gray-100 border-2 border-gray-500">
          <p className="break-words font-semibold">{api.versions[0].endpoints[0].link}</p>
          <button
            onClick={copyToClipboard}
            className="ml-auto p-2 hover:bg-gray-400 rounded-xl min-h-5"
          >
            <FaRegCopy />
          </button>
        </div>

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

export default EndpointAndDocumentation;
