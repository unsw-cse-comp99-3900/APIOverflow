import { useState, useEffect } from "react";
import { BriefApi } from "../types/apiTypes";
import ApiListing from "./ApiListing";
import { getApis, getMyApis } from "../services/apiServices";
import FetchStatus from "./FetchStatus";
import { useSelectedTags } from "../contexts/SelectedTagsContext";

interface ApiListingsProps {
  isMyAPis: boolean;
}

const ApiListings: React.FC<ApiListingsProps> = ({
  isMyAPis,
}) => {
  const [apis, setApis] = useState<BriefApi[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { selectedTags} = useSelectedTags();

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = isMyAPis ? await getMyApis() : await getApis(selectedTags);
        setApis(data);
      } catch (error) {
        console.log("Error fetching data", error);
        setError("Failed to load API data");
      } finally {
        setLoading(false);
      }
    };

    fetchApis();
  }, [selectedTags, isMyAPis]);

  const handleDelete = (deletedApiId: string) => {
    setApis((prevApis) => prevApis.filter((api) => api.id !== deletedApiId));
  };

  return (
    <FetchStatus loading={loading} error={error} data={apis}>
      <div className="container-xl lg:container mx-auto p-10">
        <h2 className="text-3xl font-bold text-blue-800 mb-6 mt-6 text-left">
          {isMyAPis ? "My APIs" : "Browse APIs"}
        </h2>
        <div className="grid grid-cols-1 gap-6">
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
