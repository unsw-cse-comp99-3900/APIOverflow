import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { getDoc } from "../services/apiServices";


interface ApiDocsProps {
  doc_ids: string[];
}

const ApiDocs:React.FC<ApiDocsProps> = ({doc_ids}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [files, setFiles] = useState<File[]>([]);

  useEffect(() => {
    const fetchDocs = async () => {
      try {

        const doc = await getDoc(doc_ids[0]);
        console.log(doc)
      } catch (error) {
        console.log("Error fetching data", error);
        if (error instanceof Error) {
          setError(error.message);
        }
        toast.error("Error loading API data");
      } finally {
        setLoading(false);
      }
    };

    fetchDocs();
  });


  return (
    <div className="w-1/4 bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">Documentation</h2>
      {/* Placeholder for Documentation */}
      <p>Coming soon</p>
    </div>
  );
};

export default ApiDocs;
