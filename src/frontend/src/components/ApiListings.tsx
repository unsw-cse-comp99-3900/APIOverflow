import { useState, useEffect } from "react";
import { Api } from "../types/apiTypes";
import ApiListing from "./ApiListing";
import Spinner from "./Spinner";
import { getApis, getMyApis } from "../services/apiServices";
import FetchStatus from "./FetchStatus";

const ApiListings = ({ isMyAPis }: { isMyAPis: boolean }) => {
  const [apis, setApis] = useState<Api[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = isMyAPis ? await getMyApis() : await getApis();
        setApis(data);
      } catch (error) {
        console.log("Error fetching data", error);
        setError("Failed to load API data");
      } finally {
        setLoading(false);
      }
    };

    fetchApis();
  }, [isMyAPis]);

  const handleDelete = (deletedApiId: number) => {
    setApis((prevApis) => prevApis.filter((api) => api.id !== deletedApiId));
  };

  return (
    <FetchStatus loading={loading} error={error} data={apis}> 
          <div className="container-xl lg:container mx-auto px-10">
        <h2 className="text-3xl font-bold text-blue-800 mb-6 mt-6 text-left">
          {isMyAPis ? "My APIs" : "Browse APIs"}
        </h2>
          <div className="grid grid-cols-[repeat(auto-fit,minmax(700px,1fr))] gap-6">
            {apis.map((api) => (
              <ApiListing
                key={api.id}
                api={api}
                isMyApis={isMyAPis}
                onDelete={handleDelete}
              />
            ))}
          </div>
      </div>
    </FetchStatus>

  );
};

export default ApiListings;
