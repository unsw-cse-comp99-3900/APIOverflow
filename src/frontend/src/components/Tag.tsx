import React from "react";
import { Link } from "react-router-dom";
import { useSelectedTags } from "../contexts/SelectedTagsContext";

interface TagProps {
  tag: string;
  className?: string;
}

const Tag: React.FC<TagProps> = ({ tag, className }) => {
  const { setTags } = useSelectedTags(); // Use the custom hook
  return (
    <Link to={`/apis`} className={className} onClick={ () => {
      setTags([tag]);
    }}>
      <span
        className={`bg-blue-800 hover:bg-amber-200 text-white hover:text-black text-sm font-semibold px-3 py-1 rounded-md cursor-pointer`}
      >
        {tag}
      </span>
    </Link>
  );
};

export default Tag;
