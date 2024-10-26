import React, { useEffect, useState } from "react";
import { Tag } from "../types/miscTypes";
import { addTag, getTags } from "../services/apiServices";
import { FaPlus } from "react-icons/fa";

interface TagsOverlayProps {
  isOpen: boolean;
  onClose: () => void;
  selectedTags: string[];
  setSelectedTags: React.Dispatch<React.SetStateAction<string[]>>;
}

const TagsOverlay: React.FC<TagsOverlayProps> = ({
  isOpen,
  onClose,
  selectedTags,
  setSelectedTags,
}) => {
  // React hooks
  const [tags, setTags] = useState<Tag[]>([]);
  const [newTag, setNewTag] = useState<Tag>("");
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

  // Helper functions
  const tagClass = ({ tag }: { tag: string }) =>
    selectedTags.includes(tag)
      ? "relative border-blue-800 border-2 bg-blue-800 text-white  flex items-center justify-center rounded-md text-sm font-semibold px-3 py-1 mx-1 my-1"
      : "relative border-blue-800 border-2 bg-white hover:bg-blue-800 text-blue-800 hover:text-white flex items-center justify-center rounded-md text-sm font-semibold px-3 py-1 mx-1 my-1";

  const toggleTag = (tag: string) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((t) => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  // Event Handlers
  const handleAddClick = () => {
    if (newTag === "") return;
    setTags([...tags, newTag]);
    addTag({
      tag: newTag,
    });
    setSelectedTags([...selectedTags, newTag]);
    setNewTag("");
  };

  const handleResetTags = () => {
    setSelectedTags([]);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50">
      <div className="relative bg-white rounded-lg shadow-lg w-11/12 max-w-4xl p-6 overflow-y-auto max-h-[90vh]">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-gray-600 hover:text-gray-800 text-2xl font-bold"
        >
          &times;
        </button>

        {/* All Tags */}
        <div className="flex flex-wrap">
          <h2 className="text-2xl font-semibold text-blue-800 mb-3 mx-1">
            Tags
          </h2>
        </div>
        <div className="flex flex-wrap">
          {tags.map((tag) => (
            <button
              key={tag}
              type="button" // Prevent form submission
              onClick={() => toggleTag(tag)}
              className={tagClass({ tag })}
            >
              {tag}
            </button>
          ))}
        </div>

        <div className="w-full px-2 mt-32 rounded-full border-2 border-gray-200 flex justify-start items-center">
          <input
            type="text"
            placeholder="Can't find your tag? Add it here"
            className="w-full text-gray-700 focus:outline-none focus:ring-0 border-none rounded-full"
            onChange={(e) => setNewTag(e.target.value)} // Update state on change
          />
          <button
            type="button"
            className="bg-blue-800 text-white h-full rounded-full"
            onClick={handleAddClick}
          >
            <FaPlus className="text-lg m-1" />
          </button>
        </div>

        <button
          type="button"
          onClick={handleResetTags}
          className=" text-blue-500 text-md hover:underline my-2 mx-4"
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default TagsOverlay;
