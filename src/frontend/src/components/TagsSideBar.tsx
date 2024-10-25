import React, { useEffect, useState } from "react";
import { Tag } from "../types/miscTypes";
import { FaCheckSquare, FaRegSquare } from "react-icons/fa";
import { getTags } from "../services/apiServices";

interface TagsSideBarProps {
  selectedTags: string[];
  setSelectedTags: React.Dispatch<React.SetStateAction<string[]>>;
}

const TagsSideBar: React.FC<TagsSideBarProps> = ({
  selectedTags,
  setSelectedTags,
}) => {
  const [tags, setTags] = useState<Tag[]>([]);

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

  const toggleTag = (tag: Tag) => {
    setSelectedTags((prevSelected) =>
      prevSelected.includes(tag)
        ? prevSelected.filter((prevTag) => prevTag !== tag)
        : [...prevSelected, tag]
    );
  };

  return (
    <aside className="fixed left-0 w-80 h-full px-4 py-8 overflow-y-auto bg-white border-r dark:bg-gray-900 dark:border-gray-700">
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

export default TagsSideBar;
