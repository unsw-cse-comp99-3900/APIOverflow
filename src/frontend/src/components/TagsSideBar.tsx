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
  const [cTagsNum, setCTagsNum] = useState<number>(0);
  const [displayNum, setDisplayNum] = useState<number>(0);
  const [displayAll, setDisplayAll] = useState<boolean>(false);

  let displayNum_c = 0;
  let cTagsNum_c = 0;

  useEffect(() => {
    const fetchApis = async () => {
      try {
        const data = await getTags(true);
        setTags(data);

        const cData = await getCustomTags();
        setCTags(cData);
        setCTagsNum(cData.length);


        // Determine how many tags should be shown
        if (cData.length > 10) {
          console.log("Ran here");
          setDisplayNum(10);
          displayNum_c = 10;

        } else {
          console.log("Ran there");
          setDisplayNum(cData.length);
          displayNum_c = cData.length;
        };
        // toast.error(`Display Num: ${displayNum} | Tags: ${cTagsNum} | CData ${cData.length}`);
      } catch (error) {
        console.error("Error fetching data:", error);
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

  const toggleDisplayAll = () => {
    setDisplayAll(!displayAll);
  };
  console.log(`Display Num: ${displayNum_c} | Tags: ${cTagsNum_c}`);
  return (
    <aside className="fixed left-0 w-80 h-full px-4 py-8 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700">
      <div className="flex justify-between items-center px-4">
        <h4 className="font-bold text-2xl text-gray-800 dark:text-gray-200 ml-1">
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
      <div>
        <h4 className="font-bold text-1xl text-gray-800 dark:text-gray-200 ml-1">
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
      <div className="mb-5 mt-5"></div>
      <div>
        <h4 className="font-bold text-1xl text-gray-800 dark:text-gray-200 ml-1">
          Trending Tags
        </h4>
      </div>
      <div className="grid grid-cols-1 gap-1">
        {cTags.slice(displayNum_c).map((tagInfo) => (
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
        {displayAll === true && (
                <div className="grid grid-cols-1 gap-1">
                {cTags.slice(displayNum_c, cTagsNum_c).map((tagInfo) => (
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
                </div>
        )}
      </div>
      <div className="mb-5 mt-5"></div>
      <div>
        {/* Conditionally render if more than 10 custom tags */}
        {cTagsNum_c > 10 && (
            <div className="flex justify-end">
              <button className="text-white px-1 py-2 font-semibold bg-blue-500 rounded-lg hover:bg-blue-800 hover:cursor-pointer mt-3"
                onClick={toggleDisplayAll}>
                {`${displayAll
                  ? "Show less"
                  : "Show all"
                  }`}
              </button>
            </div>
          )}
      </div>


    </aside>
  );
};

export default TagsSideBar;
