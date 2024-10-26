import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { DetailedApi } from "../types/apiTypes";
import { getApi } from "../services/apiServices";
import FetchStatus from "../components/FetchStatus";
import Tag from "../components/Tag";
import EditApiButton from "../components/EditApiButton";
import DeleteApiButton from "../components/DeleteApiButton";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import ApiReviews from "../components/ApiReviews";
import ApiDescription from "../components/ApiDescription";
import ApiDocs from "../components/ApiDocs";
import BackButton from "../components/BackButton";

const MyApiPage: React.FC = () => {
  const [api, setApi] = useState<DetailedApi | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchApi = async () => {
      try {
        const data = await getApi(Number(id));
        setApi(data);
      } catch (error) {
        console.log("Error fetching data", error);
        setError("Failed to load API data");
        toast.error("Error loading API data");
      } finally {
        setLoading(false);
      }
    };

    fetchApi();
  }, [id]);

  return (
    <>
        <BackButton toUrl="/profile/my-apis" />
        {/* Use FetchStatus for loading and error handling */}
        <FetchStatus loading={loading} error={error} data={api}>
          {api && (
            <div className="px-10">
              {/* Header Section */}
              <div className="mx-auto max-w-[100rem] relative bg-white rounded-2xl shadow-lg p-10">
                <div className="flex items-center">
                  <div className="flex flex-shrink-0 items-center">
                    <img
                      className="w-56 h-56 rounded-full object-cover mx-auto"
                      src={api.iconUrl || defaultApiIcon}
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

                  {/* Conditionally render buttons if api is available */}
                  <div className="absolute top-8 right-8 flex space-x-2">
                    <EditApiButton apiId={api.id}/>
                    {api.id && (
                      <DeleteApiButton
                        apiId={api.id}
                        apisRoute="/profile/my-apis"
                      />
                    )}
                  </div>
                </div>
              </div>

              {/* Reviews, Description, Documentation */}
              <div className="flex mx-auto max-w-[100rem] mt-10 space-x-10">
                <ApiReviews />
                <ApiDescription api={api} />{" "}
                {/* Pass api only when it's not null */}
                <ApiDocs />
              </div>
            </div>
          )}
        </FetchStatus>
    </>
  );
};

export default MyApiPage;
