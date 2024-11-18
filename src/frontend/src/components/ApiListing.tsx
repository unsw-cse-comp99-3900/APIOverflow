import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { BriefApi } from "../types/apiTypes";
import defaultApiIcon from "../assets/images/defaultApiIcon.jpg";
import Tag from "./Tag";
import DeleteApiButton from "./DeleteApiButton";
import EditApiButton from "./EditApiButton";
import { apiGetIcon } from "../services/apiServices";
import { FaCrown } from "react-icons/fa";

interface ApiListingProps {
  api: BriefApi;
  isMyApis: boolean;
  onDelete: (id: string) => void;
}

const ApiListing: React.FC<ApiListingProps> = ({ api, isMyApis, onDelete }) => {
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [iconURL, setIconURL] = useState<string>("");

  console.log(api);
  const bgColor = {
    Free: "bg-blue-500",
    Freemium: "bg-purple-500",
    Premium: "bg-amber-500",
  };

  useEffect(() => {
    const fetchIcon = async () => {
      try {
        const iconURL = await apiGetIcon(api.id);
        setIconURL(iconURL);
      } catch (error) {
        console.log(error);
      }
    };
    fetchIcon();

    // Cleanup the object URL to avoid memory leaks
    return () => {
      if (iconURL) {
        URL.revokeObjectURL(iconURL);
      }
    };
  }, []);
  let description = api.description;

  if (!showFullDescription && description.length > 90) {
    description = description.substring(0, 90) + "...";
  }

  return (
    <div className="bg-white rounded-xl shadow-md relative transition-transform transform hover:scale-105">
      <div className="p-4">
        <div className="pb-16">
          <div className="flex items-start mb-2">
            <img
              src={iconURL || defaultApiIcon}
              alt="API Icon"
              className="w-20 h-20 ml-4 mr-4 mt-2 rounded-full object-cover border-2 border-gray-300"
            />

            <div>
              <div className="flex items-center">
                <h3 className="text-xl font-bold my-2">{api.name}</h3>
                <div
                  className={`flex items-center ${
                    bgColor[api.payModel]
                  } rounded-md mx-3 px-2`}
                >
                  {(api.payModel === "Premium" ||
                    api.payModel === "Freemium") && (
                    <div className="flex items-center justify-center text-md text-white rounded-md mr-2">
                      <FaCrown />
                    </div>
                  )}

                  <span className="text-white text-md font-medium">
                    {api.payModel}
                  </span>
                </div>
              </div>
              <div className="text-gray-600">{`By: ${api.owner}`}</div>
              <div className="flex flex-wrap mt-4 mb-3">
                {api.tags.map((tag) => (
                  <Tag key={tag} tag={tag} className="mr-3 mb-2" />
                ))}
              </div>
            </div>
          </div>

          <div className="border border-gray-100 mx-4 mb-5"></div>

          <div className="mx-4 mb-2 text-justify break-words text-gray-700 ">
            {description}
          </div>

          {description.length > 90 && (
            <button
              onClick={() => setShowFullDescription((prevState) => !prevState)}
              className="text-indigo-500 hover:text-indigo-600 underline font-semibold ml-4"
            >
              {showFullDescription ? "Less" : "More"}
            </button>
          )}
        </div>

        {isMyApis && (
          <div className="absolute top-8 right-8 flex space-x-2">
            <EditApiButton apiId={api.id} />
            <DeleteApiButton apiId={api.id} onDelete={onDelete} />
          </div>
        )}

        <div className="absolute bottom-8 right-8">
          <Link
            to={isMyApis ? `/profile/my-apis/${api.id}` : `/apis/${api.id}`}
            className="h-[36px] border-blue-800 border-2 bg-blue-800 hover:bg-white text-white hover:text-blue-800 font-bold hover:underline px-4 py-2 rounded-lg text-center text-sm"
          >
            Read More
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ApiListing;
