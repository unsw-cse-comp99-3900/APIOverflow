import React, { useEffect, useState } from "react";
import { Tag, CustomTag } from "../types/miscTypes";
import { FaCheckSquare, FaRegSquare } from "react-icons/fa";
import { getCustomTags, getTags } from "../services/apiServices";
import { useSelectedTags } from "../contexts/SelectedTagsContext";
import { toast } from "react-toastify";

const TagsSideBar: React.FC = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const { selectedTags, toggleTag, clearTags } = useSelectedTags();
  const [cTags, setCTags] = useState<CustomTag[]>([]);
  const [cTagsDisplayed, setCTagsDisplayed] = useState<CustomTag[]>([]);
  const [displayAllCTags, setDisplayAllCTags] = useState<boolean>(false);

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = await getTags(true);
        setTags(data);
        
        const cData = await getCustomTags();
        setCTags(cData);
        setCTagsDisplayed(cData.slice(0, 10));
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchApis();
  }, []);

  useEffect(() => {
    if (displayAllCTags) {
      setCTagsDisplayed(cTags);
    } else {
      setCTagsDisplayed(cTags.slice(0, 10));
    }
  }, [displayAllCTags]);

  const toggleDisplayAllCTags = () => {
    setDisplayAllCTags(!displayAllCTags);
  };

  const tagIcon = ({ tag }: { tag: string }) =>
    selectedTags.includes(tag) ? (
      <FaCheckSquare className="mr-2" />
    ) : (
      <FaRegSquare className="mr-2" />
    );

  return (
    <aside className="fixed left-0 w-80 h-full px-4 py-8 pb-32 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700">
      <div className="flex justify-between items-center px-4">
        <h4 className="font-bold text-2xl text-gray-800 dark:text-gray-200">
          Filter by Tags
        </h4>
        <button className="text-blue-600 hover:underline" onClick={clearTags}>
          Reset
        </button>
      </div>
      <div className="border border-gray-100 mb-5 mt-5"></div>
      <div>
        <h4 className="font-bold text-1xl text-gray-800 dark:text-gray-200 ml-4">
          System Tags
        </h4>
      </div>
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

      <div className="border border-gray-100 mb-5 mt-5"></div>
      <div>
        <h4 className="font-bold text-1xl text-gray-800 dark:text-gray-200 ml-4">
          Trending Tags
        </h4>
      </div>
      <div className="grid grid-cols-1 gap-1">
        {cTagsDisplayed.map((tagInfo) => (
          <span
            key={tagInfo.tag}
            className="flex items-center px-4 py-2 text-gray-900 bg-white rounded-lg dark:bg-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 group mt-3 hover:cursor-pointer"
            onClick={() => toggleTag(tagInfo.tag)}
          >
            <span className="ml-3 font-medium flex items-center">
              {tagIcon({ tag: tagInfo.tag })}
              {tagInfo.tag} ({tagInfo.num})
            </span>
          </span>
        ))}

        {cTags.length > 10 && (
          <div
            className="text-blue-500 font-semibold underline mb-5 mt-5 text-center cursor-pointer hover:text-indigo-600"
            onClick={() => toggleDisplayAllCTags()}
          >
            Show {displayAllCTags ? "Less" : "More"}
          </div>
        )}
      </div>
    </aside>
  );
};

export default TagsSideBar;
