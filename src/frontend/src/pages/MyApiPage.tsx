import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { DetailedApi } from "../types/apiTypes";
import { apiGetIcon, getApi } from "../services/apiServices";
import FetchStatus from "../components/FetchStatus";
import ApiReviews from "../components/ApiReviews";
import ApiDescription from "../components/ApiDescription";
import BackButton from "../components/BackButton";
import EndpointAndDocumentation from "../components/VersionFields";
import ApiGeneralInfo from "../components/ApiGeneralInfo";

const MyApiPage: React.FC = () => {
  const [api, setApi] = useState<DetailedApi | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [iconURL, setIconURL] = useState<string>("");
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
        const iconURL = await apiGetIcon(id);
        setApi(data);
        console.log(data);
        setIconURL(iconURL);
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
      <BackButton toUrl="/profile/my-apis" />
      {/* Use FetchStatus for loading and error handling */}
      <FetchStatus loading={loading} error={error} data={api}>
        {api && (
          <div className="p-10">
            {/* Header Section */}
            <ApiGeneralInfo
              apiId={api.id}
              apiName={api.name}
              iconURL={iconURL}
              ownerName={api.owner.name}
              payModel={api.pay_model}
              tags={api.tags}
              isMyApi={true}
            />

            <div className="flex mx-auto max-w-[100rem] mt-10 space-x-10">
              <div className="w-2/3">
                <ApiDescription api={api} />
                <EndpointAndDocumentation versions={api.versions} />
              </div>
              <ApiReviews sid={api.id} />
            </div>
          </div>
        )}
      </FetchStatus>
    </>
  );
};

export default MyApiPage;
