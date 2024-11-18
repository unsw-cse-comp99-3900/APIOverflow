import React, { useEffect, useState } from "react";
import { Tag } from "../types/miscTypes";
import { FaCheckSquare, FaRegSquare } from "react-icons/fa";
import { getTags } from "../services/apiServices";
import { useSelectedTags } from "../contexts/SelectedTagsContext";

const EndpointsSidebar: React.FC = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const { selectedTags, toggleTag, clearTags } = useSelectedTags();

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = await getTags();
        setTags(data);
      } catch (error) {
        console.log("Error fetching data", error);
      }
    };
    fetchApis();
  }, []);

  const tagIcon = ({ tag }: { tag: string }) =>
    selectedTags.includes(tag) ? (
      <FaCheckSquare className="mr-2" />
    ) : (
      <FaRegSquare className="mr-2" />
    );

  return (
    <aside className="fixed right-0 w-80 h-full px-4 py-8 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700">
      <div className="flex justify-between items-center px-4">
        <h4 className="font-bold text-gray-800 dark:text-gray-200 ml-3">
          Filter by Tags
        </h4>
        <button
          className="text-blue-600 hover:underline"
          onClick={clearTags}
        >
          Reset
        </button>
      </div>
      <div className="border border-gray-100 mb-5 mt-5"></div>
      <div className="grid grid-cols-1 gap-1">
        {tags.map((tag) => (
          <span
            key={tag}
            className="flex items-center px-4 py-2 text-gray-900 bg-white rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3 hover:cursor-pointer"
            onClick={() => toggleTag(tag)}
          >
            <span className="ml-3 font-medium flex items-center">
              {tagIcon({ tag })}
              {tag}
            </span>
          </span>
        ))}
      </div>
    </aside>
  );
};

export default EndpointsSidebar;
