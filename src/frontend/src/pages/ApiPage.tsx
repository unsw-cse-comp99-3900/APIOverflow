import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { DetailedApi } from "../types/apiTypes";
import { apiGetIcon, getApi } from "../services/apiServices";
import FetchStatus from "../components/FetchStatus";
import Tag from "../components/Tag";
import ApiReviews from "../components/ApiReviews";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import ApiDescription from "../components/ApiDescription";
import ApiDocs from "../components/ApiDocs";
import BackButton from "../components/BackButton";

const ApiPage: React.FC = () => {
  const [api, setApi] = useState<DetailedApi | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [iconURL, setIconURL] = useState<string>("")
  const { id } = useParams();
  

  useEffect(() => {
    const fetchApi = async () => {
      if (!id) {
        setError("Invalid API ID");
        setLoading(false);
        return;
      }
      try {
        const data = await getApi(id);
        const iconURL = await apiGetIcon(id)
        setApi(data);
        setIconURL(iconURL)
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

    fetchApi();

    // Cleanup the object URL to avoid memory leaks
    return () => {
      if (iconURL) {
        URL.revokeObjectURL(iconURL);
      }
    };
  }, [id]);

  return (
    <>
      {/* Main Layout */}
      <BackButton toUrl="/apis" />
        <FetchStatus loading={loading} error={error} data={api}>
          {api && (
            <div className="px-10">
              <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
                <div className="flex items-center">
                  {/* Placeholder for API icon */}
                  <div className="flex flex-shrink-0 items-center">
                    <img
                      className="w-56 h-56 rounded-full object-cover mx-auto border-2 border-gray-300"
                      src={iconURL || defaultApiIcon}
                      alt="API Icon"
                    />
                  </div>
                  <div className="ml-10 w-full">
                    <h1 className="text-4xl font-bold mb-5">{api.name}</h1>
                    <div className="border border-gray-100 w-full mb-5"></div>
                    <div className="flex flex-wrap max-w-3xl mt-4 mb-5">
                      {api.tags.map((tag, index) => (
                        <Tag key={index} tag={tag} className="mr-3 mb-2" />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex mx-auto max-w-[100rem] mt-10 space-x-10">
                <ApiReviews />
                <ApiDescription api={api} />
                <ApiDocs doc_ids = {api.docs}/>
              </div>
            </div>
          )}
        </FetchStatus>
    </>
  );
};

export default ApiPage;
