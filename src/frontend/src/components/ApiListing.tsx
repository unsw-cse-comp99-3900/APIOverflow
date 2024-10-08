import { useState } from "react";
import { Link } from "react-router-dom";
import { Api } from "../types/apiTypes";
import Tag from "./Tag";
import DeleteApiButton from "./DeleteApiButton";
import EditApiButton from "./EditApiButton";

const ApiListing = ({
  api,
  isMyApis,
  onDelete,
}: {
  api: Api;
  isMyApis: boolean;
  onDelete: (id: number) => void;
}) => {
  const [showFullDescription, setShowFullDescription] = useState(false);

  let description = api.description;

  if (!showFullDescription && description.length > 90) {
    description = description.substring(0, 90) + "...";
  }

  return (
    <div className="bg-white rounded-xl shadow-md relative">
      <div className="p-4">
        <div className="pb-16">
          <div className="flex items-start mb-2">
            <img
              src={api.icon_url}
              alt="API Icon"
              className="w-20 h-20 ml-4 mr-4 mt-2 rounded-full object-cover"
            />

            <div>
              <h3 className="text-xl font-bold my-2">{api.name}</h3>
              <div className="text-gray-600">{api.owner}</div>
              <div className="flex flex-wrap mt-4 mb-3">
                {api?.tags?.map((tag, index) => (
                  <Tag key={index} tag={tag} className="mr-3 mb-2" />
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
            <EditApiButton />
            <DeleteApiButton apiId={api.id} onDelete={onDelete} />
          </div>
        )}

        <div className="absolute bottom-8 right-8">
          <Link
            to={isMyApis ? `/profile/myApis/${api.id}` : `/apis/${api.id}`}
            className="h-[36px] bg-blue-800 hover:bg-amber-200 text-white hover:text-black font-semibold hover:underline px-4 py-2 rounded-lg text-center text-sm"
          >
            Read More
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ApiListing;
