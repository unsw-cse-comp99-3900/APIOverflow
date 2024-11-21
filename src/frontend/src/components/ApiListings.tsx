import { useState, useEffect } from "react";
import { BriefApi } from "../types/apiTypes";
import ApiListing from "./ApiListing";
import { getApis, getMyApis, searchApis } from "../services/apiServices";
import FetchStatus from "./FetchStatus";
import { useSelectedTags } from "../contexts/SelectedTagsContext";
import { FaSearch } from "react-icons/fa";

interface ApiListingsProps {
  isMyAPis: boolean;
}

const ApiListings: React.FC<ApiListingsProps> = ({
  isMyAPis,
}) => {
  const [apis, setApis] = useState<BriefApi[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const { selectedTags } = useSelectedTags();

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = isMyAPis ? await getMyApis() : await getApis(selectedTags);
        console.log(data)
        setApis(data);
      } catch (error) {
        console.log("Error fetching data", error);
        if (error instanceof Error && error.message === "Unauthorized") {
          setError("Unauthorized");
        } else {
          setError("Failed to load API data");
        }
      } finally {
        setLoading(false);
      }
    };

    if (!isSearching) {
      fetchApis();
    }
  }, [selectedTags, isMyAPis, isSearching]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) {
      setIsSearching(false);
      return;
    }

    setLoading(true);
    setError("");
    setIsSearching(true);

    try {
      const data = await searchApis(searchTerm);
      setApis(data);
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to fetch search results');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (deletedApiId: string) => {
    setApis((prevApis) => prevApis.filter((api) => api.id !== deletedApiId));
  };

  const clearSearch = () => {
    setSearchTerm("");
    setIsSearching(false);
  };

  return (
    <FetchStatus loading={loading} error={error} data={apis}>
      <div className="container-xl lg:container mx-auto p-10">
        {/* Search Section */}
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-3xl font-bold text-blue-800">
            {isMyAPis ? "My APIs" : "Browse APIs"}
          </h2>
          <div className="flex-1 max-w-md ml-8">
            <form onSubmit={handleSearch} className="relative">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search APIs..."
                className="w-full px-4 py-2 pr-12 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div className="absolute right-0 top-0 h-full flex items-center pr-3">
                {isSearching && searchTerm && (
                  <button
                    type="button"
                    onClick={clearSearch}
                    className="text-gray-400 hover:text-gray-600 mr-2"
                  >
                    ×
                  </button>
                )}
                <button
                  type="submit"
                  className="text-gray-400 hover:text-gray-600"
                >
                  <FaSearch className="w-4 h-4" />
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Results count when searching */}
        {isSearching && (
          <div className="mb-4 text-gray-600">
            Found {apis.length} result{apis.length !== 1 ? 's' : ''} for "{searchTerm}"
          </div>
        )}

        {/* API Listings */}
        <div className="grid grid-cols-1 gap-6">
          {apis.map((api) => (
            <ApiListing
              key={api.id}
              api={api}
              isMyApis={isMyAPis}
              onDelete={handleDelete}
            />
          ))}
          {apis.length === 0 && isSearching && (
            <div className="text-center text-gray-500 py-8">
              No APIs found matching "{searchTerm}"
            </div>
          )}
        </div>
      </div>
    </FetchStatus>
  );
};

export default ApiListings;